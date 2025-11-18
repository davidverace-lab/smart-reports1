"""
MenuReportes - Módulo de interfaz para Reportes
Separado de ventana principal para mejor organización
"""
import customtkinter as ctk
from smart_reports.config.themes import HUTCHISON_COLORS
from smart_reports.config.gestor_temas import get_theme_manager

# Paneles de reportes
from smart_reports.ui.views.reportes.panel_reporte_usuario import UserReportPanel
from smart_reports.ui.views.reportes.panel_reporte_unidad import UnitReportPanel
from smart_reports.ui.views.reportes.panel_reporte_periodo import PeriodReportPanel
from smart_reports.ui.views.reportes.panel_reporte_global import GlobalReportPanel
from smart_reports.ui.views.reportes.panel_niveles_mando import ManagementLevelsPanel


class MenuReportes:
    """Clase para manejar el menú de reportes"""

    def __init__(self, parent, db_connection, cursor):
        """
        Inicializar menú de reportes

        Args:
            parent: Widget padre
            db_connection: Conexión a base de datos
            cursor: Cursor de base de datos
        """
        self.parent = parent
        self.conn = db_connection
        self.cursor = cursor
        self.theme_manager = get_theme_manager()

    def show_selection_panel(self):
        """Mostrar panel de selección de reportes"""
        if not self.conn:
            return self._show_error("No hay conexión a la base de datos")

        # Container
        container = ctk.CTkScrollableFrame(
            self.parent,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Crear título
        self._create_title(container)

        # Crear grid de reportes
        self._create_reports_grid(container)

        return container

    def _create_title(self, parent):
        """Crear título del panel"""
        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # Color del título: Navy blue en modo claro, blanco en modo oscuro
        title_color = HUTCHISON_COLORS['ports_sea_blue'] if not is_dark else '#FFFFFF'

        title_label = ctk.CTkLabel(
            parent,
            text="📊 Generación de Reportes",
            font=('Montserrat', 32, 'bold'),
            text_color=title_color
        )
        title_label.pack(pady=(10, 5))

        subtitle_label = ctk.CTkLabel(
            parent,
            text="Selecciona el tipo de reporte que deseas generar",
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        )
        subtitle_label.pack(pady=(0, 30))

    def _create_reports_grid(self, parent):
        """Crear grid con cards de reportes"""
        # Grid frame
        reports_frame = ctk.CTkFrame(parent, fg_color='transparent')
        reports_frame.pack(fill='both', expand=True)
        reports_frame.grid_columnconfigure((0, 1), weight=1)

        # Lista de reportes disponibles
        reports = [
            {
                'icon': '👤',
                'name': 'Progreso de Usuario',
                'description': 'Reporte detallado del progreso individual',
                'action': self.open_user_report
            },
            {
                'icon': '🏢',
                'name': 'Progreso por Unidad',
                'description': 'Reporte de progreso por unidad de negocio',
                'action': self.open_unit_report
            },
            {
                'icon': '📅',
                'name': 'Reporte por Período',
                'description': 'Reporte de actividad en un rango de fechas',
                'action': self.open_period_report
            },
            {
                'icon': '🌍',
                'name': 'Reporte Global',
                'description': 'Vista general del sistema completo',
                'action': self.open_global_report
            },
            {
                'icon': '👔',
                'name': 'Niveles de Mando',
                'description': 'Reporte organizado por niveles gerenciales',
                'action': self.open_management_levels_report
            }
        ]

        # Crear cards
        row = 0
        col = 0
        for report in reports:
            self._create_report_card(
                reports_frame,
                report['icon'],
                report['name'],
                report['description'],
                report['action'],
                row,
                col
            )

            col += 1
            if col > 1:
                col = 0
                row += 1

    def _create_report_card(self, parent, icon, title, description, command, row, col):
        """Crear card individual de reporte"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=2,
            border_color=theme['border']
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')

        # Contenido
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=25, pady=25)

        # Icono y título
        header = ctk.CTkLabel(
            content,
            text=f"{icon} {title}",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['text']
        )
        header.pack(anchor='w', pady=(0, 10))

        # Descripción
        desc = ctk.CTkLabel(
            content,
            text=description,
            font=('Montserrat', 13),
            text_color=theme['text_secondary'],
            wraplength=300,
            justify='left'
        )
        desc.pack(anchor='w', pady=(0, 20))

        # Botón generar
        btn = ctk.CTkButton(
            content,
            text="Generar Reporte",
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#003D8F',
            height=45,
            corner_radius=10,
            command=command
        )
        btn.pack(fill='x')

    # ==================== ABRIR PANELES DE REPORTES ====================

    def open_user_report(self):
        """Abrir panel de reporte de usuario"""
        self._clear_parent()
        panel = UserReportPanel(
            self.parent,
            db=self.conn,
            cursor=self.cursor
        )
        panel.pack(fill='both', expand=True)

    def open_unit_report(self):
        """Abrir panel de reporte de unidad"""
        self._clear_parent()
        panel = UnitReportPanel(
            self.parent,
            db=self.conn,
            cursor=self.cursor
        )
        panel.pack(fill='both', expand=True)

    def open_period_report(self):
        """Abrir panel de reporte por período"""
        self._clear_parent()
        panel = PeriodReportPanel(
            self.parent,
            db=self.conn,
            cursor=self.cursor
        )
        panel.pack(fill='both', expand=True)

    def open_global_report(self):
        """Abrir panel de reporte global"""
        self._clear_parent()
        panel = GlobalReportPanel(
            self.parent,
            db=self.conn,
            cursor=self.cursor
        )
        panel.pack(fill='both', expand=True)

    def open_management_levels_report(self):
        """Abrir panel de reporte por niveles de mando"""
        self._clear_parent()
        panel = ManagementLevelsPanel(
            self.parent,
            db=self.conn,
            cursor=self.cursor
        )
        panel.pack(fill='both', expand=True)

    # ==================== HELPERS ====================

    def _clear_parent(self):
        """Limpiar widgets del padre"""
        for widget in self.parent.winfo_children():
            widget.destroy()

    def _show_error(self, message):
        """Mostrar mensaje de error"""
        error_frame = ctk.CTkFrame(self.parent, fg_color='transparent')

        error_label = ctk.CTkLabel(
            error_frame,
            text=f'⚠️ {message}\n\nPor favor verifica la configuración.',
            font=('Montserrat', 18),
            text_color='#ff6b6b'
        )
        error_label.pack(expand=True)

        return error_frame


def show_reportes_menu(parent, db_connection, cursor):
    """
    Función helper para mostrar menú de reportes

    Args:
        parent: Widget padre
        db_connection: Conexión a base de datos
        cursor: Cursor de base de datos

    Returns:
        MenuReportes instance
    """
    menu = MenuReportes(parent, db_connection, cursor)
    menu.show_selection_panel()
    return menu
