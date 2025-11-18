"""
Motor de Animaciones Fluidas - Smart Reports
Sistema de animaciones suaves con easing functions
"""
import math
from typing import Callable, Any


class EasingFunctions:
    """Funciones de easing para animaciones fluidas"""

    @staticmethod
    def linear(t: float) -> float:
        """Lineal - sin aceleración"""
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Aceleración cuadrática"""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Desaceleración cuadrática"""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Aceleración/desaceleración cuadrática"""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Aceleración cúbica"""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Desaceleración cúbica - MUY SUAVE"""
        return 1 - pow(1 - t, 3)

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Aceleración/desaceleración cúbica"""
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def ease_in_quart(t: float) -> float:
        """Aceleración cuártica"""
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t: float) -> float:
        """Desaceleración cuártica - EXTRA SUAVE"""
        return 1 - pow(1 - t, 4)

    @staticmethod
    def ease_in_out_quart(t: float) -> float:
        """Aceleración/desaceleración cuártica"""
        return 8 * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 4) / 2

    @staticmethod
    def ease_out_elastic(t: float) -> float:
        """Efecto elástico - rebote al final"""
        c4 = (2 * math.pi) / 3
        if t == 0 or t == 1:
            return t
        return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Efecto bounce - múltiples rebotes"""
        n1 = 7.5625
        d1 = 2.75

        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375

    @staticmethod
    def ease_in_back(t: float) -> float:
        """Retrocede un poco antes de avanzar"""
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t

    @staticmethod
    def ease_out_back(t: float) -> float:
        """Sobrepasa un poco al final"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


