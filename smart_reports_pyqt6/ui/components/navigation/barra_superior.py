"""Barra Superior Completa - PyQt6 con MODO CLARO/OSCURO"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class BarraSuperior(QFrame):
    """Barra superior con breadcrumb, búsqueda y acciones"""

    logout_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    notifications_clicked = pyqtSignal()
    theme_toggle_clicked = pyqtSignal()  # NUEVO: Signal para cambiar tema

    def __init__(self, username="Usuario", user_role="Usuario", theme_manager=None, parent=None):
        super().__init__(parent)

        self.username = username
        self.user_role = user_role
        self.theme_manager = theme_manager  # NUEVO

        self.setObjectName("barraSuperior")
        self.setFixedHeight(70)

        self._create_ui()
    
    def _create_ui(self):
        """Crear interfaz de la barra superior"""
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)
        
        # Breadcrumb / Título de sección
        self.title_label = QLabel("Dashboard")
        self.title_label.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        layout.addWidget(self.title_label)
        
        layout.addStretch()

        # Botón MODO CLARO/OSCURO - CRÍTICO
        self.theme_btn = QPushButton("🌙" if self.theme_manager and not self.theme_manager.is_dark_mode() else "☀️")
        self.theme_btn.setFont(QFont("Arial", 20))
        self.theme_btn.setFixedSize(45, 45)
        self.theme_btn.clicked.connect(self._toggle_theme)
        self.theme_btn.setToolTip("Cambiar a modo claro/oscuro")
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        layout.addWidget(self.theme_btn)

        # Botón de notificaciones
        notifications_btn = QPushButton("🔔")
        notifications_btn.setFont(QFont("Arial", 18))
        notifications_btn.setFixedSize(40, 40)
        notifications_btn.clicked.connect(self.notifications_clicked.emit)
        notifications_btn.setToolTip("Notificaciones")
        layout.addWidget(notifications_btn)

        # Botón de configuración
        settings_btn = QPushButton("⚙️")
        settings_btn.setFont(QFont("Arial", 18))
        settings_btn.setFixedSize(40, 40)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        settings_btn.setToolTip("Configuración")
        layout.addWidget(settings_btn)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFixedWidth(1)
        layout.addWidget(separator)
        
        # Info de usuario
        user_container = QWidget()
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)
        
        # Icono de usuario
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Arial", 24))
        user_layout.addWidget(user_icon)
        
        # Nombre y rol
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(0)
        
        username_label = QLabel(self.username)
        username_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        user_info_layout.addWidget(username_label)
        
        role_label = QLabel(self.user_role)
        role_label.setFont(QFont("Montserrat", 9))
        role_label.setStyleSheet("color: #888888;")
        user_info_layout.addWidget(role_label)
        
        user_layout.addWidget(user_info)
        
        layout.addWidget(user_container)
        
        # Botón de cerrar sesión
        logout_btn = QPushButton("🚪")
        logout_btn.setFont(QFont("Arial", 18))
        logout_btn.setFixedSize(40, 40)
        logout_btn.clicked.connect(self.logout_clicked.emit)
        logout_btn.setToolTip("Cerrar Sesión")
        layout.addWidget(logout_btn)
    
    def set_title(self, title):
        """Establecer título de la sección actual"""
        self.title_label.setText(title)

    def _toggle_theme(self):
        """Cambiar entre modo claro y oscuro"""
        if self.theme_manager:
            self.theme_manager.toggle_theme()
            # Actualizar icono del botón
            is_dark = self.theme_manager.is_dark_mode()
            self.theme_btn.setText("☀️" if is_dark else "🌙")
            # Emitir señal
            self.theme_toggle_clicked.emit()
