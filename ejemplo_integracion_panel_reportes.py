"""
Ejemplo de cómo integrar ReportCardGitHub con el panel de reportes existente
Este ejemplo muestra cómo reemplazar la ReportCard actual con la nueva versión
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importar el nuevo componente
from smart_reports_pyqt6.ui.components import ReportCardGitHub


class ReportesPanelMejorado(QWidget):
    """
    Panel de Reportes mejorado usando ReportCardGitHub
    Ejemplo de integración con theme_manager
    """

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection
        self.report_cards = []

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz principal"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # === HEADER ===
        header = self._create_header()
        layout.addWidget(header)

        # === SCROLL AREA CON TARJETAS ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)

        # Grid de tarjetas
        grid_layout = self._create_cards_grid()
        scroll_layout.addLayout(grid_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def _create_header(self):
        """Crear header con título y botón de tema"""

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#002E6D"

        title = QLabel("Generación de Reportes")
        self.title_label = title
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {title_color}; background: transparent;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Botón para cambiar tema (opcional - si no usas theme_manager)
        if not self.theme_manager:
            toggle_btn = QPushButton("🌙 Cambiar Tema")
            toggle_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            toggle_btn.setFixedHeight(40)
            toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            toggle_btn.clicked.connect(self._manual_toggle_theme)
            header_layout.addWidget(toggle_btn)

        return header

    def _create_cards_grid(self):
        """Crear grid de tarjetas de reportes"""

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Determinar tema actual
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else True
        current_theme = "dark" if is_dark else "light"

        # Configuración de reportes
        reports_config = [
            {
                "title": "Progreso de Usuario",
                "description": "Reporte detallado del progreso individual de cada usuario en el sistema.",
                "button_text": "Configurar",
                "format_label": "Formato: PDF",
                "icon_name": "report",
                "report_type": "usuario"
            },
            {
                "title": "Progreso por Unidad",
                "description": "Reporte de progreso organizado por unidad de negocio.",
                "button_text": "Generar",
                "format_label": "Formato: PDF",
                "icon_name": "analytics",
                "report_type": "unidad"
            },
            {
                "title": "Reporte por Período",
                "description": "Reporte de actividad en un rango de fechas específico.",
                "button_text": "Seleccionar Fechas",
                "format_label": "Formato: PDF",
                "icon_name": "calendar",
                "report_type": "periodo"
            },
            {
                "title": "Reporte Global",
                "description": "Vista general completa del sistema con todas las métricas principales.",
                "button_text": "Generar",
                "format_label": "Formato: PDF",
                "icon_name": "report",
                "report_type": "global"
            },
            {
                "title": "Niveles de Mando",
                "description": "Reporte organizado por niveles gerenciales y jerarquías.",
                "button_text": "Configurar",
                "format_label": "Formato: PDF",
                "icon_name": "analytics",
                "report_type": "niveles"
            },
            {
                "title": "Impresión Rápida",
                "description": "Envía el reporte directamente a la impresora configurada.",
                "button_text": "Imprimir",
                "format_label": "Salida: Impresora",
                "icon_name": "printer",
                "report_type": "imprimir"
            }
        ]

        # Crear tarjetas y agregar al grid
        row = 0
        col = 0

        for config in reports_config:
            card = ReportCardGitHub(
                title=config["title"],
                description=config["description"],
                button_text=config["button_text"],
                format_label=config["format_label"],
                icon_name=config["icon_name"],
                theme=current_theme
            )

            # Conectar acción
            report_type = config["report_type"]
            card.action_clicked.connect(lambda rt=report_type: self._open_report_generation(rt))

            # Guardar referencia
            self.report_cards.append(card)

            # Agregar al grid (3 columnas)
            grid_layout.addWidget(card, row, col)

            col += 1
            if col > 2:  # 3 tarjetas por fila
                col = 0
                row += 1

        return grid_layout

    def _open_report_generation(self, report_type: str):
        """Abrir vista de generación de reporte"""
        print(f"📄 Abriendo generación de reporte: {report_type}")

        # Aquí iría tu lógica para abrir la vista de generación
        # Por ejemplo, mostrar un QStackedWidget con los filtros
        # o abrir un diálogo de configuración

        # Ejemplo:
        # self.stack.setCurrentWidget(self.generation_view)

    def _on_theme_changed(self, new_theme: str):
        """Actualizar tema cuando cambia el theme_manager"""

        # Actualizar todas las tarjetas
        for card in self.report_cards:
            card.set_theme(new_theme)

        # Actualizar título
        is_dark = (new_theme == 'dark')
        title_color = "#ffffff" if is_dark else "#002E6D"

        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {title_color}; background: transparent;")

        # Actualizar fondo de la ventana
        bg_color = "#0d1117" if is_dark else "#f6f8fa"
        self.setStyleSheet(f"background-color: {bg_color};")

    def _manual_toggle_theme(self):
        """Cambiar tema manualmente (si no hay theme_manager)"""

        # Detectar tema actual de la primera tarjeta
        if self.report_cards:
            current = self.report_cards[0].current_theme
            new_theme = "light" if current == "dark" else "dark"

            # Actualizar todas las tarjetas
            for card in self.report_cards:
                card.set_theme(new_theme)

            # Actualizar colores del panel
            is_dark = (new_theme == 'dark')
            title_color = "#ffffff" if is_dark else "#002E6D"
            bg_color = "#0d1117" if is_dark else "#f6f8fa"

            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet(f"color: {title_color}; background: transparent;")

            self.setStyleSheet(f"background-color: {bg_color};")


# ============================================
# EJEMPLO DE USO CON THEME MANAGER EXISTENTE
# ============================================

def ejemplo_con_theme_manager():
    """
    Ejemplo de cómo usar el panel con tu theme_manager existente
    """
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication([])

    # Tu theme_manager existente
    # theme_manager = tu_theme_manager_aqui

    # Crear el panel mejorado
    # panel = ReportesPanelMejorado(theme_manager=theme_manager)

    # Usar en ventana principal
    window = QMainWindow()
    # window.setCentralWidget(panel)
    window.setWindowTitle("Panel de Reportes Mejorado")
    window.setGeometry(100, 100, 1200, 800)
    window.show()

    app.exec()


# ============================================
# EJEMPLO SIN THEME MANAGER
# ============================================

def ejemplo_sin_theme_manager():
    """
    Ejemplo standalone sin theme_manager
    """
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication([])

    # Crear panel sin theme_manager
    panel = ReportesPanelMejorado(theme_manager=None)

    window = QMainWindow()
    window.setCentralWidget(panel)
    window.setWindowTitle("Panel de Reportes Mejorado")
    window.setGeometry(100, 100, 1200, 800)
    window.show()

    app.exec()


# ============================================
# CÓMO MODIFICAR pyqt6_panel_reportes.py
# ============================================

"""
Para integrar en tu archivo pyqt6_panel_reportes.py existente:

