"""
Motor de Gráficos SVG Estáticos
Alternativa a D3.js para renderizado embebido sin JavaScript
"""

import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import io
import base64
from typing import Dict, List
from nucleo.configuracion.ajustes import HUTCHISON_COLORS


class MotorGraficosSVG:
    """Motor para generar gráficos SVG estáticos usando matplotlib"""

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
        """Convertir color hex a RGB normalizado para matplotlib"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

    @staticmethod
    def generar_grafico_barras(datos: Dict, tema: str = 'dark', titulo: str = '') -> str:
        """
        Generar gráfico de barras SVG

        Args:
            datos: {'labels': [...], 'values': [...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            HTML con SVG embebido en base64
        """
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return "<p>No hay datos para mostrar</p>"

        # Configurar estilo según tema
        if tema == 'dark':
            plt.style.use('dark_background')
            bg_color = '#2b2d42'
            text_color = '#ffffff'
            grid_color = '#3a3d5c'
        else:
            plt.style.use('seaborn-v0_8-darkgrid')
            bg_color = '#ffffff'
            text_color = '#2b2d42'
            grid_color = '#e0e0e0'

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        # Colores para cada barra
        colors = [MotorGraficosSVG._hex_to_rgb(MotorGraficosSVG.PALETA[i % len(MotorGraficosSVG.PALETA)])
                  for i in range(len(labels))]

        # Crear barras
        bars = ax.bar(labels, values, color=colors, edgecolor='none', alpha=0.9)

        # Agregar valores sobre las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom',
                   fontsize=10, fontweight='bold', color=text_color)

        # Estilo
        ax.set_xlabel('', fontsize=12, color=text_color, fontweight='bold')
        ax.set_ylabel('Cantidad', fontsize=12, color=text_color, fontweight='bold')
        if titulo:
            ax.set_title(titulo, fontsize=14, color=text_color, fontweight='bold', pad=20)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['bottom'].set_color(grid_color)
        ax.grid(axis='y', alpha=0.3, color=grid_color, linestyle='--', linewidth=0.5)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Convertir a SVG base64
        return MotorGraficosSVG._fig_to_html(fig, bg_color, titulo)

    @staticmethod
    def generar_grafico_donut(datos: Dict, tema: str = 'dark', titulo: str = '') -> str:
        """
        Generar gráfico donut SVG

        Args:
            datos: {'labels': [...], 'values': [...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            HTML con SVG embebido
        """
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        if not labels or not values:
            return "<p>No hay datos para mostrar</p>"

        # Configurar tema
        if tema == 'dark':
            bg_color = '#2b2d42'
            text_color = '#ffffff'
        else:
            bg_color = '#ffffff'
            text_color = '#2b2d42'

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        # Colores
        colors = [MotorGraficosSVG._hex_to_rgb(MotorGraficosSVG.PALETA[i % len(MotorGraficosSVG.PALETA)])
                  for i in range(len(labels))]

        # Crear donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.5, edgecolor=bg_color, linewidth=2),
            textprops={'color': text_color, 'fontsize': 11, 'fontweight': 'bold'}
        )

        # Estilo de texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        if titulo:
            ax.set_title(titulo, fontsize=14, color=text_color, fontweight='bold', pad=20)

        plt.tight_layout()

        return MotorGraficosSVG._fig_to_html(fig, bg_color, titulo)

    @staticmethod
    def generar_grafico_lineas(datos: Dict, tema: str = 'dark', titulo: str = '') -> str:
        """
        Generar gráfico de líneas SVG

        Args:
            datos: {'labels': [...], 'series': [{'name': '', 'values': [...]}, ...]}
            tema: 'dark' o 'light'
            titulo: Título del gráfico

        Returns:
            HTML con SVG embebido
        """
        labels = datos.get('labels', [])
        series = datos.get('series', [])

        if not labels or not series:
            return "<p>No hay datos para mostrar</p>"

        # Configurar tema
        if tema == 'dark':
            plt.style.use('dark_background')
            bg_color = '#2b2d42'
            text_color = '#ffffff'
            grid_color = '#3a3d5c'
        else:
            plt.style.use('seaborn-v0_8-darkgrid')
            bg_color = '#ffffff'
            text_color = '#2b2d42'
            grid_color = '#e0e0e0'

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        # Plotear cada serie
        for idx, serie in enumerate(series):
            color = MotorGraficosSVG._hex_to_rgb(
                MotorGraficosSVG.PALETA[idx % len(MotorGraficosSVG.PALETA)]
            )
            ax.plot(
                labels,
                serie['values'],
                marker='o',
                linewidth=2.5,
                markersize=8,
                label=serie['name'],
                color=color,
                alpha=0.9
            )

        # Estilo
        if titulo:
            ax.set_title(titulo, fontsize=14, color=text_color, fontweight='bold', pad=20)
        ax.set_xlabel('', fontsize=12, color=text_color, fontweight='bold')
        ax.set_ylabel('Valor', fontsize=12, color=text_color, fontweight='bold')

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['bottom'].set_color(grid_color)
        ax.grid(True, alpha=0.3, color=grid_color, linestyle='--', linewidth=0.5)
        ax.legend(facecolor=bg_color, edgecolor=grid_color,
                 fontsize=10, loc='upper left', framealpha=0.9)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return MotorGraficosSVG._fig_to_html(fig, bg_color, titulo)

    @staticmethod
    def _fig_to_html(fig, bg_color, titulo=''):
        """Convertir figura matplotlib a HTML con SVG embebido"""
        # Guardar en buffer como SVG
        buf = io.BytesIO()
        fig.savefig(buf, format='svg', facecolor=bg_color,
                   edgecolor='none', bbox_inches='tight', dpi=150)
        buf.seek(0)
        svg_data = buf.read()
        plt.close(fig)

        # Codificar en base64
        svg_base64 = base64.b64encode(svg_data).decode('utf-8')

        # Generar HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: {bg_color};
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <img src="data:image/svg+xml;base64,{svg_base64}" alt="{titulo}">
        </body>
        </html>
        """
        return html
