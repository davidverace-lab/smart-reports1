"""
Smart Reports - Database Manager Instituto
Gestor de base de datos MySQL para tngcore con prefijo instituto_
"""

import mysql.connector
from mysql.connector import Error, pooling
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import json
import hashlib
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Configuración de la base de datos tngcore"""

    def __init__(self, host='localhost', database='tngcore',
                 user='root', password='', port=3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    def get_config(self) -> Dict:
        """Retorna configuración como diccionario"""
        return {
            'host': self.host,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': False,
            'raise_on_warnings': True
        }


class DatabaseManager:
    """Gestor principal de base de datos"""

    # Prefijo de tablas
    TABLE_PREFIX = 'instituto_'

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection_pool = None
        self._create_connection_pool()

    def _create_connection_pool(self):
        """Crea un pool de conexiones"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="instituto_pool",
                pool_size=5,
                pool_reset_session=True,
                **self.config.get_config()
            )
            logger.info(f"✅ Connection pool created successfully for {self.config.database}")
        except Error as e:
            logger.error(f"❌ Error creating connection pool: {e}")
            raise

    def get_connection(self):
        """Obtiene una conexión del pool"""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"❌ Error getting connection: {e}")
            raise

    def execute_query(self, query: str, params: Tuple = None,
                      fetch_one=False, fetch_all=False, commit=False) -> Any:
        """Ejecuta una query SQL"""
        connection = None
        cursor = None
        result = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, params or ())

            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            elif commit:
                connection.commit()
                result = cursor.lastrowid or cursor.rowcount

            return result

        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"❌ Error executing query: {e}")
            logger.error(f"   Query: {query}")
            logger.error(f"   Params: {params}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_many(self, query: str, data: List[Tuple]) -> int:
        """Ejecuta múltiples inserciones en batch"""
        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.executemany(query, data)
            connection.commit()

            rowcount = cursor.rowcount
            logger.info(f"✅ Inserted {rowcount} rows")
            return rowcount

        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"❌ Error executing batch insert: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


# =============================================================================
# MANAGERS ESPECÍFICOS CON PREFIJO instituto_
# =============================================================================

class UsuarioManager:
    """Gestor de operaciones de Usuario"""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.table = f"{db.TABLE_PREFIX}Usuario"

    def crear_usuario(self, user_data: Dict) -> int:
        """Crea un nuevo usuario"""
        query = f"""
            INSERT INTO {self.table} (
                UserId, IdUnidadDeNegocio, IdDepartamento, IdRol,
                NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo,
                Nivel, Division, Position, UserStatus, Grupo, Ubicacion
            ) VALUES (
                %(UserId)s, %(IdUnidadDeNegocio)s, %(IdDepartamento)s, %(IdRol)s,
                %(NombreCompleto)s, %(UserEmail)s, %(PasswordHash)s, %(TipoDeCorreo)s,
                %(Nivel)s, %(Division)s, %(Position)s, %(UserStatus)s, %(Grupo)s, %(Ubicacion)s
            )
        """

        if 'Password' in user_data and 'PasswordHash' not in user_data:
            user_data['PasswordHash'] = self._hash_password(user_data['Password'])

        usuario_id = self.db.execute_query(query, user_data, commit=True)
        logger.info(f"✅ Usuario creado: {user_data.get('UserId')} (ID: {usuario_id})")
        return usuario_id

    def obtener_usuario(self, user_id: str) -> Optional[Dict]:
        """Obtiene un usuario por UserId"""
        query = f"""
            SELECT u.*, un.NombreUnidad, d.NombreDepartamento, r.NombreRol
            FROM {self.table} u
            LEFT JOIN {self.db.TABLE_PREFIX}UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN {self.db.TABLE_PREFIX}Departamento d ON u.IdDepartamento = d.IdDepartamento
            LEFT JOIN {self.db.TABLE_PREFIX}Rol r ON u.IdRol = r.IdRol
            WHERE u.UserId = %s AND u.Activo = 1
        """
        return self.db.execute_query(query, (user_id,), fetch_one=True)

    def listar_usuarios(self, filtros: Dict = None) -> List[Dict]:
        """Lista usuarios con filtros opcionales"""
        query = f"""
            SELECT u.*, un.NombreUnidad, d.NombreDepartamento, r.NombreRol
            FROM {self.table} u
            LEFT JOIN {self.db.TABLE_PREFIX}UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN {self.db.TABLE_PREFIX}Departamento d ON u.IdDepartamento = d.IdDepartamento
            LEFT JOIN {self.db.TABLE_PREFIX}Rol r ON u.IdRol = r.IdRol
            WHERE u.Activo = 1
        """

        params = []
        if filtros:
            if 'IdUnidadDeNegocio' in filtros:
                query += " AND u.IdUnidadDeNegocio = %s"
                params.append(filtros['IdUnidadDeNegocio'])
            if 'IdDepartamento' in filtros:
                query += " AND u.IdDepartamento = %s"
                params.append(filtros['IdDepartamento'])

        query += " ORDER BY u.NombreCompleto"
        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)

    def _hash_password(self, password: str) -> str:
        """Genera hash de password"""
        return hashlib.sha256(password.encode()).hexdigest()


