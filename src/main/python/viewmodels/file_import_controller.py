"""
FileImportController - LÓGICA de importación de archivos
Separa la lógica de archivos de la interfaz (patrón Android: Controller = Java)

ACTUALIZADO: Ahora usa el nuevo sistema ETL completo (etl_instituto_completo.py)
"""
import os


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

    def import_file_to_database(self, tipo_archivo='auto'):
        """
        Importar archivo actual a base de datos usando el nuevo sistema ETL

        Args:
            tipo_archivo: 'training', 'org_planning' o 'auto' para detectar automáticamente

        Returns:
            tuple: (exito, estadisticas_o_error)
        """
        if not self.current_file:
            return False, "No hay archivo cargado"

        if not self.conn:
            return False, "No hay conexión a base de datos"

        try:
            # Importar ETL (solo cuando se necesite para evitar errores de inicio)
            try:
                from src.main.python.domain.services.etl_instituto_completo import (
                    ETLInstitutoCompleto,
                    ETLConfig
                )
            except ImportError:
                return False, "Sistema ETL no disponible. Verifica la instalación."

            # Detectar tipo automáticamente si es necesario
            if tipo_archivo == 'auto':
                tipo_archivo = self._detectar_tipo_archivo(self.current_file)
                self.log_import_action(f"Tipo detectado: {tipo_archivo}")

            # Configurar ETL (adaptar según tu configuración de BD)
            config = ETLConfig(
                server="localhost",
                database="InstitutoHutchison",
                username=None,  # None = Windows Authentication
                password=None
            )

            # Crear instancia del ETL
            with ETLInstitutoCompleto(config) as etl:
                # Importar según tipo
                if tipo_archivo == 'training':
                    stats = etl.importar_training_report(self.current_file)
                elif tipo_archivo == 'org_planning':
                    stats = etl.importar_org_planning(self.current_file)
                else:
                    return False, f"Tipo de archivo no soportado: {tipo_archivo}"

            # Registrar en log
            total_procesados = (
                stats.get('progresos_insertados', 0) +
                stats.get('progresos_actualizados', 0) +
                stats.get('usuarios_nuevos', 0) +
                stats.get('usuarios_actualizados', 0)
            )

            self.log_import_action(
                f"Importación exitosa: {total_procesados} registros procesados"
            )

            return True, stats

        except Exception as e:
            error_msg = f"Error en importación: {str(e)}"
            self.log_import_action(error_msg)
            return False, error_msg

    def _detectar_tipo_archivo(self, file_path):
        """
        Detecta automáticamente si es Training Report u Org Planning

        Args:
            file_path: Ruta al archivo Excel

        Returns:
            'training' o 'org_planning'
        """
        try:
            import pandas as pd

            # Leer solo las primeras filas para detectar columnas
            df = pd.read_excel(file_path, nrows=1)
            columnas = [str(col).lower() for col in df.columns]

            # Columnas típicas de Training Report
            training_keywords = ['training', 'module', 'módulo', 'score', 'calificación', 'completion']

            # Columnas típicas de Org Planning
            org_keywords = ['position', 'cargo', 'division', 'división', 'location', 'ubicación']

            # Contar coincidencias
            training_matches = sum(1 for kw in training_keywords if any(kw in col for col in columnas))
            org_matches = sum(1 for kw in org_keywords if any(kw in col for col in columnas))

            # Decidir según coincidencias
            if training_matches > org_matches:
                return 'training'
            else:
                return 'org_planning'

        except:
            # Por defecto, asumir training
            return 'training'

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
