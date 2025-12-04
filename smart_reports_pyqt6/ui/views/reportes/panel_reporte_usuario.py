"""
Panel de Reporte por Usuario - PyQt6
Reporte detallado de un usuario específico
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class PanelReporteUsuario(QWidget):
    """Panel de Reporte por Usuario"""

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

        title = QLabel("👤 Reporte por Usuario")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Búsqueda de usuario
        search_label = QLabel("Usuario:")
        search_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o ID...")
        self.search_input.setFixedWidth(250)
        header_layout.addWidget(self.search_input)

        search_btn = QPushButton("🔍 Buscar")
        search_btn.setFixedHeight(40)
        search_btn.clicked.connect(self._search_user)
        header_layout.addWidget(search_btn)

        layout.addLayout(header_layout)

        # Info del usuario
        user_info_frame = QFrame()
        user_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        user_info_layout = QVBoxLayout(user_info_frame)
        user_info_layout.setContentsMargins(20, 20, 20, 20)

        info_title = QLabel("📋 Información del Usuario")
        info_title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        user_info_layout.addWidget(info_title)

        info_text = QLabel(
            "• Nombre: Juan Pérez García\n"
            "• Unidad: ICAVE\n"
            "• Puesto: Supervisor de Operaciones\n"
            "• Nivel: Mando Medio\n"
            "• Fecha ingreso: 15/01/2023"
        )
        info_text.setFont(QFont("Montserrat", 11))
        user_info_layout.addWidget(info_text)

        layout.addWidget(user_info_frame)

        # Métricas del usuario
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Módulos Completados", "12", "✅"),
            ("Avance Total", "85%", "📊"),
            ("Horas Capacitación", "45h", "⏱️"),
            ("Calificación Prom", "9.2", "⭐"),
        ]

        for label, value, icon in metrics:
            metric_card = self._create_metric_card(label, value, icon)
            metrics_layout.addWidget(metric_card)

        layout.addLayout(metrics_layout)

        # Gráficas del usuario
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # Gráfica 1
        chart1_data = {
            'labels': ['Seg', 'Op', 'Cal', 'Lid', 'TI'],
            'values': [95, 88, 85, 80, 75]
        }
        chart1 = self._create_chart_card("Avance por Categoría", 'bar', chart1_data)
        charts_grid.addWidget(chart1, 0, 0)

        # Gráfica 2
        chart2_data = {
            'labels': ['Completado', 'En Progreso', 'Pendiente'],
            'values': [85, 12, 3]
        }
        chart2 = self._create_chart_card("Estado de Módulos", 'donut', chart2_data)
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

    def _search_user(self):
        """Buscar usuario"""
        search_text = self.search_input.text()
        print(f"🔍 Buscando usuario: {search_text}...")
