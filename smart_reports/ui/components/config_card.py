"""
Componente ConfigCard - Card para opciones de configuración
"""
import customtkinter as ctk
from smart_reports.config.theme_manager import get_theme_manager


class ConfigCard(ctk.CTkFrame):
    """Card para opciones de configuración con icono, título, descripción y botón"""

    def __init__(self, parent, icon, title, description, button_text, button_color='#6c63ff', command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            icon: Emoji o icono a mostrar
            title: Título de la opción
            description: Descripción de la funcionalidad
            button_text: Texto del botón
            button_color: Color del botón (hex)
            command: Función a ejecutar al hacer clic
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border'],
            **kwargs
        )

        self.command = command

        # Container principal con padding
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=25, pady=25)

        # Icono con color
        icon_label = ctk.CTkLabel(
            main_container,
            text=icon,
            font=('Segoe UI', 48),
            text_color=button_color,  # Color del icono igual al del botón
            anchor='center'
        )
        icon_label.pack(pady=(0, 15))

        # Título
        title_label = ctk.CTkLabel(
            main_container,
            text=title,
            font=('Segoe UI', 20, 'bold'),
            text_color=theme['text'],
            anchor='center'
        )
        title_label.pack(pady=(0, 10))

        # Descripción (solo si no está vacía)
        if description:
            desc_label = ctk.CTkLabel(
                main_container,
                text=description,
                font=('Segoe UI', 12),
                text_color=theme['text_secondary'],
                anchor='center',
                wraplength=250,
                justify='center'
            )
            desc_label.pack(pady=(0, 20))
        else:
            # Espacio en blanco si no hay descripción
            spacer_desc = ctk.CTkFrame(main_container, fg_color='transparent', height=20)
            spacer_desc.pack()

        # Spacer para empujar el botón al fondo
        spacer = ctk.CTkFrame(main_container, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Botón de acción
        self.action_btn = ctk.CTkButton(
            main_container,
            text=button_text,
            font=('Segoe UI', 14, 'bold'),
            fg_color=button_color,
            hover_color=self._darken_color(button_color),
            corner_radius=10,
            height=45,
            command=self._on_button_click
        )
        self.action_btn.pack(fill='x')

    def _on_button_click(self):
        """Ejecutar comando del botón"""
        if self.command:
            self.command()

    def _darken_color(self, hex_color, factor=0.8):
        """Oscurecer un color hex para el estado hover"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}"
