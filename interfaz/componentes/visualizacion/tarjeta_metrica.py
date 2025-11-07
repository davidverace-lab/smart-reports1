"""
Componente MetricCard - Card moderna para mostrar métricas
"""
import customtkinter as ctk
from nucleo.configuracion.gestor_temas import get_theme_manager


class MetricCard(ctk.CTkFrame):
    """Card moderna para mostrar una métrica con valor, cambio porcentual e icono"""

    def __init__(self, parent, title, value, change_percent=None, icon=None, color='#6c63ff', **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título de la métrica
            value: Valor principal a mostrar
            change_percent: Porcentaje de cambio (opcional)
            icon: Emoji o icono a mostrar (opcional)
            color: Color de acento para el icono y hover
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=20,
            border_width=1,
            border_color=theme['border'],
            **kwargs
        )

        self.accent_color = color
        self.default_border_color = theme['border']

        # Padding interno
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)

        row = 0

        # Icono (opcional)
        if icon:
            icon_label = ctk.CTkLabel(
                self,
                text=icon,
                font=('Segoe UI', 24),  # Reducido de 32 a 24
                text_color=color
            )
            icon_label.grid(row=row, column=0, padx=20, pady=(15, 5), sticky='w')
            row += 1

        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=('Montserrat', 11),  # Reducido de 14 a 11
            text_color=theme['text_secondary'],
            anchor='w'
        )
        self.title_label.grid(row=row, column=0, padx=20, pady=(8 if icon else 15, 5), sticky='w')
        row += 1

        # Valor principal
        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=('Montserrat', 28, 'bold'),  # Reducido de 48 a 28
            text_color=theme['text'],
            anchor='w'
        )
        self.value_label.grid(row=row, column=0, padx=20, pady=(0, 8), sticky='w')
        row += 1

        # Indicador de cambio (opcional)
        if change_percent is not None:
            change_color = '#51cf66' if change_percent >= 0 else '#ff6b6b'
            arrow = '↑' if change_percent >= 0 else '↓'

            change_label = ctk.CTkLabel(
                self,
                text=f'{arrow} {abs(change_percent):.1f}%',
                font=('Montserrat', 16, 'bold'),
                text_color=change_color
            )
            change_label.grid(row=row, column=0, padx=20, pady=(0, 20), sticky='w')
        else:
            # Agregar padding inferior si no hay indicador
            spacer = ctk.CTkLabel(self, text='', height=10)
            spacer.grid(row=row, column=0)

        # Efecto hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_enter(self, event):
        """Efecto hover - resaltar borde"""
        self.configure(border_color=self.accent_color)

    def _on_leave(self, event):
        """Salir del hover - restaurar borde"""
        self.configure(border_color=self.default_border_color)

    def update_value(self, new_value, new_change_percent=None):
        """Actualizar el valor de la métrica"""
        # Buscar y actualizar el label del valor
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                # Identificar label de valor por su font size
                font_info = child.cget('font')
                if '28' in str(font_info):  # Actualizado de 48 a 28
                    child.configure(text=str(new_value))
                    break
