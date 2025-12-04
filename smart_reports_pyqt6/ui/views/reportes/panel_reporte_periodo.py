"""
Panel de Reporte por Periodo - PyQt6
Reporte de un rango de fechas específico
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelReportePeriodo(QWidget):
    """Panel de Reporte por Periodo"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📅 Reporte por Periodo")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Selector de periodo
        period_label = QLabel("Desde:")
        period_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(period_label)

        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        header_layout.addWidget(self.start_date)

        to_label = QLabel("Hasta:")
        to_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(to_label)

        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        header_layout.addWidget(self.end_date)

        generate_btn = QPushButton("🔄 Generar")
        generate_btn.setFixedHeight(40)
        generate_btn.clicked.connect(self._generate_report)
        header_layout.addWidget(generate_btn)

        layout.addLayout(header_layout)

        # Resumen del periodo
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 20, 20, 20)

        summary_title = QLabel("📋 Resumen del Periodo")
        summary_title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        summary_layout.addWidget(summary_title)

        summary_text = QLabel(
            "Periodo: 01/11/2025 - 01/12/2025\n\n"
            "• Nuevos usuarios registrados: 45\n"
            "• Módulos completados: 387\n"
            "• Horas de capacitación: 1,245h\n"
            "• Tasa de finalización: 88%\n"
            "• Promedio de avance: +12%"
        )
        summary_text.setFont(QFont("Montserrat", 11))
        summary_text.setWordWrap(True)
        summary_layout.addWidget(summary_text)

        layout.addWidget(summary_frame)

        # Gráficas del periodo
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # Gráfica 1: Tendencia diaria
        chart1_data = {
            'labels': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
            'values': [85, 120, 145, 180]
        }
        chart1 = self._create_chart_card("Módulos Completados por Semana", 'line', chart1_data)
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2: Distribución
        chart2_data = {
            'labels': ['ICAVE', 'TNG', 'ECV', 'HPMX', 'Container'],
            'values': [120, 98, 75, 54, 40]
        }
        chart2 = self._create_chart_card("Actividad por Unidad", 'bar', chart2_data)
        charts_grid.addWidget(chart2, 0, 1)

        layout.addLayout(charts_grid)

        layout.addStretch()

    def _create_chart_card(self, title, chart_type, data):
        """Crear tarjeta con gráfico"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(250)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)

        chart = D3ChartWidget(card)
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'
        chart.set_chart(chart_type, title, data, tema=tema)
        layout.addWidget(chart)

        return card

    def _generate_report(self):
        """Generar reporte"""
        start = self.start_date.date().toString("dd/MM/yyyy")
        end = self.end_date.date().toString("dd/MM/yyyy")
        print(f"🔄 Generando reporte del periodo: {start} - {end}...")
