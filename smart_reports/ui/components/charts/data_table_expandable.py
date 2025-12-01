"""
Tabla de Datos Expandible In-Place - SMART REPORTS
Muestra datos de gráficas en formato tabla expandible dentro del mismo contenedor

Características:
✅ Tabla con scroll
✅ Respeta tema claro/oscuro
✅ Expansión IN-PLACE (no modal)
✅ Ordenar por columnas
✅ SIN búsqueda (según requerimiento)
"""
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS


class DataTableExpandable(ctk.CTkFrame):
    """Tabla expandible para mostrar datos in-place"""

    def __init__(self, parent, title='', data=None, chart_type='bar', on_close=None):
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=10,
            border_width=2,
            border_color=HUTCHISON_COLORS['primary']
        )

        self.title_text = title
        self.data = data or {}
        self.chart_type = chart_type
        self.on_close = on_close
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False

        # Crear UI
        self._create_ui()

        # Poblar tabla
        self._populate_table()

    def _create_ui(self):
        """Crear interfaz de la tabla expandible"""
        theme = self.theme_manager.get_current_theme()

        # === HEADER ===
        header = ctk.CTkFrame(
            self,
            fg_color=HUTCHISON_COLORS['primary'],
            corner_radius=8,
            height=60
        )
        header.pack(fill='x', padx=10, pady=10)
        header.pack_propagate(False)

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=f"📊 {self.title_text} - Datos",
            font=('Montserrat', 16, 'bold'),
            text_color='white'
        )
        title_label.pack(side='left', padx=20, pady=15)

        # Botón cerrar
        close_btn = ctk.CTkButton(
            header,
            text="✕ Cerrar",
            width=90,
            height=35,
            font=('Montserrat', 12, 'bold'),
            fg_color='transparent',
            hover_color='#b91c1c',
            text_color='white',
            border_width=2,
            border_color='white',
            command=self._close_table
        )
        close_btn.pack(side='right', padx=15, pady=12)

        # === FRAME DE TABLA ===
        table_frame = ctk.CTkFrame(
            self,
            fg_color=theme['colors']['background'],
            corner_radius=8
        )
        table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Crear Treeview con scroll
        self._create_treeview(table_frame)

        # === FOOTER CON INFO ===
        footer = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=35
        )
        footer.pack(fill='x', padx=20, pady=(0, 10))

        self.info_label = ctk.CTkLabel(
            footer,
            text="",
            font=('Montserrat', 11, 'bold'),
            text_color=theme['colors']['text']
        )
        self.info_label.pack(side='left')

    def _create_treeview(self, parent):
        """Crear tabla Treeview con scroll"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # Frame contenedor
        tree_container = tk.Frame(parent, bg=theme['colors']['background'])
        tree_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_container, orient="vertical")
        hsb = ttk.Scrollbar(tree_container, orient="horizontal")

        # Treeview
        if self.chart_type in ['bar', 'horizontal_bar', 'donut', 'pie']:
            columns = ('categoria', 'valor')
            headers = ('Categoría', 'Valor')
        else:
            columns = ('x', 'y')
            headers = ('X', 'Y')

        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='extended'
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Configurar columnas
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header, command=lambda c=col: self._sort_by_column(c))
            self.tree.column(col, width=250, anchor='center')

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Aplicar tema al Treeview
        self._apply_treeview_theme(is_dark)

        # Bind para copiar con Ctrl+C
        self.tree.bind('<Control-c>', self._copy_selection)

    def _apply_treeview_theme(self, is_dark):
        """Aplicar tema claro/oscuro al Treeview"""
        style = ttk.Style()

        if is_dark:
            # Tema oscuro
            bg_color = '#2d2d2d'
            fg_color = '#e0e0e0'
            selected_bg = HUTCHISON_COLORS['primary']
            selected_fg = 'white'
            field_bg = '#1a1a1a'
        else:
            # Tema claro
            bg_color = '#ffffff'
            fg_color = '#1a1a1a'
            selected_bg = HUTCHISON_COLORS['primary']
            selected_fg = 'white'
            field_bg = '#f8f9fa'

        style.theme_use('default')

        style.configure(
            "Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=field_bg,
            borderwidth=0,
            font=('Montserrat', 10)
        )

        style.configure(
            "Treeview.Heading",
            background=HUTCHISON_COLORS['primary'],
            foreground='white',
            borderwidth=1,
            font=('Montserrat', 11, 'bold')
        )

        style.map('Treeview',
                  background=[('selected', selected_bg)],
                  foreground=[('selected', selected_fg)])

        style.map('Treeview.Heading',
                  background=[('active', '#003D8F')],
                  foreground=[('active', 'white')])

    def _populate_table(self):
        """Poblar tabla con datos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.data or 'labels' not in self.data:
            return

        # Preparar datos
        if self.chart_type in ['bar', 'horizontal_bar', 'donut', 'pie']:
            self.filtered_data = list(zip(self.data['labels'], self.data['values']))
        else:
            self.filtered_data = list(zip(
                self.data.get('x', self.data['labels']),
                self.data.get('y', self.data['values'])
            ))

        # Insertar datos
        for i, row in enumerate(self.filtered_data):
            # Alternar colores de fondo
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=row, tags=(tag,))

        # Configurar colores alternados
        is_dark = self.theme_manager.is_dark_mode()

        if is_dark:
            self.tree.tag_configure('evenrow', background='#2d2d2d')
            self.tree.tag_configure('oddrow', background='#3a3a3a')
        else:
            self.tree.tag_configure('evenrow', background='#ffffff')
            self.tree.tag_configure('oddrow', background='#f8f9fa')

        # Actualizar info
        self._update_info()

    def _update_info(self):
        """Actualizar información del footer"""
        total_rows = len(self.filtered_data)
        total_sum = sum(row[1] for row in self.filtered_data) if self.filtered_data else 0

        self.info_label.configure(
            text=f"📊 Total de registros: {total_rows} | Suma: {total_sum:,.2f}"
        )

    def _sort_by_column(self, column):
        """Ordenar tabla por columna"""
        col_index = 0 if column in ['categoria', 'x'] else 1

        # Alternar orden
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
            self.sort_column = column

        # Ordenar datos
        self.filtered_data.sort(key=lambda x: x[col_index], reverse=self.sort_reverse)

        # Repoblar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        is_dark = self.theme_manager.is_dark_mode()

        for i, row in enumerate(self.filtered_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=row, tags=(tag,))

    def _copy_selection(self, event=None):
        """Copiar selección al portapapeles"""
        selection = self.tree.selection()

        if not selection:
            return

        # Obtener valores seleccionados
        rows = []
        for item in selection:
            values = self.tree.item(item, 'values')
            rows.append('\t'.join(str(v) for v in values))

        text = '\n'.join(rows)

        # Copiar al portapapeles
        self.clipboard_clear()
        self.clipboard_append(text)

        print(f"✅ {len(selection)} filas copiadas al portapapeles")

    def _close_table(self):
        """Cerrar tabla expandible"""
        if self.on_close:
            self.on_close()
        self.destroy()