class ModuloManager:
    """Gestor de operaciones de Módulo"""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.table = f"{db.TABLE_PREFIX}Modulo"

    def crear_modulo(self, modulo_data: Dict) -> int:
        """Crea un nuevo módulo"""
        query = f"""
            INSERT INTO {self.table} (
                NombreModulo, FechaInicioModulo, FechaCierre, Descripcion,
                DuracionEstimadaHoras, CategoriaModulo, IdCreador
            ) VALUES (
                %(NombreModulo)s, %(FechaInicioModulo)s, %(FechaCierre)s, %(Descripcion)s,
                %(DuracionEstimadaHoras)s, %(CategoriaModulo)s, %(IdCreador)s
            )
        """

        modulo_id = self.db.execute_query(query, modulo_data, commit=True)
        logger.info(f"✅ Módulo creado: {modulo_data.get('NombreModulo')} (ID: {modulo_id})")
        return modulo_id

    def listar_modulos(self, activos_solo=True) -> List[Dict]:
        """Lista módulos"""
        query = f"SELECT * FROM {self.table} WHERE 1=1"

        if activos_solo:
            query += " AND Activo = 1"

        query += " ORDER BY FechaInicioModulo DESC"
        return self.db.execute_query(query, fetch_all=True)

    def asignar_a_departamento(self, id_modulo: int, id_departamento: int,
                               obligatorio: bool = False,
                               fecha_vencimiento: datetime = None) -> int:
        """Asigna un módulo a un departamento"""
        query = f"""
            INSERT INTO {self.db.TABLE_PREFIX}ModuloDepartamento (
                IdModulo, IdDepartamento, Obligatorio, FechaAsignacion, FechaVencimiento
            ) VALUES (%s, %s, %s, NOW(), %s)
        """

        asignacion_id = self.db.execute_query(
            query,
            (id_modulo, id_departamento, obligatorio, fecha_vencimiento),
            commit=True
        )

        logger.info(f"✅ Módulo {id_modulo} asignado a departamento {id_departamento}")

        if obligatorio:
            self._asignar_a_usuarios_departamento(id_modulo, id_departamento, fecha_vencimiento)

        return asignacion_id

    def _asignar_a_usuarios_departamento(self, id_modulo: int, id_departamento: int,
                                          fecha_vencimiento: datetime):
        """Asigna módulo a todos los usuarios de un departamento"""
        query_usuarios = f"""
            SELECT UserId FROM {self.db.TABLE_PREFIX}Usuario
            WHERE IdDepartamento = %s AND Activo = 1
        """

        usuarios = self.db.execute_query(query_usuarios, (id_departamento,), fetch_all=True)

        if not usuarios:
            logger.info(f"⚠️ No hay usuarios en departamento {id_departamento}")
            return

        query_insert = f"""
            INSERT IGNORE INTO {self.db.TABLE_PREFIX}ProgresoModulo
            (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento)
            VALUES (%s, %s, 'No iniciado', NOW(), %s)
        """

        data = [(u['UserId'], id_modulo, fecha_vencimiento) for u in usuarios]
        rows = self.db.execute_many(query_insert, data)

        logger.info(f"✅ Módulo asignado a {rows} usuarios del departamento")


