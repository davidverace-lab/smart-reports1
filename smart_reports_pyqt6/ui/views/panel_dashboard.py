"""
Panel de Dashboard - Control Ejecutivo
PyQt6 Version - Migrado desde CustomTkinter
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget


# Datos del dashboard
USUARIOS_POR_UNIDAD_DATA = {
    'labels': ['LCMT', 'HPLM', 'ECV', 'TILH', 'CCI', 'TNG', 'HPMX', 'TIMSA', 'LCT', 'EIT', 'ICAVE'],
    'values': [3, 9, 23, 71, 76, 129, 145, 195, 226, 276, 372]
}

PROGRESO_UNIDADES_DATA = {
    'labels': ['TNG - 100%', 'ICAVE - 82%', 'ECV - 75%', 'Container - 68%', 'HPMX - 62%'],
    'values': [100, 82, 75, 68, 62]
}

TENDENCIA_SEMANAL_DATA = {
    'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
    'values': [65, 72, 78, 85, 92, 88, 95]
}

TOP_5_UNIDADES_DATA = {
    'labels': ['TNG', 'ICAVE', 'ECV', 'Container', 'HPMX'],
    'values': [100, 85, 75, 68, 62]
}

CUMPLIMIENTO_OBJETIVOS_DATA = {
    'labels': ['Completados', 'En Progreso', 'Pendientes', 'Retrasados'],
    'values': [70, 20, 8, 2]
}

MODULOS_MENOR_AVANCE_DATA = {
    'labels': ['Mod 8 - RRHH', 'Mod 7 - Salud', 'Mod 6 - Ciber', 'Mod 5 - Seguridad', 'Mod 4 - Rel. Lab.'],
    'values': [45, 52, 58, 65, 72]
}


class MetricCard(QFrame):
    """Tarjeta de métrica"""

    def __init__(self, title: str, value: str, icon: str = "📊", parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        # Icono
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 32))
        layout.addWidget(icon_label)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 10))
        title_label.setStyleSheet("color: #888888;")
        layout.addWidget(title_label)

        # Valor
        value_label = QLabel(value)
        value_label.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        layout.addWidget(value_label)


class ChartCard(QFrame):
    """Tarjeta con gráfico D3.js"""

    def __init__(self, title: str, chart_type: str, data: dict, theme: str = 'dark', parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Gráfico
        self.chart_widget = D3ChartWidget(self)
        self.chart_widget.set_chart(chart_type, title, data, tema=theme)
        layout.addWidget(self.chart_widget)


class DashboardPanel(QWidget):
    """Panel de Dashboard - Control Ejecutivo"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📊 Panel de Control Ejecutivo")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setFixedWidth(150)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)

        main_layout.addLayout(header_layout)

        # Métricas principales
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Total Usuarios", "1,525", "👥"),
            ("Unidades Activas", "11", "🏢"),
            ("Progreso Promedio", "78%", "📈"),
            ("Módulos Completados", "70%", "✅")
        ]

        for title, value, icon in metrics:
            card = MetricCard(title, value, icon)
            metrics_layout.addWidget(card)

        main_layout.addLayout(metrics_layout)

        # Gráficos en grid
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

        # Primera fila de gráficos
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(15)

        chart1 = ChartCard("Usuarios por Unidad", "bar", USUARIOS_POR_UNIDAD_DATA, tema)
        chart2 = ChartCard("Progreso por Unidades", "donut", PROGRESO_UNIDADES_DATA, tema)

        row1_layout.addWidget(chart1)
        row1_layout.addWidget(chart2)

        main_layout.addLayout(row1_layout)

        # Segunda fila de gráficos
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(15)

        chart3 = ChartCard("Tendencia Semanal", "line", TENDENCIA_SEMANAL_DATA, tema)
        chart4 = ChartCard("Top 5 Unidades", "bar", TOP_5_UNIDADES_DATA, tema)

        row2_layout.addWidget(chart3)
        row2_layout.addWidget(chart4)

        main_layout.addLayout(row2_layout)

        # Tercera fila de gráficos
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(15)

        chart5 = ChartCard("Cumplimiento de Objetivos", "donut", CUMPLIMIENTO_OBJETIVOS_DATA, tema)
        chart6 = ChartCard("Módulos con Menor Avance", "bar", MODULOS_MENOR_AVANCE_DATA, tema)

        row3_layout.addWidget(chart5)
        row3_layout.addWidget(chart6)

        main_layout.addLayout(row3_layout)

        # Spacer al final
        main_layout.addStretch()

    def _refresh_data(self):
        """Actualizar datos del dashboard"""
        print("🔄 Actualizando dashboard...")
        # TODO: Implementar recarga de datos desde BD
