"""
Panel de gráficos interactivos usando Matplotlib con NavigationToolbar
"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
from config.settings import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from config.theme_manager import get_theme_manager


class MatplotlibInteractivePanel(ctk.CTkFrame):
    """Panel con gráficos interactivos de Matplotlib"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
        """
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(parent, fg_color='transparent', **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Crear header
        self._create_header()

        # Crear scroll frame para gráficos
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))

        # Cargar gráficos
        self.after(100, self.create_interactive_charts)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text='📊 Dashboards Interactivos',
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(side='left', pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text='Usa las herramientas para hacer zoom, pan y explorar los datos',
            font=('Arial', 13),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(side='left', padx=(20, 0))

    def create_interactive_charts(self):
        """Crear gráficos interactivos con matplotlib"""
        theme = self.theme_manager.get_current_theme()

        # Configurar estilo de matplotlib para el tema actual
        is_dark = self.theme_manager.is_dark_mode()
        if is_dark:
            plt.style.use('dark_background')
            text_color = '#FFFFFF'
            bg_color = theme['surface']
        else:
            plt.style.use('default')
            text_color = theme['text']
            bg_color = '#FFFFFF'

        # === GRÁFICO 1: Líneas Interactivas ===
        self._create_chart_container(
            "Tendencias de Progreso por Módulo",
            "Arrastra para hacer zoom, usa los botones de la barra de herramientas",
            self._create_line_chart,
            bg_color
        )

        # === GRÁFICO 2: Barras Apiladas ===
        self._create_chart_container(
            "Distribución por Estado y Módulo",
            "Haz clic en las leyendas para ocultar/mostrar series",
            self._create_stacked_bar_chart,
            bg_color
        )

        # === GRÁFICO 3: Scatter Interactivo ===
        self._create_chart_container(
            "Análisis de Correlación - Progreso vs Tiempo",
            "Haz zoom en áreas específicas para análisis detallado",
            self._create_scatter_chart,
            bg_color
        )

        # === GRÁFICO 4: Heatmap ===
        self._create_chart_container(
            "Mapa de Calor - Actividad por Unidad y Módulo",
            "Visualiza patrones de actividad por colores",
            self._create_heatmap_chart,
            bg_color
        )

    def _create_chart_container(self, title, subtitle, chart_creator, bg_color):
        """Crear contenedor para un gráfico con toolbar"""
        theme = self.theme_manager.get_current_theme()

        # Frame contenedor
        container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        container.pack(fill='both', expand=True, pady=15)

        # Header del gráfico
        header = ctk.CTkFrame(container, fg_color='transparent', height=60)
        header.pack(fill='x', padx=20, pady=(15, 0))
        header.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=('Montserrat', 18, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title_label.pack(side='top', anchor='w')

        subtitle_label = ctk.CTkLabel(
            header,
            text=subtitle,
            font=('Arial', 11),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle_label.pack(side='top', anchor='w', pady=(5, 0))

        # Frame para el gráfico
        chart_frame = ctk.CTkFrame(container, fg_color=bg_color)
        chart_frame.pack(fill='both', expand=True, padx=20, pady=15)

        # Crear figura y canvas
        fig = chart_creator()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()

        # Toolbar de navegación
        toolbar = NavigationToolbar2Tk(canvas, chart_frame)
        toolbar.update()

        # Empaquetar
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def _create_line_chart(self):
        """Crear gráfico de líneas interactivo"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Datos de ejemplo
        modules = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
        x = np.arange(len(modules))

        units = ['TNG', 'Container Care', 'ECV-EIT', 'Operaciones']
        colors = EXECUTIVE_CHART_COLORS[:len(units)]

        for i, (unit, color) in enumerate(zip(units, colors)):
            # Generar datos sintéticos
            base = 100 - i * 10
            trend = np.random.normal(0, 5, len(modules)).cumsum()
            values = base + trend

            ax.plot(x, values, marker='o', label=unit, color=color,
                   linewidth=2.5, markersize=8, markeredgewidth=1.5,
                   markeredgecolor='white')

        ax.set_xlabel('Módulo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Progreso (%)', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(modules)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')

        fig.tight_layout()
        return fig

    def _create_stacked_bar_chart(self):
        """Crear gráfico de barras apiladas"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        modules = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
        x = np.arange(len(modules))
        width = 0.6

        # Datos sintéticos
        completado = np.array([120, 135, 140, 138, 142, 145, 148, 150])
        en_proceso = np.array([30, 28, 25, 27, 24, 22, 20, 18])
        sin_iniciar = np.array([50, 37, 35, 35, 34, 33, 32, 32])

        # Barras apiladas
        p1 = ax.bar(x, completado, width, label='Completado',
                   color=HUTCHISON_COLORS['success'])
        p2 = ax.bar(x, en_proceso, width, bottom=completado,
                   label='En Proceso', color=HUTCHISON_COLORS['warning'])
        p3 = ax.bar(x, sin_iniciar, width, bottom=completado+en_proceso,
                   label='Sin Iniciar', color=HUTCHISON_COLORS['danger'])

        ax.set_xlabel('Módulo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Usuarios', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(modules)
        ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        fig.tight_layout()
        return fig

    def _create_scatter_chart(self):
        """Crear gráfico de dispersión"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Generar datos sintéticos
        np.random.seed(42)
        n_points = 100

        units = ['TNG', 'Container Care', 'ECV-EIT']
        colors = EXECUTIVE_CHART_COLORS[:len(units)]

        for unit, color in zip(units, colors):
            dias = np.random.uniform(1, 60, n_points)
            progreso = 20 + dias * 1.2 + np.random.normal(0, 10, n_points)
            progreso = np.clip(progreso, 0, 100)

            ax.scatter(dias, progreso, label=unit, alpha=0.6,
                      s=100, color=color, edgecolors='white', linewidth=1)

        ax.set_xlabel('Días desde inicio', fontsize=12, fontweight='bold')
        ax.set_ylabel('Progreso (%)', fontsize=12, fontweight='bold')
        ax.legend(loc='lower right', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(0, 65)
        ax.set_ylim(0, 105)

        fig.tight_layout()
        return fig

    def _create_heatmap_chart(self):
        """Crear heatmap"""
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Datos sintéticos
        units = ['TNG', 'Container\nCare', 'ECV-EIT', 'Operaciones',
                'Logística', 'Mantenimiento']
        modules = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

        data = np.random.randint(60, 100, size=(len(units), len(modules)))

        im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=60, vmax=100)

        # Configurar ejes
        ax.set_xticks(np.arange(len(modules)))
        ax.set_yticks(np.arange(len(units)))
        ax.set_xticklabels(modules)
        ax.set_yticklabels(units)

        # Rotar etiquetas
        plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

        # Añadir valores en las celdas
        for i in range(len(units)):
            for j in range(len(modules)):
                text = ax.text(j, i, f'{data[i, j]}%',
                             ha="center", va="center", color="black",
                             fontsize=9, fontweight='bold')

        ax.set_xlabel('Módulo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Unidad de Negocio', fontsize=12, fontweight='bold')

        # Colorbar
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Progreso (%)', rotation=270, labelpad=20, fontsize=11)

        fig.tight_layout()
        return fig
