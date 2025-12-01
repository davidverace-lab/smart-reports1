"""
Main Window - PyQt6
Ventana principal de Smart Reports con navegación lateral
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


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

        # Sidebar (barra lateral de navegación)
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)

        # Contenedor de paneles
        self.content_area = self._create_content_area()
        main_layout.addWidget(self.content_area, 1)

    def _create_sidebar(self):
        """Crear barra lateral de navegación"""

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: """ + ("#2d2d2d" if self.theme_manager.is_dark_mode() else "#ffffff") + """;
                border-right: 1px solid """ + ("#383838" if self.theme_manager.is_dark_mode() else "#e0e0e0") + """;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        # Header con usuario
        header = self._create_sidebar_header()
        layout.addWidget(header)

        layout.addSpacing(20)

        # Menús de navegación
        self.menu_buttons = {}

        menus = [
            ("📊", "Dashboard", "dashboard"),
            ("📈", "Gráficos", "graficos"),
            ("🔍", "Consultas", "consultas"),
            ("📄", "Reportes", "reportes"),
            ("⚙️", "Configuración", "config"),
        ]

        for icon, label, key in menus:
            btn = self._create_menu_button(icon, label, key)
            self.menu_buttons[key] = btn
            layout.addWidget(btn)

        # Spacer para empujar botones hacia arriba
        layout.addStretch()

        # Botón de cambiar tema
        theme_btn = QPushButton("🌓 Tema")
        theme_btn.setProperty("class", "secondary")
        theme_btn.setFixedHeight(40)
        theme_btn.clicked.connect(self._toggle_theme)
        theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(theme_btn)

        # Botón de cerrar sesión
        logout_btn = QPushButton("🚪 Cerrar Sesión")
        logout_btn.setProperty("class", "danger")
        logout_btn.setFixedHeight(40)
        logout_btn.clicked.connect(self._logout)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(logout_btn)

        return sidebar

    def _create_sidebar_header(self):
        """Crear header de sidebar con info de usuario"""

        header = QFrame()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(10, 10, 10, 10)

        # Icono de usuario
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Arial", 32))
        user_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_icon)

        # Nombre de usuario
        username_label = QLabel(self.username)
        username_label.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(username_label)

        # Rol
        role_label = QLabel(f"Rol: {self.role.capitalize()}")
        role_label.setFont(QFont("Montserrat", 10))
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_label.setStyleSheet("color: #00D4AA;")
        layout.addWidget(role_label)

        return header

    def _create_menu_button(self, icon: str, label: str, key: str):
        """Crear botón de menú"""

        btn = QPushButton(f"{icon}  {label}")
        btn.setFont(QFont("Montserrat", 11))
        btn.setFixedHeight(45)
        btn.clicked.connect(lambda: self._navigate_to(key))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Estilo especial para botón activo
        if key == self.current_panel:
            btn.setProperty("class", "active")

        return btn

    def _create_content_area(self):
        """Crear área de contenido con stack de paneles"""

        # Scroll area para contener el stacked widget
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Stacked widget para cambiar entre paneles
        self.panel_stack = QStackedWidget()

        # Crear paneles (placeholders por ahora)
        self.panels = {}

        panel_names = ["dashboard", "graficos", "consultas", "reportes", "config"]

        for panel_name in panel_names:
            panel = self._create_placeholder_panel(panel_name)
            self.panels[panel_name] = panel
            self.panel_stack.addWidget(panel)

        scroll.setWidget(self.panel_stack)

        return scroll

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

        # Actualizar estilos de botones
        for key, btn in self.menu_buttons.items():
            if key == panel_key:
                btn.setProperty("class", "active")
            else:
                btn.setProperty("class", "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _toggle_theme(self):
        """Cambiar tema"""
        new_theme = self.theme_manager.toggle_theme(self.app)
        print(f"✅ Tema cambiado a: {new_theme}")

        # Actualizar sidebar
        self._update_sidebar_style()

    def _update_sidebar_style(self):
        """Actualizar estilo de sidebar según tema"""
        sidebar = self.findChild(QFrame, "sidebar")
        if sidebar:
            sidebar.setStyleSheet("""
                #sidebar {
                    background-color: """ + ("#2d2d2d" if self.theme_manager.is_dark_mode() else "#ffffff") + """;
                    border-right: 1px solid """ + ("#383838" if self.theme_manager.is_dark_mode() else "#e0e0e0") + """;
                }
            """)

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
