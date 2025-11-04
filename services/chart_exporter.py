"""
Servicio de Exportación de Gráficos - Conversión Matplotlib → Plotly
Convierte gráficos Matplotlib a Plotly interactivos con branding Hutchison Ports
"""
import os
import tempfile
import webbrowser
from datetime import datetime
from typing import Optional
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.figure import Figure
import numpy as np
from config.settings import HUTCHISON_COLORS


# Template de diseño Hutchison Ports para Plotly
HUTCHISON_PLOTLY_LAYOUT = {
    'font': {
        'family': 'Segoe UI, Arial, sans-serif',
        'size': 12,
        'color': '#1F2937'
    },
    'title': {
        'font': {
            'size': 20,
            'color': '#002E6D',
            'family': 'Montserrat, sans-serif'
        },
        'x': 0.5,
        'xanchor': 'center'
    },
    'paper_bgcolor': '#FFFFFF',
    'plot_bgcolor': '#F9FAFB',
    'colorway': [
        HUTCHISON_COLORS['ports_sky_blue'],
        HUTCHISON_COLORS['ports_sea_blue'],
        HUTCHISON_COLORS['ports_horizon_blue'],
        HUTCHISON_COLORS['sunray_yellow'],
        HUTCHISON_COLORS['success'],
        HUTCHISON_COLORS['warning'],
        HUTCHISON_COLORS['danger']
    ],
    'xaxis': {
        'gridcolor': '#E5E7EB',
        'linecolor': '#9CA3AF',
        'zeroline': False
    },
    'yaxis': {
        'gridcolor': '#E5E7EB',
        'linecolor': '#9CA3AF',
        'zeroline': False
    },
    'hovermode': 'closest',
    'hoverlabel': {
        'bgcolor': '#FFFFFF',
        'bordercolor': HUTCHISON_COLORS['ports_sky_blue'],
        'font': {'size': 12}
    }
}


