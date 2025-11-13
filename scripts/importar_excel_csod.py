#!/usr/bin/env python3
"""
Script de Importación de Excel CSOD
Smart Reports - Instituto Hutchison Ports

USO:
    # Training Report (Progreso y Calificaciones)
    python scripts/importar_excel_csod.py training data/training_report.xlsx

    # Org Planning (Usuarios)
    python scripts/importar_excel_csod.py usuarios data/org_planning.xlsx

REQUIERE:
    - Base de datos tngcore creada
    - Tablas instituto_* creadas
    - Archivo Excel en formato CSOD
"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main.python.data.repositories.persistence.mysql.repositories.database_manager_instituto import (
    DatabaseConfig,
    InstitutoSmartReportsDB
)
from src.main.python.domain.services.excel_importer_instituto import ExcelImporterInstituto

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


def importar_training_report(archivo_excel: str, db_system: InstitutoSmartReportsDB):
    """
    Importa Training Report

    Args:
        archivo_excel: Ruta al Excel
        db_system: Sistema de base de datos
    """
    logger.info("="*70)
    logger.info("📊 IMPORTANDO TRAINING REPORT")
    logger.info("="*70)

    try:
        # Crear importador
        importador = ExcelImporterInstituto(db_system)

        # Importar
        stats = importador.importar_training_report(archivo_excel)

        logger.info("\n✅ IMPORTACIÓN EXITOSA")
        return stats

    except Exception as e:
        logger.error(f"\n❌ ERROR EN LA IMPORTACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return None


def importar_org_planning(archivo_excel: str, db_system: InstitutoSmartReportsDB):
    """
    Importa Org Planning (Usuarios)

    Args:
        archivo_excel: Ruta al Excel
        db_system: Sistema de base de datos
    """
    logger.info("="*70)
    logger.info("👥 IMPORTANDO ORG PLANNING (USUARIOS)")
    logger.info("="*70)

    try:
        # Crear importador
        importador = ExcelImporterInstituto(db_system)

        # Importar
        stats = importador.importar_org_planning(archivo_excel)

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

    # Configurar conexión a MySQL
    logger.info("\n🔌 Conectando a base de datos...")

    config = DatabaseConfig(
        host='localhost',
        database='tngcore',
        user='root',
        password='Xbox360xd',  # ⚠️ CAMBIAR según tu configuración
        port=3306
    )

    try:
        # Conectar
        db_system = InstitutoSmartReportsDB(config)
        logger.info("✅ Conexión exitosa a tngcore")

        # Importar según tipo
        if tipo == 'training':
            stats = importar_training_report(archivo_excel, db_system)
        elif tipo == 'usuarios':
            stats = importar_org_planning(archivo_excel, db_system)
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

    finally:
        # Cerrar conexión
        if 'db_system' in locals():
            db_system.close()
            logger.info("✅ Conexión cerrada")


if __name__ == "__main__":
    sys.exit(main())
