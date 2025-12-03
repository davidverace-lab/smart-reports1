"""
Panel de Configuración con navegación interna - PyQt6
Migrado desde CustomTkinter con sistema de fragments
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ConfigCard(QFrame):
    """Tarjeta de configuración clickeable"""

    clicked = pyqtSignal()

    def __init__(self, icon: str, title: str, description: str, button_text: str = "Abrir", theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(220)

        # Aplicar tema
        self._apply_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Icono y título - MUCHO MÁS GRANDE SIN BORDES
        header_label = QLabel(f"{icon} {title}")
        header_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 22 a 24
        is_dark = theme_manager.is_dark_mode() if theme_manager else False
        text_color = "#ffffff" if is_dark else "#003087"
        header_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(header_label)

        # Descripción - MUCHO MÁS GRANDE SIN BORDES
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Montserrat", 16))  # MUCHO MÁS GRANDE: de 14 a 16
        desc_color = "#b0b0b0" if is_dark else "#666666"
        desc_label.setStyleSheet(f"color: {desc_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(desc_label)

        layout.addStretch()

        # Botón - MÁS GRANDE
        btn = QPushButton(button_text)
        btn.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 14 a 16
        btn.setFixedHeight(50)  # MÁS ALTO: de 45 a 50
        btn.setStyleSheet("""
            QPushButton {
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.clicked.emit)
        layout.addWidget(btn)

    def _apply_theme(self):
        """Aplicar tema"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"

        self.setStyleSheet(f"""
            ConfigCard {{
                background-color: {bg_color};
                border: 2px solid #003087;
                border-radius: 15px;
            }}
            ConfigCard:hover {{
                border: 3px solid #003087;
            }}
        """)


class ConfigMainView(QWidget):
    """Vista principal de configuración con grid 2x2"""

    gestionar_empleados_clicked = pyqtSignal()
    soporte_tickets_clicked = pyqtSignal()
    historial_reportes_clicked = pyqtSignal()

    def __init__(self, theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self._create_ui()

    def _create_ui(self):
        """Crear UI"""

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(5)

        title = QLabel("⚙ Configuración")  # Ícono blanco: de ⚙️ a ⚙
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 36 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        subtitle = QLabel("Gestiona las opciones del sistema")
        subtitle.setFont(QFont("Montserrat", 20))  # MUCHO MÁS GRANDE: de 16 a 20
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(subtitle)

        main_layout.addWidget(header)

        # Grid 2x2 de tarjetas
        grid = QGridLayout()
        grid.setSpacing(15)

        # Card 1: Gestionar Empleados - ICONOS BLANCOS
        card1 = ConfigCard(
            "◉", "Gestionar Empleados",  # Ícono blanco: de 👥 a ◉
            "Agregar, editar o consultar empleados del sistema",
            "Gestionar", self.theme_manager
        )
        card1.clicked.connect(self.gestionar_empleados_clicked.emit)
        grid.addWidget(card1, 0, 0)

        # Card 2: Registro de Soporte - ICONOS BLANCOS
        card2 = ConfigCard(
            "✎", "Registro de Soporte",  # Ícono blanco: de 📝 a ✎
            "Registrar soporte brindado a usuarios por correo electrónico",
            "Registrar", self.theme_manager
        )
        card2.clicked.connect(self.soporte_tickets_clicked.emit)
        grid.addWidget(card2, 0, 1)

        # Card 3: Historial de Reportes - ICONOS BLANCOS
        card3 = ConfigCard(
            "◫", "Historial de Reportes",  # Ícono blanco: de 📋 a ◫
            "Ver y descargar reportes PDF generados anteriormente",
            "Ver Historial", self.theme_manager
        )
        card3.clicked.connect(self.historial_reportes_clicked.emit)
        grid.addWidget(card3, 1, 0)

        # Card 4: Acerca de - ICONOS BLANCOS
        card4 = ConfigCard(
            "◎", "Acerca de",  # Ícono blanco: de ℹ️ a ◎
            "Información de la versión y del desarrollador",
            "Ver Info", self.theme_manager
        )
        card4.clicked.connect(self._show_about)
        grid.addWidget(card4, 1, 1)

        main_layout.addLayout(grid)
        main_layout.addStretch()

    def _show_about(self):
        """Mostrar acerca de"""
        QMessageBox.information(
            self,
            "Acerca de",
            "SMART REPORTS V2.0\n\n"
            "SISTEMA DE GESTIÓN DE CAPACITACIONES\n"
            "INSTITUTO HUTCHISON PORTS\n\n"
            "Desarrollado por: David Vera\n"
            "© 2025 - TODOS LOS DERECHOS RESERVADOS"
        )


class GestionUsuariosView(QWidget):
    """Vista de gestión de usuarios"""

    back_clicked = pyqtSignal()

    def __init__(self, theme_manager=None, db_connection=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        self._create_ui()

    def _create_ui(self):
        """Crear UI"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header con botón volver
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        back_btn = QPushButton("← Volver")
        back_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE: de 13 a 14
        back_btn.setFixedHeight(50)  # MÁS ALTO: de 45 a 50
        back_btn.setFixedWidth(150)  # MÁS ANCHO: de 140 a 150
        back_btn.setStyleSheet("""
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
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_btn)

        title = QLabel("◉ Gestión de Usuarios")  # Ícono blanco: de 👥 a ◉
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 24 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        layout.addWidget(header)

        # Tabla de usuarios
        self.users_table = QTableWidget(0, 5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Unidad", "Rol"])
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setMinimumHeight(400)
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.users_table)

        # Botones de acción - NAVY BLUE ESTANDARIZADO
        actions_layout = QHBoxLayout()

        add_btn = QPushButton("+ Agregar Usuario")  # Ícono blanco: de ➕ a +
        add_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 15
        add_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        add_btn.setStyleSheet("""
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
        add_btn.clicked.connect(self._add_user)
        actions_layout.addWidget(add_btn)

        edit_btn = QPushButton("✎ Editar")  # Ícono blanco: de ✏️ a ✎
        edit_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 15
        edit_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        edit_btn.setStyleSheet("""
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
        edit_btn.clicked.connect(self._edit_user)
        actions_layout.addWidget(edit_btn)

        delete_btn = QPushButton("× Eliminar")  # Ícono blanco: de 🗑️ a ×
        delete_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 15
        delete_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #C53030;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9B2C2C;
            }
        """)
        delete_btn.clicked.connect(self._delete_user)  # CONECTAR FUNCIÓN
        actions_layout.addWidget(delete_btn)

        actions_layout.addStretch()

        layout.addLayout(actions_layout)

        # Cargar datos dummy
        self._load_dummy_users()

    def _load_dummy_users(self):
        """Cargar usuarios dummy"""
        data = [
            ["1", "Juan Pérez", "juan@hp.com", "ICAVE", "Usuario"],
            ["2", "María García", "maria@hp.com", "TNG", "Admin"],
            ["3", "Carlos López", "carlos@hp.com", "ECV", "Usuario"],
        ]

        self.users_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.users_table.setItem(row, col, QTableWidgetItem(value))

    def _add_user(self):
        """Agregar nuevo usuario"""
        QMessageBox.information(self, "Agregar Usuario", "Funcionalidad de agregar usuario\n(En desarrollo)")

    def _edit_user(self):
        """Editar usuario seleccionado"""
        selected_rows = self.users_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Sin Selección", "Por favor seleccione un usuario para editar")
            return
        QMessageBox.information(self, "Editar Usuario", "Funcionalidad de editar usuario\n(En desarrollo)")

    def _delete_user(self):
        """Eliminar usuario seleccionado"""
        selected_rows = self.users_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Sin Selección", "Por favor seleccione un usuario para eliminar")
            return

        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro de eliminar este usuario?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.users_table.removeRow(selected_rows[0].row())
            QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente")


class SoporteTicketsView(QWidget):
    """Vista de soporte/tickets"""

    back_clicked = pyqtSignal()

    def __init__(self, theme_manager=None, db_connection=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        self._create_ui()

    def _create_ui(self):
        """Crear UI"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        back_btn = QPushButton("← Volver")
        back_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE: de 13 a 14
        back_btn.setFixedHeight(50)  # MÁS ALTO: de 45 a 50
        back_btn.setFixedWidth(150)  # MÁS ANCHO: de 140 a 150
        back_btn.setStyleSheet("""
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
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_btn)

        title = QLabel("✎ Registro de Soporte")  # Ícono blanco: de 📝 a ✎
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 24 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        layout.addWidget(header)

        # Formulario
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)

        # Usuario - MÁS GRANDE SIN BORDES
        user_label = QLabel("Usuario:")
        user_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#ffffff" if is_dark else "#003087"
        user_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        form_layout.addWidget(user_label)

        self.user_entry = QLineEdit()
        self.user_entry.setPlaceholderText("Email del usuario")
        self.user_entry.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.user_entry.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        form_layout.addWidget(self.user_entry)

        # Asunto - MÁS GRANDE SIN BORDES
        subject_label = QLabel("Asunto:")
        subject_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        subject_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        form_layout.addWidget(subject_label)

        self.subject_entry = QLineEdit()
        self.subject_entry.setPlaceholderText("Asunto del ticket")
        self.subject_entry.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.subject_entry.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        form_layout.addWidget(self.subject_entry)

        # Descripción - MÁS GRANDE SIN BORDES
        desc_label = QLabel("Descripción:")
        desc_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        desc_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        form_layout.addWidget(desc_label)

        self.desc_text = QTextEdit()
        self.desc_text.setPlaceholderText("Descripción del soporte brindado...")
        self.desc_text.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.desc_text.setMinimumHeight(150)
        form_layout.addWidget(self.desc_text)

        # Botón registrar - MÁS GRANDE
        register_btn = QPushButton("✓ Registrar Ticket")  # Ícono blanco: de ✅ a ✓
        register_btn.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 14 a 16
        register_btn.setFixedHeight(55)  # MÁS ALTO: de 50 a 55
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.clicked.connect(self._register_ticket)
        form_layout.addWidget(register_btn)

        layout.addWidget(form_frame)
        layout.addStretch()

    def _register_ticket(self):
        """Registrar ticket"""
        QMessageBox.information(self, "Éxito", "Ticket registrado correctamente")


