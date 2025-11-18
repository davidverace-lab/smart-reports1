"""
Gráficas Modernas con Plotly
Sistema de visualizaciones interactivas y animadas
"""
import customtkinter as ctk
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️ Plotly no está instalado. Instala con: pip install plotly kaleido")

from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS
import tkinter as tk
from tkinter import ttk


class ModernPlotlyChart(ctk.CTkFrame):
    """
    Widget base para gráficas Plotly modernas

    Features:
    - Interactividad completa (zoom, pan, hover)
    - Tema oscuro/claro automático
    - Exportar a imagen
    - Fullscreen mode
    """

    def __init__(self, parent, title: str = "", **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título de la gráfica
        """
        theme = get_theme_manager().get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            **kwargs
        )

        self.title = title
        self.theme = theme
        self.fig = None

        # UI
        self._create_ui()

    def _create_ui(self):
        """Crear UI base"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent', height=50)
        header.pack(fill='x', padx=15, pady=(15, 5))
        header.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            header,
            text=self.title,
            font=('Poppins', 15, 'bold'),
            text_color=self.theme['text'],
            anchor='w'
        ).pack(side='left')

        # Botones de acción
        actions_frame = ctk.CTkFrame(header, fg_color='transparent')
        actions_frame.pack(side='right')

        # Botón fullscreen
        ctk.CTkButton(
            actions_frame,
            text="⛶",
            font=('Segoe UI', 14),
            width=35,
            height=35,
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            corner_radius=8,
            command=self._toggle_fullscreen
        ).pack(side='right', padx=2)

        # Container para la gráfica
        self.chart_container = ctk.CTkFrame(
            self,
            fg_color=self.theme['background'],
            corner_radius=12
        )
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(5, 15))

    def _toggle_fullscreen(self):
        """Toggle modo pantalla completa"""
        # TODO: Implementar modal fullscreen
        print("🔍 Fullscreen mode")

    def _get_layout(self):
        """Obtener layout base de Plotly"""
        return dict(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family='Poppins',
                color=self.theme['text'],
                size=12
            ),
            hoverlabel=dict(
                bgcolor=HUTCHISON_COLORS['ports_sea_blue'],
                font_size=13,
                font_family='Poppins',
                font_color='white'
            ),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color=self.theme['text'])
            ),
            margin=dict(l=40, r=20, t=20, b=40),
            xaxis=dict(
                showgrid=False,
                color=self.theme['text_secondary'],
                linecolor=self.theme['border']
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=self.theme['border'],
                color=self.theme['text_secondary'],
                linecolor=self.theme['border']
            )
        )

    def render(self):
        """Renderizar gráfica (debe ser implementado por subclases)"""
        raise NotImplementedError("Subclases deben implementar render()")


