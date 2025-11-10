"""
Componente OptimizedChartCard - Card con gráficos matplotlib embebidos (optimizado)
Con opción de exportar a D3.js interactivo
"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import tempfile
import webbrowser
import os
from config.themes import get_theme_manager
from config.themes import HUTCHISON_COLORS


class OptimizedChartCard(ctk.CTkFrame):
    """Card con gráficos matplotlib embebidos optimizados + exportación D3.js opcional"""

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

        self.current_fig = None
        self.canvas = None
        self._title = title
        self._width = width
        self._height = height
        self._d3_data = None  # Datos para exportar a D3.js

        # Aplicar configuración de matplotlib según tema (optimizado)
        self._apply_matplotlib_theme()

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

            # Botón pequeño de exportar a D3.js (opcional)
            self.export_btn = ctk.CTkButton(
                header,
                text='🚀 D3.js',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                hover_color=HUTCHISON_COLORS['ports_sea_blue'],
                text_color='white',
                height=28,
                width=70,
                corner_radius=6,
                command=self._export_to_d3
            )
            self.export_btn.pack(side='right')
            self.export_btn.pack_forget()  # Oculto por defecto

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def _apply_matplotlib_theme(self):
        """Aplicar configuración de matplotlib según tema actual (optimizado)"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # Configuración optimizada (menos overhead)
        if is_dark:
            rcParams['figure.facecolor'] = theme['background']
            rcParams['axes.facecolor'] = theme['background']
            rcParams['text.color'] = theme['text_secondary']
            rcParams['axes.labelcolor'] = theme['text_secondary']
            rcParams['xtick.color'] = theme['text_secondary']
            rcParams['ytick.color'] = theme['text_secondary']
        else:
            rcParams['figure.facecolor'] = '#f5f5f5'
            rcParams['axes.facecolor'] = '#ffffff'
            rcParams['text.color'] = theme['text']
            rcParams['axes.labelcolor'] = theme['text']
            rcParams['xtick.color'] = theme['text']
            rcParams['ytick.color'] = theme['text']

    def set_figure(self, fig, d3_data=None):
        """
        Establecer figura de Matplotlib

        Args:
            fig: Figura de Matplotlib (matplotlib.figure.Figure)
            d3_data: Datos opcionales para exportación D3.js {'type': 'bar', 'labels': [...], 'values': [...]}
        """
        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        self.current_fig = fig
        self._d3_data = d3_data

        # Mostrar botón D3.js si hay datos
        if d3_data:
            self.export_btn.pack(side='right')
        else:
            self.export_btn.pack_forget()

        # Crear canvas de matplotlib (optimizado)
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.canvas.draw()

        # Embeber el canvas
        theme = self.theme_manager.get_current_theme()
        canvas_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg=canvas_bg, highlightthickness=0)
        canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)

    def _export_to_d3(self):
        """Exportar gráfico a D3.js interactivo (abre en navegador)"""
        if not self._d3_data:
            return

        from src.infrastructure.visualization.d3_generator import MotorTemplatesD3

        motor = MotorTemplatesD3()
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Generar HTML según tipo de gráfico
        chart_type = self._d3_data.get('type', 'bar')

        if chart_type == 'bar':
            html = motor.generar_grafico_barras(
                titulo=self._title,
                datos={
                    'labels': self._d3_data.get('labels', []),
                    'values': self._d3_data.get('values', [])
                },
                subtitulo=self._d3_data.get('subtitulo', ''),
                tema=tema
            )
        elif chart_type == 'donut':
            html = motor.generar_grafico_donut(
                titulo=self._title,
                datos={
                    'labels': self._d3_data.get('labels', []),
                    'values': self._d3_data.get('values', [])
                },
                subtitulo=self._d3_data.get('subtitulo', ''),
                tema=tema
            )
        elif chart_type == 'line':
            html = motor.generar_grafico_lineas(
                titulo=self._title,
                datos={
                    'x': self._d3_data.get('x', []),
                    'series': self._d3_data.get('series', [])
                },
                subtitulo=self._d3_data.get('subtitulo', ''),
                tema=tema
            )
        else:
            return

        # Guardar HTML en archivo temporal y abrir en navegador
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()

        # Abrir en navegador por defecto
        webbrowser.open('file://' + temp_file.name)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.current_fig:
            plt.close(self.current_fig)
            self.current_fig = None
