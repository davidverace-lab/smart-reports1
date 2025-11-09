"""
Motor de Gráficos con Matplotlib - Embebido en Tkinter
Solución definitiva que SIEMPRE muestra gráficos visuales
"""

import matplotlib
matplotlib.use('TkAgg')  # Backend para Tkinter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Dict, List
from nucleo.configuracion.ajustes import HUTCHISON_COLORS


class MotorGraficosMatplotlib:
    """Motor de gráficos con matplotlib embebido nativamente en Tkinter"""

    # Paleta de colores Hutchison
    PALETA = [
        HUTCHISON_COLORS['ports_sky_blue'],
        HUTCHISON_COLORS['ports_horizon_blue'],
        HUTCHISON_COLORS['success'],
        HUTCHISON_COLORS['warning'],
        HUTCHISON_COLORS['danger'],
        '#8B4CFA', '#FF8C42', '#4ECDC4', '#A78BFA', '#FB923C'
    ]

    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convertir color hex a RGB normalizado"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

    @staticmethod
    def _aplicar_estilo(fig, ax, tema='dark'):
        """Aplicar estilo consistente según tema"""
        if tema == 'dark':
            bg_color = '#2b2d42'
            text_color = '#ffffff'
            grid_color = '#3a3d5c'
        else:
            bg_color = '#ffffff'
            text_color = '#2b2d42'
            grid_color = '#e0e0e0'

        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # Estilo de ejes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['bottom'].set_color(grid_color)

        # Estilo de texto
        ax.tick_params(colors=text_color, labelsize=9)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)

        # Grid
        ax.grid(axis='y', alpha=0.3, color=grid_color, linestyle='--', linewidth=0.5)

    @staticmethod
    def crear_grafico_barras(parent_widget, datos: Dict, tema: str = 'dark', titulo: str = ''):
        """
        Crear gráfico de barras embebido en Tkinter

        Args:
            parent_widget: Widget padre de Tkinter
            datos: {'labels': [...], 'values': [...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            FigureCanvasTkAgg con el gráfico
        """
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return None

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Colores
        colors = [MotorGraficosMatplotlib._hex_to_rgb(
            MotorGraficosMatplotlib.PALETA[i % len(MotorGraficosMatplotlib.PALETA)]
        ) for i in range(len(labels))]

        # Crear barras
        bars = ax.bar(labels, values, color=colors, edgecolor='none', alpha=0.9, width=0.6)

        # Agregar valores sobre barras
        for bar in bars:
            height = bar.get_height()
            color = '#ffffff' if tema == 'dark' else '#2b2d42'
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom',
                   fontsize=9, fontweight='bold', color=color)

        # Estilo
        if titulo:
            ax.set_title(titulo, fontsize=12, fontweight='bold', pad=15)
        ax.set_ylabel('Cantidad', fontsize=10, fontweight='bold')

        MotorGraficosMatplotlib._aplicar_estilo(fig, ax, tema)

        # Rotar etiquetas si son muchas
        if len(labels) > 5:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        fig.tight_layout()

        # Crear canvas para Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()

        return canvas

    @staticmethod
    def crear_grafico_donut(parent_widget, datos: Dict, tema: str = 'dark', titulo: str = ''):
        """
        Crear gráfico donut embebido en Tkinter

        Args:
            parent_widget: Widget padre de Tkinter
            datos: {'labels': [...], 'values': [...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            FigureCanvasTkAgg con el gráfico
        """
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return None

        # Configurar tema
        bg_color = '#2b2d42' if tema == 'dark' else '#ffffff'
        text_color = '#ffffff' if tema == 'dark' else '#2b2d42'

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        # Colores
        colors = [MotorGraficosMatplotlib._hex_to_rgb(
            MotorGraficosMatplotlib.PALETA[i % len(MotorGraficosMatplotlib.PALETA)]
        ) for i in range(len(labels))]

        # Crear donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor=bg_color, linewidth=2),
            textprops={'color': text_color, 'fontsize': 9, 'fontweight': 'bold'}
        )

        # Estilo de porcentajes
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')

        if titulo:
            ax.set_title(titulo, fontsize=12, color=text_color, fontweight='bold', pad=15)

        fig.tight_layout()

        # Crear canvas para Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()

        return canvas

    @staticmethod
    def crear_grafico_lineas(parent_widget, datos: Dict, tema: str = 'dark', titulo: str = ''):
        """
        Crear gráfico de líneas embebido en Tkinter

        Args:
            parent_widget: Widget padre de Tkinter
            datos: {'labels': [...], 'series': [{'name': '', 'values': [...]}, ...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            FigureCanvasTkAgg con el gráfico
        """
        labels = datos.get('labels', [])
        series = datos.get('series', [])

        if not labels or not series:
            return None

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Plotear cada serie
        for idx, serie in enumerate(series):
            color = MotorGraficosMatplotlib._hex_to_rgb(
                MotorGraficosMatplotlib.PALETA[idx % len(MotorGraficosMatplotlib.PALETA)]
            )
            ax.plot(
                labels,
                serie['values'],
                marker='o',
                linewidth=2.5,
                markersize=6,
                label=serie['name'],
                color=color,
                alpha=0.9
            )

        # Estilo
        if titulo:
            ax.set_title(titulo, fontsize=12, fontweight='bold', pad=15)
        ax.set_ylabel('Valor', fontsize=10, fontweight='bold')

        MotorGraficosMatplotlib._aplicar_estilo(fig, ax, tema)

        # Leyenda
        bg_color = '#2b2d42' if tema == 'dark' else '#ffffff'
        grid_color = '#3a3d5c' if tema == 'dark' else '#e0e0e0'
        ax.legend(facecolor=bg_color, edgecolor=grid_color,
                 fontsize=9, loc='upper left', framealpha=0.9)

        # Rotar etiquetas si son muchas
        if len(labels) > 8:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        fig.tight_layout()

        # Crear canvas para Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()

        return canvas
