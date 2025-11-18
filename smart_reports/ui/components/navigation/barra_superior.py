"""
Componente TopBar - Barra superior con bienvenida y branding
"""
import customtkinter as ctk
from smart_reports.config.gestor_temas import get_theme_manager


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

    def _get_brand_color(self):
        """
        Obtener color de branding según el tema actual
        - Modo claro: #002E6D (navy blue de sidebar)
        - Modo oscuro: #009BDE (cyan - Hutchison Ports blue)
        """
        theme = self.theme_manager.get_current_theme()
        if theme['background'] == '#1a1a1a':  # Dark theme
            return '#009BDE'  # Cyan
        else:  # Light theme
            return '#002E6D'  # Navy blue

    def _create_content(self):
        """Crear contenido del top bar"""
        theme = self.theme_manager.get_current_theme()

        # Destruir widgets existentes si los hay
        for widget in self.winfo_children():
            widget.destroy()

        # Container principal con padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=30, pady=0)

        # === LADO IZQUIERDO: Bienvenida (centrada verticalmente) ===
        left_frame = ctk.CTkFrame(container, fg_color='transparent')
        left_frame.pack(side='left', fill='both', expand=True)

        # Saludo con nombre de usuario (centrado verticalmente)
        self.greeting_label = ctk.CTkLabel(
            left_frame,
            text=f"¡Bienvenido, {self.username}!",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        self.greeting_label.pack(side='left', anchor='w', pady=0)

        # === LADO DERECHO: Branding (centrado verticalmente) ===
        right_frame = ctk.CTkFrame(container, fg_color='transparent')
        right_frame.pack(side='right', fill='both', expand=True)

        # Texto "HUTCHISON PORTS" - Blanco en modo oscuro, azul marino en modo claro
        is_dark = self.theme_manager.is_dark_mode()
        brand_color = '#FFFFFF' if is_dark else '#002E6D'
        self.brand_label = ctk.CTkLabel(
            right_frame,
            text="HUTCHISON PORTS",
            font=('Montserrat', 24, 'bold'),
            text_color=brand_color,
            anchor='e'
        )
        self.brand_label.pack(side='right', anchor='e', pady=0)

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
        if hasattr(self, 'greeting_label'):
            self.greeting_label.configure(text=f"¡Bienvenido, {username}!")

    def _on_theme_changed(self, theme_colors: dict):
        """Actualizar colores cuando cambia el tema - RECREA TODO"""
        # Recrear todo el contenido para que use los colores correctos
        self.configure(fg_color=theme_colors['surface'], border_color=theme_colors['border'])
        self._create_content()
