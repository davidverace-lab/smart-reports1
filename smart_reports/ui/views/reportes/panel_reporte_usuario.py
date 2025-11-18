"""
Panel de Generación de Reportes de Usuario
Permite generar reportes PDF detallados por usuario con vista previa
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import io
import os
from datetime import datetime

# Importar reportlab para PDF
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab no está instalado. Instala con: pip install reportlab")

from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.ui.components.charts.previsualizador_reporte import PrevisualizadorReporte


class UserReportPanel(ctk.CTkFrame):
    """Panel para generar reportes PDF de usuarios con vista previa"""

    def __init__(self, parent, db=None, cursor=None, theme_manager=None):
        super().__init__(parent, fg_color='transparent')

        self.db = db
        self.cursor = cursor
        self.theme_manager = theme_manager or get_theme_manager()

        # Variables para el reporte
        self.current_pdf_buffer = None
        self.current_user_data = None

        # Configurar layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear contenido
        self._create_main_content()

        # Registrar callback de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _on_theme_changed(self, theme_colors: dict):
        """Actualizar colores cuando cambia el tema"""
        try:
            if not self.winfo_exists():
                return

            # Guardar el estado actual del preview y userid
            current_userid = ''
            preview_content = ''
            save_button_state = 'disabled'

            if hasattr(self, 'userid_entry') and self.userid_entry.winfo_exists():
                current_userid = self.userid_entry.get()

            # Preview widget ya no necesita guardar contenido (se regenera)

            if hasattr(self, 'save_button') and self.save_button.winfo_exists():
                save_button_state = str(self.save_button.cget('state'))

            # Recrear el contenido
            self._create_main_content()

            # Restaurar el estado
            if current_userid and hasattr(self, 'userid_entry'):
                self.userid_entry.delete(0, 'end')
                self.userid_entry.insert(0, current_userid)

            # Preview widget se regenera automáticamente si es necesario

            if save_button_state == 'normal' and hasattr(self, 'save_button'):
                self.save_button.configure(state='normal')

        except Exception as e:
            pass

    def destroy(self):
        """Override destroy para desregistrar callback de tema"""
        try:
            self.theme_manager.unregister_callback(self._on_theme_changed)
        except:
            pass
        super().destroy()

    def _create_main_content(self):
        """Crear contenido principal del panel"""
        # Limpiar contenido anterior
        for widget in self.winfo_children():
            widget.destroy()

        theme = self.theme_manager.get_current_theme()

        # Contenedor con scroll
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(scroll_frame, fg_color='transparent', height=80)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)

        # Título
        is_dark = self.theme_manager.is_dark_mode()
        title_color = '#FFFFFF' if is_dark else '#002E6D'

        ctk.CTkLabel(
            header_frame,
            text='📄 Generación de Reportes de Usuario',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        ).grid(row=0, column=0, sticky='w', columnspan=2)

        ctk.CTkLabel(
            header_frame,
            text='Genera reportes PDF detallados del progreso de usuarios',
            font=('Montserrat', 14),
            text_color=theme['colors']['text_secondary']
        ).grid(row=1, column=0, sticky='w', columnspan=2, pady=(5, 0))

        # Sección de entrada de usuario
        input_section = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15
        )
        input_section.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        input_section.grid_columnconfigure(1, weight=1)

        # Padding interno
        input_content = ctk.CTkFrame(input_section, fg_color='transparent')
        input_content.pack(fill='both', expand=True, padx=30, pady=30)
        input_content.grid_columnconfigure(1, weight=1)

        # Label User ID
        ctk.CTkLabel(
            input_content,
            text='User ID:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['colors']['text']
        ).grid(row=0, column=0, sticky='w', pady=10, padx=(0, 15))

        # Entry User ID
        self.userid_entry = ctk.CTkEntry(
            input_content,
            placeholder_text='Ingrese el User ID',
            font=('Montserrat', 14),
            height=45,
            corner_radius=10
        )
        self.userid_entry.grid(row=0, column=1, sticky='ew', pady=10)

        # Botón generar
        button_color = '#002E6D'  # Navy blue
        ctk.CTkButton(
            input_content,
            text='🔍 Generar Vista Previa',
            font=('Montserrat', 16, 'bold'),
            fg_color=button_color,
            hover_color='#003D8F',
            corner_radius=10,
            height=50,
            width=250,
            command=self._generate_preview
        ).grid(row=0, column=2, sticky='e', pady=10, padx=(15, 0))

        # Sección de vista previa
        preview_section = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15
        )
        preview_section.grid(row=2, column=0, sticky='nsew', pady=(0, 20))
        preview_section.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_rowconfigure(2, weight=1)

        # Header de vista previa
        preview_header = ctk.CTkFrame(preview_section, fg_color='transparent')
        preview_header.pack(fill='x', padx=30, pady=(30, 10))
        preview_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            preview_header,
            text='Vista Previa del Reporte',
            font=('Montserrat', 20, 'bold'),
            text_color=theme['colors']['text']
        ).grid(row=0, column=0, sticky='w')

        # Botón guardar (inicialmente oculto)
        self.save_button = ctk.CTkButton(
            preview_header,
            text='💾 Guardar PDF',
            font=('Montserrat', 14, 'bold'),
            fg_color=button_color,
            hover_color='#003D8F',
            corner_radius=10,
            height=45,
            width=180,
            command=self._save_pdf,
            state='disabled'
        )
        self.save_button.grid(row=0, column=1, sticky='e', padx=(15, 0))

        # Área de vista previa - HTML profesional estilo Word
        self.preview_widget = PrevisualizadorReporte(preview_section)
        self.preview_widget.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def _generate_preview(self):
        """Generar vista previa del reporte"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror(
                "Error",
                "ReportLab no está instalado.\n\n"
                "Por favor instala la librería con:\n"
                "pip install reportlab"
            )
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        userid = self.userid_entry.get().strip()
        if not userid:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return

        try:
            # Obtener datos del usuario
            self.cursor.execute("""
                SELECT UserId, NombreCompleto, UserEmail
                FROM Usuario
                WHERE UserId = %s
            """, (userid,))

            user = self.cursor.fetchone()

            if not user:
                messagebox.showerror("Error", f"No se encontró el usuario '{userid}'")
                return

            # Generar PDF
            self._generate_pdf_report(user)

            # Mostrar vista previa en texto
            self._show_preview_text(user)

            # Habilitar botón de guardar
            self.save_button.configure(state='normal')

            messagebox.showinfo(
                "Vista Previa Generada",
                f"Reporte generado para:\n\n"
                f"User ID: {user[0]}\n"
                f"Nombre: {user[1]}\n\n"
                f"Puede guardar el PDF usando el botón 'Guardar PDF'"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n\n{str(e)}")

    def _generate_pdf_report(self, user):
        """Generar el PDF del reporte"""
        # Crear buffer en memoria
        buffer = io.BytesIO()

        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                topMargin=0.5*inch, bottomMargin=0.5*inch,
                                leftMargin=0.5*inch, rightMargin=0.5*inch)

        # Contenedor de elementos
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#002E6D'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER
        )

        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#002E6D'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )

        # Título del reporte
        elements.append(Paragraph("Reporte de Progreso - Instituto Hutchison Ports", title_style))
        elements.append(Spacer(1, 0.1*inch))

        # Información del usuario
        elements.append(Paragraph("Información del Usuario", section_style))
        user_info = [
            ['User ID:', user[0]],
            ['Nombre:', user[1]],
            ['Email:', user[2] if user[2] else 'N/A'],
            ['Fecha de Reporte:', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]

        user_table = Table(user_info, colWidths=[1.5*inch, 5*inch])
        user_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#002E6D')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(user_table)
        elements.append(Spacer(1, 0.3*inch))

        # Tabla de módulos
        elements.append(Paragraph("Progreso por Módulo", section_style))

        # Datos inventados para demostración
        modulos_data = [
            ['Módulo', 'Completado', 'Fecha Finalización', 'Calificación'],
            ['Módulo 1 - Introducción', 'Sí', '15/01/2024', '95%'],
            ['Módulo 2 - Seguridad', 'Sí', '22/01/2024', '88%'],
            ['Módulo 3 - Operaciones', 'Sí', '05/02/2024', '92%'],
            ['Módulo 4 - Logística', 'Sí', '18/02/2024', '90%'],
            ['Módulo 5 - Calidad', 'Sí', '10/03/2024', '87%'],
            ['Módulo 6 - Medio Ambiente', 'Sí', '25/03/2024', '91%'],
            ['Módulo 7 - Administración', 'Sí', '08/04/2024', '89%'],
            ['Módulo 8 - RR.HH.', 'No', 'Pendiente', 'N/A']
        ]

        modulos_table = Table(modulos_data, colWidths=[2.8*inch, 1.1*inch, 1.5*inch, 1.1*inch])
        modulos_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E6D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#002E6D')),
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            # Colores alternados
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))

        elements.append(modulos_table)
        elements.append(Spacer(1, 0.3*inch))

        # Resumen
        elements.append(Paragraph("Resumen de Desempeño", section_style))
        summary_data = [
            ['Módulos Completados:', '7 / 8'],
            ['Promedio General:', '90.3%'],
            ['Estado:', 'En Progreso'],
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 4.5*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#002E6D')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(summary_table)

        # Pie de página
        elements.append(Spacer(1, 0.5*inch))
        footer_text = f"Generado automáticamente por Smart Reports v2.0 - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(footer_text, footer_style))

        # Construir PDF
        doc.build(elements)

        # Guardar buffer
        buffer.seek(0)
        self.current_pdf_buffer = buffer
        self.current_user_data = user

    def _show_preview_text(self, user):
        """Mostrar vista previa en HTML profesional"""
        # Preparar datos del usuario
        datos_usuario = {
            'user_id': user[0],
            'nombre': user[1],
            'email': user[2] if user[2] else 'N/A'
        }

        # Obtener progreso de módulos (datos de ejemplo - ajustar según BD real)
        progreso_modulos = [
            {'modulo': 'Módulo 1 - Introducción', 'completado': True, 'fecha': '15/01/2024', 'calificacion': 95},
            {'modulo': 'Módulo 2 - Seguridad', 'completado': True, 'fecha': '22/01/2024', 'calificacion': 88},
            {'modulo': 'Módulo 3 - Operaciones', 'completado': True, 'fecha': '05/02/2024', 'calificacion': 92},
            {'modulo': 'Módulo 4 - Logística', 'completado': True, 'fecha': '18/02/2024', 'calificacion': 90},
            {'modulo': 'Módulo 5 - Calidad', 'completado': True, 'fecha': '10/03/2024', 'calificacion': 87},
            {'modulo': 'Módulo 6 - Medio Ambiente', 'completado': True, 'fecha': '25/03/2024', 'calificacion': 91},
            {'modulo': 'Módulo 7 - Administración', 'completado': True, 'fecha': '08/04/2024', 'calificacion': 89},
            {'modulo': 'Módulo 8 - RR.HH.', 'completado': False, 'fecha': 'Pendiente', 'calificacion': 0},
        ]

        # Mostrar en widget HTML
        self.preview_widget.mostrar_reporte_usuario(datos_usuario, progreso_modulos)

    def _save_pdf(self):
        """Guardar PDF en PC"""
        if not self.current_pdf_buffer or not self.current_user_data:
            messagebox.showerror("Error", "No hay reporte generado para guardar")
            return

        try:
            # Sugerir nombre de archivo
            default_filename = f"Reporte_{self.current_user_data[0]}_{datetime.now().strftime('%Y%m%d')}.pdf"

            # Abrir diálogo de guardar
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=default_filename
            )

            if file_path:
                # Guardar el PDF
                with open(file_path, 'wb') as f:
                    f.write(self.current_pdf_buffer.getvalue())

                messagebox.showinfo(
                    "PDF Guardado",
                    f"Reporte guardado exitosamente en:\n\n{file_path}"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar PDF:\n\n{str(e)}")
