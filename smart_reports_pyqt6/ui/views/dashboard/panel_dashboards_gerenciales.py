"""
Panel de Dashboards Gerenciales - PyQt6
Replicando diseño de CustomTkinter con todas las funcionalidades
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class MetricCard(QFrame):
    """Tarjeta de métrica - CUADRADA Y CENTRADA"""

    def __init__(self, icon: str, title: str, value: str, subtitle: str, theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(240)  # MÁS CUADRADO
        self.setMinimumWidth(280)   # MÁS CUADRADO
        self.setMaximumWidth(350)   # MÁS CUADRADO

        # Aplicar estilo
        self._apply_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        is_dark = theme_manager.is_dark_mode() if theme_manager else False

        # Ícono - CENTRADO
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 42))
        icon_color = "#ffffff" if is_dark else "#002E6D"
        icon_label.setStyleSheet(f"color: {icon_color}; background: transparent; border: none;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Valor - CENTRADO Y GRANDE
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        text_color = "#ffffff" if is_dark else "#002E6D"
        value_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        # Título - CENTRADO
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_color = "#b0b0b0" if is_dark else "#666666"
        title_label.setStyleSheet(f"color: {title_color}; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Subtítulo - CENTRADO
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setWordWrap(True)
        subtitle_color = "#999999" if is_dark else "#888888"
        subtitle_label.setStyleSheet(f"color: {subtitle_color}; background: transparent; border: none;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

    def _apply_theme(self):
        """Aplicar tema"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#002E6D"  # Navy siempre

        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 15px;
            }}
        """)


class ChartCard(QFrame):
    """Contenedor para gráficas con botón expandir y menú"""

    expand_clicked = pyqtSignal()
    menu_clicked = pyqtSignal()

    def __init__(self, title: str, theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(350)  # Altura mínima para gráficas

        # Aplicar estilo
        self._apply_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header con título y botones
        header = QFrame()
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 12, 15, 12)
        header_layout.setSpacing(10)

        # Título
        is_dark = theme_manager.is_dark_mode() if theme_manager else False
        text_color = "#ffffff" if is_dark else "#002E6D"

        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Botón de expandir
        expand_btn = QPushButton("↗")
        expand_btn.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        expand_btn.setFixedSize(36, 36)
        expand_btn.setStyleSheet("""
            QPushButton {
                background-color: #00B5E2;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #009BDE;
            }
        """)
        expand_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        expand_btn.clicked.connect(self.expand_clicked.emit)
        header_layout.addWidget(expand_btn)

        # Botón de menú (3 puntos)
        menu_btn = QPushButton("⋮")
        menu_btn.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        menu_btn.setFixedSize(36, 36)
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.clicked.connect(self.menu_clicked.emit)
        header_layout.addWidget(menu_btn)

        layout.addWidget(header)

        # Container para el contenido (gráfica)
        self.content_container = QFrame()
        self.content_container.setStyleSheet("background: transparent; border: none;")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(15, 5, 15, 15)
        layout.addWidget(self.content_container)

    def _apply_theme(self):
        """Aplicar tema al contenedor"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#002E6D"

        self.setStyleSheet(f"""
            ChartCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """)

    def add_content(self, widget):
        """Agregar contenido al contenedor"""
        self.content_layout.addWidget(widget)


