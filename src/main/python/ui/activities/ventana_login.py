"""
Ventana de Login - Hutchison Ports Branding
Pantalla de autenticación con diseño corporativo
"""

import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image

# Android Studio structure imports
from src.main.res.config.themes import HUTCHISON_COLORS, DARK_THEME


class LoginWindow:
    """Ventana de login con diseño Hutchison Ports"""

    def __init__(self, root, on_success_callback, theme_mode='dark'):
        """
        Inicializa la ventana de login

        Args:
            root: Ventana raíz de CTk
            on_success_callback: Función a ejecutar cuando el login es exitoso
            theme_mode: 'dark' o 'light' para el modo de tema
        """
        self.root = root
        self.on_success_callback = on_success_callback
        self.theme_mode = theme_mode

        # Configurar ventana principal
        self.root.title("Instituto Hutchison Ports - Acceso al Sistema")

        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Establecer ventana en pantalla completa
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')  # Maximizar ventana

        # Variables de entrada
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        # Crear UI
        self.create_login_ui()

        # Vincular Enter key al login
        self.root.bind('<Return>', lambda e: self.attempt_login())

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_login_ui(self):
        """Crea la interfaz de usuario del login"""

        # Determinar colores según tema
        if self.theme_mode == 'light':
            bg_color = '#F5F7FA'  # Fondo claro
            card_color = '#FFFFFF'  # Tarjeta blanca
            text_primary = '#002E6D'  # Texto principal oscuro
            text_secondary = '#666666'  # Texto secundario gris
            border_color = HUTCHISON_COLORS['ports_sky_blue']
        else:  # dark
            bg_color = DARK_THEME['background']
            card_color = DARK_THEME['surface']
            text_primary = '#FFFFFF'
            text_secondary = DARK_THEME['text_secondary']
            border_color = HUTCHISON_COLORS['ports_sky_blue']

        # Frame principal
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=bg_color,
            corner_radius=0
        )
        self.main_frame.pack(fill='both', expand=True)

        # Frame central para la tarjeta de login
        center_container = ctk.CTkFrame(
            self.main_frame,
            fg_color='transparent'
        )
        center_container.place(relx=0.5, rely=0.5, anchor='center')

        # Tarjeta de login (card)
        self.login_card = ctk.CTkFrame(
            center_container,
            fg_color=card_color,
            corner_radius=20,
            border_width=2,
            border_color=border_color
        )
        self.login_card.pack(padx=40, pady=40)

        # Contenido de la tarjeta con padding
        content_frame = ctk.CTkFrame(
            self.login_card,
            fg_color='transparent'
        )
        content_frame.pack(padx=60, pady=50)

        # === TEXTO SUPERIOR: ACCESO AL SISTEMA ===
        access_label = ctk.CTkLabel(
            content_frame,
            text="ACCESO AL SISTEMA",
            font=('Montserrat', 16, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        access_label.pack(pady=(0, 20))

        # === ICONO/LOGO ===
        # Intentar cargar logo desde rutas conocidas
        logo_paths = [
            'tests/logo.png',
            'tests/integration/logo.png',
            'assets/logo.png',
            'assets/images/logo.png'
        ]

        logo_loaded = False
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    # Cargar y redimensionar imagen
                    pil_image = Image.open(logo_path)
                    pil_image = pil_image.resize((120, 120), Image.Resampling.LANCZOS)
                    logo_image = ctk.CTkImage(
                        light_image=pil_image,
                        dark_image=pil_image,
                        size=(120, 120)
                    )

                    logo_label = ctk.CTkLabel(
                        content_frame,
                        image=logo_image,
                        text=""
                    )
                    logo_label.pack(pady=(0, 20))
                    logo_loaded = True
                    break
                except Exception as e:
                    print(f"Error cargando logo desde {logo_path}: {e}")

        # Si no se cargó logo, usar icono de texto
        if not logo_loaded:
            icon_label = ctk.CTkLabel(
                content_frame,
                text="⚓",  # Icono de ancla para tema portuario
                font=('Montserrat', 64),
                text_color=HUTCHISON_COLORS['ports_sky_blue']
            )
            icon_label.pack(pady=(0, 20))

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            content_frame,
            text="INSTITUTO HUTCHISON PORTS",
            font=('Montserrat', 28, 'bold'),
            text_color=text_primary
        )
        title_label.pack(pady=(0, 5))

        # === SUBTÍTULO ===
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Sistema de Gestión de Capacitación",
            font=('Montserrat', 14),
            text_color=text_secondary
        )
        subtitle_label.pack(pady=(0, 40))

        # === CAMPO USUARIO ===
        user_label = ctk.CTkLabel(
            content_frame,
            text="Usuario",
            font=('Montserrat', 14),
            text_color=text_secondary,
            anchor='w'
        )
        user_label.pack(fill='x', pady=(0, 5))

        # Colores de entrada según tema
        if self.theme_mode == 'light':
            entry_fg = '#F8F9FA'
            entry_border = '#CCCCCC'
            entry_text = '#002E6D'
        else:
            entry_fg = DARK_THEME['surface_light']
            entry_border = DARK_THEME['border']
            entry_text = '#FFFFFF'

        self.username_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.username_var,
            placeholder_text="Ingrese su usuario",
            font=('Montserrat', 14),
            height=45,
            width=350,
            border_width=2,
            border_color=entry_border,
            fg_color=entry_fg,
            text_color=entry_text,
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 20))
        self.username_entry.focus()  # Focus inicial en usuario

        # === CAMPO CONTRASEÑA ===
        password_label = ctk.CTkLabel(
            content_frame,
            text="Contraseña",
            font=('Montserrat', 14),
            text_color=text_secondary,
            anchor='w'
        )
        password_label.pack(fill='x', pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.password_var,
            placeholder_text="Ingrese su contraseña",
            show="●",  # Ocultar contraseña
            font=('Montserrat', 14),
            height=45,
            width=350,
            border_width=2,
            border_color=entry_border,
            fg_color=entry_fg,
            text_color=entry_text,
            corner_radius=10
        )
        self.password_entry.pack(pady=(0, 30))

        # === BOTÓN ACCEDER ===
        self.login_button = ctk.CTkButton(
            content_frame,
            text="Acceder",
            font=('Montserrat', 16, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=50,
            width=350,
            corner_radius=10,
            command=self.attempt_login
        )
        self.login_button.pack(pady=(0, 25))

        # === TEXTO DEMO ===
        demo_color = '#888888' if self.theme_mode == 'light' else '#666666'
        demo_label = ctk.CTkLabel(
            content_frame,
            text="Demo: Usuario: admin | Contraseña: 1234",
            font=('Montserrat', 11),
            text_color=demo_color
        )
        demo_label.pack(pady=(10, 0))

        # === FOOTER ===
        footer_color = '#999999' if self.theme_mode == 'light' else '#555555'
        footer_label = ctk.CTkLabel(
            content_frame,
            text="Smart Reports v2.0 | Instituto Hutchison Ports",
            font=('Montserrat', 10),
            text_color=footer_color
        )
        footer_label.pack(pady=(20, 0))

    def attempt_login(self):
        """
        Intenta autenticar al usuario

        Por ahora usa credenciales hardcodeadas.
        TODO: Integrar con base de datos de usuarios
        """
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        # Validar campos vacíos
        if not username or not password:
            messagebox.showerror(
                "Error de Autenticación",
                "Por favor, ingrese usuario y contraseña"
            )
            return

        # Credenciales demo (sin base de datos)
        # TODO: Reemplazar con consulta a BD
        # Usuarios válidos con sus contraseñas y roles
        VALID_USERS = {
            'admin': {'password': '1234', 'role': 'Administrador'},
            'usuario': {'password': 'pass', 'role': 'Usuario'},
            'demo': {'password': 'demo', 'role': 'Demo'}
        }

        # Verificar credenciales
        if username in VALID_USERS and VALID_USERS[username]['password'] == password:
            # Login exitoso - obtener el rol del usuario
            user_role = VALID_USERS[username]['role']
            self.on_login_success(username, user_role)
        else:
            # Login fallido
            messagebox.showerror(
                "Error de Autenticación",
                "Usuario o contraseña incorrectos"
            )
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()

    def on_login_success(self, username, role):
        """
        Se ejecuta cuando el login es exitoso

        Args:
            username: Nombre de usuario autenticado
            role: Rol del usuario (Administrador, Usuario, Demo)
        """
        # Destruir frame de login
        self.main_frame.destroy()

        # Llamar al callback con el usuario autenticado y su rol
        self.on_success_callback(username, role)

    def destroy(self):
        """Destruye la ventana de login"""
        self.main_frame.destroy()
