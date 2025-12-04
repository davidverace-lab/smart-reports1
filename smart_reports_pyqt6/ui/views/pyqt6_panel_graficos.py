"""
Panel de Gráficos Interactivos
PyQt6 Version - Ejemplos y demos de gráficos D3.js
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


class GraficosPanel(QWidget):
    """Panel de Gráficos Interactivos"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📈 Gráficos Interactivos")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Selector de tipo
        type_label = QLabel("Tipo:")
        type_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(type_label)

        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Barras", "Donut", "Líneas"])
        self.chart_type_combo.currentIndexChanged.connect(self._change_chart_type)
        header_layout.addWidget(self.chart_type_combo)

        # Selector de datos
        data_label = QLabel("Datos:")
        data_label.setFont(QFont("Montserrat", 10, QFont.Weight.Bold))
        header_layout.addWidget(data_label)

        self.data_combo = QComboBox()
        self.data_combo.addItems(["Ventas Mensuales", "Usuarios por Unidad", "Progreso Semanal"])
        self.data_combo.currentIndexChanged.connect(self._change_data)
        header_layout.addWidget(self.data_combo)

        # Botón actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._refresh_chart)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Frame del gráfico principal
        chart_frame = QFrame()
        chart_frame.setFrameShape(QFrame.Shape.StyledPanel)
        chart_frame.setMinimumHeight(500)

        chart_layout = QVBoxLayout(chart_frame)

        self.main_chart = D3ChartWidget(chart_frame)
        chart_layout.addWidget(self.main_chart)

        layout.addWidget(chart_frame)

        # Info
        info_label = QLabel(
            "💡 <b>Características:</b> Tooltips interactivos, hover effects, "
            "animaciones suaves y click handlers personalizados"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("padding: 10px; background-color: rgba(0,0,0,0.1); border-radius: 5px;")
        layout.addWidget(info_label)

        # Galería de ejemplos
        gallery_label = QLabel("Ejemplos de Gráficos:")
        gallery_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(gallery_label)

        gallery_layout = QHBoxLayout()
        gallery_layout.setSpacing(15)

        # Ejemplo 1
        example1_btn = QPushButton("📊 Barras Horizontales")
        example1_btn.setFixedHeight(50)
        example1_btn.clicked.connect(lambda: self._show_example('bar_h'))
        gallery_layout.addWidget(example1_btn)

        # Ejemplo 2
        example2_btn = QPushButton("🍩 Gráfico Donut")
        example2_btn.setFixedHeight(50)
        example2_btn.clicked.connect(lambda: self._show_example('donut'))
        gallery_layout.addWidget(example2_btn)

        # Ejemplo 3
        example3_btn = QPushButton("📈 Líneas de Tiempo")
        example3_btn.setFixedHeight(50)
        example3_btn.clicked.connect(lambda: self._show_example('line'))
        gallery_layout.addWidget(example3_btn)

        layout.addLayout(gallery_layout)

        layout.addStretch()

        # Cargar gráfico inicial
        self._load_initial_chart()

    def _load_initial_chart(self):
        """Cargar gráfico inicial"""

        data = {
            'labels': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
            'values': [120, 190, 150, 280, 210, 245]
        }

        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

        self.main_chart.set_chart(
            'bar',
            'Ventas Mensuales 2024',
            data,
            subtitle='Datos de ejemplo',
            tema=tema
        )

    def _change_chart_type(self, index):
        """Cambiar tipo de gráfico"""
        self._refresh_chart()

    def _change_data(self, index):
        """Cambiar conjunto de datos"""
        self._refresh_chart()

    def _refresh_chart(self):
        """Actualizar gráfico con selecciones actuales"""

        # Obtener tipo
        chart_type_text = self.chart_type_combo.currentText()
        chart_type_map = {
            'Barras': 'bar',
            'Donut': 'donut',
            'Líneas': 'line'
        }
        chart_type = chart_type_map.get(chart_type_text, 'bar')

        # Obtener datos según selección
        data_text = self.data_combo.currentText()
        data_map = {
            'Ventas Mensuales': {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'values': [120, 190, 150, 280, 210, 245]
            },
            'Usuarios por Unidad': {
                'labels': ['ICAVE', 'TNG', 'ECV', 'HPMX', 'Container'],
                'values': [372, 276, 226, 195, 145]
            },
            'Progreso Semanal': {
                'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                'values': [65, 72, 78, 85, 92, 88, 95]
            }
        }
        data = data_map.get(data_text, data_map['Ventas Mensuales'])

        # Actualizar gráfico
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

        self.main_chart.set_chart(
            chart_type,
            data_text,
            data,
            subtitle='Actualizado',
            tema=tema
        )

        print(f"✅ Gráfico actualizado: {chart_type} - {data_text}")

    def _show_example(self, example_type):
        """Mostrar ejemplo específico"""

        examples = {
            'bar_h': {
                'type': 'bar',
                'title': 'Top 10 Productos',
                'data': {
                    'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
                    'values': [450, 380, 310, 280, 220]
                }
            },
            'donut': {
                'type': 'donut',
                'title': 'Distribución de Ventas',
                'data': {
                    'labels': ['Online', 'Tienda Física', 'Mayoreo', 'Otros'],
                    'values': [45, 30, 20, 5]
                }
            },
            'line': {
                'type': 'line',
                'title': 'Evolución Trimestral',
                'data': {
                    'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
                    'values': [2500, 3200, 2800, 4100]
                }
            }
        }

        if example_type in examples:
            ex = examples[example_type]
            tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

            self.main_chart.set_chart(
                ex['type'],
                ex['title'],
                ex['data'],
                subtitle='Ejemplo de demostración',
                tema=tema
            )
