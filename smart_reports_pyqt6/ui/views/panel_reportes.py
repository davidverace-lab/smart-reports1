"""
Panel de Reportes
PyQt6 Version - Generación y gestión de reportes
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QDateEdit,
    QListWidget, QListWidgetItem, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont


class ReportCard(QFrame):
    """Tarjeta de reporte"""

    def __init__(self, title: str, description: str, icon: str = "📄", parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)

        # Icono y título
        header_layout = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 32))
        header_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Descripción
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #888888;")
        layout.addWidget(desc_label)

        layout.addStretch()

        # Botón
        gen_btn = QPushButton("Generar Reporte")
        gen_btn.setFixedHeight(40)
        gen_btn.clicked.connect(self._generate_report)
        layout.addWidget(gen_btn)

    def _generate_report(self):
        """Generar reporte"""
        QMessageBox.information(self.parent(), "Generar", "Generando reporte...")


class ReportesPanel(QWidget):
    """Panel de Reportes"""

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

        title = QLabel("📄 Reportes")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        history_btn = QPushButton("📚 Historial")
        history_btn.setProperty("class", "secondary")
        history_btn.setFixedHeight(40)
        history_btn.clicked.connect(self._show_history)
        header_layout.addWidget(history_btn)

        layout.addLayout(header_layout)

        # Filtros
        filters_frame = QFrame()
        filters_frame.setFrameShape(QFrame.Shape.StyledPanel)
        filters_layout = QHBoxLayout(filters_frame)

        # Unidad
        unit_label = QLabel("Unidad:")
        unit_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        filters_layout.addWidget(unit_label)

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Todas", "ICAVE", "TNG", "ECV", "HPMX", "Container"])
        filters_layout.addWidget(self.unit_combo)

        # Periodo
        period_label = QLabel("Periodo:")
        period_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        filters_layout.addWidget(period_label)

        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        filters_layout.addWidget(self.start_date)

        filters_layout.addWidget(QLabel("-"))

        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        filters_layout.addWidget(self.end_date)

        filters_layout.addStretch()

        layout.addWidget(filters_frame)

        # Tipos de reportes en grid
        reports_label = QLabel("Tipos de Reportes Disponibles:")
        reports_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(reports_label)

        grid = QGridLayout()
        grid.setSpacing(15)

        reports = [
            ("📊 Reporte Global", "Vista general de todas las unidades y módulos", "📊"),
            ("🏢 Reporte por Unidad", "Progreso detallado de una unidad específica", "🏢"),
            ("👥 Reporte por Usuario", "Actividad y progreso de usuarios individuales", "👥"),
            ("📅 Reporte por Periodo", "Análisis de un rango de fechas específico", "📅"),
            ("📈 Reporte de Tendencias", "Gráficos de tendencias y evolución", "📈"),
            ("🎯 Reporte de Objetivos", "Cumplimiento de metas y KPIs", "🎯"),
        ]

        row = 0
        col = 0
        for title, desc, icon in reports:
            card = ReportCard(title, desc, icon)
            grid.addWidget(card, row, col)

            col += 1
            if col > 1:  # 2 columnas
                col = 0
                row += 1

        layout.addLayout(grid)

        layout.addStretch()

    def _show_history(self):
        """Mostrar historial de reportes"""
        QMessageBox.information(
            self,
            "Historial de Reportes",
            "Aquí se mostrará el historial de reportes generados"
        )
