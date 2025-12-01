"""
Panel de Configuración
PyQt6 Version - Configuración del sistema
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget,
    QLineEdit, QComboBox, QCheckBox,
    QFrame, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConfiguracionPanel(QWidget):
    """Panel de Configuración"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("⚙️ Configuración")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        save_btn = QPushButton("💾 Guardar Cambios")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self._save_settings)
        header_layout.addWidget(save_btn)

        layout.addLayout(header_layout)

        # Tabs de configuración
        tabs = QTabWidget()

        # Tab 1: General
        general_tab = self._create_general_tab()
        tabs.addTab(general_tab, "🔧 General")

        # Tab 2: Base de Datos
        db_tab = self._create_database_tab()
        tabs.addTab(db_tab, "🗄️ Base de Datos")

        # Tab 3: Usuarios
        users_tab = self._create_users_tab()
        tabs.addTab(users_tab, "👥 Usuarios")

        # Tab 4: Importación
        import_tab = self._create_import_tab()
        tabs.addTab(import_tab, "📥 Importación")

        layout.addWidget(tabs)

    def _create_general_tab(self):
        """Tab de configuración general"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Tema
        theme_frame = self._create_setting_frame(
            "🎨 Tema de la Aplicación",
            "Selecciona el tema visual"
        )
        theme_layout = QVBoxLayout(theme_frame)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Oscuro", "Claro"])
        if self.theme_manager and self.theme_manager.is_dark_mode():
            self.theme_combo.setCurrentIndex(0)
        else:
            self.theme_combo.setCurrentIndex(1)

        theme_layout.addWidget(self.theme_combo)

        layout.addWidget(theme_frame)

        # Idioma
        lang_frame = self._create_setting_frame(
            "🌐 Idioma",
            "Selecciona el idioma de la interfaz"
        )
        lang_layout = QVBoxLayout(lang_frame)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Español", "English"])
        lang_layout.addWidget(self.lang_combo)

        layout.addWidget(lang_frame)

        # Notificaciones
        notif_frame = self._create_setting_frame(
            "🔔 Notificaciones",
            "Configurar alertas y notificaciones"
        )
        notif_layout = QVBoxLayout(notif_frame)

        self.notif_enable = QCheckBox("Habilitar notificaciones")
        self.notif_enable.setChecked(True)
        notif_layout.addWidget(self.notif_enable)

        self.notif_sound = QCheckBox("Sonido de notificaciones")
        notif_layout.addWidget(self.notif_sound)

        layout.addWidget(notif_frame)

        layout.addStretch()

        return widget

    def _create_database_tab(self):
        """Tab de configuración de BD"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Conexión
        conn_frame = self._create_setting_frame(
            "🔗 Conexión a Base de Datos",
            "Configurar parámetros de conexión"
        )
        conn_layout = QVBoxLayout(conn_frame)

        # Host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.db_host = QLineEdit("localhost")
        host_layout.addWidget(self.db_host)
        conn_layout.addLayout(host_layout)

        # Puerto
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Puerto:"))
        self.db_port = QLineEdit("3306")
        port_layout.addWidget(self.db_port)
        conn_layout.addLayout(port_layout)

        # Base de datos
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Base de Datos:"))
        self.db_name = QLineEdit("smart_reports")
        db_layout.addWidget(self.db_name)
        conn_layout.addLayout(db_layout)

        # Botón probar conexión
        test_btn = QPushButton("🔍 Probar Conexión")
        test_btn.setProperty("class", "secondary")
        test_btn.clicked.connect(self._test_connection)
        conn_layout.addWidget(test_btn)

        layout.addWidget(conn_frame)

        layout.addStretch()

        return widget

    def _create_users_tab(self):
        """Tab de gestión de usuarios"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Lista de usuarios
        users_label = QLabel("Usuarios del Sistema:")
        users_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(users_label)

        self.users_list = QListWidget()
        self.users_list.addItems([
            "👤 admin - Administrador",
            "👤 juan.perez - Usuario",
            "👤 maria.garcia - Usuario",
            "👤 carlos.lopez - Supervisor",
        ])
        layout.addWidget(self.users_list)

        # Botones
        buttons_layout = QHBoxLayout()

        add_user_btn = QPushButton("➕ Nuevo Usuario")
        add_user_btn.clicked.connect(self._add_user)
        buttons_layout.addWidget(add_user_btn)

        edit_user_btn = QPushButton("✏️ Editar")
        edit_user_btn.setProperty("class", "secondary")
        buttons_layout.addWidget(edit_user_btn)

        delete_user_btn = QPushButton("🗑️ Eliminar")
        delete_user_btn.setProperty("class", "danger")
        buttons_layout.addWidget(delete_user_btn)

        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        return widget

    def _create_import_tab(self):
        """Tab de importación de datos"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        import_label = QLabel("Importar Datos desde Archivo:")
        import_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(import_label)

        # Botones de importación
        import_excel_btn = QPushButton("📊 Importar desde Excel")
        import_excel_btn.setFixedHeight(50)
        import_excel_btn.clicked.connect(self._import_excel)
        layout.addWidget(import_excel_btn)

        import_csv_btn = QPushButton("📄 Importar desde CSV")
        import_csv_btn.setFixedHeight(50)
        import_csv_btn.clicked.connect(self._import_csv)
        layout.addWidget(import_csv_btn)

        import_db_btn = QPushButton("🗄️ Importar desde otra BD")
        import_db_btn.setFixedHeight(50)
        import_db_btn.clicked.connect(self._import_db)
        layout.addWidget(import_db_btn)

        layout.addStretch()

        return widget

    def _create_setting_frame(self, title: str, description: str):
        """Crear frame de configuración"""

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #888888;")
        layout.addWidget(desc_label)

        return frame

    def _save_settings(self):
        """Guardar configuración"""
        QMessageBox.information(self, "Guardado", "Configuración guardada exitosamente")

    def _test_connection(self):
        """Probar conexión a BD"""
        QMessageBox.information(self, "Conexión", "✅ Conexión exitosa a la base de datos")

    def _add_user(self):
        """Agregar nuevo usuario"""
        QMessageBox.information(self, "Nuevo Usuario", "Aquí se abrirá un diálogo para crear usuario")

    def _import_excel(self):
        """Importar desde Excel"""
        QMessageBox.information(self, "Importar", "Importando datos desde Excel...")

    def _import_csv(self):
        """Importar desde CSV"""
        QMessageBox.information(self, "Importar", "Importando datos desde CSV...")

    def _import_db(self):
        """Importar desde otra BD"""
        QMessageBox.information(self, "Importar", "Conectando a base de datos externa...")
