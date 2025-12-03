"""
Panel de Reportes con navegación tipo app móvil - COMPLETO con filtros
PyQt6 Version - Estilo CustomTkinter migrado con todas las funcionalidades
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea,
    QLineEdit, QComboBox, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont


class ReportCard(QFrame):
    """Tarjeta clickeable para seleccionar tipo de reporte"""

    clicked = pyqtSignal()

    def __init__(self, title: str, description: str, icon: str = "◫", theme_manager=None, parent=None):  # Ícono blanco
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(180)  # MUCHO MÁS GRANDE: de 140 a 180
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Aplicar estilo
        self._apply_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # MÁS ESPACIO: de 15 a 20
        layout.setSpacing(12)  # MÁS ESPACIO: de 8 a 12

        # Icono y título - MUCHO MÁS GRANDE SIN BORDES
        header_label = QLabel(f"{icon} {title}")
        header_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 20 a 24
        is_dark = theme_manager.is_dark_mode() if theme_manager else False
        text_color = "#ffffff" if is_dark else "#003087"
        header_label.setStyleSheet(f"color: {text_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(header_label)

        # Descripción - MUCHO MÁS GRANDE SIN BORDES
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Montserrat", 16))  # MUCHO MÁS GRANDE: de 13 a 16
        desc_color = "#b0b0b0" if is_dark else "#666666"
        desc_label.setStyleSheet(f"color: {desc_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        layout.addWidget(desc_label)

        layout.addStretch()

        # Botón - MÁS GRANDE
        gen_btn = QPushButton("▶ Generar Reporte")  # Ícono blanco
        gen_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 13 a 15
        gen_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        gen_btn.setStyleSheet("""
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
        gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gen_btn.clicked.connect(self.clicked.emit)
        layout.addWidget(gen_btn)

    def _apply_theme(self):
        """Aplicar tema a la tarjeta"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#003087"

        self.setStyleSheet(f"""
            ReportCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
            ReportCard:hover {{
                border: 3px solid {border_color};
            }}
        """)


class ReportGenerationView(QWidget):
    """Vista de generación de reporte específico con filtros completos"""

    back_clicked = pyqtSignal()

    def __init__(self, report_type: str, theme_manager=None, db_connection=None, parent=None):
        super().__init__(parent)

        self.report_type = report_type
        self.theme_manager = theme_manager
        self.db_connection = db_connection

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de generación"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # REDUCIDO de 15 a 10 - SIN MÁRGENES GRISES
        layout.setSpacing(12)  # REDUCIDO de 15 a 12

        # Header con botón de retorno
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Botón de retorno - MÁS GRANDE
        back_btn = QPushButton("← Volver")
        back_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 14
        back_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        back_btn.setFixedWidth(140)  # MÁS ANCHO: de 120 a 140
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

        # Título - MUCHO MÁS GRANDE SIN BORDES
        title = QLabel(f"▤ {self.report_type}")  # Ícono blanco: de 📊 a ▤
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 26 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        layout.addWidget(header)

        # BOTONES DE ACCIÓN ARRIBA (Mejor UX - no se pierden) - MÁS GRANDES
        actions_layout = QHBoxLayout()

        preview_btn = QPushButton("◉ Vista Previa")  # Ícono blanco: de 👁️ a ◉
        preview_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 15
        preview_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        preview_btn.setStyleSheet("""
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
        preview_btn.clicked.connect(self._preview_report)
        actions_layout.addWidget(preview_btn)

        generate_btn = QPushButton("◫ Generar PDF")  # Ícono blanco: de 📄 a ◫
        generate_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 15
        generate_btn.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        generate_btn.setStyleSheet("""
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
        generate_btn.clicked.connect(self._generate_report)
        actions_layout.addWidget(generate_btn)

        layout.addLayout(actions_layout)

        # Área de configuración del reporte (scroll) - AHORA DEBAJO DE BOTONES
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(12)  # REDUCIDO de 15 a 12

        # Frame de configuración - MÁS COMPACTO
        config_frame = QFrame()
        config_frame.setFrameShape(QFrame.Shape.StyledPanel)
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        config_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid #003087;
                border-radius: 12px;
            }}
        """)
        config_layout = QVBoxLayout(config_frame)
        config_layout.setContentsMargins(15, 15, 15, 15)  # REDUCIDO de 20 a 15
        config_layout.setSpacing(10)  # REDUCIDO de 15 a 10

        # Crear filtros según el tipo de reporte
        self._create_filters(config_layout)

        scroll_layout.addWidget(config_frame)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def _create_filters(self, layout):
        """Crear filtros según el tipo de reporte"""

        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#ffffff" if is_dark else "#003087"
        label_style = f"color: {text_color}; font-weight: bold; background: transparent;"

        # Título de filtros - MÁS GRANDE SIN BORDES
        filter_title = QLabel("⚙ Configuración del Reporte")  # Ícono blanco: de ⚙️ a ⚙
        filter_title.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))  # MÁS GRANDE: de 16 a 20
        filter_title.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(filter_title)

        # Filtros específicos por tipo de reporte
        if "Usuario" in self.report_type:
            self._create_user_filters(layout, label_style)
        elif "Unidad" in self.report_type:
            self._create_unit_filters(layout, label_style)
        elif "Período" in self.report_type or "Fecha" in self.report_type:
            self._create_period_filters(layout, label_style)
        elif "Mando" in self.report_type or "Nivel" in self.report_type:
            self._create_level_filters(layout, label_style)
        elif "Global" in self.report_type:
            self._create_global_filters(layout, label_style)

    def _create_user_filters(self, layout, label_style):
        """Filtros para reporte de usuario"""
        # User ID - MÁS GRANDE SIN BORDES
        user_label = QLabel("User ID:")
        user_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        user_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(user_label)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingrese el User ID")
        self.user_input.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.user_input.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.user_input)

        # Búsqueda por nombre - MÁS GRANDE SIN BORDES
        name_label = QLabel("O buscar por nombre:")
        name_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        name_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(name_label)

        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Buscar usuario por nombre...")
        self.user_search.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.user_search.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.user_search)

    def _create_unit_filters(self, layout, label_style):
        """Filtros para reporte por unidad"""
        # Unidad de Negocio - MÁS GRANDE SIN BORDES
        unit_label = QLabel("Unidad de Negocio:")
        unit_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        unit_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(unit_label)

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(['TNG', 'ICAVE', 'ECV', 'Container Care', 'HPMX'])
        self.unit_combo.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.unit_combo.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.unit_combo)

        # Módulo - MÁS GRANDE SIN BORDES
        module_label = QLabel("Módulo:")
        module_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        module_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(module_label)

        self.module_combo = QComboBox()
        modules = ['Todos'] + [f'Módulo {i}' for i in range(1, 9)]
        self.module_combo.addItems(modules)
        self.module_combo.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.module_combo.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.module_combo)

    def _create_period_filters(self, layout, label_style):
        """Filtros para reporte por período"""
        # Fecha inicio - MÁS GRANDE SIN BORDES
        start_label = QLabel("Fecha Inicio:")
        start_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        start_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(start_label)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.start_date.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.start_date)

        # Fecha fin - MÁS GRANDE SIN BORDES
        end_label = QLabel("Fecha Fin:")
        end_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        end_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(end_label)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.end_date.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.end_date)

        # Unidad (opcional) - MÁS GRANDE SIN BORDES
        unit_label = QLabel("Filtrar por Unidad (opcional):")
        unit_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        unit_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(unit_label)

        self.unit_filter = QComboBox()
        self.unit_filter.addItems(['Todas', 'TNG', 'ICAVE', 'ECV', 'Container Care', 'HPMX'])
        self.unit_filter.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.unit_filter.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.unit_filter)

    def _create_level_filters(self, layout, label_style):
        """Filtros para reporte por nivel de mando"""
        # Nivel de mando - MÁS GRANDE SIN BORDES
        level_label = QLabel("Nivel de Mando:")
        level_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        level_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(level_label)

        self.level_combo = QComboBox()
        self.level_combo.addItems([
            'Todos',
            'Gerencia General',
            'Gerencia de Área',
            'Jefatura',
            'Supervisión',
            'Personal Operativo'
        ])
        self.level_combo.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.level_combo.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.level_combo)

        # Unidad (opcional) - MÁS GRANDE SIN BORDES
        unit_label = QLabel("Filtrar por Unidad (opcional):")
        unit_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        unit_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(unit_label)

        self.unit_filter = QComboBox()
        self.unit_filter.addItems(['Todas', 'TNG', 'ICAVE', 'ECV', 'Container Care', 'HPMX'])
        self.unit_filter.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.unit_filter.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.unit_filter)

    def _create_global_filters(self, layout, label_style):
        """Filtros para reporte global"""
        # Módulo - MÁS GRANDE SIN BORDES
        module_label = QLabel("Filtrar por Módulo:")
        module_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        module_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(module_label)

        self.module_combo = QComboBox()
        modules = ['Todos'] + [f'Módulo {i}' for i in range(1, 9)]
        self.module_combo.addItems(modules)
        self.module_combo.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.module_combo.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.module_combo)

        # Incluir estadísticas detalladas - MÁS GRANDE SIN BORDES
        stats_label = QLabel("Nivel de Detalle:")
        stats_label.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))  # MÁS GRANDE: de 12 a 16
        stats_label.setStyleSheet(f"{label_style} margin: 0; padding: 0; border: none !important;")
        layout.addWidget(stats_label)

        self.detail_combo = QComboBox()
        self.detail_combo.addItems(['Resumen Ejecutivo', 'Detallado', 'Completo con Gráficos'])
        self.detail_combo.setFont(QFont("Montserrat", 15))  # MÁS GRANDE
        self.detail_combo.setFixedHeight(50)  # MÁS ALTO: de 40 a 50
        layout.addWidget(self.detail_combo)

    def _preview_report(self):
        """Generar vista previa del reporte"""
        QMessageBox.information(
            self,
            "Vista Previa",
            f"Generando vista previa del reporte:\n{self.report_type}\n\nEsta funcionalidad se conectará con el generador de PDFs."
        )

    def _generate_report(self):
        """Generar reporte PDF"""
        QMessageBox.information(
            self,
            "Generar Reporte",
            f"Generando reporte PDF:\n{self.report_type}\n\nEsta funcionalidad se conectará con el generador de PDFs y guardará el archivo."
        )