class HistorialReportesView(QWidget):
    """Vista de historial de reportes"""

    back_clicked = pyqtSignal()

    def __init__(self, theme_manager=None, db_connection=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        self._create_ui()

    def _create_ui(self):
        """Crear UI"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        back_btn = QPushButton("← Volver")
        back_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE: de 13 a 14
        back_btn.setFixedHeight(50)  # MÁS ALTO: de 45 a 50
        back_btn.setFixedWidth(150)  # MÁS ANCHO: de 140 a 150
        back_btn.setStyleSheet("""
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
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_btn)

        title = QLabel("◫ Historial de Reportes")  # Ícono blanco: de 📋 a ◫
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 24 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        layout.addWidget(header)

        # Tabla de reportes
        self.reports_table = QTableWidget(0, 5)
        self.reports_table.setHorizontalHeaderLabels(["Fecha", "Tipo", "Usuario", "Estado", "Acciones"])
        self.reports_table.setAlternatingRowColors(True)
        self.reports_table.setMinimumHeight(400)
        self.reports_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.reports_table)

        # Cargar datos dummy
        self._load_dummy_reports()

    def _load_dummy_reports(self):
        """Cargar reportes dummy"""
        data = [
            ["2025-01-15", "Global", "admin@hp.com", "✅ Completado"],
            ["2025-01-14", "Por Unidad", "user@hp.com", "✅ Completado"],
            ["2025-01-13", "Por Usuario", "admin@hp.com", "✅ Completado"],
        ]

        self.reports_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if col == 4:  # Columna de acciones
                    btn = QPushButton("↓ Descargar")  # Ícono blanco: de 📄 a ↓
                    btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #003087;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            padding: 8px 15px;
                        }
                        QPushButton:hover {
                            background-color: #004ba0;
                        }
                    """)
                    self.reports_table.setCellWidget(row, col, btn)
                else:
                    self.reports_table.setItem(row, col, QTableWidgetItem(value))


class ConfiguracionPanel(QWidget):
    """Panel de Configuración con navegación interna tipo stack"""

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        # Stack para navegación
        self.stack = QStackedWidget()

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear UI"""

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        # Vista principal
        self.main_view = ConfigMainView(self.theme_manager)
        self.main_view.gestionar_empleados_clicked.connect(self._open_gestion_usuarios)
        self.main_view.soporte_tickets_clicked.connect(self._open_soporte_tickets)
        self.main_view.historial_reportes_clicked.connect(self._open_historial_reportes)
        self.stack.addWidget(self.main_view)

    def _open_gestion_usuarios(self):
        """Abrir gestión de usuarios"""
        view = GestionUsuariosView(self.theme_manager, self.db_connection)
        view.back_clicked.connect(lambda: self._go_back(view))
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)

    def _open_soporte_tickets(self):
        """Abrir soporte/tickets"""
        view = SoporteTicketsView(self.theme_manager, self.db_connection)
        view.back_clicked.connect(lambda: self._go_back(view))
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)

    def _open_historial_reportes(self):
        """Abrir historial de reportes"""
        view = HistorialReportesView(self.theme_manager, self.db_connection)
        view.back_clicked.connect(lambda: self._go_back(view))
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)

    def _go_back(self, view):
        """Volver a vista principal"""
        self.stack.setCurrentWidget(self.main_view)
        self.stack.removeWidget(view)
        view.deleteLater()
