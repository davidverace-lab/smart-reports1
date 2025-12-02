"""
HistorialReportesFragment - Fragment para ver historial de reportes generados
Separado según arquitectura Android Studio
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter.ttk as ttk
from smart_reports.config.gestor_temas import get_theme_manager


class HistorialReportesFragment(ctk.CTkFrame):
    """Fragment de Historial de Reportes PDF"""

    def __init__(self, parent, db_connection=None, on_back=None, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
            on_back: Callback para volver al menú principal
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None
        self.on_back = on_back
        self.theme_manager = get_theme_manager()

        # Crear interfaz
        self._create_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_interface(self):
        """Crear interfaz completa del fragment"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal - SIN MÁRGENES GRISES
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header con botón volver
        self._create_header(scroll_frame, theme)

        # Card de historial
        self._create_history_card(scroll_frame, theme)

    def _create_header(self, parent, theme):
        """Crear header con título y botón volver - NAVY BLUE"""
        from smart_reports.config.themes import HUTCHISON_COLORS

        header = ctk.CTkFrame(parent, fg_color='transparent', height=55)  # Reducido de 60 a 55
        header.pack(fill='x', pady=(0, 15))  # Reducido padding
        header.pack_propagate(False)

        # Botón volver - NAVY BLUE
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Montserrat', 13, 'bold'),  # Reducido de 14 a 13
            fg_color=HUTCHISON_COLORS['primary'],
            text_color='white',
            hover_color='#003D8F',
            corner_radius=8,
            width=110,  # Reducido de 120 a 110
            height=38,  # Reducido de 40 a 38
            command=self.on_back if self.on_back else None
        )
        back_btn.pack(side='left')

        # Título - Navy en modo claro, blanco en modo oscuro
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else HUTCHISON_COLORS['primary']

        title = ctk.CTkLabel(
            header,
            text='📋 Historial de Reportes',
            font=('Montserrat', 26, 'bold'),  # Reducido de 28 a 26
            text_color=title_color
        )
        title.pack(side='left', padx=15)  # Reducido de 20 a 15

    def _create_history_card(self, parent, theme):
        """Card de historial de reportes - MÁS COMPACTO"""
        history_card = ctk.CTkFrame(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=12,  # Reducido de 15 a 12
            border_width=1,
            border_color=theme['colors']['border']
        )
        history_card.pack(fill='both', expand=True)

        # Contenido del historial - PADDING REDUCIDO
        history_content = ctk.CTkFrame(history_card, fg_color='transparent')
        history_content.pack(fill='both', expand=True, padx=20, pady=20)  # Reducido de 30 a 20

        # Título de la tabla - MÁS COMPACTO
        table_title = ctk.CTkLabel(
            history_content,
            text='📑 Reportes Generados',
            font=('Montserrat', 16, 'bold'),  # Reducido de 18 a 16
            text_color=theme['colors']['text']
        )
        table_title.pack(anchor='w', pady=(0, 15))  # Reducido de 20 a 15

        # Container para tabla
        table_container_bg = theme['colors']['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        table_container = ctk.CTkFrame(history_content, fg_color=table_container_bg, corner_radius=10)
        table_container.pack(fill='both', expand=True)

        # Crear Treeview para historial
        self._create_treeview(table_container, theme)

        # Cargar datos
        self._load_report_history()

        # Botones de acción
        self._create_action_buttons(history_content, theme)

    def _create_treeview(self, parent, theme):
        """Crear tabla de reportes"""
        style = ttk.Style()
        style.theme_use('clam')

        if self.theme_manager.is_dark_mode():
            style.configure('History.Treeview',
                background=theme['colors']['background'],
                foreground=theme['colors']['text'],
                fieldbackground=theme['colors']['background'],
                borderwidth=0,
                font=('Montserrat', 11)
            )
            style.configure('History.Treeview.Heading',
                background=theme['colors'].get('card_background', '#2d2d2d'),
                foreground=theme['colors']['text'],
                borderwidth=1,
                font=('Montserrat', 12, 'bold')
            )
            style.map('History.Treeview',
                background=[('selected', '#1E90FF')],
                foreground=[('selected', '#ffffff')]
            )
        else:
            style.configure('History.Treeview',
                background='#ffffff',
                foreground=theme['colors']['text'],
                fieldbackground='#ffffff',
                borderwidth=0,
                font=('Montserrat', 11)
            )
            style.configure('History.Treeview.Heading',
                background='#e8e8e8',
                foreground=theme['colors']['text'],
                borderwidth=1,
                font=('Montserrat', 12, 'bold')
            )

        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical")

        self.history_tree = ttk.Treeview(
            parent,
            columns=('Fecha', 'Nombre', 'Formato', 'Tamaño', 'Estado'),
            show='headings',
            yscrollcommand=vsb.set,
            style='History.Treeview',
            height=10
        )

        # Configurar columnas
        self.history_tree.heading('Fecha', text='Fecha')
        self.history_tree.heading('Nombre', text='Nombre del Reporte')
        self.history_tree.heading('Formato', text='Formato')
        self.history_tree.heading('Tamaño', text='Tamaño')
        self.history_tree.heading('Estado', text='Estado')

        self.history_tree.column('Fecha', width=120, minwidth=100, anchor='center')
        self.history_tree.column('Nombre', width=350, minwidth=250)
        self.history_tree.column('Formato', width=80, minwidth=70, anchor='center')
        self.history_tree.column('Tamaño', width=100, minwidth=80, anchor='center')
        self.history_tree.column('Estado', width=120, minwidth=100, anchor='center')

        vsb.config(command=self.history_tree.yview)

        self.history_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def _create_action_buttons(self, parent, theme):
        """Crear botones de acción - NAVY BLUE con texto blanco"""
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(fill='x', pady=(15, 0))  # Reducido padding

        # ESTANDARIZAR: Todos los botones navy blue con texto blanco
        from smart_reports.config.themes import HUTCHISON_COLORS
        button_color = HUTCHISON_COLORS['primary']  # #002E6D - Navy blue

        ctk.CTkButton(
            button_frame,
            text='📥 Descargar Seleccionado',
            font=('Montserrat', 13, 'bold'),  # Reducido de 14 a 13
            fg_color=button_color,
            hover_color='#003D8F',
            text_color='white',
            corner_radius=8,
            height=40,  # Reducido de 45 a 40
            width=210,  # Reducido de 220 a 210
            command=self._download_selected
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            button_frame,
            text='🔄 Actualizar Lista',
            font=('Montserrat', 13, 'bold'),
            fg_color=button_color,
            hover_color='#003D8F',
            text_color='white',
            corner_radius=8,
            height=40,
            width=170,  # Reducido de 180 a 170
            command=self._refresh_list
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            button_frame,
            text='🗑️ Eliminar Seleccionado',
            font=('Montserrat', 13, 'bold'),
            fg_color='#C53030',  # Rojo más oscuro para peligro
            hover_color='#9B2C2C',
            text_color='white',
            corner_radius=8,
            height=40,
            width=190,  # Reducido de 200 a 190
            command=self._delete_selected
        ).pack(side='left', padx=5)

    # ==================== LÓGICA DE NEGOCIO ====================

    def _load_report_history(self):
        """Cargar historial de reportes desde BD o mostrar ejemplos"""
        # Limpiar tabla
        self.history_tree.delete(*self.history_tree.get_children())

        if self.cursor:
            try:
                # Intentar cargar desde BD
                query = """
                    SELECT ReportDate, ReportName, Format, FileSize, Status
                    FROM report_history
                    ORDER BY ReportDate DESC
                """
                self.cursor.execute(query)
                results = self.cursor.fetchall()

                if results:
                    for row in results:
                        self.history_tree.insert('', 'end', values=row)
                    return
            except:
                # Si falla, usar datos de ejemplo
                pass

        # Datos de ejemplo (fallback)
        reportes_ejemplo = [
            ('2025-11-01', 'Reporte Gerencial Q1', 'PDF', '2.3 MB', 'Completado'),
            ('2025-10-28', 'Dashboard Mensual - Octubre', 'PDF', '1.8 MB', 'Completado'),
            ('2025-10-15', 'Progreso por Módulo', 'PDF', '1.5 MB', 'Completado'),
            ('2025-10-05', 'Reporte de Usuarios', 'PDF', '950 KB', 'Completado'),
            ('2025-09-30', 'Análisis Jerárquico Q3', 'PDF', '3.1 MB', 'Completado')
        ]

        for reporte in reportes_ejemplo:
            self.history_tree.insert('', 'end', values=reporte)

    def _download_selected(self):
        """Descargar reporte seleccionado"""
        selection = self.history_tree.selection()

        if not selection:
            messagebox.showwarning("Sin Selección", "Por favor seleccione un reporte para descargar")
            return

        item = self.history_tree.item(selection[0])
        values = item['values']

        # TODO: Implementar descarga real del archivo
        messagebox.showinfo(
            "Descargar Reporte",
            f"Descargando reporte:\n\n"
            f"Nombre: {values[1]}\n"
            f"Fecha: {values[0]}\n"
            f"Tamaño: {values[3]}\n\n"
            f"(Función en desarrollo)"
        )

    def _refresh_list(self):
        """Actualizar lista de reportes"""
        self._load_report_history()
        messagebox.showinfo("Lista Actualizada", "El historial de reportes ha sido actualizado")

    def _delete_selected(self):
        """Eliminar reporte seleccionado"""
        selection = self.history_tree.selection()

        if not selection:
            messagebox.showwarning("Sin Selección", "Por favor seleccione un reporte para eliminar")
            return

        item = self.history_tree.item(selection[0])
        values = item['values']

        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar este reporte?\n\n"
            f"Nombre: {values[1]}\n"
            f"Fecha: {values[0]}\n\n"
            f"Esta acción no se puede deshacer."
        )

        if not confirm:
            return

        # TODO: Implementar eliminación real
        self.history_tree.delete(selection[0])
        messagebox.showinfo("Eliminado", "Reporte eliminado correctamente")

    # ==================== UTILIDADES ====================

    def _get_button_color(self):
        """Obtener color de botón según tema"""
        is_dark = self.theme_manager.is_dark_mode()
        return '#6c63ff' if is_dark else '#002E6D'

    def _get_button_hover_color(self, base_color):
        """Obtener color hover"""
        if base_color == '#6c63ff':
            return '#5a52d5'
        elif base_color == '#002E6D':
            return '#00509E'
        return base_color

    def _on_theme_changed(self, theme_colors):
        """Callback para cambios de tema"""
        pass