class AnimationEngine:
    """
    Motor de animaciones para widgets de CustomTkinter

    Uso:
        animator = AnimationEngine(widget)
        animator.animate_fade_in(duration=500)
        animator.animate_slide_in(direction='left', duration=300)
    """

    def __init__(self, widget):
        """
        Args:
            widget: Widget de CustomTkinter a animar
        """
        self.widget = widget
        self.running_animations = []

    def animate_fade_in(self, duration: int = 300, delay: int = 0,
                       easing: Callable = EasingFunctions.ease_out_cubic,
                       callback: Callable = None):
        """
        Anima fade in (aparecer)

        Args:
            duration: Duración en ms
            delay: Delay antes de iniciar en ms
            easing: Función de easing
            callback: Función a ejecutar al terminar
        """
        fps = 60
        frame_time = 1000 // fps
        total_frames = duration // frame_time
        current_frame = [0]

        # Guardar estado original
        original_state = {
            'visible': self.widget.winfo_ismapped()
        }

        def animate():
            if current_frame[0] <= total_frames:
                progress = current_frame[0] / total_frames
                eased = easing(progress)

                # Simular fade con configure (no todos los widgets soportan alpha)
                # Alternativa: usar place con relwidth/relheight
                try:
                    # Intentar con fg_color si es un Frame
                    current_color = self.widget.cget('fg_color')
                    if isinstance(current_color, str):
                        # Calcular color con alpha
                        pass  # CustomTkinter no soporta alpha directamente
                except:
                    pass

                current_frame[0] += 1
                self.widget.after(frame_time, animate)
            else:
                if callback:
                    callback()

        self.widget.after(delay, animate)

    def animate_slide_in(self, direction: str = 'left', duration: int = 300,
                        delay: int = 0, distance: float = 1.0,
                        easing: Callable = EasingFunctions.ease_out_cubic,
                        callback: Callable = None):
        """
        Anima slide in (deslizar desde fuera)

        Args:
            direction: 'left', 'right', 'top', 'bottom'
            duration: Duración en ms
            delay: Delay antes de iniciar en ms
            distance: Distancia a recorrer (0.0 a 1.0 de la pantalla)
            easing: Función de easing
            callback: Función a ejecutar al terminar
        """
        fps = 60
        frame_time = 1000 // fps
        total_frames = duration // frame_time
        current_frame = [0]

        # Determinar offset inicial según dirección
        offsets = {
            'left': (-distance, 0),
            'right': (distance, 0),
            'top': (0, -distance),
            'bottom': (0, distance)
        }

        start_x, start_y = offsets.get(direction, (0, 0))
        end_x, end_y = 0, 0

        def animate():
            if current_frame[0] <= total_frames:
                progress = current_frame[0] / total_frames
                eased = easing(progress)

                # Interpolar posición
                current_x = start_x + (end_x - start_x) * eased
                current_y = start_y + (end_y - start_y) * eased

                # Aplicar posición
                self.widget.place(relx=current_x, rely=current_y, relwidth=1, relheight=1)

                current_frame[0] += 1
                self.widget.after(frame_time, animate)
            else:
                # Cambiar a pack/grid al terminar
                self.widget.place_forget()
                if callback:
                    callback()

        self.widget.after(delay, animate)

    def animate_scale(self, from_scale: float = 0.0, to_scale: float = 1.0,
                     duration: int = 300, delay: int = 0,
                     easing: Callable = EasingFunctions.ease_out_back,
                     callback: Callable = None):
        """
        Anima escala (zoom in/out)

        Args:
            from_scale: Escala inicial (0.0 a 1.0)
            to_scale: Escala final (0.0 a 1.0)
            duration: Duración en ms
            delay: Delay antes de iniciar en ms
            easing: Función de easing
            callback: Función a ejecutar al terminar
        """
        fps = 60
        frame_time = 1000 // fps
        total_frames = duration // frame_time
        current_frame = [0]

        def animate():
            if current_frame[0] <= total_frames:
                progress = current_frame[0] / total_frames
                eased = easing(progress)

                # Interpolar escala
                current_scale = from_scale + (to_scale - from_scale) * eased

                # Aplicar escala usando place
                # Centrar el widget mientras se escala
                offset = (1 - current_scale) / 2
                self.widget.place(
                    relx=offset,
                    rely=offset,
                    relwidth=current_scale,
                    relheight=current_scale
                )

                current_frame[0] += 1
                self.widget.after(frame_time, animate)
            else:
                if callback:
                    callback()

        self.widget.after(delay, animate)

    def animate_value(self, from_value: float, to_value: float,
                     duration: int = 500, delay: int = 0,
                     easing: Callable = EasingFunctions.ease_out_cubic,
                     update_callback: Callable = None,
                     complete_callback: Callable = None):
        """
        Anima un valor numérico (útil para contadores, progreso, etc.)

        Args:
            from_value: Valor inicial
            to_value: Valor final
            duration: Duración en ms
            delay: Delay antes de iniciar en ms
            easing: Función de easing
            update_callback: Función que recibe el valor actual en cada frame
            complete_callback: Función a ejecutar al terminar
        """
        fps = 60
        frame_time = 1000 // fps
        total_frames = duration // frame_time
        current_frame = [0]

        def animate():
            if current_frame[0] <= total_frames:
                progress = current_frame[0] / total_frames
                eased = easing(progress)

                # Interpolar valor
                current_value = from_value + (to_value - from_value) * eased

                if update_callback:
                    update_callback(current_value)

                current_frame[0] += 1
                self.widget.after(frame_time, animate)
            else:
                # Asegurar valor final exacto
                if update_callback:
                    update_callback(to_value)
                if complete_callback:
                    complete_callback()

        self.widget.after(delay, animate)

    def stagger_children(self, children: list, animation_type: str = 'fade',
                        stagger_delay: int = 100, **animation_kwargs):
        """
        Anima múltiples widgets con delay escalonado

        Args:
            children: Lista de widgets a animar
            animation_type: 'fade', 'slide', 'scale'
            stagger_delay: Delay entre cada animación en ms
            **animation_kwargs: Argumentos para la animación
        """
        for i, child in enumerate(children):
            child_animator = AnimationEngine(child)
            delay = i * stagger_delay

            if animation_type == 'fade':
                child_animator.animate_fade_in(delay=delay, **animation_kwargs)
            elif animation_type == 'slide':
                child_animator.animate_slide_in(delay=delay, **animation_kwargs)
            elif animation_type == 'scale':
                child_animator.animate_scale(delay=delay, **animation_kwargs)


# =============================================================================
# UTILIDADES
# =============================================================================

def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """
    Interpola entre dos colores hex

    Args:
        color1: Color inicial (hex)
        color2: Color final (hex)
        factor: Factor de interpolación (0.0 a 1.0)

    Returns:
        Color interpolado (hex)
    """
    # Remover '#' si existe
    c1 = color1.lstrip('#')
    c2 = color2.lstrip('#')

    # Convertir a RGB
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)

    # Interpolar
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)

    # Convertir de vuelta a hex
    return f'#{r:02x}{g:02x}{b:02x}'


def create_gradient_colors(color1: str, color2: str, steps: int) -> list:
    """
    Crea una lista de colores gradiente

    Args:
        color1: Color inicial
        color2: Color final
        steps: Número de pasos

    Returns:
        Lista de colores hex
    """
    colors = []
    for i in range(steps):
        factor = i / (steps - 1) if steps > 1 else 0
        colors.append(interpolate_color(color1, color2, factor))
    return colors
