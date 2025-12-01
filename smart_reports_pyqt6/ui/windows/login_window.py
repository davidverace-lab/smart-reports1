"""
Login Window - PyQt6
Ventana de inicio de sesión para Smart Reports
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap


class LoginWindow(QMainWindow):
    """Ventana de login con PyQt6"""

    # Señal emitida cuando el login es exitoso
    login_successful = pyqtSignal(str, str)  # username, role

    def __init__(self, app, theme_manager):
        super().__init__()

        self.app = app
        self.theme_manager = theme_manager

        # Configurar ventana
        self.setWindowTitle("Smart Reports - Login")
        self.setMinimumSize(800, 600)

        # Forzar modo claro al iniciar
        if self.theme_manager:
            if self.theme_manager.is_dark_mode():
                self.theme_manager.toggle_theme(self.app)

        # Crear UI
        self._create_ui()

        # Mostrar en pantalla completa
        self.showMaximized()

    def _center_window(self):
        """Centrar ventana en la pantalla"""
        screen = self.app.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _create_ui(self):
        """Crear interfaz de usuario"""

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel izquierdo (branding)
        left_panel = self._create_left_panel()
        main_layout.addWidget(left_panel, 1)

        # Panel derecho (formulario)
        right_panel = self._create_right_panel()
        main_layout.addWidget(right_panel, 1)

    def _create_left_panel(self):
        """Crear panel izquierdo con branding"""

        panel = QFrame()
        panel.setObjectName("leftPanel")
        panel.setStyleSheet("""
            #leftPanel {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #002E6D,
                    stop:1 #0066CC
                );
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Logo de Instituto HP (imagen)
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Intentar cargar logo
        logo_path = "assets/images/LogoInstitutoHP-blanco.png"
        try:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Escalar logo manteniendo aspect ratio
                scaled_pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                # Fallback si no se encuentra la imagen
                logo_label.setText("INSTITUTO\nHUTCHISON PORTS")
                logo_label.setFont(QFont("Montserrat", 32, QFont.Weight.Bold))
                logo_label.setStyleSheet("color: white; background: transparent;")
                logo_label.setWordWrap(True)
        except Exception as e:
            # Fallback si hay error
            logo_label.setText("INSTITUTO\nHUTCHISON PORTS")
            logo_label.setFont(QFont("Montserrat", 32, QFont.Weight.Bold))
            logo_label.setStyleSheet("color: white; background: transparent;")
            logo_label.setWordWrap(True)

        layout.addWidget(logo_label)

        layout.addSpacing(40)

        # Título (movido abajo)
        title_label = QLabel("SMART REPORTS")
        title_label.setFont(QFont("Montserrat", 26, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(title_label)

        return panel

    def _create_right_panel(self):
        """Crear panel derecho con formulario de login"""

        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(60, 40, 60, 40)

        # Título del formulario
        form_title = QLabel("Iniciar Sesión")
        form_title.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(form_title)

        # Subtítulo
        form_subtitle = QLabel("Ingresa tus credenciales")
        form_subtitle.setFont(QFont("Montserrat", 12))
        form_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_subtitle.setStyleSheet("color: #888888; margin-bottom: 30px;")
        layout.addWidget(form_subtitle)

        # Campo de usuario
        user_label = QLabel("Usuario")
        user_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        user_label.setStyleSheet("color: #003087;")
        layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu usuario")
        self.username_input.setFixedHeight(45)
        self.username_input.setFont(QFont("Montserrat", 11))
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #003087;
            }
        """)
        self.username_input.returnPressed.connect(self._handle_login)
        layout.addWidget(self.username_input)

        layout.addSpacing(20)

        # Campo de contraseña
        pass_label = QLabel("Contraseña")
        pass_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        pass_label.setStyleSheet("color: #003087;")
        layout.addWidget(pass_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setFont(QFont("Montserrat", 11))
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #003087;
            }
        """)
        self.password_input.returnPressed.connect(self._handle_login)
        layout.addWidget(self.password_input)

        layout.addSpacing(30)

        # Botón de login
        self.login_button = QPushButton("INICIAR SESIÓN")
        self.login_button.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        self.login_button.setFixedHeight(55)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
            QPushButton:pressed {
                background-color: #002060;
            }
        """)
        self.login_button.clicked.connect(self._handle_login)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.login_button)

        # Spacer para empujar contenido hacia arriba
        layout.addStretch()

        return panel

    def _toggle_theme(self):
        """Cambiar tema oscuro/claro"""
        new_theme = self.theme_manager.toggle_theme(self.app)
        print(f"✅ Tema cambiado a: {new_theme}")

    def _handle_login(self):
        """Manejar intento de login"""

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Validación básica
        if not username or not password:
            QMessageBox.warning(
                self,
                "Campos vacíos",
                "Por favor ingresa usuario y contraseña"
            )
            return

        # TODO: Aquí va la autenticación real contra la base de datos
        # Por ahora, aceptamos cualquier credencial (DEMO)

        # Determinar rol (DEMO - debe venir de la BD)
        role = "admin" if "admin" in username.lower() else "user"

        print(f"✅ Login exitoso: {username} ({role})")

        # Emitir señal de login exitoso
        self.login_successful.emit(username, role)

        # Cerrar ventana de login y mostrar ventana principal
        self._show_main_window(username, role)

    def _show_main_window(self, username: str, role: str):
        """Mostrar ventana principal"""

        try:
            from smart_reports_pyqt6.ui.windows.main_window import MainWindow

            # Crear ventana principal
            self.main_window = MainWindow(self.app, self.theme_manager, username, role)
            self.main_window.show()

            # Cerrar ventana de login
            self.close()

        except Exception as e:
            print(f"❌ Error abriendo ventana principal: {e}")
            import traceback
            traceback.print_exc()

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo abrir la ventana principal:\n{e}\n\nVerifica que main_window.py esté implementado."
            )
