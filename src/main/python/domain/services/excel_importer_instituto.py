"""
Importador de Excel CSOD para estructura Instituto Hutchison Ports
Soporta: MySQL (implementado) y SQL Server (queries adaptadas)

Basado en documentación: docs/MAPEO_COLUMNAS_EXCEL_BD.md
"""
import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class ExcelImporterInstituto:
    """
    Importador de Excel CSOD para base de datos instituto_*

    Soporta 2 tipos de reportes:
    1. Training Report (Progreso y Calificaciones)
    2. Org Planning (Datos de Usuarios)
    """

    # Mapeo de nombres de módulos normalizados
    MODULOS_MAPPING = {
        1: "MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS",
        2: "MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO",
        3: "MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES",
        4: "MÓDULO 4 . RELACIONES LABORALES",
        5: "MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES",
        6: "MÓDULO 6 . CIBERSEGURIDAD",
        7: "MÓDULO 7 . ENTORNO LABORAL SALUDABLE",
        8: "MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS",
        9: "MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL",
        10: "MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS",
        11: "MÓDULO 11 . PRODUCTOS DIGITALES DE HP",
        12: "MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD",
        13: "MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA",
        14: "MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA"
    }

    # Variaciones de columnas (Español/Inglés)
    COLUMN_VARIATIONS = {
        'training_title': [
            'Título de la capacitación',
            'Training Title',
            'Course Title',
            'Title'
        ],
        'user_id': [
            'Identificación de usuario',
            'User ID',
            'User Identification',
            'ID'
        ],
        'record_status': [
            'Estado del expediente',
            'Record Status',
            'Completion Status',
            'Status'
        ],
        'transcript_date': [
            'Fecha de registro de la transcripción',
            'Transcript Registration Date',
            'Registration Date'
        ],
        'start_date': [
            'Fecha de inicio de la capacitación',
            'Training Start Date',
            'Start Date'
        ],
        'completion_date': [
            'Fecha de finalización de expediente',
            'Record Completion Date',
            'Completion Date',
            'Finished Date'
        ],
        'training_type': [
            'Tipo de capacitación',
            'Training Type',
            'Content Type',
            'Type'
        ],
        'score': [
            'Puntuación de la transcripción',
            'Transcript Score',
            'Score',
            'Grade'
        ],
        'department': [
            'Departamento',
            'Department',
            'Organization'
        ],
        'position': [
            'Cargo',
            'Position',
            'Job Title'
        ],
        'full_name': [
            'Nombre completo del usuario',
            'User - Full Name',
            'Full Name',
            'Name'
        ],
        'email': [
            'Correo electrónico del usuario',
            'User - Email Address',
            'Email',
            'E-mail'
        ],
        'business_unit': [
            'División',
            'Unidad de negocio',
            'User - Division',
            'Business Unit',
            'Division'
        ],
        'location': [
            'Ubicación',
            'User - Location',
            'Location',
            'Site'
        ],
        'level': [
            'Nivel',
            'User - Level',
            'Level'
        ]
    }

    def __init__(self, db_manager):
        """
        Args:
            db_manager: Instancia de DatabaseManager o InstitutoSmartReportsDB
        """
        self.db = db_manager
        self.detected_columns = {}
        self.stats = {
            'usuarios_nuevos': 0,
            'usuarios_actualizados': 0,
            'progresos_actualizados': 0,
            'calificaciones_registradas': 0,
            'modulos_creados': 0,
            'errores': []
        }

        # Caché para evitar N+1 queries
        self._modulos_cache = None
        self._unidades_cache = None
        self._departamentos_cache = None
        self._usuarios_cache = None
        self._evaluaciones_cache = None

    # =========================================================================
    # DETECCIÓN Y LECTURA DE EXCEL
    # =========================================================================

    def _leer_excel_con_deteccion_headers(self, archivo_excel: str) -> pd.DataFrame:
        """
        Lee Excel detectando automáticamente dónde están los headers reales

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            DataFrame con los datos
        """
        try:
            # Intentar lectura normal
            df = pd.read_excel(archivo_excel)

            # Verificar si los headers son válidos
            if any('Unnamed' in str(col) for col in df.columns):
                logger.warning("⚠️  Headers no detectados en fila 0, buscando headers reales...")

                # Buscar headers reales en las primeras 5 filas
                for skip_rows in range(1, 6):
                    df_test = pd.read_excel(archivo_excel, skiprows=skip_rows)

                    # Verificar si encontramos columnas conocidas
                    cols_str = ' '.join(str(c).lower() for c in df_test.columns)
                    if 'usuario' in cols_str or 'user' in cols_str or 'módulo' in cols_str or 'training' in cols_str:
                        logger.info(f"  ✓ Headers encontrados en fila {skip_rows}")
                        return df_test

                logger.warning("  ⚠️ No se pudieron detectar headers automáticamente")
                return df

            return df

        except Exception as e:
            logger.error(f"❌ Error leyendo Excel: {e}")
            raise

    def _detectar_columnas(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Detecta automáticamente las columnas del Excel (Español/Inglés)

        Args:
            df: DataFrame de pandas

        Returns:
            Diccionario con columnas detectadas
        """
        self.detected_columns = {}

        columnas_excel = df.columns.tolist()

        for key, variations in self.COLUMN_VARIATIONS.items():
            for variation in variations:
                for col_excel in columnas_excel:
                    if variation.lower() in str(col_excel).lower():
                        self.detected_columns[key] = col_excel
                        break
                if key in self.detected_columns:
                    break

        logger.info(f"✅ Columnas detectadas: {len(self.detected_columns)}/{len(self.COLUMN_VARIATIONS)}")

        # Mostrar columnas no detectadas
        no_detectadas = set(self.COLUMN_VARIATIONS.keys()) - set(self.detected_columns.keys())
        if no_detectadas:
            logger.warning(f"⚠️  Columnas no encontradas: {', '.join(no_detectadas)}")

        return self.detected_columns

    # =========================================================================
    # PRECARGA DE DATOS (Optimización)
    # =========================================================================

    def _precargar_modulos(self) -> Dict[str, int]:
        """Precarga módulos en memoria para evitar N queries"""
        if self._modulos_cache is not None:
            return self._modulos_cache

        query = "SELECT IdModulo, NombreModulo FROM instituto_Modulo WHERE Activo = 1"
        resultados = self.db.db.execute_query(query, fetch_all=True)

        self._modulos_cache = {}
        for row in resultados:
            self._modulos_cache[row['NombreModulo']] = row['IdModulo']

        logger.info(f"✅ Módulos precargados: {len(self._modulos_cache)}")
        return self._modulos_cache

    def _precargar_unidades_negocio(self) -> Dict[str, int]:
        """Precarga unidades de negocio"""
        if self._unidades_cache is not None:
            return self._unidades_cache

        query = "SELECT IdUnidadDeNegocio, NombreUnidad FROM instituto_UnidadDeNegocio WHERE Activo = 1"
        resultados = self.db.db.execute_query(query, fetch_all=True)

        self._unidades_cache = {}
        for row in resultados:
            self._unidades_cache[row['NombreUnidad']] = row['IdUnidadDeNegocio']

        logger.info(f"✅ Unidades de negocio precargadas: {len(self._unidades_cache)}")
        return self._unidades_cache

    def _precargar_departamentos(self) -> Dict[Tuple[int, str], int]:
        """Precarga departamentos con clave (IdUnidad, NombreDepto)"""
        if self._departamentos_cache is not None:
            return self._departamentos_cache

        query = """
            SELECT IdDepartamento, IdUnidadDeNegocio, NombreDepartamento
            FROM instituto_Departamento
            WHERE Activo = 1
        """
        resultados = self.db.db.execute_query(query, fetch_all=True)

        self._departamentos_cache = {}
        for row in resultados:
            key = (row['IdUnidadDeNegocio'], row['NombreDepartamento'])
            self._departamentos_cache[key] = row['IdDepartamento']

        logger.info(f"✅ Departamentos precargados: {len(self._departamentos_cache)}")
        return self._departamentos_cache

    def _precargar_usuarios(self, user_ids: List[str]) -> Dict[str, int]:
        """
        Precarga usuarios existentes

        Args:
            user_ids: Lista de UserIds a precargar

        Returns:
            Dict {UserId: IdUsuario}
        """
        if not user_ids:
            return {}

        # Crear placeholders para IN clause
        placeholders = ','.join(['%s'] * len(user_ids))
        query = f"""
            SELECT IdUsuario, UserId
            FROM instituto_Usuario
            WHERE UserId IN ({placeholders})
        """

        resultados = self.db.db.execute_query(query, tuple(user_ids), fetch_all=True)

        usuarios_cache = {}
        for row in resultados:
            usuarios_cache[row['UserId']] = row['IdUsuario']

        logger.info(f"✅ Usuarios precargados: {len(usuarios_cache)}")
        return usuarios_cache

    def _precargar_progresos_existentes(self, user_ids: List[str]) -> Dict[Tuple[str, int], int]:
        """
        Precarga progresos existentes

        Args:
            user_ids: Lista de UserIds

        Returns:
            Dict {(UserId, IdModulo): IdInscripcion}
        """
        if not user_ids:
            return {}

        placeholders = ','.join(['%s'] * len(user_ids))
        query = f"""
            SELECT UserId, IdModulo, IdInscripcion
            FROM instituto_ProgresoModulo
            WHERE UserId IN ({placeholders})
        """

        resultados = self.db.db.execute_query(query, tuple(user_ids), fetch_all=True)

        progresos_cache = {}
        for row in resultados:
            key = (row['UserId'], row['IdModulo'])
            progresos_cache[key] = row['IdInscripcion']

        logger.info(f"✅ Progresos existentes precargados: {len(progresos_cache)}")
        return progresos_cache

    # =========================================================================
    # NORMALIZACIÓN Y UTILIDADES
    # =========================================================================

    def _normalizar_nombre_modulo(self, titulo: str) -> Optional[int]:
        """
        Extrae el número de módulo del título

        Args:
            titulo: Título del módulo (ej: "MÓDULO 8 - PROCESOS DE RRHH")

        Returns:
            Número del módulo (1-14) o None
        """
        if not titulo or pd.isna(titulo):
            return None

        # Buscar "MÓDULO X" o "MODULE X"
        match = re.search(r'M[OÓ]DULO\s+(\d+)', str(titulo), re.IGNORECASE)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 14:
                return num

        return None

    def _normalizar_estatus(self, estatus_excel: str) -> str:
        """
        Normaliza el estado del Excel al formato de la BD

        Args:
            estatus_excel: Estado del Excel

        Returns:
            Estado normalizado
        """
        mapeo = {
            'terminado': 'Terminado',
            'completado': 'Terminado',
            'completed': 'Terminado',
            'en progreso': 'En progreso',
            'in progress': 'En progreso',
            'registrado': 'Registrado',
            'registered': 'Registrado',
            'no iniciado': 'No iniciado',
            'not started': 'No iniciado'
        }

        estatus_lower = str(estatus_excel).lower() if estatus_excel else ''

        for key, value in mapeo.items():
            if key in estatus_lower:
                return value

        return 'No iniciado'

    def _calcular_porcentaje_por_estado(self, estatus: str) -> int:
        """
        Calcula el porcentaje de avance según el estado

        Args:
            estatus: Estado normalizado

        Returns:
            Porcentaje (0-100)
        """
        mapeo = {
            'Terminado': 100,
            'En progreso': 50,  # Puede ajustarse según lógica
            'Registrado': 0,
            'No iniciado': 0
        }

        return mapeo.get(estatus, 0)

    def _parse_fecha(self, fecha_str) -> Optional[datetime]:
        """
        Parsea fecha de múltiples formatos

        Args:
            fecha_str: String de fecha o objeto datetime

        Returns:
            datetime o None
        """
        if pd.isna(fecha_str) or not fecha_str:
            return None

        # Si ya es datetime
        if isinstance(fecha_str, datetime):
            return fecha_str

        # Intentar múltiples formatos
        formatos = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y'
        ]

        fecha_str = str(fecha_str).strip()

        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except:
                continue

        logger.warning(f"⚠️  No se pudo parsear fecha: {fecha_str}")
        return None

    # =========================================================================
    # IMPORTACIÓN TRAINING REPORT
    # =========================================================================

    def importar_training_report(self, archivo_excel: str) -> Dict[str, Any]:
        """
        Importa Enterprise Training Report (Progreso y Calificaciones)

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            Estadísticas de la importación
        """
        logger.info("="*70)
        logger.info("📊 IMPORTANDO TRAINING REPORT")
        logger.info("="*70)

        # 1. Leer Excel
        logger.info("\n📖 Leyendo archivo Excel...")
        df = self._leer_excel_con_deteccion_headers(archivo_excel)
        logger.info(f"  ✓ Registros leídos: {len(df)}")

        # 2. Detectar columnas
        logger.info("\n🔍 Detectando columnas...")
        self._detectar_columnas(df)

        # 3. Procesar módulos
        self._procesar_modulos(df)

        # 4. Procesar calificaciones
        self._procesar_calificaciones(df)

        # 5. Commit
        self.db.db.get_connection().commit()

        logger.info("\n" + "="*70)
        logger.info("✅ IMPORTACIÓN COMPLETADA")
        self._mostrar_estadisticas()

        return self.stats

    def _procesar_modulos(self, df: pd.DataFrame):
        """Procesa registros de progreso de módulos"""
        logger.info("\n📋 Procesando progreso de módulos...")

        # Verificar columnas necesarias
        if 'training_title' not in self.detected_columns:
            logger.warning("  ⚠️ Columna de título no encontrada")
            return

        col_titulo = self.detected_columns['training_title']

        # Filtrar solo módulos
        df_modulos = df[df[col_titulo].str.contains('MÓDULO', case=False, na=False)].copy()

        if len(df_modulos) == 0:
            logger.info("  ℹ️  No se encontraron módulos")
            return

        logger.info(f"  📊 Registros de módulos: {len(df_modulos)}")

        # Precargar datos
        modulos_map = self._precargar_modulos()
        user_ids = df_modulos[self.detected_columns['user_id']].astype(str).str.strip().unique().tolist()
        progresos_existentes = self._precargar_progresos_existentes(user_ids)

        # Preparar batch operations
        registros_update = []
        registros_insert = []

        for idx, row in df_modulos.iterrows():
            try:
                user_id = str(row[self.detected_columns['user_id']]).strip()
                titulo = row[col_titulo]
                estado_excel = row.get(self.detected_columns.get('record_status', ''), '')

                # Parsear fechas
                fecha_inicio = self._parse_fecha(row.get(self.detected_columns.get('start_date', '')))
                fecha_fin = self._parse_fecha(row.get(self.detected_columns.get('completion_date', '')))
                fecha_registro = self._parse_fecha(row.get(self.detected_columns.get('transcript_date', '')))

                # Identificar módulo
                num_modulo = self._normalizar_nombre_modulo(titulo)
                if not num_modulo:
                    continue

                nombre_modulo = self.MODULOS_MAPPING.get(num_modulo)
                id_modulo = modulos_map.get(nombre_modulo)

                if not id_modulo:
                    logger.warning(f"  ⚠️ Módulo no encontrado: {nombre_modulo}")
                    continue

                # Calcular estado y porcentaje
                estado = self._normalizar_estatus(estado_excel)
                porcentaje = self._calcular_porcentaje_por_estado(estado)

                # Verificar si existe
                key = (user_id, id_modulo)
                if key in progresos_existentes:
                    # UPDATE
                    registros_update.append((
                        estado,
                        fecha_inicio or fecha_registro,
                        fecha_fin,
                        porcentaje,
                        user_id,
                        id_modulo
                    ))
                else:
                    # INSERT
                    registros_insert.append((
                        user_id,
                        id_modulo,
                        estado,
                        fecha_inicio or fecha_registro or datetime.now(),
                        fecha_fin,
                        porcentaje,
                        datetime.now()
                    ))

            except Exception as e:
                self.stats['errores'].append(f"Error en fila {idx}: {e}")
                logger.error(f"  ❌ Error en fila {idx}: {e}")

        # Ejecutar batch operations
        connection = self.db.db.get_connection()
        cursor = connection.cursor()

        if registros_update:
            cursor.executemany("""
                UPDATE instituto_ProgresoModulo
                SET EstatusModulo = %s,
                    FechaInicio = COALESCE(%s, FechaInicio),
                    FechaFinalizacion = %s,
                    PorcentajeAvance = %s
                WHERE UserId = %s AND IdModulo = %s
            """, registros_update)
            self.stats['progresos_actualizados'] += len(registros_update)
            logger.info(f"  ✅ Actualizados: {len(registros_update)}")

        if registros_insert:
            cursor.executemany("""
                INSERT INTO instituto_ProgresoModulo
                (UserId, IdModulo, EstatusModulo, FechaInicio, FechaFinalizacion,
                 PorcentajeAvance, FechaAsignacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, registros_insert)
            self.stats['progresos_actualizados'] += len(registros_insert)
            logger.info(f"  ✅ Insertados: {len(registros_insert)}")

        cursor.close()

    def _procesar_calificaciones(self, df: pd.DataFrame):
        """Procesa calificaciones de evaluaciones"""
        logger.info("\n📝 Procesando calificaciones...")

        # Verificar columnas necesarias
        if 'training_type' not in self.detected_columns or 'score' not in self.detected_columns:
            logger.warning("  ⚠️ Columnas necesarias no encontradas")
            return

        col_tipo = self.detected_columns['training_type']
        col_puntaje = self.detected_columns['score']

        # Filtrar solo pruebas/evaluaciones
        df_pruebas = df[
            df[col_tipo].str.contains('Prueba|Test|Assessment|Exam', case=False, na=False)
        ].copy()

        if len(df_pruebas) == 0:
            logger.info("  ℹ️  No se encontraron evaluaciones")
            return

        logger.info(f"  📊 Calificaciones a procesar: {len(df_pruebas)}")

        # Precargar datos
        modulos_map = self._precargar_modulos()
        user_ids = df_pruebas[self.detected_columns['user_id']].astype(str).str.strip().unique().tolist()
        progresos_cache = self._precargar_progresos_existentes(user_ids)

        # Preparar batch
        calificaciones_batch = []

        connection = self.db.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        for idx, row in df_pruebas.iterrows():
            try:
                user_id = str(row[self.detected_columns['user_id']]).strip()
                titulo = row[self.detected_columns['training_title']]
                puntuacion = row.get(col_puntaje)

                if pd.isna(puntuacion):
                    continue

                try:
                    puntaje_decimal = float(puntuacion)
                except:
                    continue

                # Identificar módulo
                num_modulo = self._normalizar_nombre_modulo(titulo)
                if not num_modulo:
                    continue

                nombre_modulo = self.MODULOS_MAPPING.get(num_modulo)
                id_modulo = modulos_map.get(nombre_modulo)

                if not id_modulo:
                    continue

                # Obtener IdInscripcion
                key = (user_id, id_modulo)
                id_inscripcion = progresos_cache.get(key)

                if not id_inscripcion:
                    logger.warning(f"  ⚠️ No se encontró inscripción para {user_id} - Módulo {id_modulo}")
                    continue

                # Buscar IdEvaluacion
                cursor.execute("""
                    SELECT IdEvaluacion, PuntajeMinimoAprobatorio
                    FROM instituto_Evaluacion
                    WHERE IdModulo = %s AND Activo = 1
                    LIMIT 1
                """, (id_modulo,))

                evaluacion = cursor.fetchone()

                if not evaluacion:
                    # Crear evaluación por defecto
                    cursor.execute("""
                        INSERT INTO instituto_Evaluacion
                        (IdModulo, NombreEvaluacion, PuntajeMinimoAprobatorio, Activo)
                        VALUES (%s, %s, 70.00, 1)
                    """, (id_modulo, f"Evaluación {nombre_modulo}"))

                    id_evaluacion = cursor.lastrowid
                    puntaje_minimo = 70.00
                else:
                    id_evaluacion = evaluacion['IdEvaluacion']
                    puntaje_minimo = evaluacion['PuntajeMinimoAprobatorio']

                # Determinar si aprobó
                aprobado = 1 if puntaje_decimal >= puntaje_minimo else 0

                # Contar intentos previos
                cursor.execute("""
                    SELECT COUNT(*) as total
                    FROM instituto_ResultadoEvaluacion
                    WHERE IdInscripcion = %s AND IdEvaluacion = %s
                """, (id_inscripcion, id_evaluacion))

                intento_numero = cursor.fetchone()['total'] + 1

                # Insertar resultado
                cursor.execute("""
                    INSERT INTO instituto_ResultadoEvaluacion
                    (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado,
                     IntentoNumero, FechaRealizacion)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, (id_inscripcion, id_evaluacion, puntaje_decimal, aprobado, intento_numero))

                self.stats['calificaciones_registradas'] += 1

                # Si aprobó, actualizar progreso a Terminado
                if aprobado:
                    cursor.execute("""
                        UPDATE instituto_ProgresoModulo
                        SET EstatusModulo = 'Terminado',
                            PorcentajeAvance = 100,
                            FechaFinalizacion = NOW()
                        WHERE IdInscripcion = %s
                    """, (id_inscripcion,))

            except Exception as e:
                self.stats['errores'].append(f"Error en calificación {idx}: {e}")
                logger.error(f"  ❌ Error en calificación {idx}: {e}")

        cursor.close()
        logger.info(f"  ✅ Calificaciones registradas: {self.stats['calificaciones_registradas']}")

    # =========================================================================
    # IMPORTACIÓN ORG PLANNING
    # =========================================================================

    def importar_org_planning(self, archivo_excel: str) -> Dict[str, Any]:
        """
        Importa CSOD Org Planning (Datos de Usuarios)

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            Estadísticas de la importación
        """
        logger.info("="*70)
        logger.info("👥 IMPORTANDO ORG PLANNING (USUARIOS)")
        logger.info("="*70)

        # 1. Leer Excel
        logger.info("\n📖 Leyendo archivo Excel...")
        df = self._leer_excel_con_deteccion_headers(archivo_excel)
        logger.info(f"  ✓ Registros leídos: {len(df)}")

        # 2. Detectar columnas
        logger.info("\n🔍 Detectando columnas...")
        self._detectar_columnas(df)

        # 3. Procesar usuarios
        self._procesar_usuarios(df)

        # 4. Commit
        self.db.db.get_connection().commit()

        logger.info("\n" + "="*70)
        logger.info("✅ IMPORTACIÓN COMPLETADA")
        self._mostrar_estadisticas()

        return self.stats

    def _procesar_usuarios(self, df: pd.DataFrame):
        """Procesa usuarios del Org Planning"""
        logger.info("\n👥 Procesando usuarios...")

        # Verificar columnas mínimas
        if 'user_id' not in self.detected_columns:
            logger.error("  ❌ Columna user_id no encontrada")
            return

        logger.info(f"  📊 Usuarios a procesar: {len(df)}")

        # Precargar datos
        unidades_map = self._precargar_unidades_negocio()
        departamentos_map = self._precargar_departamentos()
        user_ids = df[self.detected_columns['user_id']].astype(str).str.strip().unique().tolist()
        usuarios_existentes = self._precargar_usuarios(user_ids)

        connection = self.db.db.get_connection()
        cursor = connection.cursor()

        # Rol por defecto: "Usuario" (IdRol = 4)
        id_rol_default = 4

        for idx, row in df.iterrows():
            try:
                user_id = str(row[self.detected_columns['user_id']]).strip()
                nombre_completo = row.get(self.detected_columns.get('full_name', ''), '')
                email = row.get(self.detected_columns.get('email', ''), '')
                cargo = row.get(self.detected_columns.get('position', ''), '')
                unidad_nombre = row.get(self.detected_columns.get('business_unit', ''), '')
                depto_nombre = row.get(self.detected_columns.get('department', ''), '')
                ubicacion = row.get(self.detected_columns.get('location', ''), '')
                nivel = row.get(self.detected_columns.get('level', ''), '')

                # Buscar/crear Unidad de Negocio
                id_unidad = None
                if unidad_nombre and not pd.isna(unidad_nombre):
                    unidad_nombre_str = str(unidad_nombre).strip()

                    if unidad_nombre_str not in unidades_map:
                        # Crear nueva unidad
                        cursor.execute("""
                            INSERT IGNORE INTO instituto_UnidadDeNegocio
                            (NombreUnidad, Codigo, Activo)
                            VALUES (%s, %s, 1)
                        """, (unidad_nombre_str, unidad_nombre_str[:20]))

                        cursor.execute("""
                            SELECT IdUnidadDeNegocio
                            FROM instituto_UnidadDeNegocio
                            WHERE NombreUnidad = %s
                        """, (unidad_nombre_str,))

                        result = cursor.fetchone()
                        if result:
                            id_unidad = result[0]
                            unidades_map[unidad_nombre_str] = id_unidad
                    else:
                        id_unidad = unidades_map[unidad_nombre_str]

                # Buscar/crear Departamento
                id_departamento = None
                if depto_nombre and not pd.isna(depto_nombre) and id_unidad:
                    depto_nombre_str = str(depto_nombre).strip()
                    key = (id_unidad, depto_nombre_str)

                    if key not in departamentos_map:
                        # Crear nuevo departamento
                        cursor.execute("""
                            INSERT IGNORE INTO instituto_Departamento
                            (IdUnidadDeNegocio, NombreDepartamento, Activo)
                            VALUES (%s, %s, 1)
                        """, (id_unidad, depto_nombre_str))

                        cursor.execute("""
                            SELECT IdDepartamento
                            FROM instituto_Departamento
                            WHERE IdUnidadDeNegocio = %s AND NombreDepartamento = %s
                        """, (id_unidad, depto_nombre_str))

                        result = cursor.fetchone()
                        if result:
                            id_departamento = result[0]
                            departamentos_map[key] = id_departamento
                    else:
                        id_departamento = departamentos_map[key]

                # Insertar o actualizar usuario
                if user_id in usuarios_existentes:
                    # UPDATE
                    cursor.execute("""
                        UPDATE instituto_Usuario
                        SET NombreCompleto = %s,
                            UserEmail = %s,
                            Position = %s,
                            IdUnidadDeNegocio = %s,
                            IdDepartamento = %s,
                            Nivel = %s,
                            Ubicacion = %s
                        WHERE UserId = %s
                    """, (nombre_completo, email, cargo, id_unidad, id_departamento,
                          nivel, ubicacion, user_id))

                    self.stats['usuarios_actualizados'] += 1
                else:
                    # INSERT
                    cursor.execute("""
                        INSERT INTO instituto_Usuario
                        (UserId, IdUnidadDeNegocio, IdDepartamento, IdRol,
                         NombreCompleto, UserEmail, Position, Nivel, Ubicacion, Activo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                    """, (user_id, id_unidad, id_departamento, id_rol_default,
                          nombre_completo, email, cargo, nivel, ubicacion))

                    self.stats['usuarios_nuevos'] += 1

            except Exception as e:
                self.stats['errores'].append(f"Error en usuario {idx}: {e}")
                logger.error(f"  ❌ Error en usuario {idx}: {e}")

        cursor.close()
        logger.info(f"  ✅ Usuarios nuevos: {self.stats['usuarios_nuevos']}")
        logger.info(f"  ✅ Usuarios actualizados: {self.stats['usuarios_actualizados']}")

    # =========================================================================
    # REPORTES Y ESTADÍSTICAS
    # =========================================================================

    def _mostrar_estadisticas(self):
        """Muestra estadísticas finales"""
        logger.info("="*70)
        logger.info("📊 ESTADÍSTICAS FINALES")
        logger.info("="*70)
        logger.info(f"  • Usuarios nuevos:             {self.stats['usuarios_nuevos']}")
        logger.info(f"  • Usuarios actualizados:       {self.stats['usuarios_actualizados']}")
        logger.info(f"  • Progresos actualizados:      {self.stats['progresos_actualizados']}")
        logger.info(f"  • Calificaciones registradas:  {self.stats['calificaciones_registradas']}")
        logger.info(f"  • Módulos creados:             {self.stats['modulos_creados']}")
        logger.info(f"  • Errores:                     {len(self.stats['errores'])}")

        if self.stats['errores']:
            logger.info("\n❌ ERRORES ENCONTRADOS:")
            for i, error in enumerate(self.stats['errores'][:10], 1):
                logger.info(f"  {i}. {error}")
            if len(self.stats['errores']) > 10:
                logger.info(f"  ... y {len(self.stats['errores']) - 10} errores más")

        logger.info("="*70)
