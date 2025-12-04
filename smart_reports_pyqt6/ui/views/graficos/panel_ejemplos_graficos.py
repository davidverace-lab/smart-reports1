"""
Panel de Ejemplos de Gráficos - PyQt6
Galería de ejemplos de diferentes tipos de gráficos
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelEjemplosGraficos(QWidget):
    """Panel de Ejemplos de Gráficos"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        
        # Ejemplos de datos
        self.ejemplos = [
            {
                'titulo': 'Barras Simples',
                'tipo': 'bar',
                'datos': {
                    'labels': ['A', 'B', 'C', 'D', 'E'],
                    'values': [10, 24, 18, 32, 15]
                }
            },
            {
                'titulo': 'Gráfico de Donut',
                'tipo': 'donut',
                'datos': {
                    'labels': ['Categoría 1', 'Categoría 2', 'Categoría 3'],
                    'values': [40, 35, 25]
                }
            },
            {
                'titulo': 'Líneas de Tendencia',
                'tipo': 'line',
                'datos': {
                    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                    'values': [10, 15, 13, 18, 22, 25]
                }
            },
            {
                'titulo': 'Barras Horizontales',
                'tipo': 'bar',
                'datos': {
                    'labels': ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4'],
                    'values': [45, 38, 52, 41]
                }
            },
            {
                'titulo': 'Distribución Porcentual',
                'tipo': 'donut',
                'datos': {
                    'labels': ['Seg A', 'Seg B', 'Seg C', 'Seg D'],
                    'values': [25, 30, 20, 25]
                }
            },
            {
                'titulo': 'Series Temporales',
                'tipo': 'line',
                'datos': {
                    'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
                    'values': [100, 125, 145, 180]
                }
            }
        ]
        
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("🎨 Galería de Ejemplos")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Scroll area para ejemplos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)

        # Grid de ejemplos (3 columnas)
        ejemplos_grid = QGridLayout()
        ejemplos_grid.setSpacing(15)

        row, col = 0, 0
        for ejemplo in self.ejemplos:
            card = self._create_example_card(
                ejemplo['titulo'],
                ejemplo['tipo'],
                ejemplo['datos']
            )
            ejemplos_grid.addWidget(card, row, col)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1

        scroll_layout.addLayout(ejemplos_grid)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _create_example_card(self, titulo, tipo, datos):
        """Crear tarjeta de ejemplo"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFixedSize(280, 280)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)

        # Título
        title_label = QLabel(titulo)
        title_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Gráfico
        chart = D3ChartWidget(card)
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'
        chart.set_chart(tipo, titulo, datos, tema=tema)
        layout.addWidget(chart)

        return card
