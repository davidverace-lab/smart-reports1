"""
MatplotlibChartCard - Preview estático para dashboards
Usa Matplotlib embebido en tkinter - 100% confiable
"""
import customtkinter as ctk
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS


class MatplotlibChartCard(ctk.CTkFrame):
    """
    Tarjeta con gráfico Matplotlib estático

    Características:
    - Renderizado 100% confiable dentro de la app
    - Gráficos estáticos profesionales
    - Colores Hutchison personalizados
    - Botones para fullscreen (D3.js interactivo) y navegador
    """

    def __init__(self, parent, title='', width=500, height=400, on_fullscreen=None, **kwargs):
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
        self.on_fullscreen = on_fullscreen

        # Estado
        self.chart_type = None
        self.chart_data = None
        self.chart_subtitle = None
        self.chart_url = None  # URL del D3.js para fullscreen

        # Crear UI
        self._create_header()
        self._create_content_area()

    def _create_header(self):
        """Crear header del card"""
        if not self._title:
            return

        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=self._title,
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)

        # Badges
        badge_frame = ctk.CTkFrame(header, fg_color='transparent')
        badge_frame.pack(side='right')

        # Badge Matplotlib
        matplotlib_badge = ctk.CTkLabel(
            badge_frame,
            text='Matplotlib',
            font=('Montserrat', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            text_color='white',
            corner_radius=6,
            width=90,
            height=24
        )
        matplotlib_badge.pack(side='left', padx=5)

        # Botón fullscreen (D3.js interactivo)
        if self.on_fullscreen:
            fullscreen_btn = ctk.CTkButton(
                badge_frame,
                text='⛶',
                font=('Montserrat', 14, 'bold'),
                fg_color=HUTCHISON_COLORS['aqua_green'],
                hover_color='#00b386',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._trigger_fullscreen
            )
            fullscreen_btn.pack(side='left', padx=5)

        # Botón navegador
        browser_btn = ctk.CTkButton(
            badge_frame,
            text='🌐',
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=6,
            width=35,
            height=28,
            command=self._open_in_browser
        )
        browser_btn.pack(side='left', padx=5)

    def _create_content_area(self):
        """Crear área de contenido para matplotlib"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['background'] if is_dark else '#f8f9fa',
            corner_radius=10
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_chart(self, chart_type, datos, subtitulo='', d3_url=None):
        """
        Establecer gráfico

        Args:
            chart_type: 'bar', 'donut', 'line', 'area'
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            d3_url: URL del D3.js para fullscreen/navegador
        """
        # Guardar datos
        self.chart_type = chart_type
        self.chart_data = datos
        self.chart_subtitle = subtitulo
        self.chart_url = d3_url

        # Limpiar contenido anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Crear figura matplotlib
        is_dark = self.theme_manager.is_dark_mode()

        # Configurar estilo
        if is_dark:
            plt.style.use('dark_background')
            fig_color = '#1e1e1e'
            text_color = '#ffffff'
        else:
            plt.style.use('default')
            fig_color = '#f8f9fa'
            text_color = '#000000'

        # Crear figura
        fig = Figure(figsize=(self._width/100, self._height/100), dpi=100, facecolor=fig_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(fig_color)

        # Generar gráfico según tipo
        if chart_type == 'bar':
            self._create_bar_chart(ax, datos, text_color)
        elif chart_type == 'donut':
            self._create_donut_chart(ax, datos, text_color)
        elif chart_type == 'line':
            self._create_line_chart(ax, datos, text_color)
        elif chart_type == 'area':
            self._create_area_chart(ax, datos, text_color)

        # Ajustar layout
        fig.tight_layout()

        # Embeber en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.content_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

        print(f"✅ Matplotlib {chart_type} renderizado")

    def _create_bar_chart(self, ax, datos, text_color):
        """Crear gráfico de barras"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear barras con color Hutchison
        bars = ax.barh(labels, values, color=HUTCHISON_COLORS['ports_sea_blue'])

        # Agregar valores en las barras
        for i, (bar, value) in enumerate(zip(bars, values)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f' {value:,}',
                   ha='left', va='center',
                   color=text_color, fontsize=9)

        # Estilo
        ax.set_xlabel('Cantidad', color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _create_donut_chart(self, ax, datos, text_color):
        """Crear gráfico de dona"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Colores Hutchison
        colors = [
            HUTCHISON_COLORS['ports_sea_blue'],
            HUTCHISON_COLORS['ports_sky_blue'],
            HUTCHISON_COLORS['aqua_green'],
            HUTCHISON_COLORS['ports_horizon_blue'],
            '#ffa94d',
            '#51cf66'
        ]

        # Extender colores si es necesario
        while len(colors) < len(values):
            colors.extend(colors)
        colors = colors[:len(values)]

        # Crear dona
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90,
            textprops={'color': text_color, 'fontsize': 9},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        # Hacer dona (círculo en el centro)
        centre_circle = plt.Circle((0, 0), 0.70, fc=ax.get_facecolor(), linewidth=0)
        ax.add_artist(centre_circle)

        ax.axis('equal')

    def _create_line_chart(self, ax, datos, text_color):
        """Crear gráfico de líneas"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear línea
        x = np.arange(len(labels))
        ax.plot(x, values, color=HUTCHISON_COLORS['ports_sky_blue'],
               linewidth=2.5, marker='o', markersize=6,
               markerfacecolor=HUTCHISON_COLORS['ports_sea_blue'],
               markeredgecolor='white', markeredgewidth=1.5)

        # Etiquetas
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', color=text_color, fontsize=9)
        ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        # Estilo
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _create_area_chart(self, ax, datos, text_color):
        """Crear gráfico de área"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear área
        x = np.arange(len(labels))
        ax.fill_between(x, values, alpha=0.4, color=HUTCHISON_COLORS['ports_sky_blue'])
        ax.plot(x, values, color=HUTCHISON_COLORS['ports_sea_blue'],
               linewidth=2.5, marker='o', markersize=6,
               markerfacecolor=HUTCHISON_COLORS['ports_sea_blue'],
               markeredgecolor='white', markeredgewidth=1.5)

        # Etiquetas
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', color=text_color, fontsize=9)
        ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        # Estilo
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _trigger_fullscreen(self):
        """Activar modo fullscreen con D3.js interactivo"""
        if self.on_fullscreen and self.chart_url:
            self.on_fullscreen(
                title=self._title,
                chart_type=self.chart_type,
                data=self.chart_data,
                subtitle=self.chart_subtitle,
                url=self.chart_url
            )
            print(f"  ⛶ Activando fullscreen CEF para: {self._title}")

    def _open_in_browser(self):
        """Abrir gráfico D3.js en navegador"""
        if not self.chart_url:
            return

        try:
            import webbrowser
            webbrowser.open(self.chart_url)
            print(f"  🌐 Abierto en navegador: {self.chart_url}")
        except Exception as e:
            print(f"  ❌ Error abriendo navegador: {e}")

    def clear(self):
        """Limpiar gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.chart_url = None
        self.chart_data = None
