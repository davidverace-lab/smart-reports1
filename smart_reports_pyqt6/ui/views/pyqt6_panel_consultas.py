"""
Panel de Consultas - PyQt6
Migrado desde CustomTkinter con diseño grid 2x2
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QFrame,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SearchSectionCard(QFrame):
    """Tarjeta de sección de búsqueda"""

    def __init__(self, title: str, icon: str, theme_manager=None, parent=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # Aplicar tema
        self._apply_theme()

        # Layout principal - SIN MÁRGENES GRISES
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título - MÁS GRANDE y sin borde - CENTRADO
        title_label = QLabel(f"{title}")
        title_label.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        is_dark = theme_manager.is_dark_mode() if theme_manager else False
        text_color = "#ffffff" if is_dark else "#002E6D"
        title_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none; padding: 0; margin: 0;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        self.layout.addWidget(title_label)

    def _apply_theme(self):
        """Aplicar tema a la tarjeta y sus hijos"""
        if not self.theme_manager:
            return

        is_dark = self.theme_manager.is_dark_mode()
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        border_color = "#002E6D"  # Navy corporativo
        text_color = "#ffffff" if is_dark else "#002E6D"
        input_bg = "#1e1e1e" if is_dark else "#ffffff"
        input_text = "#ffffff" if is_dark else "#000000"

        # 1. Estilo del contenedor principal
        self.setStyleSheet(f"""
            SearchSectionCard {{
                background-color: {bg_color};
                border: 3px solid {border_color};
                border-radius: 12px;
            }}
        """)

        # 2. Actualizar todos los QLabels hijos
        for label in self.findChildren(QLabel):
            # Preservar propiedades de fuente si es posible, o reestablecer estilos base
            # Asumimos fondo transparente y sin borde para etiquetas
            label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")

        # 3. Actualizar QLineEdits
        for entry in self.findChildren(QLineEdit):
            entry.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {input_bg};
                    color: {input_text};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 8px;
                }}
                QLineEdit:focus {{
                    border: 2px solid #00B5E2;
                }}
            """)

        # 4. Actualizar QComboBoxes
        for combo in self.findChildren(QComboBox):
            combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: {input_bg};
                    color: {input_text};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 8px;
                }}
                QComboBox:hover {{
                    border: 2px solid #00B5E2;
                }}
                QComboBox::drop-down {{
                    border: none;
                }}
                QComboBox QAbstractItemView {{
                    background-color: {input_bg};
                    color: {input_text};
                    selection-background-color: #00B5E2;
                }}
            """)
            
        # 5. Actualizar QPushButtons (Opcional, si queremos cambiar color en dark mode)
        # Por ahora mantenemos el Navy corporativo, pero aseguramos que el texto sea blanco
        # for btn in self.findChildren(QPushButton):
        #     pass


class ConsultasPanel(QWidget):
    """Panel de Consultas con diseño grid 2x2"""

    def __init__(self, parent=None, theme_manager=None, db_connection=None):
        super().__init__(parent)

        self.theme_manager = theme_manager
        self.db_connection = db_connection
        
        # Lista de tarjetas para actualizar tema
        self.cards = []

        # Conectar signal de cambio de tema
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        # Scroll área principal
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)  # SIN MÁRGENES GRISES
        main_layout.setSpacing(10)

        # Header
        self._create_header(main_layout)

        # Grid de búsquedas 2x2
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # Card 1: Buscar por ID (Top-Left)
        card1 = self._create_search_by_id_card()
        self.cards.append(card1)
        grid_layout.addWidget(card1, 0, 0)

        # Card 2: Buscar por Unidad (Top-Right)
        card2 = self._create_search_by_unit_card()
        self.cards.append(card2)
        grid_layout.addWidget(card2, 0, 1)

        # Card 3: Buscar por Nombre (Bottom-Left)
        card3 = self._create_search_by_name_card()
        self.cards.append(card3)
        grid_layout.addWidget(card3, 1, 0)

        # Card 4: Estadísticas (Bottom-Right)
        card4 = self._create_stats_card()
        self.cards.append(card4)
        grid_layout.addWidget(card4, 1, 1)

        main_layout.addLayout(grid_layout)

        # Sección de resultados
        self._create_results_section(main_layout)

    def _create_header(self, layout):
        """Crear header - SIN BORDE ALREDEDOR DEL TÍTULO"""

        # Frame del header - SIN BORDE (solo texto)
        header_frame = QFrame()
        self.header_frame = header_frame
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: none;
            }}
        """)

        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(8)

        # Título - MÁS GRANDE (sin icono de emoji)
        title = QLabel("Panel de Consultas")
        self.title_label = title
        title.setFont(QFont("Montserrat", 34, QFont.Weight.Bold))  # Aumentado de 28 a 34
        title_color = "#ffffff" if is_dark else "#002E6D"
        title.setStyleSheet(f"color: {title_color}; background: transparent; border: none; padding: 0; margin: 0;")
        header_layout.addWidget(title)

        # Subtítulo - MÁS GRANDE
        subtitle = QLabel("Búsquedas y filtros en la base de datos de capacitación")
        self.subtitle_label = subtitle
        subtitle.setFont(QFont("Montserrat", 16))  # Aumentado de 14 a 16
        subtitle_color = "#b0b0b0" if is_dark else "#666666"
        subtitle.setStyleSheet(f"color: {subtitle_color}; background: transparent; border: none;")
        header_layout.addWidget(subtitle)

        layout.addWidget(header_frame)

    def _create_search_by_id_card(self):
        """Card: Buscar por ID"""

        card = SearchSectionCard("Buscar Usuario por ID", "", self.theme_manager)

        # Input frame
        input_layout = QHBoxLayout()

        label = QLabel("ID Usuario:")
        label.setFont(QFont("Montserrat", 14))
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#ffffff" if is_dark else "#002E6D"
        label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        input_layout.addWidget(label)

        self.user_id_entry = QLineEdit()
        self.user_id_entry.setPlaceholderText("Ej: 12345")
        self.user_id_entry.setFont(QFont("Montserrat", 14))
        self.user_id_entry.setFixedHeight(45)
        # Aplicar tema al input
        input_bg = "#1e1e1e" if is_dark else "#ffffff"
        input_text = "#ffffff" if is_dark else "#000000"
        input_border = "#002E6D"
        self.user_id_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {input_bg};
                color: {input_text};
                border: 2px solid {input_border};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border: 2px solid #00B5E2;
            }}
        """)
        input_layout.addWidget(self.user_id_entry, 1)

        search_btn = QPushButton("Buscar")
        search_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        search_btn.setFixedHeight(45)
        search_btn.setFixedWidth(130)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #003D82;
            }
        """)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(self._search_by_id)
        input_layout.addWidget(search_btn)

        card.layout.addLayout(input_layout)
        card.layout.addStretch()

        return card

    def _create_search_by_unit_card(self):
        """Card: Buscar por Unidad"""

        card = SearchSectionCard("Consultar por Unidad de Negocio", "", self.theme_manager)

        # Input frame
        input_layout = QHBoxLayout()

        label = QLabel("Unidad:")
        label.setFont(QFont("Montserrat", 14))
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#ffffff" if is_dark else "#002E6D"
        label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        input_layout.addWidget(label)

        self.unit_combo = QComboBox()
        self.unit_combo.addItems([
            "Selecciona una unidad",
            "ICAVE", "TNG", "ECV", "HPMX", "Container",
            "LCMT", "HPLM", "TILH", "CCI", "TIMSA", "LCT", "EIT"
        ])
        self.unit_combo.setFont(QFont("Montserrat", 14))
        self.unit_combo.setFixedHeight(45)
        # Aplicar tema al combo
        combo_bg = "#1e1e1e" if is_dark else "#ffffff"
        combo_text = "#ffffff" if is_dark else "#000000"
        combo_border = "#002E6D"
        self.unit_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {combo_bg};
                color: {combo_text};
                border: 2px solid {combo_border};
                border-radius: 8px;
                padding: 8px;
            }}
            QComboBox:hover {{
                border: 2px solid #00B5E2;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {combo_bg};
                color: {combo_text};
                selection-background-color: #00B5E2;
            }}
        """)
        input_layout.addWidget(self.unit_combo, 1)

        search_btn = QPushButton("Consultar")
        search_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        search_btn.setFixedHeight(45)
        search_btn.setFixedWidth(130)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #003D82;
            }
        """)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(self._search_by_unit)
        input_layout.addWidget(search_btn)

        card.layout.addLayout(input_layout)
        card.layout.addStretch()

        return card

    def _create_search_by_name_card(self):
        """Card: Buscar por Nombre"""

        card = SearchSectionCard("Buscar por Nombre", "", self.theme_manager)

        # Input frame
        input_layout = QHBoxLayout()

        label = QLabel("Nombre:")
        label.setFont(QFont("Montserrat", 14))
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        text_color = "#ffffff" if is_dark else "#002E6D"
        label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        input_layout.addWidget(label)

        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Ej: Juan Perez")
        self.name_entry.setFont(QFont("Montserrat", 14))
        self.name_entry.setFixedHeight(45)
        # Aplicar tema al input
        input_bg = "#1e1e1e" if is_dark else "#ffffff"
        input_text = "#ffffff" if is_dark else "#000000"
        input_border = "#002E6D"
        self.name_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {input_bg};
                color: {input_text};
                border: 2px solid {input_border};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border: 2px solid #00B5E2;
            }}
        """)
        input_layout.addWidget(self.name_entry, 1)

        search_btn = QPushButton("Buscar")
        search_btn.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        search_btn.setFixedHeight(45)
        search_btn.setFixedWidth(130)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #003D82;
            }
        """)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(self._search_by_name)
        input_layout.addWidget(search_btn)

        card.layout.addLayout(input_layout)
        card.layout.addStretch()

        return card

    def _create_stats_card(self):
        """Card: Estadísticas Globales"""

        card = SearchSectionCard("Estadísticas Globales", "", self.theme_manager)

        # Botón
        search_btn = QPushButton("Ver Estadísticas")
        search_btn.setFont(QFont("Montserrat", 15, QFont.Weight.Bold))
        search_btn.setFixedHeight(55)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #002E6D;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #003D82;
            }
        """)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(self._show_stats)
        card.layout.addWidget(search_btn)

        card.layout.addStretch()

        return card

    def _create_results_section(self, layout):
        """Sección de resultados"""

        # Frame de resultados
        results_frame = QFrame()
        self.results_frame = results_frame
        is_dark = self.theme_manager.is_dark_mode() if self.theme_manager else False
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        results_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 12px;
            }}
        """)

        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(15)

        # Título
        results_title = QLabel("📋 Resultados")
        self.results_title = results_title
        results_title.setFont(QFont("Montserrat", 18, QFont.Weight.Bold))
        text_color = "#ffffff" if is_dark else "#003087"
        results_title.setStyleSheet(f"color: {text_color}; background: transparent;")
        results_layout.addWidget(results_title)

        # Tabla de resultados
        self.results_table = QTableWidget(0, 0)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setMinimumHeight(250)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Aplicar tema a la tabla
        table_bg = "#1e1e1e" if is_dark else "#ffffff"
        table_text = "#ffffff" if is_dark else "#000000"
        table_alt = "#2d2d2d" if is_dark else "#f0f0f0"
        table_header = "#002E6D"
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {table_bg};
                color: {table_text};
                gridline-color: #444444;
                border: 1px solid #002E6D;
                border-radius: 8px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:alternate {{
                background-color: {table_alt};
            }}
            QHeaderView::section {{
                background-color: {table_header};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }}
        """)
        results_layout.addWidget(self.results_table)

        # Info de resultados - ELIMINADO
        # self.results_info = QLabel("No hay resultados. Realiza una búsqueda.")
        # self.results_info.setFont(QFont("Montserrat", 11))
        # info_color = "#888888"
        # self.results_info.setStyleSheet(f"color: {info_color}; background: transparent;")
        # results_layout.addWidget(self.results_info)

        layout.addWidget(results_frame)

    # ==================== MÉTODOS DE BÚSQUEDA ====================

    def _search_by_id(self):
        """Buscar usuario por ID"""
        user_id = self.user_id_entry.text().strip()

        if not user_id:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa un ID de usuario")
            return

        print(f"🔍 Buscando usuario con ID: {user_id}")

        # TODO: Consulta real a BD
        # Por ahora, datos dummy
        self._load_dummy_results(f"Usuario ID: {user_id}")

    def _search_by_unit(self):
        """Buscar por unidad"""
        unit = self.unit_combo.currentText()

        if unit == "Selecciona una unidad":
            QMessageBox.warning(self, "Selección requerida", "Por favor selecciona una unidad")
            return

        print(f"🔍 Buscando usuarios de unidad: {unit}")

        # TODO: Consulta real a BD
        self._load_dummy_results(f"Unidad: {unit}")

    def _search_by_name(self):
        """Buscar usuarios por nombre"""
        name = self.name_entry.text().strip()

        if not name:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa un nombre")
            return

        print(f"🔍 Buscando usuarios con nombre: {name}")
        self._load_dummy_results(f"Nombre: {name}")

    def _show_stats(self):
        """Mostrar estadísticas"""
        print("📊 Mostrando estadísticas globales")

        # TODO: Consulta real a BD
        self._load_dummy_results("Estadísticas Globales")

    def _load_dummy_results(self, query_type: str):
        """Cargar resultados dummy"""

        # Datos de ejemplo
        headers = ["ID", "Nombre", "Unidad", "Email", "Progreso", "Último Acceso"]
        data = [
            ["1001", "Juan Pérez", "ICAVE", "juan.perez@hp.com", "95%", "2025-01-15"],
            ["1002", "María García", "TNG", "maria.garcia@hp.com", "88%", "2025-01-16"],
            ["1003", "Carlos López", "ECV", "carlos.lopez@hp.com", "92%", "2025-01-17"],
            ["1004", "Ana Martínez", "HPMX", "ana.martinez@hp.com", "78%", "2025-01-18"],
            ["1005", "Luis Rodríguez", "Container", "luis.rodriguez@hp.com", "85%", "2025-01-19"],
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

        # Info - ELIMINADO
        # self.results_info.setText(f"✅ {len(data)} registros encontrados - Consulta: {query_type}")

    def _on_theme_changed(self, new_theme: str):
        """Actualizar tema"""
        is_dark = (new_theme == 'dark')
        bg_color = "#2d2d2d" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#002E6D"
        subtitle_color = "#b0b0b0" if is_dark else "#666666"

        # FORZAR TEXTO BLANCO EN MODO OSCURO PARA TODO EL PANEL
        if is_dark:
            text_color = "#ffffff"
            subtitle_color = "#cccccc"

        # Actualizar header
        if hasattr(self, 'header_frame'):
            self.header_frame.setStyleSheet(f"background-color: {bg_color}; border: none;")
        
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none; padding: 0; margin: 0;")
            
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"color: {subtitle_color}; background: transparent; border: none;")

        # Actualizar tarjetas
        for card in self.cards:
            card._apply_theme()
            # Actualizar labels dentro de las cards (esto requeriría más lógica si no se recrean)
            # Por simplicidad, asumimos que los estilos de las cards se manejan en _apply_theme

        # Actualizar frame de resultados
        if hasattr(self, 'results_frame'):
            self.results_frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 12px;")

        if hasattr(self, 'results_title'):
            self.results_title.setStyleSheet(f"color: {text_color}; background: transparent;")

        # Actualizar tabla
        table_bg = "#1e1e1e" if is_dark else "#ffffff"
        table_text = "#ffffff" if is_dark else "#000000"
        table_alt = "#2d2d2d" if is_dark else "#f0f0f0"
        table_header = "#002E6D"
        
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {table_bg};
                color: {table_text};
                gridline-color: #444444;
                border: 1px solid #002E6D;
                border-radius: 8px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:alternate {{
                background-color: {table_alt};
            }}
            QHeaderView::section {{
                background-color: {table_header};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }}
        """)
