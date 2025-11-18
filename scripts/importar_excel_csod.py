#!/usr/bin/env python3
"""
Script de Importación de Excel CSOD
Smart Reports - Instituto Hutchison Ports

ACTUALIZADO: Ahora usa el nuevo sistema ETL completo (etl_instituto_completo.py)

USO:
    # Training Report (Progreso y Calificaciones)
    python scripts/importar_excel_csod.py training data/training_report.xlsx

    # Org Planning (Usuarios)
    python scripts/importar_excel_csod.py usuarios data/org_planning.xlsx

REQUIERE:
    - SQL Server con base de datos InstitutoHutchison
    - Tablas instituto_* creadas
    - Archivo Excel en formato CSOD
    - pyodbc instalado
"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main.python.domain.services.etl_instituto_completo import (
    ETLInstitutoCompleto,
    ETLConfig
)

import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def mostrar_uso():
    """Muestra instrucciones de uso"""
    print("="*70)
    print("IMPORTADOR DE EXCEL CSOD - SMART REPORTS")
    print("="*70)
    print("\nUSO:")
    print("  python scripts/importar_excel_csod.py <tipo> <archivo>")
    print("\nTIPOS:")
    print("  training   - Enterprise Training Report (Progreso y Calificaciones)")
    print("  usuarios   - CSOD Org Planning (Datos de Usuarios)")
    print("\nEJEMPLOS:")
    print("  python scripts/importar_excel_csod.py training data/training_report.xlsx")
    print("  python scripts/importar_excel_csod.py usuarios data/org_planning.xlsx")
    print("="*70)


def validar_archivo(archivo_excel: str) -> bool:
    """
    Valida que el archivo Excel exista

    Args:
        archivo_excel: Ruta al archivo

    Returns:
        True si existe, False si no
    """
    if not os.path.exists(archivo_excel):
        logger.error(f"❌ Archivo no encontrado: {archivo_excel}")
        return False

    if not archivo_excel.endswith(('.xlsx', '.xls')):
        logger.error(f"❌ Archivo debe ser Excel (.xlsx o .xls): {archivo_excel}")
        return False

    logger.info(f"✅ Archivo encontrado: {archivo_excel}")
    return True


def importar_training_report(archivo_excel: str, config: ETLConfig):
    """
    Importa Training Report usando el nuevo ETL

    Args:
        archivo_excel: Ruta al Excel
        config: Configuración del ETL
    """
    logger.info("="*70)
    logger.info("📊 IMPORTANDO TRAINING REPORT")
    logger.info("="*70)

    try:
        # Crear importador ETL
        with ETLInstitutoCompleto(config) as etl:
            # Importar
            stats = etl.importar_training_report(archivo_excel)

        logger.info("\n✅ IMPORTACIÓN EXITOSA")
        return stats

    except Exception as e:
        logger.error(f"\n❌ ERROR EN LA IMPORTACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


def importar_org_planning(archivo_excel: str, config: ETLConfig):
    """
    Importa Org Planning (Usuarios) usando el nuevo ETL

    Args:
        archivo_excel: Ruta al Excel
        config: Configuración del ETL
    """
    logger.info("="*70)
    logger.info("👥 IMPORTANDO ORG PLANNING (USUARIOS)")
    logger.info("="*70)

    try:
        # Crear importador ETL
        with ETLInstitutoCompleto(config) as etl:
            # Importar
            stats = etl.importar_org_planning(archivo_excel)

        logger.info("\n✅ IMPORTACIÓN EXITOSA")
        return stats

    except Exception as e:
        logger.error(f"\n❌ ERROR EN LA IMPORTACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Función principal"""
    # Verificar argumentos
    if len(sys.argv) < 3:
        mostrar_uso()
        return 1

    tipo = sys.argv[1].lower()
    archivo_excel = sys.argv[2]

    # Validar tipo
    if tipo not in ['training', 'usuarios']:
        logger.error(f"❌ Tipo inválido: {tipo}")
        logger.error("   Tipos válidos: training, usuarios")
        mostrar_uso()
        return 1

    # Validar archivo
    if not validar_archivo(archivo_excel):
        return 1

    # Configurar conexión a SQL Server
    logger.info("\n🔌 Configurando conexión a SQL Server...")

    config = ETLConfig(
        server="localhost",                   # ⚠️ CAMBIAR según tu servidor
        database="InstitutoHutchison",
        username=None,                        # None = Windows Authentication
        password=None,                        # O especificar credenciales SQL Server
        driver="ODBC Driver 17 for SQL Server",
        batch_size=1000,
        enable_validation=True,
        auto_create_modules=True
    )

    try:
        logger.info("✅ Configuración lista")

        # Importar según tipo
        if tipo == 'training':
            stats = importar_training_report(archivo_excel, config)
        elif tipo == 'usuarios':
            stats = importar_org_planning(archivo_excel, config)
        else:
            logger.error(f"❌ Tipo desconocido: {tipo}")
            return 1

        if stats:
            logger.info("\n" + "="*70)
            logger.info("📊 RESUMEN FINAL")
            logger.info("="*70)
            logger.info(f"  • Archivo procesado: {archivo_excel}")
            logger.info(f"  • Tipo de reporte:   {tipo}")
            logger.info(f"  • Estado:            EXITOSO ✅")
            logger.info("="*70)
            return 0
        else:
            logger.error("\n❌ La importación falló")
            return 1

    except Exception as e:
        logger.error(f"\n❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
