"""
Panel de Generación de Reportes por Niveles de Mando
Permite generar reportes PDF por niveles gerenciales con vista previa
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import io
import os
from datetime import datetime

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

from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.ui.components.charts.previsualizador_reporte import PrevisualizadorReporte


class ManagementLevelsPanel(ctk.CTkFrame):
    """Panel para generar reportes PDF por niveles de mando con vista previa"""

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
            save_button_state = 'disabled'

            if hasattr(self, 'module_dropdown') and self.module_dropdown.winfo_exists():
                current_module = self.module_dropdown.get()

            # Preview widget ya no necesita guardar contenido (se regenera)

            if hasattr(self, 'save_button') and self.save_button.winfo_exists():
                save_button_state = str(self.save_button.cget('state'))

            # Recrear el contenido
            self._create_main_content()

            # Restaurar el estado
            if current_module and hasattr(self, 'module_dropdown'):
                self.module_dropdown.set(current_module)

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
            text='👔 Generación de Reportes por Niveles de Mando',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        ).grid(row=0, column=0, sticky='w', columnspan=2)

        ctk.CTkLabel(
            header_frame,
            text='Genera reportes PDF organizados por mandos gerenciales, medios y administrativos',
            font=('Montserrat', 14),
            text_color=theme['colors']['text_secondary']
        ).grid(row=1, column=0, sticky='w', columnspan=2, pady=(5, 0))

        # Sección de selección
        input_section = ctk.CTkFrame(
            scroll_frame,
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=15
        )
        input_section.grid(row=1, column=0, sticky='ew', pady=(0, 20))

        # Padding interno
        input_content = ctk.CTkFrame(input_section, fg_color='transparent')
        input_content.pack(fill='both', expand=True, padx=30, pady=30)
        input_content.grid_columnconfigure(1, weight=1)

        button_color = '#002E6D'  # Navy blue

        # Label Módulo
        ctk.CTkLabel(
            input_content,
            text='Módulo:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['colors']['text']
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

        # Botón generar
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
        ).grid(row=0, column=2, sticky='e', pady=10)

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

        # Área de vista previa - HTML profesional estilo Word
        self.preview_widget = PrevisualizadorReporte(preview_section)
        self.preview_widget.pack(fill='both', expand=True, padx=30, pady=(0, 30))

    def _get_total_users(self):
        """Obtener total de usuarios de la BD"""
        if not self.cursor:
            return 1525  # Valor por defecto

        try:
            self.cursor.execute("SELECT COUNT(*) FROM instituto_Usuario")
            result = self.cursor.fetchone()
            return result[0] if result else 1525
        except Exception as e:
            print(f"Error obteniendo total de usuarios: {e}")
            return 1525

    def _generate_management_levels_data(self, module_filter):
        """Generar datos por niveles de mando con población y estados"""
        total_population = self._get_total_users()

        # Determinar módulos a incluir
        if module_filter == 'Todos':
            modules_list = list(range(1, 9))
        else:
            module_num = int(module_filter.split()[1])
            modules_list = [module_num]

        # Niveles de mando
        management_levels = [
            'Mandos Gerenciales',
            'Mandos Medios',
            'Mandos Administrativos Operativos'
        ]

        # Generar datos por nivel de mando
        data = []

        # Distribución de población por nivel (valores de ejemplo)
        # 15% gerenciales, 30% medios, 55% administrativos operativos
        poblacion_gerencial = int(total_population * 0.15)
        poblacion_medios = int(total_population * 0.30)
        poblacion_operativos = total_population - poblacion_gerencial - poblacion_medios

        poblaciones = [poblacion_gerencial, poblacion_medios, poblacion_operativos]

        for idx, nivel in enumerate(management_levels):
            poblacion = poblaciones[idx]

            # Distribución de estados por nivel (valores de ejemplo)
            # Gerencial: 70% completado, 20% en proceso, 10% registrado
            # Medios: 60% completado, 25% en proceso, 15% registrado
            # Operativos: 50% completado, 30% en proceso, 20% registrado
            if idx == 0:  # Gerencial
                completado = int(poblacion * 0.70)
                en_proceso = int(poblacion * 0.20)
                registrado = poblacion - completado - en_proceso
            elif idx == 1:  # Medios
                completado = int(poblacion * 0.60)
                en_proceso = int(poblacion * 0.25)
                registrado = poblacion - completado - en_proceso
            else:  # Operativos
                completado = int(poblacion * 0.50)
                en_proceso = int(poblacion * 0.30)
                registrado = poblacion - completado - en_proceso

            data.append({
                'nivel': nivel,
                'poblacion': poblacion,
                'completado': completado,
                'registrado': registrado,
                'en_proceso': en_proceso
            })

        return data, total_population, modules_list

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

        try:
            # Generar datos por niveles de mando
            data, total_population, modules_list = self._generate_management_levels_data(module)

            # Guardar datos actuales
            self.current_report_data = {
                'module': module,
                'data': data,
                'total_population': total_population,
                'modules_list': modules_list
            }

            # Generar PDF
            self._generate_pdf_report(module, data, total_population, modules_list)

            # Mostrar vista previa
            self._show_preview_text(module, data, total_population, modules_list)

            # Habilitar botón de guardar
            self.save_button.configure(state='normal')

            messagebox.showinfo(
                "Vista Previa Generada",
                f"Reporte por niveles de mando generado:\n\n"
                f"Módulo(s): {module}\n"
                f"Población Total: {total_population} usuarios\n"
                f"Niveles de Mando: 3\n\n"
                f"Puede guardar el PDF usando el botón 'Guardar PDF'"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n\n{str(e)}")

    def _generate_pdf_report(self, module, data, total_population, modules_list):
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
        elements.append(Paragraph("Reporte por Niveles de Mando", title_style))
        elements.append(Paragraph("Instituto Hutchison Ports", title_style))
        elements.append(Spacer(1, 0.2*inch))

        # Información general
        elements.append(Paragraph("Información General", section_style))
        general_info = [
            ['Módulo(s):', module],
            ['Población Total:', f'{total_population} usuarios'],
            ['Niveles de Mando:', '3 niveles'],
            ['Fecha de Reporte:', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]

        general_table = Table(general_info, colWidths=[2*inch, 4.5*inch])
        general_table.setStyle(TableStyle([
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

        elements.append(general_table)
        elements.append(Spacer(1, 0.3*inch))

        # Tabla de estadísticas por nivel de mando
        elements.append(Paragraph("Estadísticas por Nivel de Mando", section_style))

        # Encabezado de tabla
        table_data = [
            ['Nivel de Mando', 'Población', 'Completado', 'Registrado', 'En Proceso']
        ]

        # Agregar datos
        for record in data:
            table_data.append([
                record['nivel'],
                str(record['poblacion']),
                f"{record['completado']}\n({(record['completado']/record['poblacion']*100):.1f}%)",
                f"{record['registrado']}\n({(record['registrado']/record['poblacion']*100):.1f}%)",
                f"{record['en_proceso']}\n({(record['en_proceso']/record['poblacion']*100):.1f}%)"
            ])

        # Crear tabla
        stats_table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        stats_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E6D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
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

        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))

        # Resumen general
        elements.append(Paragraph("Resumen General", section_style))

        total_completado = sum(r['completado'] for r in data)
        total_registrado = sum(r['registrado'] for r in data)
        total_en_proceso = sum(r['en_proceso'] for r in data)

        summary_data = [
            ['Total de Usuarios:', f'{total_population:,}'],
            ['Total Completado:', f"{total_completado:,} ({(total_completado/total_population*100):.1f}%)"],
            ['Total Registrado:', f"{total_registrado:,} ({(total_registrado/total_population*100):.1f}%)"],
            ['Total En Proceso:', f"{total_en_proceso:,} ({(total_en_proceso/total_population*100):.1f}%)"],
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

    def _show_preview_text(self, module, data, total_population, modules_list):
        """Mostrar vista previa en HTML profesional"""
        # Preparar datos de niveles de mando
        datos_niveles = {
            'module': module,
            'total_population': total_population,
            'num_niveles': len(data)
        }

        # Preparar estadísticas por nivel de mando
        estadisticas = []
        for record in data:
            estadisticas.append({
                'nivel': record['nivel'],
                'poblacion': record['poblacion'],
                'completado': record['completado'],
                'registrado': record['registrado'],
                'en_proceso': record['en_proceso']
            })

        # Mostrar en widget HTML
        self.preview_widget.mostrar_reporte_niveles_mando(datos_niveles, estadisticas)

    def _save_pdf(self):
        """Guardar PDF en PC"""
        if not self.current_pdf_buffer or not self.current_report_data:
            messagebox.showerror("Error", "No hay reporte generado para guardar")
            return

        try:
            # Sugerir nombre de archivo
            module_name = self.current_report_data['module'].replace(' ', '_')
            default_filename = f"Reporte_Niveles_Mando_{module_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

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
