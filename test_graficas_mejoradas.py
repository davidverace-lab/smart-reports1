"""
Script de prueba para verificar las mejoras de gráficas
- Tooltips hermosos
- Hover dramático
- Gradientes y sombras
- Modal fullscreen con animación
"""
import customtkinter as ctk
from src.interfaces.ui.views.panels.dashboard.panel_dashboards_gerenciales import DashboardsGerencialesPanel
from config.gestor_temas import get_theme_manager

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana principal
root = ctk.CTk()
root.title("🎨 Test Gráficas Mejoradas - Hutchison Ports")
root.geometry("1400x900")

# Inicializar gestor de temas
theme_manager = get_theme_manager()
theme_manager.set_dark_mode(True)

# Crear panel de dashboards
panel = DashboardsGerencialesPanel(root)
panel.pack(fill='both', expand=True)

print("\n" + "="*70)
print("🎨 SISTEMA DE GRÁFICAS MEJORADAS - LISTO")
print("="*70)
print("\n✨ CARACTERÍSTICAS IMPLEMENTADAS:")
print("  1. ✅ Tooltips hermosos con información detallada")
print("  2. ✅ Hover dramático (resalta + atenúa otras barras)")
print("  3. ✅ Gradientes profesionales en barras")
print("  4. ✅ Sombras y efectos 3D")
print("  5. ✅ Indicador visual de elementos ocultos")
print("  6. ✅ Modal fullscreen con animación deslizante")
print("  7. ✅ Ordenar con transiciones suaves")
print("  8. ✅ Click para ocultar/mostrar elementos")
print("\n📊 PRUEBA LO SIGUIENTE:")
print("  • Pasa el mouse sobre las barras → tooltip hermoso")
print("  • Click en 🔍 → Modal fullscreen con animación")
print("  • Click en barras → Ocultar/mostrar")
print("  • Botón ↓ Desc / ↑ Asc → Ordenar")
print("  • Botón ↻ Reset → Restaurar")
print("  • ESC en modal → Cerrar")
print("="*70 + "\n")

root.mainloop()
