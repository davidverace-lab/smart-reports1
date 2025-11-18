"""
Diálogo de Matching Manual - Resolver Duplicados
Permite al usuario decidir cómo manejar registros duplicados durante la importación
"""
import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS


class DialogoMatching(ctk.CTkToplevel):
    """
    Ventana de diálogo para resolver duplicados manualmente

    Permite al usuario:
    - Ver registros duplicados lado a lado
    - Elegir mantener existente, usar nuevo, o combinar
    - Aplicar decisión a todos los duplicados similares
    """

    def __init__(self, parent, duplicados, **kwargs):
        """
        Args:
            parent: Ventana padre
            duplicados: Lista de tuplas (registro_bd, registro_excel)
        """
        super().__init__(parent, **kwargs)

        self.theme_manager = get_theme_manager()
        self.duplicados = duplicados
        self.indice_actual = 0
        self.decisiones = []
        self.aplicar_a_todos = False
        self.decision_general = None

        # Configurar ventana
        self.title("🔍 Resolver Duplicados - Matching Manual")
        self.geometry("900x650")
        self.resizable(False, False)

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (650 // 2)
        self.geometry(f"900x650+{x}+{y}")

        # Crear interfaz
        self._create_ui()

        # Mostrar primer duplicado
        if self.duplicados:
            self._mostrar_duplicado_actual()

    def _create_ui(self):
        """Crear interfaz del diálogo"""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = ctk.CTkFrame(self, fg_color=HUTCHISON_COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🔍 Matching Manual de Duplicados",
            font=('Segoe UI', 20, 'bold'),
            text_color='white'
        )
        title.pack(side='left', padx=20, pady=20)

        # Contador
        self.counter_label = ctk.CTkLabel(
            header,
            text=f"Duplicado 1 de {len(self.duplicados)}",
            font=('Segoe UI', 12, 'bold'),
            text_color='white'
        )
        self.counter_label.pack(side='right', padx=20)

        # Contenedor principal
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Mensaje informativo
        info = ctk.CTkLabel(
            container,
            text="⚠ Se encontraron registros duplicados. Elige cómo proceder:",
            font=('Segoe UI', 11),
            text_color=theme['text_secondary']
        )
        info.pack(pady=(0, 15))

        # Frame de comparación (2 columnas)
        compare_frame = ctk.CTkFrame(container, fg_color='transparent')
        compare_frame.pack(fill='both', expand=True, pady=10)
        compare_frame.columnconfigure((0, 1), weight=1)

        # Columna izquierda: Registro en BD
        self.bd_frame = self._create_record_frame(
            compare_frame,
            "📁 Registro en Base de Datos",
            HUTCHISON_COLORS['primary'],
            0
        )

        # Columna derecha: Registro de Excel
        self.excel_frame = self._create_record_frame(
            compare_frame,
            "📊 Registro en Excel",
            HUTCHISON_COLORS['success'],
            1
        )

        # Separador
        sep = ctk.CTkFrame(container, fg_color=theme['border'], height=1)
        sep.pack(fill='x', pady=15)

        # Opciones de decisión
        self._create_decision_buttons(container)

        # Checkbox "Aplicar a todos"
        self.check_aplicar_todos = ctk.CTkCheckBox(
            container,
            text="✓ Aplicar esta decisión a todos los duplicados restantes",
            font=('Segoe UI', 11, 'bold'),
            text_color=theme['text'],
            command=self._toggle_aplicar_todos
        )
        self.check_aplicar_todos.pack(pady=10)

        # Botones de navegación
        nav_frame = ctk.CTkFrame(container, fg_color='transparent')
        nav_frame.pack(fill='x', pady=(10, 0))

        self.btn_anterior = ctk.CTkButton(
            nav_frame,
            text="◀ Anterior",
            font=('Segoe UI', 11, 'bold'),
            fg_color=theme['border'],
            hover_color=theme['surface_light'],
            text_color=theme['text'],
            width=120,
            command=self._anterior
        )
        self.btn_anterior.pack(side='left')
        self.btn_anterior.configure(state='disabled')

        self.btn_cancelar = ctk.CTkButton(
            nav_frame,
            text="✖ Cancelar Todo",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['danger'],
            hover_color='#d63031',
            width=140,
            command=self._cancelar
        )
        self.btn_cancelar.pack(side='left', padx=10)

        self.btn_finalizar = ctk.CTkButton(
            nav_frame,
            text="✓ Finalizar",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color='#00d2a0',
            width=120,
            command=self._finalizar,
            state='disabled'
        )
        self.btn_finalizar.pack(side='right')

    def _create_record_frame(self, parent, title, color, column):
        """Crear frame para mostrar un registro"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=10,
            border_width=2,
            border_color=color
        )
        card.grid(row=0, column=column, padx=10, sticky='nsew')

        # Header
        header = ctk.CTkFrame(card, fg_color=color, corner_radius=8, height=40)
        header.pack(fill='x', padx=5, pady=5)
        header.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=('Segoe UI', 13, 'bold'),
            text_color='white'
        )
        title_label.pack(expand=True)

        # Contenido scrollable
        scroll = ctk.CTkScrollableFrame(
            card,
            fg_color='transparent',
            height=300
        )
        scroll.pack(fill='both', expand=True, padx=10, pady=10)

        # Guardar referencia
        card.content_frame = scroll

        return card

    def _create_decision_buttons(self, parent):
        """Crear botones de decisión"""
        buttons_frame = ctk.CTkFrame(parent, fg_color='transparent')
        buttons_frame.pack(fill='x', pady=10)
        buttons_frame.columnconfigure((0, 1, 2), weight=1)

        # Mantener existente
        btn_mantener = ctk.CTkButton(
            buttons_frame,
            text="📁 Mantener Existente",
            font=('Segoe UI', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color=HUTCHISON_COLORS['primary'],
            height=50,
            command=lambda: self._tomar_decision('mantener')
        )
        btn_mantener.grid(row=0, column=0, padx=5, sticky='ew')

        # Usar nuevo
        btn_nuevo = ctk.CTkButton(
            buttons_frame,
            text="📊 Usar Nuevo",
            font=('Segoe UI', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color='#00d2a0',
            height=50,
            command=lambda: self._tomar_decision('reemplazar')
        )
        btn_nuevo.grid(row=0, column=1, padx=5, sticky='ew')

        # Combinar
        btn_combinar = ctk.CTkButton(
            buttons_frame,
            text="🔀 Combinar Datos",
            font=('Segoe UI', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['warning'],
            hover_color='#f39c12',
            height=50,
            command=lambda: self._tomar_decision('combinar')
        )
        btn_combinar.grid(row=0, column=2, padx=5, sticky='ew')

    def _mostrar_duplicado_actual(self):
        """Mostrar el duplicado actual en pantalla"""
        if self.indice_actual >= len(self.duplicados):
            return

        registro_bd, registro_excel = self.duplicados[self.indice_actual]

        # Actualizar contador
        self.counter_label.configure(
            text=f"Duplicado {self.indice_actual + 1} de {len(self.duplicados)}"
        )

        # Limpiar frames
        for widget in self.bd_frame.content_frame.winfo_children():
            widget.destroy()
        for widget in self.excel_frame.content_frame.winfo_children():
            widget.destroy()

        # Mostrar registro BD
        self._mostrar_registro(self.bd_frame.content_frame, registro_bd)

        # Mostrar registro Excel
        self._mostrar_registro(self.excel_frame.content_frame, registro_excel)

        # Actualizar botones
        self.btn_anterior.configure(
            state='normal' if self.indice_actual > 0 else 'disabled'
        )

    def _mostrar_registro(self, parent, registro):
        """Mostrar campos de un registro"""
        theme = self.theme_manager.get_current_theme()

        if isinstance(registro, dict):
            for key, value in registro.items():
                row = ctk.CTkFrame(parent, fg_color='transparent')
                row.pack(fill='x', pady=3)

                label = ctk.CTkLabel(
                    row,
                    text=f"{key}:",
                    font=('Segoe UI', 10, 'bold'),
                    text_color=theme['text_secondary'],
                    width=120,
                    anchor='w'
                )
                label.pack(side='left')

                value_label = ctk.CTkLabel(
                    row,
                    text=str(value) if value is not None else "-",
                    font=('Segoe UI', 10),
                    text_color=theme['text'],
                    anchor='w'
                )
                value_label.pack(side='left', fill='x', expand=True)

    def _tomar_decision(self, tipo):
        """Tomar decisión sobre el duplicado actual"""
        if self.aplicar_a_todos:
            # Aplicar a todos los restantes
            for i in range(self.indice_actual, len(self.duplicados)):
                self.decisiones.append({
                    'indice': i,
                    'tipo': tipo,
                    'registro_bd': self.duplicados[i][0],
                    'registro_excel': self.duplicados[i][1]
                })

            # Finalizar
            self._finalizar()
        else:
            # Guardar decisión individual
            self.decisiones.append({
                'indice': self.indice_actual,
                'tipo': tipo,
                'registro_bd': self.duplicados[self.indice_actual][0],
                'registro_excel': self.duplicados[self.indice_actual][1]
            })

            # Siguiente duplicado
            self.indice_actual += 1

            if self.indice_actual < len(self.duplicados):
                self._mostrar_duplicado_actual()
            else:
                self._finalizar()

    def _anterior(self):
        """Volver al duplicado anterior"""
        if self.indice_actual > 0:
            self.indice_actual -= 1
            # Eliminar última decisión
            if self.decisiones and self.decisiones[-1]['indice'] == self.indice_actual:
                self.decisiones.pop()
            self._mostrar_duplicado_actual()

    def _toggle_aplicar_todos(self):
        """Toggle aplicar a todos"""
        self.aplicar_a_todos = self.check_aplicar_todos.get()

    def _cancelar(self):
        """Cancelar proceso"""
        respuesta = messagebox.askyesno(
            "Cancelar",
            "¿Cancelar el proceso de matching?\n\n"
            "No se importarán los registros duplicados."
        )
        if respuesta:
            self.decisiones = []
            self.destroy()

    def _finalizar(self):
        """Finalizar matching"""
        self.btn_finalizar.configure(state='normal')
        self.destroy()

    def get_decisiones(self):
        """Obtener lista de decisiones tomadas"""
        return self.decisiones
