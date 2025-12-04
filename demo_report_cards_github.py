"""
Demostración del widget ReportCardGitHub
Muestra múltiples tarjetas con diferentes configuraciones y capacidad de cambio de tema
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importar el componente personalizado
from smart_reports_pyqt6.ui.components.report_card_github import ReportCardGitHub


class DemoWindow(QMainWindow):
    """Ventana de demostración del componente ReportCardGitHub"""

    def __init__(self):
        super().__init__()

        self.current_theme = "dark"  # Tema inicial
        self.cards = []  # Lista para guardar referencias a las tarjetas

        self.setWindowTitle("Demo: ReportCardGitHub - Estilo GitHub Actions")
        self.setMinimumSize(1200, 800)

        # Crear UI
        self._create_ui()

        # Aplicar tema inicial
        self._apply_global_theme()

    def _create_ui(self):
        """Crear la interfaz principal"""

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # === HEADER CON TÍTULO Y BOTÓN DE TEMA ===
        header_layout = QHBoxLayout()

        # Título principal
        title_label = QLabel("🎨 Demo: Widget de Reportes - Estilo GitHub Actions")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.title_label = title_label
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Botón para cambiar tema
        self.theme_toggle_btn = QPushButton("🌙 Cambiar a Tema Claro")
        self.theme_toggle_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.theme_toggle_btn.setFixedHeight(45)
        self.theme_toggle_btn.setFixedWidth(250)
        self.theme_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_toggle_btn)

        main_layout.addLayout(header_layout)

        # Subtítulo
        subtitle = QLabel("Haz clic en el botón de arriba para alternar entre modo claro y oscuro")
        subtitle.setFont(QFont("Segoe UI", 11))
        self.subtitle_label = subtitle
        main_layout.addWidget(subtitle)

        # === SCROLL AREA CON GRID DE TARJETAS ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)

        # Grid de tarjetas
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # === DEFINIR LAS TARJETAS DE REPORTE ===
        reports_config = [
            {
                "title": "Reporte de Ventas Mensual",
                "description": "Genera un PDF detallado con gráficos de rendimiento y métricas de ventas del mes actual.",
                "button_text": "Generar",
                "format_label": "Formato: PDF",
                "icon_name": "report"
            },
            {
                "title": "Análisis de Usuario",
                "description": "Reporte completo del progreso y actividad de usuarios individuales en el sistema.",
                "button_text": "Configurar",
                "format_label": "Formato: Excel",
                "icon_name": "analytics"
            },
            {
                "title": "Reporte por Período",
                "description": "Genera reportes personalizados para rangos de fechas específicos con estadísticas detalladas.",
                "button_text": "Seleccionar Fechas",
                "format_label": "Formato: PDF",
                "icon_name": "calendar"
            },
            {
                "title": "Reporte Global",
                "description": "Vista general completa del sistema con todas las métricas y KPIs principales.",
                "button_text": "Generar",
                "format_label": "Formato: PDF",
                "icon_name": "report"
            },
            {
                "title": "Exportar a Impresora",
                "description": "Envía directamente el reporte a la impresora configurada sin generar archivo.",
                "button_text": "Imprimir",
                "format_label": "Salida: Impresora",
                "icon_name": "printer"
            },
            {
                "title": "Reporte Ejecutivo",
                "description": "Resumen ejecutivo con los indicadores más importantes para la toma de decisiones.",
                "button_text": "Vista Previa",
                "format_label": "Formato: PDF",
                "icon_name": "pdf"
            }
        ]

        # Crear y agregar tarjetas al grid
        row = 0
        col = 0
        for config in reports_config:
            card = ReportCardGitHub(
                title=config["title"],
                description=config["description"],
                button_text=config["button_text"],
                format_label=config["format_label"],
                icon_name=config["icon_name"],
                theme=self.current_theme
            )

            # Conectar señal de clic
            card.action_clicked.connect(lambda t=config["title"]: self._on_card_action(t))

            # Guardar referencia
            self.cards.append(card)

            # Agregar al grid (3 columnas)
            grid_layout.addWidget(card, row, col)

            col += 1
            if col > 2:  # 3 tarjetas por fila
                col = 0
                row += 1

        scroll_layout.addLayout(grid_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # === FOOTER CON INFORMACIÓN ===
        footer_label = QLabel(
            "💡 Tip: Observa cómo los iconos cambian de color automáticamente al alternar el tema. "
            "Blanco en modo oscuro, Azul Navy en modo claro."
        )
        footer_label.setFont(QFont("Segoe UI", 10))
        footer_label.setWordWrap(True)
        self.footer_label = footer_label
        main_layout.addWidget(footer_label)

    def _toggle_theme(self):
        """Alternar entre tema claro y oscuro"""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_toggle_btn.setText("🌙 Cambiar a Tema Oscuro")
        else:
            self.current_theme = "dark"
            self.theme_toggle_btn.setText("☀️ Cambiar a Tema Claro")

        # Aplicar tema a todas las tarjetas
        for card in self.cards:
            card.set_theme(self.current_theme)

        # Aplicar tema global a la ventana
        self._apply_global_theme()

    def _apply_global_theme(self):
        """Aplicar tema global a la ventana principal"""
        is_dark = (self.current_theme == "dark")

        if is_dark:
            # MODO OSCURO
            window_bg = "#0d1117"
            text_color = "#c9d1d9"
            subtitle_color = "#8b949e"
            button_bg = "#21262d"
            button_hover = "#30363d"
        else:
            # MODO CLARO
            window_bg = "#f6f8fa"
            text_color = "#24292f"
            subtitle_color = "#57606a"
            button_bg = "#ffffff"
            button_hover = "#f3f4f6"

        # Estilo de la ventana principal
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {window_bg};
            }}
            QWidget {{
                background-color: {window_bg};
            }}
            QScrollArea {{
                background-color: {window_bg};
                border: none;
            }}
        """)

        # Actualizar colores de los labels
        self.title_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        self.subtitle_label.setStyleSheet(f"color: {subtitle_color}; background: transparent;")
        self.footer_label.setStyleSheet(f"color: {subtitle_color}; background: transparent;")

        # Actualizar estilo del botón de tema
        self.theme_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                color: {text_color};
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
                border-color: #8b949e;
            }}
            QPushButton:pressed {{
                background-color: {button_bg};
            }}
        """)

    def _on_card_action(self, report_title: str):
        """Manejar el clic en el botón de acción de una tarjeta"""
        print(f"✅ Acción ejecutada: {report_title}")


def main():
    """Función principal"""
    app = QApplication(sys.argv)

    # Configurar la aplicación
    app.setApplicationName("ReportCardGitHub Demo")
    app.setOrganizationName("Smart Reports")

    # Crear y mostrar ventana
    window = DemoWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
