"""
Panel de Dashboards de Recursos Humanos - HUTCHISON PORTS
Dashboards especializados para área de RRHH
Sistema de navegación: GRID ↔ EXPANDIDA (pantalla completa)
CON D3.JS INTERACTIVO AL EXPANDIR
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from smart_reports.ui.components.navigation.boton_pestana import CustomTabView
from smart_reports.database.models.queries_hutchison import *
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS

# Importar modal D3.js
try:
    from smart_reports.ui.components.charts.modal_d3_fullscreen import ModalD3Fullscreen, TKINTERWEB_AVAILABLE
except ImportError:
    TKINTERWEB_AVAILABLE = False
    ModalD3Fullscreen = None
    print("⚠️ Modal D3.js no disponible - usando vista expandida Matplotlib")


class PanelDashboardsRRHH(ctk.CTkFrame):
    """
    Panel especializado para Recursos Humanos con navegación de 2 vistas:

    GRID VIEW: Muestra todas las gráficas pequeñas
    EXPANDED VIEW: Muestra UNA gráfica en pantalla completa con botón volver
    """

    def __init__(self, parent, db_connection=None, usuario_actual=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        print("🚀 Inicializando Panel RRHH con navegación expandible...")

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection
        self.usuario_actual = usuario_actual or {"nombre": "RRHH"}

        # Datos de las gráficas
        self.datos_graficas = {}

        # Vistas de navegación
        self.grid_view = None
        self.expanded_view = None
        self.current_chart_data = None
        self.current_chart_title = None
        self.current_chart_type = None

        try:
            # Crear ambas vistas
            self._create_grid_view()
            self._create_expanded_view()

            # Mostrar grid por defecto
            self.show_grid_view()

            # Cargar datos
            self.after(500, self._load_data)

            print("✅ Panel RRHH inicializado correctamente")

        except Exception as e:
            print(f"❌ Error inicializando panel RRHH: {e}")
            import traceback
            traceback.print_exc()

    # ==================== NAVEGACIÓN ENTRE VISTAS ====================

    def show_grid_view(self):
        """Mostrar vista GRID con todas las gráficas"""
        if self.expanded_view:
            self.expanded_view.pack_forget()
        if self.grid_view:
            self.grid_view.pack(fill='both', expand=True)

    def _animate_expanded_view(self):
        """Animar la entrada de la vista expandida con efecto deslizante"""
        # Configuración de la animación
        duration_ms = 300  # 300ms duración total
        fps = 60  # 60 FPS
        frame_time = 1000 // fps  # ~16ms por frame
        total_frames = duration_ms // frame_time  # ~18 frames

        # Posición inicial y final
        start_offset = -0.08  # Comienza 8% arriba (fuera de vista)
        end_offset = 0.0  # Termina en posición normal

        current_frame = [0]  # Usar lista para poder modificar en función anidada

        def ease_out_cubic(t):
            """Función de easing suave (ease-out cubic)"""
            return 1 - pow(1 - t, 3)

        def animate_frame():
            if current_frame[0] <= total_frames:
                # Calcular progreso (0.0 a 1.0)
                progress = current_frame[0] / total_frames
                eased_progress = ease_out_cubic(progress)

                # Interpolar posición
                current_offset = start_offset + (end_offset - start_offset) * eased_progress

                # Aplicar posición usando place()
                self.expanded_view.place(relx=0, rely=current_offset, relwidth=1, relheight=1)

                # Siguiente frame
                current_frame[0] += 1
                self.after(frame_time, animate_frame)
            else:
                # Animación completa - cambiar a pack() para layout normal
                self.expanded_view.place_forget()
                self.expanded_view.pack(fill='both', expand=True)

        # Iniciar animación
        animate_frame()

    def show_expanded_view(self, title, data, chart_type='barras'):
        """
        Mostrar vista EXPANDIDA con gráfica D3.js interactiva

        Args:
            title: Título de la gráfica
            data: Datos de la gráfica {'labels': [...], 'values': [...]}
            chart_type: 'barras', 'dona', 'linea', 'area'
        """
        # Mapear tipo de gráfico a formato D3.js
        chart_type_map = {
            'barras': 'bar',
            'barras_h': 'horizontal_bar',
            'dona': 'donut',
            'linea': 'line',
            'area': 'area'
        }
        d3_chart_type = chart_type_map.get(chart_type, 'bar')

        # DESHABILITADO: Modal D3.js (causa error de thread)
        # Los gráficos ahora se expanden in-place directamente
        print(f"ℹ️ Expansión in-place para: {title}")
        # No usar modal - los gráficos ya tienen su propio botón de expansión

        # Usar vista expandida Matplotlib tradicional como única opción
        print(f"  ⚠️ Usando vista expandida Matplotlib (fallback)")
        self.current_chart_title = title
        self.current_chart_data = data
        self.current_chart_type = chart_type

        # Ocultar grid y mostrar expandida
        if self.grid_view:
            self.grid_view.pack_forget()

        # Renderizar gráfica expandida
        self._render_expanded_chart()

        if self.expanded_view:
            # Iniciar animación de entrada
            self._animate_expanded_view()

    # ==================== CREAR VISTA GRID ====================

    def _create_grid_view(self):
        """Crear vista GRID con todas las gráficas pequeñas"""
        theme = self.theme_manager.get_current_theme()

        self.grid_view = ctk.CTkFrame(self, fg_color='transparent')

        # Header
        header = ctk.CTkFrame(self.grid_view, fg_color='transparent', height=60)
        header.pack(fill='x', padx=20, pady=(15, 10))
        header.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            header,
            text="📊 Dashboard de Recursos Humanos",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['colors']['text']
        ).pack(side='left')

        # Container con scroll
        container = ctk.CTkScrollableFrame(self.grid_view, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Grid de gráficas
        # Fila 1: 2 gráficas
        row1 = ctk.CTkFrame(container, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 20))
        row1.columnconfigure((0, 1), weight=1)

        # Gráfica 1: Personal por Departamento
        self._create_mini_chart(
            row1,
            "👥 Personal por Departamento",
            chart_id='personal_depto',
            row=0, column=0
        )

        # Gráfica 2: Estado de Capacitación
        self._create_mini_chart(
            row1,
            "📚 Estado de Capacitación",
            chart_id='capacitacion',
            row=0, column=1
        )

        # Fila 2: 2 gráficas
        row2 = ctk.CTkFrame(container, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 20))
        row2.columnconfigure((0, 1), weight=1)

        # Gráfica 3: Calificaciones por Área
        self._create_mini_chart(
            row2,
            "⭐ Calificaciones por Área",
            chart_id='calificaciones',
            row=0, column=0
        )

        # Gráfica 4: Cumplimiento por Unidad
        self._create_mini_chart(
            row2,
            "✓ Cumplimiento por Unidad",
            chart_id='cumplimiento',
            row=0, column=1
        )

        # Fila 3: 1 gráfica completa
        row3 = ctk.CTkFrame(container, fg_color='transparent')
        row3.pack(fill='x', pady=(0, 20))
        row3.columnconfigure(0, weight=1)

        # Gráfica 5: Tendencia Mensual
        self._create_mini_chart(
            row3,
            "📈 Módulos Completados por Mes",
            chart_id='tendencia',
            row=0, column=0, wide=True
        )

    def _create_mini_chart(self, parent, title, chart_id, row, column, wide=False):
        """Crear una tarjeta de gráfica miniatura con botón expandir"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=12,
            border_width=1,
            border_color=theme['colors']['border']
        )

        if wide:
            card.grid(row=row, column=column, columnspan=2, padx=10, pady=10, sticky='nsew')
        else:
            card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

        # Header con título y botón expandir
        header = ctk.CTkFrame(card, fg_color='transparent', height=40)
        header.pack(fill='x', padx=15, pady=(10, 5))
        header.pack_propagate(False)

        # Título
        ctk.CTkLabel(
            header,
            text=title,
            font=('Montserrat', 13, 'bold'),
            text_color=theme['colors']['text']
        ).pack(side='left')

        # Botón expandir
        expand_btn = ctk.CTkButton(
            header,
            text="⛶ Ver Grande",
            font=('Montserrat', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#003D8F',
            text_color='white',
            corner_radius=8,
            height=28,
            width=110,
            command=lambda: self._on_expand_chart(chart_id, title)
        )
        expand_btn.pack(side='right')

        # Preview de la gráfica
        preview_frame = ctk.CTkFrame(
            card,
            fg_color=theme['colors']['background'],
            corner_radius=8,
            height=200 if not wide else 250
        )
        preview_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))
        preview_frame.pack_propagate(False)

        # Placeholder (se llenará con datos)
        ctk.CTkLabel(
            preview_frame,
            text="📊",
            font=('Segoe UI', 48),
            text_color=theme['colors']['text_tertiary']
        ).place(relx=0.5, rely=0.5, anchor='center')

        # Guardar referencia
        setattr(self, f'mini_{chart_id}', preview_frame)

    def _on_expand_chart(self, chart_id, title):
        """Callback cuando se expande una gráfica"""
        print(f"📊 Expandiendo gráfica: {chart_id}")

        # Obtener datos y tipo de gráfica
        if chart_id not in self.datos_graficas:
            print(f"⚠️ No hay datos para {chart_id}")
            return

        data = self.datos_graficas[chart_id]
        chart_type = data.get('tipo', 'barras')
        chart_data = {'labels': data.get('labels', []), 'values': data.get('values', [])}

        # Mostrar vista expandida
        self.show_expanded_view(title, chart_data, chart_type)

    # ==================== CREAR VISTA EXPANDIDA ====================

    def _create_expanded_view(self):
        """Crear vista EXPANDIDA con gráfica en pantalla completa"""
        theme = self.theme_manager.get_current_theme()

        self.expanded_view = ctk.CTkFrame(self, fg_color=theme['colors']['background'])

        # Header con botón volver
        header = ctk.CTkFrame(
            self.expanded_view,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            height=70
        )
        header.pack(fill='x')
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)

        # Botón volver (PROMINENTE, como gestionar usuarios)
        volver_btn = ctk.CTkButton(
            header_content,
            text="← Volver",
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['primary'],
            hover_color='#003D8F',
            text_color='white',
            corner_radius=10,
            height=45,
            width=130,
            command=self.show_grid_view
        )
        volver_btn.pack(side='left')

        # Título de la gráfica
        self.expanded_title_label = ctk.CTkLabel(
            header_content,
            text="",
            font=('Montserrat', 20, 'bold'),
            text_color=theme['colors']['text']
        )
        self.expanded_title_label.pack(side='left', padx=25)

        # Info
        ctk.CTkLabel(
            header_content,
            text="🔍 Gráfica interactiva | Rueda del mouse para zoom",
            font=('Montserrat', 11),
            text_color=theme['colors']['text_secondary']
        ).pack(side='right')

        # Container para la gráfica gigante
        self.expanded_chart_container = ctk.CTkFrame(
            self.expanded_view,
            fg_color=theme['colors']['background']
        )
        self.expanded_chart_container.pack(fill='both', expand=True, padx=20, pady=20)

    def _render_expanded_chart(self):
        """Renderizar gráfica expandida en pantalla completa"""
        # Limpiar container
        for widget in self.expanded_chart_container.winfo_children():
            widget.destroy()

        if not self.current_chart_data:
            return

        # Actualizar título
        self.expanded_title_label.configure(text=self.current_chart_title)

        theme = self.theme_manager.get_current_theme()
        is_dark = self.theme_manager.is_dark_mode()

        # Crear figura grande
        fig = Figure(figsize=(14, 8), dpi=100, facecolor=theme['colors']['background'])
        ax = fig.add_subplot(111)

        # Renderizar según tipo
        labels = self.current_chart_data.get('labels', [])
        values = self.current_chart_data.get('values', [])

        if self.current_chart_type == 'barras':
            bars = ax.bar(labels, values, color=HUTCHISON_COLORS['primary'], alpha=0.8)
            # Etiquetas en barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
            ax.set_ylabel('Cantidad', fontsize=14)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=12)

        elif self.current_chart_type == 'dona':
            colors = [HUTCHISON_COLORS['aqua_green'], HUTCHISON_COLORS['primary'],
                     HUTCHISON_COLORS['primary'], '#FFC107', '#FF5722']
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct='%1.1f%%', startangle=90,
                colors=colors[:len(values)], textprops={'fontsize': 12, 'fontweight': 'bold'}
            )
            for autotext in autotexts:
                autotext.set_color('white')
            ax.axis('equal')

        elif self.current_chart_type == 'linea':
            ax.plot(labels, values, color=HUTCHISON_COLORS['primary'],
                   linewidth=3, marker='o', markersize=8)
            ax.fill_between(range(len(labels)), values, alpha=0.3,
                           color=HUTCHISON_COLORS['primary'])
            ax.set_xlabel('Tiempo', fontsize=14)
            ax.set_ylabel('Valor', fontsize=14)

        # Estilo
        ax.set_facecolor(theme['colors']['background'])
        ax.tick_params(colors=theme['colors']['text'], labelsize=11)
        ax.spines['bottom'].set_color(theme['colors']['border'])
        ax.spines['left'].set_color(theme['colors']['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        fig.tight_layout()

        # Integrar con tkinter
        canvas = FigureCanvasTkAgg(fig, self.expanded_chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # === TOOLTIPS INTERACTIVOS (HOVER) ===
        # Crear anotación que se mostrará al hacer hover
        annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                           bbox=dict(boxstyle="round,pad=0.8", fc=HUTCHISON_COLORS['primary'],
                                    ec='white', lw=2, alpha=0.95),
                           arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3",
                                          color='white', lw=2),
                           fontsize=12, fontweight='bold', color='white',
                           visible=False, zorder=1000)

        def update_annot(bar_or_point, label, value):
            """Actualizar posición y texto del tooltip"""
            if self.current_chart_type in ['barras', 'barras_h']:
                # Para barras verticales u horizontales
                x = bar_or_point.get_x() + bar_or_point.get_width() / 2
                y = bar_or_point.get_height() if self.current_chart_type == 'barras' else bar_or_point.get_y() + bar_or_point.get_height() / 2
                annot.xy = (x, y) if self.current_chart_type == 'barras' else (bar_or_point.get_width(), y)
            else:
                # Para líneas y puntos
                annot.xy = bar_or_point

            text = f"{label}\n{int(value):,}"
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.95)

        def hover(event):
            """Manejar evento de hover del mouse"""
            vis = annot.get_visible()
            if event.inaxes == ax:
                if self.current_chart_type == 'barras':
                    # Detectar hover sobre barras verticales
                    for i, bar in enumerate(bars):
                        cont, ind = bar.contains(event)
                        if cont:
                            update_annot(bar, labels[i], values[i])
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return
                elif self.current_chart_type == 'linea':
                    # Detectar hover sobre puntos de línea
                    for i, (x, y) in enumerate(zip(range(len(labels)), values)):
                        if abs(event.xdata - x) < 0.3 and abs(event.ydata - y) < max(values) * 0.05:
                            update_annot((x, y), labels[i], values[i])
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return

                # Si no está sobre ningún elemento, ocultar tooltip
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

        # Conectar evento de movimiento del mouse
        fig.canvas.mpl_connect("motion_notify_event", hover)

        # Toolbar de navegación
        toolbar_frame = ctk.CTkFrame(self.expanded_chart_container, fg_color=theme['colors'].get('card_background', '#2d2d2d'))
        toolbar_frame.pack(fill='x', pady=(10, 0))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    # ==================== CARGA DE DATOS ====================

    def _load_data(self):
        """Cargar datos en las gráficas"""
        print("\n[RRHH] Cargando datos de dashboards...")

        # Datos ESTÁTICOS de ejemplo (reemplazar con queries reales)
        self.datos_graficas = {
            'personal_depto': {
                'tipo': 'barras',
                'labels': ['Operaciones', 'RRHH', 'TI', 'Finanzas', 'Seguridad'],
                'values': [245, 89, 134, 67, 112]
            },
            'capacitacion': {
                'tipo': 'dona',
                'labels': ['Completados', 'En Progreso', 'Registrados'],
                'values': [1234, 789, 224]
            },
            'calificaciones': {
                'tipo': 'barras',
                'labels': ['Operaciones', 'RRHH', 'TI', 'Finanzas', 'Seguridad'],
                'values': [85, 92, 78, 88, 91]
            },
            'cumplimiento': {
                'tipo': 'barras',
                'labels': ['ICAVE', 'EIT', 'TIMSA', 'HPMX', 'TNG'],
                'values': [95, 87, 92, 78, 100]
            },
            'tendencia': {
                'tipo': 'linea',
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                'values': [120, 145, 178, 210, 245, 289]
            }
        }

        print("✅ Datos cargados en memoria")
