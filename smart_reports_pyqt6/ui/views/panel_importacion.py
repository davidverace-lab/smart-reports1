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
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        # Título y subtítulo
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title = QLabel("↓ Cruce e Importación de Datos")  # Ícono blanco: de 📥 a ↓
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 32 a 40
        # Color según tema
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; border: none !important; background: transparent !important; margin: 0; padding: 0;")
        title_layout.addWidget(title)

        subtitle = QLabel("Sistema de validación y matching de datos CSOD")
        subtitle.setFont(QFont("Montserrat", 18))  # MUCHO MÁS GRANDE: de 14 a 18
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; border: none !important; background: transparent !important; margin: 0; padding: 0;")
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
        files_label = QLabel("◫ Archivos a Importar")  # Ícono blanco: de 📁 a ◫
        files_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 20 a 24
        files_label.setStyleSheet(f"color: {title_color}; border: none !important; background: transparent !important; margin: 0; padding: 0;")
        layout.addWidget(files_label)

        # Grid de archivos
        files_grid = QGridLayout()
        files_grid.setSpacing(15)

        # Archivo 1: Training Report - CONTENEDOR CON BORDE NAVY
        training_card = self._create_file_card(
            "▤ Enterprise Training Report",  # Ícono blanco: de 📊 a ▤
            "Módulos y calificaciones",
            "Seleccionar Training Report",
            self._select_training_file
        )
        files_grid.addWidget(training_card, 0, 0)

        # Archivo 2: Org Planning - CONTENEDOR CON BORDE NAVY
        org_card = self._create_file_card(
            "◉ CSOD Org Planning",  # Ícono blanco: de 👥 a ◉
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
        actions_label = QLabel("⚙ Acciones")  # Ícono blanco: de ⚙️ a ⚙
        actions_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 20 a 24
        actions_label.setStyleSheet(f"color: {title_color}; border: none !important; background: transparent !important; margin: 0; padding: 0;")
        layout.addWidget(actions_label)

        # Botones de acción - NAVY BLUE
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        import_btn = QPushButton("↓ Importar y Cruzar Datos")  # Ícono blanco: de 📥 a ↓
        import_btn.setFixedHeight(60)  # MUCHO MÁS ALTO: de 55 a 60
        import_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 13 a 15
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #003087 !important;
                color: white !important;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0 !important;
            }
        """)
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self._import_data)
        actions_layout.addWidget(import_btn)

        preview_btn = QPushButton("◉ Vista Previa")  # Ícono blanco: de 👁️ a ◉
        preview_btn.setFixedHeight(60)  # MUCHO MÁS ALTO: de 55 a 60
        preview_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 13 a 15
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #003087 !important;
                color: white !important;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0 !important;
            }
        """)
        preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        preview_btn.clicked.connect(self._preview_data)
        actions_layout.addWidget(preview_btn)

        validate_btn = QPushButton("✓ Validar Datos")  # Ícono blanco: de ✅ a ✓
        validate_btn.setFixedHeight(60)  # MUCHO MÁS ALTO: de 55 a 60
        validate_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 13 a 15
        validate_btn.setStyleSheet("""
            QPushButton {
                background-color: #003087 !important;
                color: white !important;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0 !important;
            }
        """)
        validate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        log_label = QLabel("◫ Log de Operaciones")  # Ícono blanco: de 📋 a ◫
        log_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 20 a 24
        log_label.setStyleSheet(f"color: {title_color}; border: none !important; background: transparent !important; margin: 0; padding: 0;")
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
        """Crear tarjeta de archivo - CON BORDE NAVY"""

        # Detectar tema
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#003087"

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(180)  # MÁS ALTO: de 150 a 180
        # CONTENEDOR CON BORDE NAVY
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 3px solid #003087;
                border-radius: 12px;
            }}
            QFrame QLabel {{
                background: transparent !important;
                border: none !important;
                margin: 0;
                padding: 0;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)  # MÁS padding: de 15 a 20
        layout.setSpacing(12)

        # Título - MÁS GRANDE Y SIN BORDES
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))  # MÁS GRANDE: de 13 a 18
        title_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(title_label)

        # Subtítulo - MÁS GRANDE
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Montserrat", 14))  # MÁS GRANDE: de 10 a 14
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle_label.setStyleSheet(f"color: {subtitle_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(subtitle_label)

        layout.addSpacing(10)

        # Status
        status_label = QLabel("◫ No seleccionado")  # Ícono blanco: de 📄 a ◫
        status_label.setFont(QFont("Montserrat", 12))  # MÁS GRANDE: de 10 a 12
        status_label.setStyleSheet(f"color: {subtitle_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(status_label)

        layout.addStretch()

        # Botón - MÁS GRANDE
        select_btn = QPushButton(button_text)
        select_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE
        select_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        select_btn.setStyleSheet("""
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
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
