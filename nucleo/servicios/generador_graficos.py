"""
Servicio de Generación de Gráficos
Funciones centralizadas para crear gráficos Matplotlib con branding Hutchison Ports
"""
from typing import List, Tuple, Optional, Dict
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from nucleo.configuracion.ajustes import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from nucleo.configuracion.gestor_temas import get_theme_manager


class ChartGenerator:
    """Generador centralizado de gráficos con branding Hutchison Ports"""

    def __init__(self):
        """Inicializar el generador de gráficos"""
        self.theme_manager = get_theme_manager()
        self.theme = self.theme_manager.get_current_theme()
        self.is_dark = self.theme_manager.is_dark_mode()

    def create_horizontal_bar_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str = '',
        xlabel: str = '',
        colors: Optional[List] = None,
        figsize: Tuple[int, int] = (8, 5)
    ) -> Figure:
        """
        Crear gráfico de barras horizontal

        Args:
            labels: Etiquetas del eje Y
            values: Valores a graficar
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            colors: Lista de colores (opcional, usa paleta Hutchison por defecto)
            figsize: Tamaño de la figura

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            colors = EXECUTIVE_CHART_COLORS[:len(labels)]

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        bars = ax.barh(labels, values, color=colors, edgecolor='none')

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=11)

        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.3)

        # Añadir valores en las barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + (max(values) * 0.02), bar.get_y() + bar.get_height()/2,
                    f'{int(width)}',
                    ha='left', va='center', fontsize=9,
                    fontweight='bold')

        fig.tight_layout()
        return fig

    def create_vertical_bar_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str = '',
        ylabel: str = '',
        colors: Optional[List] = None,
        figsize: Tuple[int, int] = (8, 5)
    ) -> Figure:
        """
        Crear gráfico de barras vertical

        Args:
            labels: Etiquetas del eje X
            values: Valores a graficar
            title: Título del gráfico
            ylabel: Etiqueta del eje Y
            colors: Lista de colores (opcional)
            figsize: Tamaño de la figura

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            colors = EXECUTIVE_CHART_COLORS[:len(labels)]

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        bars = ax.bar(labels, values, color=colors, edgecolor='none')

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=11)

        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)

        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9,
                    fontweight='bold')

        fig.tight_layout()
        return fig

    def create_donut_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str = '',
        colors: Optional[List] = None,
        figsize: Tuple[int, int] = (8, 5),
        hole_size: float = 0.6
    ) -> Figure:
        """
        Crear gráfico de donut

        Args:
            labels: Etiquetas de las categorías
            values: Valores a graficar
            title: Título del gráfico
            colors: Lista de colores (opcional)
            figsize: Tamaño de la figura
            hole_size: Tamaño del agujero central (0-1)

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            colors = EXECUTIVE_CHART_COLORS[:len(labels)]

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        # Color del borde según tema
        edge_color = self.theme['surface']

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor=edge_color, linewidth=2),
            pctdistance=0.85
        )

        # Estilo de texto
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        # Centrar el donut
        centre_circle = plt.Circle((0, 0), hole_size, fc=edge_color)
        ax.add_artist(centre_circle)

        ax.axis('equal')
        fig.tight_layout()
        return fig

    def create_grouped_bar_chart(
        self,
        categories: List[str],
        series_data: Dict[str, List[float]],
        title: str = '',
        ylabel: str = '',
        colors: Optional[Dict[str, str]] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> Figure:
        """
        Crear gráfico de barras agrupadas

        Args:
            categories: Categorías del eje X (ej: módulos)
            series_data: Diccionario con {nombre_serie: valores}
            title: Título del gráfico
            ylabel: Etiqueta del eje Y
            colors: Diccionario con colores por serie (opcional)
            figsize: Tamaño de la figura

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            color_list = EXECUTIVE_CHART_COLORS
            colors = {name: color_list[i % len(color_list)]
                     for i, name in enumerate(series_data.keys())}

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        # Configurar posiciones de las barras
        n_categories = len(categories)
        n_series = len(series_data)
        bar_width = 0.8 / n_series
        x = np.arange(n_categories)

        # Crear barras para cada serie
        for i, (series_name, values) in enumerate(series_data.items()):
            offset = (i - n_series/2 + 0.5) * bar_width
            ax.bar(x + offset, values, bar_width,
                   label=series_name,
                   color=colors.get(series_name, HUTCHISON_COLORS['ports_sky_blue']))

        ax.set_xticks(x)
        ax.set_xticklabels(categories)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=11)

        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper right', fontsize=9)

        fig.tight_layout()
        return fig

    def create_line_chart(
        self,
        x_data: List,
        series_data: Dict[str, List[float]],
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        colors: Optional[Dict[str, str]] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> Figure:
        """
        Crear gráfico de líneas múltiples

        Args:
            x_data: Datos del eje X
            series_data: Diccionario con {nombre_serie: valores_y}
            title: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            colors: Diccionario con colores por serie (opcional)
            figsize: Tamaño de la figura

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            color_list = EXECUTIVE_CHART_COLORS
            colors = {name: color_list[i % len(color_list)]
                     for i, name in enumerate(series_data.keys())}

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        # Crear líneas para cada serie
        for series_name, y_values in series_data.items():
            ax.plot(x_data, y_values,
                   marker='o',
                   linewidth=2,
                   markersize=6,
                   label=series_name,
                   color=colors.get(series_name, HUTCHISON_COLORS['ports_sky_blue']))

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=11)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=11)

        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(alpha=0.3)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)

        fig.tight_layout()
        return fig

    def create_stacked_bar_chart(
        self,
        categories: List[str],
        series_data: Dict[str, List[float]],
        title: str = '',
        ylabel: str = '',
        colors: Optional[Dict[str, str]] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> Figure:
        """
        Crear gráfico de barras apiladas

        Args:
            categories: Categorías del eje X
            series_data: Diccionario con {nombre_serie: valores}
            title: Título del gráfico
            ylabel: Etiqueta del eje Y
            colors: Diccionario con colores por serie (opcional)
            figsize: Tamaño de la figura

        Returns:
            Figura de Matplotlib
        """
        if colors is None:
            color_list = EXECUTIVE_CHART_COLORS
            colors = {name: color_list[i % len(color_list)]
                     for i, name in enumerate(series_data.keys())}

        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)

        # Crear barras apiladas
        bottom = np.zeros(len(categories))
        for series_name, values in series_data.items():
            ax.bar(categories, values,
                   label=series_name,
                   bottom=bottom,
                   color=colors.get(series_name, HUTCHISON_COLORS['ports_sky_blue']))
            bottom += np.array(values)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=11)

        ax.tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper left', fontsize=9)

        fig.tight_layout()
        return fig


# Instancia global del generador (Singleton)
_chart_generator = None

def get_chart_generator() -> ChartGenerator:
    """Obtener instancia global del generador de gráficos"""
    global _chart_generator
    if _chart_generator is None:
        _chart_generator = ChartGenerator()
    return _chart_generator
