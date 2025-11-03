"""
Componente ModernSidebar - Barra lateral moderna con navegación
"""
import customtkinter as ctk
from config.theme_manager import get_theme_manager
from config.settings import HUTCHISON_COLORS


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

        # En modo claro, usar azul navy como fondo del sidebar
        sidebar_bg = HUTCHISON_COLORS['ports_sea_blue'] if not self.theme_manager.is_dark_mode() else theme['surface']

        super().__init__(
            parent,
            width=240,  # Aumentado de 220 a 240
            fg_color=sidebar_bg,
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
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, todo es blanco sobre azul navy
        text_color = '#FFFFFF' if not is_dark else theme['text']
        text_secondary_color = '#E0E0E0' if not is_dark else theme['text_secondary']
        border_color = '#4a5a8a' if not is_dark else theme['border']

        logo_frame = ctk.CTkFrame(self, fg_color='transparent', height=110)
        logo_frame.pack(fill='x', padx=20, pady=(20, 10))
        logo_frame.pack_propagate(False)

        # Título principal (más grande)
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text='SMART\nREPORTS',
            font=('Montserrat', 26, 'bold'),  # Aumentado de 22 a 26
            text_color=text_color,
            justify='left'
        )
        self.logo_label.pack(anchor='w', pady=(10, 0))

        # Subtítulo (más grande)
        self.subtitle = ctk.CTkLabel(
            logo_frame,
            text='INSTITUTO\nHUTCHISON PORTS',
            font=('Arial', 11),  # Aumentado de 10 a 11
            text_color=text_secondary_color
        )
        self.subtitle.pack(anchor='w', pady=(5, 0))

        # Línea separadora
        self.header_separator = ctk.CTkFrame(self, height=1, fg_color=border_color)
        self.header_separator.pack(fill='x', padx=20, pady=(10, 20))

    def _create_navigation(self):
        """Crear botones de navegación"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, texto blanco; en modo oscuro, texto normal
        nav_text_color = '#FFFFFF' if not is_dark else theme['text_secondary']
        hover_color = '#4a5a8a' if not is_dark else theme['surface_light']

        nav_items = [
            ('📊', 'Dashboard', 'dashboard'),
            ('🔍', 'Consultas', 'consultas'),
            ('📤', 'Actualizar Datos', 'actualizar'),
            ('📄', 'Generar Reportes', 'reportes'),
            ('⚙️', 'Configuración', 'configuracion'),
        ]

        for icon, text, key in nav_items:
            if key in self.navigation_callbacks:
                btn = ctk.CTkButton(
                    self,
                    text=f'{icon}  {text}',
                    font=('Arial', 15, 'bold'),  # Aumentado de 14 a 15 y añadido 'bold'
                    fg_color='transparent',
                    text_color=nav_text_color,
                    hover_color=hover_color,
                    anchor='w',
                    height=55,  # Aumentado de 50 a 55
                    corner_radius=10,
                    command=lambda k=key: self._on_nav_click(k)
                )
                btn.pack(fill='x', padx=10, pady=5)
                self.nav_buttons.append((key, btn))

    def _create_theme_toggle(self):
        """Crear toggle para modo claro/oscuro"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, texto y bordes blancos
        text_color = '#FFFFFF' if not is_dark else theme['text_secondary']
        border_color = '#4a5a8a' if not is_dark else theme['border']

        # Frame para el toggle
        toggle_frame = ctk.CTkFrame(self, fg_color='transparent', height=70)
        toggle_frame.pack(fill='x', padx=15, pady=(15, 5))
        toggle_frame.pack_propagate(False)

        # Línea separadora superior
        self.theme_separator_top = ctk.CTkFrame(toggle_frame, height=1, fg_color=border_color)
        self.theme_separator_top.pack(fill='x', pady=(0, 10))

        # Container horizontal para icono, texto y switch
        toggle_container = ctk.CTkFrame(toggle_frame, fg_color='transparent')
        toggle_container.pack(fill='x')

        # Icono y texto (más grande)
        self.theme_label = ctk.CTkLabel(
            toggle_container,
            text='🌙  Modo Oscuro' if is_dark else '☀️  Modo Claro',
            font=('Arial', 14, 'bold'),  # Aumentado de 13 a 14 y añadido 'bold'
            text_color=text_color,
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
            button_color='#4a5a8a' if not is_dark else theme['surface_light'],
            button_hover_color='#6a7aa0' if not is_dark else theme['border'],
            fg_color='#6a7aa0' if not is_dark else theme['border'],
            command=self._on_theme_toggle
        )
        self.theme_switch.pack(side='right', padx=(0, 10))

        # Establecer estado inicial
        if is_dark:
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

        # Línea separadora inferior
        self.theme_separator_bottom = ctk.CTkFrame(toggle_frame, height=1, fg_color=border_color)
        self.theme_separator_bottom.pack(fill='x', pady=(10, 0))

    def _create_footer(self):
        """Crear footer con información de versión"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, texto blanco
        text_color = '#E0E0E0' if not is_dark else theme['text_secondary']
        border_color = '#4a5a8a' if not is_dark else theme['border']

        # Spacer para empujar footer al fondo
        spacer = ctk.CTkFrame(self, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Footer
        footer = ctk.CTkFrame(self, fg_color='transparent', height=60)
        footer.pack(side='bottom', fill='x', padx=20, pady=20)
        footer.pack_propagate(False)

        # Línea separadora superior
        self.footer_separator = ctk.CTkFrame(footer, height=1, fg_color=border_color)
        self.footer_separator.pack(fill='x', pady=(0, 10))

        # Versión (más grande)
        self.version_label = ctk.CTkLabel(
            footer,
            text='v2.0.0',
            font=('Arial', 11, 'bold'),  # Aumentado de 10 a 11 y añadido 'bold'
            text_color=text_color
        )
        self.version_label.pack()

        # Copyright (más grande)
        self.copyright_label = ctk.CTkLabel(
            footer,
            text='© 2025 INSTITUTO HP',
            font=('Arial', 10),  # Aumentado de 9 a 10
            text_color=text_color
        )
        self.copyright_label.pack()

    def _on_nav_click(self, key):
        """Manejar click en navegación"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, todo es blanco
        active_bg = '#4a5a8a' if not is_dark else theme['surface_light']
        active_text = '#FFFFFF' if not is_dark else theme['text']
        inactive_text = '#E0E0E0' if not is_dark else theme['text_secondary']

        # Actualizar estilos de botones
        for btn_key, btn in self.nav_buttons:
            if btn_key == key:
                btn.configure(
                    fg_color=active_bg,
                    text_color=active_text
                )
                self.active_button = btn
            else:
                btn.configure(
                    fg_color='transparent',
                    text_color=inactive_text
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
        is_dark = self.theme_manager.is_dark_mode()

        # En modo claro, fondo azul navy; en modo oscuro, fondo del tema
        sidebar_bg = HUTCHISON_COLORS['ports_sea_blue'] if not is_dark else theme_colors['surface']
        text_color = '#FFFFFF' if not is_dark else theme_colors['text']
        text_secondary_color = '#E0E0E0' if not is_dark else theme_colors['text_secondary']
        border_color = '#4a5a8a' if not is_dark else theme_colors['border']
        hover_color = '#4a5a8a' if not is_dark else theme_colors['surface_light']
        active_bg = '#4a5a8a' if not is_dark else theme_colors['surface_light']

        # Actualizar fondo del sidebar
        self.configure(fg_color=sidebar_bg)

        # Actualizar header
        self.logo_label.configure(text_color=text_color)
        self.subtitle.configure(text_color=text_secondary_color)
        self.header_separator.configure(fg_color=border_color)

        # Actualizar botones de navegación
        for btn_key, btn in self.nav_buttons:
            if btn == self.active_button:
                btn.configure(
                    fg_color=active_bg,
                    text_color=text_color,
                    hover_color=hover_color
                )
            else:
                btn.configure(
                    text_color=text_secondary_color if not is_dark else theme_colors['text_secondary'],
                    hover_color=hover_color
                )

        # Actualizar toggle de tema
        self.theme_label.configure(
            text='🌙  Modo Oscuro' if is_dark else '☀️  Modo Claro',
            text_color=text_color if not is_dark else theme_colors['text_secondary']
        )
        self.theme_switch.configure(
            button_color='#4a5a8a' if not is_dark else theme_colors['surface_light'],
            button_hover_color='#6a7aa0' if not is_dark else theme_colors['border'],
            fg_color='#6a7aa0' if not is_dark else theme_colors['border']
        )
        self.theme_separator_top.configure(fg_color=border_color)
        self.theme_separator_bottom.configure(fg_color=border_color)

        # Actualizar footer
        self.footer_separator.configure(fg_color=border_color)
        self.version_label.configure(text_color=text_secondary_color)
        self.copyright_label.configure(text_color=text_secondary_color)
