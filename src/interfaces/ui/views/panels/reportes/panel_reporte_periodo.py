"""
Panel de Generación de Reportes por Periodo
Permite generar reportes PDF por rango de fechas con vista previa
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import io
import os
from datetime import datetime, timedelta
import random

# Importar reportlab para PDF
try:
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab no está instalado. Instala con: pip install reportlab")

from config.gestor_temas import get_theme_manager


class PeriodReportPanel(ctk.CTkFrame):
    """Panel para generar reportes PDF por periodo con vista previa"""

    def __init__(self, parent, db=None, cursor=None, theme_manager=None):
        super().__init__(parent, fg_color='transparent')

        self.db = db
        self.cursor = cursor
        self.theme_manager = theme_manager or get_theme_manager()

        # Variables para el reporte
        self.current_pdf_buffer = None
        self.current_report_data = None

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

            # Guardar el estado actual
            current_module = ''
            current_date_type = ''
            current_start_date = ''
            current_end_date = ''
            preview_content = ''
            save_button_state = 'disabled'

            if hasattr(self, 'module_dropdown') and self.module_dropdown.winfo_exists():
                current_module = self.module_dropdown.get()

            if hasattr(self, 'date_type_dropdown') and self.date_type_dropdown.winfo_exists():
                current_date_type = self.date_type_dropdown.get()

            if hasattr(self, 'start_date_entry') and self.start_date_entry.winfo_exists():
                current_start_date = self.start_date_entry.get()

            if hasattr(self, 'end_date_entry') and self.end_date_entry.winfo_exists():
                current_end_date = self.end_date_entry.get()

            if hasattr(self, 'preview_text') and self.preview_text.winfo_exists():
                preview_content = self.preview_text.get('1.0', 'end-1c')

            if hasattr(self, 'save_button') and self.save_button.winfo_exists():
                save_button_state = str(self.save_button.cget('state'))

            # Recrear el contenido
            self._create_main_content()

            # Restaurar el estado
            if current_module and hasattr(self, 'module_dropdown'):
                self.module_dropdown.set(current_module)

            if current_date_type and hasattr(self, 'date_type_dropdown'):
                self.date_type_dropdown.set(current_date_type)
                self._on_date_type_change(current_date_type)

            if current_start_date and hasattr(self, 'start_date_entry'):
                self.start_date_entry.delete(0, 'end')
                self.start_date_entry.insert(0, current_start_date)

            if current_end_date and hasattr(self, 'end_date_entry'):
                self.end_date_entry.delete(0, 'end')
                self.end_date_entry.insert(0, current_end_date)

            if preview_content and preview_content.strip() and hasattr(self, 'preview_text'):
                self.preview_text.configure(state='normal')
                self.preview_text.delete('1.0', 'end')
                self.preview_text.insert('1.0', preview_content)
                self.preview_text.configure(state='disabled')

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
            text='⏱️ Generación de Reportes por Periodo',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        ).grid(row=0, column=0, sticky='w', columnspan=2)

        ctk.CTkLabel(
            header_frame,
            text='Genera reportes PDF filtrados por módulo y rango de fechas',
            font=('Montserrat', 14),
            text_color=theme['text_secondary']
        ).grid(row=1, column=0, sticky='w', columnspan=2, pady=(5, 0))

        # Sección de selección
        input_section = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
            corner_radius=15
        )
        input_section.grid(row=1, column=0, sticky='ew', pady=(0, 20))

        # Padding interno
        input_content = ctk.CTkFrame(input_section, fg_color='transparent')
        input_content.pack(fill='both', expand=True, padx=30, pady=30)
        input_content.grid_columnconfigure((1, 3), weight=1)

        button_color = '#002E6D'  # Navy blue

        # Fila 1: Módulo y Tipo de fecha
        # Label Módulo
        ctk.CTkLabel(
            input_content,
            text='Módulo:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w', pady=10, padx=(0, 15))

        # Dropdown Módulo
        modules = ['Todos'] + [f'Módulo {i}' for i in range(1, 9)]
        self.module_dropdown = ctk.CTkOptionMenu(
            input_content,
            values=modules,
            font=('Montserrat', 14),
            width=200,
            height=45,
            corner_radius=10
        )
        self.module_dropdown.set('Todos')
        self.module_dropdown.grid(row=0, column=1, sticky='w', pady=10, padx=(0, 30))

        # Label Tipo de Fecha
        ctk.CTkLabel(
            input_content,
            text='Tipo de Búsqueda:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).grid(row=0, column=2, sticky='w', pady=10, padx=(0, 15))

        # Dropdown Tipo de Fecha
        self.date_type_dropdown = ctk.CTkOptionMenu(
            input_content,
            values=['Fecha Única', 'Rango de Fechas'],
            font=('Montserrat', 14),
            width=200,
            height=45,
            corner_radius=10,
            command=self._on_date_type_change
        )
        self.date_type_dropdown.set('Rango de Fechas')
        self.date_type_dropdown.grid(row=0, column=3, sticky='w', pady=10)

        # Fila 2: Fechas
        # Label Fecha Inicio
        self.start_label = ctk.CTkLabel(
            input_content,
            text='Fecha Inicio:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        self.start_label.grid(row=1, column=0, sticky='w', pady=10, padx=(0, 15))

        # Entry Fecha Inicio
        self.start_date_entry = ctk.CTkEntry(
            input_content,
            placeholder_text='DD/MM/YYYY',
            font=('Montserrat', 14),
            height=45,
            width=200,
            corner_radius=10
        )
        # Fecha por defecto: hace 30 días
        default_start = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
        self.start_date_entry.insert(0, default_start)
        self.start_date_entry.grid(row=1, column=1, sticky='w', pady=10, padx=(0, 30))

        # Label Fecha Fin
        self.end_label = ctk.CTkLabel(
            input_content,
            text='Fecha Fin:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        )
        self.end_label.grid(row=1, column=2, sticky='w', pady=10, padx=(0, 15))

        # Entry Fecha Fin
        self.end_date_entry = ctk.CTkEntry(
            input_content,
            placeholder_text='DD/MM/YYYY',
            font=('Montserrat', 14),
            height=45,
            width=200,
            corner_radius=10
        )
        # Fecha por defecto: hoy
        default_end = datetime.now().strftime('%d/%m/%Y')
        self.end_date_entry.insert(0, default_end)
        self.end_date_entry.grid(row=1, column=3, sticky='w', pady=10)

        # Fila 3: Botón generar (centrado)
        button_frame = ctk.CTkFrame(input_content, fg_color='transparent')
        button_frame.grid(row=2, column=0, columnspan=4, pady=(20, 0))

        ctk.CTkButton(
            button_frame,
            text='🔍 Generar Vista Previa',
            font=('Montserrat', 16, 'bold'),
            fg_color=button_color,
            hover_color='#003D8F',
            corner_radius=10,
            height=50,
            width=250,
            command=self._generate_preview
        ).pack()

        # Sección de vista previa
        preview_section = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['surface'],
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
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w')

        # Botón guardar
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

        # Área de vista previa - Más grande y profesional
        self.preview_text = ctk.CTkTextbox(
            preview_section,
            font=('Courier New', 13),
            wrap='none',
            corner_radius=10,
            height=600
        )
        self.preview_text.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        # Mensaje inicial
        self.preview_text.insert('1.0', 'Seleccione un Módulo y Fecha(s), luego haga clic en "Generar Vista Previa" para ver el reporte.')
        self.preview_text.configure(state='disabled')

    def _on_date_type_change(self, choice):
        """Cambiar labels según el tipo de búsqueda"""
        if choice == 'Fecha Única':
            self.start_label.configure(text='Fecha:')
            self.end_label.grid_remove()
            self.end_date_entry.grid_remove()
        else:
            self.start_label.configure(text='Fecha Inicio:')
            self.end_label.grid()
            self.end_date_entry.grid()

    def _generate_sample_data(self, module_filter, start_date, end_date):
        """Generar 20 usuarios con UserIDs reales de BD y fechas/módulos variables"""
        # Nombres de ejemplo
        nombres = [
            'Juan Carlos Pérez', 'María González', 'Roberto Martínez', 'Ana López',
            'Carlos Rodríguez', 'Laura Fernández', 'José Sánchez', 'Patricia Torres',
            'Miguel Ramírez', 'Carmen Flores', 'Francisco Díaz', 'Isabel Morales',
            'Antonio Castro', 'Rosa Jiménez', 'Manuel Ruiz', 'Teresa Álvarez',
            'Pedro Gómez', 'Lucía Romero', 'Diego Vargas', 'Sofía Ortiz'
        ]

        # Obtener UserIDs reales de la BD
        user_ids = []
        if self.cursor:
            try:
                # Intentar obtener 20 UserIDs aleatorios de la BD
                self.cursor.execute("""
                    SELECT TOP 20 UserId
                    FROM Instituto_Usuario
                    ORDER BY NEWID()
                """)
                results = self.cursor.fetchall()
                user_ids = [row[0] for row in results]
            except Exception as e:
                print(f"Error obteniendo UserIDs: {e}")
                # Fallback a IDs de ejemplo
                user_ids = [f'USR{1001+i}' for i in range(20)]
        else:
            # Si no hay cursor, usar IDs de ejemplo
            user_ids = [f'USR{1001+i}' for i in range(20)]

        # Asegurar que tenemos 20 IDs
        while len(user_ids) < 20:
            user_ids.append(f'USR{1001+len(user_ids)}')

        # Generar datos
        data = []

        # Determinar módulos a incluir
        if module_filter == 'Todos':
            modules_range = list(range(1, 9))
        else:
            module_num = int(module_filter.split()[1])
            modules_range = [module_num]

        # Calcular días entre fechas
        delta_days = (end_date - start_date).days + 1

        for i in range(20):
            # Seleccionar módulo aleatorio del rango
            modulo = random.choice(modules_range)

            # Generar fecha aleatoria dentro del rango
            random_days = random.randint(0, max(0, delta_days - 1))
            fecha = start_date + timedelta(days=random_days)

            data.append({
                'usuario': nombres[i],
                'id': user_ids[i],
                'modulo': modulo,
                'fecha': fecha
            })

        # Ordenar por fecha
        data.sort(key=lambda x: x['fecha'])

        return data

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

        module = self.module_dropdown.get()
        date_type = self.date_type_dropdown.get()
        start_date_str = self.start_date_entry.get().strip()

        if not start_date_str:
            messagebox.showwarning("Advertencia", "Ingrese una fecha")
            return

        try:
            # Parsear fechas
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')

            if date_type == 'Rango de Fechas':
                end_date_str = self.end_date_entry.get().strip()
                if not end_date_str:
                    messagebox.showwarning("Advertencia", "Ingrese la fecha fin")
                    return
                end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

                if end_date < start_date:
                    messagebox.showerror("Error", "La fecha fin debe ser posterior a la fecha inicio")
                    return
            else:
                end_date = start_date

            # Generar datos de ejemplo
            sample_data = self._generate_sample_data(module, start_date, end_date)

            # Guardar datos actuales
            self.current_report_data = {
                'module': module,
                'date_type': date_type,
                'start_date': start_date,
                'end_date': end_date,
                'data': sample_data
            }

            # Generar PDF
            self._generate_pdf_report(module, date_type, start_date, end_date, sample_data)

            # Mostrar vista previa
            self._show_preview_text(module, date_type, start_date, end_date, sample_data)

            # Habilitar botón de guardar
            self.save_button.configure(state='normal')

            messagebox.showinfo(
                "Vista Previa Generada",
                f"Reporte generado:\n\n"
                f"Módulo(s): {module}\n"
                f"Periodo: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}\n"
                f"Registros: {len(sample_data)} usuarios\n\n"
                f"Puede guardar el PDF usando el botón 'Guardar PDF'"
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Formato de fecha inválido.\n\nUse el formato: DD/MM/YYYY\nEjemplo: 01/01/2024")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n\n{str(e)}")

    def _generate_pdf_report(self, module, date_type, start_date, end_date, data):
        """Generar el PDF del reporte"""
        # Crear buffer en memoria
        buffer = io.BytesIO()

        # Usar orientación horizontal para tabla más ancha
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
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
        elements.append(Paragraph("Reporte de Progreso por Periodo", title_style))
        elements.append(Paragraph("Instituto Hutchison Ports", title_style))
        elements.append(Spacer(1, 0.2*inch))

        # Información del periodo
        elements.append(Paragraph("Información del Periodo", section_style))
        period_info = [
            ['Módulo(s):', module],
            ['Tipo de Búsqueda:', date_type],
            ['Fecha Inicio:', start_date.strftime('%d/%m/%Y')],
            ['Fecha Fin:', end_date.strftime('%d/%m/%Y')],
            ['Total de Registros:', f'{len(data)} usuarios'],
            ['Fecha de Reporte:', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]

        period_table = Table(period_info, colWidths=[2*inch, 4*inch])
        period_table.setStyle(TableStyle([
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

        elements.append(period_table)
        elements.append(Spacer(1, 0.3*inch))

        # Tabla de usuarios
        elements.append(Paragraph("Detalle de Usuarios", section_style))

        # Encabezado de tabla
        table_data = [['#', 'Usuario', 'User ID', 'Módulo', 'Fecha de Finalización']]

        # Agregar datos
        for idx, record in enumerate(data, 1):
            table_data.append([
                str(idx),
                record['usuario'],
                record['id'],
                f"Módulo {record['modulo']}",
                record['fecha'].strftime('%d/%m/%Y')
            ])

        # Crear tabla
        users_table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1.2*inch, 1.3*inch, 1.5*inch])
        users_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E6D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # # columna
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # ID columna
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Módulo columna
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # Fecha columna
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Usuario columna
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#002E6D')),
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            # Colores alternados
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))

        elements.append(users_table)

        # Pie de página
        elements.append(Spacer(1, 0.3*inch))
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

    def _show_preview_text(self, module, date_type, start_date, end_date, data):
        """Mostrar vista previa en formato profesional"""
        self.preview_text.configure(state='normal')
        self.preview_text.delete('1.0', 'end')

        # Construir tabla de usuarios con formato mejorado
        table_rows = []
        for idx, record in enumerate(data, 1):
            table_rows.append(
                f"  │ {idx:>3} │ {record['usuario']:<30} │ {record['id']:<12} │   Módulo {record['modulo']}   │ {record['fecha'].strftime('%d/%m/%Y')} │"
            )

        periodo_str = f"{start_date.strftime('%d/%m/%Y')}"
        if date_type == 'Rango de Fechas':
            periodo_str += f" - {end_date.strftime('%d/%m/%Y')}"

        preview = f"""
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                             REPORTE DE PROGRESO POR PERIODO
                                                 Instituto Hutchison Ports
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ INFORMACIÓN DEL PERIODO                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    Módulo(s):               {module}
    Tipo de Búsqueda:        {date_type}
    Periodo:                 {periodo_str}
    Total de Registros:      {len(data)} usuarios
    Fecha de Reporte:        {datetime.now().strftime('%d de %B de %Y - %H:%M hrs')}


┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DETALLE DE USUARIOS                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────┬────────────────────────────────┬──────────────┬─────────────────┬──────────────┐
  │  #  │           Usuario              │   User ID    │     Módulo      │    Fecha     │
  ├─────┼────────────────────────────────┼──────────────┼─────────────────┼──────────────┤
{chr(10).join(table_rows)}
  └─────┴────────────────────────────────┴──────────────┴─────────────────┴──────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ RESUMEN                                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    📊 Total de Registros en el Periodo:    {len(data)} usuarios
    📅 Rango de Fechas Analizado:           {periodo_str}
    📚 Módulo(s) Incluido(s):               {module}


═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                    Generado automáticamente por Smart Reports v2.0
                                           {datetime.now().strftime('%d/%m/%Y a las %H:%M hrs')}
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""

        self.preview_text.insert('1.0', preview)
        self.preview_text.configure(state='disabled')

    def _save_pdf(self):
        """Guardar PDF en PC"""
        if not self.current_pdf_buffer or not self.current_report_data:
            messagebox.showerror("Error", "No hay reporte generado para guardar")
            return

        try:
            # Sugerir nombre de archivo
            module_name = self.current_report_data['module'].replace(' ', '_')
            start_str = self.current_report_data['start_date'].strftime('%Y%m%d')
            end_str = self.current_report_data['end_date'].strftime('%Y%m%d')
            default_filename = f"Reporte_Periodo_{module_name}_{start_str}-{end_str}.pdf"

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