class ChartExporter:
    """Exportador de gráficos Matplotlib a Plotly interactivo"""

    def __init__(self):
        """Inicializar el exportador"""
        self.temp_dir = tempfile.gettempdir()

    def export_to_plotly(self, matplotlib_fig: Figure, chart_title: str = 'Gráfico') -> Optional[str]:
        """
        Exportar figura de Matplotlib a Plotly interactivo y abrir en navegador

        Args:
            matplotlib_fig: Figura de Matplotlib
            chart_title: Título del gráfico

        Returns:
            Ruta del archivo HTML generado, o None si hay error
        """
        try:
            # Detectar tipo de gráfico y extraer datos
            chart_data = self._extract_chart_data(matplotlib_fig)

            if not chart_data:
                print("⚠️ No se pudo extraer datos del gráfico")
                return None

            # Crear figura de Plotly según el tipo
            plotly_fig = self._create_plotly_figure(chart_data, chart_title)

            # Aplicar branding Hutchison Ports
            plotly_fig.update_layout(**HUTCHISON_PLOTLY_LAYOUT)

            # Generar nombre de archivo único
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in chart_title if c.isalnum() or c in (' ', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"hutchison_chart_{safe_title}_{timestamp}.html"
            filepath = os.path.join(self.temp_dir, filename)

            # Guardar como HTML con CDN de Plotly (optimizado)
            plotly_fig.write_html(
                filepath,
                include_plotlyjs='cdn',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'hutchison_{safe_title}',
                        'height': 800,
                        'width': 1200,
                        'scale': 2
                    }
                }
            )

            # Abrir en navegador
            webbrowser.open('file://' + filepath)

            print(f"✓ Gráfico interactivo exportado: {filepath}")
            return filepath

        except Exception as e:
            print(f"❌ Error al exportar gráfico: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _extract_chart_data(self, fig: Figure) -> Optional[dict]:
        """
        Extraer datos de la figura de Matplotlib

        Args:
            fig: Figura de Matplotlib

        Returns:
            Diccionario con tipo y datos del gráfico
        """
        try:
            # Obtener el primer axes de la figura
            if not fig.axes:
                return None

            ax = fig.axes[0]

            # Detectar tipo de gráfico según los elementos presentes
            chart_data = {
                'type': 'unknown',
                'title': ax.get_title() or '',
                'xlabel': ax.get_xlabel() or '',
                'ylabel': ax.get_ylabel() or ''
            }

            # Detectar barras (bar chart)
            bars = [child for child in ax.get_children() if hasattr(child, 'get_height') and hasattr(child, 'get_width')]
            if bars and len(bars) > 0:
                # Determinar si es horizontal o vertical
                first_bar = bars[0]
                is_horizontal = first_bar.get_height() < first_bar.get_width()

                if is_horizontal:
                    chart_data['type'] = 'barh'
                    chart_data['labels'] = [t.get_text() for t in ax.get_yticklabels()]
                    chart_data['values'] = [bar.get_width() for bar in bars]
                else:
                    chart_data['type'] = 'bar'
                    chart_data['labels'] = [t.get_text() for t in ax.get_xticklabels()]
                    chart_data['values'] = [bar.get_height() for bar in bars]

                chart_data['colors'] = [bar.get_facecolor() for bar in bars]
                return chart_data

            # Detectar líneas (line chart)
            lines = ax.get_lines()
            if lines:
                chart_data['type'] = 'line'
                chart_data['series'] = []
                for line in lines:
                    xdata = line.get_xdata()
                    ydata = line.get_ydata()
                    label = line.get_label()
                    color = line.get_color()
                    chart_data['series'].append({
                        'x': list(xdata),
                        'y': list(ydata),
                        'label': label if label and not label.startswith('_') else 'Serie',
                        'color': color
                    })
                return chart_data

            # Detectar pie/donut chart
            wedges = [child for child in ax.get_children() if type(child).__name__ == 'Wedge']
            if wedges:
                chart_data['type'] = 'pie'
                chart_data['values'] = []
                chart_data['labels'] = []
                chart_data['colors'] = []

                # Extraer valores de los wedges
                for wedge in wedges:
                    chart_data['values'].append(wedge.theta2 - wedge.theta1)
                    chart_data['colors'].append(wedge.get_facecolor())

                # Obtener labels de los textos
                texts = [child for child in ax.get_children() if type(child).__name__ == 'Text']
                for text in texts:
                    label_text = text.get_text().strip()
                    if label_text and label_text not in ['', '0', '0.0']:
                        chart_data['labels'].append(label_text)

                # Si no hay suficientes labels, usar genéricos
                if len(chart_data['labels']) < len(chart_data['values']):
                    chart_data['labels'] = [f'Categoría {i+1}' for i in range(len(chart_data['values']))]

                return chart_data

            return chart_data

        except Exception as e:
            print(f"Error extrayendo datos: {e}")
            return None

    def _create_plotly_figure(self, chart_data: dict, title: str) -> go.Figure:
        """
        Crear figura de Plotly basada en los datos extraídos

        Args:
            chart_data: Datos del gráfico
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        chart_type = chart_data.get('type', 'unknown')

        if chart_type == 'bar':
            # Gráfico de barras vertical
            fig = go.Figure(data=[
                go.Bar(
                    x=chart_data.get('labels', []),
                    y=chart_data.get('values', []),
                    marker_color=HUTCHISON_COLORS['ports_sky_blue'],
                    text=chart_data.get('values', []),
                    textposition='auto',
                    texttemplate='%{text:.0f}',
                    hovertemplate='<b>%{x}</b><br>Valor: %{y:.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title=title,
                xaxis_title=chart_data.get('xlabel', ''),
                yaxis_title=chart_data.get('ylabel', ''),
                showlegend=False
            )

        elif chart_type == 'barh':
            # Gráfico de barras horizontal
            fig = go.Figure(data=[
                go.Bar(
                    y=chart_data.get('labels', []),
                    x=chart_data.get('values', []),
                    orientation='h',
                    marker_color=HUTCHISON_COLORS['ports_sky_blue'],
                    text=chart_data.get('values', []),
                    textposition='auto',
                    texttemplate='%{text:.0f}',
                    hovertemplate='<b>%{y}</b><br>Valor: %{x:.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title=title,
                xaxis_title=chart_data.get('ylabel', ''),  # Invertido en horizontal
                yaxis_title=chart_data.get('xlabel', ''),  # Invertido en horizontal
                showlegend=False
            )

        elif chart_type == 'line':
            # Gráfico de líneas
            fig = go.Figure()
            for serie in chart_data.get('series', []):
                fig.add_trace(go.Scatter(
                    x=serie['x'],
                    y=serie['y'],
                    mode='lines+markers',
                    name=serie['label'],
                    line=dict(width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{fullData.name}</b><br>X: %{x}<br>Y: %{y:.2f}<extra></extra>'
                ))
            fig.update_layout(
                title=title,
                xaxis_title=chart_data.get('xlabel', ''),
                yaxis_title=chart_data.get('ylabel', ''),
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )

        elif chart_type == 'pie':
            # Gráfico de pie/donut
            fig = go.Figure(data=[
                go.Pie(
                    labels=chart_data.get('labels', []),
                    values=chart_data.get('values', []),
                    hole=0.4,  # Hacer donut
                    marker=dict(
                        colors=[HUTCHISON_COLORS['ports_sky_blue'],
                                HUTCHISON_COLORS['ports_sea_blue'],
                                HUTCHISON_COLORS['ports_horizon_blue'],
                                HUTCHISON_COLORS['sunray_yellow'],
                                HUTCHISON_COLORS['success']]
                    ),
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Valor: %{value:.0f}<br>Porcentaje: %{percent}<extra></extra>'
                )
            ])
            fig.update_layout(
                title=title,
                showlegend=True,
                legend=dict(
                    orientation='v',
                    yanchor='middle',
                    y=0.5,
                    xanchor='left',
                    x=1.05
                )
            )

        else:
            # Tipo desconocido - crear gráfico básico
            fig = go.Figure()
            fig.add_annotation(
                text=f"Tipo de gráfico no soportado: {chart_type}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(title=title)

        # Configuración común para todos los gráficos
        fig.update_layout(
            height=600,
            margin=dict(l=80, r=80, t=100, b=80),
            template='plotly_white'
        )

        return fig


# Instancia global del exportador
_chart_exporter = None

def get_chart_exporter() -> ChartExporter:
    """Obtener instancia global del exportador (Singleton)"""
    global _chart_exporter
    if _chart_exporter is None:
        _chart_exporter = ChartExporter()
    return _chart_exporter
