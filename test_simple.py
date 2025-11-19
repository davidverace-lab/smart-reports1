"""
Test simplificado - Simula exactamente lo que hace ventana_principal_view.py
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

print("="*80)
print("TEST SIMPLIFICADO - Simulando ventana_principal_view.py")
print("="*80)

# Test 1: Verificar dependencias críticas
print("\n[TEST 1] Verificando dependencias críticas...")
dependencias_faltantes = []

try:
    import customtkinter as ctk
    print("  ✓ customtkinter")
except ImportError:
    print("  ✗ customtkinter - INSTALA: pip install customtkinter")
    dependencias_faltantes.append("customtkinter")

try:
    import matplotlib
    print("  ✓ matplotlib")
except ImportError:
    print("  ⚠ matplotlib - RECOMENDADO: pip install matplotlib")
    print("    (Dashboard no funcionará sin esto)")

try:
    import pandas
    print("  ✓ pandas")
except ImportError:
    print("  ⚠ pandas - RECOMENDADO: pip install pandas")
    print("    (Importación no funcionará sin esto)")

if dependencias_faltantes:
    print("\n❌ FALTAN DEPENDENCIAS CRÍTICAS")
    print("Ejecuta: pip install " + " ".join(dependencias_faltantes))
    sys.exit(1)

# Test 2: Imports de configuración
print("\n[TEST 2] Importando configuración...")
try:
    from smart_reports.config.themes import HUTCHISON_COLORS
    from smart_reports.config.gestor_temas import get_theme_manager
    print("  ✓ Configuración OK")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: Simular lo que hace show_dashboard()
print("\n[TEST 3] Simulando show_dashboard()...")
try:
    print("  1. Importando show_dashboard_menu...")
    from smart_reports.ui.views.menu_dashboard import show_dashboard_menu
    print("     ✓ Import OK")

    print("  2. Creando ventana de prueba...")
    root = ctk.CTk()
    root.withdraw()  # No mostrar ventana

    print("  3. Creando container...")
    container = ctk.CTkFrame(root)

    print("  4. Llamando show_dashboard_menu...")
    panel = show_dashboard_menu(
        container,
        db_connection=None,
        username="Test",
        user_role="Admin"
    )

    if panel:
        print("     ✓ Panel creado correctamente")
        print(f"     Tipo: {type(panel).__name__}")
    else:
        print("     ✗ Panel es None")

    root.destroy()
    print("  ✓ Dashboard funciona")

except Exception as e:
    print(f"  ✗ Error en Dashboard: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Simular show_consultas()
print("\n[TEST 4] Simulando show_consultas()...")
try:
    from smart_reports.ui.views.menu_consultas import show_consultas_menu

    root = ctk.CTk()
    root.withdraw()
    container = ctk.CTkFrame(root)

    panel = show_consultas_menu(container, db_connection=None)

    if panel:
        print(f"  ✓ Consultas funciona - Tipo: {type(panel).__name__}")
    else:
        print("  ✗ Consultas retorna None")

    root.destroy()

except Exception as e:
    print(f"  ✗ Error en Consultas: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Simular show_importacion()
print("\n[TEST 5] Simulando show_importacion()...")
try:
    from smart_reports.ui.views.configuracion.panel_importacion_datos import PanelImportacionDatos

    root = ctk.CTk()
    root.withdraw()
    container = ctk.CTkFrame(root)

    panel = PanelImportacionDatos(container, db_connection=None)

    if panel:
        print(f"  ✓ Importación funciona - Tipo: {type(panel).__name__}")
    else:
        print("  ✗ Importación retorna None")

    root.destroy()

except Exception as e:
    print(f"  ✗ Error en Importación: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Simular show_reportes()
print("\n[TEST 6] Simulando show_reportes()...")
try:
    from smart_reports.ui.views.menu_reportes import show_reportes_menu

    root = ctk.CTk()
    root.withdraw()
    container = ctk.CTkFrame(root)

    menu = show_reportes_menu(container, db_connection=None, cursor=None)

    if menu:
        print(f"  ✓ Reportes funciona - Tipo: {type(menu).__name__}")
    else:
        print("  ✗ Reportes retorna None")

    root.destroy()

except Exception as e:
    print(f"  ✗ Error en Reportes: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Simular show_configuracion()
print("\n[TEST 7] Simulando show_configuracion()...")
try:
    from smart_reports.ui.views.menu_configuracion import show_configuracion_menu

    root = ctk.CTk()
    root.withdraw()
    container = ctk.CTkFrame(root)

    panel = show_configuracion_menu(container, db_connection=None, cursor=None, db_instance=None)

    if panel:
        print(f"  ✓ Configuración funciona - Tipo: {type(panel).__name__}")
    else:
        print("  ✗ Configuración retorna None")

    root.destroy()

except Exception as e:
    print(f"  ✗ Error en Configuración: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("FIN DEL TEST")
print("="*80)
print("\nSi todos los tests pasaron (✓), entonces la aplicación DEBERÍA funcionar.")
print("Si algún test falló (✗), revisa el traceback para ver qué falta.")
print("\nPara ejecutar la aplicación: python main.py")
print("="*80)
