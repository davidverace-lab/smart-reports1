"""
Panel de Dashboard - Control Ejecutivo
PyQt6 Version - Replicando diseño de CustomTkinter
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from smart_reports_pyqt6.ui.widgets.pyqt6_d3_chart_widget import D3ChartWidget


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


class ExpandedChartView(QWidget):
    """Vista expandida de gráfico (flujo tipo app móvil)"""

    back_clicked = pyqtSignal()

    def __init__(self, chart_type: str, title: str, data: dict, theme: str = 'dark', theme_manager=None, parent=None):
        super().__init__(parent)

        self.chart_type = chart_type
        self.title = title
        self.data = data
        self.theme = theme
        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de vista expandida con header compacto"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Header compacto con todos los controles en una sola fila
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(10)

        # Botón de retorno
        back_btn = QPushButton("←")
        back_btn.setFixedSize(50, 45)
        back_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Arial';
                font-size: 22px;
                font-weight: bold;
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        back_btn.setToolTip("Volver al dashboard")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_btn)

        # Título del gráfico
        title_label = QLabel(self.title)
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else (self.theme == 'dark')
        title_color = "#ffffff" if is_dark else "#003087"
        title_label.setStyleSheet(f"""
            font-family: 'Montserrat';
            font-size: 20px;
            font-weight: bold;
            color: {title_color};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Botón de menú con opciones
        menu_btn = QPushButton("⋯")
        menu_btn.setFixedSize(50, 45)
        menu_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Arial';
                font-size: 26px;
                font-weight: bold;
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        menu_btn.setToolTip("Opciones del gráfico")
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.clicked.connect(self._show_menu)
        header_layout.addWidget(menu_btn)

        layout.addWidget(header)

        # Gráfico grande (ocupa todo el espacio restante)
        self.chart_widget = D3ChartWidget(self)
        self.chart_widget.set_chart(self.chart_type, "", self.data, tema=self.theme)
        layout.addWidget(self.chart_widget)

    def _show_menu(self):
        """Mostrar menú de opciones"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction

        menu = QMenu(self)

        # Opciones similares al ChartCard
        table_action = QAction("Mostrar en Tabla", self)
        table_action.triggered.connect(self._show_data_table)
        menu.addAction(table_action)

        copy_data_action = QAction("Copiar Datos al Portapapeles", self)
        copy_data_action.triggered.connect(self._copy_data_to_clipboard)
        menu.addAction(copy_data_action)

        menu.addSeparator()

        export_pdf_action = QAction("Exportar como PDF", self)
        export_pdf_action.triggered.connect(self._export_as_pdf)
        menu.addAction(export_pdf_action)

        export_png_action = QAction("Exportar como PNG", self)
        export_png_action.triggered.connect(lambda: self._export_chart("png"))
        menu.addAction(export_png_action)

        copy_png_action = QAction("Copiar PNG al Portapapeles", self)
        copy_png_action.triggered.connect(self._copy_png_to_clipboard)
        menu.addAction(copy_png_action)

        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

    def _show_data_table(self):
        """Mostrar datos en tabla"""
        print(f"📊 Mostrando tabla de datos para '{self.title}'")

    def _copy_data_to_clipboard(self):
        """Copiar datos al portapapeles"""
        print(f"📋 Copiando datos de '{self.title}'")

    def _export_as_pdf(self):
        """Exportar como PDF"""
        print(f"📄 Exportando '{self.title}' como PDF")

    def _export_chart(self, format: str):
        """Exportar gráfico"""
        print(f"💾 Exportando '{self.title}' como {format.upper()}")

    def _copy_png_to_clipboard(self):
        """Copiar PNG al portapapeles"""
        print(f"🖼️ Copiando imagen de '{self.title}'")


class MetricCard(QFrame):
    """Tarjeta de métrica - Cuadrada y centrada"""

    def __init__(self, title: str, value: str, subtitle: str = "", icon: str = "", theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.title_text = title
        self.value_text = value
        self.subtitle_text = subtitle
        self.icon_text = icon

        self.setFrameShape(QFrame.Shape.StyledPanel)
        # MÁS CUADRADO: tamaño similar en alto y ancho
        self.setMinimumHeight(220)
        self.setMinimumWidth(220)
        self.setMaximumWidth(280)

        self._create_ui()
        self._update_theme()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(lambda: self._update_theme())

    def _create_ui(self):
        """Crear interfaz de la tarjeta - TODO CENTRADO"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # CENTRAR TODO

        # Ícono (si existe) - CENTRADO
        if self.icon_text:
            self.icon_label = QLabel(self.icon_text)
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.icon_label.setStyleSheet("""
                font-family: 'Segoe UI Emoji';
                font-size: 40px;
                border: none;
                background: transparent;
            """)
            layout.addWidget(self.icon_label)

        # Valor - CENTRADO Y MÁS GRANDE
        self.value_label = QLabel(self.value_text)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 36px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        self.value_label.setWordWrap(True)
        layout.addWidget(self.value_label)

        # Título - CENTRADO
        self.title_label = QLabel(self.title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 14px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        # Subtítulo (si existe) - CENTRADO
        if self.subtitle_text:
            self.subtitle_label = QLabel(self.subtitle_text)
            self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.subtitle_label.setStyleSheet("""
                font-family: 'Montserrat';
                font-size: 11px;
                font-weight: normal;
                border: none;
                background: transparent;
            """)
            self.subtitle_label.setWordWrap(True)
            layout.addWidget(self.subtitle_label)

    def _update_theme(self):
        """Actualizar colores según tema"""
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#003087"
        text_color = "#ffffff" if is_dark else "#003087"

        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {bg_color};
                border: 3px solid {border_color};
                border-radius: 12px;
            }}
        """)

        # Actualizar colores de los labels
        if hasattr(self, 'icon_label'):
            self.icon_label.setStyleSheet(f"""
                font-family: 'Segoe UI Emoji';
                font-size: 40px;
                color: {text_color};
                border: none;
                background: transparent;
            """)

        if hasattr(self, 'value_label'):
            self.value_label.setStyleSheet(f"""
                font-family: 'Montserrat';
                font-size: 36px;
                font-weight: bold;
                color: {text_color};
                border: none;
                background: transparent;
            """)

        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"""
                font-family: 'Montserrat';
                font-size: 14px;
                font-weight: bold;
                color: {text_color};
                border: none;
                background: transparent;
            """)

        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"""
                font-family: 'Montserrat';
                font-size: 11px;
                font-weight: normal;
                color: {text_color};
                border: none;
                background: transparent;
            """)


class ChartCard(QFrame):
    """Tarjeta con gráfico D3.js y menú de opciones"""

    def __init__(self, title: str, chart_type: str, data: dict, theme: str = 'dark', theme_manager=None, parent=None):
        super().__init__(parent)

        self.title = title
        self.chart_type = chart_type
        self.data = data
        self.theme = theme
        self.theme_manager = theme_manager

        self.setFrameShape(QFrame.Shape.StyledPanel)
        # ALTURA AUMENTADA para ver gráficas completas
        self.setMinimumHeight(480)
        self.setSizePolicy(QWidget().sizePolicy().Policy.Expanding, QWidget().sizePolicy().Policy.Expanding)

        # Aplicar estilo con borde
        self._apply_card_style()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header con título y botones de acción
        header = QWidget()
        header.setFixedHeight(40)
        header.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 3, 12, 3)

        # Título del gráfico
        self.title_label = QLabel(title)
        is_dark = theme_manager.is_dark_mode() if theme_manager else (theme == 'dark')
        title_color = "#ffffff" if is_dark else "#003087"
        self.title_label.setStyleSheet(f"""
            font-family: 'Montserrat';
            font-size: 14px;
            font-weight: bold;
            color: {title_color};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Botón de expandir (FUERA del menú) con icono de flecha
        self.expand_btn = QPushButton("↗")
        self.expand_btn.setFixedSize(38, 38)
        self.expand_btn.setToolTip("Expandir gráfico")
        self.expand_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.expand_btn.clicked.connect(self._toggle_fullscreen)
        header_layout.addWidget(self.expand_btn)

        # Botón de menú (3 puntos) con icono mejorado
        self.menu_btn = QPushButton("⋯")
        self.menu_btn.setFixedSize(38, 38)
        self.menu_btn.setToolTip("Opciones del gráfico")
        self.menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_btn.clicked.connect(self._show_menu)
        header_layout.addWidget(self.menu_btn)

        # Aplicar estilos iniciales a botones
        self._update_button_styles()

        layout.addWidget(header)

        # Gráfico
        self.chart_widget = D3ChartWidget(self)
        self.chart_widget.set_chart(chart_type, title, data, tema=theme)
        layout.addWidget(self.chart_widget)

    def _show_menu(self):
        """Mostrar menú de opciones"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction

        menu = QMenu(self)

        # Acción: Mostrar en Tabla
        table_action = QAction("Mostrar en Tabla", self)
        table_action.triggered.connect(self._show_data_table)
        menu.addAction(table_action)

        # Acción: Copiar Datos al Portapapeles
        copy_data_action = QAction("Copiar Datos al Portapapeles", self)
        copy_data_action.triggered.connect(self._copy_data_to_clipboard)
        menu.addAction(copy_data_action)

        menu.addSeparator()

        # Acción: Exportar PDF
        export_pdf_action = QAction("Exportar como PDF", self)
        export_pdf_action.triggered.connect(self._export_as_pdf)
        menu.addAction(export_pdf_action)

        # Acción: Exportar PNG
        export_png_action = QAction("Exportar como PNG", self)
        export_png_action.triggered.connect(lambda: self._export_chart("png"))
        menu.addAction(export_png_action)

        # Acción: Copiar PNG al Portapapeles
        copy_png_action = QAction("Copiar PNG al Portapapeles", self)
        copy_png_action.triggered.connect(self._copy_png_to_clipboard)
        menu.addAction(copy_png_action)

        # Acción: Exportar SVG
        export_svg_action = QAction("Exportar como SVG", self)
        export_svg_action.triggered.connect(lambda: self._export_chart("svg"))
        menu.addAction(export_svg_action)

        menu.addSeparator()

        # Acción: Actualizar
        refresh_action = QAction("Actualizar", self)
        refresh_action.triggered.connect(self._refresh_chart)
        menu.addAction(refresh_action)

        # Mostrar menú
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

    def _toggle_fullscreen(self):
        """Expandir gráfico en nueva vista (flujo de app móvil)"""
        # Obtener referencia a la ventana principal
        main_window = self.window()

        # Verificar si tiene panel_stack (está en MainWindow)
        if not hasattr(main_window, 'panel_stack'):
            # Fallback a modal si no está en contexto correcto
            self._show_modal_fullscreen()
            return

        # Crear vista expandida
        expanded_view = ExpandedChartView(
            chart_type=self.chart_type,
            title=self.title,
            data=self.data,
            theme=self.theme,
            theme_manager=self.theme_manager,
            parent=main_window
        )

        # Conectar botón de retorno
        expanded_view.back_clicked.connect(lambda: self._close_expanded_view(main_window, expanded_view))

        # Agregar al stack
        main_window.panel_stack.addWidget(expanded_view)
        main_window.panel_stack.setCurrentWidget(expanded_view)

    def _close_expanded_view(self, main_window, expanded_view):
        """Cerrar vista expandida y volver al dashboard"""
        # Volver al dashboard
        if hasattr(main_window, 'panels') and 'dashboard' in main_window.panels:
            main_window.panel_stack.setCurrentWidget(main_window.panels['dashboard'])

        # Remover widget del stack
        main_window.panel_stack.removeWidget(expanded_view)
        expanded_view.deleteLater()

    def _show_modal_fullscreen(self):
        """Mostrar gráfico en modal (fallback)"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout

        dialog = QDialog(self.window())
        dialog.setWindowTitle(self.title)
        dialog.showMaximized()

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        chart = D3ChartWidget(dialog)
        chart.set_chart(self.chart_type, self.title, self.data, tema=self.theme)
        layout.addWidget(chart)

        close_btn = QPushButton("← Cerrar")
        close_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Montserrat';
                font-size: 12px;
                font-weight: bold;
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        close_btn.setFixedHeight(45)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec()

    def _export_chart(self, format: str):
        """Exportar gráfico"""
        print(f"📊 Exportando gráfico '{self.title}' como {format.upper()}...")

    def _refresh_chart(self):
        """Actualizar gráfico"""
        print(f"🔄 Actualizando gráfico '{self.title}'...")
        self.chart_widget.set_chart(self.chart_type, self.title, self.data, tema=self.theme)

    def _show_data_table(self):
        """Mostrar datos del gráfico en tabla"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

        # Crear diálogo
        dialog = QDialog(self.window())
        dialog.setWindowTitle(f"Datos: {self.title}")
        dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title_label = QLabel(f"Datos de '{self.title}'")
        title_label.setStyleSheet("""
            font-family: 'Montserrat';
            font-size: 14px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)
        layout.addWidget(title_label)

        # Crear tabla
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Categoría", "Valor"])

        # Poblar tabla con datos
        if 'labels' in self.data and 'values' in self.data:
            table.setRowCount(len(self.data['labels']))
            for i, (label, value) in enumerate(zip(self.data['labels'], self.data['values'])):
                table.setItem(i, 0, QTableWidgetItem(str(label)))
                table.setItem(i, 1, QTableWidgetItem(str(value)))

        # Ajustar columnas
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)

        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #004ba0;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec()

    def _export_as_pdf(self):
        """Exportar gráfico como PDF"""
        print(f"📄 Exportando '{self.title}' como PDF")

    def _copy_data_to_clipboard(self):
        """Copiar datos del gráfico al portapapeles"""
        from PyQt6.QtWidgets import QApplication, QMessageBox

        try:
            # Preparar datos en formato CSV
            csv_data = "Categoría,Valor\n"
            if 'labels' in self.data and 'values' in self.data:
                for label, value in zip(self.data['labels'], self.data['values']):
                    csv_data += f"{label},{value}\n"

            # Copiar al portapapeles
            clipboard = QApplication.clipboard()
            clipboard.setText(csv_data)

            QMessageBox.information(
                self.window(),
                "Datos Copiados",
                f"Los datos de '{self.title}' han sido copiados al portapapeles en formato CSV.\n\nPuedes pegarlos en Excel, Google Sheets, etc."
            )

        except Exception as e:
            QMessageBox.critical(
                self.window(),
                "Error",
                f"Error al copiar datos al portapapeles:\n{e}"
            )

    def _copy_png_to_clipboard(self):
        """Copiar imagen PNG del gráfico al portapapeles"""
        from PyQt6.QtWidgets import QApplication, QMessageBox

        try:
            # Capturar el widget del gráfico como imagen
            pixmap = self.chart_widget.grab()

            # Copiar al portapapeles
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)

            QMessageBox.information(
                self.window(),
                "Imagen Copiada",
                f"La imagen del gráfico '{self.title}' ha sido copiada al portapapeles.\n\nPuedes pegarla en Word, PowerPoint, Paint, etc."
            )

        except Exception as e:
            QMessageBox.critical(
                self.window(),
                "Error",
                f"Error al copiar imagen al portapapeles:\n{e}"
            )

    def _apply_card_style(self):
        """Aplicar estilo de borde a la tarjeta"""
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else (self.theme == 'dark')
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#003087"

        self.setStyleSheet(f"""
            ChartCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """)

    def _update_button_styles(self):
        """Actualizar estilos de los botones según el tema"""
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else (self.theme == 'dark')

        # Colores adaptados al tema
        if is_dark:
            btn_bg = "#00B5E2"  # Cyan brillante para modo oscuro
            btn_hover = "#009BDE"
        else:
            btn_bg = "#003087"  # Navy para modo claro
            btn_hover = "#004ba0"

        # Estilo del botón de expandir
        if hasattr(self, 'expand_btn'):
            self.expand_btn.setStyleSheet(f"""
                QPushButton {{
                    font-family: 'Arial';
                    font-size: 18px;
                    font-weight: bold;
                    background-color: {btn_bg};
                    color: white;
                    border: none;
                    border-radius: 19px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                }}
            """)

        # Estilo del botón de menú
        if hasattr(self, 'menu_btn'):
            self.menu_btn.setStyleSheet(f"""
                QPushButton {{
                    font-family: 'Arial';
                    font-size: 22px;
                    font-weight: bold;
                    background-color: {btn_bg};
                    color: white;
                    border: none;
                    border-radius: 19px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                }}
            """)

    def update_theme_colors(self):
        """Actualizar colores del tema"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        title_color = "#ffffff" if is_dark else "#003087"

        # Actualizar estilo de la tarjeta
        self._apply_card_style()

        # Actualizar estilos de los botones
        self._update_button_styles()

        # Actualizar color del título
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"""
                font-family: 'Montserrat';
                font-size: 14px;
                font-weight: bold;
                color: {title_color};
                background: transparent;
                border: none;
            """)


class DashboardPanel(QWidget):
    """Panel de Dashboard - Control Ejecutivo (Sin Tabs, replicando CustomTkinter)"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.chart_cards = []
        self.metric_cards = []

        self.setStyleSheet("background: transparent; border: none;")

        # Crear UI
        self._create_ui()

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

    def _create_ui(self):
        """Crear interfaz"""

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("border: none; background: transparent;")

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent; border: none;")
        scroll.setWidget(scroll_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

        main_layout = QVBoxLayout(scroll_widget)
        # SIN MÁRGENES GRISES
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Métricas principales (3 métricas en fila) - CENTRADAS
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        metrics_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Métrica 1: Total de Usuarios
        card1 = MetricCard(
            "Total de Usuarios",
            "1,525",
            "Usuarios activos en el sistema",
            "👥",
            self.theme_manager
        )
        self.metric_cards.append(card1)
        metrics_layout.addWidget(card1)

        # Métrica 2: Módulo Actual
        card2 = MetricCard(
            "Módulo Actual",
            "SIGA",
            "Módulo 8 - Procesos de RRHH",
            "📄",
            self.theme_manager
        )
        self.metric_cards.append(card2)
        metrics_layout.addWidget(card2)

        # Métrica 3: Tasa de Completado
        card3 = MetricCard(
            "Tasa de Completado",
            "70.0%",
            "Progreso general del instituto",
            "✓",
            self.theme_manager
        )
        self.metric_cards.append(card3)
        metrics_layout.addWidget(card3)

        main_layout.addLayout(metrics_layout)

        # Gráficos en grid 2x3 (2 COLUMNAS, 3 FILAS para verlas más grandes)
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

        # Grid de gráficos - 2 COLUMNAS
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)
        charts_grid.setContentsMargins(10, 10, 10, 10)

        # FILA 1 (2 gráficas)
        chart1 = ChartCard("📊 Usuarios por Unidad", "horizontal_bar", USUARIOS_POR_UNIDAD_DATA, tema, self.theme_manager)
        chart2 = ChartCard("🍩 Progreso General por Unidad", "donut", PROGRESO_UNIDADES_DATA, tema, self.theme_manager)

        self.chart_cards.extend([chart1, chart2])

        charts_grid.addWidget(chart1, 0, 0)
        charts_grid.addWidget(chart2, 0, 1)

        # FILA 2 (2 gráficas)
        chart3 = ChartCard("📈 Tendencia Semanal", "line", TENDENCIA_SEMANAL_DATA, tema, self.theme_manager)
        chart4 = ChartCard("📊 Top 5 Unidades de Mayor Progreso", "bar", TOP_5_UNIDADES_DATA, tema, self.theme_manager)

        self.chart_cards.extend([chart3, chart4])

        charts_grid.addWidget(chart3, 1, 0)
        charts_grid.addWidget(chart4, 1, 1)

        # FILA 3 (2 gráficas)
        chart5 = ChartCard("🎯 Cumplimiento de Objetivos", "donut", CUMPLIMIENTO_OBJETIVOS_DATA, tema, self.theme_manager)
        chart6 = ChartCard("📉 Módulos con Menor Avance", "horizontal_bar", MODULOS_MENOR_AVANCE_DATA, tema, self.theme_manager)

        self.chart_cards.extend([chart5, chart6])

        charts_grid.addWidget(chart5, 2, 0)
        charts_grid.addWidget(chart6, 2, 1)

        main_layout.addLayout(charts_grid)

        # Spacer al final
        main_layout.addStretch()

    def _on_theme_changed(self, new_theme: str):
        """Callback cuando cambia el tema - SIN REINICIALIZAR GRÁFICAS"""
        print(f"🎨 Dashboard: Actualizando tema a {new_theme}")

        # Actualizar tema de los gráficos - SOLO ACTUALIZAR COLORES, NO REINICIALIZAR
        for chart_card in self.chart_cards:
            chart_card.theme = new_theme
            # Solo actualizar los colores del contenedor (ChartCard)
            if hasattr(chart_card, 'update_theme_colors'):
                chart_card.update_theme_colors()

            # NO reinicializar las gráficas - solo dejar que el tema cambie automáticamente
            # Las gráficas D3 se adaptan al tema mediante CSS

        # Actualizar métricas
        for metric_card in self.metric_cards:
            if hasattr(metric_card, '_update_theme'):
                metric_card._update_theme()

        # Forzar actualización visual
        self.update()
        self.repaint()
