"""
Panel de Gráficos Interactivos - PyQt6
Galería de gráficos interactivos con D3.js
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget


class PanelGraficosInteractivos(QWidget):
    """Panel de Gráficos Interactivos"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        
        # Datos de ejemplo para gráficos
        self.datos_ejemplos = {
            'ventas_trimestre': {
                'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
                'values': [45000, 52000, 48000, 61000]
            },
            'distribucion_productos': {
                'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
                'values': [30, 25, 20, 15, 10]
            },
            'tendencia_anual': {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                'values': [12, 15, 18, 22, 28, 32, 35, 38, 34, 30, 26, 20]
            }
        }
        
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📊 Gráficos Interactivos")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Selector de tipo de gráfico
        type_label = QLabel("Tipo:")
        type_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(type_label)

        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Barras", "Donut", "Líneas"])
        self.chart_type_combo.currentIndexChanged.connect(self._update_charts)
        header_layout.addWidget(self.chart_type_combo)

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._update_charts)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Grid de gráficos interactivos
        self.charts_grid = QGridLayout()
        self.charts_grid.setSpacing(20)

        # Crear gráficos iniciales
        self._create_charts()

        layout.addLayout(self.charts_grid)

        layout.addStretch()

    def _create_charts(self):
        """Crear gráficos"""

        # Limpiar grid
        while self.charts_grid.count():
            item = self.charts_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        chart_type_text = self.chart_type_combo.currentText()
        chart_type_map = {
            'Barras': 'bar',
            'Donut': 'donut',
            'Líneas': 'line'
        }
        chart_type = chart_type_map.get(chart_type_text, 'bar')

        # Gráfico 1
        chart1 = self._create_chart_card(
            "Ventas por Trimestre",
            chart_type,
            self.datos_ejemplos['ventas_trimestre']
        )
        self.charts_grid.addWidget(chart1, 0, 0)

        # Gráfico 2
        chart2 = self._create_chart_card(
            "Distribución de Productos",
            chart_type,
            self.datos_ejemplos['distribucion_productos']
        )
        self.charts_grid.addWidget(chart2, 0, 1)

        # Gráfico 3
        chart3 = self._create_chart_card(
            "Tendencia Anual",
            chart_type,
            self.datos_ejemplos['tendencia_anual']
        )
        self.charts_grid.addWidget(chart3, 1, 0, 1, 2)

    def _create_chart_card(self, title, chart_type, data):
        """Crear tarjeta con gráfico"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(300)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Gráfico
        chart = D3ChartWidget(card)
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'
        chart.set_chart(chart_type, title, data, tema=tema)
        layout.addWidget(chart)

        return card

    def _update_charts(self):
        """Actualizar gráficos"""
        print("🔄 Actualizando gráficos interactivos...")
        self._create_charts()
