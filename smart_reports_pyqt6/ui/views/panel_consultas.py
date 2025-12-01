"""
Panel de Consultas SQL
PyQt6 Version - Consultas a la base de datos
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QComboBox,
    QFrame, QScrollArea, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConsultasPanel(QWidget):
    """Panel de Consultas SQL"""

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("🔍 Consultas SQL")
        title.setFont(QFont("Montserrat", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        execute_btn = QPushButton("▶️ Ejecutar")
        execute_btn.setFixedHeight(40)
        execute_btn.setFixedWidth(150)
        execute_btn.clicked.connect(self._execute_query)
        header_layout.addWidget(execute_btn)

        clear_btn = QPushButton("🗑️ Limpiar")
        clear_btn.setProperty("class", "secondary")
        clear_btn.setFixedHeight(40)
        clear_btn.setFixedWidth(120)
        clear_btn.clicked.connect(self._clear_query)
        header_layout.addWidget(clear_btn)

        layout.addLayout(header_layout)

        # Tabs
        tabs = QTabWidget()

        # Tab 1: Consulta personalizada
        custom_tab = self._create_custom_query_tab()
        tabs.addTab(custom_tab, "📝 Consulta Personalizada")

        # Tab 2: Consultas predefinidas
        predefined_tab = self._create_predefined_queries_tab()
        tabs.addTab(predefined_tab, "⚡ Consultas Rápidas")

        # Tab 3: Historial
        history_tab = self._create_history_tab()
        tabs.addTab(history_tab, "📚 Historial")

        layout.addWidget(tabs)

    def _create_custom_query_tab(self):
        """Tab de consulta personalizada"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Editor de SQL
        sql_label = QLabel("Query SQL:")
        sql_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        layout.addWidget(sql_label)

        self.sql_editor = QTextEdit()
        self.sql_editor.setPlaceholderText("SELECT * FROM tabla WHERE ...")
        self.sql_editor.setMinimumHeight(150)
        self.sql_editor.setFont(QFont("Courier New", 10))
        layout.addWidget(self.sql_editor)

        # Botones de ayuda
        help_layout = QHBoxLayout()

        help_btn = QPushButton("❓ Ayuda SQL")
        help_btn.setProperty("class", "secondary")
        help_btn.clicked.connect(self._show_sql_help)
        help_layout.addWidget(help_btn)

        tables_btn = QPushButton("📋 Ver Tablas")
        tables_btn.setProperty("class", "secondary")
        tables_btn.clicked.connect(self._show_tables)
        help_layout.addWidget(tables_btn)

        help_layout.addStretch()

        layout.addLayout(help_layout)

        # Resultados
        results_label = QLabel("Resultados:")
        results_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        layout.addWidget(results_label)

        self.results_table = QTableWidget(0, 0)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setMinimumHeight(300)
        layout.addWidget(self.results_table)

        # Info de resultados
        self.results_info = QLabel("No hay resultados")
        self.results_info.setStyleSheet("color: #888888;")
        layout.addWidget(self.results_info)

        return widget

    def _create_predefined_queries_tab(self):
        """Tab de consultas predefinidas"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Selector de consulta
        query_label = QLabel("Selecciona una consulta:")
        query_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        layout.addWidget(query_label)

        self.query_combo = QComboBox()
        self.query_combo.addItems([
            "-- Selecciona una consulta --",
            "Usuarios por unidad de negocio",
            "Progreso de módulos",
            "Reportes generados últimos 7 días",
            "Top 10 usuarios más activos",
            "Unidades con menor avance",
            "Consultas más ejecutadas",
            "Estadísticas generales"
        ])
        self.query_combo.currentIndexChanged.connect(self._load_predefined_query)
        layout.addWidget(self.query_combo)

        # Descripción
        self.query_description = QLabel("Selecciona una consulta para ver su descripción")
        self.query_description.setWordWrap(True)
        self.query_description.setStyleSheet("color: #888888; padding: 10px; background-color: rgba(0,0,0,0.1); border-radius: 5px;")
        layout.addWidget(self.query_description)

        # Preview del SQL
        preview_label = QLabel("Vista previa SQL:")
        preview_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        layout.addWidget(preview_label)

        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        self.query_preview.setMinimumHeight(100)
        self.query_preview.setFont(QFont("Courier New", 9))
        layout.addWidget(self.query_preview)

        # Tabla de resultados predefinidos
        self.predefined_results_table = QTableWidget(0, 0)
        self.predefined_results_table.setAlternatingRowColors(True)
        self.predefined_results_table.setMinimumHeight(200)
        layout.addWidget(self.predefined_results_table)

        layout.addStretch()

        return widget

    def _create_history_tab(self):
        """Tab de historial de consultas"""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Tabla de historial
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["Fecha", "Consulta", "Resultados", "Acciones"])
        self.history_table.setAlternatingRowColors(True)
        layout.addWidget(self.history_table)

        # Cargar historial dummy
        self._load_history_dummy()

        # Botones
        buttons_layout = QHBoxLayout()

        clear_history_btn = QPushButton("🗑️ Limpiar Historial")
        clear_history_btn.setProperty("class", "danger")
        clear_history_btn.clicked.connect(self._clear_history)
        buttons_layout.addWidget(clear_history_btn)

        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        return widget

    def _execute_query(self):
        """Ejecutar consulta SQL"""

        query = self.sql_editor.toPlainText().strip()

        if not query:
            QMessageBox.warning(self, "Query vacía", "Por favor ingresa una consulta SQL")
            return

        print(f"🔍 Ejecutando query: {query[:100]}...")

        # TODO: Ejecutar query real en la base de datos
        # Por ahora, datos dummy
        self._load_dummy_results()

    def _load_dummy_results(self):
        """Cargar resultados dummy"""

        # Datos de ejemplo
        headers = ["ID", "Nombre", "Unidad", "Módulo", "Progreso", "Fecha"]
        data = [
            ["1", "Juan Pérez", "ICAVE", "Módulo 1", "95%", "2024-01-15"],
            ["2", "María García", "TNG", "Módulo 2", "88%", "2024-01-16"],
            ["3", "Carlos López", "ECV", "Módulo 1", "92%", "2024-01-17"],
            ["4", "Ana Martínez", "HPMX", "Módulo 3", "78%", "2024-01-18"],
            ["5", "Luis Rodríguez", "Container", "Módulo 2", "85%", "2024-01-19"],
        ]

        # Configurar tabla
        self.results_table.setRowCount(len(data))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        # Llenar datos
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.results_table.setItem(row, col, item)

        # Ajustar columnas
        self.results_table.resizeColumnsToContents()

        # Info
        self.results_info.setText(f"✅ {len(data)} registros encontrados")

    def _clear_query(self):
        """Limpiar editor"""
        self.sql_editor.clear()
        self.results_table.setRowCount(0)
        self.results_info.setText("No hay resultados")

    def _show_sql_help(self):
        """Mostrar ayuda de SQL"""
        QMessageBox.information(
            self,
            "Ayuda SQL",
            """
