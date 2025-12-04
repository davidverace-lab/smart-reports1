"""
Panel de Control Ejecutivo - PyQt6
Dashboard de control ejecutivo con KPIs y métricas de alto nivel
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelControlEjecutivo(QWidget):
    """Panel de Control Ejecutivo"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # KPIs ejecutivos
        self.datos_ejecutivos = {
            'kpi_unidades': {
                'labels': ['ICAVE', 'TNG', 'ECV', 'HPMX', 'Container', 'Otros'],
                'values': [372, 276, 226, 195, 145, 311]
            },
            'cumplimiento_global': {
                'labels': ['Completado', 'En Progreso', 'Pendiente'],
                'values': [75, 20, 5]
            },
            'tendencia_trimestral': {
                'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
                'values': [58, 68, 75, 82]
            },
            'objetivos_estrategicos': {
                'labels': ['Capacitación', 'Seguridad', 'Calidad', 'Operaciones'],
                'values': [92, 88, 85, 79]
            }
        }

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header ejecutivo
        header_layout = QHBoxLayout()

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title = QLabel("📊 Control Ejecutivo")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        title_layout.addWidget(title)

        subtitle = QLabel("KPIs y métricas estratégicas")
        subtitle.setFont(QFont("Montserrat", 11))
        subtitle.setStyleSheet("color: #888888;")
        title_layout.addWidget(subtitle)

        header_layout.addWidget(title_container)
        header_layout.addStretch()

        # Badge ejecutivo
        badge = QLabel("🔒 Nivel Ejecutivo")
        badge.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        badge.setFixedHeight(30)
        badge.setStyleSheet("""
            QLabel {
                background-color: #003087;
                color: white;
                border-radius: 6px;
                padding: 5px 12px;
            }
        """)
        header_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addLayout(header_layout)

        # KPIs ejecutivos
        kpis_layout = QHBoxLayout()
        kpis_layout.setSpacing(15)

        kpis = [
            ("Cumplimiento Global", "75%", "🎯"),
            ("Unidades Activas", "11", "🏢"),
            ("Objetivos Logrados", "92%", "✅"),
            ("ROI Capacitación", "+34%", "💰"),
        ]

        for label, value, icon in kpis:
            kpi_card = self._create_kpi_card(label, value, icon)
            kpis_layout.addWidget(kpi_card)

        layout.addLayout(kpis_layout)

        # Grid de análisis
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        # Gráfica 1
        chart1 = self._create_chart_card(
            "🏢 Desempeño por Unidad",
            'bar',
            self.datos_ejecutivos['kpi_unidades']
        )
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2 = self._create_chart_card(
            "📊 Cumplimiento Global",
            'donut',
            self.datos_ejecutivos['cumplimiento_global']
        )
        charts_grid.addWidget(chart2, 0, 1)

        # Gráfica 3
        chart3 = self._create_chart_card(
            "📈 Tendencia Trimestral",
            'line',
            self.datos_ejecutivos['tendencia_trimestral']
        )
        charts_grid.addWidget(chart3, 1, 0)

        # Gráfica 4
        chart4 = self._create_chart_card(
            "🎯 Objetivos Estratégicos",
            'bar',
            self.datos_ejecutivos['objetivos_estrategicos']
        )
        charts_grid.addWidget(chart4, 1, 1)

        layout.addLayout(charts_grid)

    def _create_kpi_card(self, label, value, icon):
        """Crear tarjeta de KPI"""

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
        value_label.setStyleSheet("color: #00D4AA;")
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
