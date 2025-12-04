"""
Panel de Reporte por Unidad - PyQt6
Reporte detallado de una unidad específica
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelReporteUnidad(QWidget):
    """Panel de Reporte por Unidad"""

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

        title = QLabel("🏢 Reporte por Unidad")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Selector de unidad
        unit_label = QLabel("Unidad:")
        unit_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(unit_label)

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["ICAVE", "TNG", "ECV", "HPMX", "Container"])
        self.unit_combo.currentIndexChanged.connect(self._load_unit_data)
        header_layout.addWidget(self.unit_combo)

        generate_btn = QPushButton("🔄 Generar")
        generate_btn.setFixedHeight(40)
        generate_btn.clicked.connect(self._generate_report)
        header_layout.addWidget(generate_btn)

        layout.addLayout(header_layout)

        # Métricas de la unidad
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Total Usuarios", "372", "👥"),
            ("Módulos Completados", "278", "✅"),
            ("Promedio Avance", "75%", "📊"),
            ("Tasa Cumplimiento", "92%", "🎯"),
        ]

        for label, value, icon in metrics:
            metric_card = self._create_metric_card(label, value, icon)
            metrics_layout.addWidget(metric_card)

        layout.addLayout(metrics_layout)

        # Gráficas de unidad
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # Gráfica 1
        chart1_data = {
            'labels': ['Mod 1', 'Mod 2', 'Mod 3', 'Mod 4', 'Mod 5'],
            'values': [95, 88, 75, 68, 62]
        }
        chart1 = self._create_chart_card("Avance por Módulo", 'bar', chart1_data)
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2_data = {
            'labels': ['Completado', 'En Progreso', 'Pendiente'],
            'values': [75, 20, 5]
        }
        chart2 = self._create_chart_card("Estado General", 'donut', chart2_data)
        charts_grid.addWidget(chart2, 0, 1)

        layout.addLayout(charts_grid)

        layout.addStretch()

    def _create_metric_card(self, label, value, icon):
        """Crear tarjeta de métrica"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFixedHeight(100)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        layout.addWidget(icon_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        layout.addWidget(value_label)

        label_label = QLabel(label)
        label_label.setFont(QFont("Montserrat", 9))
        label_label.setStyleSheet("color: #888888;")
        layout.addWidget(label_label)

        return card

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

    def _load_unit_data(self):
        """Cargar datos de la unidad seleccionada"""
        unit = self.unit_combo.currentText()
        print(f"📊 Cargando datos de {unit}...")

    def _generate_report(self):
        """Generar reporte"""
        print("🔄 Generando reporte de unidad...")
