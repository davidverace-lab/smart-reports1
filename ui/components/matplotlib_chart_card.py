"""
Componente MatplotlibChartCard - Card con gráficos Matplotlib embebidos
"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
from smart_reports.config.theme_manager import get_theme_manager


class MatplotlibChartCard(ctk.CTkFrame):
    """Card con gráficos Matplotlib embebidos"""

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

        # Aplicar configuración de matplotlib según tema
        self._apply_matplotlib_theme()

        # Header si hay título
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            self.title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Segoe UI', 16, 'bold'),
                text_color=theme['text'],
                anchor='w'
            )
            self.title_label.pack(side='left', fill='x', expand=True)

        # Container para el gráfico
        chart_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.chart_container = ctk.CTkFrame(self, fg_color=chart_bg, corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def _apply_matplotlib_theme(self):
        """Aplicar configuración de matplotlib según tema actual"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        if is_dark:
            # Tema oscuro
            rcParams['figure.facecolor'] = theme['background']
            rcParams['axes.facecolor'] = theme['background']
            rcParams['axes.edgecolor'] = theme['border']
            rcParams['axes.labelcolor'] = theme['text_secondary']
            rcParams['text.color'] = theme['text_secondary']
            rcParams['xtick.color'] = theme['text_secondary']
            rcParams['ytick.color'] = theme['text_secondary']
            rcParams['grid.color'] = theme['border']
            rcParams['grid.alpha'] = 0.3
            rcParams['legend.facecolor'] = theme['surface']
            rcParams['legend.edgecolor'] = theme['border']
        else:
            # Tema claro
            rcParams['figure.facecolor'] = '#f5f5f5'
            rcParams['axes.facecolor'] = '#ffffff'
            rcParams['axes.edgecolor'] = theme['border']
            rcParams['axes.labelcolor'] = theme['text']
            rcParams['text.color'] = theme['text']
            rcParams['xtick.color'] = theme['text']
            rcParams['ytick.color'] = theme['text']
            rcParams['grid.color'] = theme['border']
            rcParams['grid.alpha'] = 0.2
            rcParams['legend.facecolor'] = '#ffffff'
            rcParams['legend.edgecolor'] = theme['border']

    def set_figure(self, fig):
        """
        Establecer figura de Matplotlib

        Args:
            fig: Figura de Matplotlib (matplotlib.figure.Figure)
        """
        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        self.current_fig = fig

        # Crear canvas de matplotlib
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.canvas.draw()

        # Embebed el canvas en el container
        theme = self.theme_manager.get_current_theme()
        canvas_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg=canvas_bg, highlightthickness=0)
        canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)

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
