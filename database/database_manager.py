"""
Smart Reports - Database Manager
Sistema de gestión de base de datos MySQL para módulos de capacitación
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
    """Configuración de la base de datos"""

    def __init__(self, host='localhost', database='SmartReportsDB',
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

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection_pool = None
        self._create_connection_pool()

    def _create_connection_pool(self):
        """Crea un pool de conexiones"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="smartreports_pool",
                pool_size=5,
                pool_reset_session=True,
                **self.config.get_config()
            )
            logger.info("✅ Connection pool created successfully")
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
        """
        Ejecuta una query SQL

        Args:
            query: Query SQL a ejecutar
            params: Parámetros para la query (tupla)
            fetch_one: Si retorna un solo resultado
            fetch_all: Si retorna todos los resultados
            commit: Si hace commit de la transacción

        Returns:
            Resultados según parámetros
        """
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
        """
        Ejecuta múltiples inserciones en batch

        Args:
            query: Query de inserción
            data: Lista de tuplas con datos

        Returns:
            Número de filas afectadas
        """
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
# MANAGERS ESPECÍFICOS POR ENTIDAD
# =============================================================================

class UsuarioManager:
    """Gestor de operaciones de Usuario"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def crear_usuario(self, user_data: Dict) -> int:
        """
        Crea un nuevo usuario

        Args:
            user_data: Diccionario con datos del usuario

        Returns:
            ID del usuario creado
        """
        query = """
            INSERT INTO Usuario (
                UserId, IdUnidadDeNegocio, IdDepartamento, IdRol,
                NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo,
                Nivel, Division, Position, UserStatus, Grupo, Ubicacion
            ) VALUES (
                %(UserId)s, %(IdUnidadDeNegocio)s, %(IdDepartamento)s, %(IdRol)s,
                %(NombreCompleto)s, %(UserEmail)s, %(PasswordHash)s, %(TipoDeCorreo)s,
                %(Nivel)s, %(Division)s, %(Position)s, %(UserStatus)s, %(Grupo)s, %(Ubicacion)s
            )
        """

        # Hash de password si viene en texto plano
        if 'Password' in user_data and 'PasswordHash' not in user_data:
            user_data['PasswordHash'] = self._hash_password(user_data['Password'])

        usuario_id = self.db.execute_query(query, user_data, commit=True)
        logger.info(f"✅ Usuario creado: {user_data.get('UserId')} (ID: {usuario_id})")
        return usuario_id

    def obtener_usuario(self, user_id: str) -> Optional[Dict]:
        """Obtiene un usuario por UserId"""
        query = """
            SELECT u.*, un.NombreUnidad, d.NombreDepartamento, r.NombreRol
            FROM Usuario u
            LEFT JOIN UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN Departamento d ON u.IdDepartamento = d.IdDepartamento
            LEFT JOIN Rol r ON u.IdRol = r.IdRol
            WHERE u.UserId = %s AND u.Activo = 1
        """
        return self.db.execute_query(query, (user_id,), fetch_one=True)

    def actualizar_usuario(self, user_id: str, datos: Dict) -> bool:
        """Actualiza datos de un usuario"""
        # Construir query dinámicamente según campos a actualizar
        campos = [f"{k} = %s" for k in datos.keys()]
        valores = list(datos.values())
        valores.append(user_id)

        query = f"""
            UPDATE Usuario
            SET {', '.join(campos)}
            WHERE UserId = %s
        """

        rows = self.db.execute_query(query, tuple(valores), commit=True)
        logger.info(f"✅ Usuario actualizado: {user_id}")
        return rows > 0

    def listar_usuarios(self, filtros: Dict = None) -> List[Dict]:
        """
        Lista usuarios con filtros opcionales

        Args:
            filtros: Diccionario con filtros (IdUnidadDeNegocio, IdDepartamento, UserStatus, etc.)

        Returns:
            Lista de usuarios
        """
        query = """
            SELECT u.*, un.NombreUnidad, d.NombreDepartamento, r.NombreRol
            FROM Usuario u
            LEFT JOIN UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
            LEFT JOIN Departamento d ON u.IdDepartamento = d.IdDepartamento
            LEFT JOIN Rol r ON u.IdRol = r.IdRol
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
            if 'UserStatus' in filtros:
                query += " AND u.UserStatus = %s"
                params.append(filtros['UserStatus'])

        query += " ORDER BY u.NombreCompleto"

        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)

    def validar_credenciales(self, user_id: str, password: str) -> Optional[Dict]:
        """Valida credenciales de usuario"""
        usuario = self.obtener_usuario(user_id)

        if usuario and self._verify_password(password, usuario['PasswordHash']):
            # Registrar acceso exitoso
            self._registrar_acceso(usuario['IdUsuario'], 'Login', True)
            return usuario
        else:
            # Registrar intento fallido
            if usuario:
                self._registrar_acceso(usuario['IdUsuario'], 'Login', False)
            return None

    def _hash_password(self, password: str) -> str:
        """Genera hash de password (usar bcrypt en producción)"""
        # NOTA: Esto es simplificado. En producción usar bcrypt
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica password contra hash"""
        return self._hash_password(password) == password_hash

    def _registrar_acceso(self, id_usuario: int, accion: str, exito: bool):
        """Registra en auditoría de acceso"""
        query = """
            INSERT INTO AuditoriaAcceso (IdUsuario, Accion, Exito)
            VALUES (%s, %s, %s)
        """
        self.db.execute_query(query, (id_usuario, accion, exito), commit=True)


class ModuloManager:
    """Gestor de operaciones de Módulo"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def crear_modulo(self, modulo_data: Dict) -> int:
        """Crea un nuevo módulo"""
        query = """
            INSERT INTO Modulo (
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

    def obtener_modulo(self, id_modulo: int) -> Optional[Dict]:
        """Obtiene un módulo por ID"""
        query = """
            SELECT m.*, u.NombreCompleto as NombreCreador
            FROM Modulo m
            LEFT JOIN Usuario u ON m.IdCreador = u.IdUsuario
            WHERE m.IdModulo = %s AND m.Activo = 1
        """
        return self.db.execute_query(query, (id_modulo,), fetch_one=True)

    def listar_modulos(self, activos_solo=True, categoria=None) -> List[Dict]:
        """Lista módulos con filtros opcionales"""
        query = "SELECT * FROM Modulo WHERE 1=1"
        params = []

        if activos_solo:
            query += " AND Activo = 1"

        if categoria:
            query += " AND CategoriaModulo = %s"
            params.append(categoria)

        query += " ORDER BY FechaInicioModulo DESC"

        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)

    def asignar_a_departamento(self, id_modulo: int, id_departamento: int,
                               obligatorio: bool = False,
                               fecha_vencimiento: datetime = None) -> int:
        """Asigna un módulo a un departamento"""
        query = """
            INSERT INTO ModuloDepartamento (
                IdModulo, IdDepartamento, Obligatorio, FechaAsignacion, FechaVencimiento
            ) VALUES (%s, %s, %s, NOW(), %s)
        """

        asignacion_id = self.db.execute_query(
            query,
            (id_modulo, id_departamento, obligatorio, fecha_vencimiento),
            commit=True
        )

        logger.info(f"✅ Módulo {id_modulo} asignado a departamento {id_departamento}")

        # Asignar automáticamente a usuarios del departamento
        if obligatorio:
            self._asignar_a_usuarios_departamento(id_modulo, id_departamento, fecha_vencimiento)

        return asignacion_id

    def _asignar_a_usuarios_departamento(self, id_modulo: int, id_departamento: int,
                                          fecha_vencimiento: datetime):
        """Asigna módulo a todos los usuarios de un departamento"""
        # Obtener usuarios del departamento
        query_usuarios = """
            SELECT UserId FROM Usuario
            WHERE IdDepartamento = %s AND Activo = 1
        """

        usuarios = self.db.execute_query(query_usuarios, (id_departamento,), fetch_all=True)

        if not usuarios:
            logger.info(f"⚠️ No hay usuarios en departamento {id_departamento}")
            return

        # Insertar progreso para cada usuario
        query_insert = """
            INSERT IGNORE INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento)
            VALUES (%s, %s, 'No iniciado', NOW(), %s)
        """

        data = [(u['UserId'], id_modulo, fecha_vencimiento) for u in usuarios]
        rows = self.db.execute_many(query_insert, data)

        logger.info(f"✅ Módulo asignado a {rows} usuarios del departamento")


class ProgresoManager:
    """Gestor de operaciones de Progreso de Módulos"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def obtener_progreso_usuario(self, user_id: str, id_modulo: int = None) -> List[Dict]:
        """
        Obtiene el progreso de un usuario

        Args:
            user_id: ID del usuario
            id_modulo: ID del módulo específico (opcional)

        Returns:
            Lista de progresos
        """
        query = """
            SELECT p.*, m.NombreModulo, m.CategoriaModulo, m.DuracionEstimadaHoras
            FROM ProgresoModulo p
            JOIN Modulo m ON p.IdModulo = m.IdModulo
            WHERE p.UserId = %s
        """

        params = [user_id]

        if id_modulo:
            query += " AND p.IdModulo = %s"
            params.append(id_modulo)

        query += " ORDER BY p.FechaAsignacion DESC"

        return self.db.execute_query(query, tuple(params), fetch_all=True)

    def actualizar_progreso(self, id_inscripcion: int, estatus: str,
                           porcentaje: float, comentario: str = None) -> bool:
        """Actualiza el progreso de un módulo usando procedimiento almacenado"""
        query = "CALL sp_ActualizarProgreso(%s, %s, %s, %s)"

        self.db.execute_query(
            query,
            (id_inscripcion, estatus, porcentaje, comentario),
            commit=True
        )

        logger.info(f"✅ Progreso actualizado: Inscripción {id_inscripcion} -> {estatus} ({porcentaje}%)")
        return True

    def obtener_modulos_vencidos(self, dias_anticipacion: int = 3) -> List[Dict]:
        """Obtiene módulos próximos a vencer"""
        query = """
            SELECT p.*, u.NombreCompleto, u.UserEmail, m.NombreModulo,
                   DATEDIFF(p.FechaVencimiento, NOW()) as DiasRestantes
            FROM ProgresoModulo p
            JOIN Usuario u ON p.UserId = u.UserId
            JOIN Modulo m ON p.IdModulo = m.IdModulo
            WHERE p.EstatusModulo != 'Completado'
              AND p.FechaVencimiento IS NOT NULL
              AND DATEDIFF(p.FechaVencimiento, NOW()) BETWEEN 0 AND %s
            ORDER BY p.FechaVencimiento ASC
        """

        return self.db.execute_query(query, (dias_anticipacion,), fetch_all=True)

    def obtener_historial(self, id_inscripcion: int) -> List[Dict]:
        """Obtiene el historial de cambios de un progreso"""
        query = """
            SELECT h.*, u.NombreCompleto as ModificadoPor
            FROM HistorialProgreso h
            LEFT JOIN Usuario u ON h.IdUsuarioModificador = u.IdUsuario
            WHERE h.IdInscripcion = %s
            ORDER BY h.FechaCambio DESC
        """

        return self.db.execute_query(query, (id_inscripcion,), fetch_all=True)


