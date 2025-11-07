"""
Componente EmbeddedD3ChartCard - Card con gráficos D3.js embebidos nativamente
Embebe HTML/D3.js directamente dentro de la aplicación de escritorio
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import os
from nucleo.configuracion.gestor_temas import get_theme_manager
from nucleo.configuracion.ajustes import HUTCHISON_COLORS
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3

# Intentar importar tkinterweb (HTML widget nativo)
try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False
    print("⚠️  tkinterweb no disponible. Instalando...")


class EmbeddedD3ChartCard(ctk.CTkFrame):
    """Card con gráficos D3.js embebidos DENTRO de la aplicación"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            width: Ancho del card
            height: Altura del card
        """
        # Obtener tema actual
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border'],
            **kwargs
        )

        self._title = title
        self._width = width
        self._height = height
        self.motor_d3 = MotorTemplatesD3()
        self.html_widget = None

        # Header si hay título
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            self.title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Montserrat', 16, 'bold'),
                text_color=theme['text'],
                anchor='w'
            )
            self.title_label.pack(side='left', fill='x', expand=True)

            # Indicador D3.js
            badge = ctk.CTkLabel(
                header,
                text='D3.js',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=60,
                height=24
            )
            badge.pack(side='right', padx=5)

        # Container para el gráfico D3.js embebido
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Verificar disponibilidad de tkinterweb
        if not TKINTERWEB_AVAILABLE:
            self._show_installation_message()

    def _show_installation_message(self):
        """Mostrar mensaje de instalación si tkinterweb no está disponible"""
        msg_frame = ctk.CTkFrame(self.chart_container, fg_color='transparent')
        msg_frame.pack(fill='both', expand=True, padx=20, pady=20)

        theme = self.theme_manager.get_current_theme()

        icon = ctk.CTkLabel(
            msg_frame,
            text='📦',
            font=('Montserrat', 48)
        )
        icon.pack(pady=(20, 10))

        title = ctk.CTkLabel(
            msg_frame,
            text='Biblioteca Adicional Requerida',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        title.pack(pady=10)

        desc = ctk.CTkLabel(
            msg_frame,
            text='Para ver gráficos D3.js embebidos, instala tkinterweb:\n\npip install tkinterweb',
            font=('Montserrat', 12),
            text_color=theme['text_secondary'],
            justify='center'
        )
        desc.pack(pady=10)

        note = ctk.CTkLabel(
            msg_frame,
            text='Reinicia la aplicación después de instalar.',
            font=('Montserrat', 10, 'italic'),
            text_color=theme['text_secondary']
        )
        note.pack(pady=(10, 20))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico D3.js embebido

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line')
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico
        """
        if not TKINTERWEB_AVAILABLE:
            return

        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML según tipo
        if chart_type == 'bar':
            html = self.motor_d3.generar_grafico_barras(
                titulo='',  # Sin título (ya está en el header)
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'donut':
            html = self.motor_d3.generar_grafico_donut(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        elif chart_type == 'line':
            html = self.motor_d3.generar_grafico_lineas(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema
            )
        else:
            return

        # Crear widget HTML embebido
        try:
            # Frame regular de tkinter (no CTkFrame) para HtmlFrame
            html_container = Frame(self.chart_container, bg=self.chart_container._fg_color)
            html_container.pack(fill='both', expand=True, padx=5, pady=5)

            # Crear HtmlFrame (widget HTML nativo)
            self.html_widget = HtmlFrame(
                html_container,
                messages_enabled=False,
                vertical_scrollbar=False,
                horizontal_scrollbar=False
            )
            self.html_widget.load_html(html)
            self.html_widget.pack(fill='both', expand=True)

        except Exception as e:
            # Si falla, mostrar mensaje de error
            error_label = ctk.CTkLabel(
                self.chart_container,
                text=f'Error al cargar gráfico D3.js:\n{str(e)}',
                font=('Montserrat', 11),
                text_color='#ff6b6b',
                wraplength=400
            )
            error_label.pack(expand=True, pady=20)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.html_widget = None
