"""
Barra de Progreso en Tiempo Real
Muestra el progreso de importación con estadísticas actualizadas
"""
import customtkinter as ctk
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class BarraProgresoImportacion(ctk.CTkFrame):
    """
    Componente de barra de progreso para importaciones

    Características:
    - Barra de progreso animada
    - Estadísticas en tiempo real (registros procesados, errores, etc.)
    - Estimación de tiempo restante
    - Estado actual de la operación
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.total_registros = 0
        self.registros_procesados = 0
        self.errores = 0
        self.tiempo_inicio = None

        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de la barra de progreso"""
        theme = self.theme_manager.get_current_theme()

        # Card contenedor
        self.card = ctk.CTkFrame(
            self,
            fg_color=theme['surface'],
            corner_radius=12,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.card.pack(fill='both', expand=True, padx=10, pady=10)

        # Header
        header = ctk.CTkFrame(self.card, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))

        self.titulo_label = ctk.CTkLabel(
            header,
            text="📊 Importando Datos...",
            font=('Segoe UI', 16, 'bold'),
            text_color=theme['text']
        )
        self.titulo_label.pack(side='left')

        self.estado_label = ctk.CTkLabel(
            header,
            text="Inicializando...",
            font=('Segoe UI', 11),
            text_color=theme['text_secondary']
        )
        self.estado_label.pack(side='right')

        # Barra de progreso
        self.progressbar = ctk.CTkProgressBar(
            self.card,
            width=400,
            height=20,
            corner_radius=10,
            progress_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        self.progressbar.pack(padx=20, pady=(10, 5))
        self.progressbar.set(0)

        # Porcentaje
        self.porcentaje_label = ctk.CTkLabel(
            self.card,
            text="0%",
            font=('Segoe UI', 14, 'bold'),
            text_color=theme['text']
        )
        self.porcentaje_label.pack(pady=(0, 15))

        # Estadísticas (3 columnas)
        stats_frame = ctk.CTkFrame(self.card, fg_color='transparent')
        stats_frame.pack(fill='x', padx=20, pady=(0, 15))
        stats_frame.columnconfigure((0, 1, 2), weight=1)

        # Procesados
        self.stat_procesados = self._create_stat_card(
            stats_frame,
            "✓ Procesados",
            "0",
            HUTCHISON_COLORS['success'],
            0
        )

        # Pendientes
        self.stat_pendientes = self._create_stat_card(
            stats_frame,
            "⏳ Pendientes",
            "0",
            HUTCHISON_COLORS['warning'],
            1
        )

        # Errores
        self.stat_errores = self._create_stat_card(
            stats_frame,
            "❌ Errores",
            "0",
            HUTCHISON_COLORS['danger'],
            2
        )

        # Tiempo estimado
        self.tiempo_label = ctk.CTkLabel(
            self.card,
            text="⏱ Tiempo estimado: Calculando...",
            font=('Segoe UI', 10),
            text_color=theme['text_tertiary']
        )
        self.tiempo_label.pack(pady=(0, 15))

    def _create_stat_card(self, parent, titulo, valor, color, column):
        """Crear card de estadística"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface_light'],
            corner_radius=8,
            height=60
        )
        card.grid(row=0, column=column, padx=5, sticky='ew')
        card.pack_propagate(False)

        title = ctk.CTkLabel(
            card,
            text=titulo,
            font=('Segoe UI', 10, 'bold'),
            text_color=theme['text_secondary']
        )
        title.pack(pady=(8, 2))

        value = ctk.CTkLabel(
            card,
            text=valor,
            font=('Segoe UI', 18, 'bold'),
            text_color=color
        )
        value.pack()

        # Guardar referencia
        card.value_label = value

        return card

    def iniciar(self, total_registros, titulo="Importando Datos"):
        """
        Iniciar progreso

        Args:
            total_registros: Número total de registros a procesar
            titulo: Título de la operación
        """
        import time
        self.total_registros = total_registros
        self.registros_procesados = 0
        self.errores = 0
        self.tiempo_inicio = time.time()

        self.titulo_label.configure(text=f"📊 {titulo}...")
        self.estado_label.configure(text="Procesando...")
        self.progressbar.set(0)
        self.porcentaje_label.configure(text="0%")

        self.stat_procesados.value_label.configure(text="0")
        self.stat_pendientes.value_label.configure(text=str(total_registros))
        self.stat_errores.value_label.configure(text="0")

    def actualizar(self, procesados=None, errores=None, estado=None):
        """
        Actualizar progreso

        Args:
            procesados: Número de registros procesados (opcional)
            errores: Número de errores (opcional)
            estado: Texto del estado actual (opcional)
        """
        if procesados is not None:
            self.registros_procesados = procesados

        if errores is not None:
            self.errores = errores

        # Calcular progreso
        if self.total_registros > 0:
            progreso = self.registros_procesados / self.total_registros
            self.progressbar.set(progreso)
            porcentaje = int(progreso * 100)
            self.porcentaje_label.configure(text=f"{porcentaje}%")

            # Actualizar estadísticas
            pendientes = self.total_registros - self.registros_procesados
            self.stat_procesados.value_label.configure(text=str(self.registros_procesados))
            self.stat_pendientes.value_label.configure(text=str(pendientes))
            self.stat_errores.value_label.configure(text=str(self.errores))

            # Estimar tiempo restante
            if self.tiempo_inicio and self.registros_procesados > 0:
                import time
                tiempo_transcurrido = time.time() - self.tiempo_inicio
                tiempo_por_registro = tiempo_transcurrido / self.registros_procesados
                tiempo_restante = tiempo_por_registro * pendientes

                if tiempo_restante < 60:
                    tiempo_str = f"{int(tiempo_restante)} segundos"
                elif tiempo_restante < 3600:
                    minutos = int(tiempo_restante / 60)
                    segundos = int(tiempo_restante % 60)
                    tiempo_str = f"{minutos}m {segundos}s"
                else:
                    horas = int(tiempo_restante / 3600)
                    minutos = int((tiempo_restante % 3600) / 60)
                    tiempo_str = f"{horas}h {minutos}m"

                self.tiempo_label.configure(text=f"⏱ Tiempo estimado restante: {tiempo_str}")

        # Actualizar estado
        if estado:
            self.estado_label.configure(text=estado)

    def finalizar(self, exito=True, mensaje="Completado"):
        """
        Finalizar progreso

        Args:
            exito: True si fue exitoso, False si hubo error
            mensaje: Mensaje final
        """
        if exito:
            self.progressbar.set(1.0)
            self.porcentaje_label.configure(text="100%")
            self.titulo_label.configure(text="✅ Importación Completada")
            self.estado_label.configure(text=mensaje)
        else:
            self.titulo_label.configure(text="❌ Importación con Errores")
            self.estado_label.configure(text=mensaje)

        import time
        if self.tiempo_inicio:
            tiempo_total = time.time() - self.tiempo_inicio
            if tiempo_total < 60:
                tiempo_str = f"{int(tiempo_total)} segundos"
            else:
                minutos = int(tiempo_total / 60)
                segundos = int(tiempo_total % 60)
                tiempo_str = f"{minutos}m {segundos}s"

            self.tiempo_label.configure(text=f"⏱ Tiempo total: {tiempo_str}")
