"""
CEFBrowserWindow - Ventana fullscreen con Chromium embebido
Muestra D3.js interactivo funcionando PERFECTAMENTE dentro de la aplicación
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import Frame
import sys
import os

# Importar CEF Python
try:
    from cefpython3 import cefpython as cef
    CEF_AVAILABLE = True
except ImportError:
    CEF_AVAILABLE = False
    print("⚠️ CEF Python no disponible")

from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class CEFBrowserWindow:
    """
    Ventana modal con navegador Chromium embebido

    Características:
    - Chromium REAL embebido en tkinter
    - D3.js funciona 100% con todas sus funcionalidades
    - Animaciones, tooltips, interactividad completa
    - Se ejecuta DENTRO de la aplicación
    """

    def __init__(self, parent, title="Dashboard Fullscreen", url=None):
        """
        Crear ventana CEF Browser

        Args:
            parent: Ventana padre
            title: Título de la ventana
            url: URL a cargar (archivo local o http)
        """
        self.parent = parent
        self.title = title
        self.url = url
        self.browser = None
        self.window = None

        if not CEF_AVAILABLE:
            print("❌ CEF Python no está disponible")
            return

        # Crear ventana modal
        self._create_window()

        # Inicializar CEF
        self._init_cef()

    def _create_window(self):
        """Crear ventana TopLevel"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)

        # Tamaño y posición
        width = 1400
        height = 900

        # Centrar en pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Modal
        self.window.transient(self.parent)
        self.window.grab_set()

        # Header con botón cerrar
        self._create_header()

        # Frame para el navegador
        self.browser_frame = Frame(self.window, bg='white')
        self.browser_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Manejar cierre
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def _create_header(self):
        """Crear header con botón cerrar"""
        header = Frame(self.window, bg=HUTCHISON_COLORS['ports_sea_blue'], height=60)
        header.pack(fill='x', padx=20, pady=(20, 10))
        header.pack_propagate(False)

        # Título
        title_label = tk.Label(
            header,
            text=f"📊 {self.title}",
            font=('Montserrat', 18, 'bold'),
            bg=HUTCHISON_COLORS['ports_sea_blue'],
            fg='white'
        )
        title_label.pack(side='left', padx=20)

        # Botón cerrar
        close_btn = tk.Button(
            header,
            text='✕ Cerrar',
            font=('Montserrat', 12, 'bold'),
            bg='#003D8F',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.close
        )
        close_btn.pack(side='right', padx=20)

        # Hover effect
        def on_enter(e):
            close_btn['bg'] = '#001a3d'

        def on_leave(e):
            close_btn['bg'] = '#003D8F'

        close_btn.bind('<Enter>', on_enter)
        close_btn.bind('<Leave>', on_leave)

    def _init_cef(self):
        """Inicializar CEF Python y cargar URL"""
        if not CEF_AVAILABLE or not self.url:
            return

        try:
            # Configuración CEF
            sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

            # Configurar CEF con settings
            settings = {
                "debug": False,
                "log_severity": cef.LOGSEVERITY_INFO,
                "log_file": "",
            }

            # Inicializar CEF si no está inicializado
            if not cef.GetAppSetting("initialized"):
                cef.Initialize(settings)

            # Información de la ventana
            window_info = cef.WindowInfo()
            window_info.SetAsChild(
                self.browser_frame.winfo_id(),
                [0, 0, self.browser_frame.winfo_width(), self.browser_frame.winfo_height()]
            )

            # Crear navegador
            self.browser = cef.CreateBrowserSync(
                window_info,
                url=self.url
            )

            print(f"✅ CEF Browser creado: {self.url}")

            # Message loop
            self.window.after(10, self._message_loop)

        except Exception as e:
            print(f"❌ Error inicializando CEF: {e}")
            import traceback
            traceback.print_exc()

    def _message_loop(self):
        """Loop de mensajes de CEF"""
        if self.browser and self.window.winfo_exists():
            try:
                cef.MessageLoopWork()
                self.window.after(10, self._message_loop)
            except:
                pass

    def close(self):
        """Cerrar ventana y limpiar CEF"""
        print("🔒 Cerrando CEF Browser Window")

        if self.browser:
            try:
                self.browser.CloseBrowser(True)
                self.browser = None
            except:
                pass

        if self.window:
            try:
                self.window.grab_release()
                self.window.destroy()
            except:
                pass


def open_cef_window(parent, title, url):
    """
    Helper function para abrir ventana CEF fácilmente

    Args:
        parent: Ventana padre
        title: Título del dashboard
        url: URL del D3.js

    Returns:
        CEFBrowserWindow instance
    """
    if not CEF_AVAILABLE:
        print("❌ CEF Python no disponible - abriendo en navegador")
        import webbrowser
        webbrowser.open(url)
        return None

    return CEFBrowserWindow(parent, title=title, url=url)
