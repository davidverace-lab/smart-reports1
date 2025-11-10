"""
Componente de Tarjeta con Gráfico Matplotlib - SIMPLE Y QUE SIEMPRE FUNCIONA
"""
import customtkinter as ctk
from tkinter import Frame
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class SimpleMatplotlibCard(ctk.CTkFrame):
    """Card con gráfico matplotlib embebido - GARANTIZADO que funciona"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
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

        # Header
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Montserrat', 16, 'bold'),
                text_color=theme['text'],
                anchor='w'
            )
            title_label.pack(side='left', fill='x', expand=True)

            # Badge matplotlib
            badge = ctk.CTkLabel(
                header,
                text='📊 Gráfico',
                font=('Montserrat', 10, 'bold'),
                fg_color=HUTCHISON_COLORS['ports_sky_blue'],
                text_color='white',
                corner_radius=6,
                width=70,
                height=24
            )
            badge.pack(side='right', padx=5)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.canvas = None
        self.current_fig = None

    def set_chart(self, chart_type, datos):
        """
        Establecer gráfico matplotlib

        Args:
            chart_type: 'bar', 'donut', o 'line'
            datos: dict con 'labels' y 'values'
        """
        # Limpiar anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.current_fig:
            matplotlib.pyplot.close(self.current_fig)

        # Tema
        tema = 'dark' if self.theme_manager.is_dark_mode() else 'light'

        # Crear gráfico según tipo
        if chart_type == 'bar':
            self._create_bar_chart(datos, tema)
        elif chart_type == 'donut':
            self._create_donut_chart(datos, tema)
        elif chart_type == 'line':
            self._create_line_chart(datos, tema)

    def _create_bar_chart(self, datos, tema):
        """Crear gráfico de barras"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return

        # Configuración de tema
        if tema == 'dark':
            bg_color = '#2b2d42'
            text_color = '#ffffff'
            grid_color = '#3a3d5c'
        else:
            bg_color = '#ffffff'
            text_color = '#2b2d42'
            grid_color = '#e0e0e0'

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=90)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Colores Hutchison
        paleta = [
            HUTCHISON_COLORS['ports_sky_blue'],
            HUTCHISON_COLORS['ports_horizon_blue'],
            HUTCHISON_COLORS['success'],
            HUTCHISON_COLORS['warning'],
            HUTCHISON_COLORS['danger'],
            '#8B4CFA', '#FF8C42', '#4ECDC4'
        ]
        colors = [paleta[i % len(paleta)] for i in range(len(labels))]

        # Barras
        bars = ax.bar(labels, values, color=colors, alpha=0.9, width=0.6)

        # Valores sobre barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom',
                   fontsize=9, fontweight='bold', color=text_color)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['bottom'].set_color(grid_color)
        ax.tick_params(colors=text_color, labelsize=9)
        ax.set_ylabel('Cantidad', fontsize=10, fontweight='bold', color=text_color)
        ax.grid(axis='y', alpha=0.3, color=grid_color, linestyle='--', linewidth=0.5)

        # Rotar etiquetas si son muchas
        if len(labels) > 5:
            matplotlib.pyplot.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        fig.tight_layout()

        # Embeber en tkinter
        canvas_frame = Frame(self.chart_container, bg=bg_color)
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.current_fig = fig

    def _create_donut_chart(self, datos, tema):
        """Crear gráfico donut"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return

        # Configuración de tema
        if tema == 'dark':
            bg_color = '#2b2d42'
            text_color = '#ffffff'
        else:
            bg_color = '#ffffff'
            text_color = '#2b2d42'

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=90)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Colores
        paleta = [
            HUTCHISON_COLORS['ports_sky_blue'],
            HUTCHISON_COLORS['ports_horizon_blue'],
            HUTCHISON_COLORS['success'],
            HUTCHISON_COLORS['warning'],
            HUTCHISON_COLORS['danger'],
            '#8B4CFA', '#FF8C42', '#4ECDC4'
        ]
        colors = [paleta[i % len(paleta)] for i in range(len(labels))]

        # Donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor=bg_color, linewidth=2),
            textprops={'color': text_color, 'fontsize': 9, 'fontweight': 'bold'}
        )

        # Porcentajes en blanco
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')

        fig.tight_layout()

        # Embeber en tkinter
        canvas_frame = Frame(self.chart_container, bg=bg_color)
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.current_fig = fig

    def _create_line_chart(self, datos, tema):
        """Crear gráfico de líneas"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return

        # Configuración de tema
        if tema == 'dark':
            bg_color = '#2b2d42'
            text_color = '#ffffff'
            grid_color = '#3a3d5c'
        else:
            bg_color = '#ffffff'
            text_color = '#2b2d42'
            grid_color = '#e0e0e0'

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=90)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Línea
        ax.plot(labels, values, color=HUTCHISON_COLORS['ports_sky_blue'],
               linewidth=2, marker='o', markersize=6)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['bottom'].set_color(grid_color)
        ax.tick_params(colors=text_color, labelsize=9)
        ax.grid(alpha=0.3, color=grid_color, linestyle='--', linewidth=0.5)

        fig.tight_layout()

        # Embeber en tkinter
        canvas_frame = Frame(self.chart_container, bg=bg_color)
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.current_fig = fig

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        if self.current_fig:
            matplotlib.pyplot.close(self.current_fig)
        self.canvas = None
        self.current_fig = None
