"""
Componente ConfigCard - Card para opciones de configuración (Rediseñado con colores dinámicos)
"""
import customtkinter as ctk
from smart_reports.config.gestor_temas import get_theme_manager


class ConfigCard(ctk.CTkFrame):
    """Card para opciones de configuración con icono, título, descripción y botón"""

    def __init__(self, parent, icon, title, description, button_text, command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            icon: Emoji o icono a mostrar
            title: Título de la opción
            description: Descripción de la funcionalidad
            button_text: Texto del botón
            command: Función a ejecutar al hacer clic
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15,
            border_width=1,
            border_color=theme['colors']['border'],
            **kwargs
        )

        self.icon = icon
        self.title = title
        self.description = description
        self.button_text = button_text
        self.command = command

        # Crear contenido
        self._create_content()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _get_button_color(self):
        """
        Obtener color de botones según el tema actual
        - Modo claro: #002E6D (navy blue de sidebar)
        - Modo oscuro: #009BDE (cyan - Hutchison Ports blue)
        """
        theme = self.theme_manager.get_current_theme()
        if theme['colors']['background'] == '#1a1a1a':  # Dark theme
            return '#009BDE'  # Cyan
        else:  # Light theme
            return '#002E6D'  # Navy blue

    def _get_icon_color(self):
        """
        Obtener color del icono según el tema actual
        - Modo claro: #002E6D (navy blue)
        - Modo oscuro: #FFFFFF (blanco para visibilidad)
        """
        theme = self.theme_manager.get_current_theme()
        if theme['colors']['background'] == '#1a1a1a':  # Dark theme
            return '#FFFFFF'  # Blanco para máxima visibilidad
        else:  # Light theme
            return '#002E6D'  # Navy blue

    def _create_content(self):
        """Crear contenido del card con colores dinámicos"""
        theme = self.theme_manager.get_current_theme()
        button_color = self._get_button_color()
        icon_color = self._get_icon_color()

        # Destruir widgets existentes si los hay
        for widget in self.winfo_children():
            widget.destroy()

        # Container principal con padding más grande
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=30, pady=30)

        # Icono con color dinámico (más grande)
        self.icon_label = ctk.CTkLabel(
            main_container,
            text=self.icon,
            font=('Montserrat', 56),
            text_color=icon_color,
            anchor='center'
        )
        self.icon_label.pack(pady=(0, 20))

        # Título (más grande)
        self.title_label = ctk.CTkLabel(
            main_container,
            text=self.title,
            font=('Montserrat', 22, 'bold'),
            text_color=theme['colors']['text'],
            anchor='center'
        )
        self.title_label.pack(pady=(0, 12))

        # Descripción (solo si no está vacía) (más grande)
        if self.description:
            self.desc_label = ctk.CTkLabel(
                main_container,
                text=self.description,
                font=('Montserrat', 13),
                text_color=theme['colors']['text_secondary'],
                anchor='center',
                wraplength=280,
                justify='center'
            )
            self.desc_label.pack(pady=(0, 25))
        else:
            # Espacio en blanco si no hay descripción
            spacer_desc = ctk.CTkFrame(main_container, fg_color='transparent', height=25)
            spacer_desc.pack()

        # Spacer para empujar el botón al fondo
        spacer = ctk.CTkFrame(main_container, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Botón de acción con color dinámico (MÁS GRANDE Y VISIBLE)
        self.action_btn = ctk.CTkButton(
            main_container,
            text=self.button_text,
            font=('Montserrat', 16, 'bold'),
            fg_color=button_color,
            hover_color=self._get_hover_color(button_color),
            corner_radius=12,
            height=52,
            border_width=0,
            command=self._on_button_click
        )
        self.action_btn.pack(fill='x', pady=(0, 5))

    def _on_button_click(self):
        """Ejecutar comando del botón"""
        if self.command:
            self.command()

    def _get_hover_color(self, base_color):
        """Generar color hover más claro/oscuro que el color base"""
        if base_color == '#002E6D':  # Navy blue
            return '#003D8F'  # Más claro
        elif base_color == '#009BDE':  # Cyan
            return '#00B5FF'  # Más claro
        return self._darken_color(base_color)

    def _darken_color(self, hex_color, factor=0.8):
        """Oscurecer un color hex para el estado hover"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}"

    def _on_theme_changed(self, theme_colors: dict):
        """Actualizar colores cuando cambia el tema - RECREA TODO"""
        try:
            # Verificar si el widget todavía existe
            if not self.winfo_exists():
                return

            # Actualizar el fondo del card
            self.configure(fg_color=theme_colors['surface'], border_color=theme_colors['border'])

            # Recrear todo el contenido con los nuevos colores
            self._create_content()
        except Exception as e:
            # Si hay cualquier error, desregistrar el callback silenciosamente
            pass

    def destroy(self):
        """Override destroy para desregistrar callback de tema"""
        try:
            # Desregistrar callback antes de destruir
            self.theme_manager.unregister_callback(self._on_theme_changed)
        except:
            pass

        # Llamar al destroy original
        super().destroy()
