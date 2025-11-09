"""
Script para importar asignaciones de módulos desde Excel
Lee Excel con asignaciones y crea registros en instituto_ProgresoModulo

Estructura esperada del Excel:
- UserId: Identificador del usuario
- Módulo: Nombre del módulo
- Fecha Asignación: Fecha de asignación
- Fecha Vencimiento: Fecha límite
"""
import pandas as pd
import mysql.connector
from datetime import datetime
from pathlib import Path
import sys


class ImportadorAsignaciones:
    """Importador de asignaciones de módulos desde Excel"""

    def __init__(self, config):
        """
        Args:
            config: Diccionario con configuración de MySQL
                    {'host', 'user', 'password', 'database'}
        """
        self.config = config
        self.conn = None
        self.stats = {
            'leidos': 0,
            'usuarios_encontrados': 0,
            'usuarios_no_encontrados': 0,
            'modulos_creados': 0,
            'asignaciones_creadas': 0,
            'asignaciones_actualizadas': 0,
            'errores': 0
        }

    def conectar(self):
        """Conectar a MySQL"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            print(f"✅ Conectado a {self.config['database']}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a MySQL: {e}")
            return False

    def desconectar(self):
        """Desconectar de MySQL"""
        if self.conn:
            self.conn.close()
            print("✅ Desconectado de MySQL")

    def leer_excel(self, archivo_excel):
        """
        Lee archivo Excel con asignaciones

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            DataFrame de pandas
        """
        print(f"\n📖 Leyendo archivo: {archivo_excel}")

        # Leer Excel
        df = pd.read_excel(archivo_excel)

        print(f"✅ Leídos {len(df)} registros")
        print(f"📋 Columnas: {list(df.columns)}")

        self.stats['leidos'] = len(df)
        return df

    def mapear_columnas(self, df):
        """
        Mapea columnas del Excel a estructura esperada

        Busca variaciones de nombres de columnas
        """
        mapeo = {
            # UserId
            'UserId': 'UserId',
            'User Id': 'UserId',
            'ID Usuario': 'UserId',
            'Usuario': 'UserId',

            # Módulo
            'Modulo': 'NombreModulo',
            'Módulo': 'NombreModulo',
            'Module': 'NombreModulo',
            'Curso': 'NombreModulo',

            # Fecha Asignación
            'Fecha Asignacion': 'FechaAsignacion',
            'Fecha Asignación': 'FechaAsignacion',
            'Assignment Date': 'FechaAsignacion',
            'Fecha Inicio': 'FechaAsignacion',

            # Fecha Vencimiento
            'Fecha Vencimiento': 'FechaVencimiento',
            'Due Date': 'FechaVencimiento',
            'Fecha Limite': 'FechaVencimiento',
            'Fecha Límite': 'FechaVencimiento',
        }

        # Renombrar columnas
        for col_excel, col_estandar in mapeo.items():
            if col_excel in df.columns:
                df.rename(columns={col_excel: col_estandar}, inplace=True)

        # Verificar columnas requeridas
        requeridas = ['UserId', 'NombreModulo', 'FechaAsignacion']
        faltantes = [col for col in requeridas if col not in df.columns]

        if faltantes:
            raise ValueError(f"❌ Columnas faltantes: {faltantes}")

        # FechaVencimiento es opcional
        if 'FechaVencimiento' not in df.columns:
            df['FechaVencimiento'] = None

        return df

    def obtener_o_crear_modulo(self, nombre_modulo):
        """
        Busca módulo por nombre, si no existe lo crea

        Args:
            nombre_modulo: Nombre del módulo

        Returns:
            IdModulo
        """
        cursor = self.conn.cursor()

        # Buscar módulo existente
        cursor.execute(
            "SELECT IdModulo FROM instituto_Modulo WHERE NombreModulo = %s",
            (nombre_modulo,)
        )
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]

        # Crear nuevo módulo
        cursor.execute(
            """
            INSERT INTO instituto_Modulo (NombreModulo, CategoriaModulo, Activo)
            VALUES (%s, 'Importado desde Excel', 1)
            """,
            (nombre_modulo,)
        )
        self.conn.commit()
        id_modulo = cursor.lastrowid
        cursor.close()

        self.stats['modulos_creados'] += 1
        print(f"   ✅ Módulo creado: {nombre_modulo} (ID: {id_modulo})")

        return id_modulo

    def verificar_usuario_existe(self, user_id):
        """
        Verifica si usuario existe en instituto_Usuario

        Args:
            user_id: UserId del usuario

        Returns:
            bool
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM instituto_Usuario WHERE UserId = %s",
            (user_id,)
        )
        existe = cursor.fetchone() is not None
        cursor.close()
        return existe

    def importar_asignacion(self, row):
        """
        Importa una asignación individual

        Args:
            row: Fila del DataFrame

        Returns:
            bool: True si se importó correctamente
        """
        user_id = str(row['UserId']).strip()
        nombre_modulo = str(row['NombreModulo']).strip()
        fecha_asignacion = row['FechaAsignacion']
        fecha_vencimiento = row.get('FechaVencimiento')

        # Verificar usuario existe
        if not self.verificar_usuario_existe(user_id):
            print(f"   ⚠️ Usuario no encontrado: {user_id}")
            self.stats['usuarios_no_encontrados'] += 1
            return False

        self.stats['usuarios_encontrados'] += 1

        # Obtener o crear módulo
        try:
            id_modulo = self.obtener_o_crear_modulo(nombre_modulo)
        except Exception as e:
            print(f"   ❌ Error obteniendo módulo {nombre_modulo}: {e}")
            self.stats['errores'] += 1
            return False

        # Formatear fechas
        try:
            if pd.notna(fecha_asignacion):
                if isinstance(fecha_asignacion, str):
                    fecha_asignacion = pd.to_datetime(fecha_asignacion).strftime('%Y-%m-%d')
                else:
                    fecha_asignacion = fecha_asignacion.strftime('%Y-%m-%d')
            else:
                fecha_asignacion = datetime.now().strftime('%Y-%m-%d')

            if pd.notna(fecha_vencimiento):
                if isinstance(fecha_vencimiento, str):
                    fecha_vencimiento = pd.to_datetime(fecha_vencimiento).strftime('%Y-%m-%d')
                else:
                    fecha_vencimiento = fecha_vencimiento.strftime('%Y-%m-%d')
            else:
                fecha_vencimiento = None

        except Exception as e:
            print(f"   ⚠️ Error parseando fechas: {e}")
            fecha_asignacion = datetime.now().strftime('%Y-%m-%d')
            fecha_vencimiento = None

        # Verificar si ya existe asignación
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT IdProgreso FROM instituto_ProgresoModulo
            WHERE UserId = %s AND IdModulo = %s
            """,
            (user_id, id_modulo)
        )
        existe = cursor.fetchone()

        if existe:
            # Actualizar asignación existente
            id_progreso = existe[0]
            cursor.execute(
                """
                UPDATE instituto_ProgresoModulo
                SET FechaAsignacion = %s,
                    FechaVencimiento = %s,
                    FechaUltimaActualizacion = NOW()
                WHERE IdProgreso = %s
                """,
                (fecha_asignacion, fecha_vencimiento, id_progreso)
            )
            self.conn.commit()
            cursor.close()
            self.stats['asignaciones_actualizadas'] += 1
            return True

        # Crear nueva asignación
        try:
            cursor.execute(
                """
                INSERT INTO instituto_ProgresoModulo (
                    UserId,
                    IdModulo,
                    EstatusModulo,
                    FechaAsignacion,
                    FechaVencimiento,
                    PorcentajeAvance,
                    FechaUltimaActualizacion
                ) VALUES (%s, %s, 'No iniciado', %s, %s, 0.0, NOW())
                """,
                (user_id, id_modulo, fecha_asignacion, fecha_vencimiento)
            )
            self.conn.commit()
            cursor.close()
            self.stats['asignaciones_creadas'] += 1
            return True

        except Exception as e:
            print(f"   ❌ Error creando asignación: {e}")
            cursor.close()
            self.stats['errores'] += 1
            return False

    def importar_desde_excel(self, archivo_excel):
        """
        Importa todas las asignaciones desde Excel

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            dict: Estadísticas de importación
        """
        print("\n" + "="*60)
        print("IMPORTACIÓN DE ASIGNACIONES DE MÓDULOS")
        print("="*60)

        try:
            # 1. Leer Excel
            df = self.leer_excel(archivo_excel)

            # 2. Mapear columnas
            print("\n🔄 Mapeando columnas...")
            df = self.mapear_columnas(df)
            print(f"✅ Columnas mapeadas: {list(df.columns)}")

            # 3. Conectar a MySQL
            if not self.conectar():
                return None

            # 4. Importar cada asignación
            print(f"\n📥 Importando {len(df)} asignaciones...")
            for idx, row in df.iterrows():
                if (idx + 1) % 100 == 0:
                    print(f"   Procesados: {idx + 1}/{len(df)}")

                self.importar_asignacion(row)

            # 5. Desconectar
            self.desconectar()

            # 6. Mostrar resumen
            print("\n" + "="*60)
            print("RESUMEN DE IMPORTACIÓN")
            print("="*60)
            print(f"📊 Registros leídos:              {self.stats['leidos']}")
            print(f"✅ Usuarios encontrados:          {self.stats['usuarios_encontrados']}")
            print(f"⚠️  Usuarios no encontrados:       {self.stats['usuarios_no_encontrados']}")
            print(f"🆕 Módulos creados:               {self.stats['modulos_creados']}")
            print(f"✅ Asignaciones creadas:          {self.stats['asignaciones_creadas']}")
            print(f"🔄 Asignaciones actualizadas:     {self.stats['asignaciones_actualizadas']}")
            print(f"❌ Errores:                       {self.stats['errores']}")
            print("="*60)

            return self.stats

        except Exception as e:
            print(f"\n❌ ERROR GENERAL: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Función principal"""
    import sys

    print("="*60)
    print("IMPORTADOR DE ASIGNACIONES - SMART REPORTS")
    print("="*60)

    # Configuración de MySQL
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Cambiar según tu configuración
        'database': 'tngcore'
    }

    # Buscar archivo Excel
    if len(sys.argv) > 1:
        archivo_excel = sys.argv[1]
    else:
        # Buscar en directorio actual
        archivos = list(Path('.').glob('*asignacion*.xlsx')) + \
                   list(Path('.').glob('*assignment*.xlsx'))

        if not archivos:
            print("\n❌ No se encontró archivo Excel de asignaciones")
            print("\n💡 Uso:")
            print("   python importar_asignaciones_excel.py archivo_asignaciones.xlsx")
            return

        archivo_excel = archivos[0]
        print(f"\n📁 Archivo encontrado: {archivo_excel}")

    # Verificar archivo existe
    if not Path(archivo_excel).exists():
        print(f"\n❌ Archivo no encontrado: {archivo_excel}")
        return

    # Importar
    importador = ImportadorAsignaciones(config)
    importador.importar_desde_excel(archivo_excel)


if __name__ == "__main__":
    main()
