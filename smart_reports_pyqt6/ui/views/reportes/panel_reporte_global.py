"""
Panel de Reporte Global - PyQt6
Reporte global del sistema con métricas consolidadas
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelReporteGlobal(QWidget):
    """Panel de Reporte Global"""

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

        title = QLabel("📊 Reporte Global del Sistema")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Botones
        export_btn = QPushButton("📥 Exportar PDF")
        export_btn.setFixedHeight(40)
        export_btn.clicked.connect(self._export_pdf)
        header_layout.addWidget(export_btn)

        generate_btn = QPushButton("🔄 Generar Reporte")
        generate_btn.setFixedHeight(40)
        generate_btn.clicked.connect(self._generate_report)
        header_layout.addWidget(generate_btn)

        layout.addLayout(header_layout)

        # Resumen ejecutivo
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 20, 20, 20)

        summary_title = QLabel("📋 Resumen Ejecutivo")
        summary_title.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        summary_layout.addWidget(summary_title)

        summary_text = QLabel(
            "• Total de unidades activas: 11\n"
            "• Total de usuarios registrados: 1,525\n"
            "• Módulos completados: 4,521\n"
            "• Promedio de avance global: 75%\n"
            "• Tasa de cumplimiento: 92%"
        )
        summary_text.setFont(QFont("Montserrat", 11))
        summary_text.setWordWrap(True)
        summary_layout.addWidget(summary_text)

        layout.addWidget(summary_frame)

        # Gráficas resumen
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # Gráfica 1
        chart1_data = {
            'labels': ['ICAVE', 'TNG', 'ECV', 'HPMX', 'Container'],
            'values': [372, 276, 226, 195, 145]
        }
        chart1 = self._create_chart_card("Usuarios por Unidad", 'bar', chart1_data)
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2_data = {
            'labels': ['Completado', 'En Progreso', 'Pendiente'],
            'values': [75, 20, 5]
        }
        chart2 = self._create_chart_card("Avance Global", 'donut', chart2_data)
        charts_grid.addWidget(chart2, 0, 1)

        layout.addLayout(charts_grid)

        # Tabla de datos
        table_label = QLabel("📊 Datos Consolidados por Unidad")
        table_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(table_label)

        self.table = self._create_data_table()
        layout.addWidget(self.table)

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

    def _create_data_table(self):
        """Crear tabla de datos"""
        table = QTableWidget(5, 4)
        table.setHorizontalHeaderLabels(["Unidad", "Usuarios", "Completados", "Avance %"])

        # Datos
        data = [
            ["ICAVE", "372", "278", "75%"],
            ["TNG", "276", "276", "100%"],
            ["ECV", "226", "170", "75%"],
            ["HPMX", "195", "121", "62%"],
            ["Container", "145", "99", "68%"],
        ]

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setFixedHeight(200)

        return table

    def _generate_report(self):
        """Generar reporte"""
        print("🔄 Generando reporte global...")

    def _export_pdf(self):
        """Exportar a PDF"""
        print("📥 Exportando reporte a PDF...")
