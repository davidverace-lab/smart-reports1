"""
Panel de Importación y Cruce de Datos - Sistema de Capacitación
Sistema mejorado con validación, preview y matching manual
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import pandas as pd
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS
from src.application.services.importador_capacitacion import ImportadorCapacitacion


class PanelImportacionDatos(ctk.CTkFrame):
    """Panel mejorado para importar y cruzar datos desde Excel"""

    def __init__(self, parent, db_connection=None, **kwargs):
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.theme_manager = get_theme_manager()
        self.db_connection = db_connection

        # Variables
        self.archivo_training = None
        self.archivo_org_planning = None
        self.df_training_preview = None
        self.df_org_preview = None
        self.importando = False

        # Crear interfaz mejorada
        self._create_header()
        self._create_content()

    def _create_header(self):
        """Crear header del panel"""
        theme = self.theme_manager.get_current_theme()

        header = ctk.CTkFrame(self, fg_color='transparent', height=70)
        header.pack(fill='x', padx=20, pady=(15, 10))
        header.pack_propagate(False)

        # Container izquierdo
        left_frame = ctk.CTkFrame(header, fg_color='transparent')
        left_frame.pack(side='left', fill='both', expand=True)

        # Título
        title = ctk.CTkLabel(
            left_frame,
            text="📥 Cruce e Importación de Datos",
            font=('Segoe UI', 22, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title.pack(anchor='w', pady=(0, 2))

        # Subtítulo
        subtitle = ctk.CTkLabel(
            left_frame,
            text="Sistema inteligente de validación, preview y matching de datos CSOD",
            font=('Segoe UI', 11),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle.pack(anchor='w')

        # Badge
        badge = ctk.CTkLabel(
            header,
            text="✨ Smart Import",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            text_color='white',
            corner_radius=6,
            padx=12,
            height=26
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
        container.pack(fill='both', expand=True, padx=20, pady=(0, 15))

        # ========== SECCIÓN 1: ARCHIVOS ==========
        self._create_files_section(container, theme)

        # Separador
        sep1 = ctk.CTkFrame(container, fg_color=theme['border'], height=1)
        sep1.pack(fill='x', pady=20)

        # ========== SECCIÓN 2: PREVIEW Y VALIDACIÓN ==========
        self._create_preview_section(container, theme)

        # Separador
        sep2 = ctk.CTkFrame(container, fg_color=theme['border'], height=1)
        sep2.pack(fill='x', pady=20)

        # ========== SECCIÓN 3: ACCIONES ==========
        self._create_actions_section(container, theme)

        # Separador
        sep3 = ctk.CTkFrame(container, fg_color=theme['border'], height=1)
        sep3.pack(fill='x', pady=20)

        # ========== SECCIÓN 4: LOG ==========
        self._create_log_section(container, theme)

    def _create_files_section(self, parent, theme):
        """Sección compacta para selección de archivos"""

        section_title = ctk.CTkLabel(
            parent,
            text="📁 Archivos a Importar",
            font=('Segoe UI', 15, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        section_title.pack(anchor='w', pady=(0, 12))

        # Grid para 2 archivos
        files_grid = ctk.CTkFrame(parent, fg_color='transparent')
        files_grid.pack(fill='x', pady=(0, 10))
        files_grid.columnconfigure((0, 1), weight=1)

        # ARCHIVO 1: Training Report
        file1_frame = self._create_file_card(
            files_grid,
            title="📊 Enterprise Training Report",
            subtitle="Módulos y calificaciones",
            button_command=self._select_training_file,
            row=0,
            col=0
        )
        self.label_training = self._get_file_label(file1_frame)

        # ARCHIVO 2: Org Planning
        file2_frame = self._create_file_card(
            files_grid,
            title="👥 CSOD Org Planning",
            subtitle="Usuarios y departamentos",
            button_command=self._select_org_planning_file,
            row=0,
            col=1
        )
        self.label_org = self._get_file_label(file2_frame)

    def _create_file_card(self, parent, title, subtitle, button_command, row, col):
        """Crear card compacta para archivo"""
        theme = self.theme_manager.get_current_theme()

        card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=10,
            border_width=1,
            border_color=theme['border']
        )
        card.grid(row=row, column=col, padx=8, pady=5, sticky='ew')

        # Header
        header = ctk.CTkFrame(card, fg_color='transparent')
        header.pack(fill='x', padx=15, pady=(12, 8))

        # Info
        info = ctk.CTkFrame(header, fg_color='transparent')
        info.pack(side='left', fill='x', expand=True)

        title_label = ctk.CTkLabel(
            info,
            text=title,
            font=('Segoe UI', 13, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        title_label.pack(anchor='w')

        subtitle_label = ctk.CTkLabel(
            info,
            text=subtitle,
            font=('Segoe UI', 10),
            text_color=theme['text_secondary'],
            anchor='w'
        )
        subtitle_label.pack(anchor='w')

        # Botón
        btn = ctk.CTkButton(
            header,
            text="📁 Seleccionar",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            command=button_command,
            width=120,
            height=32
        )
        btn.pack(side='right')

        # Label de estado
        file_label = ctk.CTkLabel(
            card,
            text="⚠ No seleccionado",
            font=('Segoe UI', 9),
            text_color=theme['text_tertiary'],
            anchor='w'
        )
        file_label.pack(anchor='w', padx=15, pady=(0, 12))

        # Guardar referencia
        card.file_label = file_label

        return card

    def _get_file_label(self, card):
        """Obtener label de archivo de una card"""
        return card.file_label

    def _create_preview_section(self, parent, theme):
        """Sección de preview y validación"""

        # Título
        section_title = ctk.CTkLabel(
            parent,
            text="🔍 Preview y Validación",
            font=('Segoe UI', 15, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        section_title.pack(anchor='w', pady=(0, 12))

        # Tabs para preview
        self.preview_tabs = ctk.CTkTabview(parent, height=300)
        self.preview_tabs.pack(fill='both', expand=True, pady=(0, 10))

        # Tab 1: Training Report
        self.tab_preview_training = self.preview_tabs.add("📊 Training Report")
        self._create_preview_content(self.tab_preview_training, "training")

        # Tab 2: Org Planning
        self.tab_preview_org = self.preview_tabs.add("👥 Org Planning")
        self._create_preview_content(self.tab_preview_org, "org")

        # Tab 3: Validación
        self.tab_validation = self.preview_tabs.add("✅ Validación")
        self._create_validation_content(self.tab_validation)

    def _create_preview_content(self, parent, tipo):
        """Crear contenido de preview"""
        theme = self.theme_manager.get_current_theme()

        # Mensaje inicial
        msg = ctk.CTkLabel(
            parent,
            text=f"📋 Selecciona un archivo {tipo.upper()} para ver el preview",
            font=('Segoe UI', 12),
            text_color=theme['text_secondary']
        )
        msg.pack(expand=True)

        # Guardar referencia
        if tipo == "training":
            self.preview_training_frame = parent
            self.preview_training_msg = msg
        else:
            self.preview_org_frame = parent
            self.preview_org_msg = msg

    def _create_validation_content(self, parent):
        """Crear contenido de validación"""
        theme = self.theme_manager.get_current_theme()

        # Textbox para resultados de validación
        self.validation_text = ctk.CTkTextbox(
            parent,
            font=('Consolas', 10),
            fg_color=theme['background'],
            text_color=theme['text'],
            wrap='word'
        )
        self.validation_text.pack(fill='both', expand=True, padx=10, pady=10)

        self.validation_text.insert('1.0', "✓ Selecciona archivos y haz clic en 'Validar Datos' para verificar la estructura.\n\n")
        self.validation_text.configure(state='disabled')

    def _create_actions_section(self, parent, theme):
        """Sección de botones de acción"""

        # Grid para botones
        actions_grid = ctk.CTkFrame(parent, fg_color='transparent')
        actions_grid.pack(fill='x', pady=5)
        actions_grid.columnconfigure((0, 1, 2, 3), weight=1)

        # Botón Validar
        self.btn_validar = ctk.CTkButton(
            actions_grid,
            text="🔍 Validar Datos",
            font=('Segoe UI', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_horizon_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=45,
            corner_radius=10,
            command=self._validar_datos
        )
        self.btn_validar.grid(row=0, column=0, padx=4, sticky='ew')

        # Botón Importar Todo
        self.btn_importar_todo = ctk.CTkButton(
            actions_grid,
            text="🚀 Importar Todo",
            font=('Segoe UI', 12, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            hover_color='#51cf66',
            text_color='white',
            height=45,
            corner_radius=10,
            command=self._importar_todo
        )
        self.btn_importar_todo.grid(row=0, column=1, padx=4, sticky='ew')

        # Botón Solo Training
        self.btn_importar_training = ctk.CTkButton(
            actions_grid,
            text="📊 Solo Training",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color='white',
            height=45,
            corner_radius=10,
            command=self._importar_training
        )
        self.btn_importar_training.grid(row=0, column=2, padx=4, sticky='ew')

        # Botón Solo Org
        self.btn_importar_org = ctk.CTkButton(
            actions_grid,
            text="👥 Solo Org",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            hover_color='#001a3d',
            text_color='white',
            height=45,
            corner_radius=10,
            command=self._importar_org
        )
        self.btn_importar_org.grid(row=0, column=3, padx=4, sticky='ew')

    def _create_log_section(self, parent, theme):
        """Sección de log"""

        # Título
        log_title = ctk.CTkLabel(
            parent,
            text="📋 Log de Operaciones",
            font=('Segoe UI', 15, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        log_title.pack(anchor='w', pady=(0, 8))

        # Textbox para log
        log_frame = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=10,
            border_width=1,
            border_color=theme['border']
        )
        log_frame.pack(fill='both', expand=True)

        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=('Consolas', 9),
            fg_color=theme['background'],
            text_color=theme['text'],
            wrap='word',
            height=250
        )
        self.log_text.pack(fill='both', expand=True, padx=12, pady=12)

        # Log inicial
        self.log("✓ Sistema de importación inicializado correctamente")
        self.log("📌 Selecciona archivos Excel para comenzar")

    # ========== MÉTODOS DE SELECCIÓN DE ARCHIVOS ==========

    def _select_training_file(self):
        """Seleccionar archivo Training Report con validación"""
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

            # Actualizar label
            self.label_training.configure(
                text=f"✅ {filename}",
                text_color=HUTCHISON_COLORS['success']
            )

            self.log(f"✅ Training Report: {filename}")

            # Cargar preview
            self._load_preview_training(file)

    def _select_org_planning_file(self):
        """Seleccionar archivo Org Planning con validación"""
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

            # Actualizar label
            self.label_org.configure(
                text=f"✅ {filename}",
                text_color=HUTCHISON_COLORS['success']
            )

            self.log(f"✅ Org Planning: {filename}")

            # Cargar preview
            self._load_preview_org(file)

    # ========== MÉTODOS DE PREVIEW ==========

    def _load_preview_training(self, file_path):
        """Cargar preview del Training Report"""
        try:
            self.log("🔄 Cargando preview de Training Report...")

            # Leer Excel
            df = pd.read_excel(file_path, nrows=10)
            self.df_training_preview = df

            # Limpiar frame
            for widget in self.preview_training_frame.winfo_children():
                widget.destroy()

            # Crear tabla de preview
            self._create_preview_table(self.preview_training_frame, df, "Training Report")

            self.log(f"✓ Preview cargado: {len(df.columns)} columnas, primeras 10 filas")

        except Exception as e:
            self.log(f"❌ Error cargando preview: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el preview:\n{str(e)}")

    def _load_preview_org(self, file_path):
        """Cargar preview del Org Planning"""
        try:
            self.log("🔄 Cargando preview de Org Planning...")

            # Leer Excel
            df = pd.read_excel(file_path, nrows=10)
            self.df_org_preview = df

            # Limpiar frame
            for widget in self.preview_org_frame.winfo_children():
                widget.destroy()

            # Crear tabla de preview
            self._create_preview_table(self.preview_org_frame, df, "Org Planning")

            self.log(f"✓ Preview cargado: {len(df.columns)} columnas, primeras 10 filas")

        except Exception as e:
            self.log(f"❌ Error cargando preview: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el preview:\n{str(e)}")

    def _create_preview_table(self, parent, df, title):
        """Crear tabla visual de preview"""
        theme = self.theme_manager.get_current_theme()

        # Contenedor con scroll
        scroll_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Info
        info_label = ctk.CTkLabel(
            scroll_frame,
            text=f"📊 {title} - Primeras {len(df)} filas de {len(df.columns)} columnas",
            font=('Segoe UI', 11, 'bold'),
            text_color=theme['text'],
            anchor='w'
        )
        info_label.pack(anchor='w', pady=(5, 10))

        # Crear tabla simple
        table_frame = ctk.CTkFrame(scroll_frame, fg_color=theme['surface'])
        table_frame.pack(fill='both', expand=True)

        # Headers (primeras 5 columnas)
        cols_to_show = min(5, len(df.columns))
        header_frame = ctk.CTkFrame(table_frame, fg_color=theme['surface_light'])
        header_frame.pack(fill='x', padx=5, pady=5)

        for i, col in enumerate(df.columns[:cols_to_show]):
            header_label = ctk.CTkLabel(
                header_frame,
                text=str(col)[:20],  # Truncar a 20 chars
                font=('Segoe UI', 10, 'bold'),
                text_color=theme['text'],
                width=150,
                anchor='w'
            )
            header_label.grid(row=0, column=i, padx=2, pady=5, sticky='w')

        # Datos
        for row_idx, row in df.head(10).iterrows():
            row_frame = ctk.CTkFrame(table_frame, fg_color='transparent')
            row_frame.pack(fill='x', padx=5, pady=1)

            for col_idx, col in enumerate(df.columns[:cols_to_show]):
                value = str(row[col])[:30] if pd.notna(row[col]) else "-"

                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=('Segoe UI', 9),
                    text_color=theme['text_secondary'],
                    width=150,
                    anchor='w'
                )
                cell_label.grid(row=0, column=col_idx, padx=2, pady=2, sticky='w')

        # Nota si hay más columnas
        if len(df.columns) > 5:
            note = ctk.CTkLabel(
                scroll_frame,
                text=f"💡 Mostrando 5 de {len(df.columns)} columnas totales",
                font=('Segoe UI', 9, 'italic'),
                text_color=theme['text_tertiary'],
                anchor='w'
            )
            note.pack(anchor='w', pady=(5, 0))

    # ========== VALIDACIÓN ==========

    def _validar_datos(self):
        """Validar estructura de archivos"""
        if not self.archivo_training and not self.archivo_org_planning:
            messagebox.showwarning(
                "Sin archivos",
                "Selecciona al menos un archivo para validar."
            )
            return

        self.validation_text.configure(state='normal')
        self.validation_text.delete('1.0', 'end')
        self.validation_text.insert('1.0', "🔍 VALIDACIÓN DE ARCHIVOS\n" + "="*60 + "\n\n")

        # Validar Training Report
        if self.archivo_training:
            self.validation_text.insert('end', "📊 TRAINING REPORT:\n")
            resultado = self._validar_training_report(self.archivo_training)
            self.validation_text.insert('end', resultado + "\n\n")

        # Validar Org Planning
        if self.archivo_org_planning:
            self.validation_text.insert('end', "👥 ORG PLANNING:\n")
            resultado = self._validar_org_planning(self.archivo_org_planning)
            self.validation_text.insert('end', resultado + "\n\n")

        self.validation_text.insert('end', "="*60 + "\n✅ Validación completada\n")
        self.validation_text.configure(state='disabled')

        # Cambiar a tab de validación
        self.preview_tabs.set("✅ Validación")

    def _validar_training_report(self, file_path):
        """Validar estructura del Training Report"""
        try:
            df = pd.read_excel(file_path, nrows=5)

            # Columnas esperadas (ajustar según tu estructura real)
            cols_requeridas = ['User Id', 'Training Name', 'Status']
            cols_opcionales = ['Score', 'Completion Date', 'Due Date']

            resultado = []
            resultado.append(f"  ✓ Archivo leído: {len(df)} filas de muestra")
            resultado.append(f"  ✓ Total columnas: {len(df.columns)}")

            # Verificar columnas requeridas
            faltantes = [col for col in cols_requeridas if col not in df.columns]
            if faltantes:
                resultado.append(f"  ⚠ Columnas faltantes: {', '.join(faltantes)}")
            else:
                resultado.append("  ✓ Todas las columnas requeridas presentes")

            # Verificar columnas opcionales
            opcionales_presentes = [col for col in cols_opcionales if col in df.columns]
            if opcionales_presentes:
                resultado.append(f"  ✓ Columnas opcionales: {', '.join(opcionales_presentes)}")

            return '\n'.join(resultado)

        except Exception as e:
            return f"  ❌ Error: {str(e)}"

    def _validar_org_planning(self, file_path):
        """Validar estructura del Org Planning"""
        try:
            df = pd.read_excel(file_path, nrows=5)

            # Columnas esperadas
            cols_requeridas = ['User Id', 'User Email', 'Name']
            cols_opcionales = ['Position', 'Division', 'Location']

            resultado = []
            resultado.append(f"  ✓ Archivo leído: {len(df)} filas de muestra")
            resultado.append(f"  ✓ Total columnas: {len(df.columns)}")

            # Verificar columnas requeridas
            faltantes = [col for col in cols_requeridas if col not in df.columns]
            if faltantes:
                resultado.append(f"  ⚠ Columnas faltantes: {', '.join(faltantes)}")
            else:
                resultado.append("  ✓ Todas las columnas requeridas presentes")

            # Verificar columnas opcionales
            opcionales_presentes = [col for col in cols_opcionales if col in df.columns]
            if opcionales_presentes:
                resultado.append(f"  ✓ Columnas opcionales: {', '.join(opcionales_presentes)}")

            return '\n'.join(resultado)

        except Exception as e:
            return f"  ❌ Error: {str(e)}"

    # ========== MÉTODOS DE IMPORTACIÓN ==========

    def _importar_todo(self):
        """Importar ambos archivos"""
        if not self.archivo_training or not self.archivo_org_planning:
            messagebox.showwarning(
                "Archivos faltantes",
                "Selecciona ambos archivos antes de importar."
            )
            return

        if self.importando:
            messagebox.showinfo("Importación en curso", "Ya hay una importación en progreso.")
            return

        # Confirmar
        respuesta = messagebox.askyesno(
            "Confirmar Importación",
            "¿Importar ambos archivos?\n\n"
            "Esto actualizará:\n"
            "• Estatus de módulos\n"
            "• Calificaciones\n"
            "• Datos de usuarios\n"
            "• Departamentos y cargos\n\n"
            "¿Continuar?"
        )

        if respuesta:
            self._ejecutar_importacion(importar_training=True, importar_org=True)

    def _importar_training(self):
        """Importar solo Training Report"""
        if not self.archivo_training:
            messagebox.showwarning(
                "Archivo faltante",
                "Selecciona el archivo Training Report."
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
                "Selecciona el archivo Org Planning."
            )
            return

        if self.importando:
            return

        self._ejecutar_importacion(importar_training=False, importar_org=True)

    def _ejecutar_importacion(self, importar_training=False, importar_org=False):
        """Ejecutar importación en thread separado"""
        self.importando = True
        self._deshabilitar_botones()
        self.log("\n" + "="*70)
        self.log("🚀 INICIANDO IMPORTACIÓN...")
        self.log("="*70)

        # Ejecutar en thread
        thread = threading.Thread(
            target=self._proceso_importacion,
            args=(importar_training, importar_org),
            daemon=True
        )
        thread.start()

    def _proceso_importacion(self, importar_training, importar_org):
        """Proceso de importación (thread separado)"""
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

            # Reporte final
            reporte = importador.generar_reporte()
            self.log_thread("\n" + reporte)

            # Notificar éxito
            self.after(0, lambda: messagebox.showinfo(
                "✅ Importación Completada",
                "Datos importados exitosamente.\nRevisa el log para detalles."
            ))

        except Exception as e:
            error_msg = f"❌ ERROR: {str(e)}"
            self.log_thread(error_msg)
            import traceback
            self.log_thread(traceback.format_exc())

            self.after(0, lambda: messagebox.showerror(
                "Error de Importación",
                f"Error durante la importación:\n\n{str(e)}"
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

    def _deshabilitar_botones(self):
        """Deshabilitar botones durante importación"""
        self.btn_validar.configure(state='disabled')
        self.btn_importar_todo.configure(state='disabled')
        self.btn_importar_training.configure(state='disabled')
        self.btn_importar_org.configure(state='disabled')

    def _habilitar_botones(self):
        """Habilitar botones después de importación"""
        self.btn_validar.configure(state='normal')
        self.btn_importar_todo.configure(state='normal')
        self.btn_importar_training.configure(state='normal')
        self.btn_importar_org.configure(state='normal')