class ProgresoManager:
    """Gestor de operaciones de Progreso de Módulos"""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.table = f"{db.TABLE_PREFIX}ProgresoModulo"

    def obtener_progreso_usuario(self, user_id: str) -> List[Dict]:
        """Obtiene el progreso de un usuario"""
        query = f"""
            SELECT p.*, m.NombreModulo, m.CategoriaModulo
            FROM {self.table} p
            JOIN {self.db.TABLE_PREFIX}Modulo m ON p.IdModulo = m.IdModulo
            WHERE p.UserId = %s
            ORDER BY p.FechaAsignacion DESC
        """

        return self.db.execute_query(query, (user_id,), fetch_all=True)

    def actualizar_progreso(self, id_inscripcion: int, estatus: str,
                           porcentaje: float, comentario: str = None) -> bool:
        """Actualiza el progreso usando procedimiento almacenado"""
        query = "CALL sp_instituto_ActualizarProgreso(%s, %s, %s, %s)"

        self.db.execute_query(
            query,
            (id_inscripcion, estatus, porcentaje, comentario),
            commit=True
        )

        logger.info(f"✅ Progreso actualizado: {id_inscripcion} -> {estatus} ({porcentaje}%)")
        return True


class ReporteManager:
    """Gestor de operaciones de Reportes"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def reporte_cumplimiento_unidad(self, id_unidad: int = None) -> List[Dict]:
        """Genera reporte de cumplimiento por unidad de negocio"""
        query = f"""
            SELECT
                un.NombreUnidad,
                d.NombreDepartamento,
                COUNT(DISTINCT p.IdInscripcion) as TotalAsignaciones,
                SUM(CASE WHEN p.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as Completados,
                SUM(CASE WHEN p.EstatusModulo = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                SUM(CASE WHEN p.FechaVencimiento < NOW() AND p.EstatusModulo != 'Completado' THEN 1 ELSE 0 END) as Vencidos,
                ROUND(SUM(CASE WHEN p.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as PorcentajeCumplimiento
            FROM {self.db.TABLE_PREFIX}UnidadDeNegocio un
            JOIN {self.db.TABLE_PREFIX}Departamento d ON un.IdUnidadDeNegocio = d.IdUnidadDeNegocio
            JOIN {self.db.TABLE_PREFIX}Usuario u ON d.IdDepartamento = u.IdDepartamento
            JOIN {self.db.TABLE_PREFIX}ProgresoModulo p ON u.UserId = p.UserId
            WHERE un.Activo = 1
        """

        params = []
        if id_unidad:
            query += " AND un.IdUnidadDeNegocio = %s"
            params.append(id_unidad)

        query += " GROUP BY un.IdUnidadDeNegocio, d.IdDepartamento"

        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)


# =============================================================================
# CLASE PRINCIPAL UNIFICADA
# =============================================================================

class InstitutoSmartReportsDB:
    """Clase principal para base de datos tngcore con prefijo instituto_"""

    def __init__(self, config: DatabaseConfig):
        self.db = DatabaseManager(config)
        self.usuarios = UsuarioManager(self.db)
        self.modulos = ModuloManager(self.db)
        self.progreso = ProgresoManager(self.db)
        self.reportes = ReporteManager(self.db)

    def close(self):
        """Cierra el pool de conexiones"""
        if self.db.connection_pool:
            logger.info("✅ Database manager closed")


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    # Configuración para tngcore
    config = DatabaseConfig(
        host='localhost',
        database='tngcore',
        user='root',
        password='',  # Cambiar según tu configuración
        port=3306
    )

    # Inicializar sistema
    db_system = InstitutoSmartReportsDB(config)

    print("=" * 60)
    print("INSTITUTO SMART REPORTS - DATABASE MANAGER")
    print("Base de datos: tngcore")
    print("Prefijo de tablas: instituto_")
    print("=" * 60)

    try:
        # Ejemplo: Listar unidades de negocio
        print("\n📊 Consultando unidades de negocio...")
        query = "SELECT * FROM instituto_UnidadDeNegocio WHERE Activo = 1"
        unidades = db_system.db.execute_query(query, fetch_all=True)

        if unidades:
            print(f"✅ Encontradas {len(unidades)} unidades de negocio:")
            for unidad in unidades:
                print(f"   - {unidad['NombreUnidad']} ({unidad['Codigo']})")
        else:
            print("⚠️ No hay unidades de negocio registradas")

        # Ejemplo: Listar módulos
        print("\n📚 Consultando módulos...")
        modulos = db_system.modulos.listar_modulos()

        if modulos:
            print(f"✅ Encontrados {len(modulos)} módulos:")
            for modulo in modulos[:5]:
                print(f"   - {modulo['NombreModulo']}")
        else:
            print("⚠️ No hay módulos registrados")

        print("\n" + "=" * 60)
        print("✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db_system.close()
