"""
Navigation Controller
Controlador para navegación entre vistas (stub temporal)
"""


class NavigationController:
    """Controlador temporal para navegación"""

    def __init__(self):
        self.current_view = None
        self.history = []

    def navigate_to(self, view_name, data=None):
        """Navega a una vista con datos opcionales"""
        if self.current_view:
            self.history.append(self.current_view)
        self.current_view = view_name
        print(f"Navegando a: {view_name}")

    def go_back(self):
        """Vuelve a la vista anterior"""
        if self.history:
            self.current_view = self.history.pop()
            print(f"Volviendo a: {self.current_view}")
        return self.current_view

    def clear_history(self):
        """Limpia el historial de navegación"""
        self.history = []
