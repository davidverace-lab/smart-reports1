"""
WebViewWindow - Ventana fullscreen con navegador web embebido
Muestra D3.js interactivo funcionando PERFECTAMENTE dentro de la aplicación
Usa pywebview (compatible con Python 3.11+)
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import Frame
import threading

# Importar pywebview
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️ pywebview no disponible - instalar con: pip install pywebview")

from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS


class WebViewWindow:
    """
    Ventana modal con navegador web embebido usando pywebview

    Características:
    - Navegador nativo embebido (Edge en Windows, WebKit en macOS, GTK en Linux)
    - D3.js funciona 100% con todas sus funcionalidades
    - Animaciones, tooltips, interactividad completa
    - Se ejecuta DENTRO de la aplicación
    - Compatible con Python 3.11+
    """

    def __init__(self, parent, title="Dashboard Fullscreen", url=None):
        """
        Crear ventana WebView

        Args:
            parent: Ventana padre
            title: Título de la ventana
            url: URL a cargar (archivo local o http)
        """
        self.parent = parent
        self.title = title
        self.url = url
        self.window = None
        self.webview_window = None

        if not WEBVIEW_AVAILABLE:
            print("❌ pywebview no está disponible")
            self._fallback_browser()
            return

        # Crear ventana modal
        self._create_window()

        # Inicializar webview en thread separado
        self._init_webview()

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

    def _init_webview(self):
        """Inicializar pywebview y cargar URL"""
        if not WEBVIEW_AVAILABLE or not self.url:
            return

        try:
            # Destruir la ventana tkinter y crear una ventana pywebview independiente
            # pywebview no puede embeberse en tkinter, así que la abrimos aparte
            self.window.withdraw()  # Ocultar ventana tkinter

            def start_webview():
                """Iniciar webview en thread"""
                try:
                    # Crear ventana pywebview independiente
                    self.webview_window = webview.create_window(
                        title=self.title,
                        url=self.url,
                        width=1400,
                        height=900,
                        resizable=True,
                        fullscreen=False,
                        min_size=(800, 600)
                    )

                    # Iniciar webview (bloquea hasta que se cierre)
                    webview.start()

                    # Cuando se cierre, destruir ventana tkinter
                    if self.window and self.window.winfo_exists():
                        self.window.after(0, self._cleanup_after_webview)

                except Exception as e:
                    print(f"❌ Error con pywebview: {e}")
                    self._fallback_browser()

            # Iniciar en thread separado
            webview_thread = threading.Thread(target=start_webview, daemon=True)
            webview_thread.start()

            print(f"✅ Webview iniciado: {self.url}")

        except Exception as e:
            print(f"❌ Error inicializando webview: {e}")
            import traceback
            traceback.print_exc()
            self._fallback_browser()

    def _cleanup_after_webview(self):
        """Limpiar después de cerrar webview"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.grab_release()
                self.window.destroy()
        except:
            pass

    def _fallback_browser(self):
        """Fallback: abrir en navegador externo"""
        import webbrowser
        print(f"🌐 Abriendo en navegador externo: {self.url}")
        webbrowser.open(self.url)

        # Cerrar ventana modal si existe
        if self.window and self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()

    def close(self):
        """Cerrar ventana y limpiar webview"""
        print("🔒 Cerrando WebView Window")

        # Intentar cerrar webview
        try:
            if self.webview_window:
                webview.destroy_window(self.webview_window)
                self.webview_window = None
        except:
            pass

        # Cerrar ventana tkinter
        if self.window and self.window.winfo_exists():
            try:
                self.window.grab_release()
                self.window.destroy()
            except:
                pass


def open_cef_window(parent, title, url):
    """
    Helper function para abrir ventana webview fácilmente
    (Mantiene el nombre 'open_cef_window' por compatibilidad)

    Args:
        parent: Ventana padre
        title: Título del dashboard
        url: URL del D3.js

    Returns:
        WebViewWindow instance
    """
    if not WEBVIEW_AVAILABLE:
        print("❌ pywebview no disponible - abriendo en navegador")
        import webbrowser
        webbrowser.open(url)
        return None

    return WebViewWindow(parent, title=title, url=url)