class EvaluacionManager:
    """Gestor de operaciones de Evaluaciones"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def crear_evaluacion(self, evaluacion_data: Dict) -> int:
        """Crea una nueva evaluación"""
        query = """
            INSERT INTO Evaluacion (
                IdModulo, NombreEvaluacion, Descripcion,
                PuntajeMinimoAprobatorio, PuntajeMaximo, IntentosPermitidos, TiempoLimiteMinutos
            ) VALUES (
                %(IdModulo)s, %(NombreEvaluacion)s, %(Descripcion)s,
                %(PuntajeMinimoAprobatorio)s, %(PuntajeMaximo)s, %(IntentosPermitidos)s, %(TiempoLimiteMinutos)s
            )
        """

        evaluacion_id = self.db.execute_query(query, evaluacion_data, commit=True)
        logger.info(f"✅ Evaluación creada: {evaluacion_data.get('NombreEvaluacion')} (ID: {evaluacion_id})")
        return evaluacion_id

    def registrar_resultado(self, id_inscripcion: int, id_evaluacion: int,
                           puntaje: float, intento: int) -> Dict:
        """Registra el resultado de una evaluación usando procedimiento almacenado"""
        query = "CALL sp_RegistrarResultadoEvaluacion(%s, %s, %s, %s)"

        result = self.db.execute_query(
            query,
            (id_inscripcion, id_evaluacion, puntaje, intento),
            fetch_one=True
        )

        logger.info(f"✅ Resultado registrado: Evaluación {id_evaluacion}, Puntaje: {puntaje}, Aprobado: {result.get('Aprobado')}")
        return result

    def obtener_resultados_usuario(self, user_id: str, id_modulo: int = None) -> List[Dict]:
        """Obtiene los resultados de evaluaciones de un usuario"""
        query = """
            SELECT re.*, e.NombreEvaluacion, e.PuntajeMinimoAprobatorio,
                   m.NombreModulo, p.IdInscripcion
            FROM ResultadoEvaluacion re
            JOIN ProgresoModulo p ON re.IdInscripcion = p.IdInscripcion
            JOIN Evaluacion e ON re.IdEvaluacion = e.IdEvaluacion
            JOIN Modulo m ON e.IdModulo = m.IdModulo
            WHERE p.UserId = %s
        """

        params = [user_id]

        if id_modulo:
            query += " AND m.IdModulo = %s"
            params.append(id_modulo)

        query += " ORDER BY re.FechaRealizacion DESC"

        return self.db.execute_query(query, tuple(params), fetch_all=True)


class ReporteManager:
    """Gestor de operaciones de Reportes"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def reporte_cumplimiento_unidad(self, id_unidad: int = None) -> List[Dict]:
        """Genera reporte de cumplimiento por unidad de negocio"""
        query = """
            SELECT
                un.NombreUnidad,
                d.NombreDepartamento,
                COUNT(DISTINCT p.IdInscripcion) as TotalAsignaciones,
                SUM(CASE WHEN p.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as Completados,
                SUM(CASE WHEN p.EstatusModulo = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                SUM(CASE WHEN p.FechaVencimiento < NOW() AND p.EstatusModulo != 'Completado' THEN 1 ELSE 0 END) as Vencidos,
                ROUND(SUM(CASE WHEN p.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as PorcentajeCumplimiento
            FROM UnidadDeNegocio un
            JOIN Departamento d ON un.IdUnidadDeNegocio = d.IdUnidadDeNegocio
            JOIN Usuario u ON d.IdDepartamento = u.IdDepartamento
            JOIN ProgresoModulo p ON u.UserId = p.UserId
            WHERE un.Activo = 1
        """

        params = []
        if id_unidad:
            query += " AND un.IdUnidadDeNegocio = %s"
            params.append(id_unidad)

        query += " GROUP BY un.IdUnidadDeNegocio, d.IdDepartamento ORDER BY un.NombreUnidad, d.NombreDepartamento"

        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)

    def reporte_evaluaciones(self, id_modulo: int = None) -> List[Dict]:
        """Genera reporte de estadísticas de evaluaciones"""
        query = "SELECT * FROM vw_EstadisticasEvaluaciones WHERE 1=1"

        params = []
        if id_modulo:
            query += " AND IdModulo = %s"
            params.append(id_modulo)

        return self.db.execute_query(query, tuple(params) if params else None, fetch_all=True)

    def guardar_reporte(self, id_usuario: int, nombre: str, tipo: str,
                       filtros: Dict, descripcion: str = None) -> int:
        """Guarda configuración de reporte"""
        query = """
            INSERT INTO ReporteGuardado (IdUsuarioCreador, NombreReporte, TipoReporte, Descripcion, FiltrosJSON)
            VALUES (%s, %s, %s, %s, %s)
        """

        reporte_id = self.db.execute_query(
            query,
            (id_usuario, nombre, tipo, descripcion, json.dumps(filtros)),
            commit=True
        )

        logger.info(f"✅ Reporte guardado: {nombre} (ID: {reporte_id})")
        return reporte_id

    def obtener_reportes_usuario(self, id_usuario: int) -> List[Dict]:
        """Obtiene reportes guardados de un usuario"""
        query = """
            SELECT * FROM ReporteGuardado
            WHERE IdUsuarioCreador = %s OR Compartido = 1
            ORDER BY FechaCreacion DESC
        """

        return self.db.execute_query(query, (id_usuario,), fetch_all=True)


