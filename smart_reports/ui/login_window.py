"""
Ventana de Login - Hutchison Ports Branding
Pantalla de autenticación con diseño corporativo
"""

import customtkinter as ctk
from tkinter import messagebox
from ..config.settings import HUTCHISON_COLORS, DARK_THEME


class LoginWindow:
    """Ventana de login con diseño Hutchison Ports"""

    def __init__(self, root, on_success_callback):
        """
        Inicializa la ventana de login

        Args:
            root: Ventana raíz de CTk
            on_success_callback: Función a ejecutar cuando el login es exitoso
        """
        self.root = root
        self.on_success_callback = on_success_callback

        # Configurar ventana principal
        self.root.title("HUTCHISON PORTS - Login")
        self.root.geometry("1200x700")

        # Centrar ventana en pantalla
        self.center_window()

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

        # Frame principal (fondo degradado simulado con color sólido)
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=DARK_THEME['background'],
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
            fg_color=DARK_THEME['surface'],
            corner_radius=20,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.login_card.pack(padx=40, pady=40)

        # Contenido de la tarjeta con padding
        content_frame = ctk.CTkFrame(
            self.login_card,
            fg_color='transparent'
        )
        content_frame.pack(padx=60, pady=50)

        # === ICONO/LOGO ===
        icon_label = ctk.CTkLabel(
            content_frame,
            text="⚓",  # Icono de ancla para tema portuario
            font=('Arial', 64),
            text_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        icon_label.pack(pady=(0, 20))

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            content_frame,
            text="HUTCHISON PORTS",
            font=('Montserrat', 32, 'bold'),  # Montserrat Bold
            text_color='white'
        )
        title_label.pack(pady=(0, 5))

        # === SUBTÍTULO ===
        subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Acceso al Sistema",
            font=('Montserrat', 18),  # Montserrat Regular
            text_color=DARK_THEME['text_secondary']
        )
        subtitle_label.pack(pady=(0, 40))

        # === CAMPO USUARIO ===
        user_label = ctk.CTkLabel(
            content_frame,
            text="Usuario",
            font=('Arial', 14),
            text_color=DARK_THEME['text_secondary'],
            anchor='w'
        )
        user_label.pack(fill='x', pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.username_var,
            placeholder_text="Ingrese su usuario",
            font=('Arial', 14),
            height=45,
            width=350,
            border_width=2,
            border_color=DARK_THEME['border'],
            fg_color=DARK_THEME['surface_light'],
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 20))
        self.username_entry.focus()  # Focus inicial en usuario

        # === CAMPO CONTRASEÑA ===
        password_label = ctk.CTkLabel(
            content_frame,
            text="Contraseña",
            font=('Arial', 14),
            text_color=DARK_THEME['text_secondary'],
            anchor='w'
        )
        password_label.pack(fill='x', pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            content_frame,
            textvariable=self.password_var,
            placeholder_text="Ingrese su contraseña",
            show="●",  # Ocultar contraseña
            font=('Arial', 14),
            height=45,
            width=350,
            border_width=2,
            border_color=DARK_THEME['border'],
            fg_color=DARK_THEME['surface_light'],
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
        demo_label = ctk.CTkLabel(
            content_frame,
            text="Demo: Usuario: admin | Contraseña: 1234",
            font=('Arial', 11),
            text_color='#666666'
        )
        demo_label.pack(pady=(10, 0))

        # === FOOTER ===
        footer_label = ctk.CTkLabel(
            content_frame,
            text="Smart Reports v2.0 | Instituto Hutchison Ports",
            font=('Arial', 10),
            text_color='#555555'
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
        VALID_USERS = {
            'admin': '1234',
            'usuario': 'pass',
            'demo': 'demo'
        }

        # Verificar credenciales
        if username in VALID_USERS and VALID_USERS[username] == password:
            # Login exitoso
            self.on_login_success(username)
        else:
            # Login fallido
            messagebox.showerror(
                "Error de Autenticación",
                "Usuario o contraseña incorrectos"
            )
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()

    def on_login_success(self, username):
        """
        Se ejecuta cuando el login es exitoso

        Args:
            username: Nombre de usuario autenticado
        """
        # Destruir frame de login
        self.main_frame.destroy()

        # Llamar al callback con el usuario autenticado
        self.on_success_callback(username)

    def destroy(self):
        """Destruye la ventana de login"""
        self.main_frame.destroy()
