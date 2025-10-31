"""
Componente TopBar - Barra superior con bienvenida y branding
"""
import customtkinter as ctk
from smart_reports.config.theme_manager import get_theme_manager
from smart_reports.config.settings import HUTCHISON_COLORS


class TopBar(ctk.CTkFrame):
    """Barra superior con bienvenida al usuario y branding Hutchison Ports"""

    def __init__(self, parent, username="Usuario", user_role="Administrador", **kwargs):
        """
        Args:
            parent: Widget padre
            username: Nombre del usuario autenticado
            user_role: Rol del usuario (Administrador, Operador, etc.)
        """
        # Obtener gestor de temas
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            height=80,
            fg_color=theme['surface'],
            corner_radius=0,
            border_width=0,
            border_color=theme['border'],
            **kwargs
        )

        self.username = username
        self.user_role = user_role

        # Evitar que el frame cambie de tamaño
        self.pack_propagate(False)

        # Crear contenido
        self._create_content()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_content(self):
        """Crear contenido del top bar"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=30, pady=15)

        # === LADO IZQUIERDO: Bienvenida ===
        left_frame = ctk.CTkFrame(container, fg_color='transparent')
        left_frame.pack(side='left', fill='y')

        # Saludo con nombre de usuario
        self.greeting_label = ctk.CTkLabel(
            left_frame,
            text=f"¡Bienvenido, {self.username}!",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        self.greeting_label.pack(side='top', anchor='w')

        # === LADO DERECHO: Branding ===
        right_frame = ctk.CTkFrame(container, fg_color='transparent')
        right_frame.pack(side='right', fill='y')

        # Logo/Icono de Hutchison Ports
        logo_label = ctk.CTkLabel(
            right_frame,
            text="⚓",  # Icono de ancla
            font=('Arial', 32),
            text_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        logo_label.pack(side='left', padx=(0, 15))

        # Texto "HUTCHISON PORTS"
        brand_frame = ctk.CTkFrame(right_frame, fg_color='transparent')
        brand_frame.pack(side='left')

        self.brand_label = ctk.CTkLabel(
            brand_frame,
            text="HUTCHISON PORTS",
            font=('Montserrat', 18, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sky_blue'],
            anchor='e'
        )
        self.brand_label.pack(anchor='e')

        # Línea divisoria inferior
        self.bottom_border = ctk.CTkFrame(
            self,
            height=2,
            fg_color=theme['border']
        )
        self.bottom_border.pack(side='bottom', fill='x')

    def update_user(self, username, user_role):
        """
        Actualizar información del usuario

        Args:
            username: Nuevo nombre de usuario
            user_role: Nuevo rol
        """
        self.username = username
        self.user_role = user_role
        self.greeting_label.configure(text=f"¡Bienvenido, {username}!")

    def _on_theme_changed(self, theme_colors: dict):
        """Actualizar colores cuando cambia el tema"""
        # Actualizar fondo
        self.configure(fg_color=theme_colors['surface'], border_color=theme_colors['border'])

        # Actualizar textos
        self.greeting_label.configure(text_color=theme_colors['text'])

        # Actualizar borde inferior
        self.bottom_border.configure(fg_color=theme_colors['border'])
