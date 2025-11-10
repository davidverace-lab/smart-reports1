"""
Panel de Importación de Datos - Sistema de Capacitación
Permite importar datos desde archivos Excel de CSOD
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS
from src.application.services.importador_capacitacion import ImportadorCapacitacion


class PanelImportacionDatos(ctk.CTkFrame):
    """Panel para importar datos desde Excel"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection

        # Variables
        self.archivo_training = None
        self.archivo_org_planning = None
        self.importando = False

        # Crear interfaz
        self._create_header()
        self._create_content()

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=80)
        header.pack(fill='x', padx=20, pady=(20, 15))
        header.pack_propagate(False)

        # Título
        title = ctk.CTkLabel(
            header,
            text="📥 Importación de Datos de Capacitación",
            font=('Montserrat', 24, 'bold'),
            text_color=theme['text']
        )
        title.pack(side='left', anchor='w')

        # Badge
        badge = ctk.CTkLabel(
            header,
            text="CSOD Excel Import",
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            text_color='white',
            corner_radius=8,
            padx=15,
            height=30
        )
        badge.pack(side='right', anchor='e')

    def _create_content(self):
        """Crear contenido principal"""
        theme = self.theme_manager.get_current_theme()

        # Container principal con scroll
        container = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # ========== SECCIÓN 1: ENTERPRISE TRAINING REPORT ==========
        self._create_training_section(container, theme)

        # Separador
        sep1 = ctk.CTkFrame(container, fg_color=theme['border'], height=2)
        sep1.pack(fill='x', pady=30)

        # ========== SECCIÓN 2: CSOD ORG PLANNING ==========
        self._create_org_planning_section(container, theme)

        # Separador
        sep2 = ctk.CTkFrame(container, fg_color=theme['border'], height=2)
        sep2.pack(fill='x', pady=30)

        # ========== SECCIÓN 3: BOTONES DE ACCIÓN ==========
        self._create_actions_section(container, theme)

        # Separador
        sep3 = ctk.CTkFrame(container, fg_color=theme['border'], height=2)
        sep3.pack(fill='x', pady=30)

        # ========== SECCIÓN 4: LOG DE IMPORTACIÓN ==========
        self._create_log_section(container, theme)

    def _create_training_section(self, parent, theme):
        """Sección para Enterprise Training Report"""

        section = ctk.CTkFrame(parent, fg_color=theme['surface'],
                               corner_radius=15, border_width=1,
                               border_color=theme['border'])
        section.pack(fill='x', pady=10)

        # Header de sección
        section_header = ctk.CTkFrame(section, fg_color='transparent')
        section_header.pack(fill='x', padx=20, pady=15)

        icon = ctk.CTkLabel(
            section_header,
            text="📊",
            font=('Montserrat', 24)
        )
        icon.pack(side='left', padx=(0, 10))

        info_frame = ctk.CTkFrame(section_header, fg_color='transparent')
        info_frame.pack(side='left', fill='x', expand=True)

        title = ctk.CTkLabel(
            info_frame,
            text="Enterprise Training Report",
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(anchor='w')

        subtitle = ctk.CTkLabel(
            info_frame,
            text="Estatus de módulos y calificaciones de evaluaciones",
            font=('Montserrat', 11),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(anchor='w')

        # Botón seleccionar archivo
        select_btn = ctk.CTkButton(
            section_header,
            text="📁 Seleccionar Archivo",
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            command=self._select_training_file,
            width=180,
            height=40
        )
        select_btn.pack(side='right')

        # Label de archivo seleccionado
        self.label_training = ctk.CTkLabel(
            section,
            text="📄 No se ha seleccionado ningún archivo",
            font=('Montserrat', 10),
            text_color=theme['text_tertiary'],
            anchor='w'
        )
        self.label_training.pack(anchor='w', padx=20, pady=(0, 15))

    def _create_org_planning_section(self, parent, theme):
        """Sección para CSOD Org Planning"""

        section = ctk.CTkFrame(parent, fg_color=theme['surface'],
                               corner_radius=15, border_width=1,
                               border_color=theme['border'])
        section.pack(fill='x', pady=10)

        # Header de sección
        section_header = ctk.CTkFrame(section, fg_color='transparent')
        section_header.pack(fill='x', padx=20, pady=15)

        icon = ctk.CTkLabel(
            section_header,
            text="👥",
            font=('Montserrat', 24)
        )
        icon.pack(side='left', padx=(0, 10))

        info_frame = ctk.CTkFrame(section_header, fg_color='transparent')
        info_frame.pack(side='left', fill='x', expand=True)

        title = ctk.CTkLabel(
            info_frame,
            text="CSOD Data Source for Org Planning",
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(anchor='w')

        subtitle = ctk.CTkLabel(
            info_frame,
            text="Datos de usuarios, ubicaciones, cargos y departamentos",
            font=('Montserrat', 11),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(anchor='w')

        # Botón seleccionar archivo
        select_btn = ctk.CTkButton(
            section_header,
            text="📁 Seleccionar Archivo",
            font=('Montserrat', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            command=self._select_org_planning_file,
            width=180,
            height=40
        )
        select_btn.pack(side='right')

        # Label de archivo seleccionado
        self.label_org = ctk.CTkLabel(
            section,
            text="📄 No se ha seleccionado ningún archivo",
            font=('Montserrat', 10),
            text_color=theme['text_tertiary'],
            anchor='w'
        )
        self.label_org.pack(anchor='w', padx=20, pady=(0, 15))

    def _create_actions_section(self, parent, theme):
        """Sección de botones de acción"""

        actions_frame = ctk.CTkFrame(parent, fg_color='transparent')
        actions_frame.pack(fill='x', pady=10)

        # Grid para botones
        actions_frame.columnconfigure((0, 1, 2), weight=1)

        # Botón Importar Ambos
        self.btn_importar_todo = ctk.CTkButton(
            actions_frame,
            text="🚀 Importar Ambos Archivos",
            font=('Montserrat', 14, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color='#51cf66',
            text_color='white',
            height=50,
            corner_radius=12,
            command=self._importar_todo
        )
        self.btn_importar_todo.grid(row=0, column=0, padx=5, sticky='ew')

        # Botón Importar Solo Training
        self.btn_importar_training = ctk.CTkButton(
            actions_frame,
            text="📊 Solo Training Report",
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_horizon_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=50,
            corner_radius=12,
            command=self._importar_training
        )
        self.btn_importar_training.grid(row=0, column=1, padx=5, sticky='ew')

        # Botón Importar Solo Org Planning
        self.btn_importar_org = ctk.CTkButton(
            actions_frame,
            text="👥 Solo Org Planning",
            font=('Montserrat', 13, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=50,
            corner_radius=12,
            command=self._importar_org
        )
        self.btn_importar_org.grid(row=0, column=2, padx=5, sticky='ew')

    def _create_log_section(self, parent, theme):
        """Sección de log de importación"""

        # Título
        log_title = ctk.CTkLabel(
            parent,
            text="📋 Log de Importación",
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        log_title.pack(anchor='w', pady=(0, 10))

        # Text area para log
        log_frame = ctk.CTkFrame(parent, fg_color=theme['surface'],
                                 corner_radius=10, border_width=1,
                                 border_color=theme['border'])
        log_frame.pack(fill='both', expand=True)

        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=('Consolas', 10),
            fg_color=theme['background'],
            text_color=theme['text'],
            wrap='word',
            height=300
        )
        self.log_text.pack(fill='both', expand=True, padx=15, pady=15)

        # Log inicial
        self.log("Sistema de importación listo.")
        self.log("Selecciona los archivos Excel y presiona 'Importar'")

    # ========== MÉTODOS DE SELECCIÓN DE ARCHIVOS ==========

    def _select_training_file(self):
        """Seleccionar archivo Training Report"""
        file = filedialog.askopenfilename(
            title="Seleccionar Enterprise Training Report",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )

        if file:
            self.archivo_training = file
            filename = file.split('/')[-1]
            self.label_training.configure(
                text=f"✅ {filename}",
                text_color=HUTCHISON_COLORS['success']
            )
            self.log(f"✅ Training Report seleccionado: {filename}")

    def _select_org_planning_file(self):
        """Seleccionar archivo Org Planning"""
        file = filedialog.askopenfilename(
            title="Seleccionar CSOD Org Planning",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )

        if file:
            self.archivo_org_planning = file
            filename = file.split('/')[-1]
            self.label_org.configure(
                text=f"✅ {filename}",
                text_color=HUTCHISON_COLORS['success']
            )
            self.log(f"✅ Org Planning seleccionado: {filename}")

    # ========== MÉTODOS DE IMPORTACIÓN ==========

    def _importar_todo(self):
        """Importar ambos archivos"""
        if not self.archivo_training or not self.archivo_org_planning:
            messagebox.showwarning(
                "Archivos faltantes",
                "Por favor selecciona ambos archivos Excel antes de importar."
            )
            return

        if self.importando:
            messagebox.showinfo("Importación en curso", "Ya hay una importación en progreso.")
            return

        # Confirmar
        respuesta = messagebox.askyesno(
            "Confirmar Importación",
            "¿Deseas importar ambos archivos?\n\n"
            "Esto actualizará:\n"
            "• Estatus de módulos\n"
            "• Calificaciones\n"
            "• Datos de usuarios\n"
            "• Departamentos y cargos"
        )

        if respuesta:
            self._ejecutar_importacion(importar_training=True, importar_org=True)

    def _importar_training(self):
        """Importar solo Training Report"""
        if not self.archivo_training:
            messagebox.showwarning(
                "Archivo faltante",
                "Por favor selecciona el archivo Training Report."
            )
            return

        if self.importando:
            return

        self._ejecutar_importacion(importar_training=True, importar_org=False)

    def _importar_org(self):
        """Importar solo Org Planning"""
        if not self.archivo_org_planning:
            messagebox.showwarning(
                "Archivo faltante",
                "Por favor selecciona el archivo Org Planning."
            )
            return

        if self.importando:
            return

        self._ejecutar_importacion(importar_training=False, importar_org=True)

    def _ejecutar_importacion(self, importar_training=False, importar_org=False):
        """Ejecutar importación en thread separado"""
        self.importando = True
        self._desabilitar_botones()
        self.log("\n" + "="*70)
        self.log("🚀 INICIANDO IMPORTACIÓN...")
        self.log("="*70)

        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(
            target=self._proceso_importacion,
            args=(importar_training, importar_org),
            daemon=True
        )
        thread.start()

    def _proceso_importacion(self, importar_training, importar_org):
        """Proceso de importación (ejecuta en thread separado)"""
        try:
            # Crear importador
            importador = ImportadorCapacitacion(self.db_connection)

            # Importar Training Report
            if importar_training:
                self.log_thread("\n📊 Importando Training Report...")
                stats_training = importador.importar_training_report(self.archivo_training)

            # Importar Org Planning
            if importar_org:
                self.log_thread("\n👥 Importando Org Planning...")
                stats_org = importador.importar_org_planning(self.archivo_org_planning)

            # Mostrar reporte final
            reporte = importador.generar_reporte()
            self.log_thread("\n" + reporte)

            # Notificar éxito
            self.after(0, lambda: messagebox.showinfo(
                "Importación Completada",
                "Los datos se han importado exitosamente.\n"
                "Revisa el log para ver los detalles."
            ))

        except Exception as e:
            error_msg = f"❌ ERROR: {str(e)}"
            self.log_thread(error_msg)
            import traceback
            self.log_thread(traceback.format_exc())

            self.after(0, lambda: messagebox.showerror(
                "Error de Importación",
                f"Ocurrió un error durante la importación:\n\n{str(e)}"
            ))

        finally:
            self.importando = False
            self.after(0, self._habilitar_botones)

    # ========== UTILIDADES ==========

    def log(self, mensaje):
        """Agregar mensaje al log"""
        self.log_text.insert('end', mensaje + '\n')
        self.log_text.see('end')

    def log_thread(self, mensaje):
        """Agregar mensaje al log desde thread"""
        self.after(0, lambda: self.log(mensaje))

    def _desabilitar_botones(self):
        """Deshabilitar botones durante importación"""
        self.btn_importar_todo.configure(state='disabled')
        self.btn_importar_training.configure(state='disabled')
        self.btn_importar_org.configure(state='disabled')

    def _habilitar_botones(self):
        """Habilitar botones después de importación"""
        self.btn_importar_todo.configure(state='normal')
        self.btn_importar_training.configure(state='normal')
        self.btn_importar_org.configure(state='normal')
