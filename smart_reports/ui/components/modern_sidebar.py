"""
Componente ModernSidebar - Barra lateral moderna con navegación
"""
import customtkinter as ctk
from smart_reports.config.theme_manager import get_theme_manager
from smart_reports.config.settings import HUTCHISON_COLORS


class ModernSidebar(ctk.CTkFrame):
    """Sidebar moderna con logo, navegación y footer"""

    def __init__(self, parent, navigation_callbacks, theme_change_callback=None, **kwargs):
        """
        Args:
            parent: Widget padre
            navigation_callbacks: Dict con {nombre: callback_function}
            theme_change_callback: Callback para notificar cambio de tema
        """
        # Obtener gestor de temas
        self.theme_manager = get_theme_manager()
        self.theme_change_callback = theme_change_callback

        # Colores según tema actual
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            width=220,
            fg_color=theme['surface'],
            corner_radius=0,
            **kwargs
        )

        self.navigation_callbacks = navigation_callbacks
        self.nav_buttons = []
        self.active_button = None

        # Logo/Header
        self._create_header()

        # Navegación
        self._create_navigation()

        # Toggle de tema
        self._create_theme_toggle()

        # Footer con versión
        self._create_footer()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_header(self):
        """Crear header con logo y título"""
        theme = self.theme_manager.get_current_theme()

        logo_frame = ctk.CTkFrame(self, fg_color='transparent', height=100)
        logo_frame.pack(fill='x', padx=20, pady=(20, 10))
        logo_frame.pack_propagate(False)

        # Título principal
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text='SMART\nREPORTS',
            font=('Montserrat', 22, 'bold'),
            text_color=theme['text'],
            justify='left'
        )
        self.logo_label.pack(anchor='w', pady=(10, 0))

        # Subtítulo
        self.subtitle = ctk.CTkLabel(
            logo_frame,
            text='INSTITUTO\nHUTCHISON PORTS',
            font=('Arial', 10),
            text_color=theme['text_secondary']
        )
        self.subtitle.pack(anchor='w', pady=(5, 0))

        # Línea separadora
        self.header_separator = ctk.CTkFrame(self, height=1, fg_color=theme['border'])
        self.header_separator.pack(fill='x', padx=20, pady=(10, 20))

    def _create_navigation(self):
        """Crear botones de navegación"""
        theme = self.theme_manager.get_current_theme()

        nav_items = [
            ('📊', 'Dashboard', 'dashboard'),
            ('🔍', 'Consultas', 'consultas'),
            ('📤', 'Actualizar Datos', 'actualizar'),
            ('⚙️', 'Configuración', 'configuracion'),
        ]

        for icon, text, key in nav_items:
            if key in self.navigation_callbacks:
                btn = ctk.CTkButton(
                    self,
                    text=f'{icon}  {text}',
                    font=('Arial', 14),
                    fg_color='transparent',
                    text_color=theme['text_secondary'],
                    hover_color=theme['surface_light'],
                    anchor='w',
                    height=50,
                    corner_radius=10,
                    command=lambda k=key: self._on_nav_click(k)
                )
                btn.pack(fill='x', padx=10, pady=5)
                self.nav_buttons.append((key, btn))

    def _create_theme_toggle(self):
        """Crear toggle para modo claro/oscuro"""
        theme = self.theme_manager.get_current_theme()

        # Frame para el toggle
        toggle_frame = ctk.CTkFrame(self, fg_color='transparent', height=70)
        toggle_frame.pack(fill='x', padx=15, pady=(15, 5))
        toggle_frame.pack_propagate(False)

        # Línea separadora superior
        self.theme_separator_top = ctk.CTkFrame(toggle_frame, height=1, fg_color=theme['border'])
        self.theme_separator_top.pack(fill='x', pady=(0, 10))

        # Container horizontal para icono, texto y switch
        toggle_container = ctk.CTkFrame(toggle_frame, fg_color='transparent')
        toggle_container.pack(fill='x')

        # Icono y texto
        self.theme_label = ctk.CTkLabel(
            toggle_container,
            text='🌙  Modo Oscuro' if self.theme_manager.is_dark_mode() else '☀️  Modo Claro',
            font=('Arial', 13),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        self.theme_label.pack(side='left', padx=(10, 0))

        # Switch toggle - Usar color corporativo Hutchison Ports
        self.theme_switch = ctk.CTkSwitch(
            toggle_container,
            text='',
            width=50,
            height=24,
            progress_color=HUTCHISON_COLORS['ports_sky_blue'],
            button_color=theme['surface_light'],
            button_hover_color=theme['border'],
            fg_color=theme['border'],
            command=self._on_theme_toggle
        )
        self.theme_switch.pack(side='right', padx=(0, 10))

        # Establecer estado inicial
        if self.theme_manager.is_dark_mode():
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Línea separadora inferior
        self.theme_separator_bottom = ctk.CTkFrame(toggle_frame, height=1, fg_color=theme['border'])
        self.theme_separator_bottom.pack(fill='x', pady=(10, 0))

    def _create_footer(self):
        """Crear footer con información de versión"""
        theme = self.theme_manager.get_current_theme()

        # Spacer para empujar footer al fondo
        spacer = ctk.CTkFrame(self, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Footer
        footer = ctk.CTkFrame(self, fg_color='transparent', height=60)
        footer.pack(side='bottom', fill='x', padx=20, pady=20)
        footer.pack_propagate(False)

        # Línea separadora superior
        self.footer_separator = ctk.CTkFrame(footer, height=1, fg_color=theme['border'])
        self.footer_separator.pack(fill='x', pady=(0, 10))

        # Versión
        self.version_label = ctk.CTkLabel(
            footer,
            text='v2.0.0',
            font=('Arial', 10),
            text_color=theme['text_secondary']
        )
        self.version_label.pack()

        # Copyright
        self.copyright_label = ctk.CTkLabel(
            footer,
            text='© 2025 INSTITUTO HP',
            font=('Arial', 9),
            text_color=theme['text_secondary']
        )
        self.copyright_label.pack()

    def _on_nav_click(self, key):
        """Manejar click en navegación"""
        theme = self.theme_manager.get_current_theme()

        # Actualizar estilos de botones
        for btn_key, btn in self.nav_buttons:
            if btn_key == key:
                btn.configure(
                    fg_color=theme['surface_light'],
                    text_color=theme['text']
                )
                self.active_button = btn
            else:
                btn.configure(
                    fg_color='transparent',
                    text_color=theme['text_secondary']
                )

        # Ejecutar callback
        if key in self.navigation_callbacks:
            self.navigation_callbacks[key]()

    def set_active(self, key):
        """Establecer botón activo programáticamente"""
        self._on_nav_click(key)

    def _on_theme_toggle(self):
        """Manejar cambio de tema"""
        self.theme_manager.toggle_theme()
        # El callback _on_theme_changed se llamará automáticamente

        # Notificar a la ventana principal
        if self.theme_change_callback:
            self.theme_change_callback(self.theme_manager.get_current_theme())

    def _on_theme_changed(self, theme_colors: dict):
        """Actualizar colores del sidebar cuando cambia el tema"""
        # Actualizar fondo del sidebar
        self.configure(fg_color=theme_colors['surface'])

        # Actualizar header
        self.logo_label.configure(text_color=theme_colors['text'])
        self.subtitle.configure(text_color=theme_colors['text_secondary'])
        self.header_separator.configure(fg_color=theme_colors['border'])

        # Actualizar botones de navegación
        for btn_key, btn in self.nav_buttons:
            if btn == self.active_button:
                btn.configure(
                    fg_color=theme_colors['surface_light'],
                    text_color=theme_colors['text'],
                    hover_color=theme_colors['surface_light']
                )
            else:
                btn.configure(
                    text_color=theme_colors['text_secondary'],
                    hover_color=theme_colors['surface_light']
                )

        # Actualizar toggle de tema
        is_dark = self.theme_manager.is_dark_mode()
        self.theme_label.configure(
            text='🌙  Modo Oscuro' if is_dark else '☀️  Modo Claro',
            text_color=theme_colors['text_secondary']
        )
        self.theme_switch.configure(
            button_color=theme_colors['surface_light'],
            button_hover_color=theme_colors['border'],
            fg_color=theme_colors['border']
        )
        self.theme_separator_top.configure(fg_color=theme_colors['border'])
        self.theme_separator_bottom.configure(fg_color=theme_colors['border'])

        # Actualizar footer
        self.footer_separator.configure(fg_color=theme_colors['border'])
        self.version_label.configure(text_color=theme_colors['text_secondary'])
        self.copyright_label.configure(text_color=theme_colors['text_secondary'])
