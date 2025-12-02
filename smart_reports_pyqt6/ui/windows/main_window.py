"""
Main Window - PyQt6
Ventana principal de Smart Reports con navegación lateral colapsable
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importar ModernSidebar
from smart_reports_pyqt6.ui.components.navigation.modern_sidebar import ModernSidebar


class MainWindow(QMainWindow):
    """Ventana principal con navegación y paneles"""

    def __init__(self, app, theme_manager, username: str, role: str):
        super().__init__()

        self.app = app
        self.theme_manager = theme_manager
        self.username = username
        self.role = role

        # Configurar ventana
        self.setWindowTitle(f"Smart Reports - {username}")
        self.setMinimumSize(1400, 800)

        # Estado
        self.current_panel = "dashboard"

        # Crear UI
        self._create_ui()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

        # Mostrar pantalla completa por defecto
        self.showMaximized()

    def _create_ui(self):
        """Crear interfaz de usuario"""

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar moderna con botón hamburguesa (COLAPSABLE)
        navigation_callbacks = {
            'dashboard': lambda: self._navigate_to('dashboard'),
            'consultas': lambda: self._navigate_to('consultas'),
            'importacion': lambda: self._navigate_to('importacion'),
            'reportes': lambda: self._navigate_to('reportes'),
            'configuracion': lambda: self._navigate_to('config'),
        }

        self.sidebar = ModernSidebar(
            parent=central_widget,
            navigation_callbacks=navigation_callbacks,
            theme_manager=self.theme_manager
        )
        # Conectar signal de logout
        self.sidebar.logout_clicked.connect(self._logout)
        main_layout.addWidget(self.sidebar)

        # Contenedor de paneles
        self.content_area = self._create_content_area()
        main_layout.addWidget(self.content_area, 1)

    def _create_top_bar(self):
        """Crear barra superior con rol e institución"""

        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(60)

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#383838" if is_dark else "#e0e0e0"
        text_color = "#ffffff" if is_dark else "#003087"

        top_bar.setStyleSheet(f"""
            #topBar {{
                background-color: {bg_color};
                border-bottom: 1px solid {border_color};
            }}
        """)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(30, 10, 30, 10)

        # Mensaje de bienvenida con rol
        welcome_label = QLabel(f"Bienvenido {self.role.upper()}")
        welcome_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        welcome_label.setStyleSheet(f"color: {text_color};")
        layout.addWidget(welcome_label)

        layout.addStretch()

        # Instituto a la derecha
        instituto_label = QLabel("Instituto Hutchison Ports")
        instituto_label.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
        instituto_label.setStyleSheet(f"color: {text_color};")
        layout.addWidget(instituto_label)

        return top_bar

    def _create_content_area(self):
        """Crear área de contenido con stack de paneles"""

        # Container principal para top bar + contenido
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top bar con info de usuario
        top_bar = self._create_top_bar()
        content_layout.addWidget(top_bar)

        # Scroll area para contener el stacked widget
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Stacked widget para cambiar entre paneles
        self.panel_stack = QStackedWidget()

        # Crear paneles REALES (migrados desde CustomTkinter)
        self.panels = {}

        # Importar paneles
        from smart_reports_pyqt6.ui.views.panel_dashboard import DashboardPanel
        from smart_reports_pyqt6.ui.views.panel_graficos import GraficosPanel
        from smart_reports_pyqt6.ui.views.panel_consultas import ConsultasPanel
        from smart_reports_pyqt6.ui.views.panel_reportes import ReportesPanel
        from smart_reports_pyqt6.ui.views.panel_configuracion import ConfiguracionPanel
        from smart_reports_pyqt6.ui.views.panel_importacion import PanelImportacion

        try:
            # Dashboard
            dashboard_panel = DashboardPanel(parent=self, theme_manager=self.theme_manager)
            self.panels['dashboard'] = dashboard_panel
            self.panel_stack.addWidget(dashboard_panel)
            print("✅ Panel Dashboard cargado")

            # Gráficos
            graficos_panel = GraficosPanel(parent=self, theme_manager=self.theme_manager)
            self.panels['graficos'] = graficos_panel
            self.panel_stack.addWidget(graficos_panel)
            print("✅ Panel Gráficos cargado")

            # Consultas
            consultas_panel = ConsultasPanel(parent=self, theme_manager=self.theme_manager)
            self.panels['consultas'] = consultas_panel
            self.panel_stack.addWidget(consultas_panel)
            print("✅ Panel Consultas cargado")

            # Reportes
            reportes_panel = ReportesPanel(parent=self, theme_manager=self.theme_manager)
            self.panels['reportes'] = reportes_panel
            self.panel_stack.addWidget(reportes_panel)
            print("✅ Panel Reportes cargado")

            # Configuración
            config_panel = ConfiguracionPanel(parent=self, theme_manager=self.theme_manager)
            self.panels['config'] = config_panel
            self.panel_stack.addWidget(config_panel)
            print("✅ Panel Configuración cargado")

            # Importación
            importacion_panel = PanelImportacion(parent=self, theme_manager=self.theme_manager)
            self.panels['importacion'] = importacion_panel
            self.panel_stack.addWidget(importacion_panel)
            print("✅ Panel Importación cargado")

        except Exception as e:
            print(f"❌ Error cargando paneles: {e}")
            import traceback
            traceback.print_exc()

            # Fallback a placeholder si hay error
            for panel_name in ["dashboard", "graficos", "consultas", "reportes", "config", "importacion"]:
                if panel_name not in self.panels:
                    panel = self._create_placeholder_panel(panel_name)
                    self.panels[panel_name] = panel
                    self.panel_stack.addWidget(panel)

        scroll.setWidget(self.panel_stack)
        content_layout.addWidget(scroll)

        return content_container

    def _create_placeholder_panel(self, panel_name: str):
        """Crear panel placeholder (temporal)"""

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        title = QLabel(f"Panel: {panel_name.capitalize()}")
        title.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(20)

        # Mensaje
        msg = QLabel(f"""
        <h3>🚧 Panel en construcción</h3>
        <p>Este panel será migrado desde CustomTkinter.</p>
        <p><b>Para migrar este panel:</b></p>
        <ol>
            <li>Crea <code>smart_reports_pyqt6/ui/views/panel_{panel_name}.py</code></li>
            <li>Implementa la clase <code>{panel_name.capitalize()}Panel</code></li>
            <li>Importa y usa en este archivo (main_window.py)</li>
        </ol>
        <p>Ver <b>GUIA_MIGRACION_PYQT6.md</b> para instrucciones detalladas.</p>
        """)
        msg.setFont(QFont("Montserrat", 11))
        msg.setWordWrap(True)
        layout.addWidget(msg)

        # Botón de ejemplo
        example_btn = QPushButton("📊 Ejemplo de gráfico D3.js")
        example_btn.setFixedHeight(50)
        example_btn.clicked.connect(self._show_example_chart)
        layout.addWidget(example_btn)

        layout.addStretch()

        return panel

    def _navigate_to(self, panel_key: str):
        """Navegar a un panel"""

        if panel_key not in self.panels:
            print(f"⚠️ Panel '{panel_key}' no existe")
            return

        print(f"📍 Navegando a: {panel_key}")

        # Actualizar panel actual
        self.current_panel = panel_key

        # Cambiar panel en stack
        panel_widget = self.panels[panel_key]
        self.panel_stack.setCurrentWidget(panel_widget)

        # Actualizar botón activo en sidebar
        self.sidebar.set_active(panel_key)

    def _on_theme_changed(self, new_theme: str):
        """Callback cuando cambia el tema"""
        print(f"🎨 MainWindow: Actualizando tema a {new_theme}")

        # Actualizar el top bar
        if hasattr(self, 'content_area'):
            # Recrear el top bar con los nuevos colores
            content_layout = self.content_area.layout()
            if content_layout and content_layout.count() > 0:
                old_top_bar = content_layout.itemAt(0).widget()
                if old_top_bar:
                    old_top_bar.deleteLater()
                    new_top_bar = self._create_top_bar()
                    content_layout.insertWidget(0, new_top_bar)

    def _toggle_theme(self):
        """Cambiar tema"""
        new_theme = self.theme_manager.toggle_theme(self.app)
        print(f"✅ Tema cambiado a: {new_theme}")

        # El sidebar y los paneles se actualizan automáticamente mediante sus callbacks

    def _logout(self):
        """Cerrar sesión"""

        print(f"👋 Cerrando sesión: {self.username}")

        # Cerrar ventana principal
        self.close()

        # Mostrar ventana de login nuevamente
        from smart_reports_pyqt6.ui.windows.login_window import LoginWindow

        self.login_window = LoginWindow(self.app, self.theme_manager)
        self.login_window.show()

    def _show_example_chart(self):
        """Mostrar ejemplo de gráfico D3.js (para testing)"""

        try:
            from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget
            from PyQt6.QtWidgets import QDialog, QVBoxLayout

            # Crear diálogo con gráfico
            dialog = QDialog(self)
            dialog.setWindowTitle("Ejemplo: Gráfico D3.js")
            dialog.setMinimumSize(800, 600)

            layout = QVBoxLayout(dialog)

            # Crear widget de gráfico
            chart = D3ChartWidget(dialog)

            # Datos de ejemplo
            datos = {
                'labels': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
                'values': [120, 190, 150, 280, 210]
            }

            # Cargar gráfico
            chart.set_chart('bar', 'Ventas Mensuales', datos, tema=self.theme_manager.current_theme)

            layout.addWidget(chart)

            dialog.exec()

        except Exception as e:
            print(f"❌ Error mostrando gráfico: {e}")
            import traceback
            traceback.print_exc()
