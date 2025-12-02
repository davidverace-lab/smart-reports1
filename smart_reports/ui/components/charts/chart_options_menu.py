"""
Menú de Opciones para Gráficas - SMART REPORTS
Componente reutilizable con funcionalidades avanzadas

Opciones incluidas:
✅ Actualizar datos (refresh con timestamp)
✅ Ver datos en tabla (modal)
✅ Exportar a CSV
✅ Exportar gráfica como PNG
✅ Exportar tabla como PDF
✅ Copiar datos al portapapeles
✅ Ver estadísticas
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv
from datetime import datetime
import os
from io import BytesIO
from smart_reports.config.gestor_temas import get_theme_manager
from smart_reports.config.themes import HUTCHISON_COLORS


class ChartOptionsMenu(ctk.CTkFrame):
    """
    Menú desplegable de opciones para gráficas

    Usage:
        menu = ChartOptionsMenu(
            parent=card,
            chart_title="Ventas por Región",
            chart_data={'labels': [...], 'values': [...]},
            chart_type='bar',
            on_option_selected=callback
        )
    """

    def __init__(self, parent, chart_title='', chart_data=None, chart_type='bar',
                 chart_figure=None, html_content=None, on_refresh=None, on_show_table=None, **kwargs):
        self.theme_manager = get_theme_manager()
        theme = self.theme_manager.get_current_theme()

        super().__init__(
            parent,
            fg_color='transparent',
            **kwargs
        )

        self.chart_title = chart_title
        self.chart_data = chart_data or {}
        self.chart_type = chart_type
        self.chart_figure = chart_figure
        self.html_content = html_content
        self.on_refresh = on_refresh  # Callback para actualizar datos
        self.on_show_table = on_show_table  # Callback para mostrar tabla expandible
        self.menu_visible = False
        self.last_update = None  # Timestamp de última actualización

        # Crear botón de 3 puntitos
        self._create_menu_button()

        # Crear menú desplegable (inicialmente oculto)
        self._create_dropdown_menu()

        # Registrar callback para cambios de tema
        self.theme_manager.register_callback(self._on_theme_changed)

    def _create_menu_button(self):
        """Crear botón de 3 puntitos (⋮) - MÁS VISIBLE"""
        theme = self.theme_manager.get_current_theme()

        self.menu_btn = ctk.CTkButton(
            self,
            text="⋮",  # Tres puntos verticales
            width=40,  # Más ancho
            height=32,  # Más alto
            font=('Segoe UI', 20, 'bold'),  # Fuente más grande
            fg_color=HUTCHISON_COLORS['primary'],  # Azul navy para visibilidad
            hover_color='#001a3d',
            text_color='white',  # Texto blanco para contraste
            corner_radius=8,
            border_width=0,  # Sin borde para look más limpio
            command=self._toggle_menu
        )
        self.menu_btn.pack()

    def _create_dropdown_menu(self):
        """Crear menú desplegable con opciones"""
        theme = self.theme_manager.get_current_theme()

        # Frame del menú (flotante)
        self.dropdown = ctk.CTkFrame(
            self.winfo_toplevel(),  # Parent es la ventana principal
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            corner_radius=10,
            border_width=2,
            border_color=HUTCHISON_COLORS['primary']
        )

        # Opciones del menú
        options = [
            ("🔄 Actualizar Datos", self._refresh_data, '#10b981'),
            ("📊 Ver Tabla de Datos", self._show_data_table, HUTCHISON_COLORS['primary']),
            ("📥 Exportar CSV", self._export_csv, '#22c55e'),
            ("🖼️ Exportar PNG", self._export_png, '#3b82f6'),
            ("📄 Exportar Tabla PDF", self._export_table_pdf, '#ef4444'),
            ("📋 Copiar al Portapapeles", self._copy_to_clipboard, '#f59e0b'),
        ]

        for i, (text, command, color) in enumerate(options):
            btn = ctk.CTkButton(
                self.dropdown,
                text=text,
                font=('Montserrat', 12),
                fg_color='transparent',
                hover_color=color,
                text_color=theme['colors']['text'],
                anchor='w',
                height=40,
                command=lambda cmd=command: self._execute_option(cmd)
            )
            btn.pack(fill='x', padx=5, pady=2)

        # Inicialmente oculto
        self.dropdown.place_forget()

    def _toggle_menu(self):
        """Mostrar/ocultar menú"""
        if self.menu_visible:
            self._hide_menu()
        else:
            self._show_menu()

    def _show_menu(self):
        """Mostrar menú desplegable"""
        # Forzar update para obtener coordenadas correctas
        self.menu_btn.update_idletasks()

        # Calcular posición (debajo del botón, alineado a la derecha)
        button_x = self.menu_btn.winfo_rootx()
        button_y = self.menu_btn.winfo_rooty()
        button_width = self.menu_btn.winfo_width()
        button_height = self.menu_btn.winfo_height()

        # Convertir a coordenadas relativas de la ventana
        win_x = self.winfo_toplevel().winfo_rootx()
        win_y = self.winfo_toplevel().winfo_rooty()

        # Posicionar menú DEBAJO del botón, alineado a la DERECHA
        menu_width = 250  # Ancho aproximado del menú
        rel_x = button_x - win_x - menu_width + button_width  # Alineado a la derecha del botón
        rel_y = button_y - win_y + button_height + 5  # 5px debajo del botón

        self.dropdown.place(x=rel_x, y=rel_y)
        self.dropdown.lift()
        self.menu_visible = True

        # Bind para cerrar al hacer clic fuera
        self.winfo_toplevel().bind('<Button-1>', self._check_click_outside)

    def _hide_menu(self):
        """Ocultar menú"""
        self.dropdown.place_forget()
        self.menu_visible = False
        self.winfo_toplevel().unbind('<Button-1>')

    def _check_click_outside(self, event):
        """Verificar si click fue fuera del menú"""
        widget = event.widget

        # Verificar si el click fue en el dropdown o menu_btn
        if widget not in [self.dropdown, self.menu_btn] and not self._is_child(widget, self.dropdown):
            self._hide_menu()

    def _is_child(self, widget, parent):
        """Verificar si widget es hijo de parent"""
        while widget:
            if widget == parent:
                return True
            widget = widget.master
        return False

    def _execute_option(self, command):
        """Ejecutar opción y cerrar menú"""
        self._hide_menu()
        command()

    # ========== OPCIONES DEL MENÚ ==========

    def _show_data_table(self):
        """Mostrar datos en tabla expandible IN-PLACE"""
        print(f"📊 Mostrando tabla de datos: {self.chart_title}")

        # Llamar al callback para mostrar tabla expandible
        if self.on_show_table:
            self.on_show_table()
        else:
            messagebox.showinfo(
                "Función no disponible",
                "La visualización de tabla no está disponible para este gráfico"
            )

    def _export_csv(self):
        """Exportar datos a CSV"""
        if not self.chart_data or 'labels' not in self.chart_data:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return

        try:
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = self.chart_title.replace(" ", "_").replace("/", "-")[:30]
            filename = f"datos_{title_clean}_{timestamp}.csv"

            # Diálogo de guardado
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                initialfile=filename,
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Exportar datos a CSV"
            )

            if not filepath:
                return

            # Escribir CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Header
                if self.chart_type in ['bar', 'donut', 'pie']:
                    writer.writerow(['Categoría', 'Valor'])
                    for label, value in zip(self.chart_data['labels'], self.chart_data['values']):
                        writer.writerow([label, value])
                elif self.chart_type in ['line', 'area']:
                    writer.writerow(['X', 'Y'])
                    for x, y in zip(self.chart_data.get('x', self.chart_data['labels']),
                                   self.chart_data.get('y', self.chart_data['values'])):
                        writer.writerow([x, y])

            messagebox.showinfo("Éxito", f"Datos exportados a:\n{filepath}")
            print(f"✅ CSV exportado: {filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV:\n{str(e)}")
            print(f"❌ Error exportando CSV: {e}")

    def _export_png(self):
        """Exportar gráfica como PNG"""
        if self.html_content:
            messagebox.showinfo(
                "Exportar PNG",
                "Para exportar gráficos D3/NVD3 como PNG:\n\n"
                "1. Haz clic en el botón 🌐 para abrir en navegador\n"
                "2. Usa la herramienta de captura de pantalla\n"
                "3. O usa extensiones del navegador para exportar\n\n"
                "Próximamente: Exportación automática de D3 a PNG"
            )
        elif self.chart_figure:
            # Exportar figura matplotlib
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                title_clean = self.chart_title.replace(" ", "_").replace("/", "-")[:30]
                filename = f"grafico_{title_clean}_{timestamp}.png"

                filepath = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    initialfile=filename,
                    filetypes=[
                        ("PNG Image", "*.png"),
                        ("PDF Document", "*.pdf"),
                        ("SVG Vector", "*.svg")
                    ],
                    title="Exportar Gráfico"
                )

                if filepath:
                    self.chart_figure.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
                    messagebox.showinfo("Éxito", f"Gráfico exportado a:\n{filepath}")
                    print(f"✅ PNG exportado: {filepath}")

            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar PNG:\n{str(e)}")
                print(f"❌ Error exportando PNG: {e}")
        else:
            messagebox.showwarning("Sin gráfico", "No hay gráfico para exportar")

    def _export_table_pdf(self):
        """Exportar tabla de datos como PDF"""
        if not self.chart_data or 'labels' not in self.chart_data:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER

            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_clean = self.chart_title.replace(" ", "_").replace("/", "-")[:30]
            filename = f"tabla_{title_clean}_{timestamp}.pdf"

            # Diálogo de guardado
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=filename,
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Exportar tabla a PDF"
            )

            if not filepath:
                return

            # Crear PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()

            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#002E6D'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            title = Paragraph(f"<b>{self.chart_title}</b>", title_style)
            story.append(title)
            story.append(Spacer(1, 0.2*inch))

            # Fecha
            date_text = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            date_para = Paragraph(date_text, styles['Normal'])
            story.append(date_para)
            story.append(Spacer(1, 0.3*inch))

            # Preparar datos de tabla
            if self.chart_type in ['bar', 'donut', 'pie']:
                table_data = [['Categoría', 'Valor']]
                for label, value in zip(self.chart_data['labels'], self.chart_data['values']):
                    table_data.append([str(label), str(value)])
            else:
                table_data = [['X', 'Y']]
                for x, y in zip(self.chart_data.get('x', self.chart_data['labels']),
                               self.chart_data.get('y', self.chart_data['values'])):
                    table_data.append([str(x), str(y)])

            # Crear tabla
            t = Table(table_data)

            # Estilo de tabla (tema Hutchison)
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002E6D')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#002E6D')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#E8F4F8')]),
            ])

            t.setStyle(table_style)
            story.append(t)

            # Footer
            story.append(Spacer(1, 0.5*inch))
            footer = Paragraph(
                "<i>Instituto Hutchison Ports - SMART REPORTS</i>",
                styles['Normal']
            )
            story.append(footer)

            # Generar PDF
            doc.build(story)

            messagebox.showinfo("Éxito", f"Tabla exportada a PDF:\n{filepath}")
            print(f"✅ PDF exportado: {filepath}")

        except ImportError:
            messagebox.showerror(
                "Error",
                "ReportLab no está instalado.\n\n"
                "Instala con: pip install reportlab"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF:\n{str(e)}")
            print(f"❌ Error exportando PDF: {e}")
            import traceback
            traceback.print_exc()

    def _copy_to_clipboard(self):
        """Copiar datos al portapapeles"""
        if not self.chart_data or 'labels' not in self.chart_data:
            messagebox.showwarning("Sin datos", "No hay datos para copiar")
            return

        try:
            # Formatear datos como texto tabulado
            lines = []

            if self.chart_type in ['bar', 'donut', 'pie']:
                lines.append("Categoría\tValor")
                for label, value in zip(self.chart_data['labels'], self.chart_data['values']):
                    lines.append(f"{label}\t{value}")
            else:
                lines.append("X\tY")
                for x, y in zip(self.chart_data.get('x', self.chart_data['labels']),
                               self.chart_data.get('y', self.chart_data['values'])):
                    lines.append(f"{x}\t{y}")

            text = "\n".join(lines)

            # Copiar al portapapeles
            self.winfo_toplevel().clipboard_clear()
            self.winfo_toplevel().clipboard_append(text)

            messagebox.showinfo("Copiado", "Datos copiados al portapapeles")
            print("✅ Datos copiados al portapapeles")

        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar:\n{str(e)}")
            print(f"❌ Error copiando: {e}")

    def _show_statistics(self):
        """Mostrar estadísticas de los datos"""
        if not self.chart_data or 'values' not in self.chart_data:
            messagebox.showwarning("Sin datos", "No hay datos para analizar")
            return

        try:
            values = self.chart_data['values']

            # Calcular estadísticas
            total = sum(values)
            count = len(values)
            promedio = total / count if count > 0 else 0
            minimo = min(values) if values else 0
            maximo = max(values) if values else 0

            # Mediana
            sorted_values = sorted(values)
            if count % 2 == 0:
                mediana = (sorted_values[count//2 - 1] + sorted_values[count//2]) / 2
            else:
                mediana = sorted_values[count//2]

            stats_text = (
                f"Estadísticas: {self.chart_title}\n\n"
                f"Total: {total:,.2f}\n"
                f"Cantidad de elementos: {count}\n"
                f"Promedio: {promedio:,.2f}\n"
                f"Mediana: {mediana:,.2f}\n"
                f"Mínimo: {minimo:,.2f}\n"
                f"Máximo: {maximo:,.2f}\n"
                f"Rango: {maximo - minimo:,.2f}"
            )

            messagebox.showinfo("Estadísticas", stats_text)
            print(f"📈 Estadísticas calculadas: {self.chart_title}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular estadísticas:\n{str(e)}")
            print(f"❌ Error en estadísticas: {e}")

    def _refresh_data(self):
        """Actualizar datos del gráfico"""
        if not self.on_refresh:
            # Si no hay callback, mostrar info de última actualización
            if self.last_update:
                from datetime import datetime
                time_diff = datetime.now() - self.last_update

                if time_diff.seconds < 60:
                    time_str = f"{time_diff.seconds} segundos"
                elif time_diff.seconds < 3600:
                    time_str = f"{time_diff.seconds // 60} minutos"
                else:
                    time_str = f"{time_diff.seconds // 3600} horas"

                last_update_str = self.last_update.strftime("%d/%m/%Y %H:%M:%S")
                messagebox.showinfo(
                    "Actualizar Datos",
                    f"Última actualización:\n{last_update_str}\n\n"
                    f"Hace {time_str}\n\n"
                    "No hay función de actualización configurada."
                )
            else:
                messagebox.showinfo(
                    "Actualizar Datos",
                    "No hay función de actualización configurada.\n\n"
                    "Para habilitar actualización automática, configura\n"
                    "el callback 'on_refresh' en el ChartOptionsMenu."
                )
            return

        try:
            print(f"🔄 Actualizando datos: {self.chart_title}")

            # Llamar al callback de actualización
            self.on_refresh()

            # Actualizar timestamp
            from datetime import datetime
            self.last_update = datetime.now()

            messagebox.showinfo(
                "Datos Actualizados",
                f"Gráfico actualizado exitosamente\n\n"
                f"Hora: {self.last_update.strftime('%H:%M:%S')}"
            )

            print(f"✅ Datos actualizados: {self.chart_title}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar datos:\n{str(e)}")
            print(f"❌ Error actualizando datos: {e}")
            import traceback
            traceback.print_exc()

    def _on_theme_changed(self, theme_mode: str):
        """Actualizar colores del menú cuando cambia el tema"""
        theme = self.theme_manager.get_current_theme()

        # Actualizar botón de menú
        self.menu_btn.configure(
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            text_color=theme['colors']['text'],
            border_color=theme['colors']['border']
        )

        # Actualizar dropdown
        self.dropdown.configure(
            fg_color=theme['colors'].get('card_background', '#2d2d2d'),
            border_color=HUTCHISON_COLORS['primary']
        )

        # Actualizar botones del dropdown
        for widget in self.dropdown.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(text_color=theme['colors']['text'])
