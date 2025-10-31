"""
Componente ChartCard - Card con gráficos Plotly interactivos
"""
import customtkinter as ctk
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from tkinter import filedialog, messagebox
import os

try:
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Warning: Plotly no está disponible.")


class ChartCard(ctk.CTkFrame):
    """Card para mostrar gráficos con Plotly interactivos"""

    def __init__(self, parent, title, chart_type='bar', width=400, height=300, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            chart_type: Tipo de gráfico ('bar', 'horizontal_bar', 'donut', 'line', 'area', 'stacked_bar')
            width: Ancho del card
            height: Altura del card
        """
        super().__init__(
            parent,
            fg_color='#2b2d42',
            corner_radius=20,
            border_width=1,
            border_color='#3a3d5c',
            width=width,
            height=height,
            **kwargs
        )

        self.chart_type = chart_type
        self.current_fig = None
        self.chart_html_path = None

        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=('Segoe UI', 18, 'bold'),
            text_color='#ffffff',
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)

        # Botón de exportar
        export_btn = ctk.CTkButton(
            header,
            text='💾',
            font=('Segoe UI', 16),
            width=40,
            height=30,
            fg_color='#3a3d5c',
            hover_color='#4a4d6c',
            corner_radius=8,
            command=self._export_chart
        )
        export_btn.pack(side='right', padx=(10, 0))

        # Container para el gráfico
        self.chart_container = ctk.CTkFrame(self, fg_color='transparent')
        self.chart_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    def create_chart(self, data, labels=None, data2=None, data3=None):
        """
        Crea el gráfico con Plotly interactivo

        Args:
            data: Datos principales (lista de números)
            labels: Etiquetas para el eje x o segmentos (lista de strings)
            data2: Datos secundarios para gráficos apilados (opcional)
            data3: Datos terciarios para gráficos apilados (opcional)
        """
        if not PLOTLY_AVAILABLE:
            self._show_error("Plotly no está instalado")
            return

        # Limpiar gráfico anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Crear figura de Plotly
        fig = go.Figure()

        # Configurar colores modernos
        colors = ['#ffd93d', '#6c63ff', '#4ecdc4', '#ff6b6b', '#51cf66', '#ff8c42', '#a78bfa', '#fb923c']

        if self.chart_type == 'bar':
            fig.add_trace(go.Bar(
                x=labels if labels else list(range(len(data))),
                y=data,
                marker=dict(
                    color=colors[:len(data)],
                    line=dict(color='#2b2d42', width=2)
                ),
                text=data,
                textposition='outside',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{x}</b><br>Valor: %{y}<extra></extra>'
            ))

        elif self.chart_type == 'horizontal_bar':
            fig.add_trace(go.Bar(
                x=data,
                y=labels if labels else list(range(len(data))),
                orientation='h',
                marker=dict(
                    color=colors[:len(data)],
                    line=dict(color='#2b2d42', width=2)
                ),
                text=data,
                textposition='outside',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{y}</b><br>Valor: %{x}<extra></extra>'
            ))

        elif self.chart_type == 'donut':
            fig.add_trace(go.Pie(
                labels=labels,
                values=data,
                hole=0.5,
                marker=dict(
                    colors=colors[:len(data)],
                    line=dict(color='#2b2d42', width=3)
                ),
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>Valor: %{value}<br>Porcentaje: %{percent}<extra></extra>'
            ))

        elif self.chart_type == 'line':
            fig.add_trace(go.Scatter(
                x=labels if labels else list(range(len(data))),
                y=data,
                mode='lines+markers',
                line=dict(color='#6c63ff', width=3),
                marker=dict(
                    size=10,
                    color='#ffd93d',
                    line=dict(color='#6c63ff', width=2)
                ),
                fill='tonexty',
                fillcolor='rgba(108, 99, 255, 0.3)',
                hovertemplate='<b>%{x}</b><br>Valor: %{y}<extra></extra>'
            ))

        elif self.chart_type == 'area':
            fig.add_trace(go.Scatter(
                x=labels if labels else list(range(len(data))),
                y=data,
                mode='lines',
                line=dict(color='#4ecdc4', width=2),
                fill='tozeroy',
                fillcolor='rgba(78, 205, 196, 0.6)',
                hovertemplate='<b>%{x}</b><br>Valor: %{y}<extra></extra>'
            ))

        elif self.chart_type == 'stacked_bar':
            x_labels = labels if labels else list(range(len(data)))

            fig.add_trace(go.Bar(
                x=x_labels,
                y=data,
                name='Completado',
                marker=dict(color='#51cf66', line=dict(color='#2b2d42', width=2)),
                hovertemplate='<b>%{x}</b><br>Completado: %{y}<extra></extra>'
            ))

            if data2 is not None:
                fig.add_trace(go.Bar(
                    x=x_labels,
                    y=data2,
                    name='En Progreso',
                    marker=dict(color='#ffd93d', line=dict(color='#2b2d42', width=2)),
                    hovertemplate='<b>%{x}</b><br>En Progreso: %{y}<extra></extra>'
                ))

            if data3 is not None:
                fig.add_trace(go.Bar(
                    x=x_labels,
                    y=data3,
                    name='Registrado',
                    marker=dict(color='#6c6c80', line=dict(color='#2b2d42', width=2)),
                    hovertemplate='<b>%{x}</b><br>Registrado: %{y}<extra></extra>'
                ))

            fig.update_layout(barmode='stack')

        # Configurar layout con tema oscuro
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#2b2d42',
            plot_bgcolor='#2b2d42',
            font=dict(color='#a0a0b0', size=11),
            margin=dict(l=40, r=20, t=20, b=40),
            height=250,
            showlegend=(self.chart_type == 'stacked_bar'),
            legend=dict(
                bgcolor='rgba(58, 61, 92, 0.9)',
                bordercolor='#4a4d6c',
                borderwidth=1,
                font=dict(color='white')
            ),
            xaxis=dict(
                gridcolor='rgba(160, 160, 176, 0.1)',
                linecolor='#3a3d5c',
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(160, 160, 176, 0.1)',
                linecolor='#3a3d5c',
                showgrid=True
            ),
            hoverlabel=dict(
                bgcolor='#1a1d2e',
                font_size=12,
                font_family='Segoe UI'
            )
        )

        # Guardar figura
        self.current_fig = fig

        # Crear HTML temporal y mostrarlo
        self._display_plotly_chart(fig)

        return fig

    def _display_plotly_chart(self, fig):
        """Muestra el gráfico de Plotly usando un widget HTML"""
        import tempfile

        # Crear archivo HTML temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            # Configurar para no mostrar la barra de herramientas de Plotly
            config = {
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'displaylogo': False
            }

            html_content = fig.to_html(
                include_plotlyjs='cdn',
                config=config,
                div_id='plotly_chart'
            )

            # Agregar estilos personalizados para hacer el fondo transparente
            html_content = html_content.replace(
                '<head>',
                '<head><style>body{margin:0;background-color:#2b2d42;overflow:hidden;}</style>'
            )

            f.write(html_content)
            self.chart_html_path = f.name

        # Mostrar en un frame con texto explicativo
        # (Nota: tkinter no soporta nativamente HTML, así que mostramos un placeholder)
        placeholder = ctk.CTkLabel(
            self.chart_container,
            text=f"📊 Gráfico {self.chart_type.upper()} generado\n\n"
                 f"⚠️ Vista previa no disponible en esta versión\n"
                 f"Haz clic en 💾 para exportar a imagen",
            font=('Segoe UI', 12),
            text_color='#a0a0b0',
            justify='center'
        )
        placeholder.pack(fill='both', expand=True)

        # Botón para abrir en navegador
        open_btn = ctk.CTkButton(
            self.chart_container,
            text='🌐 Abrir en Navegador',
            font=('Segoe UI', 12),
            fg_color='#6c63ff',
            hover_color='#5a52d5',
            command=lambda: os.startfile(self.chart_html_path)
        )
        open_btn.pack(pady=10)

    def _export_chart(self):
        """Exporta el gráfico actual a imagen"""
        if not self.current_fig:
            messagebox.showwarning("Sin Gráfico", "No hay ningún gráfico para exportar")
            return

        try:
            # Solicitar ubicación para guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("SVG Image", "*.svg"),
                    ("PDF", "*.pdf")
                ],
                title="Guardar Gráfico"
            )

            if file_path:
                # Exportar con kaleido
                self.current_fig.write_image(file_path, width=1200, height=800)
                messagebox.showinfo("Éxito", f"Gráfico exportado a:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar gráfico:\n{str(e)}")

    def _show_error(self, message):
        """Muestra un mensaje de error en el contenedor del gráfico"""
        error_label = ctk.CTkLabel(
            self.chart_container,
            text=f"❌ {message}",
            font=('Segoe UI', 14),
            text_color='#ff6b6b'
        )
        error_label.pack(fill='both', expand=True)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.current_fig = None
        if self.chart_html_path and os.path.exists(self.chart_html_path):
            try:
                os.remove(self.chart_html_path)
            except:
                pass
            self.chart_html_path = None
