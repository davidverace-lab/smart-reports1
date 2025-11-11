"""
Panel de Generación de Reportes por Unidad de Negocio
Permite generar reportes PDF detallados por unidad con vista previa
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
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab no está instalado. Instala con: pip install reportlab")

from config.gestor_temas import get_theme_manager
from src.interfaces.ui.views.components.charts.previsualizador_reporte import PrevisualizadorReporte


class UnitReportPanel(ctk.CTkFrame):
    """Panel para generar reportes PDF por unidad de negocio con vista previa"""

    def __init__(self, parent, db=None, cursor=None, theme_manager=None):
        super().__init__(parent, fg_color='transparent')

        self.db = db
        self.cursor = cursor
        self.theme_manager = theme_manager or get_theme_manager()

        # Variables para el reporte
        self.current_pdf_buffer = None
        self.current_unit_data = None
        self.current_module = None

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
            current_unit = ''
            current_module = ''
            save_button_state = 'disabled'

            if hasattr(self, 'unit_dropdown') and self.unit_dropdown.winfo_exists():
                current_unit = self.unit_dropdown.get()

            if hasattr(self, 'module_dropdown') and self.module_dropdown.winfo_exists():
                current_module = self.module_dropdown.get()

            # Preview widget ya no necesita guardar contenido (se regenera)

            if hasattr(self, 'save_button') and self.save_button.winfo_exists():
                save_button_state = str(self.save_button.cget('state'))

            # Recrear el contenido
            self._create_main_content()

            # Restaurar el estado
            if current_unit and hasattr(self, 'unit_dropdown'):
                self.unit_dropdown.set(current_unit)

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
            text='🏢 Generación de Reportes por Unidad de Negocio',
            font=('Montserrat', 28, 'bold'),
            text_color=title_color
        ).grid(row=0, column=0, sticky='w', columnspan=2)

        ctk.CTkLabel(
            header_frame,
            text='Genera reportes PDF detallados del progreso por unidad de negocio',
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
        input_section.grid_columnconfigure((1, 2), weight=1)

        # Padding interno
        input_content = ctk.CTkFrame(input_section, fg_color='transparent')
        input_content.pack(fill='both', expand=True, padx=30, pady=30)
        input_content.grid_columnconfigure((1, 3), weight=1)

        # Label Unidad de Negocio
        ctk.CTkLabel(
            input_content,
            text='Unidad de Negocio:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).grid(row=0, column=0, sticky='w', pady=10, padx=(0, 15))

        # Dropdown Unidad de Negocio
        units = self._get_units_from_db()
        self.unit_dropdown = ctk.CTkOptionMenu(
            input_content,
            values=units if units else ['TNG', 'ICAVE', 'ECV', 'Container Care', 'HPMX'],
            font=('Montserrat', 14),
            width=250,
            height=45,
            corner_radius=10
        )
        self.unit_dropdown.grid(row=0, column=1, sticky='ew', pady=10, padx=(0, 20))

        # Label Módulo
        ctk.CTkLabel(
            input_content,
            text='Módulo:',
            font=('Montserrat', 16, 'bold'),
            text_color=theme['text']
        ).grid(row=0, column=2, sticky='w', pady=10, padx=(0, 15))

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
        self.module_dropdown.grid(row=0, column=3, sticky='ew', pady=10, padx=(0, 20))

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
        ).grid(row=0, column=4, sticky='e', pady=10, padx=(20, 0))

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

        # Botón guardar (inicialmente deshabilitado)
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

    def _get_units_from_db(self):
        """Obtener unidades de negocio desde la base de datos"""
        if not self.cursor:
            return None

        try:
            # Intentar obtener las unidades de la BD
            self.cursor.execute("""
                SELECT DISTINCT NombreUnidad
                FROM instituto_UnidadDeNegocio
                ORDER BY NombreUnidad
            """)
            results = self.cursor.fetchall()
            if results:
                return [row[0] for row in results]
        except Exception as e:
            print(f"Error obteniendo unidades: {e}")

        return None

    def _get_unit_population(self, unit_name):
        """Obtener población asignada de una unidad desde BD"""
        if not self.cursor:
            return 150  # Valor por defecto

        try:
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM instituto_Usuario u
                JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE un.NombreUnidad = %s
            """, (unit_name,))
            result = self.cursor.fetchone()
            return result[0] if result else 150
        except Exception as e:
            print(f"Error obteniendo población: {e}")
            return 150

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

        unit = self.unit_dropdown.get()
        module = self.module_dropdown.get()

        if not unit:
            messagebox.showwarning("Advertencia", "Seleccione una Unidad de Negocio")
            return

        try:
            # Obtener población real de la unidad
            population = self._get_unit_population(unit)

            # Guardar datos actuales
            self.current_unit_data = {
                'name': unit,
                'population': population
            }
            self.current_module = module

            # Generar PDF
            self._generate_pdf_report(unit, module, population)

            # Mostrar vista previa en texto
            self._show_preview_text(unit, module, population)

            # Habilitar botón de guardar
            self.save_button.configure(state='normal')

            messagebox.showinfo(
                "Vista Previa Generada",
                f"Reporte generado para:\n\n"
                f"Unidad: {unit}\n"
                f"Módulo(s): {module}\n"
                f"Población: {population} usuarios\n\n"
                f"Puede guardar el PDF usando el botón 'Guardar PDF'"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n\n{str(e)}")

    def _generate_pdf_report(self, unit, module, population):
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
        elements.append(Paragraph(f"Reporte de Progreso - {unit}", title_style))
        elements.append(Paragraph("Instituto Hutchison Ports", title_style))
        elements.append(Spacer(1, 0.2*inch))

        # Información general
        elements.append(Paragraph("Información General", section_style))
        general_info = [
            ['Unidad de Negocio:', unit],
            ['Módulo(s):', module],
            ['Población Total:', f'{population} usuarios'],
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

        # Tabla de progreso por módulo
        elements.append(Paragraph("Progreso por Módulo", section_style))

        # Generar datos de tabla según selección
        if module == 'Todos':
            modules_list = list(range(1, 9))
        else:
            module_num = int(module.split()[1])
            modules_list = [module_num]

        # Datos de la tabla (estáticos por ahora)
        table_data = [
            ['Módulo', 'Población\nAsignada', 'Sin Iniciar', 'En Proceso', 'Completado']
        ]

        for mod_num in modules_list:
            # Valores estáticos de ejemplo (distribuidos de la población)
            sin_iniciar = int(population * 0.15)
            en_proceso = int(population * 0.25)
            completado = population - sin_iniciar - en_proceso

            table_data.append([
                f'Módulo {mod_num}',
                str(population),
                f'{sin_iniciar}\n({(sin_iniciar/population*100):.1f}%)',
                f'{en_proceso}\n({(en_proceso/population*100):.1f}%)',
                f'{completado}\n({(completado/population*100):.1f}%)'
            ])

        progress_table = Table(table_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        progress_table.setStyle(TableStyle([
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
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            # Colores alternados
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))

        elements.append(progress_table)
        elements.append(Spacer(1, 0.3*inch))

        # Resumen
        elements.append(Paragraph("Resumen General", section_style))

        # Calcular totales
        total_sin_iniciar = len(modules_list) * int(population * 0.15)
        total_en_proceso = len(modules_list) * int(population * 0.25)
        total_completado = len(modules_list) * population - total_sin_iniciar - total_en_proceso
        total_registros = len(modules_list) * population

        summary_data = [
            ['Total de Registros:', f'{total_registros}'],
            ['Sin Iniciar:', f'{total_sin_iniciar} ({(total_sin_iniciar/total_registros*100):.1f}%)'],
            ['En Proceso:', f'{total_en_proceso} ({(total_en_proceso/total_registros*100):.1f}%)'],
            ['Completado:', f'{total_completado} ({(total_completado/total_registros*100):.1f}%)'],
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

    def _show_preview_text(self, unit, module, population):
        """Mostrar vista previa en HTML profesional"""
        # Preparar datos de la unidad
        datos_unidad = {
            'unit': unit,
            'module': module,
            'population': population
        }

        # Generar datos de tabla según selección
        if module == 'Todos':
            modules_list = list(range(1, 9))
        else:
            module_num = int(module.split()[1])
            modules_list = [module_num]

        # Preparar estadísticas por módulo
        estadisticas = []
        for mod_num in modules_list:
            sin_iniciar = int(population * 0.15)
            en_proceso = int(population * 0.25)
            completado = population - sin_iniciar - en_proceso

            estadisticas.append({
                'modulo': f'Módulo {mod_num}',
                'poblacion_asignada': population,
                'sin_iniciar': sin_iniciar,
                'en_proceso': en_proceso,
                'completado': completado
            })

        # Mostrar en widget HTML
        self.preview_widget.mostrar_reporte_unidad(datos_unidad, estadisticas)

    def _save_pdf(self):
        """Guardar PDF en PC"""
        if not self.current_pdf_buffer or not self.current_unit_data:
            messagebox.showerror("Error", "No hay reporte generado para guardar")
            return

        try:
            # Sugerir nombre de archivo
            unit_name = self.current_unit_data['name'].replace(' ', '_')
            module_name = self.current_module.replace(' ', '_')
            default_filename = f"Reporte_{unit_name}_{module_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

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