# =============================================================================
# CLASE PRINCIPAL UNIFICADA
# =============================================================================

class SmartReportsDB:
    """Clase principal que unifica todos los managers"""

    def __init__(self, config: DatabaseConfig):
        self.db = DatabaseManager(config)
        self.usuarios = UsuarioManager(self.db)
        self.modulos = ModuloManager(self.db)
        self.progreso = ProgresoManager(self.db)
        self.evaluaciones = EvaluacionManager(self.db)
        self.reportes = ReporteManager(self.db)

    def close(self):
        """Cierra el pool de conexiones"""
        if self.db.connection_pool:
            # El pool se cierra automáticamente al terminar el programa
            logger.info("✅ Database manager closed")


# =============================================================================
# EJEMPLOS DE USO
# =============================================================================

if __name__ == "__main__":
    # Configuración
    config = DatabaseConfig(
        host='localhost',
        database='SmartReportsDB',
        user='root',
        password='',  # Cambiar según tu configuración
        port=3306
    )

    # Inicializar sistema
    db_system = SmartReportsDB(config)

    print("=" * 60)
    print("SMART REPORTS - DATABASE MANAGER")
    print("=" * 60)

    try:
        # EJEMPLO 1: Crear un usuario
        print("\n1. Creando usuario de ejemplo...")
        nuevo_usuario = {
            'UserId': 'jperez',
            'NombreCompleto': 'Juan Pérez',
            'UserEmail': 'juan.perez@hutchison.com',
            'Password': 'password123',  # Se hasheará automáticamente
            'IdUnidadDeNegocio': 1,
            'IdDepartamento': 1,
            'IdRol': 4,
            'UserStatus': 'Activo',
            'Nivel': 'Operativo',
            'Position': 'Operador'
        }

        user_id = db_system.usuarios.crear_usuario(nuevo_usuario)
        print(f"   ✅ Usuario creado con ID: {user_id}")

        # EJEMPLO 2: Listar usuarios de una unidad de negocio
        print("\n2. Listando usuarios de ICAVE...")
        usuarios = db_system.usuarios.listar_usuarios({'IdUnidadDeNegocio': 1})
        print(f"   ✅ Encontrados {len(usuarios)} usuarios")
        for u in usuarios[:3]:
            print(f"      - {u['NombreCompleto']} ({u['UserEmail']})")

        # EJEMPLO 3: Crear un módulo
        print("\n3. Creando módulo de capacitación...")
        nuevo_modulo = {
            'NombreModulo': 'Seguridad Industrial Básica',
            'FechaInicioModulo': datetime.now().date(),
            'FechaCierre': (datetime.now() + timedelta(days=30)).date(),
            'Descripcion': 'Curso básico de seguridad industrial',
            'DuracionEstimadaHoras': 8,
            'CategoriaModulo': 'Seguridad',
            'IdCreador': 1
        }

        modulo_id = db_system.modulos.crear_modulo(nuevo_modulo)
        print(f"   ✅ Módulo creado con ID: {modulo_id}")

        # EJEMPLO 4: Asignar módulo a departamento
        print("\n4. Asignando módulo a departamento...")
        fecha_vencimiento = datetime.now() + timedelta(days=30)
        db_system.modulos.asignar_a_departamento(
            modulo_id, 1, obligatorio=True, fecha_vencimiento=fecha_vencimiento
        )
        print(f"   ✅ Módulo asignado a departamento")

        # EJEMPLO 5: Consultar progreso de usuario
        print("\n5. Consultando progreso de usuario...")
        progreso = db_system.progreso.obtener_progreso_usuario('jperez')
        print(f"   ✅ Usuario tiene {len(progreso)} módulos asignados")
        for p in progreso:
            print(f"      - {p['NombreModulo']}: {p['EstatusModulo']} ({p['PorcentajeAvance']}%)")

        # EJEMPLO 6: Actualizar progreso
        if progreso:
            print("\n6. Actualizando progreso...")
            db_system.progreso.actualizar_progreso(
                progreso[0]['IdInscripcion'],
                'En progreso',
                25.0,
                'Usuario inició el módulo'
            )
            print(f"   ✅ Progreso actualizado")

        # EJEMPLO 7: Obtener módulos próximos a vencer
        print("\n7. Consultando módulos próximos a vencer...")
        vencidos = db_system.progreso.obtener_modulos_vencidos(dias_anticipacion=30)
        print(f"   ✅ Hay {len(vencidos)} módulos próximos a vencer")
        for v in vencidos[:3]:
            print(f"      - {v['NombreCompleto']}: {v['NombreModulo']} (vence en {v['DiasRestantes']} días)")

        # EJEMPLO 8: Generar reporte de cumplimiento
        print("\n8. Generando reporte de cumplimiento...")
        reporte = db_system.reportes.reporte_cumplimiento_unidad()
        print(f"   ✅ Reporte generado con {len(reporte)} filas")
        for r in reporte[:3]:
            print(f"      - {r['NombreUnidad']} / {r['NombreDepartamento']}: {r['PorcentajeCumplimiento']}% cumplimiento")

        # EJEMPLO 9: Validar credenciales
        print("\n9. Validando credenciales de usuario...")
        usuario_autenticado = db_system.usuarios.validar_credenciales('jperez', 'password123')
        if usuario_autenticado:
            print(f"   ✅ Autenticación exitosa: {usuario_autenticado['NombreCompleto']}")
        else:
            print("   ❌ Autenticación fallida")

        print("\n" + "=" * 60)
        print("✅ TODOS LOS EJEMPLOS EJECUTADOS CORRECTAMENTE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cerrar conexiones
        db_system.close()
