"""
CustomTabButton - Botones de pestañas personalizados más grandes y elegantes
"""
import customtkinter as ctk
from config.themes import HUTCHISON_COLORS


class CustomTabButton(ctk.CTkButton):
    """Botón de pestaña personalizado con diseño mejorado"""

    def __init__(self, parent, text, icon="", command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            text: Texto del botón
            icon: Emoji o icono (opcional)
            command: Función a ejecutar al hacer click
        """
        self.is_active = False
        self.tab_text = text
        self.tab_icon = icon

        display_text = f"{icon}  {text}" if icon else text

        super().__init__(
            parent,
            text=display_text,
            font=('Montserrat', 14, 'bold'),
            fg_color='transparent',
            text_color='#888888',
            hover_color='#3a3d5c',
            corner_radius=12,
            height=55,
            width=250,
            anchor='w',
            command=command,
            border_width=0,
            **kwargs
        )

    def set_active(self, active=True):
        """
        Establecer estado activo/inactivo

        Args:
            active: True si está activo, False si no
        """
        self.is_active = active

        if active:
            self.configure(
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='#ffffff',
                hover_color=HUTCHISON_COLORS['ports_sea_blue']
            )
        else:
            self.configure(
                fg_color='transparent',
                text_color='#888888',
                hover_color='#3a3d5c'
            )


class CustomTabView(ctk.CTkFrame):
    """Vista de pestañas personalizada con botones más grandes"""

    def __init__(self, parent, **kwargs):
        """
        Args:
            parent: Widget padre
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        # Contenedor para pestañas
        self.tabs = {}
        self.tab_buttons = {}
        self.active_tab = None
        self.on_change_callback = None

        # Frame para botones de pestañas
        self.tabs_frame = ctk.CTkFrame(self, fg_color='transparent', height=70)
        self.tabs_frame.pack(side='top', fill='x', pady=(0, 15))
        self.tabs_frame.pack_propagate(False)

        # Frame para contenido de pestañas
        self.content_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.content_frame.pack(side='top', fill='both', expand=True)

    def add(self, tab_name, icon=""):
        """
        Agregar una nueva pestaña

        Args:
            tab_name: Nombre de la pestaña
            icon: Icono emoji (opcional)

        Returns:
            Frame de la pestaña
        """
        # Crear botón de pestaña
        button = CustomTabButton(
            self.tabs_frame,
            text=tab_name,
            icon=icon,
            command=lambda: self.select_tab(tab_name)
        )
        button.pack(side='left', padx=8)

        # Crear frame de contenido
        tab_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')

        # Guardar referencias
        self.tab_buttons[tab_name] = button
        self.tabs[tab_name] = tab_frame

        # Si es la primera pestaña, activarla
        if len(self.tabs) == 1:
            self.select_tab(tab_name)

        return tab_frame

    def select_tab(self, tab_name):
        """
        Seleccionar una pestaña con transición fluida

        Args:
            tab_name: Nombre de la pestaña a seleccionar
        """
        if tab_name not in self.tabs or tab_name == self.active_tab:
            return

        # Desactivar todos los botones
        for name in self.tab_buttons:
            self.tab_buttons[name].set_active(False)

        # Activar botón seleccionado inmediatamente
        self.tab_buttons[tab_name].set_active(True)

        # Ocultar pestaña anterior
        if self.active_tab:
            self.tabs[self.active_tab].pack_forget()

        # Mostrar nueva pestaña con transición suave
        self.tabs[tab_name].pack(fill='both', expand=True)
        self.active_tab = tab_name

        # Llamar callback si existe
        if self.on_change_callback:
            self.on_change_callback(tab_name)

    def get(self):
        """Obtener nombre de la pestaña activa"""
        return self.active_tab

    def set_command(self, command):
        """Establecer callback para cambios de pestaña"""
        self.on_change_callback = command
