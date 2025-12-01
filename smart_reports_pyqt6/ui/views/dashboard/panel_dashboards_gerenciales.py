"""
Panel de Dashboards Gerenciales - PyQt6
Dashboards gerenciales con gráficas interactivas
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget


class DashboardsGerencialesPanel(QWidget):
    """Panel de Dashboards Gerenciales"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Datos de gráficas
        self.datos_graficas = {
            'usuarios_unidad': {
                'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
                'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
            },
            'progreso_unidades': {
                'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
                'values': [100, 82, 75, 68, 62]
            },
            'tendencia_semanal': {
                'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                'values': [65, 72, 78, 85, 92, 88, 95]
            },
            'top5_unidades': {
                'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
                'values': [100, 85, 75, 68, 62]
            },
            'cumplimiento': {
                'labels': ['Completados', 'En Progreso', 'Pendientes', 'Retrasados'],
                'values': [70, 20, 8, 2]
            },
            'menor_avance': {
                'labels': ['Mod 8 - RRHH', 'Mod 7 - Salud', 'Mod 6 - Ciber', 'Mod 5 - Seguridad', 'Mod 4 - Rel. Lab.'],
                'values': [45, 52, 58, 65, 72]
            }
        }

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📊 Dashboards Gerenciales")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Botón actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Grid de gráficas (3 filas x 2 columnas)
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        # Gráfica 1: Usuarios por Unidad
        chart1 = self._create_chart_card(
            "👥 Usuarios por Unidad",
            'bar',
            self.datos_graficas['usuarios_unidad']
        )
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2: Progreso por Unidades
        chart2 = self._create_chart_card(
            "📈 Progreso por Unidades",
            'donut',
            self.datos_graficas['progreso_unidades']
        )
        charts_grid.addWidget(chart2, 0, 1)

        # Gráfica 3: Tendencia Semanal
        chart3 = self._create_chart_card(
            "📊 Tendencia Semanal",
            'line',
            self.datos_graficas['tendencia_semanal']
        )
        charts_grid.addWidget(chart3, 1, 0)

        # Gráfica 4: Top 5 Unidades
        chart4 = self._create_chart_card(
            "🏆 Top 5 Unidades",
            'bar',
            self.datos_graficas['top5_unidades']
        )
        charts_grid.addWidget(chart4, 1, 1)

        # Gráfica 5: Cumplimiento de Objetivos
        chart5 = self._create_chart_card(
            "🎯 Cumplimiento de Objetivos",
            'donut',
            self.datos_graficas['cumplimiento']
        )
        charts_grid.addWidget(chart5, 2, 0)

        # Gráfica 6: Módulos con Menor Avance
        chart6 = self._create_chart_card(
            "📉 Módulos con Menor Avance",
            'bar',
            self.datos_graficas['menor_avance']
        )
        charts_grid.addWidget(chart6, 2, 1)

        layout.addLayout(charts_grid)

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

    def _refresh_data(self):
        """Actualizar datos"""
        print("🔄 Actualizando dashboards gerenciales...")