1. Importa el nuevo componente al inicio del archivo:

    from smart_reports_pyqt6.ui.components import ReportCardGitHub

2. En el método _create_selection_view(), reemplaza la creación de ReportCard:

    # ANTES:
    card = ReportCard(title, desc, icon, self.theme_manager)

    # DESPUÉS:
    is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
    current_theme = "dark" if is_dark else "light"

    card = ReportCardGitHub(
        title=title,
        description=desc,
        button_text="Generar Reporte",
        format_label="Formato: PDF",
        icon_name=self._get_icon_name(title),  # Ver función auxiliar abajo
        theme=current_theme
    )

3. Agrega una función auxiliar para mapear títulos a iconos:

    def _get_icon_name(self, title: str) -> str:
        \"\"\"Obtener nombre de icono según el título del reporte\"\"\"
        icon_map = {
            "Progreso de Usuario": "report",
            "Progreso por Unidad": "analytics",
            "Reporte por Período": "calendar",
            "Reporte Global": "report",
            "Niveles de Mando": "analytics",
        }
        return icon_map.get(title, "report")

4. En el método _on_theme_changed(), asegúrate de llamar set_theme() en las tarjetas:

    def _on_theme_changed(self, new_theme: str):
        # ... código existente ...

        for card in self.report_cards:
            card.set_theme(new_theme)

¡Y eso es todo! Las tarjetas ahora tendrán el diseño de GitHub Actions.
"""


if __name__ == "__main__":
    # Ejecutar ejemplo sin theme_manager
    ejemplo_sin_theme_manager()

    # Para ejecutar con theme_manager, descomenta:
    # ejemplo_con_theme_manager()
