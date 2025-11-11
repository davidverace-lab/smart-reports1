"""
NavigationController - LÓGICA de navegación entre paneles
Separa la lógica de navegación de la interfaz (patrón Android: Controller = Java)
"""


class NavigationController:
    """Controller para manejar la navegación entre diferentes paneles"""

    def __init__(self):
        """Inicializar controller de navegación"""
        self.current_panel = None
        self.navigation_history = []
        self.panel_cache = {}  # Cache de paneles para reutilizar

    def navigate_to(self, panel_name, panel_instance):
        """
        Navegar a un panel específico

        Args:
            panel_name: Nombre identificador del panel
            panel_instance: Instancia del panel

        Returns:
            bool: True si navegación exitosa
        """
        try:
            # Guardar en historial
            if self.current_panel:
                self.navigation_history.append(self.current_panel)

            # Actualizar panel actual
            self.current_panel = panel_name

            # Guardar en cache para reutilizar
            self.panel_cache[panel_name] = panel_instance

            return True

        except Exception as e:
            print(f"Error en navegación: {e}")
            return False

    def go_back(self):
        """
        Regresar al panel anterior en el historial

        Returns:
            str: Nombre del panel anterior o None
        """
        if self.navigation_history:
            previous_panel = self.navigation_history.pop()
            self.current_panel = previous_panel
            return previous_panel

        return None

    def get_current_panel(self):
        """
        Obtener nombre del panel actual

        Returns:
            str: Nombre del panel actual
        """
        return self.current_panel

    def get_panel_from_cache(self, panel_name):
        """
        Obtener panel del cache si existe

        Args:
            panel_name: Nombre del panel

        Returns:
            Panel instance o None
        """
        return self.panel_cache.get(panel_name)

    def clear_cache(self):
        """Limpiar cache de paneles"""
        self.panel_cache.clear()

    def clear_history(self):
        """Limpiar historial de navegación"""
        self.navigation_history.clear()

    def get_navigation_stack(self):
        """
        Obtener pila de navegación actual

        Returns:
            list: Lista de paneles en el historial
        """
        return self.navigation_history.copy()

    def can_go_back(self):
        """
        Verificar si se puede regresar al panel anterior

        Returns:
            bool: True si hay historial
        """
        return len(self.navigation_history) > 0