class ModernBarChart(ModernPlotlyChart):
    """
    Gráfica de barras moderna con gradientes

    Features:
    - Gradiente en las barras
    - Valores en las barras
    - Hover interactivo
    - Ordenamiento automático
    """

    def __init__(self, parent, title: str, labels: list, values: list,
                 orientation: str = 'v', color_scale: str = 'Blues', **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título
            labels: Etiquetas (categorías)
            values: Valores numéricos
            orientation: 'v' (vertical) o 'h' (horizontal)
            color_scale: Escala de colores ('Blues', 'Greens', 'Purples', etc.)
        """
        super().__init__(parent, title, **kwargs)

        self.labels = labels
        self.values = values
        self.orientation = orientation
        self.color_scale = color_scale

        # Renderizar
        self.render()

    def render(self):
        """Renderizar gráfica de barras"""
        if not PLOTLY_AVAILABLE:
            self._show_error()
            return

        # Crear figura
        self.fig = go.Figure()

        if self.orientation == 'v':
            # Barras verticales
            self.fig.add_trace(go.Bar(
                x=self.labels,
                y=self.values,
                marker=dict(
                    color=self.values,
                    colorscale=self.color_scale,
                    line=dict(color='rgba(255,255,255,0.2)', width=1.5),
                    showscale=False
                ),
                text=self.values,
                textposition='outside',
                textfont=dict(size=12, color=self.theme['text']),
                hovertemplate='<b>%{x}</b><br>Valor: %{y:,}<extra></extra>'
            ))
        else:
            # Barras horizontales
            self.fig.add_trace(go.Bar(
                x=self.values,
                y=self.labels,
                orientation='h',
                marker=dict(
                    color=self.values,
                    colorscale=self.color_scale,
                    line=dict(color='rgba(255,255,255,0.2)', width=1.5),
                    showscale=False
                ),
                text=self.values,
                textposition='outside',
                textfont=dict(size=12, color=self.theme['text']),
                hovertemplate='<b>%{y}</b><br>Valor: %{x:,}<extra></extra>'
            ))

        # Aplicar layout
        self.fig.update_layout(**self._get_layout())
        self.fig.update_layout(showlegend=False)

        # Mostrar en el widget
        self._display_plotly()

    def _display_plotly(self):
        """Mostrar gráfica Plotly en el widget"""
        # Limpiar container
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Crear HTML temporal
        import tempfile
        import os

        # Generar HTML
        html = self.fig.to_html(include_plotlyjs='cdn', config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        })

        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
            f.write(html)
            html_path = f.name

        # Mostrar en navegador embebido (si está disponible)
        try:
            import tkinterweb
            browser = tkinterweb.HtmlFrame(self.chart_container)
            browser.load_file(html_path)
            browser.pack(fill='both', expand=True)
        except ImportError:
            # Alternativa: Mostrar mensaje
            ctk.CTkLabel(
                self.chart_container,
                text="📊 Gráfica generada\n\n⚠️ Instala tkinterweb para visualización embebida:\npip install tkinterweb",
                font=('Poppins', 12),
                text_color=self.theme['text_secondary'],
                justify='center'
            ).pack(expand=True)

            # Botón para abrir en navegador
            ctk.CTkButton(
                self.chart_container,
                text="🌐 Abrir en Navegador",
                command=lambda: os.system(f'start {html_path}'),
                fg_color=HUTCHISON_COLORS['ports_sea_blue'],
                hover_color='#003D8F'
            ).pack(pady=10)

    def _show_error(self):
        """Mostrar error si Plotly no está disponible"""
        ctk.CTkLabel(
            self.chart_container,
            text="⚠️ Plotly no está instalado\n\nInstala con:\npip install plotly kaleido",
            font=('Poppins', 12),
            text_color='#ff6b6b',
            justify='center'
        ).pack(expand=True)


class ModernDonutChart(ModernPlotlyChart):
    """
    Gráfica de dona moderna con efectos 3D

    Features:
    - Centro hueco con total
    - Colores vibrantes
    - Porcentajes en las secciones
    - Pull effect en primera sección
    """

    def __init__(self, parent, title: str, labels: list, values: list,
                 colors: list = None, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título
            labels: Etiquetas
            values: Valores
            colors: Colores personalizados (opcional)
        """
        super().__init__(parent, title, **kwargs)

        self.labels = labels
        self.values = values
        self.colors = colors or ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']

        self.render()

    def render(self):
        """Renderizar gráfica de dona"""
        if not PLOTLY_AVAILABLE:
            self._show_error()
            return

        self.fig = go.Figure(data=[go.Pie(
            labels=self.labels,
            values=self.values,
            hole=0.6,
            marker=dict(
                colors=self.colors[:len(self.labels)],
                line=dict(color=self.theme['background'], width=3)
            ),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=13, family='Poppins', color=self.theme['text']),
            hovertemplate='<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>',
            pull=[0.1] + [0] * (len(self.labels) - 1),  # Separar primera sección
            rotation=45
        )])

        # Agregar texto central con total
        total = sum(self.values)
        self.fig.add_annotation(
            text=f"<b>{total:,}</b><br>Total",
            x=0.5, y=0.5,
            font=dict(size=28, family='Poppins', color=self.theme['text']),
            showarrow=False
        )

        # Layout
        layout = self._get_layout()
        layout.update(
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=1.1
            )
        )
        self.fig.update_layout(**layout)

        self._display_plotly()

    def _show_error(self):
        """Mostrar error si Plotly no está disponible"""
        ctk.CTkLabel(
            self.chart_container,
            text="⚠️ Plotly no está instalado",
            font=('Poppins', 12),
            text_color='#ff6b6b'
        ).pack(expand=True)


class ModernAreaChart(ModernPlotlyChart):
    """
    Gráfica de área con gradiente

    Features:
    - Relleno con gradiente
    - Línea suave
    - Puntos resaltados
    - Animación de entrada
    """

    def __init__(self, parent, title: str, labels: list, values: list,
                 line_color: str = '#667eea', fill_gradient: bool = True, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título
            labels: Etiquetas (eje X)
            values: Valores (eje Y)
            line_color: Color de la línea
            fill_gradient: Usar gradiente en el relleno
        """
        super().__init__(parent, title, **kwargs)

        self.labels = labels
        self.values = values
        self.line_color = line_color
        self.fill_gradient = fill_gradient

        self.render()

    def render(self):
        """Renderizar gráfica de área"""
        if not PLOTLY_AVAILABLE:
            self._show_error()
            return

        self.fig = go.Figure()

        # Área con gradiente
        self.fig.add_trace(go.Scatter(
            x=self.labels,
            y=self.values,
            mode='lines',
            line=dict(
                color=self.line_color,
                width=4
            ),
            fill='tonexty',
            fillgradient=dict(
                type='vertical',
                colorscale=[
                    [0, f'{self.line_color}'],
                    [1, f'rgba{self.line_color[3:-1]}, 0)']
                ]
            ) if self.fill_gradient else None,
            hovertemplate='<b>%{x}</b><br>Valor: %{y:,}<extra></extra>'
        ))

        # Puntos resaltados
        self.fig.add_trace(go.Scatter(
            x=self.labels,
            y=self.values,
            mode='markers',
            marker=dict(
                color='white',
                size=10,
                line=dict(color=self.line_color, width=3)
            ),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Layout
        self.fig.update_layout(**self._get_layout())
        self.fig.update_layout(showlegend=False)

        self._display_plotly()

    def _show_error(self):
        """Mostrar error"""
        ctk.CTkLabel(
            self.chart_container,
            text="⚠️ Plotly no disponible",
            font=('Poppins', 12),
            text_color='#ff6b6b'
        ).pack(expand=True)


# Nota: Para usar estas gráficas Plotly, necesitas instalar:
# pip install plotly kaleido tkinterweb
