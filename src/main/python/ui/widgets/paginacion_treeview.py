"""
Widget de Paginación para Treeview
OPTIMIZACIÓN: Evita congelar la UI con miles de filas

ANTES: Cargar 5000 filas = 8 segundos (UI congelada)
AHORA: Cargar 100 filas = 100ms (fluido)
"""
import customtkinter as ctk
from tkinter import ttk
from typing import List, Tuple, Optional, Callable
from src.main.res.config.gestor_temas import get_theme_manager


class TreeviewPaginado(ctk.CTkFrame):
    """
    Treeview con paginación automática

    Características:
    - Carga solo 100-500 filas a la vez
    - Navegación con botones (Anterior/Siguiente)
    - Salto a página específica
    - Indicador de página actual

    Uso:
        tree_paginado = TreeviewPaginado(
            parent,
            columns=('ID', 'Nombre', 'Email'),
            page_size=100
        )
        tree_paginado.set_data(resultados)  # Lista de tuplas
    """

    def __init__(self, parent, columns: Tuple[str, ...], page_size: int = 100, **kwargs):
        """
        Args:
            parent: Widget padre
            columns: Tupla con nombres de columnas
            page_size: Filas por página (default: 100)
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.columns = columns
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = 0
        self.all_data = []

        self.theme_manager = get_theme_manager()

        # Crear componentes
        self._create_treeview()
        self._create_pagination_controls()

    def _create_treeview(self):
        """Crear Treeview principal"""
        theme = self.theme_manager.get_current_theme()

        # Container para tabla
        table_container = ctk.CTkFrame(self, fg_color=theme['background'], corner_radius=10)
        table_container.pack(fill='both', expand=True, padx=0, pady=(0, 10))

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        is_dark = self.theme_manager.is_dark_mode()
        if is_dark:
            style.configure('Paginated.Treeview',
                background=theme['background'],
                foreground=theme['text'],
                fieldbackground=theme['background'],
                borderwidth=0,
                font=('Montserrat', 10)
            )
            style.configure('Paginated.Treeview.Heading',
                background=theme['surface'],
                foreground=theme['text'],
                borderwidth=1,
                font=('Montserrat', 11, 'bold')
            )
            style.map('Paginated.Treeview',
                background=[('selected', '#6c63ff')],
                foreground=[('selected', '#ffffff')]
            )
        else:
            style.configure('Paginated.Treeview',
                background='#ffffff',
                foreground=theme['text'],
                fieldbackground='#ffffff',
                borderwidth=0,
                font=('Montserrat', 10)
            )
            style.configure('Paginated.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['text'],
                borderwidth=1,
                font=('Montserrat', 11, 'bold')
            )

        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical")
        hsb = ttk.Scrollbar(table_container, orient="horizontal")

        # Treeview
        self.tree = ttk.Treeview(
            table_container,
            columns=self.columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style='Paginated.Treeview',
            height=15
        )

        # Configurar columnas
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='w')

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

    def _create_pagination_controls(self):
        """Crear controles de paginación"""
        theme = self.theme_manager.get_current_theme()

        controls_frame = ctk.CTkFrame(self, fg_color='transparent')
        controls_frame.pack(fill='x', pady=5)

        # Info de página
        self.page_info_label = ctk.CTkLabel(
            controls_frame,
            text="Página 0 de 0 | 0 resultados",
            font=('Montserrat', 12),
            text_color=theme['text_secondary']
        )
        self.page_info_label.pack(side='left', padx=10)

        # Botones de navegación
        nav_frame = ctk.CTkFrame(controls_frame, fg_color='transparent')
        nav_frame.pack(side='right', padx=10)

        button_color = '#6c63ff' if self.theme_manager.is_dark_mode() else '#002E6D'

        self.btn_first = ctk.CTkButton(
            nav_frame,
            text="⏮ Primera",
            font=('Montserrat', 11, 'bold'),
            fg_color=button_color,
            hover_color='#5a52d5',
            height=32,
            width=100,
            command=self.first_page
        )
        self.btn_first.pack(side='left', padx=2)

        self.btn_prev = ctk.CTkButton(
            nav_frame,
            text="◀ Anterior",
            font=('Montserrat', 11, 'bold'),
            fg_color=button_color,
            hover_color='#5a52d5',
            height=32,
            width=100,
            command=self.prev_page
        )
        self.btn_prev.pack(side='left', padx=2)

        # Entry para salto de página
        self.page_entry = ctk.CTkEntry(
            nav_frame,
            width=60,
            height=32,
            font=('Montserrat', 11),
            placeholder_text="Pág."
        )
        self.page_entry.pack(side='left', padx=5)
        self.page_entry.bind('<Return>', lambda e: self.goto_page())

        ctk.CTkButton(
            nav_frame,
            text="Ir",
            font=('Montserrat', 11, 'bold'),
            fg_color=button_color,
            hover_color='#5a52d5',
            height=32,
            width=50,
            command=self.goto_page
        ).pack(side='left', padx=2)

        self.btn_next = ctk.CTkButton(
            nav_frame,
            text="Siguiente ▶",
            font=('Montserrat', 11, 'bold'),
            fg_color=button_color,
            hover_color='#5a52d5',
            height=32,
            width=100,
            command=self.next_page
        )
        self.btn_next.pack(side='left', padx=2)

        self.btn_last = ctk.CTkButton(
            nav_frame,
            text="Última ⏭",
            font=('Montserrat', 11, 'bold'),
            fg_color=button_color,
            hover_color='#5a52d5',
            height=32,
            width=100,
            command=self.last_page
        )
        self.btn_last.pack(side='left', padx=2)

    # ==================== API PÚBLICA ====================

    def set_data(self, data: List[Tuple]):
        """
        Cargar datos completos y mostrar primera página

        Args:
            data: Lista de tuplas (una por fila)
        """
        self.all_data = data
        self.total_pages = max(1, (len(data) + self.page_size - 1) // self.page_size)
        self.current_page = 0

        self._refresh_page()

    def clear(self):
        """Limpiar todos los datos"""
        self.all_data = []
        self.current_page = 0
        self.total_pages = 0
        self.tree.delete(*self.tree.get_children())
        self._update_controls()

    def get_selected(self) -> Optional[Tuple]:
        """Obtener fila seleccionada"""
        selection = self.tree.selection()
        if not selection:
            return None

        item = self.tree.item(selection[0])
        return tuple(item['values'])

    # ==================== NAVEGACIÓN ====================

    def first_page(self):
        """Ir a primera página"""
        if self.current_page != 0:
            self.current_page = 0
            self._refresh_page()

    def prev_page(self):
        """Página anterior"""
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_page()

    def next_page(self):
        """Página siguiente"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._refresh_page()

    def last_page(self):
        """Ir a última página"""
        if self.current_page != self.total_pages - 1:
            self.current_page = self.total_pages - 1
            self._refresh_page()

    def goto_page(self):
        """Ir a página específica"""
        try:
            page_num = int(self.page_entry.get()) - 1  # Usuario ingresa 1-indexed

            if 0 <= page_num < self.total_pages:
                self.current_page = page_num
                self._refresh_page()
            else:
                self.page_entry.delete(0, 'end')

        except ValueError:
            self.page_entry.delete(0, 'end')

    def _refresh_page(self):
        """Actualizar vista con datos de página actual"""
        # Limpiar tabla
        self.tree.delete(*self.tree.get_children())

        # Calcular rango de filas
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.all_data))

        # Insertar solo filas de página actual
        for row in self.all_data[start_idx:end_idx]:
            self.tree.insert('', 'end', values=row)

        # Actualizar controles
        self._update_controls()

    def _update_controls(self):
        """Actualizar estado de botones y etiquetas"""
        # Actualizar label
        total_results = len(self.all_data)
        self.page_info_label.configure(
            text=f"Página {self.current_page + 1} de {self.total_pages} | {total_results:,} resultados"
        )

        # Deshabilitar botones según contexto
        self.btn_first.configure(state='normal' if self.current_page > 0 else 'disabled')
        self.btn_prev.configure(state='normal' if self.current_page > 0 else 'disabled')
        self.btn_next.configure(state='normal' if self.current_page < self.total_pages - 1 else 'disabled')
        self.btn_last.configure(state='normal' if self.current_page < self.total_pages - 1 else 'disabled')
