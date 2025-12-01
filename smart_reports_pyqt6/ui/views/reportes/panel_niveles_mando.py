"""
Panel de Reporte de Niveles de Mando - PyQt6
Reporte por niveles jerárquicos de la organización
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget


class PanelNivelesMando(QWidget):
    """Panel de Reporte de Niveles de Mando"""

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

        title = QLabel("🎯 Reporte por Niveles de Mando")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        generate_btn = QPushButton("🔄 Actualizar")
        generate_btn.setFixedHeight(40)
        generate_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(generate_btn)

        layout.addLayout(header_layout)

        # Tabs por nivel
        tabs = QTabWidget()

        # Tab 1: Alta Dirección
        tab1 = self._create_level_tab("Alta Dirección", {
            'personal': 45,
            'completado': 95,
            'modulos': ['Liderazgo Estratégico', 'Gestión del Cambio', 'Toma de Decisiones'],
            'grafico_data': {
                'labels': ['Liderazgo', 'Gestión', 'Estrategia', 'Innovación'],
                'values': [98, 95, 92, 90]
            }
        })
        tabs.addTab(tab1, "🎩 Alta Dirección")

        # Tab 2: Mando Medio
        tab2 = self._create_level_tab("Mando Medio", {
            'personal': 182,
            'completado': 85,
            'modulos': ['Supervisión', 'Gestión de Equipos', 'Resolución de Conflictos'],
            'grafico_data': {
                'labels': ['Supervisión', 'Equipos', 'Conflictos', 'Comunicación'],
                'values': [88, 85, 82, 80]
            }
        })
        tabs.addTab(tab2, "👔 Mando Medio")

        # Tab 3: Operativo
        tab3 = self._create_level_tab("Personal Operativo", {
            'personal': 1298,
            'completado': 72,
            'modulos': ['Seguridad', 'Operaciones', 'Calidad', 'Procedimientos'],
            'grafico_data': {
                'labels': ['Seguridad', 'Operaciones', 'Calidad', 'Procedimientos'],
                'values': [78, 75, 70, 68]
            }
        })
        tabs.addTab(tab3, "👷 Operativo")

        layout.addWidget(tabs)

    def _create_level_tab(self, level_name, data):
        """Crear tab para un nivel"""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(20, 20, 20, 20)
        tab_layout.setSpacing(15)

        # Métricas del nivel
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        metrics = [
            ("Total Personal", str(data['personal']), "👥"),
            ("% Completado", f"{data['completado']}%", "✅"),
            ("Módulos Activos", str(len(data['modulos'])), "📚"),
        ]

        for label, value, icon in metrics:
            metric_card = self._create_metric_card(label, value, icon)
            metrics_layout.addWidget(metric_card)

        tab_layout.addLayout(metrics_layout)

        # Módulos principales
        modulos_frame = QFrame()
        modulos_frame.setFrameShape(QFrame.Shape.StyledPanel)
        modulos_layout = QVBoxLayout(modulos_frame)
        modulos_layout.setContentsMargins(15, 15, 15, 15)

        modulos_title = QLabel(f"📚 Módulos Principales - {level_name}")
        modulos_title.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        modulos_layout.addWidget(modulos_title)

        for modulo in data['modulos']:
            modulo_label = QLabel(f"• {modulo}")
            modulo_label.setFont(QFont("Montserrat", 10))
            modulos_layout.addWidget(modulo_label)

        tab_layout.addWidget(modulos_frame)

        # Gráfico de avance
        chart_card = self._create_chart_card(
            f"Avance por Categoría - {level_name}",
            'bar',
            data['grafico_data']
        )
        tab_layout.addWidget(chart_card)

        tab_layout.addStretch()

        return tab

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

    def _refresh_data(self):
        """Actualizar datos"""
        print("🔄 Actualizando reporte de niveles de mando...")
