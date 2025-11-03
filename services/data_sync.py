"""
Módulo de Cruce de Datos (Data Sync)
Smart Reports v2.0

Este módulo maneja la sincronización de datos desde archivos Excel de Cornerstone
hacia el esquema de base de datos Instituto.* (14 tablas).

Funcionalidades:
- Lectura de 1-3 archivos Excel
- Mapeo de columnas Excel -> BD
- UPSERT seguro con transacciones SQL
- Normalización de nombres de módulos
- Funciones helper get_or_create
"""

import pandas as pd
import re
import unicodedata
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class DataSyncManager:
    """Gestor de sincronización de datos desde Excel a BD"""

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión activa a la base de datos
        """
        self.conn = db_connection
        self.cursor = db_connection.cursor()

        # Estadísticas del proceso
        self.stats = {
            'usuarios_creados': 0,
            'usuarios_actualizados': 0,
            'modulos_creados': 0,
            'inscripciones_creadas': 0,
            'inscripciones_actualizadas': 0,
            'evaluaciones_creadas': 0,
            'departamentos_creados': 0,
            'errores': []
        }

    # ==================== FUNCIONES DE NORMALIZACIÓN ====================

    @staticmethod
    def normalize_module_name(name: str) -> str:
        """
        Normalizar nombre de módulo para matching

        Transforma:
        - "MÓDULO 1. FILOSOFIA" -> "filosofia"
        - "Filosofia HP" -> "filosofia"
        - "MÓDULO 2. SEGURIDAD INDUSTRIAL" -> "seguridad industrial"

        Args:
            name: Nombre original del módulo

        Returns:
            Nombre normalizado (sin acentos, minúsculas, sin prefijos)
        """
        if not name:
            return ""

        # Convertir a string y minúsculas
        name = str(name).lower().strip()

        # Remover "módulo X." o "modulo X."
        name = re.sub(r'^m[oó]dulo\s*\d+[\.\:]\s*', '', name, flags=re.IGNORECASE)

        # Remover acentos
        name = ''.join(
            c for c in unicodedata.normalize('NFD', name)
            if unicodedata.category(c) != 'Mn'
        )

        # Remover caracteres especiales (mantener espacios y letras)
        name = re.sub(r'[^a-z0-9\s]', '', name)

        # Normalizar espacios múltiples
        name = re.sub(r'\s+', ' ', name).strip()

        return name

    @staticmethod
    def parse_module_number(name: str) -> Optional[int]:
        """
        Extraer número de módulo del título

        Ejemplos:
        - "MÓDULO 1. FILOSOFIA" -> 1
        - "Modulo 2: Seguridad" -> 2

        Args:
            name: Nombre del módulo

        Returns:
            Número del módulo o None
        """
        match = re.search(r'm[oó]dulo\s*(\d+)', str(name), flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def normalize_status(status: str) -> str:
        """
        Normalizar estado del módulo

        Mapeos:
        - "Terminado", "Completado", "Complete" -> "Terminado"
        - "En Proceso", "In Progress", "Started" -> "En Proceso"
        - "Registrado", "Registered", "Not Started" -> "Registrado"
        - "Fallo", "Fallido", "Failed", "Vencido" -> "Fallido"

        Args:
            status: Estado original

        Returns:
            Estado normalizado
        """
        if not status:
            return "Registrado"

        status = str(status).lower().strip()

        # Terminado
        if any(x in status for x in ['terminado', 'completado', 'complete', 'finalizado']):
            return "Terminado"

        # En Proceso
        if any(x in status for x in ['en proceso', 'in progress', 'started', 'en progreso']):
            return "En Proceso"

        # Fallido
        if any(x in status for x in ['fallo', 'fallido', 'failed', 'vencido', 'expired']):
            return "Fallido"

        # Por defecto
        return "Registrado"

    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """
        Parsear fecha desde múltiples formatos

        Soporta:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY-MM-DD
        - MM/DD/YYYY

        Args:
            date_str: String de fecha

        Returns:
            Objeto datetime o None si no se puede parsear
        """
        if not date_str or pd.isna(date_str):
            return None

        date_str = str(date_str).strip()

        # Formatos a intentar
        formats = [
            '%d/%m/%Y',
            '%d-%m-%Y',
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%d %H:%M:%S'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # Si pandas puede parsearlo
        try:
            return pd.to_datetime(date_str)
        except:
            return None

    # ==================== FUNCIONES HELPER GET_OR_CREATE ====================

    def get_or_create_module(self, module_name: str, module_number: Optional[int] = None) -> int:
        """
        Obtener IdModulo existente o crear uno nuevo

        Args:
            module_name: Nombre del módulo (será normalizado)
            module_number: Número del módulo (opcional)

        Returns:
            IdModulo (INT)
        """
        normalized_name = self.normalize_module_name(module_name)

        if not normalized_name:
            raise ValueError(f"Nombre de módulo inválido: {module_name}")

        # Buscar módulo existente por nombre normalizado
        self.cursor.execute("""
            SELECT IdModulo, NombreModulo
            FROM dbo.Instituto_Modulo
        """)

        for row in self.cursor.fetchall():
            id_modulo = row[0]
            existing_name = row[1]
            if self.normalize_module_name(existing_name) == normalized_name:
                return id_modulo

        # No existe, crear nuevo módulo
        # Usar el nombre original (sin normalizar) para la BD
        clean_name = module_name
        if module_number:
            clean_name = f"Módulo {module_number}: {module_name}"

        self.cursor.execute("""
            INSERT INTO dbo.Instituto_Modulo (NombreModulo, Activo)
            VALUES (?, 1)
        """, (clean_name,))

        self.conn.commit()

        # Obtener ID del nuevo módulo
        self.cursor.execute("SELECT @@IDENTITY")
        new_id = self.cursor.fetchone()[0]

        self.stats['modulos_creados'] += 1

        return new_id

    def get_or_create_department(self, department_name: str, unit_id: Optional[int] = None) -> int:
        """
        Obtener IdDepartamento existente o crear uno nuevo

        Args:
            department_name: Nombre del departamento
            unit_id: IdUnidadDeNegocio (opcional)

        Returns:
            IdDepartamento (INT)
        """
        if not department_name:
            return None

        # Buscar departamento existente
        self.cursor.execute("""
            SELECT IdDepartamento
            FROM dbo.Instituto_Departamento
            WHERE NombreDepartamento = ?
        """, (department_name,))

        result = self.cursor.fetchone()
        if result:
            return result[0]

        # No existe, crear nuevo
        self.cursor.execute("""
            INSERT INTO dbo.Instituto_Departamento (NombreDepartamento, IdUnidadDeNegocio)
            VALUES (?, ?)
        """, (department_name, unit_id))

        self.conn.commit()

        # Obtener ID del nuevo departamento
        self.cursor.execute("SELECT @@IDENTITY")
        new_id = self.cursor.fetchone()[0]

        self.stats['departamentos_creados'] += 1

        return new_id

    def get_user_id_by_userid(self, user_id: str) -> Optional[int]:
        """
        Obtener ID interno del usuario por UserId

        Args:
            user_id: UserId (string, ej. "U001")

        Returns:
            ID interno (INT) o None si no existe
        """
        self.cursor.execute("""
            SELECT Id
            FROM dbo.Instituto_Usuario
            WHERE UserId = ?
        """, (user_id,))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_or_create_user(self, user_id: str, user_name: str = None, user_email: str = None) -> int:
        """
        Obtener ID interno del usuario o crearlo si no existe

        Args:
            user_id: UserId (string)
            user_name: Nombre del usuario (opcional)
            user_email: Email del usuario (opcional)

        Returns:
            ID interno (INT)
        """
        # Intentar obtener usuario existente
        internal_id = self.get_user_id_by_userid(user_id)
        if internal_id:
            return internal_id

        # No existe, crear nuevo usuario
        self.cursor.execute("""
            INSERT INTO dbo.Instituto_Usuario (UserId, UserName, UserEmail, Activo)
            VALUES (?, ?, ?, 1)
        """, (user_id, user_name or user_id, user_email))

        self.conn.commit()

        # Obtener ID del nuevo usuario
        self.cursor.execute("SELECT @@IDENTITY")
        new_id = self.cursor.fetchone()[0]

        self.stats['usuarios_creados'] += 1

        return new_id

    def get_inscripcion_id(self, user_id_interno: int, module_id: int) -> Optional[int]:
        """
        Obtener IdInscripcion (IdProgresoModulo) por usuario y módulo

        Args:
            user_id_interno: ID interno del usuario
            module_id: ID del módulo

        Returns:
            IdInscripcion o None
        """
        self.cursor.execute("""
            SELECT IdInscripcion
            FROM dbo.Instituto_ProgresoModulo
            WHERE UserId = ? AND IdModulo = ?
        """, (user_id_interno, module_id))

        result = self.cursor.fetchone()
        return result[0] if result else None

    # ==================== FUNCIONES DE SINCRONIZACIÓN ====================

    def sync_transcript_data(self, excel_path: str, sheet_name: str = 0) -> Dict:
        """
        Sincronizar datos de transcripciones desde Excel

        Mapeo de columnas:
        - "Identificación de usuario" -> dbo.Instituto_Usuario.UserId
        - "Título de la capacitación" -> dbo.Instituto_Modulo.NombreModulo
        - "Estado del expediente" -> dbo.Instituto_ProgresoModulo.EstatusModulo
        - "Fecha de registro de la transcripción" -> dbo.Instituto_ProgresoModulo.FechaAsignacion
        - "Fecha de finalización del expediente" -> dbo.Instituto_ProgresoModulo.FechaFinalizacion

        Args:
            excel_path: Ruta al archivo Excel
            sheet_name: Nombre o índice de la hoja (default: 0)

        Returns:
            Diccionario con estadísticas del proceso
        """
        try:
            # Leer Excel
            df = pd.read_excel(excel_path, sheet_name=sheet_name)

            # Mapeo de columnas (flexibles para diferentes formatos)
            col_map = {
                'user_id': None,
                'training_title': None,
                'status': None,
                'fecha_registro': None,
                'fecha_finalizacion': None
            }

            # Detectar columnas
            for col in df.columns:
                col_lower = str(col).lower()
                if 'identificaci' in col_lower and 'usuario' in col_lower:
                    col_map['user_id'] = col
                elif 't' in col_lower[0] and 'capacitaci' in col_lower:
                    col_map['training_title'] = col
                elif 'estado' in col_lower and 'expediente' in col_lower:
                    col_map['status'] = col
                elif 'fecha' in col_lower and 'registro' in col_lower:
                    col_map['fecha_registro'] = col
                elif 'fecha' in col_lower and 'finalizaci' in col_lower:
                    col_map['fecha_finalizacion'] = col

            # Validar que se encontraron las columnas necesarias
            if not col_map['user_id'] or not col_map['training_title']:
                raise ValueError("No se encontraron las columnas necesarias en el Excel")

            # Procesar cada fila
            for idx, row in df.iterrows():
                try:
                    user_id = str(row[col_map['user_id']]).strip()
                    training_title = str(row[col_map['training_title']]).strip()
                    status = str(row[col_map['status']]) if col_map['status'] else 'Registrado'

                    if not user_id or not training_title or user_id == 'nan':
                        continue

                    # Obtener o crear usuario
                    user_internal_id = self.get_or_create_user(user_id)

                    # Parsear número de módulo
                    module_number = self.parse_module_number(training_title)

                    # Obtener o crear módulo
                    module_id = self.get_or_create_module(training_title, module_number)

                    # Normalizar estado
                    normalized_status = self.normalize_status(status)

                    # Parsear fechas
                    fecha_asignacion = None
                    fecha_finalizacion = None

                    if col_map['fecha_registro']:
                        fecha_asignacion = self.parse_date(row[col_map['fecha_registro']])

                    if col_map['fecha_finalizacion']:
                        fecha_finalizacion = self.parse_date(row[col_map['fecha_finalizacion']])

                    # UPSERT en ProgresoModulo
                    self._upsert_progreso_modulo(
                        user_id=user_internal_id,
                        module_id=module_id,
                        status=normalized_status,
                        fecha_asignacion=fecha_asignacion,
                        fecha_finalizacion=fecha_finalizacion
                    )

                except Exception as e:
                    error_msg = f"Fila {idx + 2}: {str(e)}"
                    self.stats['errores'].append(error_msg)
                    print(f"Error procesando fila {idx + 2}: {e}")

            # Commit final
            self.conn.commit()

            return self.stats

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error sincronizando transcripciones: {str(e)}")

    def sync_scores_data(self, excel_path: str, sheet_name: str = 0) -> Dict:
        """
        Sincronizar datos de puntuaciones desde Excel

        Mapeo de columnas:
        - "Identificación de usuario" -> dbo.Instituto_Usuario.UserId
        - "Título de la capacitación" -> dbo.Instituto_Modulo.NombreModulo
        - "Puntuación de la transcripción" -> dbo.Instituto_ResultadoEvaluacion.PuntajeObtenido
        - "Estado del expediente" (Fallo/Fallido) -> dbo.Instituto_ResultadoEvaluacion.Aprobado = 0

        Args:
            excel_path: Ruta al archivo Excel
            sheet_name: Nombre o índice de la hoja

        Returns:
            Diccionario con estadísticas
        """
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)

            # Detectar columnas
            col_map = {
                'user_id': None,
                'training_title': None,
                'score': None,
                'status': None
            }

            for col in df.columns:
                col_lower = str(col).lower()
                if 'identificaci' in col_lower and 'usuario' in col_lower:
                    col_map['user_id'] = col
                elif 't' in col_lower[0] and 'capacitaci' in col_lower:
                    col_map['training_title'] = col
                elif 'puntuaci' in col_lower or 'score' in col_lower:
                    col_map['score'] = col
                elif 'estado' in col_lower:
                    col_map['status'] = col

            # Procesar filas
            for idx, row in df.iterrows():
                try:
                    user_id = str(row[col_map['user_id']]).strip()
                    training_title = str(row[col_map['training_title']]).strip()

                    if not user_id or not training_title or user_id == 'nan':
                        continue

                    # Obtener IDs
                    user_internal_id = self.get_or_create_user(user_id)
                    module_id = self.get_or_create_module(training_title)

                    # Obtener IdInscripcion
                    inscripcion_id = self.get_inscripcion_id(user_internal_id, module_id)
                    if not inscripcion_id:
                        # Crear inscripción si no existe
                        self._upsert_progreso_modulo(user_internal_id, module_id, 'Registrado')
                        inscripcion_id = self.get_inscripcion_id(user_internal_id, module_id)

                    # Parsear puntuación
                    score = None
                    if col_map['score'] and not pd.isna(row[col_map['score']]):
                        try:
                            score = float(row[col_map['score']])
                        except:
                            pass

                    # Determinar aprobación
                    status = str(row[col_map['status']]) if col_map['status'] else ''
                    aprobado = 0 if 'fall' in status.lower() else 1

                    # Insertar evaluación
                    if score is not None:
                        self._insert_evaluacion(inscripcion_id, score, aprobado)

                except Exception as e:
                    error_msg = f"Fila {idx + 2}: {str(e)}"
                    self.stats['errores'].append(error_msg)

            self.conn.commit()
            return self.stats

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error sincronizando puntuaciones: {str(e)}")

    def sync_user_data(self, excel_path: str, sheet_name: str = 0) -> Dict:
        """
        Sincronizar datos de usuario (actualizar email, departamento, cargo, ubicación)

        Mapeo de columnas:
        - "Identificación de usuario" -> dbo.Instituto_Usuario.UserId
        - "Usuario - Correo electrónico del usuario" -> dbo.Instituto_Usuario.UserEmail
        - "Usuario - Departamento" -> dbo.Instituto_Departamento.NombreDepartamento
        - "Usuario - Cargo" -> dbo.Instituto_Usuario.Position
        - "Usuario - Ubicación" -> dbo.Instituto_Usuario.Ubicacion

        Args:
            excel_path: Ruta al archivo Excel
            sheet_name: Nombre o índice de la hoja

        Returns:
            Diccionario con estadísticas
        """
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)

            # Detectar columnas
            col_map = {
                'user_id': None,
                'email': None,
                'department': None,
                'position': None,
                'location': None
            }

            for col in df.columns:
                col_lower = str(col).lower()
                if 'identificaci' in col_lower and 'usuario' in col_lower:
                    col_map['user_id'] = col
                elif 'correo' in col_lower or 'email' in col_lower:
                    col_map['email'] = col
                elif 'departamento' in col_lower or 'department' in col_lower:
                    col_map['department'] = col
                elif 'cargo' in col_lower or 'position' in col_lower:
                    col_map['position'] = col
                elif 'ubicaci' in col_lower or 'location' in col_lower:
                    col_map['location'] = col

            # Procesar filas
            for idx, row in df.iterrows():
                try:
                    user_id = str(row[col_map['user_id']]).strip()

                    if not user_id or user_id == 'nan':
                        continue

                    # Obtener o crear usuario
                    user_internal_id = self.get_or_create_user(user_id)

                    # Obtener valores
                    email = str(row[col_map['email']]) if col_map['email'] and not pd.isna(row[col_map['email']]) else None
                    department = str(row[col_map['department']]) if col_map['department'] and not pd.isna(row[col_map['department']]) else None
                    position = str(row[col_map['position']]) if col_map['position'] and not pd.isna(row[col_map['position']]) else None
                    location = str(row[col_map['location']]) if col_map['location'] and not pd.isna(row[col_map['location']]) else None

                    # Obtener o crear departamento
                    id_departamento = None
                    if department:
                        id_departamento = self.get_or_create_department(department)

                    # Actualizar usuario
                    self.cursor.execute("""
                        UPDATE dbo.Instituto_Usuario
                        SET UserEmail = COALESCE(?, UserEmail),
                            IdDepartamento = COALESCE(?, IdDepartamento),
                            Position = COALESCE(?, Position),
                            Ubicacion = COALESCE(?, Ubicacion)
                        WHERE Id = ?
                    """, (email, id_departamento, position, location, user_internal_id))

                    if self.cursor.rowcount > 0:
                        self.stats['usuarios_actualizados'] += 1

                except Exception as e:
                    error_msg = f"Fila {idx + 2}: {str(e)}"
                    self.stats['errores'].append(error_msg)

            self.conn.commit()
            return self.stats

        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error sincronizando datos de usuario: {str(e)}")

    # ==================== FUNCIONES AUXILIARES PRIVADAS ====================

    def _upsert_progreso_modulo(
        self,
        user_id: int,
        module_id: int,
        status: str,
        fecha_asignacion: Optional[datetime] = None,
        fecha_finalizacion: Optional[datetime] = None,
        fecha_vencimiento: Optional[datetime] = None
    ):
        """
        Insertar o actualizar registro en dbo.Instituto_ProgresoModulo

        Usa UNIQUE KEY (UserId, IdModulo) para hacer UPSERT
        """
        # Verificar si ya existe
        self.cursor.execute("""
            SELECT IdInscripcion
            FROM dbo.Instituto_ProgresoModulo
            WHERE UserId = ? AND IdModulo = ?
        """, (user_id, module_id))

        existing = self.cursor.fetchone()

        if existing:
            # Actualizar
            update_query = """
                UPDATE dbo.Instituto_ProgresoModulo
                SET EstatusModulo = ?
            """
            params = [status]

            if fecha_asignacion:
                update_query += ", FechaAsignacion = ?"
                params.append(fecha_asignacion)

            if fecha_finalizacion:
                update_query += ", FechaFinalizacion = ?"
                params.append(fecha_finalizacion)

            if fecha_vencimiento:
                update_query += ", FechaVencimiento = ?"
                params.append(fecha_vencimiento)

            update_query += " WHERE IdInscripcion = ?"
            params.append(existing[0])

            self.cursor.execute(update_query, params)
            self.stats['inscripciones_actualizadas'] += 1
        else:
            # Insertar
            self.cursor.execute("""
                INSERT INTO dbo.Instituto_ProgresoModulo
                (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaFinalizacion, FechaVencimiento)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, module_id, status, fecha_asignacion, fecha_finalizacion, fecha_vencimiento))

            self.stats['inscripciones_creadas'] += 1

    def _insert_evaluacion(self, inscripcion_id: int, puntaje: float, aprobado: int):
        """
        Insertar resultado de evaluación
        """
        try:
            # Verificar si ya existe una evaluación
            self.cursor.execute("""
                SELECT IdResultado
                FROM dbo.Instituto_ResultadoEvaluacion
                WHERE IdInscripcion = ?
            """, (inscripcion_id,))

            if self.cursor.fetchone():
                # Ya existe, actualizar
                self.cursor.execute("""
                    UPDATE dbo.Instituto_ResultadoEvaluacion
                    SET PuntajeObtenido = ?,
                        Aprobado = ?
                    WHERE IdInscripcion = ?
                """, (puntaje, aprobado, inscripcion_id))
            else:
                # No existe, insertar
                self.cursor.execute("""
                    INSERT INTO dbo.Instituto_ResultadoEvaluacion
                    (IdInscripcion, PuntajeObtenido, Aprobado, FechaEvaluacion)
                    VALUES (?, ?, ?, GETDATE())
                """, (inscripcion_id, puntaje, aprobado))

                self.stats['evaluaciones_creadas'] += 1

        except Exception as e:
            print(f"Error insertando evaluación: {e}")

    def process_multiple_excels(self, files: List[Dict[str, str]]) -> Dict:
        """
        Procesar múltiples archivos Excel en una transacción

        Args:
            files: Lista de diccionarios con 'path' y 'type' de cada archivo
                   Tipos: 'transcripts', 'scores', 'users', 'expirations'

        Returns:
            Estadísticas consolidadas
        """
        try:
            for file_info in files:
                file_path = file_info['path']
                file_type = file_info['type']

                print(f"Procesando {file_type}: {file_path}")

                if file_type == 'transcripts':
                    self.sync_transcript_data(file_path)
                elif file_type == 'scores':
                    self.sync_scores_data(file_path)
                elif file_type == 'users':
                    self.sync_user_data(file_path)
                # Agregar más tipos según necesites

            # Commit final de toda la transacción
            self.conn.commit()

            print("\n=== RESUMEN DE SINCRONIZACIÓN ===")
            print(f"Usuarios creados: {self.stats['usuarios_creados']}")
            print(f"Usuarios actualizados: {self.stats['usuarios_actualizados']}")
            print(f"Módulos creados: {self.stats['modulos_creados']}")
            print(f"Inscripciones creadas: {self.stats['inscripciones_creadas']}")
            print(f"Inscripciones actualizadas: {self.stats['inscripciones_actualizadas']}")
            print(f"Evaluaciones creadas: {self.stats['evaluaciones_creadas']}")
            print(f"Departamentos creados: {self.stats['departamentos_creados']}")
            print(f"Errores: {len(self.stats['errores'])}")

            if self.stats['errores']:
                print("\nPrimeros 10 errores:")
                for error in self.stats['errores'][:10]:
                    print(f"  - {error}")

            return self.stats

        except Exception as e:
            # Rollback en caso de error
            self.conn.rollback()
            raise Exception(f"Error en proceso de sincronización: {str(e)}")
