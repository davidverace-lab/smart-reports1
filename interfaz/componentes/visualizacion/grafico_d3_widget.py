"""
Widget para Gráficos D3.js Interactivos
Embebe HTML/JS en ventanas nativas usando PyWebView
"""

import webview
from threading import Thread
from typing import Dict, Any, Optional, Callable
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3
from nucleo.configuracion.gestor_temas import get_theme_manager


class GraficoD3Widget:
    """
    Widget escalable para mostrar gráficos D3.js interactivos

    Características:
    - Embebe HTML/JS en ventanas nativas (sin navegador externo)
    - Soporte para múltiples tipos de gráficos
    - Comunicación bidireccional Python ↔ JavaScript
    - Temas dinámicos (dark/light)
    - Exportación de imágenes
    - Altamente personalizable
    """

    def __init__(
        self,
        width: int = 1200,
        height: int = 800,
        resizable: bool = True,
        on_close: Optional[Callable] = None
    ):
        """
        Inicializar widget

        Args:
            width: Ancho de la ventana
            height: Alto de la ventana
            resizable: Si la ventana es redimensionable
            on_close: Callback al cerrar ventana
        """
        self.width = width
        self.height = height
        self.resizable = resizable
        self.on_close = on_close
        self.window = None
        self.motor = MotorTemplatesD3()
        self.theme_manager = get_theme_manager()

    def crear_grafico_barras(
        self,
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        modal: bool = False
    ):
        """
        Crear gráfico de barras interactivo

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            modal: Si la ventana es modal (bloquea aplicación principal)

        Ejemplo:
            ```python
            widget = GraficoD3Widget()
            widget.crear_grafico_barras(
                titulo="Progreso por Módulo",
                datos={
                    'labels': ['M1', 'M2', 'M3', 'M4'],
                    'values': [85, 92, 78, 95]
                },
                subtitulo="Capacitación Instituto 2024"
            )
            ```
        """
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'
        html = self.motor.generar_grafico_barras(titulo, datos, subtitulo, tema)
        self._mostrar_ventana(titulo, html, modal)

    def crear_grafico_donut(
        self,
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        modal: bool = False
    ):
        """
        Crear gráfico de donut interactivo

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            modal: Si la ventana es modal

        Ejemplo:
            ```python
            widget = GraficoD3Widget()
            widget.crear_grafico_donut(
                titulo="Distribución por Nivel de Mando",
                datos={
                    'labels': ['Gerenciales', 'Medios', 'Operativos'],
                    'values': [15, 30, 55]
                }
            )
            ```
        """
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'
        html = self.motor.generar_grafico_donut(titulo, datos, subtitulo, tema)
        self._mostrar_ventana(titulo, html, modal)

    def crear_grafico_lineas(
        self,
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        modal: bool = False
    ):
        """
        Crear gráfico de líneas interactivo (múltiples series)

        Args:
            titulo: Título del gráfico
            datos: {
                'labels': [...],
                'series': [
                    {'name': 'Serie 1', 'values': [...]},
                    {'name': 'Serie 2', 'values': [...]}
                ]
            }
            subtitulo: Subtítulo opcional
            modal: Si la ventana es modal

        Ejemplo:
            ```python
            widget = GraficoD3Widget()
            widget.crear_grafico_lineas(
                titulo="Evolución Mensual",
                datos={
                    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                    'series': [
                        {
                            'name': 'Completados',
                            'values': [45, 52, 61, 70, 82, 95]
                        },
                        {
                            'name': 'En Proceso',
                            'values': [30, 28, 25, 20, 15, 10]
                        }
                    ]
                }
            )
            ```
        """
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'
        html = self.motor.generar_grafico_lineas(titulo, datos, subtitulo, tema)
        self._mostrar_ventana(titulo, html, modal)

    def crear_grafico_html(
        self,
        titulo: str,
        html: str,
        modal: bool = False
    ):
        """
        Crear gráfico desde HTML personalizado

        Args:
            titulo: Título de la ventana
            html: HTML completo con D3.js embebido
            modal: Si la ventana es modal

        Ejemplo:
            ```python
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://d3js.org/d3.v7.min.js"></script>
            </head>
            <body>
                <!-- Tu código D3.js aquí -->
            </body>
            </html>
            '''

            widget = GraficoD3Widget()
            widget.crear_grafico_html("Mi Gráfico", html)
            ```
        """
        self._mostrar_ventana(titulo, html, modal)

    def _mostrar_ventana(self, titulo: str, html: str, modal: bool = False):
        """
        Mostrar ventana PyWebView con el HTML

        Args:
            titulo: Título de la ventana
            html: HTML completo
            modal: Si es modal (bloquea app principal)
        """
        def run():
            self.window = webview.create_window(
                title=titulo,
                html=html,
                width=self.width,
                height=self.height,
                resizable=self.resizable,
                background_color='#1a1d2e',
                on_top=modal,
                confirm_close=False
            )

            # Agregar callback de cierre si existe
            if self.on_close:
                webview.start(http_server=True)
                self.on_close()
            else:
                webview.start(http_server=True)

        # Ejecutar en thread separado
        thread = Thread(target=run, daemon=True)
        thread.start()

    def cerrar(self):
        """Cerrar la ventana actual"""
        if self.window:
            self.window.destroy()


