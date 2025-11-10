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
        """Generar HTML estilo Word para reporte de usuario"""

        fecha_actual = datetime.now().strftime('%d de %B de %Y')

        # Calcular estadísticas
        total_modulos = len(progreso)
        completados = sum(1 for m in progreso if m.get('completado', False))
        porcentaje_global = (completados / total_modulos * 100) if total_modulos > 0 else 0

        # Generar filas de tabla
        filas_modulos = ""
        for modulo in progreso:
            estado = "✓ Completado" if modulo.get('completado', False) else "○ Pendiente"
            estado_color = "#51cf66" if modulo.get('completado', False) else "#ffa94d"
            fecha = modulo.get('fecha', 'Pendiente')
            calificacion = f"{modulo.get('calificacion', 0)}%" if modulo.get('completado', False) else "N/A"

            filas_modulos += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0;">{modulo.get('modulo', 'N/A')}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; color: {estado_color}; font-weight: 600;">
                    {estado}
                </td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">{fecha}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center; font-weight: 600;">
                    {calificacion}
                </td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}

                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 21cm;
                    margin: 0 auto;
                    padding: 40px;
                    background: white;
                }}

                .header {{
                    text-align: center;
                    border-bottom: 4px solid #002E6D;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}

                .header h1 {{
                    color: #002E6D;
                    font-size: 28px;
                    margin: 0 0 10px 0;
                    font-weight: 700;
                }}

                .header .subtitle {{
                    color: #009BDE;
                    font-size: 16px;
                    font-weight: 600;
                }}

                .section {{
                    margin: 30px 0;
                }}

                .section-title {{
                    background: linear-gradient(135deg, #002E6D 0%, #004C97 100%);
                    color: white;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: 600;
                    border-radius: 6px;
                    margin-bottom: 15px;
                }}

                .info-grid {{
                    display: grid;
                    grid-template-columns: 180px 1fr;
                    gap: 12px;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 6px;
                    border-left: 4px solid #009BDE;
                }}

                .info-label {{
                    font-weight: 600;
                    color: #002E6D;
                }}

                .info-value {{
                    color: #333;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    background: white;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    border-radius: 6px;
                    overflow: hidden;
                }}

                thead {{
                    background: linear-gradient(135deg, #002E6D 0%, #004C97 100%);
                    color: white;
                }}

                th {{
                    padding: 15px 12px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 14px;
                }}

                td {{
                    padding: 12px;
                    border-bottom: 1px solid #e0e0e0;
                }}

                tr:last-child td {{
                    border-bottom: none;
                }}

                tr:hover {{
                    background: #f8f9fa;
                }}

                .stats-box {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }}

                .stat-card {{
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px solid #dee2e6;
                }}

                .stat-value {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #002E6D;
                    margin: 5px 0;
                }}

                .stat-label {{
                    font-size: 13px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}

                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #e0e0e0;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>REPORTE DE PROGRESO DEL USUARIO</h1>
                <div class="subtitle">Instituto Hutchison Ports</div>
                <div style="color: #666; margin-top: 10px; font-size: 14px;">{fecha_actual}</div>
            </div>

            <div class="section">
                <div class="section-title">Información del Usuario</div>
                <div class="info-grid">
                    <div class="info-label">User ID:</div>
                    <div class="info-value">{datos.get('user_id', 'N/A')}</div>

                    <div class="info-label">Nombre Completo:</div>
                    <div class="info-value">{datos.get('nombre', 'N/A')}</div>

                    <div class="info-label">Correo Electrónico:</div>
                    <div class="info-value">{datos.get('email', 'N/A')}</div>

                    <div class="info-label">Fecha de Reporte:</div>
                    <div class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M hrs')}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Resumen de Desempeño</div>
                <div class="stats-box">
                    <div class="stat-card">
                        <div class="stat-label">Total Módulos</div>
                        <div class="stat-value">{total_modulos}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Completados</div>
                        <div class="stat-value" style="color: #51cf66;">{completados}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Progreso General</div>
                        <div class="stat-value" style="color: #009BDE;">{porcentaje_global:.1f}%</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Progreso por Módulo</div>
                <table>
                    <thead>
                        <tr>
                            <th>Módulo</th>
                            <th>Estado</th>
                            <th style="text-align: center;">Fecha Finalización</th>
                            <th style="text-align: center;">Calificación</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_modulos}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <div>© {datetime.now().year} Instituto Hutchison Ports - Todos los derechos reservados</div>
                <div style="margin-top: 5px;">Sistema Smart Reports v2.0</div>
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
        """Generar HTML estilo Word para reporte de periodo"""
        fecha_actual = datetime.now().strftime('%d de %B de %Y')

        # Generar filas de tabla
        filas_registros = ""
        for reg in registros:
            filas_registros += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{reg.get('usuario', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{reg.get('modulo', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center;">{reg.get('fecha', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center; font-weight: 600;">
                    {reg.get('estado', 'N/A')}
                </td>
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
            <div class="header">
                <h1>REPORTE POR PERIODO</h1>
                <div class="subtitle">Instituto Hutchison Ports</div>
                <div style="color: #666; margin-top: 10px; font-size: 14px;">{fecha_actual}</div>
            </div>

            <div class="section">
                <div class="section-title">Parámetros del Reporte</div>
                <div class="info-grid">
                    <div class="info-label">Módulo:</div>
                    <div class="info-value">{datos.get('modulo', 'Todos')}</div>

                    <div class="info-label">Fecha Inicio:</div>
                    <div class="info-value">{datos.get('fecha_inicio', 'N/A')}</div>

                    <div class="info-label">Fecha Fin:</div>
                    <div class="info-value">{datos.get('fecha_fin', 'N/A')}</div>

                    <div class="info-label">Total Registros:</div>
                    <div class="info-value">{len(registros)}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Registros del Periodo</div>
                <table>
                    <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Módulo</th>
                            <th style="text-align: center;">Fecha</th>
                            <th style="text-align: center;">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_registros if filas_registros else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay registros para mostrar</td></tr>'}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <div>© {datetime.now().year} Instituto Hutchison Ports - Todos los derechos reservados</div>
                <div style="margin-top: 5px;">Sistema Smart Reports v2.0</div>
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_unidad(self, datos, estadisticas):
        """Generar HTML estilo Word para reporte de unidad de negocio"""
        fecha_actual = datetime.now().strftime('%d de %B de %Y')

        # Generar filas de tabla de usuarios
        filas_usuarios = ""
        for usuario in estadisticas.get('usuarios', []):
            progreso_color = "#51cf66" if usuario.get('progreso', 0) >= 70 else "#ffa94d"
            filas_usuarios += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{usuario.get('nombre', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{usuario.get('cargo', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center; font-weight: 600; color: {progreso_color};">
                    {usuario.get('progreso', 0)}%
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center;">
                    {usuario.get('completados', 0)}/{usuario.get('total', 8)}
                </td>
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
            <div class="header">
                <h1>REPORTE POR UNIDAD DE NEGOCIO</h1>
                <div class="subtitle">Instituto Hutchison Ports</div>
                <div style="color: #666; margin-top: 10px; font-size: 14px;">{fecha_actual}</div>
            </div>

            <div class="section">
                <div class="section-title">Información de la Unidad</div>
                <div class="info-grid">
                    <div class="info-label">Unidad de Negocio:</div>
                    <div class="info-value">{datos.get('unidad', 'N/A')}</div>

                    <div class="info-label">Código:</div>
                    <div class="info-value">{datos.get('codigo', 'N/A')}</div>

                    <div class="info-label">Total Usuarios:</div>
                    <div class="info-value">{estadisticas.get('total_usuarios', 0)}</div>

                    <div class="info-label">Módulo Consultado:</div>
                    <div class="info-value">{datos.get('modulo', 'Todos')}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Estadísticas de la Unidad</div>
                <div class="stats-box">
                    <div class="stat-card">
                        <div class="stat-label">Progreso Promedio</div>
                        <div class="stat-value" style="color: #009BDE;">{estadisticas.get('progreso_promedio', 0):.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Usuarios Activos</div>
                        <div class="stat-value" style="color: #51cf66;">{estadisticas.get('usuarios_activos', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Módulos Completados</div>
                        <div class="stat-value" style="color: #002E6D;">{estadisticas.get('modulos_completados', 0)}</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Progreso por Usuario</div>
                <table>
                    <thead>
                        <tr>
                            <th>Nombre Usuario</th>
                            <th>Cargo</th>
                            <th style="text-align: center;">Progreso</th>
                            <th style="text-align: center;">Módulos</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_usuarios if filas_usuarios else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <div>© {datetime.now().year} Instituto Hutchison Ports - Todos los derechos reservados</div>
                <div style="margin-top: 5px;">Sistema Smart Reports v2.0</div>
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_global(self, estadisticas):
        """Generar HTML estilo Word para reporte global"""
        fecha_actual = datetime.now().strftime('%d de %B de %Y')

        # Generar filas para módulos
        filas_modulos = ""
        for modulo in estadisticas.get('por_modulo', []):
            filas_modulos += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{modulo.get('nombre', 'N/A')}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center;">{modulo.get('inscritos', 0)}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center; font-weight: 600; color: #51cf66;">
                    {modulo.get('completados', 0)}
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: center; color: #009BDE; font-weight: 600;">
                    {modulo.get('porcentaje', 0):.1f}%
                </td>
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
            <div class="header">
                <h1>REPORTE GLOBAL DEL INSTITUTO</h1>
                <div class="subtitle">Instituto Hutchison Ports</div>
                <div style="color: #666; margin-top: 10px; font-size: 14px;">{fecha_actual}</div>
            </div>

            <div class="section">
                <div class="section-title">Estadísticas Generales</div>
                <div class="stats-box">
                    <div class="stat-card">
                        <div class="stat-label">Total Usuarios</div>
                        <div class="stat-value">{estadisticas.get('total_usuarios', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Usuarios Activos</div>
                        <div class="stat-value" style="color: #51cf66;">{estadisticas.get('usuarios_activos', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Progreso Global</div>
                        <div class="stat-value" style="color: #009BDE;">{estadisticas.get('progreso_global', 0):.1f}%</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Resumen por Módulo</div>
                <table>
                    <thead>
                        <tr>
                            <th>Módulo</th>
                            <th style="text-align: center;">Inscritos</th>
                            <th style="text-align: center;">Completados</th>
                            <th style="text-align: center;">% Completado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_modulos if filas_modulos else '<tr><td colspan="4" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <div class="section-title">Métricas Adicionales</div>
                <div class="info-grid">
                    <div class="info-label">Total Evaluaciones:</div>
                    <div class="info-value">{estadisticas.get('total_evaluaciones', 0)}</div>

                    <div class="info-label">Evaluaciones Aprobadas:</div>
                    <div class="info-value">{estadisticas.get('evaluaciones_aprobadas', 0)}</div>

                    <div class="info-label">Promedio General:</div>
                    <div class="info-value">{estadisticas.get('promedio_general', 0):.1f}%</div>

                    <div class="info-label">Tasa de Aprobación:</div>
                    <div class="info-value">{estadisticas.get('tasa_aprobacion', 0):.1f}%</div>
                </div>
            </div>

            <div class="footer">
                <div>© {datetime.now().year} Instituto Hutchison Ports - Todos los derechos reservados</div>
                <div style="margin-top: 5px;">Sistema Smart Reports v2.0</div>
            </div>
        </body>
        </html>
        """
        return html

    def _generar_html_niveles_mando(self, datos, estadisticas):
        """Generar HTML estilo Word para reporte por niveles de mando"""
        fecha_actual = datetime.now().strftime('%d de %B de %Y')

        # Generar filas para niveles
        filas_niveles = ""
        for nivel in estadisticas.get('por_nivel', []):
            progreso_color = "#51cf66" if nivel.get('progreso_promedio', 0) >= 70 else "#ffa94d"
            filas_niveles += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">{nivel.get('nivel', 'N/A')}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center;">{nivel.get('total_usuarios', 0)}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center; font-weight: 600; color: {progreso_color};">
                    {nivel.get('progreso_promedio', 0):.1f}%
                </td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center; color: #51cf66;">
                    {nivel.get('completados', 0)}
                </td>
                <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; text-align: center; color: #ffa94d;">
                    {nivel.get('en_progreso', 0)}
                </td>
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
            <div class="header">
                <h1>REPORTE POR NIVELES DE MANDO</h1>
                <div class="subtitle">Instituto Hutchison Ports</div>
                <div style="color: #666; margin-top: 10px; font-size: 14px;">{fecha_actual}</div>
            </div>

            <div class="section">
                <div class="section-title">Parámetros del Reporte</div>
                <div class="info-grid">
                    <div class="info-label">Módulo Consultado:</div>
                    <div class="info-value">{datos.get('modulo', 'Todos los módulos')}</div>

                    <div class="info-label">Total Niveles:</div>
                    <div class="info-value">{len(estadisticas.get('por_nivel', []))}</div>

                    <div class="info-label">Total Usuarios:</div>
                    <div class="info-value">{estadisticas.get('total_usuarios', 0)}</div>

                    <div class="info-label">Fecha de Generación:</div>
                    <div class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M hrs')}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Estadísticas Consolidadas</div>
                <div class="stats-box">
                    <div class="stat-card">
                        <div class="stat-label">Progreso Promedio</div>
                        <div class="stat-value" style="color: #009BDE;">{estadisticas.get('progreso_total', 0):.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Completados</div>
                        <div class="stat-value" style="color: #51cf66;">{estadisticas.get('total_completados', 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">En Progreso</div>
                        <div class="stat-value" style="color: #ffa94d;">{estadisticas.get('total_en_progreso', 0)}</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Progreso por Nivel de Mando</div>
                <table>
                    <thead>
                        <tr>
                            <th>Nivel de Mando</th>
                            <th style="text-align: center;">Usuarios</th>
                            <th style="text-align: center;">Progreso</th>
                            <th style="text-align: center;">Completados</th>
                            <th style="text-align: center;">En Progreso</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_niveles if filas_niveles else '<tr><td colspan="5" style="text-align:center; padding:20px;">No hay datos disponibles</td></tr>'}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <div>© {datetime.now().year} Instituto Hutchison Ports - Todos los derechos reservados</div>
                <div style="margin-top: 5px;">Sistema Smart Reports v2.0</div>
            </div>
        </body>
        </html>
        """
        return html

    def _get_common_styles(self):
        """Estilos CSS comunes para todos los reportes"""
        return """
                @page {
                    size: A4;
                    margin: 2cm;
                }

                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 21cm;
                    margin: 0 auto;
                    padding: 40px;
                    background: white;
                }

                .header {
                    text-align: center;
                    border-bottom: 4px solid #002E6D;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }

                .header h1 {
                    color: #002E6D;
                    font-size: 28px;
                    margin: 0 0 10px 0;
                    font-weight: 700;
                }

                .header .subtitle {
                    color: #009BDE;
                    font-size: 16px;
                    font-weight: 600;
                }

                .section {
                    margin: 30px 0;
                }

                .section-title {
                    background: linear-gradient(135deg, #002E6D 0%, #004C97 100%);
                    color: white;
                    padding: 12px 20px;
                    font-size: 16px;
                    font-weight: 600;
                    border-radius: 6px;
                    margin-bottom: 15px;
                }

                .info-grid {
                    display: grid;
                    grid-template-columns: 180px 1fr;
                    gap: 12px;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 6px;
                    border-left: 4px solid #009BDE;
                }

                .info-label {
                    font-weight: 600;
                    color: #002E6D;
                }

                .info-value {
                    color: #333;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    background: white;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    border-radius: 6px;
                    overflow: hidden;
                }

                thead {
                    background: linear-gradient(135deg, #002E6D 0%, #004C97 100%);
                    color: white;
                }

                th {
                    padding: 15px 12px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 14px;
                }

                td {
                    padding: 12px;
                    border-bottom: 1px solid #e0e0e0;
                }

                tr:last-child td {
                    border-bottom: none;
                }

                tr:hover {
                    background: #f8f9fa;
                }

                .stats-box {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }

                .stat-card {
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px solid #dee2e6;
                }

                .stat-value {
                    font-size: 32px;
                    font-weight: 700;
                    color: #002E6D;
                    margin: 5px 0;
                }

                .stat-label {
                    font-size: 13px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .footer {
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #e0e0e0;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }
        """
