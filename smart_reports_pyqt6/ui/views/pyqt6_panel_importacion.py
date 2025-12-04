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

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

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

        title = QLabel("Cruce e Importación de Datos")
        self.title_label = title
        title.setFont(QFont("Montserrat", 36, QFont.Weight.Bold))  # Aumentado de 28 a 36
        # Color según tema
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#002E6D"
        title.setStyleSheet(f"color: {title_color}; border: none; background: transparent; padding: 0; margin: 0;")
        title_layout.addWidget(title)

        subtitle = QLabel("Sistema de validación y matching de datos CSOD")
        self.subtitle_label = subtitle
        subtitle.setFont(QFont("Montserrat", 16))  # Aumentado de 11 a 16
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; border: none; background: transparent; padding: 0; margin: 0;")
        title_layout.addWidget(subtitle)

        header_layout.addWidget(title_container)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Sección de archivos - SIN EMOJI
        files_label = QLabel("Archivos a Importar")
        self.files_label = files_label
        files_label.setFont(QFont("Montserrat", 22, QFont.Weight.Bold))  # Aumentado de 16 a 22
        files_label.setStyleSheet(f"color: {title_color}; border: none; background: transparent; padding: 0; margin: 0;")
        layout.addWidget(files_label)

        # Grid de archivos
        files_grid = QGridLayout()
        files_grid.setSpacing(15)

        # Archivo 1: Training Report - CON CONTENEDOR NAVY
        training_card = self._create_file_card(
            "Enterprise Training Report",
            "Módulos y calificaciones",
            "Seleccionar Training Report",
            self._select_training_file,
            highlighted=True
        )
        self.training_card = training_card
        files_grid.addWidget(training_card, 0, 0)

        # Archivo 2: Org Planning - CON CONTENEDOR NAVY
        org_card = self._create_file_card(
            "CSOD Org Planning",
            "Usuarios y departamentos",
            "Seleccionar Org Planning",
            self._select_org_file,
            highlighted=True
        )
        self.org_card = org_card
        files_grid.addWidget(org_card, 0, 1)

        layout.addLayout(files_grid)

        # Separador - adaptado al tema
        sep1 = QFrame()
        self.sep1 = sep1
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setFixedHeight(1)
        sep_color = "#444444" if is_dark else "#d0d0d0"
        sep1.setStyleSheet(f"background-color: {sep_color};")
        layout.addWidget(sep1)

        # Sección de acciones - SIN EMOJI
        actions_label = QLabel("Acciones")
        self.actions_label = actions_label
        actions_label.setFont(QFont("Montserrat", 22, QFont.Weight.Bold))  # Aumentado de 16 a 22
        actions_label.setStyleSheet(f"color: {title_color}; border: none; background: transparent; padding: 0; margin: 0;")
        layout.addWidget(actions_label)

        # Botones de acción - NAVY CORPORATIVO
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        import_btn = QPushButton("Importar y Cruzar Datos")
        import_btn.setFixedHeight(60)  # Aumentado de 50 a 60
        import_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # Aumentado de 12 a 15
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D !important;
                color: white !important;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #003D82 !important;
            }
        """)
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.clicked.connect(self._import_data)
        actions_layout.addWidget(import_btn)

        preview_btn = QPushButton("Vista Previa")
        preview_btn.setFixedHeight(60)
        preview_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D !important;
                color: white !important;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #003D82 !important;
            }
        """)
        preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        preview_btn.clicked.connect(self._preview_data)
        actions_layout.addWidget(preview_btn)

        validate_btn = QPushButton("Validar Datos")
        validate_btn.setFixedHeight(60)
        validate_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
        validate_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D !important;
                color: white !important;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #003D82 !important;
            }
        """)
        validate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        validate_btn.clicked.connect(self._validate_data)
        actions_layout.addWidget(validate_btn)

        layout.addLayout(actions_layout)

        # Separador - adaptado al tema
        sep2 = QFrame()
        self.sep2 = sep2
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep_color = "#444444" if is_dark else "#d0d0d0"
        sep2.setStyleSheet(f"background-color: {sep_color};")
        layout.addWidget(sep2)

        # Sección de log - SIN EMOJI
        log_label = QLabel("Log de Operaciones")
        self.log_label = log_label
        log_label.setFont(QFont("Montserrat", 22, QFont.Weight.Bold))  # Aumentado de 16 a 22
        log_label.setStyleSheet(f"color: {title_color}; border: none; background: transparent; padding: 0; margin: 0;")
        layout.addWidget(log_label)

        # Log text area - adaptado al tema
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        self.log_text.setFont(QFont("Courier New", 10))
        self.log_text.setPlaceholderText("Los logs de importación aparecerán aquí...")
        log_bg = "#1e1e1e" if is_dark else "#ffffff"
        log_text = "#00ff00" if is_dark else "#008000"  # Verde para logs
        log_border = "#002E6D"
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {log_bg};
                color: {log_text};
                border: 2px solid {log_border};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        layout.addWidget(self.log_text)

        layout.addStretch()

    def _create_file_card(self, title, subtitle, button_text, command, highlighted=False):
        """Crear tarjeta de archivo"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(180)

        # Aplicar borde navy si está destacado
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#002E6D" if highlighted else "#383838"
        border_width = "3px" if highlighted else "1px"

        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: {border_width} solid {border_color};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título - MÁS GRANDE
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        text_color = "#ffffff" if is_dark else "#002E6D"
        title_label.setStyleSheet(f"color: {text_color}; border: none; background: transparent;")
        layout.addWidget(title_label)

        # Subtítulo - MÁS GRANDE
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Montserrat", 13))
        subtitle_label.setStyleSheet("color: #888888; border: none; background: transparent;")
        layout.addWidget(subtitle_label)

        layout.addSpacing(15)

        # Status - SIN EMOJI
        status_label = QLabel("No seleccionado")
        status_label.setFont(QFont("Montserrat", 12))
        status_label.setStyleSheet("color: #888888; border: none; background: transparent;")
        layout.addWidget(status_label)

        layout.addStretch()

        # Botón - NAVY
        select_btn = QPushButton(button_text)
        select_btn.setFixedHeight(45)
        select_btn.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #003D82;
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

    def _on_theme_changed(self, new_theme: str):
        """Actualizar tema"""
        is_dark = (new_theme == 'dark')
        text_color = "#ffffff" if is_dark else "#002E6D"
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        sep_color = "#444444" if is_dark else "#d0d0d0"

        # Labels
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {text_color}; border: none; background: transparent; padding: 0; margin: 0;")
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"color: {subtitle_color}; border: none; background: transparent; padding: 0; margin: 0;")
        if hasattr(self, 'files_label'):
            self.files_label.setStyleSheet(f"color: {text_color}; border: none; background: transparent; padding: 0; margin: 0;")
        if hasattr(self, 'actions_label'):
            self.actions_label.setStyleSheet(f"color: {text_color}; border: none; background: transparent; padding: 0; margin: 0;")
        if hasattr(self, 'log_label'):
            self.log_label.setStyleSheet(f"color: {text_color}; border: none; background: transparent; padding: 0; margin: 0;")

        # Separadores
        if hasattr(self, 'sep1'):
            self.sep1.setStyleSheet(f"background-color: {sep_color};")
        if hasattr(self, 'sep2'):
            self.sep2.setStyleSheet(f"background-color: {sep_color};")

        # Log Text
        log_bg = "#1e1e1e" if is_dark else "#ffffff"
        log_text = "#00ff00" if is_dark else "#008000"
        log_border = "#002E6D"
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {log_bg};
                color: {log_text};
                border: 2px solid {log_border};
                border-radius: 8px;
                padding: 10px;
            }}
        """)

        # Cards (re-aplicar estilos)
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#002E6D" # Highlighted
        
        for card in [self.training_card, self.org_card]:
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: 3px solid {border_color};
                    border-radius: 12px;
                }}
            """)
            # Actualizar labels internos (simplificado)
            card.findChild(QLabel).setStyleSheet(f"color: {text_color}; border: none; background: transparent;")
