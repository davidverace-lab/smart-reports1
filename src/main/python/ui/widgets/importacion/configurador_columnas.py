"""
Configurador de Mapeo de Columnas
Permite personalizar qué columnas de Excel se mapean a qué campos de BD
"""
import customtkinter as ctk
from tkinter import messagebox
import json
import os
from config.gestor_temas import get_theme_manager
from config.themes import HUTCHISON_COLORS


class ConfiguradorColumnas(ctk.CTkToplevel):
    """
    Ventana para configurar mapeo de columnas Excel → BD

    Permite:
    - Ver columnas detectadas en Excel
    - Mapear a campos de la base de datos
    - Guardar/cargar configuraciones
    - Validar mapeos
    """

    def __init__(self, parent, columnas_excel, campos_bd, **kwargs):
        """
        Args:
            parent: Ventana padre
            columnas_excel: Lista de columnas encontradas en Excel
            campos_bd: Diccionario de campos de BD disponibles
        """
        super().__init__(parent, **kwargs)

        self.theme_manager = get_theme_manager()
        self.columnas_excel = columnas_excel
        self.campos_bd = campos_bd
        self.mapeos = {}
        self.mapeo_guardado = False

        # Configurar ventana
        self.title("⚙ Configuración de Mapeo de Columnas")
        self.geometry("800x600")
        self.resizable(True, True)

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"800x600+{x}+{y}")

        self._create_ui()
        self._cargar_mapeo_predeterminado()

    def _create_ui(self):
        """Crear interfaz"""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = ctk.CTkFrame(self, fg_color=HUTCHISON_COLORS['ports_sea_blue'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="⚙ Configuración de Mapeo de Columnas",
            font=('Segoe UI', 18, 'bold'),
            text_color='white'
        )
        title.pack(side='left', padx=20, pady=15)

        # Botones header
        btn_frame = ctk.CTkFrame(header, fg_color='transparent')
        btn_frame.pack(side='right', padx=10)

        btn_guardar_config = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Config",
            font=('Segoe UI', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            width=130,
            height=30,
            command=self._guardar_configuracion
        )
        btn_guardar_config.pack(side='left', padx=5)

        btn_cargar_config = ctk.CTkButton(
            btn_frame,
            text="📂 Cargar Config",
            font=('Segoe UI', 10, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            width=130,
            height=30,
            command=self._cargar_configuracion
        )
        btn_cargar_config.pack(side='left', padx=5)

        # Info
        info = ctk.CTkLabel(
            self,
            text="Mapea las columnas de Excel a los campos de la base de datos:",
            font=('Segoe UI', 11),
            text_color=theme['text_secondary']
        )
        info.pack(padx=20, pady=(15, 10))

        # Área de mapeo scrollable
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))

        # Grid de mapeos
        self.mapeo_rows = []
        for i, col_excel in enumerate(self.columnas_excel):
            row_frame = self._create_mapeo_row(scroll_frame, col_excel, i)
            row_frame.pack(fill='x', pady=3)
            self.mapeo_rows.append(row_frame)

        # Botones finales
        buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        buttons_frame.pack(fill='x', padx=20, pady=(0, 15))

        btn_cancelar = ctk.CTkButton(
            buttons_frame,
            text="✖ Cancelar",
            font=('Segoe UI', 11, 'bold'),
            fg_color=theme['border'],
            hover_color=theme['surface_light'],
            text_color=theme['text'],
            width=120,
            command=self.destroy
        )
        btn_cancelar.pack(side='left')

        btn_validar = ctk.CTkButton(
            buttons_frame,
            text="🔍 Validar",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['warning'],
            width=120,
            command=self._validar_mapeos
        )
        btn_validar.pack(side='left', padx=10)

        btn_aplicar = ctk.CTkButton(
            buttons_frame,
            text="✓ Aplicar",
            font=('Segoe UI', 11, 'bold'),
            fg_color=HUTCHISON_COLORS['success'],
            width=120,
            command=self._aplicar_mapeos
        )
        btn_aplicar.pack(side='right')

    def _create_mapeo_row(self, parent, columna_excel, index):
        """Crear fila de mapeo"""
        theme = self.theme_manager.get_current_theme()

        row = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=8,
            border_width=1,
            border_color=theme['border']
        )

        # Columna Excel (izquierda)
        excel_label = ctk.CTkLabel(
            row,
            text=f"📊 {columna_excel}",
            font=('Segoe UI', 11, 'bold'),
            text_color=theme['text'],
            width=250,
            anchor='w'
        )
        excel_label.pack(side='left', padx=15, pady=10)

        # Flecha
        arrow = ctk.CTkLabel(
            row,
            text="→",
            font=('Segoe UI', 14, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sky_blue']
        )
        arrow.pack(side='left', padx=10)

        # Dropdown de campos BD (derecha)
        opciones = ["(Sin mapear)"] + list(self.campos_bd.keys())

        dropdown = ctk.CTkOptionMenu(
            row,
            values=opciones,
            font=('Segoe UI', 11),
            fg_color=HUTCHISON_COLORS['ports_horizon_blue'],
            button_color=HUTCHISON_COLORS['ports_sea_blue'],
            button_hover_color=HUTCHISON_COLORS['ports_sky_blue'],
            width=250
        )
        dropdown.pack(side='left', padx=15, pady=10)
        dropdown.set("(Sin mapear)")

        # Guardar referencia
        row.columna_excel = columna_excel
        row.dropdown = dropdown

        return row

    def _cargar_mapeo_predeterminado(self):
        """Cargar mapeo predeterminado basado en nombres similares"""
        # Mapeos comunes conocidos
        mapeos_comunes = {
            'User Id': 'UserId',
            'UserId': 'UserId',
            'User Email': 'UserEmail',
            'Email': 'UserEmail',
            'Name': 'NombreCompleto',
            'Training Name': 'NombreModulo',
            'Status': 'EstatusModulo',
            'Score': 'Calificacion',
            'Completion Date': 'FechaFinalizacion',
            'Due Date': 'FechaVencimiento',
            'Position': 'Position',
            'Division': 'Division',
            'Location': 'Ubicacion'
        }

        for row in self.mapeo_rows:
            col_excel = row.columna_excel

            # Buscar mapeo automático
            if col_excel in mapeos_comunes:
                campo_bd = mapeos_comunes[col_excel]
                if campo_bd in self.campos_bd:
                    row.dropdown.set(campo_bd)

    def _validar_mapeos(self):
        """Validar que los mapeos sean correctos"""
        mapeos_actuales = {}
        campos_usados = set()
        errores = []

        for row in self.mapeo_rows:
            campo_seleccionado = row.dropdown.get()

            if campo_seleccionado != "(Sin mapear)":
                # Verificar duplicados
                if campo_seleccionado in campos_usados:
                    errores.append(f"⚠ Campo '{campo_seleccionado}' está mapeado más de una vez")
                else:
                    campos_usados.add(campo_seleccionado)

                mapeos_actuales[row.columna_excel] = campo_seleccionado

        # Verificar campos requeridos
        campos_requeridos = ['UserId', 'NombreModulo']  # Ajustar según necesidad
        for campo_req in campos_requeridos:
            if campo_req not in campos_usados:
                errores.append(f"❌ Campo requerido '{campo_req}' no está mapeado")

        # Mostrar resultados
        if errores:
            mensaje = "Se encontraron problemas:\n\n" + "\n".join(errores)
            messagebox.showwarning("Validación de Mapeos", mensaje)
        else:
            messagebox.showinfo(
                "✅ Validación Exitosa",
                f"Mapeos válidos:\n\n"
                f"• {len(mapeos_actuales)} columnas mapeadas\n"
                f"• Todos los campos requeridos presentes"
            )

    def _aplicar_mapeos(self):
        """Aplicar mapeos y cerrar"""
        self.mapeos = {}

        for row in self.mapeo_rows:
            campo_seleccionado = row.dropdown.get()
            if campo_seleccionado != "(Sin mapear)":
                self.mapeos[row.columna_excel] = campo_seleccionado

        self.mapeo_guardado = True
        self.destroy()

    def _guardar_configuracion(self):
        """Guardar configuración de mapeo en archivo JSON"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            title="Guardar Configuración de Mapeo",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            config = {}
            for row in self.mapeo_rows:
                campo = row.dropdown.get()
                if campo != "(Sin mapear)":
                    config[row.columna_excel] = campo

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("✅ Guardado", f"Configuración guardada en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")

    def _cargar_configuracion(self):
        """Cargar configuración de mapeo desde archivo JSON"""
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Cargar Configuración de Mapeo",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # Aplicar configuración
                for row in self.mapeo_rows:
                    if row.columna_excel in config:
                        campo = config[row.columna_excel]
                        if campo in self.campos_bd or campo == "(Sin mapear)":
                            row.dropdown.set(campo)

                messagebox.showinfo("✅ Cargado", "Configuración aplicada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar:\n{str(e)}")

    def get_mapeos(self):
        """Obtener diccionario de mapeos aplicados"""
        return self.mapeos if self.mapeo_guardado else {}
