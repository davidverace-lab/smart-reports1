"""
Panel de Importación de Datos - PyQt6
Sistema básico para importar datos desde Excel
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PanelImportacion(QWidget):
    """Panel de Importación de Datos"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Variables
        self.archivo_training = None
        self.archivo_org = None

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        # Título y subtítulo
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title = QLabel("📥 Cruce e Importación de Datos")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        title_layout.addWidget(title)

        subtitle = QLabel("Sistema de validación y matching de datos CSOD")
        subtitle.setFont(QFont("Montserrat", 11))
        subtitle.setStyleSheet("color: #888888;")
        title_layout.addWidget(subtitle)

        header_layout.addWidget(title_container)
        header_layout.addStretch()

        # Badge
        badge = QLabel("✨ Smart Import")
        badge.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        badge.setFixedHeight(30)
        badge.setStyleSheet("""
            QLabel {
                background-color: #003087;
                color: white;
                border-radius: 6px;
                padding: 5px 12px;
            }
        """)
        header_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addLayout(header_layout)

        # Sección de archivos
        files_label = QLabel("📁 Archivos a Importar")
        files_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        layout.addWidget(files_label)

        # Grid de archivos
        files_grid = QGridLayout()
        files_grid.setSpacing(15)

        # Archivo 1: Training Report
        training_card = self._create_file_card(
            "📊 Enterprise Training Report",
            "Módulos y calificaciones",
            "Seleccionar Training Report",
            self._select_training_file
        )
        files_grid.addWidget(training_card, 0, 0)

        # Archivo 2: Org Planning
        org_card = self._create_file_card(
            "👥 CSOD Org Planning",
            "Usuarios y departamentos",
            "Seleccionar Org Planning",
            self._select_org_file
        )
        files_grid.addWidget(org_card, 0, 1)

        layout.addLayout(files_grid)

        # Separador
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setFixedHeight(1)
        sep1.setStyleSheet("background-color: #383838;")
        layout.addWidget(sep1)

        # Sección de acciones
        actions_label = QLabel("⚙️ Acciones")
        actions_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        layout.addWidget(actions_label)

        # Botones de acción
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        import_btn = QPushButton("📥 Importar y Cruzar Datos")
        import_btn.setFixedHeight(50)
        import_btn.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        import_btn.clicked.connect(self._import_data)
        actions_layout.addWidget(import_btn)

        preview_btn = QPushButton("👁️ Vista Previa")
        preview_btn.setFixedHeight(50)
        preview_btn.setProperty("class", "secondary")
        preview_btn.clicked.connect(self._preview_data)
        actions_layout.addWidget(preview_btn)

        validate_btn = QPushButton("✅ Validar Datos")
        validate_btn.setFixedHeight(50)
        validate_btn.setProperty("class", "secondary")
        validate_btn.clicked.connect(self._validate_data)
        actions_layout.addWidget(validate_btn)

        layout.addLayout(actions_layout)

        # Separador
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: #383838;")
        layout.addWidget(sep2)

        # Sección de log
        log_label = QLabel("📋 Log de Operaciones")
        log_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        layout.addWidget(log_label)

        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        self.log_text.setFont(QFont("Courier New", 10))
        self.log_text.setPlaceholderText("Los logs de importación aparecerán aquí...")
        layout.addWidget(self.log_text)

        layout.addStretch()

    def _create_file_card(self, title, subtitle, button_text, command):
        """Crear tarjeta de archivo"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(150)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Subtítulo
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Montserrat", 10))
        subtitle_label.setStyleSheet("color: #888888;")
        layout.addWidget(subtitle_label)

        layout.addSpacing(10)

        # Status
        status_label = QLabel("📄 No seleccionado")
        status_label.setFont(QFont("Montserrat", 10))
        status_label.setStyleSheet("color: #888888;")
        layout.addWidget(status_label)

        layout.addStretch()

        # Botón
        select_btn = QPushButton(button_text)
        select_btn.setFixedHeight(40)
        select_btn.clicked.connect(command)
        layout.addWidget(select_btn)

        # Guardar referencia al status label
        card.status_label = status_label

        return card

    def _select_training_file(self):
        """Seleccionar archivo Training Report"""

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Enterprise Training Report",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if file_name:
            self.archivo_training = file_name
            self._log(f"✅ Training Report seleccionado: {file_name}")

            # Actualizar status en card
            # (necesitaríamos guardar referencia a la card para actualizarla)

    def _select_org_file(self):
        """Seleccionar archivo Org Planning"""

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar CSOD Org Planning",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if file_name:
            self.archivo_org = file_name
            self._log(f"✅ Org Planning seleccionado: {file_name}")

    def _import_data(self):
        """Importar y cruzar datos"""

        if not self.archivo_training or not self.archivo_org:
            QMessageBox.warning(
                self,
                "Archivos Faltantes",
                "Por favor selecciona ambos archivos antes de importar."
            )
            return

        self._log("🔄 Iniciando importación de datos...")
        self._log(f"📊 Training Report: {self.archivo_training}")
        self._log(f"👥 Org Planning: {self.archivo_org}")

        QMessageBox.information(
            self,
            "Importación",
            "Funcionalidad de importación en desarrollo.\n\n"
            "Esta característica estará disponible próximamente con:\n"
            "- Validación de datos\n"
            "- Preview de cambios\n"
            "- Matching automático\n"
            "- Sistema de rollback"
        )

    def _preview_data(self):
        """Vista previa de datos"""

        if not self.archivo_training and not self.archivo_org:
            QMessageBox.warning(
                self,
                "Archivos Faltantes",
                "Por favor selecciona al menos un archivo."
            )
            return

        self._log("👁️ Generando vista previa...")
        QMessageBox.information(
            self,
            "Vista Previa",
            "Funcionalidad de preview en desarrollo"
        )

    def _validate_data(self):
        """Validar datos"""

        if not self.archivo_training and not self.archivo_org:
            QMessageBox.warning(
                self,
                "Archivos Faltantes",
                "Por favor selecciona al menos un archivo."
            )
            return

        self._log("✅ Validando datos...")
        QMessageBox.information(
            self,
            "Validación",
            "Funcionalidad de validación en desarrollo"
        )

    def _log(self, message):
        """Agregar mensaje al log"""
        self.log_text.append(message)
