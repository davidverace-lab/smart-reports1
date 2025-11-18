"""
Modal Fullscreen para Gráficos - ANIMACIÓN DESLIZANTE DESDE ABAJO
✨ CARACTERÍSTICAS:
- Ventana modal oscura con overlay
- Gráfico GIGANTE (1200x800)
- Animación de entrada deslizante desde abajo
- Botón cerrar elegante (X) + tecla ESC
- Mismas interactividades que el gráfico pequeño
"""
import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.res.config.themes import HUTCHISON_COLORS
import numpy as np


class ModalFullscreenChart(ctk.CTkToplevel):
    """Modal fullscreen para mostrar gráficos ampliados"""

    def __init__(self, parent, title, chart_type, chart_data, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme_manager = get_theme_manager()
        self.title_text = title
        self.chart_type = chart_type
        self.chart_data = chart_data

        # Estado
        self.hover_index = -1
        self.hidden_items = set()
        self.sort_order = 'desc'
        self.original_data = {
            'labels': chart_data['labels'].copy(),
            'values': chart_data['values'].copy()
        }

        # Referencias
        self.canvas = None
        self.fig = None
        self.ax = None
        self.bars = None
        self.annotation = None

        # Configurar ventana modal
        self._setup_window()
        self._create_ui()
        self._animate_entrance()

        # Capturar tecla ESC
        self.bind('<Escape>', lambda e: self._close_modal())

    def _setup_window(self):
        """Configurar ventana modal"""
        # Fullscreen
        self.attributes('-fullscreen', False)  # No fullscreen nativo
        self.attributes('-topmost', True)

        # Tamaño casi fullscreen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 95% de la pantalla
        width = int(screen_width * 0.95)
        height = int(screen_height * 0.95)

        # Centrar
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Estilo
        theme = self.theme_manager.get_current_theme()
        self.configure(fg_color=theme['background'])

        # Sin bordes de ventana
        self.overrideredirect(False)  # Mantener botones de ventana

        # Título de ventana
        self.title(f"📊 {self.title_text}")

    def _create_ui(self):
        """Crear interfaz del modal"""
        theme = self.theme_manager.get_current_theme()

        # === HEADER CON TÍTULO Y BOTÓN CERRAR ===
        header = ctk.CTkFrame(
            self,
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            height=80,
            corner_radius=0
        )
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        # Botón cerrar (izquierda)
        close_btn = ctk.CTkButton(
            header,
            text="✕ Cerrar",
            font=('Segoe UI', 16, 'bold'),
            fg_color='#003D8F',
            hover_color='#001a3d',
            command=self._close_modal,
            width=150,
            height=50,
            corner_radius=10
        )
        close_btn.pack(side='left', padx=30, pady=15)

        # Título (centro)
        title_label = ctk.CTkLabel(
            header,
            text=f"📊 {self.title_text}",
            font=('Segoe UI', 28, 'bold'),
            text_color='white'
        )
        title_label.pack(side='left', expand=True, padx=30)

        # Controles (derecha)
        controls = ctk.CTkFrame(header, fg_color='transparent')
        controls.pack(side='right', padx=30)

        # Botón ordenar
        self.sort_btn = ctk.CTkButton(
            controls,
            text="↓ Desc",
            width=100,
            height=40,
            font=('Segoe UI', 13, 'bold'),
            fg_color='#00B5E2',
            hover_color='#009BDE',
            command=self._toggle_sort
        )
        self.sort_btn.pack(side='left', padx=5)

        # Botón reset
        reset_btn = ctk.CTkButton(
            controls,
            text="↻ Reset",
            width=100,
            height=40,
            font=('Segoe UI', 13, 'bold'),
            fg_color='#666666',
            hover_color='#555555',
            command=self._reset_chart
        )
        reset_btn.pack(side='left', padx=5)

        # Indicador de elementos ocultos
        self.hidden_indicator = ctk.CTkLabel(
            controls,
            text="",
            font=('Segoe UI', 12, 'bold'),
            text_color='#ff9800'
        )
        self.hidden_indicator.pack(side='left', padx=15)

        # === CONTAINER PARA EL GRÁFICO GIGANTE ===
        self.chart_container = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        self.chart_container.pack(fill='both', expand=True, padx=30, pady=30)

        # Renderizar gráfico
        self._render_chart()

    def _render_chart(self):
        """Renderizar el gráfico gigante"""
        # Limpiar canvas anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Obtener tema
        theme = self.theme_manager.get_current_theme()
        bg_color = theme['background']
        text_color = theme['text']

        # Crear figura GIGANTE
        self.fig = Figure(figsize=(16, 10), dpi=100, facecolor=bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(bg_color)

        # Renderizar según tipo
        if self.chart_type == 'bar':
            self._create_bar_chart_fullscreen(text_color)
        elif self.chart_type == 'donut':
            self._create_donut_chart_fullscreen(text_color)
        elif self.chart_type == 'line':
            self._create_line_chart_fullscreen(text_color)

        # Aplicar estilo
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(text_color)
        self.ax.spines['bottom'].set_color(text_color)
        self.ax.tick_params(colors=text_color, labelsize=12)

        # Ajustar layout
        self.fig.tight_layout()

        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Conectar eventos
        self.canvas.mpl_connect('motion_notify_event', self._on_hover)
        self.canvas.mpl_connect('button_press_event', self._on_click)

    def _create_bar_chart_fullscreen(self, text_color):
        """Crear gráfico de barras GIGANTE con efectos PRO"""
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

        # Actualizar indicador
        if self.hidden_items:
            self.hidden_indicator.configure(text=f"👁️ {len(self.hidden_items)} ocultos")
        else:
            self.hidden_indicator.configure(text="")

        # Gradientes profesionales
        gradient_colors = [
            ('#003D82', '#009BDE'),
            ('#0052A3', '#00B5E2'),
            ('#004C97', '#33C7F0'),
            ('#003D82', '#66D4F5'),
            ('#002E6D', '#009BDE'),
            ('#0066CC', '#00B5E2'),
            ('#0080FF', '#33C7F0'),
            ('#004C97', '#99E1FA'),
        ]

        y_pos = np.arange(len(filtered_labels))
        self.bars = []

        for i, (y, val) in enumerate(zip(y_pos, filtered_values)):
            color_start, color_end = gradient_colors[i % len(gradient_colors)]

            # Barra principal
            bar = self.ax.barh(
                y, val,
                height=0.65,
                color=color_end,
                edgecolor='white',
                linewidth=2,
                alpha=0.95,
                zorder=3
            )

            # Sombra
            self.ax.barh(
                y - 0.025, val * 0.97,
                height=0.65,
                color='#000000',
                alpha=0.2,
                zorder=1
            )

            self.bars.append(bar[0])

        # Configurar ejes
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(filtered_labels, fontsize=14, fontweight='600')
        self.ax.set_xlabel('Cantidad', color=text_color, fontsize=16, fontweight='700')
        self.ax.invert_yaxis()

        # Grid
        self.ax.grid(axis='x', alpha=0.2, linestyle='--', linewidth=1.2, color=text_color)
        self.ax.set_axisbelow(True)

        # Valores en las barras
        max_val = max(filtered_values) if filtered_values else 1
        for bar, val in zip(self.bars, filtered_values):
            self.ax.text(
                val + max_val * 0.02,
                bar.get_y() + bar.get_height()/2,
                f'{int(val):,}',
                va='center',
                fontsize=14,
                fontweight='bold',
                color=HUTCHISON_COLORS['ports_sea_blue']
            )

        if filtered_values:
            self.ax.set_xlim(0, max(filtered_values) * 1.15)

    def _create_donut_chart_fullscreen(self, text_color):
        """Crear gráfico donut GIGANTE"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        # Filtrar
        filtered_labels = [l for i, l in enumerate(labels) if l not in self.hidden_items]
        filtered_values = [v for i, v in enumerate(values) if labels[i] not in self.hidden_items]

        if not filtered_labels:
            filtered_labels, filtered_values = labels, values
            self.hidden_items = set()

        if self.hidden_items:
            self.hidden_indicator.configure(text=f"👁️ {len(self.hidden_items)} ocultos")
        else:
            self.hidden_indicator.configure(text="")

        # Colores profesionales
        colors = ['#003D82', '#0052A3', '#009BDE', '#00B5E2', '#33C7F0', '#66D4F5', '#0066CC', '#0080FF']

        # Crear donut
        wedges, texts, autotexts = self.ax.pie(
            filtered_values,
            labels=filtered_labels,
            colors=colors[:len(filtered_labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': text_color, 'fontsize': 13, 'fontweight': '700'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'alpha': 0.95},
            pctdistance=0.85
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(14)

        # Círculo central
        centre = plt.Circle((0, 0), 0.68, fc=self.ax.get_facecolor(), edgecolor='white', linewidth=4)
        self.ax.add_artist(centre)

        # Total
        total = sum(filtered_values)
        self.ax.text(0, 0.1, f'{int(total):,}', ha='center', va='center', fontsize=32,
                    fontweight='bold', color=HUTCHISON_COLORS['ports_sky_blue'])
        self.ax.text(0, -0.2, 'TOTAL', ha='center', va='center', fontsize=14,
                    fontweight='700', color=text_color, alpha=0.7)

        self.bars = wedges
        self.ax.axis('equal')

    def _create_line_chart_fullscreen(self, text_color):
        """Crear gráfico de línea GIGANTE"""
        labels = self.chart_data['labels']
        values = self.chart_data['values']

        filtered_labels = [l for i, l in enumerate(labels) if l not in self.hidden_items]
        filtered_values = [v for i, v in enumerate(values) if labels[i] not in self.hidden_items]

        if not filtered_labels:
            filtered_labels, filtered_values = labels, values

        self.ax.plot(filtered_labels, filtered_values, marker='o', linewidth=4, markersize=14,
                    color='#003D82', markerfacecolor='#33C7F0', markeredgewidth=3,
                    markeredgecolor='#003D82', alpha=0.95, linestyle='-', solid_capstyle='round')

        self.ax.fill_between(range(len(filtered_labels)), filtered_values, alpha=0.3,
                            color='#009BDE', linewidth=0)

        self.ax.set_xticks(range(len(filtered_labels)))
        self.ax.set_xticklabels(filtered_labels, rotation=45, ha='right', fontsize=13)
        self.ax.set_ylabel('Valor', color=text_color, fontsize=16, fontweight='700')
        self.ax.grid(alpha=0.25, linestyle='--', linewidth=1)

    def _on_hover(self, event):
        """Hover con efectos dramáticos"""
        if event.inaxes != self.ax or not self.bars:
            if self.hover_index != -1:
                self._reset_bar_effects()
            if self.annotation:
                self.annotation.set_visible(False)
                self.canvas.draw_idle()
            return

        found = False
        for i, bar in enumerate(self.bars):
            contains, _ = bar.contains(event)
            if contains:
                if self.hover_index != i:
                    self._apply_hover_effect(i)
                self._show_tooltip(event, i)
                found = True
                break

        if not found and self.hover_index != -1:
            self._reset_bar_effects()
            if self.annotation:
                self.annotation.set_visible(False)
                self.canvas.draw_idle()

    def _apply_hover_effect(self, index):
        """Aplicar hover effect"""
        self.hover_index = index
        for i, bar in enumerate(self.bars):
            if i == index:
                bar.set_alpha(1.0)
                bar.set_edgecolor('yellow')
                bar.set_linewidth(3.5)
            else:
                bar.set_alpha(0.3)
        self.canvas.draw_idle()

    def _reset_bar_effects(self):
        """Resetear efectos"""
        self.hover_index = -1
        for bar in self.bars:
            bar.set_alpha(0.95)
            bar.set_edgecolor('white')
            bar.set_linewidth(2.5 if self.chart_type == 'donut' else 2)
        self.canvas.draw_idle()

    def _show_tooltip(self, event, index):
        """Tooltip hermoso con instrucción para ocultar"""
        labels = [l for l in self.chart_data['labels'] if l not in self.hidden_items]
        values = [v for i, v in enumerate(self.chart_data['values'])
                 if self.chart_data['labels'][i] not in self.hidden_items]

        if index >= len(labels):
            return

        label, value = labels[index], values[index]
        total = sum(values)
        percentage = (value / total * 100) if total > 0 else 0
        ranking = sorted(values, reverse=True).index(value) + 1

        if not self.annotation:
            self.annotation = self.ax.annotate(
                '', xy=(0, 0), xytext=(30, 30), textcoords="offset points",
                bbox=dict(boxstyle="round,pad=1.2", fc='#1a1d2e', ec=HUTCHISON_COLORS['ports_sky_blue'],
                         alpha=0.98, linewidth=3),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3',
                               color=HUTCHISON_COLORS['ports_sky_blue'], lw=3),
                fontsize=11, color='white', fontweight='700', zorder=1000
            )

        # Tooltip mejorado con instrucción de clic
        tooltip_text = (
            f"📊 {label}\n"
            f"{'─' * 26}\n"
            f"👥 {int(value):,} usuarios\n"
            f"📈 {percentage:.1f}% del total\n"
            f"🏆 Ranking: #{ranking}\n"
            f"{'─' * 26}\n"
            f"👆 Click para ocultar/mostrar"
        )
        self.annotation.set_text(tooltip_text)
        self.annotation.xy = (event.xdata, event.ydata)
        self.annotation.set_visible(True)
        self.canvas.draw_idle()

    def _on_click(self, event):
        """Click para ocultar con efecto visual"""
        if event.inaxes != self.ax or not self.bars:
            return

        for i, bar in enumerate(self.bars):
            contains, _ = bar.contains(event)
            if contains:
                # Efecto visual de clic - parpadeo
                self._flash_click_effect(bar)

                labels = self.chart_data['labels']
                if i < len(labels):
                    label = labels[i]
                    if label in self.hidden_items:
                        self.hidden_items.remove(label)
                    else:
                        self.hidden_items.add(label)

                    # Pequeño delay para que se vea el efecto antes de re-renderizar
                    self.after(200, self._render_chart)
                    break

    def _flash_click_effect(self, bar):
        """Efecto de parpadeo al hacer clic"""
        try:
            # Guardar color original
            original_color = bar.get_facecolor()
            original_edge = bar.get_edgecolor()

            # Cambiar a color de clic
            bar.set_facecolor('#FFD700')  # Amarillo/dorado
            bar.set_edgecolor('#FFD700')
            bar.set_linewidth(4)
            self.canvas.draw_idle()

            # Restaurar después de 150ms (el re-render lo hará)
        except:
            pass

    def _toggle_sort(self):
        """Ordenar"""
        self.sort_order = 'asc' if self.sort_order == 'desc' else 'desc'
        self.sort_btn.configure(text="↑ Asc" if self.sort_order == 'asc' else "↓ Desc")

        labels, values = self.chart_data['labels'], self.chart_data['values']
        pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=(self.sort_order == 'desc'))
        self.chart_data['labels'] = [p[0] for p in pairs]
        self.chart_data['values'] = [p[1] for p in pairs]
        self._render_chart()

    def _reset_chart(self):
        """Resetear"""
        self.chart_data = {
            'labels': self.original_data['labels'].copy(),
            'values': self.original_data['values'].copy()
        }
        self.hidden_items = set()
        self.sort_order = 'desc'
        self.sort_btn.configure(text="↓ Desc")
        self._render_chart()

    def _animate_entrance(self):
        """Animar entrada deslizante desde abajo"""
        # Posición inicial (fuera de pantalla, abajo)
        screen_height = self.winfo_screenheight()
        self.geometry(f"+{self.winfo_x()}+{screen_height}")
        self.update()

        # Animar hacia arriba
        target_y = (screen_height - self.winfo_height()) // 2
        current_y = screen_height
        steps = 20
        delay = 10  # ms

        def animate_step(step):
            nonlocal current_y
            if step < steps:
                # Easing out (desaceleración suave)
                progress = step / steps
                ease = 1 - (1 - progress) ** 3  # Cubic ease-out
                current_y = screen_height - (screen_height - target_y) * ease
                self.geometry(f"+{self.winfo_x()}+{int(current_y)}")
                self.after(delay, lambda: animate_step(step + 1))
            else:
                self.geometry(f"+{self.winfo_x()}+{target_y}")

        self.after(50, lambda: animate_step(0))

    def _close_modal(self):
        """Cerrar modal con animación"""
        # Animar salida (opcional: hacia abajo)
        self.destroy()