class ReportesPanel(QWidget):
    """Panel de Reportes con navegación tipo app móvil"""

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        # Stack para navegación
        self.stack = QStackedWidget()

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz principal"""

        # Layout principal con stack
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        # Crear vista principal (selección de reportes)
        self.selection_view = self._create_selection_view()
        self.stack.addWidget(self.selection_view)

    def _create_selection_view(self):
        """Crear vista de selección de reportes"""

        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(10, 10, 10, 10)  # REDUCIDO - SIN MÁRGENES GRISES
        layout.setSpacing(12)  # REDUCIDO

        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)

        title = QLabel("▤ Generación de Reportes")  # Ícono blanco: de 📊 a ▤
        title.setFont(QFont("Montserrat", 40, QFont.Weight.Bold))  # MUCHO MÁS GRANDE: de 32 a 40
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(title)

        subtitle = QLabel("Selecciona el tipo de reporte que deseas generar")
        subtitle.setFont(QFont("Montserrat", 20))  # MUCHO MÁS GRANDE: de 16 a 20
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; background: transparent !important; border: none !important; margin: 0; padding: 0;")
        header_layout.addWidget(subtitle)

        layout.addWidget(header)

        # Scroll area para las tarjetas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(12)
        scroll.setWidget(scroll_widget)

        # Tipos de reportes - ICONOS BLANCOS
        reports = [
            ("Progreso de Usuario", "Reporte detallado del progreso individual", "◉"),  # de 👤 a ◉
            ("Progreso por Unidad", "Reporte de progreso por unidad de negocio", "▣"),  # de 🏢 a ▣
            ("Reporte por Período", "Reporte de actividad en un rango de fechas", "◐"),  # de 📅 a ◐
            ("Reporte Global", "Vista general del sistema completo", "◎"),  # de 🌍 a ◎
            ("Niveles de Mando", "Reporte organizado por niveles gerenciales", "▤"),  # de 👔 a ▤
        ]

        row = 0
        col = 0
        for title, desc, icon in reports:
            card = ReportCard(title, desc, icon, self.theme_manager)
            card.clicked.connect(lambda t=title: self._open_report_generation(t))
            scroll_layout.addWidget(card, row, col)

            col += 1
            if col > 1:  # 2 columnas
                col = 0
                row += 1

        layout.addWidget(scroll)

        return view

    def _open_report_generation(self, report_type: str):
        """Abrir vista de generación de reporte"""

        print(f"📄 Abriendo generación de reporte: {report_type}")

        # Crear vista de generación
        generation_view = ReportGenerationView(report_type, self.theme_manager, self.db_connection)
        generation_view.back_clicked.connect(self._go_back)

        # Agregar al stack y mostrar
        self.stack.addWidget(generation_view)
        self.stack.setCurrentWidget(generation_view)

    def _go_back(self):
        """Volver a la vista de selección"""

        # Obtener vista actual
        current_view = self.stack.currentWidget()

        # Volver a selección
        self.stack.setCurrentWidget(self.selection_view)

        # Remover vista anterior
        if current_view != self.selection_view:
            self.stack.removeWidget(current_view)
            current_view.deleteLater()
