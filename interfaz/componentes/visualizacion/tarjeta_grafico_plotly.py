"""
Componente PlotlyChartCard - Card con gráficos Plotly con vista previa
"""
import customtkinter as ctk
import plotly.graph_objects as go
from tkinter import messagebox
import os
import tempfile
from PIL import Image

try:
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class PlotlyChartCard(ctk.CTkFrame):
    """Card con vista previa de gráficos Plotly interactivos"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            width: Ancho del card
            height: Altura del card
        """
        super().__init__(
            parent,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=1,
            border_color='#3a3d5c',
            **kwargs
        )

        self.current_fig = None
        self.chart_html_path = None
        self.chart_image_path = None
        self._title = title
        self._width = width
        self._height = height

        # Header si hay título
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Segoe UI', 16, 'bold'),
                text_color='#ffffff',
                anchor='w'
            )
            title_label.pack(side='left', fill='x', expand=True)

            # Botón abrir en navegador
            open_btn = ctk.CTkButton(
                header,
                text='🌐',
                font=('Segoe UI', 14),
                width=35,
                height=28,
                fg_color='#3a3d5c',
                hover_color='#4a4d6c',
                corner_radius=8,
                command=self._open_in_browser
            )
            open_btn.pack(side='right')

        # Container para el gráfico
        self.chart_container = ctk.CTkFrame(self, fg_color='#1a1d2e', corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_figure(self, fig, preview_width=800, preview_height=500):
        """
        Establecer figura de Plotly con vista previa

        Args:
            fig: Figura de Plotly (go.Figure)
            preview_width: Ancho de la imagen de vista previa
            preview_height: Altura de la imagen de vista previa
        """
        if not PLOTLY_AVAILABLE:
            self._show_error("Plotly no está instalado")
            return

        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # Aplicar configuración de tema oscuro
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#1a1d2e',
            plot_bgcolor='#1a1d2e',
            font=dict(color='#a0a0b0', size=11, family='Segoe UI'),
            margin=dict(l=50, r=30, t=30, b=50),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(58, 61, 92, 0.8)',
                bordercolor='#4a4d6c',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(
                gridcolor='rgba(160, 160, 176, 0.1)',
                linecolor='#3a3d5c',
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(160, 160, 176, 0.1)',
                linecolor='#3a3d5c',
                showgrid=True,
                zeroline=False
            ),
            hoverlabel=dict(
                bgcolor='#1a1d2e',
                font_size=11,
                font_family='Segoe UI',
                bordercolor='#6c63ff'
            )
        )

        self.current_fig = fig

        # Crear HTML temporal
        self._create_html()

        # Intentar crear vista previa
        try:
            self._create_preview(preview_width, preview_height)
        except Exception as e:
            print(f"Error creando vista previa: {e}")
            # Fallback a placeholder
            self._show_placeholder()

    def _create_preview(self, width, height):
        """Crear vista previa como imagen PNG"""
        # Crear archivo temporal para la imagen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_image_path = f.name

        try:
            # Exportar figura a imagen usando kaleido
            self.current_fig.write_image(
                temp_image_path,
                width=width,
                height=height,
                scale=1.5  # Mayor resolución
            )

            self.chart_image_path = temp_image_path

            # Cargar imagen con PIL
            pil_image = Image.open(temp_image_path)

            # Obtener dimensiones del container
            self.chart_container.update_idletasks()
            container_width = self.chart_container.winfo_width()
            container_height = self.chart_container.winfo_height()

            # Si el container aún no tiene tamaño, usar valores predeterminados
            if container_width <= 1:
                container_width = 600
            if container_height <= 1:
                container_height = 400

            # Calcular tamaño de la imagen manteniendo aspecto
            img_width, img_height = pil_image.size
            aspect_ratio = img_width / img_height
            container_aspect = container_width / container_height

            if aspect_ratio > container_aspect:
                # Imagen más ancha que el container
                new_width = int(container_width * 0.95)
                new_height = int(new_width / aspect_ratio)
            else:
                # Imagen más alta que el container
                new_height = int(container_height * 0.95)
                new_width = int(new_height * aspect_ratio)

            # Redimensionar imagen
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Crear CTkImage
            ctk_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(new_width, new_height)
            )

            # Mostrar imagen en label
            image_label = ctk.CTkLabel(
                self.chart_container,
                image=ctk_image,
                text=''
            )
            image_label.image = ctk_image  # Mantener referencia
            image_label.pack(expand=True)

            # Mensaje informativo pequeño
            info_label = ctk.CTkLabel(
                self.chart_container,
                text='💡 Haz clic en 🌐 para vista interactiva',
                font=('Segoe UI', 9),
                text_color='#6c6c80'
            )
            info_label.pack(pady=(5, 0))

        except ImportError:
            # kaleido no está instalado
            self._show_kaleido_error()
        except Exception as e:
            print(f"Error al generar imagen: {e}")
            self._show_placeholder()

    def _create_html(self):
        """Crear archivo HTML temporal del gráfico"""
        if not self.current_fig:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            config = {
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'displaylogo': False,
                'responsive': True
            }

            html_content = self.current_fig.to_html(
                include_plotlyjs='cdn',
                config=config,
                div_id='plotly_chart'
            )

            html_content = html_content.replace(
                '<head>',
                '<head><style>body{margin:0;background-color:#1a1d2e;overflow:auto;}</style>'
            )

            f.write(html_content)
            self.chart_html_path = f.name

    def _show_placeholder(self):
        """Mostrar placeholder cuando no se puede generar vista previa"""
        placeholder = ctk.CTkLabel(
            self.chart_container,
            text=f"📊 {self._title or 'Gráfico'} generado\n\n"
                 f"Haz clic en 🌐 para abrir en navegador",
            font=('Segoe UI', 12),
            text_color='#a0a0b0',
            justify='center'
        )
        placeholder.pack(expand=True)

    def _show_kaleido_error(self):
        """Mostrar mensaje de error cuando kaleido no está instalado"""
        error_frame = ctk.CTkFrame(self.chart_container, fg_color='transparent')
        error_frame.pack(expand=True)

        error_label = ctk.CTkLabel(
            error_frame,
            text="⚠️ Vista previa no disponible",
            font=('Segoe UI', 14, 'bold'),
            text_color='#ff8c42'
        )
        error_label.pack(pady=(0, 10))

        info_label = ctk.CTkLabel(
            error_frame,
            text="Para habilitar vistas previas, instala:\npip install kaleido",
            font=('Segoe UI', 11),
            text_color='#a0a0b0',
            justify='center'
        )
        info_label.pack(pady=(0, 15))

        browser_label = ctk.CTkLabel(
            error_frame,
            text="Haz clic en 🌐 para ver en navegador",
            font=('Segoe UI', 10),
            text_color='#6c63ff'
        )
        browser_label.pack()

    def _open_in_browser(self):
        """Abrir gráfico en navegador"""
        if not self.chart_html_path or not os.path.exists(self.chart_html_path):
            messagebox.showwarning("Sin Gráfico", "No hay ningún gráfico para mostrar")
            return

        try:
            os.startfile(self.chart_html_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el navegador:\n{str(e)}")

    def _show_error(self, message):
        """Muestra un mensaje de error"""
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

        # Limpiar archivos temporales
        if self.chart_html_path and os.path.exists(self.chart_html_path):
            try:
                os.remove(self.chart_html_path)
            except:
                pass
            self.chart_html_path = None

        if self.chart_image_path and os.path.exists(self.chart_image_path):
            try:
                os.remove(self.chart_image_path)
            except:
                pass
            self.chart_image_path = None
