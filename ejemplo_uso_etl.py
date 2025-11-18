"""
Ejemplo de Uso del Sistema ETL - Instituto Hutchison Ports
==========================================================

Este script muestra cómo usar el sistema ETL para importar datos
de CSOD a la base de datos SQL Server.

Autor: Sistema ETL Instituto Hutchison Ports
Fecha: 2025-01-18
"""

import sys
import os
from pathlib import Path

# Agregar ruta del proyecto al PYTHONPATH
proyecto_root = Path(__file__).parent
sys.path.insert(0, str(proyecto_root))

from src.main.python.domain.services.etl_instituto_completo import (
    ETLInstitutoCompleto,
    ETLConfig
)
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ejemplo_basico():
    """
    Ejemplo 1: Uso básico del ETL con autenticación Windows
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: USO BÁSICO - Autenticación Windows")
    print("="*80)

    # Configuración
    config = ETLConfig(
        server="localhost",
        database="InstitutoHutchison",
        username=None,  # None = Windows Authentication
        password=None,
        batch_size=1000,
        enable_validation=True,
        auto_create_modules=True
    )

    try:
        # Crear instancia del ETL (context manager)
        with ETLInstitutoCompleto(config) as etl:
            # Ejemplo: Importar Org Planning
            logger.info("📥 Importando datos de usuarios (Org Planning)...")

            # IMPORTANTE: Reemplaza con la ruta real de tu archivo
            archivo_org_planning = "data/CSOD_Data_Source_for_Org_Planning.xlsx"

            if os.path.exists(archivo_org_planning):
                stats = etl.importar_org_planning(archivo_org_planning)

                # Mostrar resumen
                print("\n📊 RESUMEN DE IMPORTACIÓN:")
                print(f"  • Usuarios nuevos: {stats['usuarios_nuevos']}")
                print(f"  • Usuarios actualizados: {stats['usuarios_actualizados']}")
                print(f"  • Unidades creadas: {stats['unidades_creadas']}")
                print(f"  • Departamentos creados: {stats['departamentos_creados']}")
                print(f"  • Errores: {len(stats['errores'])}")
            else:
                logger.warning(f"⚠️  Archivo no encontrado: {archivo_org_planning}")
                logger.info("    Asegúrate de tener el archivo en la carpeta 'data/'")

    except Exception as e:
        logger.error(f"❌ Error en ejemplo básico: {e}")
        raise


def ejemplo_training_report():
    """
    Ejemplo 2: Importar Training Report (Progreso y Calificaciones)
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: TRAINING REPORT - Progreso y Calificaciones")
    print("="*80)

    config = ETLConfig(
        server="localhost",
        database="InstitutoHutchison",
        username=None,
        password=None
    )

    try:
        with ETLInstitutoCompleto(config) as etl:
            logger.info("📥 Importando progreso de capacitación...")

            # IMPORTANTE: Reemplaza con la ruta real de tu archivo
            archivo_training = "data/Enterprise_Training_Report.xlsx"

            if os.path.exists(archivo_training):
                stats = etl.importar_training_report(archivo_training)

                # Mostrar resumen
                print("\n📊 RESUMEN DE IMPORTACIÓN:")
                print(f"  • Progresos insertados: {stats['progresos_insertados']}")
                print(f"  • Progresos actualizados: {stats['progresos_actualizados']}")
                print(f"  • Calificaciones registradas: {stats['calificaciones_registradas']}")
                print(f"  • Módulos creados: {stats['modulos_creados']}")
                print(f"  • Evaluaciones creadas: {stats['evaluaciones_creadas']}")
                print(f"  • Errores: {len(stats['errores'])}")
            else:
                logger.warning(f"⚠️  Archivo no encontrado: {archivo_training}")
                logger.info("    Asegúrate de tener el archivo en la carpeta 'data/'")

    except Exception as e:
        logger.error(f"❌ Error en ejemplo training report: {e}")
        raise