<b>Sintaxis básica SQL:</b><br><br>

<b>SELECT:</b> Seleccionar columnas<br>
SELECT columna1, columna2 FROM tabla;<br><br>

<b>WHERE:</b> Filtrar filas<br>
SELECT * FROM tabla WHERE condicion;<br><br>

<b>ORDER BY:</b> Ordenar resultados<br>
SELECT * FROM tabla ORDER BY columna ASC;<br><br>

<b>LIMIT:</b> Limitar resultados<br>
SELECT * FROM tabla LIMIT 10;
            """
        )

    def _show_tables(self):
        """Mostrar tablas disponibles"""
        QMessageBox.information(
            self,
            "Tablas Disponibles",
            """
<b>Tablas del sistema:</b><br><br>

• usuarios<br>
• unidades_negocio<br>
• modulos<br>
• progreso<br>
• reportes<br>
• consultas<br>
• tickets<br>
• logs
            """
        )

    def _load_predefined_query(self, index):
        """Cargar consulta predefinida"""

        queries = {
            1: {
                'desc': 'Obtiene el conteo de usuarios por cada unidad de negocio',
                'sql': 'SELECT unidad, COUNT(*) as total\nFROM usuarios\nGROUP BY unidad\nORDER BY total DESC;'
            },
            2: {
                'desc': 'Muestra el progreso promedio de todos los módulos',
                'sql': 'SELECT modulo, AVG(progreso) as promedio\nFROM progreso\nGROUP BY modulo;'
            },
            3: {
                'desc': 'Reportes generados en los últimos 7 días',
                'sql': 'SELECT *\nFROM reportes\nWHERE fecha >= DATE_SUB(NOW(), INTERVAL 7 DAY);'
            }
        }

        if index in queries:
            q = queries[index]
            self.query_description.setText(q['desc'])
            self.query_preview.setText(q['sql'])
        else:
            self.query_description.setText("Selecciona una consulta para ver su descripción")
            self.query_preview.clear()

    def _load_history_dummy(self):
        """Cargar historial dummy"""

        history = [
            ["2024-01-20 10:30", "SELECT * FROM usuarios...", "152 registros", "Ver"],
            ["2024-01-20 09:15", "SELECT unidad, COUNT(*)...", "11 registros", "Ver"],
            ["2024-01-19 16:45", "SELECT * FROM reportes...", "89 registros", "Ver"],
        ]

        self.history_table.setRowCount(len(history))

        for row, row_data in enumerate(history):
            for col, value in enumerate(row_data):
                if col == 3:  # Botón de acción
                    btn = QPushButton("📄 " + value)
                    btn.setProperty("class", "secondary")
                    self.history_table.setCellWidget(row, col, btn)
                else:
                    item = QTableWidgetItem(value)
                    self.history_table.setItem(row, col, item)

        self.history_table.resizeColumnsToContents()

    def _clear_history(self):
        """Limpiar historial"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Seguro que deseas limpiar todo el historial?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.history_table.setRowCount(0)
            QMessageBox.information(self, "Éxito", "Historial limpiado")
