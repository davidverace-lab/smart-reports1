"""
Script de diagnóstico para probar todos los menús
Ejecutar: python test_menus.py
"""
import sys
from pathlib import Path

# Agregar directorio al path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

print("="*80)
print("PRUEBA DE MENÚS - SMART REPORTS")
print("="*80)

# Test 1: Dependencias
print("\n[1] Verificando dependencias...")
try:
    import customtkinter as ctk
    print("  ✓ customtkinter instalado")
except ImportError:
    print("  ✗ customtkinter NO instalado - ejecuta: pip install customtkinter")
    sys.exit(1)

try:
    import matplotlib
    print("  ✓ matplotlib instalado")
except ImportError:
    print("  ✗ matplotlib NO instalado - ejecuta: pip install matplotlib")

# Test 2: Imports de configuración
print("\n[2] Verificando imports de configuración...")
try:
    from smart_reports.config.themes import HUTCHISON_COLORS, DARK_THEME, LIGHT_THEME
    print(f"  ✓ Themes OK ({len(HUTCHISON_COLORS)} colores)")
    print(f"    - aqua_green: {'✓' if 'aqua_green' in HUTCHISON_COLORS else '✗'}")
    print(f"    - danger: {'✓' if 'danger' in HUTCHISON_COLORS else '✗'}")
except Exception as e:
    print(f"  ✗ Error en themes: {e}")
    sys.exit(1)

try:
    from smart_reports.config.gestor_temas import get_theme_manager
    theme_mgr = get_theme_manager()
    theme = theme_mgr.get_current_theme()
    print(f"  ✓ Gestor de temas OK (modo: {theme['name']})")
except Exception as e:
    print(f"  ✗ Error en gestor_temas: {e}")
    sys.exit(1)

# Test 3: Imports de componentes UI
print("\n[3] Verificando componentes UI...")
try:
    from smart_reports.ui.components.navigation.boton_pestana import CustomTabView
    print("  ✓ CustomTabView")
except Exception as e:
    print(f"  ✗ CustomTabView: {e}")

try:
    from smart_reports.ui.components.navigation.barra_lateral import ModernSidebar
    print("  ✓ ModernSidebar")
except Exception as e:
    print(f"  ✗ ModernSidebar: {e}")

# Test 4: Imports de menús
print("\n[4] Verificando imports de menús...")
menus_ok = []
menus_error = []

# Test Dashboard
try:
    from smart_reports.ui.views.menu_dashboard import show_dashboard_menu
    from smart_reports.ui.views.dashboard.panel_dashboards_gerenciales import DashboardsGerencialesPanel
    print("  ✓ Dashboard")
    menus_ok.append("Dashboard")
except Exception as e:
    print(f"  ✗ Dashboard: {e}")
    menus_error.append(("Dashboard", str(e)))

# Test Consultas
try:
    from smart_reports.ui.views.menu_consultas import show_consultas_menu
    from smart_reports.ui.views.panel_consultas import PanelConsultas
    print("  ✓ Consultas")
    menus_ok.append("Consultas")
except Exception as e:
    print(f"  ✗ Consultas: {e}")
    menus_error.append(("Consultas", str(e)))

# Test Importación
try:
    from smart_reports.ui.views.menu_actualizar import show_actualizar_menu
    from smart_reports.ui.views.configuracion.panel_importacion_datos import PanelImportacionDatos
    print("  ✓ Importación")
    menus_ok.append("Importación")
except Exception as e:
    print(f"  ✗ Importación: {e}")
    menus_error.append(("Importación", str(e)))

# Test Reportes
try:
    from smart_reports.ui.views.menu_reportes import show_reportes_menu, MenuReportes
    print("  ✓ Reportes")
    menus_ok.append("Reportes")
except Exception as e:
    print(f"  ✗ Reportes: {e}")
    menus_error.append(("Reportes", str(e)))

# Test Configuración
try:
    from smart_reports.ui.views.menu_configuracion import show_configuracion_menu
    from smart_reports.ui.views.configuracion.panel_configuracion import ConfiguracionPanel
    print("  ✓ Configuración")
    menus_ok.append("Configuración")
except Exception as e:
    print(f"  ✗ Configuración: {e}")
    menus_error.append(("Configuración", str(e)))

# Test 5: Crear ventana de prueba
print("\n[5] Creando ventana de prueba...")
try:
    root = ctk.CTk()
    root.geometry("800x600")
    root.title("Prueba de Menús")

    container = ctk.CTkFrame(root)
    container.pack(fill='both', expand=True)

    print("  ✓ Ventana creada")

    # Probar crear un panel
    if "Dashboard" in menus_ok:
        print("\n  Probando crear Dashboard...")
        try:
            panel = DashboardsGerencialesPanel(
                container,
                db_connection=None,
                usuario_actual={"nombre": "Test", "rol": "Admin"}
            )
            print("    ✓ Dashboard se crea correctamente")
        except Exception as e:
            print(f"    ✗ Error creando Dashboard: {e}")
            import traceback
            traceback.print_exc()

    root.destroy()

except Exception as e:
    print(f"  ✗ Error creando ventana: {e}")

# Resumen
print("\n" + "="*80)
print("RESUMEN")
print("="*80)
print(f"Menús funcionando: {len(menus_ok)}/5")
for menu in menus_ok:
    print(f"  ✓ {menu}")

if menus_error:
    print(f"\nMenús con errores: {len(menus_error)}")
    for menu, error in menus_error:
        print(f"  ✗ {menu}: {error}")

print("\n" + "="*80)
if len(menus_ok) == 5:
    print("✅ TODOS LOS MENÚS ESTÁN OK - La aplicación debería funcionar")
else:
    print("⚠️  ALGUNOS MENÚS TIENEN ERRORES - Revisa los detalles arriba")
print("="*80)
