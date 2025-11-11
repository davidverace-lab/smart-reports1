"""
Exportador de Logs
Permite guardar logs de importación en archivos de texto
"""
import os
from datetime import datetime
from tkinter import filedialog, messagebox


class ExportadorLogs:
    """Clase para exportar logs a archivos"""

    @staticmethod
    def exportar_log(contenido_log, nombre_base="importacion"):
        """
        Exportar log a archivo de texto

        Args:
            contenido_log: Contenido del log (string)
            nombre_base: Nombre base del archivo

        Returns:
            str: Ruta del archivo guardado o None si se canceló
        """
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_sugerido = f"log_{nombre_base}_{timestamp}.txt"

        # Diálogo para guardar
        file_path = filedialog.asksaveasfilename(
            title="Guardar Log de Importación",
            defaultextension=".txt",
            initialfile=nombre_sugerido,
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not file_path:
            return None

        try:
            # Guardar archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                # Header
                f.write("="*80 + "\n")
                f.write("SMART REPORTS - LOG DE IMPORTACIÓN\n")
                f.write("Instituto Hutchison Ports\n")
                f.write("="*80 + "\n\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Archivo: {os.path.basename(file_path)}\n")
                f.write("\n" + "="*80 + "\n\n")

                # Contenido
                f.write(contenido_log)

                # Footer
                f.write("\n\n" + "="*80 + "\n")
                f.write("FIN DEL LOG\n")
                f.write("="*80 + "\n")

            messagebox.showinfo(
                "✅ Log Exportado",
                f"Log guardado exitosamente:\n\n{file_path}"
            )

            return file_path

        except Exception as e:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo guardar el log:\n\n{str(e)}"
            )
            return None

    @staticmethod
    def exportar_log_html(contenido_log, nombre_base="importacion"):
        """
        Exportar log a archivo HTML con formato

        Args:
            contenido_log: Contenido del log (string)
            nombre_base: Nombre base del archivo

        Returns:
            str: Ruta del archivo guardado o None si se canceló
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_sugerido = f"log_{nombre_base}_{timestamp}.html"

        file_path = filedialog.asksaveasfilename(
            title="Guardar Log HTML",
            defaultextension=".html",
            initialfile=nombre_sugerido,
            filetypes=[
                ("Archivos HTML", "*.html"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not file_path:
            return None

        try:
            # Convertir log a HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log de Importación - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: 'Consolas', 'Courier New', monospace;
            background: #1a1d2e;
            color: #ffffff;
            padding: 30px;
            line-height: 1.6;
        }}
        .header {{
            background: #002E6D;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            color: #ffffff;
        }}
        .header p {{
            margin: 5px 0;
            color: #9ACAEB;
        }}
        .log-content {{
            background: #2b2d42;
            padding: 20px;
            border-radius: 10px;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .success {{ color: #00B5AD; }}
        .error {{ color: #FF6B35; }}
        .warning {{ color: #FFD700; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 SMART REPORTS - Log de Importación</h1>
        <p>Instituto Hutchison Ports</p>
        <p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <div class="log-content">{ExportadorLogs._format_log_html(contenido_log)}</div>
</body>
</html>
"""

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            messagebox.showinfo(
                "✅ Log HTML Exportado",
                f"Log HTML guardado exitosamente:\n\n{file_path}"
            )

            return file_path

        except Exception as e:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo guardar el log HTML:\n\n{str(e)}"
            )
            return None

    @staticmethod
    def _format_log_html(contenido):
        """Formatear contenido de log para HTML"""
        # Reemplazar caracteres especiales
        import html as html_module
        contenido = html_module.escape(contenido)

        # Aplicar colores según palabras clave
        contenido = contenido.replace("✅", '<span class="success">✅</span>')
        contenido = contenido.replace("✓", '<span class="success">✓</span>')
        contenido = contenido.replace("❌", '<span class="error">❌</span>')
        contenido = contenido.replace("ERROR", '<span class="error">ERROR</span>')
        contenido = contenido.replace("⚠", '<span class="warning">⚠</span>')
        contenido = contenido.replace("WARN", '<span class="warning">WARN</span>')

        return contenido
