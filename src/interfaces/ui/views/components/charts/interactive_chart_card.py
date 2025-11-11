"""
InteractiveChartCard - Gráfico Matplotlib TOTALMENTE interactivo
- Tooltips al pasar mouse
- Click para ordenar ascendente/descendente
- Click en leyenda para ocultar/mostrar elementos
- Zoom con scroll
"""
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS
import numpy as np


class InteractiveChartCard(ctk.CTkFrame):
    """Tarjeta con gráfico Matplotlib TOTALMENTE interactivo"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self._width = width
        self._height = height
        self.title_text = title

        # Estado del gráfico
        self.chart_type = None
        self.chart_data = None
        self.original_data = None  # Backup de datos originales
        self.hidden_items = set()  # Items ocultos por usuario
        self.sort_order = 'desc'  # 'asc' o 'desc'

        # Referencias
        self.canvas = None
        self.fig = None
        self.ax = None
        self.bars = None
        self.annotation = None  # Tooltip flotante

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de la tarjeta"""
        theme = self.theme_manager.get_current_theme()

        # Card container
        self.card = ctk.CTkFrame(
            self,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=1,
            border_color=theme['border']
        )
        self.card.pack(fill='both', expand=True)

        # Header
        header = ctk.CTkFrame(self.card, fg_color='transparent', height=50)
        header.pack(fill='x', padx=15, pady=(15, 5))
        header.pack_propagate(False)

        # Título
        title_label = ctk.CTkLabel(
            header,
            text=self.title_text,
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)

        # Botones de control
        controls = ctk.CTkFrame(header, fg_color='transparent')
        controls.pack(side='right')

        # Botón ordenar
        self.sort_btn = ctk.CTkButton(
            controls,
            text="↓ Desc",
            width=70,
            height=30,
            font=('Segoe UI', 11),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            command=self._toggle_sort
        )
        self.sort_btn.pack(side='left', padx=5)

        # Botón resetear
        reset_btn = ctk.CTkButton(
            controls,
            text="↻ Reset",
            width=70,
            height=30,
            font=('Segoe UI', 11),
            fg_color='#666666',
            hover_color='#555555',
            command=self._reset_chart
        )
        reset_btn.pack(side='left', padx=5)

        # Container para el gráfico
        self.content_container = ctk.CTkFrame(
            self.card,
            fg_color='transparent'
        )
        self.content_container.pack(fill='both', expand=True, padx=15, pady=(5, 15))

    def set_chart(self, chart_type, datos, subtitulo=''):
        """
        Establecer datos del gráfico

        Args:
            chart_type: 'bar', 'donut', 'line', 'area'
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Texto descriptivo
        """
        self.chart_type = chart_type
        self.original_data = {
            'labels': datos['labels'].copy(),
            'values': datos['values'].copy()
        }
        self.chart_data = datos
        self.hidden_items = set()
        self.sort_order = 'desc'

        self._render_chart()

    def _render_chart(self):
        """Renderizar el gráfico"""
        # Limpiar canvas anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Obtener tema
        theme = self.theme_manager.get_current_theme()
        bg_color = theme['background']
        text_color = theme['text']

        # Crear figura
        self.fig = Figure(figsize=(self._width/100, self._height/100), facecolor=bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(bg_color)

        # Renderizar según tipo
        if self.chart_type == 'bar':
            self._create_interactive_bar_chart(text_color)
        elif self.chart_type == 'donut':
            self._create_interactive_donut_chart(text_color)
        elif self.chart_type == 'line':
            self._create_interactive_line_chart(text_color)

        # Aplicar estilo
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(text_color)
        self.ax.spines['bottom'].set_color(text_color)
        self.ax.tick_params(colors=text_color)

        # Ajustar layout
        self.fig.tight_layout()

        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Conectar eventos de mouse
        self.canvas.mpl_connect('motion_notify_event', self._on_hover)
        self.canvas.mpl_connect('button_press_event', self._on_click)

    def _create_interactive_bar_chart(self, text_color):
        """Crear gráfico de barras interactivo"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Filtrar items ocultos
        filtered_labels = []
        filtered_values = []
        for i, label in enumerate(labels):
            if label not in self.hidden_items:
                filtered_labels.append(label)
                filtered_values.append(values[i])

        if not filtered_labels:
            filtered_labels = labels
            filtered_values = values
            self.hidden_items = set()

        # Colores Hutchison
        colors = [
            HUTCHISON_COLORS['ports_sea_blue'],
            HUTCHISON_COLORS['ports_sky_blue'],
            HUTCHISON_COLORS['aqua_green'],
            HUTCHISON_COLORS['sunset_orange'],
            '#003D8F', '#00A3E0', '#7CC576', '#FFB84D'
        ] * 10

        # Crear barras horizontales
        y_pos = np.arange(len(filtered_labels))
        self.bars = self.ax.barh(y_pos, filtered_values, color=colors[:len(filtered_labels)])

        # Configurar ejes
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(filtered_labels, fontsize=10)
        self.ax.set_xlabel('Cantidad', color=text_color, fontsize=11)
        self.ax.invert_yaxis()

        # Agregar valores al final de las barras
        for i, (bar, val) in enumerate(zip(self.bars, filtered_values)):
            self.ax.text(
                val + max(filtered_values) * 0.02,
                bar.get_y() + bar.get_height()/2,
                f'{int(val)}',
                va='center',
                fontsize=10,
                fontweight='bold',
                color=text_color
            )

        # Grid sutil
        self.ax.grid(axis='x', alpha=0.3, linestyle='--')

    def _create_interactive_donut_chart(self, text_color):
        """Crear gráfico donut interactivo"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Filtrar items ocultos
        filtered_labels = []
        filtered_values = []
        for i, label in enumerate(labels):
            if label not in self.hidden_items:
                filtered_labels.append(label)
                filtered_values.append(values[i])

        if not filtered_labels:
            filtered_labels = labels
            filtered_values = values
            self.hidden_items = set()

        # Colores
        colors = [
            HUTCHISON_COLORS['ports_sea_blue'],
            HUTCHISON_COLORS['aqua_green'],
            HUTCHISON_COLORS['sunset_orange'],
            HUTCHISON_COLORS['ports_sky_blue'],
            '#003D8F', '#7CC576', '#FFB84D'
        ] * 10

        # Crear donut
        wedges, texts, autotexts = self.ax.pie(
            filtered_values,
            labels=filtered_labels,
            colors=colors[:len(filtered_labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': text_color, 'fontsize': 10}
        )

        # Hacer donut (círculo en el centro)
        centre_circle = plt.Circle((0, 0), 0.70, fc=self.ax.get_facecolor())
        self.ax.add_artist(centre_circle)

        # Guardar wedges para interactividad
        self.bars = wedges

        self.ax.axis('equal')

    def _create_interactive_line_chart(self, text_color):
        """Crear gráfico de línea interactivo"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Filtrar items ocultos (si alguno)
        if self.hidden_items:
            filtered_labels = []
            filtered_values = []
            for i, label in enumerate(labels):
                if label not in self.hidden_items:
                    filtered_labels.append(label)
                    filtered_values.append(values[i])
        else:
            filtered_labels = labels
            filtered_values = values

        # Crear línea
        self.ax.plot(
            filtered_labels,
            filtered_values,
            marker='o',
            linewidth=2.5,
            markersize=8,
            color=HUTCHISON_COLORS['ports_sea_blue'],
            markerfacecolor=HUTCHISON_COLORS['aqua_green'],
            markeredgewidth=2,
            markeredgecolor=HUTCHISON_COLORS['ports_sea_blue']
        )

        # Área bajo la línea
        self.ax.fill_between(
            range(len(filtered_labels)),
            filtered_values,
            alpha=0.2,
            color=HUTCHISON_COLORS['ports_sky_blue']
        )

        # Configurar ejes
        self.ax.set_xticks(range(len(filtered_labels)))
        self.ax.set_xticklabels(filtered_labels, rotation=45, ha='right', fontsize=9)
        self.ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        self.ax.grid(alpha=0.3, linestyle='--')

    def _on_hover(self, event):
        """Manejar evento de hover del mouse"""
        if event.inaxes != self.ax or not self.bars:
            if self.annotation:
                self.annotation.set_visible(False)
                self.canvas.draw_idle()
            return

        # Detectar si el mouse está sobre una barra
        for i, bar in enumerate(self.bars):
            if self.chart_type == 'bar':
                contains, _ = bar.contains(event)
                if contains:
                    self._show_tooltip(event, i)
                    return
            elif self.chart_type == 'donut':
                contains, _ = bar.contains(event)
                if contains:
                    self._show_tooltip(event, i)
                    return

        # Si no está sobre ninguna barra, ocultar tooltip
        if self.annotation:
            self.annotation.set_visible(False)
            self.canvas.draw_idle()

    def _show_tooltip(self, event, index):
        """Mostrar tooltip con información"""
        labels = [l for l in self.chart_data['labels'] if l not in self.hidden_items]
        values = [v for i, v in enumerate(self.chart_data['values'])
                  if self.chart_data['labels'][i] not in self.hidden_items]

        if index >= len(labels):
            return

        label = labels[index]
        value = values[index]

        # Crear o actualizar tooltip
        if not self.annotation:
            self.annotation = self.ax.annotate(
                '', xy=(0, 0), xytext=(20, 20),
                textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.5", fc=HUTCHISON_COLORS['ports_sea_blue'], alpha=0.95),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='white', lw=2),
                fontsize=11,
                color='white',
                fontweight='bold'
            )

        self.annotation.set_text(f"{label}\n{int(value)} usuarios")
        self.annotation.xy = (event.xdata, event.ydata)
        self.annotation.set_visible(True)
        self.canvas.draw_idle()

    def _on_click(self, event):
        """Manejar click en elementos del gráfico"""
        if event.inaxes != self.ax or not self.bars:
            return

        # Click en barra para ocultar/mostrar
        for i, bar in enumerate(self.bars):
            contains, _ = bar.contains(event)
            if contains:
                labels = self.chart_data['labels']
                if i < len(labels):
                    label = labels[i]
                    if label in self.hidden_items:
                        self.hidden_items.remove(label)
                    else:
                        self.hidden_items.add(label)
                    self._render_chart()
                    break

    def _toggle_sort(self):
        """Cambiar orden de datos"""
        if self.sort_order == 'desc':
            self.sort_order = 'asc'
            self.sort_btn.configure(text="↑ Asc")
        else:
            self.sort_order = 'desc'
            self.sort_btn.configure(text="↓ Desc")

        # Ordenar datos
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Crear pares y ordenar
        pairs = list(zip(labels, values))
        pairs.sort(key=lambda x: x[1], reverse=(self.sort_order == 'desc'))

        # Actualizar datos
        self.chart_data['labels'] = [p[0] for p in pairs]
        self.chart_data['values'] = [p[1] for p in pairs]

        self._render_chart()

    def _reset_chart(self):
        """Resetear gráfico a estado original"""
        self.chart_data = {
            'labels': self.original_data['labels'].copy(),
            'values': self.original_data['values'].copy()
        }
        self.hidden_items = set()
        self.sort_order = 'desc'
        self.sort_btn.configure(text="↓ Desc")
        self._render_chart()
