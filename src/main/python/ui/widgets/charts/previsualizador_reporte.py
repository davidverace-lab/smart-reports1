"""
Componente para previsualizar reportes en formato HTML profesional
Estilo documento Word - NO ASCII
"""
import customtkinter as ctk
from tkinter import Frame
import tempfile
import os
from datetime import datetime

try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False


class PrevisualizadorReporte(ctk.CTkFrame):
    """Previsualización de reporte estilo documento Word"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color='white', **kwargs)

        if not TKINTERWEB_AVAILABLE:
            error_label = ctk.CTkLabel(
                self,
                text="⚠️ tkinterweb no disponible\nInstala: pip install tkinterweb",
                font=('Arial', 12),
                text_color='#ff6b6b'
            )
            error_label.pack(expand=True, pady=20)
            return

        # Frame para HTML
        html_container = Frame(self, bg='white')
        html_container.pack(fill='both', expand=True)

        self.html_widget = HtmlFrame(
            html_container,
            messages_enabled=False,
            vertical_scrollbar=True,
            horizontal_scrollbar=False
        )
        self.html_widget.pack(fill='both', expand=True)

    def mostrar_reporte_usuario(self, datos_usuario, progreso_modulos):
        """
        Mostrar reporte de usuario en formato Word

        Args:
            datos_usuario: dict con {user_id, nombre, email}
            progreso_modulos: list de dict con {modulo, completado, fecha, calificacion}
        """
        html = self._generar_html_usuario(datos_usuario, progreso_modulos)

        # Guardar temporal y cargar
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()

        self.html_widget.load_file(temp_file.name)

    def mostrar_reporte_unidad(self, datos_unidad, estadisticas):
        """Mostrar reporte de unidad de negocio"""
        html = self._generar_html_unidad(datos_unidad, estadisticas)

        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()

        self.html_widget.load_file(temp_file.name)

    def mostrar_reporte_global(self, estadisticas_globales):
        """Mostrar reporte global"""
        html = self._generar_html_global(estadisticas_globales)

        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()

        self.html_widget.load_file(temp_file.name)

    def _generar_html_usuario(self, datos, progreso):
        """
        Generar HTML que replica EXACTAMENTE el formato del PDF de ReportLab
        Sin gradientes, sin cards elaborados - igual al PDF
        """
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Calcular estadísticas
        total_modulos = len(progreso)
        completados = sum(1 for m in progreso if m.get('completado', False))
        suma_calif = sum(m.get('calificacion', 0) for m in progreso if m.get('completado', False))
        promedio = (suma_calif / completados) if completados > 0 else 0

        # Generar filas de tabla - igual al PDF
        filas_modulos = ""
        for idx, modulo in enumerate(progreso):
            completado_si_no = "Sí" if modulo.get('completado', False) else "No"
            fecha = modulo.get('fecha', 'Pendiente')
            calificacion = f"{modulo.get('calificacion', 0)}%" if modulo.get('completado', False) else "N/A"
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F5F5F5"  # Filas alternadas como el PDF

            filas_modulos += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px 8px;">{modulo.get('modulo', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{completado_si_no}</td>
                <td style="padding: 10px 8px; text-align: center;">{fecha}</td>
                <td style="padding: 10px 8px; text-align: center;">{calificacion}</td>
            </tr>
            """

        # Estado general
        estado_general = "En Progreso" if completados < total_modulos else "Completado"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Helvetica, Arial, sans-serif;
                    color: #000000;
                    max-width: 8.5in;
                    margin: 0 auto;
                    padding: 0.5in;
                    background: white;
                    line-height: 1.4;
                }}

                h1 {{
                    color: #002E6D;
                    font-size: 20px;
                    text-align: center;
                    margin: 0 0 10px 0;
                    font-weight: bold;
                }}

                .subtitle {{
                    text-align: center;
                    font-size: 12px;
                    color: #666666;
                    margin-bottom: 30px;
                }}

                .section-title {{
                    color: #002E6D;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 20px 0 10px 0;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 11px;
                }}

                .info-table td {{
                    padding: 8px 10px;
                    border: none;
                }}

                .info-table td:first-child {{
                    font-weight: bold;
                    color: #002E6D;
                    width: 150px;
                }}

                .data-table {{
                    border: 0.5px solid #808080;
                }}

                .data-table thead {{
                    background-color: #002E6D;
                    color: white;
                }}

                .data-table th {{
                    padding: 10px 8px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 11px;
                    border-bottom: 2px solid #002E6D;
                }}

                .data-table td {{
                    padding: 10px 8px;
                    border: 0.5px solid #808080;
                    font-size: 10px;
                }}

                .data-table tbody tr:nth-child(even) {{
                    background-color: #F5F5F5;
                }}

                .data-table tbody tr:nth-child(odd) {{
                    background-color: #FFFFFF;
                }}

                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 9px;
                    color: #808080;
                }}
            </style>
        </head>
        <body>
            <h1>Reporte de Progreso - Instituto Hutchison Ports</h1>

            <div class="section-title">Información del Usuario</div>
            <table class="info-table">
                <tr>
                    <td>User ID:</td>
                    <td>{datos.get('user_id', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Nombre:</td>
                    <td>{datos.get('nombre', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Email:</td>
                    <td>{datos.get('email', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Fecha de Reporte:</td>
                    <td>{fecha_actual}</td>
                </tr>
            </table>

            <div class="section-title">Progreso por Módulo</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Módulo</th>
                        <th>Completado</th>
                        <th>Fecha Finalización</th>
                        <th>Calificación</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_modulos}
                </tbody>
            </table>

            <div class="section-title">Resumen de Desempeño</div>
            <table class="info-table">
                <tr>
                    <td>Módulos Completados:</td>
                    <td>{completados} / {total_modulos}</td>
                </tr>
                <tr>
                    <td>Promedio General:</td>
                    <td>{promedio:.1f}%</td>
                </tr>
                <tr>
                    <td>Estado:</td>
                    <td>{estado_general}</td>
                </tr>
            </table>

            <div class="footer">
                Generado automáticamente por Smart Reports v2.0 - {fecha_actual}
            </div>
        </body>
        </html>
        """

        return html

    def mostrar_reporte_periodo(self, datos_periodo, registros):
        """Mostrar reporte de periodo"""
        html = self._generar_html_periodo(datos_periodo, registros)
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()
        self.html_widget.load_file(temp_file.name)

    def mostrar_reporte_niveles_mando(self, datos_niveles, estadisticas):
        """Mostrar reporte por niveles de mando"""
        html = self._generar_html_niveles_mando(datos_niveles, estadisticas)
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html)
        temp_file.close()
        self.html_widget.load_file(temp_file.name)

    def _generar_html_periodo(self, datos, registros):
        """Generar HTML que replica EXACTAMENTE el formato del PDF de ReportLab"""
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Generar filas de tabla - igual al PDF
        filas_registros = ""
        for idx, reg in enumerate(registros):
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F5F5F5"
            filas_registros += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px 8px;">{reg.get('usuario', 'N/A')}</td>
                <td style="padding: 10px 8px;">{reg.get('modulo', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{reg.get('fecha', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{reg.get('estado', 'N/A')}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_common_styles()}
            </style>
        </head>
        <body>
            <h1>Reporte por Periodo - Instituto Hutchison Ports</h1>

            <div class="section-title">Parámetros del Reporte</div>
            <table class="info-table">
                <tr>
                    <td>Módulo:</td>
                    <td>{datos.get('modulo', 'Todos')}</td>
                </tr>
                <tr>
                    <td>Fecha Inicio:</td>
                    <td>{datos.get('fecha_inicio', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Fecha Fin:</td>
                    <td>{datos.get('fecha_fin', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Total Registros:</td>
                    <td>{len(registros)}</td>
                </tr>
            </table>

            <div class="section-title">Registros del Periodo</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Módulo</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_registros if filas_registros else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay registros para mostrar</td></tr>'}
                </tbody>
            </table>

            <div class="footer">
                Generado automáticamente por Smart Reports v2.0 - {fecha_actual}
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_unidad(self, datos, estadisticas):
        """Generar HTML que replica EXACTAMENTE el formato del PDF de ReportLab"""
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Generar filas de tabla de usuarios - igual al PDF
        filas_usuarios = ""
        for idx, usuario in enumerate(estadisticas.get('usuarios', [])):
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F5F5F5"
            filas_usuarios += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px 8px;">{usuario.get('nombre', 'N/A')}</td>
                <td style="padding: 10px 8px;">{usuario.get('cargo', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{usuario.get('progreso', 0)}%</td>
                <td style="padding: 10px 8px; text-align: center;">{usuario.get('completados', 0)}/{usuario.get('total', 8)}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_common_styles()}
            </style>
        </head>
        <body>
            <h1>Reporte por Unidad de Negocio - Instituto Hutchison Ports</h1>

            <div class="section-title">Información de la Unidad</div>
            <table class="info-table">
                <tr>
                    <td>Unidad de Negocio:</td>
                    <td>{datos.get('unidad', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Código:</td>
                    <td>{datos.get('codigo', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Total Usuarios:</td>
                    <td>{estadisticas.get('total_usuarios', 0)}</td>
                </tr>
                <tr>
                    <td>Módulo Consultado:</td>
                    <td>{datos.get('modulo', 'Todos')}</td>
                </tr>
            </table>

            <div class="section-title">Estadísticas de la Unidad</div>
            <table class="info-table">
                <tr>
                    <td>Progreso Promedio:</td>
                    <td>{estadisticas.get('progreso_promedio', 0):.1f}%</td>
                </tr>
                <tr>
                    <td>Usuarios Activos:</td>
                    <td>{estadisticas.get('usuarios_activos', 0)}</td>
                </tr>
                <tr>
                    <td>Módulos Completados:</td>
                    <td>{estadisticas.get('modulos_completados', 0)}</td>
                </tr>
            </table>

            <div class="section-title">Progreso por Usuario</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nombre Usuario</th>
                        <th>Cargo</th>
                        <th>Progreso</th>
                        <th>Módulos</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_usuarios if filas_usuarios else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                </tbody>
            </table>

            <div class="footer">
                Generado automáticamente por Smart Reports v2.0 - {fecha_actual}
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_global(self, estadisticas):
        """Generar HTML que replica EXACTAMENTE el formato del PDF de ReportLab"""
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Generar filas para módulos - igual al PDF
        filas_modulos = ""
        for idx, modulo in enumerate(estadisticas.get('por_modulo', [])):
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F5F5F5"
            filas_modulos += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px 8px;">{modulo.get('nombre', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{modulo.get('inscritos', 0)}</td>
                <td style="padding: 10px 8px; text-align: center;">{modulo.get('completados', 0)}</td>
                <td style="padding: 10px 8px; text-align: center;">{modulo.get('porcentaje', 0):.1f}%</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_common_styles()}
            </style>
        </head>
        <body>
            <h1>Reporte Global del Instituto - Instituto Hutchison Ports</h1>

            <div class="section-title">Estadísticas Generales</div>
            <table class="info-table">
                <tr>
                    <td>Total Usuarios:</td>
                    <td>{estadisticas.get('total_usuarios', 0)}</td>
                </tr>
                <tr>
                    <td>Usuarios Activos:</td>
                    <td>{estadisticas.get('usuarios_activos', 0)}</td>
                </tr>
                <tr>
                    <td>Progreso Global:</td>
                    <td>{estadisticas.get('progreso_global', 0):.1f}%</td>
                </tr>
            </table>

            <div class="section-title">Resumen por Módulo</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Módulo</th>
                        <th>Inscritos</th>
                        <th>Completados</th>
                        <th>% Completado</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_modulos if filas_modulos else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                </tbody>
            </table>

            <div class="section-title">Métricas Adicionales</div>
            <table class="info-table">
                <tr>
                    <td>Total Evaluaciones:</td>
                    <td>{estadisticas.get('total_evaluaciones', 0)}</td>
                </tr>
                <tr>
                    <td>Evaluaciones Aprobadas:</td>
                    <td>{estadisticas.get('evaluaciones_aprobadas', 0)}</td>
                </tr>
                <tr>
                    <td>Promedio General:</td>
                    <td>{estadisticas.get('promedio_general', 0):.1f}%</td>
                </tr>
                <tr>
                    <td>Tasa de Aprobación:</td>
                    <td>{estadisticas.get('tasa_aprobacion', 0):.1f}%</td>
                </tr>
            </table>

            <div class="footer">
                Generado automáticamente por Smart Reports v2.0 - {fecha_actual}
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_niveles_mando(self, datos, estadisticas):
        """Generar HTML que replica EXACTAMENTE el formato del PDF de ReportLab"""
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Generar filas para niveles - igual al PDF
        filas_niveles = ""
        for idx, nivel in enumerate(estadisticas.get('por_nivel', [])):
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F5F5F5"
            filas_niveles += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 10px 8px;">{nivel.get('nivel', 'N/A')}</td>
                <td style="padding: 10px 8px; text-align: center;">{nivel.get('total_usuarios', 0)}</td>
                <td style="padding: 10px 8px; text-align: center;">{nivel.get('progreso_promedio', 0):.1f}%</td>
                <td style="padding: 10px 8px; text-align: center;">{nivel.get('completados', 0)}</td>
                <td style="padding: 10px 8px; text-align: center;">{nivel.get('en_progreso', 0)}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {self._get_common_styles()}
            </style>
        </head>
        <body>
            <h1>Reporte por Niveles de Mando - Instituto Hutchison Ports</h1>

            <div class="section-title">Parámetros del Reporte</div>
            <table class="info-table">
                <tr>
                    <td>Módulo Consultado:</td>
                    <td>{datos.get('modulo', 'Todos los módulos')}</td>
                </tr>
                <tr>
                    <td>Total Niveles:</td>
                    <td>{len(estadisticas.get('por_nivel', []))}</td>
                </tr>
                <tr>
                    <td>Total Usuarios:</td>
                    <td>{estadisticas.get('total_usuarios', 0)}</td>
                </tr>
                <tr>
                    <td>Fecha de Generación:</td>
                    <td>{fecha_actual}</td>
                </tr>
            </table>

            <div class="section-title">Estadísticas Consolidadas</div>
            <table class="info-table">
                <tr>
                    <td>Progreso Promedio:</td>
                    <td>{estadisticas.get('progreso_total', 0):.1f}%</td>
                </tr>
                <tr>
                    <td>Completados:</td>
                    <td>{estadisticas.get('total_completados', 0)}</td>
                </tr>
                <tr>
                    <td>En Progreso:</td>
                    <td>{estadisticas.get('total_en_progreso', 0)}</td>
                </tr>
            </table>

            <div class="section-title">Progreso por Nivel de Mando</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nivel de Mando</th>
                        <th>Usuarios</th>
                        <th>Progreso</th>
                        <th>Completados</th>
                        <th>En Progreso</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_niveles if filas_niveles else '<tr><td colspan="5" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                </tbody>
            </table>

            <div class="footer">
                Generado automáticamente por Smart Reports v2.0 - {fecha_actual}
            </div>
        </body>
        </html>
        """
        return html

    def _get_common_styles(self):
        """
        Estilos CSS que replican el formato de PDFs de ReportLab
        Sin gradientes, sin bordes redondeados - estilo documento profesional
        """
        return """
                body {
                    font-family: Helvetica, Arial, sans-serif;
                    color: #000000;
                    max-width: 8.5in;
                    margin: 0 auto;
                    padding: 0.5in;
                    background: white;
                    line-height: 1.4;
                }

                h1 {
                    color: #002E6D;
                    font-size: 20px;
                    text-align: center;
                    margin: 0 0 10px 0;
                    font-weight: bold;
                }

                .subtitle {
                    text-align: center;
                    font-size: 12px;
                    color: #666666;
                    margin-bottom: 30px;
                }

                .section-title {
                    color: #002E6D;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 20px 0 10px 0;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 11px;
                }

                .info-table td {
                    padding: 8px 10px;
                    border: none;
                }

                .info-table td:first-child {
                    font-weight: bold;
                    color: #002E6D;
                    width: 200px;
                }

                .data-table {
                    border: 0.5px solid #808080;
                }

                .data-table thead {
                    background-color: #002E6D;
                    color: white;
                }

                .data-table th {
                    padding: 10px 8px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 11px;
                    border-bottom: 2px solid #002E6D;
                }

                .data-table td {
                    padding: 10px 8px;
                    border: 0.5px solid #808080;
                    font-size: 10px;
                }

                .data-table tbody tr:nth-child(even) {
                    background-color: #F5F5F5;
                }

                .data-table tbody tr:nth-child(odd) {
                    background-color: #FFFFFF;
                }

                .footer {
                    margin-top: 50px;
                    text-align: center;
                    font-size: 9px;
                    color: #808080;
                }
        """
