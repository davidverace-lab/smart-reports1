"""
MatplotlibChartCard - Preview estático para dashboards
Usa Matplotlib embebido en tkinter - 100% confiable
Al hacer clic en expandir, se abre modal D3.js interactivo
"""
import customtkinter as ctk
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS

# Importar modal D3.js (con fallback si no está disponible)
try:
    from smart_reports.ui.components.charts.modal_d3_fullscreen import ModalD3Fullscreen, TKINTERWEB_AVAILABLE
except ImportError:
    TKINTERWEB_AVAILABLE = False
    ModalD3Fullscreen = None


class MatplotlibChartCard(ctk.CTkFrame):
    """
    Tarjeta con gráfico Matplotlib estático

    Características:
    - Renderizado 100% confiable dentro de la app
    - Gráficos estáticos profesionales
    - Colores Hutchison personalizados
    - Botones para fullscreen (D3.js interactivo) y navegador
    """

    def __init__(self, parent, title='', width=500, height=400, on_fullscreen=None, chart_engine='nvd3', **kwargs):
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15,
            border_width=1,
            border_color=theme['colors']['border'],
            **kwargs
        )

        self._title = title
        self._width = width
        self._height = height
        self.chart_engine = chart_engine  # 'nvd3' (default) o 'd3'
        self.on_fullscreen = on_fullscreen

        # Estado
        self.is_expanded = False
        self.chart_type = None
        self.chart_data = None
        self.chart_subtitle = None
        self.chart_url = None  # URL del D3.js para fullscreen

        # Referencias
        self.html_frame = None  # Frame para gráfico D3/NVD3 expandido
        self.canvas_widget = None  # Widget del canvas de matplotlib
        self.chart_container = None  # Contenedor del gráfico

        # Crear UI
        self._create_header()
        self._create_content_area()

    def _create_header(self):
        """Crear header del card"""
        if not self._title:
            return

        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=self._title,
            font=('Montserrat', 16, 'bold'),
            text_color=theme['colors']['text'],
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)

        # Badges
        badge_frame = ctk.CTkFrame(header, fg_color='transparent')
        badge_frame.pack(side='right')

        # Badge Matplotlib
        matplotlib_badge = ctk.CTkLabel(
            badge_frame,
            text='Matplotlib',
            font=('Montserrat', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            text_color='white',
            corner_radius=6,
            width=90,
            height=24
        )
        matplotlib_badge.pack(side='left', padx=5)

        # Botón fullscreen (D3.js interactivo)
        if self.on_fullscreen:
            fullscreen_btn = ctk.CTkButton(
                badge_frame,
                text='⛶',
                font=('Montserrat', 14, 'bold'),
                fg_color=HUTCHISON_COLORS['aqua_green'],
                hover_color='#00b386',
                text_color='white',
                corner_radius=6,
                width=35,
                height=28,
                command=self._trigger_fullscreen
            )
            fullscreen_btn.pack(side='left', padx=5)

        # Botón navegador
        browser_btn = ctk.CTkButton(
            badge_frame,
            text='🌐',
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#001a3d',
            text_color='white',
            corner_radius=6,
            width=35,
            height=28,
            command=self._open_in_browser
        )
        browser_btn.pack(side='left', padx=5)

    def _create_content_area(self):
        """Crear área de contenido para matplotlib"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color=theme['colors']['background'] if is_dark else '#f8f9fa',
            corner_radius=10
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_chart(self, chart_type, datos, subtitulo='', d3_url=None):
        """
        Establecer gráfico

        Args:
            chart_type: 'bar', 'donut', 'line', 'area'
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            d3_url: URL del D3.js para fullscreen/navegador
        """
        # Guardar datos
        self.chart_type = chart_type
        self.chart_data = datos
        self.chart_subtitle = subtitulo
        self.chart_url = d3_url

        # Limpiar contenido anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Crear figura matplotlib
        is_dark = self.theme_manager.is_dark_mode()

        # Configurar estilo
        if is_dark:
            plt.style.use('dark_background')
            fig_color = '#1e1e1e'
            text_color = '#ffffff'
        else:
            plt.style.use('default')
            fig_color = '#f8f9fa'
            text_color = '#000000'

        # Crear figura
        fig = Figure(figsize=(self._width/100, self._height/100), dpi=100, facecolor=fig_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(fig_color)

        # Generar gráfico según tipo
        if chart_type == 'bar':
            self._create_bar_chart(ax, datos, text_color)
        elif chart_type == 'donut':
            self._create_donut_chart(ax, datos, text_color)
        elif chart_type == 'line':
            self._create_line_chart(ax, datos, text_color)
        elif chart_type == 'area':
            self._create_area_chart(ax, datos, text_color)

        # Ajustar layout
        fig.tight_layout()

        # Embeber en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.content_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

        print(f"✅ Matplotlib {chart_type} renderizado")

    def _create_bar_chart(self, ax, datos, text_color):
        """Crear gráfico de barras"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear barras con color Hutchison
        bars = ax.barh(labels, values, color=HUTCHISON_COLORS['primary'])

        # Agregar valores en las barras
        for i, (bar, value) in enumerate(zip(bars, values)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f' {value:,}',
                   ha='left', va='center',
                   color=text_color, fontsize=9)

        # Estilo
        ax.set_xlabel('Cantidad', color=text_color, fontsize=11)
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _create_donut_chart(self, ax, datos, text_color):
        """Crear gráfico de dona"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Colores Hutchison
        colors = [
            HUTCHISON_COLORS['primary'],
            HUTCHISON_COLORS['primary'],
            HUTCHISON_COLORS['aqua_green'],
            HUTCHISON_COLORS['info'],
            '#ffa94d',
            '#51cf66'
        ]

        # Extender colores si es necesario
        while len(colors) < len(values):
            colors.extend(colors)
        colors = colors[:len(values)]

        # Crear dona
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90,
            textprops={'color': text_color, 'fontsize': 9},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        # Hacer dona (círculo en el centro)
        centre_circle = plt.Circle((0, 0), 0.70, fc=ax.get_facecolor(), linewidth=0)
        ax.add_artist(centre_circle)

        ax.axis('equal')

    def _create_line_chart(self, ax, datos, text_color):
        """Crear gráfico de líneas"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear línea
        x = np.arange(len(labels))
        ax.plot(x, values, color=HUTCHISON_COLORS['primary'],
               linewidth=2.5, marker='o', markersize=6,
               markerfacecolor=HUTCHISON_COLORS['primary'],
               markeredgecolor='white', markeredgewidth=1.5)

        # Etiquetas
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', color=text_color, fontsize=9)
        ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        # Estilo
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _create_area_chart(self, ax, datos, text_color):
        """Crear gráfico de área"""
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Crear área
        x = np.arange(len(labels))
        ax.fill_between(x, values, alpha=0.4, color=HUTCHISON_COLORS['primary'])
        ax.plot(x, values, color=HUTCHISON_COLORS['primary'],
               linewidth=2.5, marker='o', markersize=6,
               markerfacecolor=HUTCHISON_COLORS['primary'],
               markeredgecolor='white', markeredgewidth=1.5)

        # Etiquetas
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', color=text_color, fontsize=9)
        ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

        # Estilo
        ax.tick_params(colors=text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(text_color)
        ax.spines['bottom'].set_color(text_color)

    def _trigger_fullscreen(self):
        """Expandir/contraer gráfico D3.js/NVD3.js in-place"""
        if not self.chart_type or not self.chart_data:
            print("⚠️ No hay datos de gráfico para expandir")
            return

        if not TKINTERWEB_AVAILABLE:
            print("⚠️ tkinterweb no disponible - no se puede expandir a D3/NVD3")
            if self.on_fullscreen and self.chart_url:
                self.on_fullscreen(self.chart_url)
            return

        # Toggle entre estado expandido y compacto
        if self.is_expanded:
            self._collapse_chart()
        else:
            self._expand_chart()

    def _expand_chart(self):
        """Expandir gráfico a vista interactiva D3/NVD3"""
        try:
            engine_name = "NVD3.js" if self.chart_engine == 'nvd3' else "D3.js"
            print(f"  📊 Expandiendo a {engine_name} interactivo: {self._title}")

            # Ocultar canvas de matplotlib
            if self.canvas_widget:
                self.canvas_widget.pack_forget()

            # Generar HTML con el motor seleccionado
            from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3
            from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3

            Motor = MotorTemplatesNVD3 if self.chart_engine == 'nvd3' else MotorTemplatesD3
            chart_theme = 'dark' if self.theme_manager.get_current_theme()['name'] == 'dark' else 'light'

            # Generar HTML según tipo de gráfico
            if self.chart_type in ['bar', 'horizontal_bar']:
                html = Motor.generar_grafico_barras(
                    titulo="",
                    datos=self.chart_data,
                    subtitulo="",
                    tema=chart_theme,
                    interactivo=True if self.chart_engine == 'd3' else None
                )
            elif self.chart_type == 'donut':
                html = Motor.generar_grafico_donut(
                    titulo="",
                    datos=self.chart_data,
                    subtitulo="",
                    tema=chart_theme
                )
            elif self.chart_type == 'line':
                html = Motor.generar_grafico_lineas(
                    titulo="",
                    datos=self.chart_data,
                    subtitulo="",
                    tema=chart_theme
                )
            elif self.chart_type == 'area':
                html = Motor.generar_grafico_area(
                    titulo="",
                    datos=self.chart_data,
                    subtitulo="",
                    tema=chart_theme
                )
            else:
                html = Motor.generar_grafico_barras(
                    titulo="",
                    datos=self.chart_data,
                    tema=chart_theme
                )

            # Crear HtmlFrame si no existe
            from tkinterweb import HtmlFrame

            if self.html_frame is None:
                self.html_frame = HtmlFrame(
                    self.chart_container,
                    messages_enabled=False
                )

            # Cargar HTML
            self.html_frame.load_html(html)
            self.html_frame.pack(fill='both', expand=True)

            # Actualizar estado
            self.is_expanded = True

            # Cambiar texto del botón a "Volver"
            self._update_expand_button_text("↙")

            print(f"  ✅ Expandido a vista {engine_name} interactiva")

        except Exception as e:
            print(f"❌ Error expandiendo gráfico: {e}")
            import traceback
            traceback.print_exc()
            # Restaurar canvas si falla
            if self.canvas_widget:
                self.canvas_widget.pack(fill='both', expand=True)

    def _collapse_chart(self):
        """Colapsar gráfico a vista compacta Matplotlib"""
        try:
            print(f"  📉 Colapsando a vista compacta: {self._title}")

            # Ocultar HtmlFrame
            if self.html_frame:
                self.html_frame.pack_forget()

            # Mostrar canvas de matplotlib
            if self.canvas_widget:
                self.canvas_widget.pack(fill='both', expand=True)

            # Actualizar estado
            self.is_expanded = False

            # Cambiar texto del botón a "Expandir"
            self._update_expand_button_text("↗")

            print(f"  ✅ Colapsado a vista Matplotlib")

        except Exception as e:
            print(f"❌ Error colapsando gráfico: {e}")
            import traceback
            traceback.print_exc()

    def _update_expand_button_text(self, text):
        """Actualizar texto del botón de expandir"""
        try:
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkButton) and (grandchild.cget("text") in ["↗", "↙"]):
                            grandchild.configure(text=text)
                            return
        except Exception as e:
            pass  # Ignorar errores

    def _fallback_fullscreen(self):
        """Fallback original si falla la expansión in-place"""
        if self.on_fullscreen and self.chart_url:
            self.on_fullscreen(
                title=self._title,
                chart_type=self.chart_type,
                data=self.chart_data,
                subtitle=self.chart_subtitle,
                url=self.chart_url
            )
            print(f"  ⛶ Usando callback fullscreen externo para: {self._title}")
        else:
            print("⚠️ tkinterweb no disponible y no hay callback fullscreen definido")

    def _open_in_browser(self):
        """Abrir gráfico D3.js en navegador"""
        if not self.chart_url:
            return

        try:
            import webbrowser
            webbrowser.open(self.chart_url)
            print(f"  🌐 Abierto en navegador: {self.chart_url}")
        except Exception as e:
            print(f"  ❌ Error abriendo navegador: {e}")

    def clear(self):
        """Limpiar gráfico"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.chart_url = None
        self.chart_data = None
