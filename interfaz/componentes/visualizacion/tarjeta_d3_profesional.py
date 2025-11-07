"""
Componente ProfessionalD3ChartCard - Gráficos D3.js embebidos profesionalmente
Solución robusta con múltiples fallbacks para garantizar visualización
"""
import customtkinter as ctk
from tkinter import Frame, Text, Scrollbar
import tempfile
import os
import webbrowser
from nucleo.configuracion.gestor_temas import get_theme_manager
from nucleo.configuracion.ajustes import HUTCHISON_COLORS
from nucleo.servicios.motor_templates_d3 import MotorTemplatesD3

# Intentar importar tkhtmlview (más estable que tkinterweb)
try:
    from tkhtmlview import HTMLScrolledText
    HTML_RENDERER = 'tkhtmlview'
except ImportError:
    HTML_RENDERER = None

# Si tkhtmlview falla, intentar tkinterweb
if HTML_RENDERER is None:
    try:
        from tkinterweb import HtmlFrame
        HTML_RENDERER = 'tkinterweb'
    except ImportError:
        HTML_RENDERER = None


class ProfessionalD3ChartCard(ctk.CTkFrame):
    """Card con gráficos D3.js embebidos profesionalmente - SOLUCIÓN ROBUSTA"""

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
        self.current_html = None

        # Header
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

            # Badge D3.js + botón abrir en navegador
            btn_frame = ctk.CTkFrame(header, fg_color='transparent')
            btn_frame.pack(side='right')

            badge = ctk.CTkLabel(
                btn_frame,
                text='D3.js',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=50,
                height=24
            )
            badge.pack(side='left', padx=5)

            self.open_btn = ctk.CTkButton(
                btn_frame,
                text='🔗',
                font=('Montserrat', 12, 'bold'),
                fg_color=HUTCHISON_COLORS['success'],
                hover_color='#41a755',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._open_in_browser
            )
            self.open_btn.pack(side='left', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_d3_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer gráfico D3.js embebido

        Args:
            chart_type: Tipo de gráfico ('bar', 'donut', 'line')
            datos: Diccionario con datos del gráfico
            subtitulo: Subtítulo del gráfico
        """
        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML según tipo
        if chart_type == 'bar':
            html = self.motor_d3.generar_grafico_barras(
                titulo='',
                datos=datos,
                subtitulo=subtitulo,
                tema=tema,
                interactivo=True
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
            self._show_error("Tipo de gráfico no soportado")
            return

        self.current_html = html

        # Intentar renderizar con el mejor método disponible
        if HTML_RENDERER == 'tkhtmlview':
            self._render_with_tkhtmlview(html)
        elif HTML_RENDERER == 'tkinterweb':
            self._render_with_tkinterweb(html)
        else:
            # Fallback: Mostrar preview con opción de abrir en navegador
            self._show_preview_mode(chart_type, datos)

    def _render_with_tkhtmlview(self, html):
        """Renderizar con tkhtmlview (más estable)"""
        try:
            html_container = Frame(self.chart_container, bg=self.chart_container._fg_color)
            html_container.pack(fill='both', expand=True, padx=5, pady=5)

            self.html_widget = HTMLScrolledText(
                html_container,
                html=html,
                wrap='none'
            )
            self.html_widget.pack(fill='both', expand=True)
        except Exception as e:
            print(f"Error con tkhtmlview: {e}")
            self._show_preview_mode('bar', {})

    def _render_with_tkinterweb(self, html):
        """Renderizar con tkinterweb"""
        try:
            html_container = Frame(self.chart_container, bg=self.chart_container._fg_color)
            html_container.pack(fill='both', expand=True, padx=5, pady=5)

            self.html_widget = HtmlFrame(
                html_container,
                messages_enabled=False,
                vertical_scrollbar=False,
                horizontal_scrollbar=False
            )
            self.html_widget.load_html(html)
            self.html_widget.pack(fill='both', expand=True)
        except Exception as e:
            print(f"Error con tkinterweb: {e}")
            self._show_preview_mode('bar', {})

    def _show_preview_mode(self, chart_type, datos):
        """Mostrar modo preview con datos y botón para abrir en navegador"""
        theme = self.theme_manager.get_current_theme()

        preview_frame = ctk.CTkFrame(self.chart_container, fg_color='transparent')
        preview_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Icono
        icon_map = {'bar': '📊', 'donut': '🍩', 'line': '📈'}
        icon = ctk.CTkLabel(
            preview_frame,
            text=icon_map.get(chart_type, '📊'),
            font=('Montserrat', 64)
        )
        icon.pack(pady=(20, 15))

        # Título
        title = ctk.CTkLabel(
            preview_frame,
            text=f'Gráfico D3.js {chart_type.upper()}',
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text']
        )
        title.pack(pady=10)

        # Mostrar datos
        if 'labels' in datos and 'values' in datos:
            data_text = "Datos:\n"
            for label, value in zip(datos['labels'][:5], datos['values'][:5]):
                data_text += f"• {label}: {value}\n"
            if len(datos['labels']) > 5:
                data_text += f"... y {len(datos['labels']) - 5} más"

            data_label = ctk.CTkLabel(
                preview_frame,
                text=data_text,
                font=('Montserrat', 11),
                text_color=theme['text_secondary'],
                justify='left'
            )
            data_label.pack(pady=15)

        # Botón grande para abrir
        open_btn_big = ctk.CTkButton(
            preview_frame,
            text='🚀 Abrir Gráfico Interactivo en Navegador',
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=50,
            corner_radius=10,
            command=self._open_in_browser
        )
        open_btn_big.pack(pady=20, padx=40, fill='x')

        # Nota
        note = ctk.CTkLabel(
            preview_frame,
            text='💡 Instala "pip install tkhtmlview" para ver gráficos embebidos',
            font=('Montserrat', 9, 'italic'),
            text_color=theme['text_secondary']
        )
        note.pack(pady=(10, 20))

    def _open_in_browser(self):
        """Abrir gráfico en navegador"""
        if not self.current_html:
            return

        try:
            # Guardar HTML en archivo temporal
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.html',
                delete=False,
                encoding='utf-8'
            )
            temp_file.write(self.current_html)
            temp_file.close()

            # Abrir en navegador
            webbrowser.open('file://' + temp_file.name)
        except Exception as e:
            print(f"Error abriendo en navegador: {e}")

    def _show_error(self, message):
        """Mostrar mensaje de error"""
        theme = self.theme_manager.get_current_theme()
        error_label = ctk.CTkLabel(
            self.chart_container,
            text=f'❌ {message}',
            font=('Montserrat', 12),
            text_color='#ff6b6b'
        )
        error_label.pack(expand=True, pady=20)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.html_widget = None
        self.current_html = None