class DashboardsGerencialesPanel(QWidget):
    """Panel de Dashboards Gerenciales - Diseño modernizado"""

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

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
        """Crear interfaz completa"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)  # SIN MÁRGENES GRISES
        layout.setSpacing(15)

        # Scroll área
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(20)

        # ═══ HEADER ═══
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(5)

        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#002E6D"

        title = QLabel("📊 Dashboards Interactivos - Sistema Gerencial")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {title_color}; background: transparent; border: none;")
        header_layout.addWidget(title)

        subtitle = QLabel("Visualiza métricas y estadísticas en tiempo real")
        subtitle.setFont(QFont("Montserrat", 14))
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; background: transparent; border: none;")
        header_layout.addWidget(subtitle)

        scroll_layout.addWidget(header)

        # ═══ MÉTRICAS (3 CONTENEDORES CUADRADOS) ═══
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("background: transparent; border: none;")
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setSpacing(15)
        metrics_layout.setColumnStretch(0, 1)
        metrics_layout.setColumnStretch(1, 1)
        metrics_layout.setColumnStretch(2, 1)

        # Card 1: Total de Usuarios
        metric1 = MetricCard(
            icon="👥",
            title="Total de Usuarios",
            value="1,525",
            subtitle="Usuarios activos en el sistema",
            theme_manager=self.theme_manager
        )
        metrics_layout.addWidget(metric1, 0, 0, Qt.AlignmentFlag.AlignCenter)

        # Card 2: Módulo Actual
        metric2 = MetricCard(
            icon="📄",
            title="Módulo Actual",
            value="Módulo 8",
            subtitle="Procesos de Recursos Humanos",
            theme_manager=self.theme_manager
        )
        metrics_layout.addWidget(metric2, 0, 1, Qt.AlignmentFlag.AlignCenter)

        # Card 3: Tasa de Completado
        metric3 = MetricCard(
            icon="✓",
            title="Tasa de Completado",
            value="70.0%",
            subtitle="Progreso general del instituto",
            theme_manager=self.theme_manager
        )
        metrics_layout.addWidget(metric3, 0, 2, Qt.AlignmentFlag.AlignCenter)

        scroll_layout.addWidget(metrics_frame)

        # ═══ GRÁFICAS (2 POR FILA) ═══
        charts_frame = QFrame()
        charts_frame.setStyleSheet("background: transparent; border: none;")
        charts_layout = QGridLayout(charts_frame)
        charts_layout.setSpacing(15)
        charts_layout.setColumnStretch(0, 1)
        charts_layout.setColumnStretch(1, 1)

        # FILA 1
        chart1 = self._create_chart_card(
            "📊 Usuarios por Unidad de Negocio",
            'usuarios_unidad'
        )
        charts_layout.addWidget(chart1, 0, 0)

        chart2 = self._create_chart_card(
            "🍩 Progreso General por Unidad",
            'progreso_unidades'
        )
        charts_layout.addWidget(chart2, 0, 1)

        # FILA 2
        chart3 = self._create_chart_card(
            "📈 Tendencia Semanal",
            'tendencia_semanal'
        )
        charts_layout.addWidget(chart3, 1, 0)

        chart4 = self._create_chart_card(
            "📊 Top 5 Unidades de Mayor Progreso",
            'top5_unidades'
        )
        charts_layout.addWidget(chart4, 1, 1)

        # FILA 3
        chart5 = self._create_chart_card(
            "🎯 Cumplimiento de Objetivos",
            'cumplimiento'
        )
        charts_layout.addWidget(chart5, 2, 0)

        chart6 = self._create_chart_card(
            "📉 Módulos con Menor Avance",
            'menor_avance'
        )
        charts_layout.addWidget(chart6, 2, 1)

        scroll_layout.addWidget(charts_frame)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def _create_chart_card(self, title, chart_id):
        """Crear tarjeta con gráfico"""

        card = ChartCard(title, self.theme_manager)
        card.expand_clicked.connect(lambda: self._on_expand_chart(chart_id, title))
        card.menu_clicked.connect(lambda: self._on_menu_chart(chart_id, title))

        # Agregar gráfico placeholder
        data = self.datos_graficas.get(chart_id, {'labels': [], 'values': []})

        placeholder = QLabel(f"📊 Gráfico: {title}\n\n{len(data['values'])} elementos")
        placeholder.setFont(QFont("Montserrat", 12))
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(280)  # ALTURA MÍNIMA PARA VER GRÁFICA COMPLETA

        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#b0b0b0" if is_dark else "#666666"
        placeholder.setStyleSheet(f"color: {text_color}; background: transparent;")

        card.add_content(placeholder)

        return card

    def _on_expand_chart(self, chart_id, title):
        """Expandir gráfico"""
        print(f"↗ Expandir gráfico: {title} ({chart_id})")
        # TODO: Implementar expansión de gráfico

    def _on_menu_chart(self, chart_id, title):
        """Abrir menú de gráfico"""
        print(f"⋮ Menú gráfico: {title} ({chart_id})")
        # TODO: Implementar menú de opciones
