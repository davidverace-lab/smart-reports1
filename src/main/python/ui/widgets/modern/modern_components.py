"""
Componentes Modernos con Gradientes y Animaciones
Sistema de UI moderno para dashboards
"""
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from src.main.res.config.gestor_temas import get_theme_manager
from src.main.python.ui.widgets.animations import AnimationEngine, EasingFunctions, create_gradient_colors
import math


class ModernMetricCard(ctk.CTkFrame):
    """
    Card moderna con gradiente, icono y animación

    Features:
    - Gradiente de fondo
    - Icono con efecto glow
    - Valor animado al aparecer
    - Sparkline opcional
    - Hover effect
    """

    def __init__(self, parent, title: str, value: str, icon: str = "📊",
                 gradient_colors: tuple = ('#667eea', '#764ba2'),
                 change_percent: float = None,
                 sparkline_data: list = None,
                 **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título de la métrica
            value: Valor a mostrar
            icon: Emoji o icono
            gradient_colors: Tupla de 2 colores para el gradiente
            change_percent: Porcentaje de cambio (positivo/negativo)
            sparkline_data: Datos para mini gráfica de tendencia
        """
        theme = get_theme_manager().get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=20,
            **kwargs
        )

        self.title = title
        self.value = value
        self.icon = icon
        self.gradient_colors = gradient_colors
        self.change_percent = change_percent
        self.sparkline_data = sparkline_data
        self.theme = theme

        # Estado
        self.is_hovered = False

        # Crear UI
        self._create_ui()

        # Animación de entrada
        self.animator = AnimationEngine(self)
        self.after(100, lambda: self.animator.animate_scale(
            from_scale=0.8,
            to_scale=1.0,
            duration=500,
            easing=EasingFunctions.ease_out_back
        ))

        # Hover effects
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _create_ui(self):
        """Crear UI de la card"""
        # Canvas para gradiente de fondo
        self.bg_canvas = tk.Canvas(
            self,
            bg=self.theme['surface'],
            highlightthickness=0,
            height=200
        )
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Dibujar gradiente
        self._draw_gradient()

        # Container de contenido
        content_frame = ctk.CTkFrame(self, fg_color='transparent')
        content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Header con icono
        header_frame = ctk.CTkFrame(content_frame, fg_color='transparent', height=60)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        # Icono con efecto glow
        self.icon_label = ctk.CTkLabel(
            header_frame,
            text=self.icon,
            font=('Segoe UI Emoji', 36),
            text_color='white'
        )
        self.icon_label.pack(side='left')

        # Badge de cambio (si aplica)
        if self.change_percent is not None:
            self._create_change_badge(header_frame)

        # Título
        self.title_label = ctk.CTkLabel(
            content_frame,
            text=self.title,
            font=('Poppins', 12),
            text_color='rgba(255,255,255,0.8)',
            anchor='w'
        )
        self.title_label.pack(fill='x', padx=20, pady=(0, 5))

        # Valor principal
        self.value_label = ctk.CTkLabel(
            content_frame,
            text=self.value,
            font=('Poppins', 38, 'bold'),
            text_color='white',
            anchor='w'
        )
        self.value_label.pack(fill='x', padx=20, pady=(0, 10))

        # Sparkline (si hay datos)
        if self.sparkline_data:
            self._create_sparkline(content_frame)

    def _draw_gradient(self):
        """Dibuja gradiente en el canvas"""
        width = 400  # Ancho aproximado
        height = 200

        # Crear gradiente vertical
        steps = 50
        gradient_colors = create_gradient_colors(
            self.gradient_colors[0],
            self.gradient_colors[1],
            steps
        )

        step_height = height / steps
        for i, color in enumerate(gradient_colors):
            self.bg_canvas.create_rectangle(
                0, i * step_height,
                width, (i + 1) * step_height,
                fill=color,
                outline=''
            )

        # Borde brillante (glassmorphism)
        self.bg_canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            outline='rgba(255,255,255,0.2)',
            width=2
        )

    def _create_change_badge(self, parent):
        """Crear badge de cambio porcentual"""
        is_positive = self.change_percent >= 0
        bg_color = '#51cf66' if is_positive else '#ff6b6b'
        arrow = '↑' if is_positive else '↓'

        badge = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=12,
            height=28
        )
        badge.pack(side='right')
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text=f'{arrow} {abs(self.change_percent):.1f}%',
            font=('Poppins', 11, 'bold'),
            text_color='white'
        ).pack(padx=12, pady=4)

    def _create_sparkline(self, parent):
        """Crear mini gráfica de tendencia"""
        canvas = tk.Canvas(
            parent,
            bg='transparent',
            highlightthickness=0,
            height=40
        )
        canvas.pack(fill='x', padx=20, pady=(0, 15))

        # Esperar a que el canvas tenga tamaño
        def draw():
            width = canvas.winfo_width()
            if width <= 1:
                canvas.after(100, draw)
                return

            height = 40
            data = self.sparkline_data

            if not data or len(data) < 2:
                return

            # Normalizar datos
            min_val = min(data)
            max_val = max(data)
            range_val = max_val - min_val if max_val != min_val else 1

            # Crear puntos
            points = []
            step_x = width / (len(data) - 1)
            for i, val in enumerate(data):
                x = i * step_x
                y = height - ((val - min_val) / range_val * (height - 10)) - 5
                points.extend([x, y])

            # Dibujar línea
            if len(points) >= 4:
                canvas.create_line(
                    points,
                    fill='white',
                    width=2,
                    smooth=True
                )

                # Área bajo la curva
                area_points = [0, height] + points + [width, height]
                canvas.create_polygon(
                    area_points,
                    fill='white',
                    outline='',
                    stipple='gray50'  # Transparencia simulada
                )

        canvas.after(100, draw)

    def _on_enter(self, event):
        """Hover effect - entrar"""
        self.is_hovered = True
        # Efecto de elevación
        self.configure(border_width=2, border_color='white')

    def _on_leave(self, event):
        """Hover effect - salir"""
        self.is_hovered = False
        self.configure(border_width=0)

    def update_value(self, new_value: str, animate: bool = True):
        """Actualizar valor con animación opcional"""
        if animate:
            # Si es número, animar contador
            try:
                old_num = float(self.value.replace(',', '').replace('%', ''))
                new_num = float(str(new_value).replace(',', '').replace('%', ''))

                def update_label(current):
                    self.value_label.configure(text=f'{current:,.0f}')

                animator = AnimationEngine(self)
                animator.animate_value(
                    old_num, new_num,
                    duration=800,
                    update_callback=update_label
                )
            except:
                self.value_label.configure(text=new_value)
        else:
            self.value_label.configure(text=new_value)

        self.value = new_value


class CircularProgress(ctk.CTkFrame):
    """
    Indicador de progreso circular animado

    Features:
    - Animación de entrada
    - Gradiente en el arco
    - Texto central
    - Glow effect
    """

    def __init__(self, parent, percentage: int = 0, size: int = 140,
                 label: str = "Progreso", color: str = '#667eea', **kwargs):
        """
        Args:
            parent: Widget padre
            percentage: Porcentaje (0-100)
            size: Tamaño del círculo
            label: Etiqueta inferior
            color: Color del progreso
        """
        theme = get_theme_manager().get_current_theme()

        super().__init__(
            parent,
            fg_color='transparent',
            width=size,
            height=size,
            **kwargs
        )
        self.pack_propagate(False)

        self.percentage = percentage
        self.size = size
        self.label = label
        self.color = color
        self.theme = theme

        # Canvas para dibujar
        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg=theme['background'],
            highlightthickness=0
        )
        self.canvas.pack()

        # Variables de animación
        self.current_percentage = 0
        self.arc = None

        # Dibujar
        self._draw_base()
        self._draw_progress()

        # Animar entrada
        self.after(200, lambda: self._animate_to(percentage))

    def _draw_base(self):
        """Dibujar círculo base"""
        padding = 15
        size = self.size - padding * 2

        # Círculo de fondo (oscuro)
        self.canvas.create_oval(
            padding, padding,
            self.size - padding, self.size - padding,
            outline=self.theme['border'],
            width=12,
            fill=''
        )

        # Texto central - porcentaje
        self.percentage_text = self.canvas.create_text(
            self.size / 2, self.size / 2 - 12,
            text='0%',
            font=('Poppins', 32, 'bold'),
            fill='white'
        )

        # Texto central - label
        self.canvas.create_text(
            self.size / 2, self.size / 2 + 20,
            text=self.label,
            font=('Poppins', 11),
            fill=self.theme['text_secondary']
        )

    def _draw_progress(self):
        """Dibujar arco de progreso"""
        padding = 15
        extent = -(360 * self.current_percentage / 100)

        if self.arc:
            self.canvas.delete(self.arc)

        self.arc = self.canvas.create_arc(
            padding, padding,
            self.size - padding, self.size - padding,
            start=90,
            extent=extent,
            outline=self.color,
            width=12,
            style='arc'
        )

        # Actualizar texto
        self.canvas.itemconfig(
            self.percentage_text,
            text=f'{int(self.current_percentage)}%'
        )

    def _animate_to(self, target_percentage: int):
        """Animar a un porcentaje objetivo"""
        def update(current):
            self.current_percentage = current
            self._draw_progress()

        animator = AnimationEngine(self)
        animator.animate_value(
            0, target_percentage,
            duration=1500,
            easing=EasingFunctions.ease_out_cubic,
            update_callback=update
        )

    def update_percentage(self, new_percentage: int):
        """Actualizar porcentaje con animación"""
        old = self.current_percentage

        def update(current):
            self.current_percentage = current
            self._draw_progress()

        animator = AnimationEngine(self)
        animator.animate_value(
            old, new_percentage,
            duration=800,
            easing=EasingFunctions.ease_out_cubic,
            update_callback=update
        )


class ModernButton(ctk.CTkButton):
    """
    Botón moderno con gradiente y animaciones

    Features:
    - Gradiente de fondo
    - Hover effect suave
    - Ripple effect al hacer click
    - Icon + Text
    """

    def __init__(self, parent, text: str = "", icon: str = None,
                 gradient_colors: tuple = ('#667eea', '#764ba2'),
                 **kwargs):
        """
        Args:
            parent: Widget padre
            text: Texto del botón
            icon: Icono emoji (opcional)
            gradient_colors: Colores del gradiente
        """
        # Combinar icono y texto
        display_text = f"{icon}  {text}" if icon else text

        super().__init__(
            parent,
            text=display_text,
            font=('Poppins', 13, 'bold'),
            fg_color=gradient_colors[0],
            hover_color=gradient_colors[1],
            corner_radius=15,
            height=50,
            border_width=0,
            **kwargs
        )

        self.gradient_colors = gradient_colors

        # Bind para efectos
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)

    def _on_enter(self, event):
        """Hover effect"""
        # Efecto de elevación
        self.configure(cursor='hand2')

    def _on_leave(self, event):
        """Salir del hover"""
        self.configure(cursor='')

    def _on_click(self, event):
        """Click effect - ripple"""
        # Animación de escala
        original_height = self.cget('height')

        def shrink():
            self.configure(height=original_height - 4)
            self.after(50, grow)

        def grow():
            self.configure(height=original_height)

        shrink()


class GlassCard(ctk.CTkFrame):
    """
    Card con efecto glassmorphism

    Features:
    - Fondo semi-transparente
    - Blur simulado
    - Borde brillante
    - Hover effect
    """

    def __init__(self, parent, **kwargs):
        """
        Args:
            parent: Widget padre
        """
        theme = get_theme_manager().get_current_theme()

        super().__init__(
            parent,
            fg_color=theme['surface'],
            corner_radius=20,
            border_width=1,
            border_color='rgba(255,255,255,0.1)',
            **kwargs
        )

        # Efecto hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_enter(self, event):
        """Hover effect"""
        self.configure(border_color='rgba(255,255,255,0.3)')

    def _on_leave(self, event):
        """Salir del hover"""
        self.configure(border_color='rgba(255,255,255,0.1)')


class ModernTooltip:
    """
    Tooltip moderno con animación

    Features:
    - Fade in/out suave
    - Posicionamiento inteligente
    - Estilo glassmorphism
    """

    def __init__(self, widget, text: str, delay: int = 500):
        """
        Args:
            widget: Widget al que se le agrega el tooltip
            text: Texto del tooltip
            delay: Delay antes de mostrar (ms)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        widget.bind('<Enter>', self.schedule_tooltip)
        widget.bind('<Leave>', self.hide_tooltip)

    def schedule_tooltip(self, event):
        """Programar mostrar tooltip"""
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self):
        """Mostrar tooltip con animación"""
        if self.tooltip_window:
            return

        # Posición
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        # Crear ventana
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes('-alpha', 0.0)  # Iniciar transparente

        # Frame con estilo
        frame = ctk.CTkFrame(
            self.tooltip_window,
            fg_color='#667eea',
            corner_radius=12,
            border_width=2,
            border_color='white'
        )
        frame.pack()

        # Label
        label = ctk.CTkLabel(
            frame,
            text=self.text,
            font=('Poppins', 11),
            text_color='white'
        )
        label.pack(padx=15, pady=8)

        # Animar fade in
        self._fade_in()

    def _fade_in(self, alpha=0.0):
        """Animación fade in"""
        if alpha < 0.95:
            self.tooltip_window.attributes('-alpha', alpha)
            self.tooltip_window.after(20, lambda: self._fade_in(alpha + 0.1))
        else:
            self.tooltip_window.attributes('-alpha', 0.95)

    def hide_tooltip(self, event=None):
        """Ocultar tooltip"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
