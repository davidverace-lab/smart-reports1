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

    def __init__(self, title: str, value: str, icon: str = "", theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(100)

        # Estilo con borde navy
        is_dark = theme_manager.is_dark_mode() if theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#003087"
        text_color = "#ffffff" if is_dark else "#003087"
        value_color = "#ffffff" if is_dark else "#003087"

        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {text_color};")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        layout.addStretch()

        # Valor
        value_label = QLabel(value)
        value_label.setFont(QFont("Montserrat", 22, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {value_color};")
        value_label.setWordWrap(True)
        layout.addWidget(value_label)


class ChartCard(QFrame):
    """Tarjeta con gráfico D3.js y menú de opciones"""

    def __init__(self, title: str, chart_type: str, data: dict, theme: str = 'dark', theme_manager=None, parent=None):
        super().__init__(parent)

        self.title = title
        self.chart_type = chart_type
        self.data = data
        self.theme = theme
        self.theme_manager = theme_manager

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(450)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header con título y botones de acción
        header = QWidget()
        header.setFixedHeight(45)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        # Título del gráfico
        title_label = QLabel(title)
        title_label.setFont(QFont("Montserrat", 13, QFont.Weight.Bold))
        is_dark = theme_manager.is_dark_mode() if theme_manager else (theme == 'dark')
        title_color = "#ffffff" if is_dark else "#003087"
        title_label.setStyleSheet(f"color: {title_color};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Botón de expandir (FUERA del menú)
        expand_btn = QPushButton("⤢")
        expand_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        expand_btn.setFixedSize(35, 35)
        expand_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background-color: #004ba0;
            }}
        """)
        expand_btn.setToolTip("Expandir a pantalla completa")
        expand_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        expand_btn.clicked.connect(self._toggle_fullscreen)
        header_layout.addWidget(expand_btn)

        # Botón de menú (3 puntos)
        menu_btn = QPushButton("⋮")
        menu_btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        menu_btn.setFixedSize(35, 35)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #003087;
                color: white;
                border: none;
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background-color: #004ba0;
            }}
        """)
        menu_btn.setToolTip("Más opciones")
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.clicked.connect(self._show_menu)
        header_layout.addWidget(menu_btn)

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
        """Expandir gráfico a pantalla completa (sin modal)"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout

        # Crear diálogo fullscreen
        dialog = QDialog(self.window())
        dialog.setWindowTitle(self.title)
        dialog.showMaximized()

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # Crear nuevo widget de gráfico
        chart = D3ChartWidget(dialog)
        chart.set_chart(self.chart_type, self.title, self.data, tema=self.theme)
        layout.addWidget(chart)

        # Botón para cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(40)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec()

    def _export_chart(self, format: str):
        """Exportar gráfico"""
        print(f"📊 Exportando gráfico '{self.title}' como {format.upper()}...")
        # TODO: Implementar exportación real

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
        title_label.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
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
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        import os

        # Solicitar ubicación de guardado
        filename, _ = QFileDialog.getSaveFileName(
            self.window(),
            "Guardar PDF",
            f"{self.title}.pdf",
            "PDF Files (*.pdf)"
        )

        if not filename:
            return  # Usuario canceló

        try:
            # Importar generador de PDF
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
            from smart_reports.utils.visualization.pdf_generator import PDFReportGenerator

            # Crear generador
            pdf_gen = PDFReportGenerator()

            # Preparar datos para tabla
            data_table = [["Categoría", "Valor"]]
            if 'labels' in self.data and 'values' in self.data:
                for label, value in zip(self.data['labels'], self.data['values']):
                    data_table.append([str(label), str(value)])

            # Información adicional
            additional_info = {
                "Tipo de Gráfico": self.chart_type.capitalize(),
                "Total de Registros": len(self.data.get('labels', [])),
            }

            # Por ahora sin figura matplotlib (solo tabla)
            # TODO: Convertir gráfico D3 a matplotlib o imagen
            pdf_gen.create_dashboard_pdf(
                filename=filename,
                dashboard_title=self.title,
                figure=None,
                data_table=data_table,
                additional_info=additional_info
            )

            QMessageBox.information(
                self.window(),
                "PDF Generado",
                f"El PDF se ha guardado correctamente en:\n{filename}"
            )

        except ImportError as e:
            QMessageBox.warning(
                self.window(),
                "Librería Faltante",
                f"No se pudo generar el PDF. Falta instalar ReportLab:\n\npip install reportlab\n\nError: {e}"
            )
        except Exception as e:
            QMessageBox.critical(
                self.window(),
                "Error",
                f"Error al generar PDF:\n{e}"
            )

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
        from PyQt6.QtGui import QPixmap, QImage
        from PyQt6.QtCore import QBuffer, QIODevice

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


class DashboardPanel(QWidget):
    """Panel de Dashboard - Control Ejecutivo"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.chart_cards = []  # Almacenar referencias a los gráficos
        self.metric_cards = []  # Almacenar referencias a las métricas

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

        title = QLabel("Panel de Control Ejecutivo")
        title.setFont(QFont("Montserrat", 26, QFont.Weight.Bold))
        # Color según tema
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        title_color = "#ffffff" if is_dark else "#003087"
        title.setStyleSheet(f"color: {title_color};")
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = QPushButton("Actualizar")
        refresh_btn.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        refresh_btn.setFixedHeight(40)
        refresh_btn.setFixedWidth(140)
        refresh_btn.setStyleSheet("""
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
        refresh_btn.clicked.connect(self._refresh_data)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(refresh_btn)

        main_layout.addLayout(header_layout)

        # Métricas principales (3 métricas)
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)

        # Métrica 1: Total de Usuarios
        card1 = MetricCard("Total de Usuarios", "1,525", "", self.theme_manager)
        self.metric_cards.append(card1)
        metrics_layout.addWidget(card1)

        # Métrica 2: Módulo Actual
        card2 = MetricCard("Módulo Actual", "Módulo 9: Evaluación Final", "", self.theme_manager)
        self.metric_cards.append(card2)
        metrics_layout.addWidget(card2)

        # Métrica 3: Progreso General
        card3 = MetricCard("Progreso General del Instituto", "78%", "", self.theme_manager)
        self.metric_cards.append(card3)
        metrics_layout.addWidget(card3)

        main_layout.addLayout(metrics_layout)

        # Gráficos en grid
        tema = self.theme_manager.current_theme if self.theme_manager else 'dark'

        # Primera fila de gráficos
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)

        chart1 = ChartCard("Usuarios por Unidad", "bar", USUARIOS_POR_UNIDAD_DATA, tema, self.theme_manager)
        chart2 = ChartCard("Progreso por Unidades", "donut", PROGRESO_UNIDADES_DATA, tema, self.theme_manager)
        self.chart_cards.extend([chart1, chart2])

        row1_layout.addWidget(chart1)
        row1_layout.addWidget(chart2)

        main_layout.addLayout(row1_layout)

        # Segunda fila de gráficos
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(20)

        chart3 = ChartCard("Tendencia Semanal", "line", TENDENCIA_SEMANAL_DATA, tema, self.theme_manager)
        chart4 = ChartCard("Top 5 Unidades", "bar", TOP_5_UNIDADES_DATA, tema, self.theme_manager)
        self.chart_cards.extend([chart3, chart4])

        row2_layout.addWidget(chart3)
        row2_layout.addWidget(chart4)

        main_layout.addLayout(row2_layout)

        # Tercera fila de gráficos
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(20)

        chart5 = ChartCard("Cumplimiento de Objetivos", "donut", CUMPLIMIENTO_OBJETIVOS_DATA, tema, self.theme_manager)
        chart6 = ChartCard("Módulos con Menor Avance", "bar", MODULOS_MENOR_AVANCE_DATA, tema, self.theme_manager)
        self.chart_cards.extend([chart5, chart6])

        row3_layout.addWidget(chart5)
        row3_layout.addWidget(chart6)

        main_layout.addLayout(row3_layout)

        # Spacer al final
        main_layout.addStretch()

    def _refresh_data(self):
        """Actualizar datos del dashboard"""
        print("🔄 Actualizando dashboard...")
        # TODO: Implementar recarga de datos desde BD

    def _on_theme_changed(self, new_theme: str):
        """Callback cuando cambia el tema"""
        print(f"🎨 Dashboard: Actualizando tema a {new_theme}")

        # Actualizar todos los gráficos
        for chart_card in self.chart_cards:
            chart_card.update_theme(new_theme)

        # Actualizar todas las métricas
        for metric_card in self.metric_cards:
            metric_card.update_theme(new_theme)

        # Recargar el panel completo (más simple)
        # Esto recargará todo el UI con los colores correctos
        self._reload_ui()

    def _reload_ui(self):
        """Recargar UI completo con nuevo tema"""
        # Limpiar layout actual
        layout = self.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Limpiar referencias
        self.chart_cards.clear()
        self.metric_cards.clear()

        # Recrear UI
        self._create_ui()
