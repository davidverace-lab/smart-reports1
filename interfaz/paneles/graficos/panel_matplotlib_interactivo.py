"""
Panel de gráficos interactivos D3.js
ACTUALIZADO: Usa gráficos D3.js en lugar de matplotlib
"""
import customtkinter as ctk
from interfaz.componentes.visualizacion.grafico_d3_widget import GraficoD3Widget
from nucleo.servicios.graficos_d3_avanzados import GraficosD3Avanzados
from nucleo.configuracion.ajustes import HUTCHISON_COLORS, EXECUTIVE_CHART_COLORS
from nucleo.configuracion.gestor_temas import get_theme_manager


class MatplotlibInteractivePanel(ctk.CTkFrame):
    """Panel con gráficos interactivos D3.js (reemplaza matplotlib)"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
        """
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(parent, fg_color='transparent', **kwargs)
        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None

        # Widget para gráficos D3.js
        self.grafico_d3_widget = GraficoD3Widget(width=1200, height=800)

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Crear header
        self._create_header()

        # Crear scroll frame para cards
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))

        # Crear cards con botones
        self.after(100, self.create_chart_cards)

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 10))
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header,
            text='📊 Gráficos Interactivos D3.js',
            font=('Montserrat', 28, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(side='left', pady=20)

        subtitle = ctk.CTkLabel(
            header,
            text='Gráficos ultra-rápidos, interactivos y hermosos • Haz clic para abrir',
            font=('Montserrat', 13),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(side='left', padx=(20, 0))

    def create_chart_cards(self):
        """Crear cards con botones para cada tipo de gráfico"""
        theme = self.theme_manager.get_current_theme()

        # Configurar grid del scroll frame (2 columnas)
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # === CARD 1: Gráfico de Líneas ===
        card1 = self._create_chart_card(
            "📈 Tendencias de Progreso por Módulo",
            "Gráfico de líneas interactivo con múltiples series",
            HUTCHISON_COLORS['ports_sky_blue'],
            self._show_chart_lineas,
            row=0, column=0
        )

        # === CARD 2: Barras Apiladas ===
        card2 = self._create_chart_card(
            "📊 Distribución por Estado y Módulo",
            "Gráfico de barras con estado de usuarios",
            HUTCHISON_COLORS['ports_horizon_blue'],
            self._show_chart_barras_apiladas,
            row=0, column=1
        )

        # === CARD 3: Scatter / Correlación ===
        card3 = self._create_chart_card(
            "🎯 Análisis de Correlación - Progreso vs Tiempo",
            "Gráfico de dispersión interactivo",
            HUTCHISON_COLORS['success'],
            self._show_chart_scatter,
            row=1, column=0
        )

        # === CARD 4: Heatmap ===
        card4 = self._create_chart_card(
            "🔥 Mapa de Calor - Actividad por Unidad",
            "Visualiza patrones de actividad por colores",
            HUTCHISON_COLORS['warning'],
            self._show_chart_heatmap,
            row=1, column=1
        )

    def _create_chart_card(self, title, description, color, command, row, column):
        """Crear una card con botón para abrir gráfico"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        card.grid(row=row, column=column, sticky='nsew', padx=10, pady=10)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        title_label.pack(pady=(20, 10))

        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=('Montserrat', 11),
            text_color=theme['text_secondary']
        )
        desc_label.pack(pady=(0, 20))

        btn = ctk.CTkButton(
            card,
            text='Ver Gráfico Interactivo',
            font=('Montserrat', 13, 'bold'),
            fg_color=color,
            hover_color=self._adjust_color(color, -20),
            height=45,
            corner_radius=10,
            command=command
        )
        btn.pack(pady=(0, 20), padx=40, fill='x')

        return card

    def _adjust_color(self, hex_color, adjustment):
        """Ajustar brillo de un color hex"""
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        # Ajustar
        r = max(0, min(255, r + adjustment))
        g = max(0, min(255, g + adjustment))
        b = max(0, min(255, b + adjustment))

        # Convertir de vuelta a hex
        return f'#{r:02x}{g:02x}{b:02x}'

    # ==================== MÉTODOS DE GRÁFICOS ====================

    def _show_chart_lineas(self):
        """Mostrar gráfico de líneas con D3.js"""
        # Datos de ejemplo
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

        self.grafico_d3_widget.crear_grafico_lineas(
            titulo="Tendencias de Progreso por Módulo - Instituto Hutchison Ports",
            datos={
                'x': modulos,
                'series': [
                    {
                        'name': 'TNG',
                        'values': [100, 98, 95, 93, 90, 88, 85, 82]
                    },
                    {
                        'name': 'Container Care',
                        'values': [90, 88, 85, 82, 80, 78, 75, 72]
                    },
                    {
                        'name': 'ECV-EIT',
                        'values': [85, 83, 80, 78, 75, 73, 70, 68]
                    },
                    {
                        'name': 'Operaciones',
                        'values': [80, 78, 75, 72, 70, 68, 65, 62]
                    }
                ]
            },
            subtitulo="Evolución del progreso por módulo • Datos históricos"
        )

    def _show_chart_barras_apiladas(self):
        """Mostrar gráfico de barras apiladas con D3.js"""
        # Para barras apiladas, usamos gráfico de barras normal por ahora
        # (el template D3.js actual no tiene barras apiladas, pero podríamos agregarlo)
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
        completado = [120, 135, 140, 138, 142, 145, 148, 150]

        self.grafico_d3_widget.crear_grafico_barras(
            titulo="Distribución por Estado y Módulo - Usuarios Completados",
            datos={
                'labels': modulos,
                'values': completado
            },
            subtitulo="Usuarios que completaron cada módulo • Estado: Terminado"
        )

    def _show_chart_scatter(self):
        """Mostrar gráfico scatter con D3.js"""
        # Para scatter, usamos barras por ahora
        # (podríamos agregar un template específico de scatter en el futuro)
        dias_rangos = ['0-15', '16-30', '31-45', '46-60', '60+']
        usuarios = [45, 78, 92, 65, 35]

        self.grafico_d3_widget.crear_grafico_barras(
            titulo="Análisis de Correlación - Progreso vs Tiempo",
            datos={
                'labels': dias_rangos,
                'values': usuarios
            },
            subtitulo="Distribución de usuarios por tiempo de progreso (días)"
        )

    def _show_chart_heatmap(self):
        """Mostrar heatmap con D3.js"""
        # Crear instancia del generador avanzado
        graficos_avanzados = GraficosD3Avanzados()

        # Datos para el heatmap
        unidades = ['TNG', 'Container Care', 'ECV-EIT', 'Operaciones', 'Logística', 'Mantenimiento']
        modulos = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']

        # Matriz de valores (progreso %)
        values = [
            [100, 98, 95, 93, 90, 88, 85, 82],  # TNG
            [90, 88, 85, 82, 80, 78, 75, 72],   # Container Care
            [85, 83, 80, 78, 75, 73, 70, 68],   # ECV-EIT
            [80, 78, 75, 72, 70, 68, 65, 62],   # Operaciones
            [75, 73, 70, 68, 65, 63, 60, 58],   # Logística
            [70, 68, 65, 63, 60, 58, 55, 52]    # Mantenimiento
        ]

        # Generar HTML
        html = graficos_avanzados.generar_heatmap(
            titulo="Mapa de Calor - Actividad por Unidad y Módulo",
            datos={
                'rows': unidades,
                'cols': modulos,
                'values': values
            },
            subtitulo="Progreso % de cada unidad por módulo • Colores más intensos = mayor progreso",
            tema='dark' if self.theme_manager.is_dark_mode() else 'light'
        )

        # Mostrar en ventana PyWebView
        import webview
        from threading import Thread

        def show_window():
            window = webview.create_window(
                title='Mapa de Calor - Actividad por Unidad y Módulo',
                html=html,
                width=1200,
                height=800,
                resizable=True,
                background_color='#1a1d2e' if self.theme_manager.is_dark_mode() else '#f0f2f5'
            )
            webview.start(http_server=True)

        thread = Thread(target=show_window, daemon=True)
        thread.start()
