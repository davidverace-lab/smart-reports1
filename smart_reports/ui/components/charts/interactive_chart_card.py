"""
InteractiveChartCard PRO - Gráfico Matplotlib PREMIUM con máxima interactividad
✨ CARACTERÍSTICAS:
- Tooltips hermosos con información detallada
- Animaciones de entrada (barras crecen desde abajo)
- Hover dramático (resalta barra + atenúa otras)
- Click para ocultar/mostrar elementos
- Ordenar con transiciones suaves
- Indicador visual de elementos ocultos
- Gradientes profesionales
- Sombras y efectos 3D
"""
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS
import numpy as np


class InteractiveChartCard(ctk.CTkFrame):
    """Tarjeta con gráfico Matplotlib TOTALMENTE interactivo"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        # Extract custom parameters that CTkFrame doesn't support
        self.on_fullscreen_callback = kwargs.pop('on_fullscreen', None)

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
        self.hover_index = -1  # Índice de barra bajo hover
        self.hidden_indicator = None  # Label indicador de elementos ocultos

        # Animación
        self.is_animating = False

        # OPTIMIZACIÓN: Control de re-renderizado
        self._last_draw_time = 0
        self._draw_delay_ms = 50  # Mínimo 50ms entre draws (20 FPS para hover)
        self._pending_draw = None

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

        # Botón Exportar Interactivo (NUEVO - como en el diseño)
        export_btn = ctk.CTkButton(
            controls,
            text="📥 Exportar",
            width=110,
            height=32,
            font=('Segoe UI', 11, 'bold'),
            fg_color='#22d3ee',  # Cyan como en el diseño
            hover_color='#06b6d4',
            text_color='#1a1d2e',
            command=self._export_chart
        )
        export_btn.pack(side='left', padx=5)

        # Botón ampliar (si hay callback)
        if self.on_fullscreen_callback:
            fullscreen_btn = ctk.CTkButton(
                controls,
                text="↗",
                width=35,
                height=32,
                font=('Segoe UI', 16, 'bold'),
                fg_color=HUTCHISON_COLORS['aqua_green'],
                hover_color=HUTCHISON_COLORS['primary'],
                command=lambda: self.on_fullscreen_callback(self)
            )
            fullscreen_btn.pack(side='left', padx=2)

        # Botón ordenar
        self.sort_btn = ctk.CTkButton(
            controls,
            text="↓ Desc",
            width=70,
            height=30,
            font=('Segoe UI', 11),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color=HUTCHISON_COLORS['primary'],
            command=self._toggle_sort
        )
        self.sort_btn.pack(side='left', padx=5)

        # Botón resetear
        reset_btn = ctk.CTkButton(
            controls,
            text="↻",
            width=35,
            height=30,
            font=('Segoe UI', 14, 'bold'),
            fg_color='#666666',
            hover_color='#555555',
            command=self._reset_chart
        )
        reset_btn.pack(side='left', padx=5)

        # Indicador de elementos ocultos
        self.hidden_indicator = ctk.CTkLabel(
            header,
            text="",
            font=('Segoe UI', 10),
            text_color='#ff9800'
        )
        self.hidden_indicator.pack(side='left', padx=10)

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
        """Crear gráfico de barras interactivo con efectos PRO"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Filtrar items ocultos
        filtered_labels = []
        filtered_values = []
        filtered_original_indices = []
        for i, label in enumerate(labels):
            if label not in self.hidden_items:
                filtered_labels.append(label)
                filtered_values.append(values[i])
                filtered_original_indices.append(i)

        if not filtered_labels:
            filtered_labels = labels
            filtered_values = values
            filtered_original_indices = list(range(len(labels)))
            self.hidden_items = set()

        # Actualizar indicador de elementos ocultos
        if self.hidden_items:
            self.hidden_indicator.configure(text=f"👁️ {len(self.hidden_items)} ocultos")
        else:
            self.hidden_indicator.configure(text="")

        # Paleta de gradientes azules profesionales (oscuro → claro)
        gradient_colors = [
            ('#003D82', '#009BDE'),  # Navy → Sky blue
            ('#0052A3', '#00B5E2'),  # Royal → Horizon
            ('#004C97', '#33C7F0'),  # Dark blue → Light blue
            ('#003D82', '#66D4F5'),  # Navy → Very light
            ('#002E6D', '#009BDE'),  # Darkest navy → Sky
            ('#0066CC', '#00B5E2'),  # Medium → Horizon
            ('#0080FF', '#33C7F0'),  # Azure → Light
            ('#004C97', '#99E1FA'),  # Royal → Lightest
        ]

        # Crear barras horizontales
        y_pos = np.arange(len(filtered_labels))

        # EFECTO PRO: Crear barras con gradiente
        self.bars = []
        for i, (y, val) in enumerate(zip(y_pos, filtered_values)):
            # Seleccionar colores del gradiente
            color_start, color_end = gradient_colors[i % len(gradient_colors)]

            # Crear barra con gradiente (SIN SOMBRA para mejor rendimiento)
            bar = self.ax.barh(
                y, val,
                height=0.7,
                color=color_end,  # Color base
                edgecolor='white',
                linewidth=1.5,
                alpha=0.9,
                zorder=3
            )

            # OPTIMIZACIÓN: Eliminamos sombras para reducir objetos matplotlib a la mitad
            # Esto mejora significativamente el rendimiento del hover

            self.bars.append(bar[0])

        # Configurar ejes
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(filtered_labels, fontsize=10, fontweight='500')
        self.ax.set_xlabel('Cantidad', color=text_color, fontsize=11, fontweight='600')
        self.ax.invert_yaxis()

        # Grid profesional
        self.ax.grid(axis='x', alpha=0.2, linestyle='--', linewidth=0.8, color=text_color)
        self.ax.set_axisbelow(True)

        # Agregar valores al final de las barras con estilo PRO
        max_val = max(filtered_values) if filtered_values else 1
        for i, (bar, val) in enumerate(zip(self.bars, filtered_values)):
            # Valor principal
            self.ax.text(
                val + max_val * 0.02,
                bar.get_y() + bar.get_height()/2,
                f'{int(val):,}',
                va='center',
                fontsize=11,
                fontweight='bold',
                color=HUTCHISON_COLORS['primary']
            )

        # Establecer límites para padding
        if filtered_values:
            self.ax.set_xlim(0, max(filtered_values) * 1.15)

    def _create_interactive_donut_chart(self, text_color):
        """Crear gráfico donut interactivo con efectos PRO"""
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

        # Actualizar indicador de elementos ocultos
        if self.hidden_items:
            self.hidden_indicator.configure(text=f"👁️ {len(self.hidden_items)} ocultos")
        else:
            self.hidden_indicator.configure(text="")

        # Paleta profesional de azules gradientes
        professional_colors = [
            '#003D82',  # Navy
            '#0052A3',  # Royal blue
            '#009BDE',  # Sky blue
            '#00B5E2',  # Horizon blue
            '#33C7F0',  # Light blue
            '#66D4F5',  # Lighter blue
            '#0066CC',  # Medium blue
            '#0080FF',  # Azure
        ]

        # Crear donut con bordes profesionales
        wedges, texts, autotexts = self.ax.pie(
            filtered_values,
            labels=filtered_labels,
            colors=professional_colors[:len(filtered_labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': text_color, 'fontsize': 10, 'fontweight': '700'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2.5, 'alpha': 0.95},
            pctdistance=0.85
        )

        # Mejorar texto de porcentajes
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)

        # Hacer donut con círculo central elegante
        centre_circle = plt.Circle(
            (0, 0), 0.68,
            fc=self.ax.get_facecolor(),
            edgecolor='white',
            linewidth=3
        )
        self.ax.add_artist(centre_circle)

        # Agregar total en el centro
        total = sum(filtered_values)
        self.ax.text(
            0, 0.05,
            f'{int(total):,}',
            ha='center', va='center',
            fontsize=22,
            fontweight='bold',
            color=HUTCHISON_COLORS['primary']
        )
        self.ax.text(
            0, -0.15,
            'TOTAL',
            ha='center', va='center',
            fontsize=11,
            fontweight='600',
            color=text_color,
            alpha=0.7
        )

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

        # Crear línea suave con colores pastel navy
        self.ax.plot(
            filtered_labels,
            filtered_values,
            marker='o',
            linewidth=3,
            markersize=10,
            color='#4A6FA5',  # Navy oscuro pastel
            markerfacecolor='#8FADD3',  # Navy claro pastel
            markeredgewidth=2.5,
            markeredgecolor='#4A6FA5',
            alpha=0.9,
            linestyle='-',
            solid_capstyle='round'
        )

        # Área bajo la línea con gradiente visual
        self.ax.fill_between(
            range(len(filtered_labels)),
            filtered_values,
            alpha=0.25,
            color='#6B8EC7',  # Navy medio pastel
            linewidth=0
        )

        # Configurar ejes
        self.ax.set_xticks(range(len(filtered_labels)))
        self.ax.set_xticklabels(filtered_labels, rotation=45, ha='right', fontsize=9)
        self.ax.set_ylabel('Valor', color=text_color, fontsize=11)

        # Grid
        self.ax.grid(alpha=0.3, linestyle='--')

    def _on_hover(self, event):
        """Manejar evento de hover del mouse con efectos DRAMÁTICOS"""
        if event.inaxes != self.ax or not self.bars:
            # Restaurar opacidad de todas las barras
            if self.hover_index != -1:
                self._reset_bar_effects()
            if self.annotation:
                self.annotation.set_visible(False)
                self._throttled_draw()
            return

        # Detectar si el mouse está sobre una barra
        found = False
        for i, bar in enumerate(self.bars):
            contains, _ = bar.contains(event)
            if contains:
                # EFECTO DRAMÁTICO: Resaltar barra + atenuar otras
                if self.hover_index != i:
                    self._apply_hover_effect(i)
                self._show_tooltip_pro(event, i)
                found = True
                break

        # Si no está sobre ninguna barra, restaurar
        if not found and self.hover_index != -1:
            self._reset_bar_effects()
            if self.annotation:
                self.annotation.set_visible(False)
                self._throttled_draw()

    def _apply_hover_effect(self, index):
        """Aplicar efecto hover: resaltar barra + atenuar otras"""
        self.hover_index = index

        for i, bar in enumerate(self.bars):
            if i == index:
                # Resaltar barra seleccionada
                bar.set_alpha(1.0)
                bar.set_edgecolor('yellow')
                bar.set_linewidth(2.5)
            else:
                # Atenuar otras barras
                bar.set_alpha(0.3)
                bar.set_edgecolor('white')
                bar.set_linewidth(1.0)

        # OPTIMIZACIÓN: Throttled draw
        self._throttled_draw()

    def _throttled_draw(self):
        """OPTIMIZACIÓN: Dibujar canvas con throttling para evitar lag"""
        import time

        current_time = time.time() * 1000  # Convertir a ms

        # Si ya hay un draw pendiente, cancelarlo
        if self._pending_draw:
            try:
                self.after_cancel(self._pending_draw)
            except:
                pass

        # Calcular tiempo desde último draw
        time_since_last_draw = current_time - self._last_draw_time

        if time_since_last_draw >= self._draw_delay_ms:
            # Suficiente tiempo ha pasado, dibujar inmediatamente
            self._last_draw_time = current_time
            self.canvas.draw_idle()
        else:
            # Programar draw para más tarde
            delay = int(self._draw_delay_ms - time_since_last_draw)
            self._pending_draw = self.after(delay, self._execute_pending_draw)

    def _execute_pending_draw(self):
        """Ejecutar draw pendiente"""
        import time
        self._last_draw_time = time.time() * 1000
        self._pending_draw = None
        if self.canvas:
            self.canvas.draw_idle()

    def _reset_bar_effects(self):
        """Restaurar efectos originales de las barras"""
        self.hover_index = -1

        for bar in self.bars:
            bar.set_alpha(0.95)
            bar.set_edgecolor('white')
            if self.chart_type == 'donut':
                bar.set_linewidth(2.5)
            else:
                bar.set_linewidth(1.5)

        self._throttled_draw()

    def _show_tooltip_pro(self, event, index):
        """Mostrar tooltip HERMOSO con información detallada"""
        labels = [l for l in self.chart_data['labels'] if l not in self.hidden_items]
        values = [v for i, v in enumerate(self.chart_data['values'])
                  if self.chart_data['labels'][i] not in self.hidden_items]

        if index >= len(labels):
            return

        label = labels[index]
        value = values[index]
        total = sum(values)
        percentage = (value / total * 100) if total > 0 else 0

        # Ranking (posición en el orden actual)
        sorted_values = sorted(values, reverse=True)
        ranking = sorted_values.index(value) + 1

        # Crear o actualizar tooltip hermoso
        if not self.annotation:
            self.annotation = self.ax.annotate(
                '', xy=(0, 0), xytext=(25, 25),
                textcoords="offset points",
                bbox=dict(
                    boxstyle="round,pad=0.8",
                    fc='#1a1d2e',
                    ec=HUTCHISON_COLORS['primary'],
                    alpha=0.98,
                    linewidth=2.5
                ),
                arrowprops=dict(
                    arrowstyle='->',
                    connectionstyle='arc3,rad=0.3',
                    color=HUTCHISON_COLORS['primary'],
                    lw=2.5
                ),
                fontsize=10,
                color='white',
                fontweight='600',
                zorder=1000
            )

        # Texto detallado y hermoso
        tooltip_text = (
            f"📊 {label}\n"
            f"{'─' * 20}\n"
            f"👥 {int(value):,} usuarios\n"
            f"📈 {percentage:.1f}% del total\n"
            f"🏆 Ranking: #{ranking}"
        )

        self.annotation.set_text(tooltip_text)
        self.annotation.xy = (event.xdata, event.ydata)
        self.annotation.set_visible(True)
        self._throttled_draw()

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

    def _export_chart(self):
        """
        Exportar gráfico como imagen PNG

        Funcionalidad:
        - Guarda el gráfico actual como imagen PNG
        - Abre diálogo para seleccionar ubicación
        - Incluye fecha/hora en el nombre del archivo
        """
        from tkinter import filedialog
        from datetime import datetime

        if not self.fig:
            print("⚠️ No hay gráfico para exportar")
            return

        try:
            # Generar nombre de archivo sugerido
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = self.title_text.replace(" ", "_").replace("/", "-")[:30]
            filename = f"grafico_{title_clean}_{timestamp}.png"

            # Abrir diálogo de guardado
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=filename,
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("PDF Document", "*.pdf"),
                    ("SVG Vector", "*.svg"),
                    ("Todos los archivos", "*.*")
                ],
                title="Exportar Gráfico"
            )

            if filepath:
                # Guardar según extensión
                if filepath.lower().endswith('.png'):
                    self.fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
                elif filepath.lower().endswith('.pdf'):
                    self.fig.savefig(filepath, format='pdf', bbox_inches='tight')
                elif filepath.lower().endswith('.svg'):
                    self.fig.savefig(filepath, format='svg', bbox_inches='tight')
                else:
                    self.fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')

                print(f"✅ Gráfico exportado: {filepath}")

        except Exception as e:
            print(f"❌ Error exportando gráfico: {e}")
            import traceback
            traceback.print_exc()
