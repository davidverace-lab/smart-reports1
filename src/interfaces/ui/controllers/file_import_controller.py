"""
FileImportController - LÓGICA de importación de archivos
Separa la lógica de archivos de la interfaz (patrón Android: Controller = Java)
"""
import os
from src.application.services.importador_capacitacion import ImportadorCapacitacion


class FileImportController:
    """Controller para manejar la importación de archivos"""

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a la base de datos
        """
        self.db = db_connection
        self.conn = db_connection.connect() if db_connection else None
        self.current_file = None
        self.changes_log = []

    def validate_file(self, file_path):
        """
        Validar que el archivo existe y es válido

        Args:
            file_path: Ruta del archivo

        Returns:
            tuple: (es_valido, mensaje)
        """
        if not file_path:
            return False, "No se especificó ningún archivo"

        if not os.path.exists(file_path):
            return False, f"El archivo no existe: {file_path}"

        if not file_path.lower().endswith(('.xlsx', '.xls', '.csv')):
            return False, "El archivo debe ser Excel (.xlsx, .xls) o CSV (.csv)"

        # Verificar que el archivo no esté vacío
        if os.path.getsize(file_path) == 0:
            return False, "El archivo está vacío"

        return True, "Archivo válido"

    def load_file(self, file_path):
        """
        Cargar archivo para preview

        Args:
            file_path: Ruta del archivo

        Returns:
            tuple: (exito, mensaje_o_error)
        """
        is_valid, message = self.validate_file(file_path)
        if not is_valid:
            return False, message

        try:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)

            return True, {
                'filename': filename,
                'path': file_path,
                'size': f"{size_mb:.2f} MB",
                'extension': os.path.splitext(filename)[1]
            }

        except Exception as e:
            return False, f"Error al cargar archivo: {str(e)}"

    def import_file_to_database(self):
        """
        Importar archivo actual a base de datos

        Returns:
            tuple: (exito, estadisticas_o_error)
        """
        if not self.current_file:
            return False, "No hay archivo cargado"

        if not self.conn:
            return False, "No hay conexión a base de datos"

        try:
            # Crear importador
            importador = ImportadorCapacitacion(self.conn)

            # Ejecutar importación
            stats = importador.importar_desde_excel(self.current_file)

            # Registrar en log
            self.log_import_action(
                f"Importación exitosa: {stats.get('registros_procesados', 0)} registros"
            )

            return True, stats

        except Exception as e:
            error_msg = f"Error en importación: {str(e)}"
            self.log_import_action(error_msg)
            return False, error_msg

    def log_import_action(self, message):
        """
        Registrar acción en el log

        Args:
            message: Mensaje a registrar
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.changes_log.append(log_entry)
        print(log_entry)

    def get_import_log(self):
        """
        Obtener log de importaciones

        Returns:
            list: Lista de mensajes del log
        """
        return self.changes_log.copy()

    def clear_import_log(self):
        """Limpiar el log de importaciones"""
        self.changes_log.clear()

    def get_current_file_info(self):
        """
        Obtener información del archivo actual

        Returns:
            dict: Información del archivo o None
        """
        if not self.current_file:
            return None

        try:
            return {
                'path': self.current_file,
                'filename': os.path.basename(self.current_file),
                'size': os.path.getsize(self.current_file),
                'exists': os.path.exists(self.current_file)
            }
        except:
            return None
