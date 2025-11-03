"""
InteractiveChartsPanel - Panel con gráficos interactivos usando Plotly
"""
import customtkinter as ctk
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from config.settings import EXECUTIVE_CHART_COLORS, HUTCHISON_COLORS
from ui.components.plotly_interactive_chart import PlotlyInteractiveChart


class InteractiveChartsPanel(ctk.CTkFrame):
    """Panel con gráficos interactivos de Plotly"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
        """
        super().__init__(parent, fg_color='transparent', **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Crear header
        self._create_header()

        # Crear grid de gráficos
        self._create_charts_grid()

        # Cargar datos
        self.after(100, self.load_charts)

    def _create_header(self):
        """Crear header del panel"""
        header = ctk.CTkFrame(self, fg_color='transparent', height=60)
        header.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text='📊 Análisis Interactivo',
            font=('Montserrat', 24, 'bold'),
            text_color='#ffffff',
            anchor='w'
        )
        title.pack(side='left')

        subtitle = ctk.CTkLabel(
            header,
            text='Gráficos interactivos con funciones avanzadas',
            font=('Arial', 12),
            text_color='#a0a0a0',
            anchor='w'
        )
        subtitle.pack(side='left', padx=(15, 0))

    def _create_charts_grid(self):
        """Crear grid de gráficos"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            scrollbar_button_color='#3a3d5c'
        )
        scroll_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))

        # Grid 2x2
        scroll_frame.grid_columnconfigure((0, 1), weight=1)
        scroll_frame.grid_rowconfigure((0, 1), weight=1)

        # Chart 1: Líneas interactivas con zoom
        self.chart1 = PlotlyInteractiveChart(
            scroll_frame,
            title='Tendencias por Módulo (Interactivo)'
        )
        self.chart1.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Chart 2: Barras apiladas interactivas
        self.chart2 = PlotlyInteractiveChart(
            scroll_frame,
            title='Distribución por Estado (Clickeable)'
        )
        self.chart2.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # Chart 3: Sunburst jerárquico
        self.chart3 = PlotlyInteractiveChart(
            scroll_frame,
            title='Jerarquía Organizacional (Explorable)'
        )
        self.chart3.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Chart 4: Scatter 3D
        self.chart4 = PlotlyInteractiveChart(
            scroll_frame,
            title='Análisis Multidimensional (3D)'
        )
        self.chart4.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    def load_charts(self):
        """Cargar todos los gráficos"""
        self._create_line_chart()
        self._create_stacked_bar_chart()
        self._create_sunburst_chart()
        self._create_scatter_3d()

    def _create_line_chart(self):
        """Crear gráfico de líneas interactivo con zoom y hover"""
        # Datos de ejemplo
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

        fig = go.Figure()

        # Completados
        fig.add_trace(go.Scatter(
            x=modulos,
            y=[123, 134, 133, 135, 133, 135, 135, 145],
            name='Completados',
            mode='lines+markers',
            line=dict(color=EXECUTIVE_CHART_COLORS[0], width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Completados: %{y}<extra></extra>'
        ))

        # En Proceso
        fig.add_trace(go.Scatter(
            x=modulos,
            y=[32, 28, 25, 30, 27, 32, 28, 25],
            name='En Proceso',
            mode='lines+markers',
            line=dict(color=EXECUTIVE_CHART_COLORS[4], width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>En Proceso: %{y}<extra></extra>'
        ))

        # Sin Iniciar
        fig.add_trace(go.Scatter(
            x=modulos,
            y=[45, 38, 42, 35, 40, 33, 37, 30],
            name='Sin Iniciar',
            mode='lines+markers',
            line=dict(color=EXECUTIVE_CHART_COLORS[5], width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Sin Iniciar: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title='Progreso por Módulo',
            xaxis_title='Módulo',
            yaxis_title='Cantidad de Usuarios',
            hovermode='x unified',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        self.chart1.set_figure(fig)

    def _create_stacked_bar_chart(self):
        """Crear gráfico de barras apiladas interactivo"""
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Completados',
            x=modulos,
            y=[123, 134, 133, 135, 133, 135, 135, 145],
            marker_color=EXECUTIVE_CHART_COLORS[0],
            text=[123, 134, 133, 135, 133, 135, 135, 145],
            textposition='inside',
            hovertemplate='<b>%{x}</b><br>Completados: %{y}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            name='En Proceso',
            x=modulos,
            y=[32, 28, 25, 30, 27, 32, 28, 25],
            marker_color=EXECUTIVE_CHART_COLORS[4],
            text=[32, 28, 25, 30, 27, 32, 28, 25],
            textposition='inside',
            hovertemplate='<b>%{x}</b><br>En Proceso: %{y}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            name='Sin Iniciar',
            x=modulos,
            y=[45, 38, 42, 35, 40, 33, 37, 30],
            marker_color=EXECUTIVE_CHART_COLORS[5],
            text=[45, 38, 42, 35, 40, 33, 37, 30],
            textposition='inside',
            hovertemplate='<b>%{x}</b><br>Sin Iniciar: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title='Distribución Acumulada por Estado',
            barmode='stack',
            xaxis_title='Módulo',
            yaxis_title='Total de Usuarios',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        self.chart2.set_figure(fig)

    def _create_sunburst_chart(self):
        """Crear gráfico sunburst jerárquico interactivo"""
        # Crear datos jerárquicos
        labels = ['Total',
                  'TNG', 'Container Care', 'ECV-EIT',
                  'TNG-Completado', 'TNG-Proceso', 'TNG-Sin Iniciar',
                  'CC-Completado', 'CC-Proceso', 'CC-Sin Iniciar',
                  'ECV-Completado', 'ECV-Proceso', 'ECV-Sin Iniciar']

        parents = ['',
                   'Total', 'Total', 'Total',
                   'TNG', 'TNG', 'TNG',
                   'Container Care', 'Container Care', 'Container Care',
                   'ECV-EIT', 'ECV-EIT', 'ECV-EIT']

        values = [1050,
                  600, 250, 200,
                  400, 120, 80,
                  180, 40, 30,
                  150, 30, 20]

        colors = ['#ffffff',
                  EXECUTIVE_CHART_COLORS[0], EXECUTIVE_CHART_COLORS[1], EXECUTIVE_CHART_COLORS[2],
                  EXECUTIVE_CHART_COLORS[0], EXECUTIVE_CHART_COLORS[4], EXECUTIVE_CHART_COLORS[5],
                  EXECUTIVE_CHART_COLORS[1], EXECUTIVE_CHART_COLORS[4], EXECUTIVE_CHART_COLORS[5],
                  EXECUTIVE_CHART_COLORS[2], EXECUTIVE_CHART_COLORS[4], EXECUTIVE_CHART_COLORS[5]]

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors),
            branchvalues='total',
            hovertemplate='<b>%{label}</b><br>Usuarios: %{value}<br>Porcentaje: %{percentParent}<extra></extra>'
        ))

        fig.update_layout(
            title='Distribución Jerárquica por Unidad y Estado',
        )

        self.chart3.set_figure(fig)

    def _create_scatter_3d(self):
        """Crear gráfico scatter 3D interactivo"""
        # Generar datos de ejemplo
        np.random.seed(42)
        n = 200

        modulos = np.random.choice(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'], n)
        progreso = np.random.randint(0, 100, n)
        tiempo = np.random.randint(1, 30, n)
        nivel = np.random.choice(['Básico', 'Intermedio', 'Avanzado'], n)

        # Mapear niveles a colores
        color_map = {'Básico': EXECUTIVE_CHART_COLORS[5],
                     'Intermedio': EXECUTIVE_CHART_COLORS[4],
                     'Avanzado': EXECUTIVE_CHART_COLORS[0]}
        colors = [color_map[n] for n in nivel]

        fig = go.Figure(data=[go.Scatter3d(
            x=modulos,
            y=progreso,
            z=tiempo,
            mode='markers',
            marker=dict(
                size=8,
                color=colors,
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            text=nivel,
            hovertemplate='<b>Módulo:</b> %{x}<br>' +
                          '<b>Progreso:</b> %{y}%<br>' +
                          '<b>Tiempo:</b> %{z} días<br>' +
                          '<b>Nivel:</b> %{text}<extra></extra>'
        )])

        fig.update_layout(
            title='Análisis 3D: Módulo vs Progreso vs Tiempo',
            scene=dict(
                xaxis_title='Módulo',
                yaxis_title='Progreso (%)',
                zaxis_title='Tiempo (días)',
                bgcolor='#1a1d2e'
            ),
            showlegend=False
        )

        self.chart4.set_figure(fig)
