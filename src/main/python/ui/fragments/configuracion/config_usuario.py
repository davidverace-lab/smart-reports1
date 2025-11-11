"""
Configuración - Gestión de Usuarios
Panel para CRUD de usuarios y asignación de roles
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
from src.main.res.config.gestor_temas import get_theme_manager


class ConfigUsuariosPanel(ctk.CTkFrame):
    """Panel de gestión de usuarios"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.db_connection = db_connection
        self.theme_manager = get_theme_manager()

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de gestión de usuarios"""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = ctk.CTkLabel(
            self,
            text="👥 Gestión de Usuarios",
            font=('Montserrat', 22, 'bold'),
            text_color=theme['text']
        )
        header.pack(pady=(10, 20), padx=20, anchor='w')

        # TODO: Agregar formulario de usuarios
        # TODO: Agregar tabla de usuarios
        # TODO: Agregar botones CRUD

        placeholder = ctk.CTkLabel(
            self,
            text="Panel de gestión de usuarios\n(En desarrollo)",
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        )
        placeholder.pack(expand=True)