def ejemplo_sql_server_auth():
    """
    Ejemplo 3: Uso con autenticación SQL Server (no Windows)
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: AUTENTICACIÓN SQL SERVER")
    print("="*80)

    # Configuración con usuario y contraseña
    config = ETLConfig(
        server="mi-servidor.database.windows.net",  # Servidor remoto
        database="InstitutoHutchison",
        username="usuario_sql",
        password="password_seguro",  # ⚠️ NO hardcodear en producción
        driver="ODBC Driver 17 for SQL Server"
    )

    logger.info("ℹ️  Ejemplo configurado pero no ejecutado (requiere servidor remoto)")
    logger.info("    Edita las credenciales y descomenta el código para usar")

    # Descomenta para ejecutar:
    # try:
    #     with ETLInstitutoCompleto(config) as etl:
    #         stats = etl.importar_org_planning("data/Org_Planning.xlsx")
    #         print(f"✅ Importación exitosa: {stats['usuarios_nuevos']} usuarios nuevos")
    # except Exception as e:
    #     logger.error(f"❌ Error: {e}")


def ejemplo_completo_ambos_archivos():
    """
    Ejemplo 4: Importar ambos archivos (Org Planning + Training Report)
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: IMPORTACIÓN COMPLETA (Usuarios + Progreso)")
    print("="*80)

    config = ETLConfig(
        server="localhost",
        database="InstitutoHutchison"
    )

    archivo_org = "data/CSOD_Data_Source_for_Org_Planning.xlsx"
    archivo_training = "data/Enterprise_Training_Report.xlsx"

    try:
        with ETLInstitutoCompleto(config) as etl:
            # Paso 1: Importar usuarios
            if os.path.exists(archivo_org):
                logger.info("📥 Paso 1/2: Importando usuarios...")
                stats_usuarios = etl.importar_org_planning(archivo_org)
                logger.info(f"✅ {stats_usuarios['usuarios_nuevos']} usuarios nuevos")
            else:
                logger.warning(f"⚠️  Archivo no encontrado: {archivo_org}")

            # Paso 2: Importar progreso
            if os.path.exists(archivo_training):
                logger.info("\n📥 Paso 2/2: Importando progreso de capacitación...")
                stats_training = etl.importar_training_report(archivo_training)
                logger.info(f"✅ {stats_training['progresos_insertados']} progresos nuevos")
            else:
                logger.warning(f"⚠️  Archivo no encontrado: {archivo_training}")

            logger.info("\n✅ IMPORTACIÓN COMPLETA FINALIZADA")

    except Exception as e:
        logger.error(f"❌ Error en importación completa: {e}")
        raise


def main():
    """
    Función principal - Ejecuta todos los ejemplos
    """
    print("\n" + "="*80)
    print("🚀 EJEMPLOS DE USO - SISTEMA ETL INSTITUTO HUTCHISON PORTS")
    print("="*80)

    try:
        # Verificar que el módulo ETL esté disponible
        logger.info("✅ Módulo ETL cargado correctamente")

        # Ejecutar ejemplos
        print("\n⚠️  IMPORTANTE: Estos ejemplos requieren:")
        print("    1. SQL Server corriendo en localhost")
        print("    2. Base de datos 'InstitutoHutchison' creada")
        print("    3. Archivos Excel en la carpeta 'data/'")
        print("\n¿Deseas continuar? (s/n): ", end="")

        # Comentar la siguiente línea para ejecutar sin confirmación
        # respuesta = input().lower()
        respuesta = 'n'  # Cambia a 's' para ejecutar automáticamente

        if respuesta == 's':
            # Ejecutar ejemplos
            ejemplo_basico()
            ejemplo_training_report()
            ejemplo_sql_server_auth()
            ejemplo_completo_ambos_archivos()
        else:
            logger.info("ℹ️  Ejemplos no ejecutados (modo demostración)")
            logger.info("    Edita este archivo y cambia 'respuesta = s' para ejecutar")

        print("\n" + "="*80)
        print("✅ SCRIPT DE EJEMPLOS COMPLETADO")
        print("="*80)

    except KeyboardInterrupt:
        logger.info("\n⚠️  Operación cancelada por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
