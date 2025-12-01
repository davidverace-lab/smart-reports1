"""
Panel de Dashboard de RRHH - PyQt6
Dashboard de recursos humanos con métricas de personal
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget


class PanelRRHH(QWidget):
    """Panel de Dashboard de Recursos Humanos"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Datos específicos de RRHH
        self.datos_rrhh = {
            'personal_area': {
                'labels': ['Operaciones', 'Administración', 'Ventas', 'TI', 'RRHH', 'Seguridad'],
                'values': [450, 180, 120, 85, 45, 95]
            },
            'capacitacion_mes': {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'values': [120, 145, 135, 178, 165, 192]
            },
            'certificaciones': {
                'labels': ['Activas', 'Por Vencer', 'Vencidas', 'En Proceso'],
                'values': [65, 20, 10, 5]
            },
            'evaluaciones': {
                'labels': ['Excelente', 'Bueno', 'Regular', 'Mejorable'],
                'values': [45, 35, 15, 5]
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

        title = QLabel("👥 Dashboard de Recursos Humanos")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Métricas principales
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Total Empleados", "1,525", "👥"),
            ("En Capacitación", "192", "📚"),
            ("Certificados Activos", "487", "✅"),
            ("Tasa Cumplimiento", "95%", "📊"),
        ]

        for label, value, icon in metrics:
            metric_card = self._create_metric_card(label, value, icon)
            metrics_layout.addWidget(metric_card)

        layout.addLayout(metrics_layout)

        # Grid de gráficas
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        # Gráfica 1
        chart1 = self._create_chart_card(
            "👥 Personal por Área",
            'bar',
            self.datos_rrhh['personal_area']
        )
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2 = self._create_chart_card(
            "📚 Capacitaciones por Mes",
            'line',
            self.datos_rrhh['capacitacion_mes']
        )
        charts_grid.addWidget(chart2, 0, 1)

        # Gráfica 3
        chart3 = self._create_chart_card(
            "📜 Estado de Certificaciones",
            'donut',
            self.datos_rrhh['certificaciones']
        )
        charts_grid.addWidget(chart3, 1, 0)

        # Gráfica 4
        chart4 = self._create_chart_card(
            "⭐ Evaluaciones de Desempeño",
            'donut',
            self.datos_rrhh['evaluaciones']
        )
        charts_grid.addWidget(chart4, 1, 1)

        layout.addLayout(charts_grid)

    def _create_metric_card(self, label, value, icon):
        """Crear tarjeta de métrica"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFixedHeight(120)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Icono
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 32))
        layout.addWidget(icon_label)

        # Valor
        value_label = QLabel(value)
        value_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        layout.addWidget(value_label)

        # Label
        label_label = QLabel(label)
        label_label.setFont(QFont("Montserrat", 10))
        label_label.setStyleSheet("color: #888888;")
        layout.addWidget(label_label)

        return card

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
        print("🔄 Actualizando dashboard RRHH...")
