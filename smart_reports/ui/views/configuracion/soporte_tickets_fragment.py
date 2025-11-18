"""
SoporteTicketsFragment - Fragment para registro de soporte brindado
Separado según arquitectura Android Studio
"""
import customtkinter as ctk
from tkinter import messagebox
from src.main.res.config.gestor_temas import get_theme_manager


class SoporteTicketsFragment(ctk.CTkFrame):
    """Fragment de Registro de Soporte Brindado"""

    def __init__(self, parent, db_connection=None, on_back=None, **kwargs):
        """
        Args:
            parent: Widget padre
            db_connection: Conexión a la base de datos
            on_back: Callback para volver al menú principal
        """
        super().__init__(parent, fg_color='transparent', **kwargs)

        self.db = db_connection
        self.cursor = db_connection.cursor() if db_connection else None
        self.on_back = on_back
        self.theme_manager = get_theme_manager()

        # Crear interfaz
        self._create_interface()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_interface(self):
        """Crear interfaz completa del fragment"""
        theme = self.theme_manager.get_current_theme()

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header con botón volver
        self._create_header(scroll_frame, theme)

        # Card de formulario
        self._create_form_card(scroll_frame, theme)

    def _create_header(self, parent, theme):
        """Crear header con título y botón volver"""
        header = ctk.CTkFrame(parent, fg_color='transparent', height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text='← Volver',
            font=('Montserrat', 14, 'bold'),
            fg_color=theme['surface'],
            text_color=theme['text'],
            hover_color=theme['surface_light'],
            corner_radius=10,
            width=120,
            height=40,
            command=self.on_back if self.on_back else None
        )
        back_btn.pack(side='left')

        # Título
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        title = ctk.CTkLabel(
            header,
            text='📝 Registro de Soporte Brindado',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        )
        title.pack(side='left', padx=20)

    def _create_form_card(self, parent, theme):
        """Card de formulario de registro de soporte"""
        form_card = ctk.CTkFrame(
            parent,
            fg_color=theme['surface'],
            corner_radius=15,
            border_width=1,
            border_color=theme['border']
        )
        form_card.pack(fill='both', expand=True)

        # Contenido del formulario
        form_content = ctk.CTkFrame(form_card, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=30, pady=30)

        # Campo User ID del Usuario
        ctk.CTkLabel(
            form_content,
            text='User ID del Usuario:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.soporte_userid = ctk.CTkEntry(
            form_content,
            placeholder_text='Ej: E12345',
            font=('Montserrat', 14),
            height=45,
            corner_radius=10
        )
        self.soporte_userid.pack(fill='x', pady=(0, 20))

        # Campo Asunto
        ctk.CTkLabel(
            form_content,
            text='Asunto:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.ticket_asunto = ctk.CTkEntry(
            form_content,
            placeholder_text='Resumen del soporte brindado...',
            font=('Montserrat', 14),
            height=45,
            corner_radius=10
        )
        self.ticket_asunto.pack(fill='x', pady=(0, 20))

        # Campo Descripción
        ctk.CTkLabel(
            form_content,
            text='Descripción del Problema y Solución:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        textbox_bg = theme['background'] if self.theme_manager.is_dark_mode() else '#f5f5f5'
        self.ticket_descripcion = ctk.CTkTextbox(
            form_content,
            fg_color=textbox_bg,
            border_color=theme['border'],
            border_width=1,
            corner_radius=10,
            font=('Montserrat', 13),
            text_color=theme['text'],
            height=300
        )
        self.ticket_descripcion.insert("1.0", "Problema reportado:\n\n\nSolución brindada:\n\n")
        self.ticket_descripcion.pack(fill='both', expand=True, pady=(0, 20))

        # Campo Categoría
        ctk.CTkLabel(
            form_content,
            text='Categoría:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).pack(anchor='w', pady=(0, 10))

        self.ticket_categoria = ctk.CTkOptionMenu(
            form_content,
            values=['Técnico', 'Funcional', 'Acceso/Permisos', 'Datos', 'Otro'],
            font=('Montserrat', 14),
            width=250,
            height=45,
            corner_radius=10
        )
        self.ticket_categoria.pack(anchor='w', pady=(0, 30))

        # Botones de acción
        button_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        button_frame.pack(fill='x')

        button_color = self._get_button_color()

        ctk.CTkButton(
            button_frame,
            text='💾 Guardar Registro',
            font=('Montserrat', 16, 'bold'),
            fg_color=button_color,
            hover_color=self._get_button_hover_color(button_color),
            corner_radius=10,
            height=50,
            width=200,
            command=self._submit_ticket
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            button_frame,
            text='🗑️ Limpiar',
            font=('Montserrat', 16, 'bold'),
            fg_color=theme['surface_light'],
            text_color=theme['text'],
            hover_color=theme['border'],
            corner_radius=10,
            height=50,
            width=150,
            command=self._clear_ticket_form
        ).pack(side='left', padx=5)

    # ==================== LÓGICA DE NEGOCIO ====================

    def _submit_ticket(self):
        """Guardar registro de soporte brindado"""
        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        userid = self.soporte_userid.get().strip()
        asunto = self.ticket_asunto.get().strip()
        descripcion = self.ticket_descripcion.get("1.0", "end-1c").strip()
        categoria = self.ticket_categoria.get()

        if not userid or not asunto or not descripcion:
            messagebox.showwarning("Campos Requeridos", "User ID, Asunto y Descripción son obligatorios")
            return

        try:
            # Detectar tipo de base de datos
            from src.main.res.config.database import DB_TYPE
            is_mysql = DB_TYPE == 'mysql'
            placeholder = '%s' if is_mysql else '?'

            # Verificar que la tabla existe (compatible con ambas BD)
            if is_mysql:
                self.cursor.execute("""
                    SELECT COUNT(*)
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Instituto_Soporte'
                """)
            else:
                self.cursor.execute("""
                    SELECT COUNT(*)
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_NAME = 'Instituto_Soporte'
                """)

            tabla_existe = self.cursor.fetchone()[0] > 0

            if not tabla_existe:
                db_name = "MySQL" if is_mysql else "SQL Server Management Studio"
                messagebox.showerror(
                    "Error - Tabla No Existe",
                    f"La tabla 'Instituto_Soporte' no existe en la base de datos.\n\n"
                    f"Por favor, ejecuta el script SQL:\n"
                    f"database/create_soporte_table.sql\n\n"
                    f"en {db_name} para crear la tabla."
                )
                return

            # Verificar que el usuario existe
            self.cursor.execute(f"SELECT UserId FROM instituto_Usuario WHERE UserId = {placeholder}", (userid,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", f"El User ID '{userid}' no existe en el sistema")
                return

            # Insertar el registro de soporte (compatible con ambas BD)
            if is_mysql:
                insert_query = f"""
                    INSERT INTO Instituto_Soporte
                    (UserId, Asunto, Descripcion, Categoria, FechaRegistro)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, NOW())
                """
            else:
                insert_query = f"""
                    INSERT INTO Instituto_Soporte
                    (UserId, Asunto, Descripcion, Categoria, FechaRegistro)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, GETDATE())
                """

            self.cursor.execute(insert_query, (userid, asunto, descripcion, categoria))
            self.db.commit()

            messagebox.showinfo(
                "Registro Guardado",
                f"Registro de soporte guardado exitosamente\n\n"
                f"Usuario: {userid}\n"
                f"Asunto: {asunto}\n"
                f"Categoría: {categoria}\n\n"
                f"El registro ha sido almacenado en el sistema."
            )

            # Limpiar formulario
            self._clear_ticket_form()

        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Error al guardar registro de soporte:\n\n{str(e)}")

    def _clear_ticket_form(self):
        """Limpiar formulario de registro de soporte"""
        self.soporte_userid.delete(0, 'end')
        self.ticket_asunto.delete(0, 'end')
        self.ticket_descripcion.delete("1.0", "end")
        self.ticket_descripcion.insert("1.0", "Problema reportado:\n\n\nSolución brindada:\n\n")
        self.ticket_categoria.set('Técnico')

    # ==================== UTILIDADES ====================

    def _get_button_color(self):
        """Obtener color de botón según tema"""
        is_dark = self.theme_manager.is_dark_mode()
        return '#6c63ff' if is_dark else '#002E6D'

    def _get_button_hover_color(self, base_color):
        """Obtener color hover"""
        if base_color == '#6c63ff':
            return '#5a52d5'
        elif base_color == '#002E6D':
            return '#00509E'
        return base_color

    def _on_theme_changed(self, theme_colors):
        """Callback para cambios de tema"""
        pass
