"""
PlotlyInteractiveChart - Componente para gráficos interactivos con Plotly
"""
import customtkinter as ctk
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import tkinter as tk
from tkinter import Canvas
import webbrowser
import tempfile
import os


class PlotlyInteractiveChart(ctk.CTkFrame):
    """Card con gráfico interactivo de Plotly embebido"""

    def __init__(self, parent, title='', **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
        """
        super().__init__(
            parent,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=1,
            border_color='#3a3d5c',
            **kwargs
        )

        self._title = title
        self.current_fig = None

        # Header si hay título
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Montserrat', 16, 'bold'),
                text_color='#ffffff',
                anchor='w'
            )
            title_label.pack(side='left', fill='x', expand=True)

            # Botón para abrir en navegador
            open_btn = ctk.CTkButton(
                header,
                text="🔗 Abrir Interactivo",
                font=('Arial', 11),
                fg_color='#009BDE',
                hover_color='#002E6D',
                corner_radius=8,
                height=30,
                width=150,
                command=self.open_in_browser
            )
            open_btn.pack(side='right')

        # Container para el gráfico
        self.chart_container = ctk.CTkFrame(self, fg_color='#1a1d2e', corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Placeholder
        self.placeholder_label = ctk.CTkLabel(
            self.chart_container,
            text="📊 Cargando gráfico interactivo...",
            font=('Arial', 14),
            text_color='#666666'
        )
        self.placeholder_label.pack(expand=True)

    def set_figure(self, fig):
        """
        Establecer figura de Plotly

        Args:
            fig: Figura de Plotly (plotly.graph_objects.Figure)
        """
        self.current_fig = fig

        # Remover placeholder
        self.placeholder_label.pack_forget()

        # Configurar tema oscuro para Plotly
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#1a1d2e',
            plot_bgcolor='#1a1d2e',
            font=dict(color='#a0a0b0', family='Arial'),
            title_font=dict(color='#ffffff', family='Montserrat', size=18),
            hoverlabel=dict(
                bgcolor='#2b2d42',
                font_size=12,
                font_family='Arial'
            ),
            margin=dict(l=50, r=50, t=60, b=50)
        )

        # Crear preview estático
        # Generar imagen preview
        try:
            import io
            from PIL import Image, ImageTk

            # Exportar como imagen
            img_bytes = fig.to_image(format="png", width=800, height=600)
            img = Image.open(io.BytesIO(img_bytes))

            # Convertir a PhotoImage
            photo = ImageTk.PhotoImage(img)

            # Mostrar en Canvas
            for widget in self.chart_container.winfo_children():
                widget.destroy()

            canvas = Canvas(
                self.chart_container,
                bg='#1a1d2e',
                highlightthickness=0
            )
            canvas.pack(fill='both', expand=True)

            # Centrar imagen
            canvas.create_image(
                canvas.winfo_reqwidth() // 2,
                canvas.winfo_reqheight() // 2,
                image=photo,
                anchor='center'
            )

            # Mantener referencia
            canvas.image = photo

            # Agregar hint de interactividad
            hint_label = ctk.CTkLabel(
                self.chart_container,
                text="💡 Haz clic en '🔗 Abrir Interactivo' para funciones completas",
                font=('Arial', 10),
                text_color='#666666'
            )
            hint_label.place(relx=0.5, rely=0.95, anchor='center')

        except Exception as e:
            print(f"Error generando preview: {e}")
            # Mostrar mensaje alternativo
            preview_label = ctk.CTkLabel(
                self.chart_container,
                text=f"📊 Gráfico: {self._title}\n\nHaz clic en '🔗 Abrir Interactivo' para visualizar",
                font=('Arial', 13),
                text_color='#ffffff',
                justify='center'
            )
            preview_label.pack(expand=True)

    def open_in_browser(self):
        """Abrir el gráfico interactivo en el navegador"""
        if self.current_fig is None:
            return

        try:
            # Crear archivo temporal HTML
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f'plotly_chart_{id(self)}.html')

            # Guardar figura como HTML
            self.current_fig.write_html(
                temp_file,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'hutchison_ports_{self._title}',
                        'height': 800,
                        'width': 1200,
                        'scale': 2
                    }
                }
            )

            # Abrir en navegador
            webbrowser.open(f'file://{temp_file}')

        except Exception as e:
            print(f"Error abriendo gráfico en navegador: {e}")

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        self.current_fig = None

        # Mostrar placeholder
        self.placeholder_label = ctk.CTkLabel(
            self.chart_container,
            text="📊 Sin gráfico",
            font=('Arial', 14),
            text_color='#666666'
        )
        self.placeholder_label.pack(expand=True)
