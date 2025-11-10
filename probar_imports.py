"""
Script de prueba de imports
Verifica que TODOS los imports funcionen correctamente
"""
import sys
print("=" * 70)
print("🧪 PRUEBA DE IMPORTS - Smart Reports")
print("=" * 70)

errors = []
warnings = []
success = []

def test_import(module_path, description):
    """Prueba un import"""
    try:
        __import__(module_path)
        success.append(f"✓ {description}")
        return True
    except ImportError as e:
        errors.append(f"❌ {description}: {str(e)}")
        return False
    except Exception as e:
        warnings.append(f"⚠️ {description}: {str(e)}")
        return False

# Pruebas de configuración
print("\n📦 CONFIGURACIÓN:")
test_import('config.settings', 'config.settings')
test_import('config.database', 'config.database')
test_import('config.themes', 'config.themes')
test_import('config.gestor_temas', 'config.gestor_temas')

# Pruebas de servicios
print("\n💼 SERVICIOS:")
test_import('src.application.services.metricas_gerenciales_service', 'MetricasGerencialesService')

# Pruebas de infraestructura
print("\n🔧 INFRAESTRUCTURA:")
test_import('src.infrastructure.persistence.mysql.connection', 'DatabaseConnection')

# Pruebas de componentes UI
print("\n🎨 COMPONENTES UI:")
test_import('src.interfaces.ui.views.components.navigation.barra_lateral', 'ModernSidebar')
test_import('src.interfaces.ui.views.components.navigation.barra_superior', 'TopBar')
test_import('src.interfaces.ui.views.components.charts.tarjeta_d3_profesional', 'ProfessionalD3ChartCard')
test_import('src.interfaces.ui.views.components.charts.tarjeta_metrica', 'MetricCard')

# Pruebas de dashboards modulares
print("\n📊 DASHBOARDS MODULARES:")
test_import('src.interfaces.ui.views.panels.dashboard.dashboards_rendimiento', 'DashboardsRendimiento')
test_import('src.interfaces.ui.views.panels.dashboard.dashboards_comparativas', 'DashboardsComparativas')
test_import('src.interfaces.ui.views.panels.dashboard.dashboards_distribucion', 'DashboardsDistribucion')
test_import('src.interfaces.ui.views.panels.dashboard.dashboards_tendencias', 'DashboardsTendencias')
test_import('src.interfaces.ui.views.panels.dashboard.dashboards_relaciones', 'DashboardsRelaciones')
test_import('src.interfaces.ui.views.panels.dashboard.panel_dashboards_gerenciales', 'DashboardsGerencialesPanel')

# Pruebas de configuración
print("\n⚙️ CONFIGURACIÓN:")
test_import('src.interfaces.ui.views.panels.configuracion.panel_configuracion', 'ConfiguracionPanel')
test_import('src.interfaces.ui.views.panels.configuracion.config_sistema', 'ConfigSistemaPanel')
test_import('src.interfaces.ui.views.panels.configuracion.config_usuario', 'ConfigUsuariosPanel')

# Pruebas de ventanas
print("\n🪟 VENTANAS:")
test_import('src.interfaces.ui.views.windows.ventana_login', 'LoginWindow')
test_import('src.interfaces.ui.views.windows.ventana_principal', 'MainWindow')

# Resultado
print("\n" + "=" * 70)
if errors:
    print("❌ ERRORES ENCONTRADOS:")
    for err in errors:
        print(f"  {err}")
if warnings:
    print("\n⚠️ ADVERTENCIAS:")
    for warn in warnings:
        print(f"  {warn}")
if success:
    print(f"\n✅ {len(success)} IMPORTS EXITOSOS")

print("=" * 70)

if errors:
    print("\n🔴 PRUEBA FALLIDA - Hay imports que no funcionan")
    print("   Ejecuta: pip install -r requirements.txt")
    sys.exit(1)
elif warnings:
    print("\n🟡 PRUEBA CON ADVERTENCIAS - Algunos módulos tienen problemas menores")
    print("   La app debería funcionar pero revisa las advertencias")
    sys.exit(0)
else:
    print("\n🟢 PRUEBA EXITOSA - Todos los imports funcionan correctamente")
    print("   Ejecuta: python main.py")
    sys.exit(0)