class APIGrafico:
    """
    API para comunicación bidireccional Python ↔ JavaScript

    Permite llamar funciones Python desde JavaScript y viceversa
    """

    def __init__(self):
        self.callbacks = {}

    def registrar_callback(self, nombre: str, funcion: Callable):
        """
        Registrar función Python callable desde JS

        Args:
            nombre: Nombre de la función (accesible desde JS)
            funcion: Función Python a ejecutar

        Ejemplo:
            ```python
            def on_click_punto(x, y, valor):
                print(f"Clickeaste en ({x}, {y}) con valor {valor}")

            api = APIGrafico()
            api.registrar_callback('onClickPunto', on_click_punto)
            ```

            Desde JS:
            ```javascript
            // Llamar función Python desde JavaScript
            pywebview.api.onClickPunto(10, 20, 50);
            ```
        """
        self.callbacks[nombre] = funcion

    def ejecutar(self, nombre: str, *args, **kwargs):
        """Ejecutar callback registrado"""
        if nombre in self.callbacks:
            return self.callbacks[nombre](*args, **kwargs)
        else:
            raise ValueError(f"Callback '{nombre}' no registrado")


# Ejemplo de uso rápido
if __name__ == "__main__":
    import customtkinter as ctk

    def demo():
        """Demostración de uso"""

        # Crear ventana principal
        root = ctk.CTk()
        root.title("Demo Gráficos D3.js")
        root.geometry("400x300")

        # Frame principal
        frame = ctk.CTkFrame(root)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        titulo = ctk.CTkLabel(
            frame,
            text="🎨 Gráficos D3.js Interactivos",
            font=('Montserrat', 24, 'bold')
        )
        titulo.pack(pady=20)

        # Botones de ejemplo
        def mostrar_barras():
            widget = GraficoD3Widget(width=1200, height=700)
            widget.crear_grafico_barras(
                titulo="Progreso por Módulo",
                datos={
                    'labels': ['Módulo 1', 'Módulo 2', 'Módulo 3', 'Módulo 4',
                              'Módulo 5', 'Módulo 6', 'Módulo 7', 'Módulo 8'],
                    'values': [85, 92, 78, 95, 88, 91, 76, 89]
                },
                subtitulo="Capacitación Instituto Hutchison Ports 2024"
            )

        def mostrar_donut():
            widget = GraficoD3Widget(width=1000, height=700)
            widget.crear_grafico_donut(
                titulo="Distribución por Nivel de Mando",
                datos={
                    'labels': ['Mandos Gerenciales', 'Mandos Medios',
                              'Mandos Administrativos Operativos'],
                    'values': [45, 120, 235]
                },
                subtitulo="Total de usuarios por categoría"
            )

        def mostrar_lineas():
            widget = GraficoD3Widget(width=1200, height=700)
            widget.crear_grafico_lineas(
                titulo="Evolución de Capacitaciones",
                datos={
                    'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                    'series': [
                        {
                            'name': 'Completados',
                            'values': [45, 52, 61, 70, 82, 95]
                        },
                        {
                            'name': 'En Proceso',
                            'values': [30, 28, 25, 20, 15, 10]
                        },
                        {
                            'name': 'Registrados',
                            'values': [25, 30, 32, 35, 40, 45]
                        }
                    ]
                },
                subtitulo="Progreso mensual 2024"
            )

        btn1 = ctk.CTkButton(
            frame,
            text="📊 Ver Gráfico de Barras",
            font=('Montserrat', 14, 'bold'),
            height=50,
            command=mostrar_barras
        )
        btn1.pack(pady=10, fill='x')

        btn2 = ctk.CTkButton(
            frame,
            text="🍩 Ver Gráfico Donut",
            font=('Montserrat', 14, 'bold'),
            height=50,
            command=mostrar_donut
        )
        btn2.pack(pady=10, fill='x')

        btn3 = ctk.CTkButton(
            frame,
            text="📈 Ver Gráfico de Líneas",
            font=('Montserrat', 14, 'bold'),
            height=50,
            command=mostrar_lineas
        )
        btn3.pack(pady=10, fill='x')

        root.mainloop()

    demo()
