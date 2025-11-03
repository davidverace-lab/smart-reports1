"""
Diálogo de Gestión de Usuarios - Formulario para agregar/editar usuarios
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk


class UserManagementDialog(ctk.CTkToplevel):
    """Diálogo modal para gestión de usuarios"""

    def __init__(self, parent, db_connection, **kwargs):
        """
        Args:
            parent: Ventana padre
            db_connection: Conexión a la base de datos
        """
        super().__init__(parent, **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None
        self.result = None

        # Configurar ventana
        self.title("Gestión de Usuarios")
        self.geometry("800x700")

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        # Centrar en pantalla
        self.center_window()

        # Crear interfaz
        self._create_interface()

        # Cargar datos iniciales
        self._load_business_units()

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_interface(self):
        """Crear interfaz del diálogo"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color='#1a1d2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))

        title = ctk.CTkLabel(
            header,
            text='👥 Gestión de Usuarios',
            font=('Segoe UI', 28, 'bold'),
            text_color='#ffffff'
        )
        title.pack(side='left')

        # Panel de búsqueda
        search_panel = ctk.CTkFrame(main_frame, fg_color='#2b2d42', corner_radius=15, border_width=1, border_color='#3a3d5c')
        search_panel.pack(fill='x', pady=(0, 15))

        search_container = ctk.CTkFrame(search_panel, fg_color='transparent')
        search_container.pack(fill='x', padx=30, pady=20)

        ctk.CTkLabel(
            search_container,
            text='🔍  Buscar Usuario por ID:',
            font=('Segoe UI', 14, 'bold'),
            text_color='#ffffff'
        ).pack(side='left', padx=(0, 10))

        self.search_id_entry = ctk.CTkEntry(
            search_container,
            placeholder_text='Ingrese User ID para buscar...',
            font=('Segoe UI', 13),
            width=300,
            height=40,
            corner_radius=10
        )
        self.search_id_entry.pack(side='left', padx=5)

        search_btn = ctk.CTkButton(
            search_container,
            text='Buscar',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#6c63ff',
            hover_color='#5a52d5',
            corner_radius=10,
            height=40,
            width=120,
            command=self._search_user
        )
        search_btn.pack(side='left', padx=5)

        self.search_result_label = ctk.CTkLabel(
            search_container,
            text='',
            font=('Segoe UI', 11),
            text_color='#a0a0b0'
        )
        self.search_result_label.pack(side='left', padx=10)

        # Scroll frame para formulario
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color='#2b2d42',
            corner_radius=15,
            scrollbar_button_color='#3a3d5c'
        )
        scroll_frame.pack(fill='both', expand=True)

        # Formulario
        form_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        form_container.pack(fill='both', expand=True, padx=30, pady=20)

        # Variable para rastrear si estamos editando un usuario existente
        self.current_user_id = None

        # Campo: User ID
        self._create_form_field(
            form_container, 'User ID:', 'user_id',
            placeholder='Ingrese el ID del usuario (ej: U12345)',
            row=0
        )

        # Campo: Nombre
        self._create_form_field(
            form_container, 'Nombre Completo:', 'nombre',
            placeholder='Ingrese el nombre completo',
            row=1
        )

        # Campo: Email
        self._create_form_field(
            form_container, 'Email:', 'email',
            placeholder='usuario@hutchison.com',
            row=2
        )

        # Campo: Unidad de Negocio (ComboBox)
        label_unit = ctk.CTkLabel(
            form_container,
            text='Unidad de Negocio:',
            font=('Segoe UI', 14, 'bold'),
            text_color='#ffffff'
        )
        label_unit.grid(row=3, column=0, sticky='w', pady=(15, 5))

        self.business_unit_var = tk.StringVar()
        self.business_unit_combo = ctk.CTkComboBox(
            form_container,
            variable=self.business_unit_var,
            font=('Segoe UI', 13),
            width=400,
            height=40,
            corner_radius=10,
            values=['Cargando...']
        )
        self.business_unit_combo.grid(row=3, column=1, sticky='w', pady=(15, 5))

        # Campo: Nivel
        self._create_form_field(
            form_container, 'Nivel/Puesto:', 'nivel',
            placeholder='Ej: Supervisor, Operador, Jefe de Turno',
            row=4
        )

        # Campo: División
        self._create_form_field(
            form_container, 'División:', 'division',
            placeholder='Ej: Operaciones, Logística, Administración',
            row=5
        )

        # Separador
        separator = ctk.CTkFrame(form_container, height=2, fg_color='#3a3d5c')
        separator.grid(row=6, column=0, columnspan=2, sticky='ew', pady=20)

        # Información adicional
        info_label = ctk.CTkLabel(
            form_container,
            text='ℹ️ Los campos marcados son obligatorios',
            font=('Segoe UI', 12),
            text_color='#a0a0b0'
        )
        info_label.grid(row=7, column=0, columnspan=2, sticky='w', pady=(0, 10))

        # Botones de acción
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(fill='x', pady=(20, 0))

        # Botón Cancelar
        cancel_btn = ctk.CTkButton(
            button_frame,
            text='✖  Cancelar',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#ff6b6b',
            hover_color='#ff5252',
            corner_radius=10,
            height=45,
            width=180,
            command=self._on_cancel
        )
        cancel_btn.pack(side='right', padx=5)

        # Botón Guardar
        save_btn = ctk.CTkButton(
            button_frame,
            text='✓  Guardar Usuario',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#51cf66',
            hover_color='#40c057',
            corner_radius=10,
            height=45,
            width=180,
            command=self._on_save
        )
        save_btn.pack(side='right', padx=5)

        # Botón Limpiar Formulario
        clear_btn = ctk.CTkButton(
            button_frame,
            text='🗑  Limpiar',
            font=('Segoe UI', 14),
            fg_color='#6c6c80',
            hover_color='#5c5c70',
            corner_radius=10,
            height=45,
            width=150,
            command=self._clear_form
        )
        clear_btn.pack(side='left', padx=5)

        # Botón Eliminar
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text='🗑️  Eliminar Usuario',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#ff6b6b',
            hover_color='#ff5252',
            corner_radius=10,
            height=45,
            width=180,
            command=self._on_delete,
            state='disabled'  # Deshabilitado por defecto
        )
        self.delete_btn.pack(side='left', padx=5)

        # Diccionario para almacenar referencias a los campos
        self.form_fields = {}

    def _create_form_field(self, parent, label_text, field_name, placeholder='', row=0):
        """Crear un campo de formulario"""
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=('Segoe UI', 14, 'bold'),
            text_color='#ffffff'
        )
        label.grid(row=row, column=0, sticky='w', pady=(15, 5))

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=('Segoe UI', 13),
            width=400,
            height=40,
            corner_radius=10
        )
        entry.grid(row=row, column=1, sticky='w', pady=(15, 5))

        self.form_fields[field_name] = entry

    def _load_business_units(self):
        """Cargar unidades de negocio desde la BD"""
        if not self.cursor:
            self.business_unit_combo.configure(values=['No hay conexión a BD'])
            return

        try:
            self.cursor.execute("""
                SELECT DISTINCT NombreUnidad
                FROM Instituto_UnidadDeNegocio
                ORDER BY NombreUnidad
            """)
            units = self.cursor.fetchall()
            unit_names = [unit[0] for unit in units]

            if unit_names:
                self.business_unit_combo.configure(values=unit_names)
                self.business_unit_combo.set(unit_names[0])
            else:
                self.business_unit_combo.configure(values=['No hay unidades disponibles'])
        except Exception as e:
            print(f"Error cargando unidades: {e}")
            self.business_unit_combo.configure(values=['Error al cargar unidades'])

    def _validate_form(self):
        """Validar campos del formulario"""
        # Validar User ID
        user_id = self.form_fields['user_id'].get().strip()
        if not user_id:
            messagebox.showerror("Error de Validación", "El User ID es obligatorio")
            return False

        # Validar Nombre
        nombre = self.form_fields['nombre'].get().strip()
        if not nombre:
            messagebox.showerror("Error de Validación", "El Nombre es obligatorio")
            return False

        # Validar Email
        email = self.form_fields['email'].get().strip()
        if not email:
            messagebox.showerror("Error de Validación", "El Email es obligatorio")
            return False

        if '@' not in email or '.' not in email:
            messagebox.showerror("Error de Validación", "El Email no es válido")
            return False

        # Validar Unidad de Negocio
        unit = self.business_unit_var.get()
        if not unit or unit in ['Cargando...', 'No hay conexión a BD', 'No hay unidades disponibles']:
            messagebox.showerror("Error de Validación", "Debe seleccionar una Unidad de Negocio válida")
            return False

        return True

    def _on_save(self):
        """Guardar usuario en la base de datos"""
        if not self._validate_form():
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            # Obtener valores del formulario
            user_id = self.form_fields['user_id'].get().strip()
            nombre = self.form_fields['nombre'].get().strip()
            email = self.form_fields['email'].get().strip()
            unit_name = self.business_unit_var.get()
            nivel = self.form_fields['nivel'].get().strip() or 'No especificado'
            division = self.form_fields['division'].get().strip() or 'No especificada'

            # Obtener ID de unidad de negocio
            self.cursor.execute("""
                SELECT IdUnidadDeNegocio
                FROM Instituto_UnidadDeNegocio
                WHERE NombreUnidad = ?
            """, (unit_name,))

            unit_result = self.cursor.fetchone()
            if not unit_result:
                messagebox.showerror("Error", f"No se encontró la unidad de negocio: {unit_name}")
                return

            unit_id = unit_result[0]

            # Verificar si el usuario ya existe
            self.cursor.execute("""
                SELECT UserId FROM Instituto_Usuario WHERE UserId = ?
            """, (user_id,))

            existing = self.cursor.fetchone()

            if existing:
                # Actualizar usuario existente
                response = messagebox.askyesno(
                    "Usuario Existente",
                    f"El usuario {user_id} ya existe.\n\n¿Desea actualizar su información?"
                )

                if response:
                    self.cursor.execute("""
                        UPDATE Instituto_Usuario
                        SET Nombre = ?, Email = ?, IdUnidadDeNegocio = ?,
                            Nivel = ?, Division = ?
                        WHERE UserId = ?
                    """, (nombre, email, unit_id, nivel, division, user_id))

                    self.db.commit()
                    messagebox.showinfo("Éxito", f"Usuario {user_id} actualizado correctamente")
                    self.result = 'updated'
                    self._clear_form()
            else:
                # Insertar nuevo usuario
                self.cursor.execute("""
                    INSERT INTO Instituto_Usuario
                    (UserId, Nombre, Email, IdUnidadDeNegocio, Nivel, Division)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, nombre, email, unit_id, nivel, division))

                self.db.commit()
                messagebox.showinfo("Éxito", f"Usuario {user_id} creado correctamente")
                self.result = 'created'
                self._clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar usuario:\n{str(e)}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()

    def _search_user(self):
        """Buscar usuario por ID y cargar sus datos en el formulario"""
        search_id = self.search_id_entry.get().strip()

        if not search_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID para buscar")
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Nivel, u.Division
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.UserId = ?
            """, (search_id,))

            result = self.cursor.fetchone()

            if result:
                # Cargar datos en el formulario
                self.form_fields['user_id'].delete(0, 'end')
                self.form_fields['user_id'].insert(0, result[0])

                self.form_fields['nombre'].delete(0, 'end')
                self.form_fields['nombre'].insert(0, result[1] or '')

                self.form_fields['email'].delete(0, 'end')
                self.form_fields['email'].insert(0, result[2] or '')

                if result[3]:
                    self.business_unit_var.set(result[3])

                self.form_fields['nivel'].delete(0, 'end')
                self.form_fields['nivel'].insert(0, result[4] or '')

                self.form_fields['division'].delete(0, 'end')
                self.form_fields['division'].insert(0, result[5] or '')

                # Guardar ID actual y habilitar botón eliminar
                self.current_user_id = result[0]
                self.delete_btn.configure(state='normal')

                self.search_result_label.configure(
                    text=f'✓ Usuario encontrado',
                    text_color='#51cf66'
                )
            else:
                messagebox.showinfo("No Encontrado", f"No se encontró el usuario con ID: {search_id}")
                self.search_result_label.configure(
                    text=f'✗ Usuario no encontrado',
                    text_color='#ff6b6b'
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar usuario:\n{str(e)}")
            print(f"Error detallado: {e}")

    def _on_delete(self):
        """Eliminar usuario de la base de datos"""
        if not self.current_user_id:
            messagebox.showwarning("Advertencia", "No hay un usuario cargado para eliminar")
            return

        # Confirmar eliminación
        response = messagebox.askyesnocancel(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el usuario {self.current_user_id}?\n\n"
            f"Esta acción NO se puede deshacer.\n\n"
            f"IMPORTANTE: También se eliminarán todos los registros de progreso asociados a este usuario."
        )

        if not response:
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            # Eliminar primero los registros relacionados en Instituto_ProgresoModulo
            self.cursor.execute("""
                DELETE FROM Instituto_ProgresoModulo
                WHERE UserId = ?
            """, (self.current_user_id,))

            # Eliminar el usuario
            self.cursor.execute("""
                DELETE FROM Instituto_Usuario
                WHERE UserId = ?
            """, (self.current_user_id,))

            self.db.commit()

            messagebox.showinfo("Éxito", f"Usuario {self.current_user_id} eliminado correctamente")
            self.result = 'deleted'

            # Limpiar formulario y deshabilitar botón eliminar
            self._clear_form()
            self.current_user_id = None
            self.delete_btn.configure(state='disabled')
            self.search_result_label.configure(text='')

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario:\n{str(e)}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()

    def _clear_form(self):
        """Limpiar todos los campos del formulario"""
        for field in self.form_fields.values():
            field.delete(0, 'end')

        # Resetear combobox
        self._load_business_units()

        # Deshabilitar botón eliminar y limpiar ID actual
        self.current_user_id = None
        self.delete_btn.configure(state='disabled')
        self.search_result_label.configure(text='')

    def _on_cancel(self):
        """Cancelar y cerrar diálogo"""
        self.result = 'cancelled'
        self.destroy()
