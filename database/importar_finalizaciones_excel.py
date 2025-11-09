"""
Script para importar finalizaciones de módulos desde Excel
Actualiza registros existentes en instituto_ProgresoModulo con fechas de finalización

Estructura esperada del Excel:
- UserId: Identificador del usuario
- Módulo: Nombre del módulo
- Fecha Finalización: Fecha de completación
- Estatus: Completado/Incompleto (opcional)
- Calificación: Nota obtenida (opcional)
"""
import pandas as pd
import mysql.connector
from datetime import datetime
from pathlib import Path
import sys


class ImportadorFinalizaciones:
    """Importador de finalizaciones de módulos desde Excel"""

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
            'progreso_encontrado': 0,
            'progreso_no_encontrado': 0,
            'finalizaciones_registradas': 0,
            'incompletos_registrados': 0,
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
        Lee archivo Excel con finalizaciones

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

            # Fecha Finalización
            'Fecha Finalizacion': 'FechaFinalizacion',
            'Fecha Finalización': 'FechaFinalizacion',
            'Completion Date': 'FechaFinalizacion',
            'Fecha Completado': 'FechaFinalizacion',

            # Estatus
            'Estatus': 'Estatus',
            'Status': 'Estatus',
            'Estado': 'Estatus',

            # Calificación
            'Calificacion': 'Calificacion',
            'Calificación': 'Calificacion',
            'Score': 'Calificacion',
            'Nota': 'Calificacion',
            'Grade': 'Calificacion',
        }

        # Renombrar columnas
        for col_excel, col_estandar in mapeo.items():
            if col_excel in df.columns:
                df.rename(columns={col_excel: col_estandar}, inplace=True)

        # Verificar columnas requeridas
        requeridas = ['UserId', 'NombreModulo', 'FechaFinalizacion']
        faltantes = [col for col in requeridas if col not in df.columns]

        if faltantes:
            raise ValueError(f"❌ Columnas faltantes: {faltantes}")

        # Columnas opcionales
        if 'Estatus' not in df.columns:
            df['Estatus'] = 'Completado'

        if 'Calificacion' not in df.columns:
            df['Calificacion'] = None

        return df

    def buscar_progreso(self, user_id, nombre_modulo):
        """
        Busca registro de progreso existente

        Args:
            user_id: UserId del usuario
            nombre_modulo: Nombre del módulo

        Returns:
            IdProgreso o None
        """
        cursor = self.conn.cursor()

        # Buscar por UserId y nombre de módulo
        cursor.execute(
            """
            SELECT pm.IdProgreso
            FROM instituto_ProgresoModulo pm
            INNER JOIN instituto_Modulo m ON pm.IdModulo = m.IdModulo
            WHERE pm.UserId = %s AND m.NombreModulo = %s
            """,
            (user_id, nombre_modulo)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]

        return None

    def importar_finalizacion(self, row):
        """
        Importa una finalización individual

        Args:
            row: Fila del DataFrame

        Returns:
            bool: True si se importó correctamente
        """
        user_id = str(row['UserId']).strip()
        nombre_modulo = str(row['NombreModulo']).strip()
        fecha_finalizacion = row['FechaFinalizacion']
        estatus = str(row['Estatus']).strip()
        calificacion = row.get('Calificacion')

        # Buscar registro de progreso
        id_progreso = self.buscar_progreso(user_id, nombre_modulo)

        if not id_progreso:
            print(f"   ⚠️ Progreso no encontrado: {user_id} - {nombre_modulo}")
            self.stats['progreso_no_encontrado'] += 1
            return False

        self.stats['progreso_encontrado'] += 1

        # Formatear fecha
        try:
            if pd.notna(fecha_finalizacion):
                if isinstance(fecha_finalizacion, str):
                    fecha_finalizacion = pd.to_datetime(fecha_finalizacion).strftime('%Y-%m-%d')
                else:
                    fecha_finalizacion = fecha_finalizacion.strftime('%Y-%m-%d')
            else:
                fecha_finalizacion = None
        except Exception as e:
            print(f"   ⚠️ Error parseando fecha: {e}")
            fecha_finalizacion = None

        # Determinar estatus y porcentaje
        estatus_normalizado = self._normalizar_estatus(estatus)
        porcentaje_avance = 100.0 if estatus_normalizado == 'Completado' else 0.0

        # Formatear calificación
        if pd.notna(calificacion):
            try:
                calificacion = float(calificacion)
            except:
                calificacion = None
        else:
            calificacion = None

        # Actualizar progreso
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE instituto_ProgresoModulo
                SET FechaFinalizacion = %s,
                    EstatusModulo = %s,
                    PorcentajeAvance = %s,
                    CalificacionObtenida = %s,
                    FechaUltimaActualizacion = NOW()
                WHERE IdProgreso = %s
                """,
                (fecha_finalizacion, estatus_normalizado, porcentaje_avance,
                 calificacion, id_progreso)
            )
            self.conn.commit()
            cursor.close()

            if estatus_normalizado == 'Completado':
                self.stats['finalizaciones_registradas'] += 1
            else:
                self.stats['incompletos_registrados'] += 1

            return True

        except Exception as e:
            print(f"   ❌ Error actualizando progreso: {e}")
            cursor.close()
            self.stats['errores'] += 1
            return False

    def _normalizar_estatus(self, estatus):
        """
        Normaliza diferentes variaciones de estatus

        Args:
            estatus: String con estatus

        Returns:
            'Completado' o 'Incompleto'
        """
        estatus_lower = str(estatus).lower().strip()

        if estatus_lower in ['completado', 'complete', 'completed', 'finalizado', 'aprobado', 'passed']:
            return 'Completado'
        elif estatus_lower in ['incompleto', 'incomplete', 'failed', 'reprobado', 'fallado']:
            return 'Incompleto'
        else:
            # Por defecto, si tiene fecha de finalización es completado
            return 'Completado'

    def importar_desde_excel(self, archivo_excel):
        """
        Importa todas las finalizaciones desde Excel

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            dict: Estadísticas de importación
        """
        print("\n" + "="*60)
        print("IMPORTACIÓN DE FINALIZACIONES DE MÓDULOS")
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

            # 4. Importar cada finalización
            print(f"\n📥 Importando {len(df)} finalizaciones...")
            for idx, row in df.iterrows():
                if (idx + 1) % 100 == 0:
                    print(f"   Procesados: {idx + 1}/{len(df)}")

                self.importar_finalizacion(row)

            # 5. Desconectar
            self.desconectar()

            # 6. Mostrar resumen
            print("\n" + "="*60)
            print("RESUMEN DE IMPORTACIÓN")
            print("="*60)
            print(f"📊 Registros leídos:              {self.stats['leidos']}")
            print(f"✅ Progresos encontrados:         {self.stats['progreso_encontrado']}")
            print(f"⚠️  Progresos no encontrados:      {self.stats['progreso_no_encontrado']}")
            print(f"✅ Completados registrados:       {self.stats['finalizaciones_registradas']}")
            print(f"⚠️  Incompletos registrados:       {self.stats['incompletos_registrados']}")
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
    print("IMPORTADOR DE FINALIZACIONES - SMART REPORTS")
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
        archivos = list(Path('.').glob('*finalizacion*.xlsx')) + \
                   list(Path('.').glob('*completion*.xlsx')) + \
                   list(Path('.').glob('*completado*.xlsx'))

        if not archivos:
            print("\n❌ No se encontró archivo Excel de finalizaciones")
            print("\n💡 Uso:")
            print("   python importar_finalizaciones_excel.py archivo_finalizaciones.xlsx")
            return

        archivo_excel = archivos[0]
        print(f"\n📁 Archivo encontrado: {archivo_excel}")

    # Verificar archivo existe
    if not Path(archivo_excel).exists():
        print(f"\n❌ Archivo no encontrado: {archivo_excel}")
        return

    # Importar
    importador = ImportadorFinalizaciones(config)
    importador.importar_desde_excel(archivo_excel)


if __name__ == "__main__":
    main()
