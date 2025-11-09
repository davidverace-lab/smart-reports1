"""
Script Maestro para Importación Completa - Fase 1
Importa los 3 Excel en el orden correcto:
1. Usuarios
2. Asignaciones
3. Finalizaciones

USO:
    python importar_todo_excel.py <usuarios.xlsx> <asignaciones.xlsx> <finalizaciones.xlsx>

O colocar los 3 archivos en la carpeta 'data/' con nombres:
    - usuarios.xlsx
    - asignaciones.xlsx
    - finalizaciones.xlsx
"""
import sys
from pathlib import Path
from datetime import datetime

# Importar los 3 importadores
from importar_usuarios_excel import procesar_excel_a_csv
from importar_asignaciones_excel import ImportadorAsignaciones
from importar_finalizaciones_excel import ImportadorFinalizaciones


class ImportadorCompleto:
    """Coordina la importación completa de los 3 Excel"""

    def __init__(self, config_mysql):
        """
        Args:
            config_mysql: Configuración de MySQL
        """
        self.config = config_mysql
        self.archivos = {
            'usuarios': None,
            'asignaciones': None,
            'finalizaciones': None
        }
        self.resultados = {}

    def detectar_archivos(self, archivos_args=None):
        """
        Detecta archivos Excel automáticamente o usa los proporcionados

        Args:
            archivos_args: Lista de rutas [usuarios, asignaciones, finalizaciones]

        Returns:
            bool: True si encontró todos los archivos
        """
        print("\n" + "="*60)
        print("DETECCIÓN DE ARCHIVOS EXCEL")
        print("="*60)

        if archivos_args and len(archivos_args) == 3:
            # Usar archivos proporcionados
            self.archivos['usuarios'] = archivos_args[0]
            self.archivos['asignaciones'] = archivos_args[1]
            self.archivos['finalizaciones'] = archivos_args[2]

            # Verificar que existan
            for tipo, archivo in self.archivos.items():
                if not Path(archivo).exists():
                    print(f"❌ Archivo no encontrado: {archivo}")
                    return False
                print(f"✅ {tipo.capitalize():15} → {archivo}")

            return True

        # Buscar en carpeta 'data/'
        data_dir = Path('data')
        if not data_dir.exists():
            data_dir.mkdir()
            print(f"📁 Carpeta 'data/' creada. Coloca los 3 Excel ahí:")
            print(f"   - usuarios.xlsx")
            print(f"   - asignaciones.xlsx")
            print(f"   - finalizaciones.xlsx")
            return False

        # Buscar archivos por patrón
        patrones = {
            'usuarios': ['*usuario*.xlsx', '*user*.xlsx', '*users*.xlsx'],
            'asignaciones': ['*asignacion*.xlsx', '*assignment*.xlsx'],
            'finalizaciones': ['*finalizacion*.xlsx', '*completion*.xlsx', '*completado*.xlsx']
        }

        for tipo, patrones_lista in patrones.items():
            for patron in patrones_lista:
                archivos = list(data_dir.glob(patron))
                if archivos:
                    self.archivos[tipo] = str(archivos[0])
                    print(f"✅ {tipo.capitalize():15} → {archivos[0].name}")
                    break

            if not self.archivos[tipo]:
                print(f"❌ {tipo.capitalize():15} → No encontrado")

        # Verificar que tengamos todos
        if all(self.archivos.values()):
            return True
        else:
            print("\n💡 Coloca los archivos en la carpeta 'data/' o especifica rutas:")
            print("   python importar_todo_excel.py usuarios.xlsx asignaciones.xlsx finalizaciones.xlsx")
            return False

    def importar_usuarios(self):
        """
        Paso 1: Importar usuarios

        Returns:
            bool: True si fue exitoso
        """
        print("\n" + "="*60)
        print("PASO 1/3: IMPORTAR USUARIOS")
        print("="*60)

        try:
            resultado = procesar_excel_a_csv(self.archivos['usuarios'])

            if resultado:
                self.resultados['usuarios'] = {
                    'exitoso': True,
                    'csv_generado': resultado[0],
                    'sql_generado': resultado[1]
                }

                print("\n✅ USUARIOS: CSV y SQL generados")
                print(f"   Ahora debes importar el CSV a MySQL")
                print(f"   Ver archivo: {resultado[1]}")

                return True
            else:
                print("\n❌ Error importando usuarios")
                return False

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

    def importar_asignaciones(self):
        """
        Paso 2: Importar asignaciones

        Returns:
            bool: True si fue exitoso
        """
        print("\n" + "="*60)
        print("PASO 2/3: IMPORTAR ASIGNACIONES")
        print("="*60)

        try:
            importador = ImportadorAsignaciones(self.config)
            stats = importador.importar_desde_excel(self.archivos['asignaciones'])

            if stats:
                self.resultados['asignaciones'] = stats
                print("\n✅ ASIGNACIONES: Importadas correctamente")
                return True
            else:
                print("\n❌ Error importando asignaciones")
                return False

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

    def importar_finalizaciones(self):
        """
        Paso 3: Importar finalizaciones

        Returns:
            bool: True si fue exitoso
        """
        print("\n" + "="*60)
        print("PASO 3/3: IMPORTAR FINALIZACIONES")
        print("="*60)

        try:
            importador = ImportadorFinalizaciones(self.config)
            stats = importador.importar_desde_excel(self.archivos['finalizaciones'])

            if stats:
                self.resultados['finalizaciones'] = stats
                print("\n✅ FINALIZACIONES: Importadas correctamente")
                return True
            else:
                print("\n❌ Error importando finalizaciones")
                return False

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generar_reporte_final(self):
        """Genera reporte consolidado de toda la importación"""
        print("\n" + "="*60)
        print("📊 REPORTE FINAL DE IMPORTACIÓN")
        print("="*60)
        print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        # Usuarios
        if 'usuarios' in self.resultados:
            print("\n✅ USUARIOS:")
            print(f"   CSV generado: {self.resultados['usuarios'].get('csv_generado', 'N/A')}")
            print(f"   SQL generado: {self.resultados['usuarios'].get('sql_generado', 'N/A')}")

        # Asignaciones
        if 'asignaciones' in self.resultados:
            stats = self.resultados['asignaciones']
            print("\n✅ ASIGNACIONES:")
            print(f"   Registros leídos:              {stats.get('leidos', 0)}")
            print(f"   Usuarios encontrados:          {stats.get('usuarios_encontrados', 0)}")
            print(f"   Usuarios no encontrados:       {stats.get('usuarios_no_encontrados', 0)}")
            print(f"   Módulos creados:               {stats.get('modulos_creados', 0)}")
            print(f"   Asignaciones creadas:          {stats.get('asignaciones_creadas', 0)}")
            print(f"   Asignaciones actualizadas:     {stats.get('asignaciones_actualizadas', 0)}")

        # Finalizaciones
        if 'finalizaciones' in self.resultados:
            stats = self.resultados['finalizaciones']
            print("\n✅ FINALIZACIONES:")
            print(f"   Registros leídos:              {stats.get('leidos', 0)}")
            print(f"   Progresos encontrados:         {stats.get('progreso_encontrado', 0)}")
            print(f"   Progresos no encontrados:      {stats.get('progreso_no_encontrado', 0)}")
            print(f"   Completados registrados:       {stats.get('finalizaciones_registradas', 0)}")
            print(f"   Incompletos registrados:       {stats.get('incompletos_registrados', 0)}")

        print("\n" + "="*60)
        print("✅ IMPORTACIÓN COMPLETA FINALIZADA")
        print("="*60)

    def ejecutar_importacion_completa(self, archivos_args=None):
        """
        Ejecuta toda la importación en orden

        Args:
            archivos_args: Lista de rutas a los 3 Excel (opcional)

        Returns:
            bool: True si todo fue exitoso
        """
        print("\n" + "="*60)
        print("🚀 IMPORTACIÓN COMPLETA - FASE 1")
        print("Smart Reports - Instituto Hutchison Ports")
        print("="*60)

        # 1. Detectar archivos
        if not self.detectar_archivos(archivos_args):
            return False

        # 2. Importar usuarios
        if not self.importar_usuarios():
            print("\n⚠️ ADVERTENCIA: Usuarios no importados")
            print("   Asegúrate de importar el CSV antes de continuar")
            respuesta = input("\n¿Continuar de todos modos? (s/n): ")
            if respuesta.lower() != 's':
                return False

        # 3. Importar asignaciones
        if not self.importar_asignaciones():
            print("\n❌ Error en asignaciones. Abortando...")
            return False

        # 4. Importar finalizaciones
        if not self.importar_finalizaciones():
            print("\n❌ Error en finalizaciones. Abortando...")
            return False

        # 5. Reporte final
        self.generar_reporte_final()

        return True


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("SMART REPORTS - IMPORTADOR COMPLETO FASE 1")
    print("="*60)

    # Configuración de MySQL
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # CAMBIAR según tu configuración
        'database': 'tngcore'
    }

    # Obtener archivos de argumentos (si se proporcionaron)
    archivos_args = None
    if len(sys.argv) == 4:
        archivos_args = sys.argv[1:4]
        print(f"\n📁 Usando archivos proporcionados:")
        for i, archivo in enumerate(archivos_args, 1):
            print(f"   {i}. {archivo}")

    # Crear importador y ejecutar
    importador = ImportadorCompleto(config)
    exitoso = importador.ejecutar_importacion_completa(archivos_args)

    if exitoso:
        print("\n🎉 ¡IMPORTACIÓN EXITOSA!")
        print("\n📊 Próximos pasos:")
        print("   1. Verificar datos en MySQL Workbench")
        print("   2. Ejecutar queries de validación")
        print("   3. Generar dashboards con los datos importados")
    else:
        print("\n❌ Importación incompleta. Revisa los errores arriba.")

    return 0 if exitoso else 1


if __name__ == "__main__":
    sys.exit(main())
