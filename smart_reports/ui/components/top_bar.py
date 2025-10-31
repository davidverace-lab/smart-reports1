"""
Componente TopBar - Barra superior con bienvenida y branding (Rediseñado con botones)
"""
import customtkinter as ctk
from smart_reports.config.theme_manager import get_theme_manager


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

    def _get_button_color(self):
        """
        Obtener color de botones según el tema actual
        - Modo claro: #002E6D (navy blue de sidebar)
        - Modo oscuro: #009BDE (Hutchison Ports blue)
        """
        theme = self.theme_manager.get_current_theme()
        # Si es tema oscuro (background oscuro), usar Hutchison blue
        # Si es tema claro (background claro), usar navy blue
        if theme['background'] == '#1a1a1a':  # Dark theme
            return '#009BDE'
        else:  # Light theme
            return '#002E6D'

    def _create_content(self):
        """Crear contenido del top bar con botones"""
        theme = self.theme_manager.get_current_theme()
        button_color = self._get_button_color()

        # Destruir widgets existentes si los hay
        for widget in self.winfo_children():
            widget.destroy()

        # Container principal con padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=30, pady=15)

        # === LADO IZQUIERDO: Bienvenida con botones ===
        left_frame = ctk.CTkFrame(container, fg_color='transparent')
        left_frame.pack(side='left', fill='y')

        # Contenedor horizontal para saludo y botones
        greeting_container = ctk.CTkFrame(left_frame, fg_color='transparent')
        greeting_container.pack(side='top', fill='x')

        # Saludo con nombre de usuario
        self.greeting_label = ctk.CTkLabel(
            greeting_container,
            text=f"¡Bienvenido, {self.username}!",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        self.greeting_label.pack(side='left', padx=(0, 15))

        # Botón de perfil
        self.profile_button = ctk.CTkButton(
            greeting_container,
            text="👤 Perfil",
            width=100,
            height=32,
            fg_color=button_color,
            hover_color=self._get_hover_color(button_color),
            font=('Montserrat', 12, 'bold'),
            corner_radius=8,
            command=self._on_profile_click
        )
        self.profile_button.pack(side='left', padx=5)

        # Botón de configuración
        self.settings_button = ctk.CTkButton(
            greeting_container,
            text="⚙️ Ajustes",
            width=100,
            height=32,
            fg_color=button_color,
            hover_color=self._get_hover_color(button_color),
            font=('Montserrat', 12, 'bold'),
            corner_radius=8,
            command=self._on_settings_click
        )
        self.settings_button.pack(side='left', padx=5)

        # === LADO DERECHO: Branding con botones ===
        right_frame = ctk.CTkFrame(container, fg_color='transparent')
        right_frame.pack(side='right', fill='y')

        # Contenedor horizontal para branding
        brand_container = ctk.CTkFrame(right_frame, fg_color='transparent')
        brand_container.pack(side='top')

        # Logo/Icono de Hutchison Ports como botón
        self.logo_button = ctk.CTkButton(
            brand_container,
            text="⚓",
            width=50,
            height=50,
            fg_color=button_color,
            hover_color=self._get_hover_color(button_color),
            font=('Arial', 28),
            corner_radius=10,
            command=self._on_logo_click
        )
        self.logo_button.pack(side='left', padx=(0, 10))

        # Texto "HUTCHISON PORTS" como botón
        self.brand_button = ctk.CTkButton(
            brand_container,
            text="HUTCHISON PORTS",
            width=200,
            height=50,
            fg_color=button_color,
            hover_color=self._get_hover_color(button_color),
            font=('Montserrat', 16, 'bold'),
            corner_radius=10,
            command=self._on_brand_click
        )
        self.brand_button.pack(side='left')

        # Línea divisoria inferior
        self.bottom_border = ctk.CTkFrame(
            self,
            height=2,
            fg_color=theme['border']
        )
        self.bottom_border.pack(side='bottom', fill='x')

    def _get_hover_color(self, base_color):
        """Generar color hover más claro que el color base"""
        # Hacer el color un poco más claro para el hover
        if base_color == '#002E6D':  # Navy blue
            return '#003D8F'  # Más claro
        elif base_color == '#009BDE':  # Hutchison blue
            return '#00B5FF'  # Más claro
        return base_color

    def _on_profile_click(self):
        """Callback para clic en botón de perfil"""
        print(f"Perfil de usuario: {self.username} ({self.user_role})")

    def _on_settings_click(self):
        """Callback para clic en botón de ajustes"""
        print("Abriendo configuración...")

    def _on_logo_click(self):
        """Callback para clic en logo"""
        print("Logo Hutchison Ports clickeado")

    def _on_brand_click(self):
        """Callback para clic en brand"""
        print("Hutchison Ports branding clickeado")

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
        # La solución definitiva: recrear todo el contenido con los nuevos colores
        self.configure(fg_color=theme_colors['surface'], border_color=theme_colors['border'])

        # Recrear todo el contenido para que use los colores correctos
        self._create_content()
