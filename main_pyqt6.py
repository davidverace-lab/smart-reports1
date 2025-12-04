"""
SMART REPORTS - INSTITUTO HUTCHISON PORTS
Main Application - PyQt6 Version
Versión 3.0 - Migración completa a PyQt6
"""

import sys
import os
from pathlib import Path

# Configurar paths
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# CRÍTICO: Importar QtWebEngineWidgets ANTES de crear QApplication
# Esto es necesario para que QWebEngineView funcione correctamente
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    print("✅ QtWebEngineWidgets importado correctamente")
except ImportError as e:
    print(f"⚠️ Error importando QtWebEngineWidgets: {e}")
    print("   Instalar con: pip install PyQt6-WebEngine")

# Importar configuración
from smart_reports_pyqt6.config.themes import ThemeManager
from smart_reports_pyqt6.ui.windows.pyqt6_login_window import LoginWindow


def main():
    """Función principal de la aplicación PyQt6"""

    # Establecer atributo para OpenGL (requerido por QtWebEngine)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    # Crear aplicación Qt
    app = QApplication(sys.argv)

    # Configurar nombre y organización
    app.setApplicationName("Smart Reports - Hutchison Ports")
    app.setOrganizationName("Instituto Hutchison Ports")
    app.setOrganizationDomain("hutchison.com")

    # Configurar fuente predeterminada
    font = QFont("Montserrat", 10)
    app.setFont(font)

    # Habilitar High DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Crear gestor de temas
    theme_manager = ThemeManager()

    # Aplicar tema oscuro por defecto
    theme_manager.set_theme(app, 'dark')

    # Crear y mostrar ventana de login
    login_window = LoginWindow(app, theme_manager)
    login_window.show()

    print("🚀 Smart Reports PyQt6 iniciado")
    print(f"   Tema: {theme_manager.current_theme}")
    print(f"   Python: {sys.version}")
    print(f"   PyQt6: OK")

    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
