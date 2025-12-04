"""
Panel de Dashboard Moderno - PyQt6
Dashboard moderno con diseño actualizado y métricas en tiempo real
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelDashboardModerno(QWidget):
    """Panel de Dashboard Moderno"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Datos modernos
        self.datos_modernos = {
            'usuarios_activos': {
                'labels': ['0-6h', '6-12h', '12-18h', '18-24h'],
                'values': [120, 280, 450, 175]
            },
            'modulos_populares': {
                'labels': ['Seguridad', 'Operaciones', 'Calidad', 'Liderazgo', 'TI'],
                'values': [450, 380, 320, 285, 240]
            },
            'tasa_completado': {
                'labels': ['Completados', 'En Progreso', 'No Iniciados'],
                'values': [68, 25, 7]
            },
            'actividad_mensual': {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'values': [3200, 3450, 3680, 3920, 4150, 4380]
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

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        title = QLabel("Dashboard Moderno")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        title_layout.addWidget(title)

        subtitle = QLabel("Métricas en tiempo real y análisis avanzado")
        subtitle.setFont(QFont("Montserrat", 11))
        subtitle.setStyleSheet("color: #888888;")
        title_layout.addWidget(subtitle)

        header_layout.addWidget(title_container)
        header_layout.addStretch()

        refresh_btn = QPushButton("Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Métricas principales con diseño moderno
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Usuarios Activos", "1,025", "👤", "#00D4AA"),
            ("Módulos Activos", "124", "📚", "#003087"),
            ("Tasa Completado", "68%", "✅", "#00D4AA"),
            ("Tiempo Promedio", "4.5h", "⏱️", "#003087"),
        ]

        for label, value, icon, color in metrics:
            metric_card = self._create_modern_metric_card(label, value, icon, color)
            metrics_layout.addWidget(metric_card)

        layout.addLayout(metrics_layout)

        # Grid de gráficas
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        # Gráfica 1
        chart1 = self._create_chart_card(
            "Usuarios Activos por Hora",
            'bar',
            self.datos_modernos['usuarios_activos']
        )
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2 = self._create_chart_card(
            "Módulos Más Populares",
            'bar',
            self.datos_modernos['modulos_populares']
        )
        charts_grid.addWidget(chart2, 0, 1)

        # Gráfica 3
        chart3 = self._create_chart_card(
            "Tasa de Completado",
            'donut',
            self.datos_modernos['tasa_completado']
        )
        charts_grid.addWidget(chart3, 1, 0)

        # Gráfica 4
        chart4 = self._create_chart_card(
            "Actividad Mensual",
            'line',
            self.datos_modernos['actividad_mensual']
        )
        charts_grid.addWidget(chart4, 1, 1)

        layout.addLayout(charts_grid)

    def _create_modern_metric_card(self, label, value, icon, color):
        """Crear tarjeta de métrica moderna"""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                border-left: 4px solid {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Icono
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 28))
        layout.addWidget(icon_label)

        # Valor
        value_label = QLabel(value)
        value_label.setFont(QFont("Montserrat", 26, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
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
        print("🔄 Actualizando dashboard moderno...")
