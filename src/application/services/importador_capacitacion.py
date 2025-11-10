"""
Servicio de Importación de Datos desde Excel - Sistema de Capacitación
Maneja el cruce de datos entre reportes CSOD y la base de datos local
"""
import pandas as pd
import os
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional
import re


class ImportadorCapacitacion:
    """
    Servicio para importar y actualizar datos de capacitación desde Excel

    Archivos soportados:
    1. Enterprise_Training_Report*.xlsx - Estatus y calificaciones
    2. CSOD_Data_Source_for_Org_Planning*.xlsx - Datos de usuarios
    """

    # ============================================================================
    # MAPEO DE COLUMNAS - SOPORTE BILINGÜE (ESPAÑOL/INGLÉS)
    # ============================================================================
    COLUMN_MAPPING = {
        # Training Report Columns
        'training_title': ['Título de la capacitación', 'Training Title', 'Course Title', 'Title'],
        'user_id': ['Identificación de usuario', 'User ID', 'User Identification', 'UserID'],
        'record_status': ['Estado del expediente', 'Record Status', 'Completion Status', 'Status'],
        'transcript_date': ['Fecha de registro de la transcripción', 'Transcript Registration Date',
                           'Registration Date', 'Transcript Date'],
        'start_date': ['Fecha de inicio de la capacitación', 'Training Start Date', 'Start Date',
                      'Commencement Date'],
        'completion_date': ['Fecha de finalización de expediente', 'Record Completion Date',
                          'Completion Date', 'Finished Date'],
        'training_type': ['Tipo de capacitación', 'Training Type', 'Type', 'Content Type'],
        'score': ['Puntuación de la transcripción', 'Transcript Score', 'Score', 'Test Score'],
        'department': ['Departamento', 'Department', 'Organization'],
        'position': ['Cargo', 'Position', 'Job Title', 'Title'],

        # Org Planning Columns
        'org_user_id': ['Usuario - Identificación de usuario', 'User - User ID', 'User ID'],
        'org_full_name': ['Usuario - Nombre completo del usuario', 'User - Full Name',
                         'User - Name', 'Full Name'],
        'org_email': ['Usuario - Correo electrónico del usuario', 'User - Email Address',
                     'User - Email', 'Email'],
        'org_position': ['Usuario - Cargo', 'User - Job Title', 'User - Position', 'Job Title'],
        'org_department': ['Usuario - Departamento', 'User - Department', 'Department'],
        'org_location': ['Usuario - Ubicación', 'User - Location', 'Location'],
        'org_city': ['Usuario - Ciudad', 'User - City', 'City'],
        'org_country': ['Usuario - País del usuario', 'User - Country', 'Country']
    }

    # Mapeo de nombres de módulos para normalización
    MODULOS_MAPPING = {
        1: {
            'titulo': 'MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS',
            'prueba': ['INTRODUCCIÓN A LA FILOSOFÍA', 'introducción a la filosofía']
        },
        2: {
            'titulo': 'MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO',
            'prueba': ['SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 'sostenibilidad, nuestro compromiso con el futuro']
        },
        3: {
            'titulo': 'MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES',
            'prueba': ['INTRODUCCIÓN A LAS OPERACIONES', 'introducción a las operaciones']
        },
        4: {
            'titulo': 'MÓDULO 4 . RELACIONES LABORALES',
            'prueba': ['RELACIONES LABORALES', 'relaciones laborales']
        },
        5: {
            'titulo': 'MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES',
            'prueba': ['Seguridad en las Operaciones', 'seguridad en las operaciones', 'SEGURIDAD EN LAS OPERACIONES']
        },
        6: {
            'titulo': 'MÓDULO 6 . CIBERSEGURIDAD',
            'prueba': ['Ciberseguridad', 'ciberseguridad', 'CIBERSEGURIDAD']
        },
        7: {
            'titulo': 'MÓDULO 7 . ENTORNO LABORAL SALUDABLE',
            'prueba': ['Entorno Laboral Saludable', 'entorno laboral saludable', 'ENTORNO LABORAL SALUDABLE']
        },
        8: {
            'titulo': 'MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS',
            'prueba': ['Procesos de Recursos Humanos', 'procesos de recursos humanos', 'PROCESOS DE RECURSOS HUMANOS']
        },
        9: {
            'titulo': 'MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL',
            'prueba': ['Programas de Bienestar Integral', 'programas de bienestar integral']
        },
        10: {
            'titulo': 'MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS',
            'prueba': ['Desarrollo de Nuevos Productos', 'desarrollo de nuevos productos']
        },
        11: {
            'titulo': 'MÓDULO 11 . PRODUCTOS DIGITALES DE HP',
            'prueba': ['Productos Digitales de HP', 'productos digitales de hp']
        },
        12: {
            'titulo': 'MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD',
            'prueba': ['Tecnología: Impulso para la Eficiencia y Productividad', 'tecnología']
        },
        13: {
            'titulo': 'MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA',
            'prueba': ['Activación de Protocolos y Brigadas de Contingencia', 'activación de protocolos']
        },
        14: {
            'titulo': 'MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA',
            'prueba': ['Sistema Integrado de Gestión de Calidad y Mejora Continua', 'sistema integrado']
        }
    }

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a la base de datos (MySQL o SQL Server)
        """
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.stats = {
            'usuarios_nuevos': 0,
            'usuarios_actualizados': 0,
            'modulos_creados': 0,
            'progresos_actualizados': 0,
            'calificaciones_registradas': 0,
            'errores': []
        }
        self.detected_columns = {}  # Almacena columnas detectadas del Excel actual

    # ============================================================================
    # UTILIDADES
    # ============================================================================

    def _leer_excel_con_deteccion_headers(self, archivo_excel: str) -> pd.DataFrame:
        """
        Lee Excel detectando automáticamente en qué fila están los headers reales.
        Los reportes CSOD a veces tienen filas de título/logo antes de los headers.

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            DataFrame con headers correctos
        """
        # Intentar leer las primeras 10 filas para detectar headers
        df_preview = pd.read_excel(archivo_excel, nrows=10)

        # Si las columnas son "Unnamed: X", los headers están en otra fila
        if any('Unnamed' in str(col) for col in df_preview.columns):
            print("⚠️  Headers no detectados en fila 0, buscando headers reales...")

            # Probar leyendo desde diferentes filas
            for skip_rows in range(1, 6):
                try:
                    df_test = pd.read_excel(archivo_excel, skiprows=skip_rows, nrows=5)

                    # Verificar si esta fila tiene headers válidos
                    # Buscar columnas conocidas de CSOD
                    columnas_test = [str(col).lower() for col in df_test.columns]
                    palabras_clave = ['training', 'user', 'title', 'status', 'título', 'usuario',
                                     'capacitación', 'department', 'departamento']

                    if any(keyword in ' '.join(columnas_test) for keyword in palabras_clave):
                        print(f"  ✓ Headers encontrados en fila {skip_rows + 1}")
                        # Leer el Excel completo saltando las filas superiores
                        return pd.read_excel(archivo_excel, skiprows=skip_rows)
                except:
                    continue

            # Si no encontramos headers, usar lectura por defecto
            print("  ⚠️ No se pudieron detectar headers automáticamente. Usando lectura por defecto.")
            return pd.read_excel(archivo_excel)
        else:
            # Headers están en la primera fila, leer normalmente
            return pd.read_excel(archivo_excel)

    def _detectar_columnas(self, df: pd.DataFrame):
        """
        Detecta qué nombres de columnas están presentes en el DataFrame
        y crea un mapeo para acceso consistente (bilingüe).

        Args:
            df: DataFrame de pandas con el Excel cargado
        """
        columnas_excel = df.columns.tolist()
        print(f"\n🔍 Columnas detectadas en Excel ({len(columnas_excel)}):")
        print(f"   {', '.join(columnas_excel[:10])}..." if len(columnas_excel) > 10 else f"   {', '.join(columnas_excel)}")

        self.detected_columns = {}

        # Para cada columna que buscamos
        for key, possible_names in self.COLUMN_MAPPING.items():
            # Buscar la primera coincidencia
            for possible_name in possible_names:
                if possible_name in columnas_excel:
                    self.detected_columns[key] = possible_name
                    break

        # Mostrar columnas detectadas
        print(f"\n✅ Columnas mapeadas:")
        for key, col_name in self.detected_columns.items():
            print(f"   • {key}: '{col_name}'")

        # Advertir sobre columnas no encontradas
        missing = [k for k in self.COLUMN_MAPPING.keys() if k not in self.detected_columns]
        if missing:
            print(f"\n⚠️  Columnas no encontradas (pueden no estar en este tipo de reporte):")
            print(f"   {', '.join(missing)}")

    def _get_column(self, df: pd.DataFrame, key: str, default=None):
        """
        Obtiene el valor de una columna usando la detección automática

        Args:
            df: DataFrame
            key: Clave del mapeo (ej: 'training_title', 'user_id')
            default: Valor por defecto si la columna no existe

        Returns:
            Serie de pandas con los valores de la columna
        """
        if key in self.detected_columns:
            return df[self.detected_columns[key]]
        return default

    def _normalizar_nombre_modulo(self, nombre: str) -> Optional[int]:
        """
        Encuentra el número de módulo basado en el nombre (case-insensitive)

        Returns:
            int: Número de módulo (1-14) o None si no se encuentra
        """
        nombre_lower = nombre.lower().strip()

        # Buscar en títulos primero
        for num_modulo, data in self.MODULOS_MAPPING.items():
            if data['titulo'].lower() in nombre_lower:
                return num_modulo

        # Buscar en nombres de pruebas
        for num_modulo, data in self.MODULOS_MAPPING.items():
            for prueba in data['prueba']:
                if prueba.lower() in nombre_lower or nombre_lower in prueba.lower():
                    return num_modulo

        return None

    def _calcular_estado_modulo(self,
                                estado_excel: str,
                                fecha_finalizacion: Optional[datetime],
                                fecha_vencimiento: Optional[datetime]) -> str:
        """
        Calcula el estado del módulo basado en datos del Excel

        Estados posibles:
        - "Terminado"
        - "En progreso"
        - "En progreso / Vencido"
        - "Registrado"
        - "Registrado / Vencido"
        - "No iniciado"
        """
        hoy = datetime.now()

        # Si está terminado, siempre es "Terminado"
        if estado_excel and estado_excel.lower() == 'terminado':
            return 'Terminado'

        # Si tiene fecha de finalización, está terminado
        if fecha_finalizacion:
            return 'Terminado'

        # Verificar si está vencido
        esta_vencido = fecha_vencimiento and fecha_vencimiento < hoy

        # Si el estado es "En progreso" o similar
        if estado_excel and ('progreso' in estado_excel.lower() or 'curso' in estado_excel.lower()):
            return 'En progreso / Vencido' if esta_vencido else 'En progreso'

        # Si el estado es "Registrado" o similar
        if estado_excel and ('registrado' in estado_excel.lower() or 'inscrito' in estado_excel.lower()):
            return 'Registrado / Vencido' if esta_vencido else 'Registrado'

        # Por defecto
        return 'No iniciado'

    def _parse_fecha(self, fecha_str) -> Optional[datetime]:
        """Convierte string de fecha a datetime, maneja varios formatos"""
        if pd.isna(fecha_str) or not fecha_str:
            return None

        # Si ya es datetime
        if isinstance(fecha_str, (datetime, date)):
            return datetime.combine(fecha_str, datetime.min.time()) if isinstance(fecha_str, date) else fecha_str

        # Intentar parsear string
        try:
            return pd.to_datetime(fecha_str)
        except:
            return None

    # ============================================================================
    # IMPORTACIÓN EXCEL 1: ENTERPRISE TRAINING REPORT
    # ============================================================================

    def importar_training_report(self, archivo_excel: str) -> Dict:
        """
        Importa datos de estatus y calificaciones desde Enterprise_Training_Report

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            dict: Estadísticas de la importación
        """
        print(f"\n{'='*70}")
        print(f"📊 IMPORTANDO ENTERPRISE TRAINING REPORT")
        print(f"{'='*70}")
        print(f"Archivo: {os.path.basename(archivo_excel)}\n")

        try:
            # Leer Excel con detección automática de fila de headers
            df = self._leer_excel_con_deteccion_headers(archivo_excel)
            print(f"✅ Excel leído: {len(df)} registros")

            # Detectar columnas (auto-mapeo bilingüe)
            self._detectar_columnas(df)

            # Procesar estatus de módulos
            self._procesar_estatus_modulos(df)

            # Procesar calificaciones
            self._procesar_calificaciones(df)

            # Actualizar departamentos y cargos
            self._actualizar_info_usuarios(df)

            self.conn.commit()
            print(f"\n✅ IMPORTACIÓN COMPLETADA")

        except Exception as e:
            self.conn.rollback()
            error_msg = f"❌ Error importando training report: {e}"
            print(error_msg)
            self.stats['errores'].append(error_msg)
            import traceback
            traceback.print_exc()

        return self.stats

    def _procesar_estatus_modulos(self, df: pd.DataFrame):
        """Procesa estatus de módulos y actualiza instituto_ProgresoModulo"""
        print("\n📋 Procesando estatus de módulos...")

        # Verificar que tenemos las columnas necesarias
        if 'training_title' not in self.detected_columns:
            print("  ⚠️ Columna de título de capacitación no encontrada. Saltando procesamiento de módulos.")
            return

        # Filtrar solo registros de módulos (títulos que contengan "MÓDULO")
        col_titulo = self.detected_columns['training_title']
        df_modulos = df[df[col_titulo].str.contains('MÓDULO', case=False, na=False)]

        for idx, row in df_modulos.iterrows():
            try:
                # Obtener datos usando columnas detectadas
                user_id = str(row[self.detected_columns['user_id']]).strip()
                titulo = row[col_titulo]
                estado_excel = row.get(self.detected_columns.get('record_status', ''), '')
                fecha_registro = self._parse_fecha(row.get(self.detected_columns.get('transcript_date', '')))
                fecha_inicio = self._parse_fecha(row.get(self.detected_columns.get('start_date', '')))
                fecha_fin = self._parse_fecha(row.get(self.detected_columns.get('completion_date', '')))

                # Identificar módulo
                num_modulo = self._normalizar_nombre_modulo(titulo)
                if not num_modulo:
                    continue

                # Obtener IdModulo de la BD
                id_modulo = self._get_or_create_modulo(num_modulo)

                # Calcular estado
                estado = self._calcular_estado_modulo(estado_excel, fecha_fin, None)

                # Actualizar progreso
                self._actualizar_progreso_modulo(
                    user_id=user_id,
                    id_modulo=id_modulo,
                    estado=estado,
                    fecha_inicio=fecha_inicio or fecha_registro,
                    fecha_finalizacion=fecha_fin
                )

                self.stats['progresos_actualizados'] += 1

            except Exception as e:
                error_msg = f"Error procesando fila {idx}: {e}"
                print(f"  ⚠️ {error_msg}")
                self.stats['errores'].append(error_msg)

        print(f"  ✅ Progresos actualizados: {self.stats['progresos_actualizados']}")

    def _procesar_calificaciones(self, df: pd.DataFrame):
        """Procesa calificaciones de pruebas"""
        print("\n📝 Procesando calificaciones...")

        # Verificar columnas necesarias
        if 'training_type' not in self.detected_columns or 'training_title' not in self.detected_columns:
            print("  ⚠️ Columnas necesarias no encontradas. Saltando procesamiento de calificaciones.")
            return

        # Filtrar solo pruebas
        col_tipo = self.detected_columns['training_type']
        df_pruebas = df[df[col_tipo].str.contains('Prueba|Test|Assessment|Exam', case=False, na=False)]

        for idx, row in df_pruebas.iterrows():
            try:
                user_id = str(row[self.detected_columns['user_id']]).strip()
                titulo = row[self.detected_columns['training_title']]
                puntuacion = row.get(self.detected_columns.get('score', ''), None)

                # Identificar módulo
                num_modulo = self._normalizar_nombre_modulo(titulo)
                if not num_modulo:
                    continue

                # Validar puntuación
                if pd.isna(puntuacion):
                    continue

                # Convertir puntuación a decimal
                try:
                    puntuacion_decimal = float(puntuacion)
                except:
                    continue

                # Obtener IdModulo
                id_modulo = self._get_or_create_modulo(num_modulo)

                # Registrar calificación
                self._registrar_calificacion(
                    user_id=user_id,
                    id_modulo=id_modulo,
                    puntuacion=puntuacion_decimal
                )

                self.stats['calificaciones_registradas'] += 1

            except Exception as e:
                error_msg = f"Error procesando calificación fila {idx}: {e}"
                print(f"  ⚠️ {error_msg}")
                self.stats['errores'].append(error_msg)

        print(f"  ✅ Calificaciones registradas: {self.stats['calificaciones_registradas']}")

    def _actualizar_info_usuarios(self, df: pd.DataFrame):
        """Actualiza Departamento y Cargo de usuarios"""
        print("\n👥 Actualizando info de usuarios...")

        # Verificar columnas necesarias
        if 'user_id' not in self.detected_columns:
            print("  ⚠️ Columna de User ID no encontrada. Saltando actualización de usuarios.")
            return

        usuarios_unicos = df.drop_duplicates(subset=[self.detected_columns['user_id']])

        for idx, row in usuarios_unicos.iterrows():
            try:
                user_id = str(row[self.detected_columns['user_id']]).strip()
                departamento = row.get(self.detected_columns.get('department', ''), '')
                cargo = row.get(self.detected_columns.get('position', ''), '')

                if departamento or cargo:
                    self._actualizar_usuario_depto_cargo(user_id, departamento, cargo)
                    self.stats['usuarios_actualizados'] += 1

            except Exception as e:
                print(f"  ⚠️ Error actualizando usuario {user_id}: {e}")

        print(f"  ✅ Usuarios actualizados: {self.stats['usuarios_actualizados']}")

    # ============================================================================
    # IMPORTACIÓN EXCEL 2: CSOD ORG PLANNING
    # ============================================================================

    def importar_org_planning(self, archivo_excel: str) -> Dict:
        """
        Importa datos de usuarios desde CSOD_Data_Source_for_Org_Planning

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            dict: Estadísticas de la importación
        """
        print(f"\n{'='*70}")
        print(f"👥 IMPORTANDO CSOD ORG PLANNING")
        print(f"{'='*70}")
        print(f"Archivo: {os.path.basename(archivo_excel)}\n")

        try:
            # Leer Excel con detección automática de fila de headers
            df = self._leer_excel_con_deteccion_headers(archivo_excel)
            print(f"✅ Excel leído: {len(df)} registros")

            # Detectar columnas (auto-mapeo bilingüe)
            self._detectar_columnas(df)

            # Verificar columnas necesarias
            if 'org_user_id' not in self.detected_columns:
                print("  ⚠️ Columna de User ID no encontrada. No se puede continuar.")
                return self.stats

            # Procesar usuarios
            for idx, row in df.iterrows():
                try:
                    user_id = str(row[self.detected_columns['org_user_id']]).strip()
                    nombre = row.get(self.detected_columns.get('org_full_name', ''), '')
                    email = row.get(self.detected_columns.get('org_email', ''), '')
                    cargo = row.get(self.detected_columns.get('org_position', ''), '')
                    departamento = row.get(self.detected_columns.get('org_department', ''), '')
                    ubicacion = row.get(self.detected_columns.get('org_location', ''), '')
                    ciudad = row.get(self.detected_columns.get('org_city', ''), '')
                    pais = row.get(self.detected_columns.get('org_country', ''), '')

                    # Verificar si usuario existe
                    existe = self._usuario_existe(user_id)

                    if existe:
                        # Actualizar
                        self._actualizar_usuario_org_planning(
                            user_id, nombre, email, cargo,
                            departamento, ubicacion, ciudad, pais
                        )
                        self.stats['usuarios_actualizados'] += 1
                    else:
                        # Crear nuevo
                        self._crear_usuario_org_planning(
                            user_id, nombre, email, cargo,
                            departamento, ubicacion, ciudad, pais
                        )
                        self.stats['usuarios_nuevos'] += 1

                except Exception as e:
                    error_msg = f"Error procesando usuario fila {idx}: {e}"
                    print(f"  ⚠️ {error_msg}")
                    self.stats['errores'].append(error_msg)

            self.conn.commit()
            print(f"\n✅ IMPORTACIÓN COMPLETADA")
            print(f"  • Usuarios nuevos: {self.stats['usuarios_nuevos']}")
            print(f"  • Usuarios actualizados: {self.stats['usuarios_actualizados']}")

        except Exception as e:
            self.conn.rollback()
            error_msg = f"❌ Error importando org planning: {e}"
            print(error_msg)
            self.stats['errores'].append(error_msg)
            import traceback
            traceback.print_exc()

        return self.stats

    # ============================================================================
    # MÉTODOS DE BASE DE DATOS
    # ============================================================================

    def _get_or_create_modulo(self, num_modulo: int) -> int:
        """Obtiene o crea un módulo en la BD"""
        nombre_modulo = self.MODULOS_MAPPING[num_modulo]['titulo']

        # Buscar módulo
        self.cursor.execute("""
            SELECT IdModulo FROM instituto_Modulo
            WHERE NombreModulo = %s
        """, (nombre_modulo,))

        result = self.cursor.fetchone()
        if result:
            return result[0]

        # Crear módulo
        self.cursor.execute("""
            INSERT INTO instituto_Modulo (NombreModulo, Activo)
            VALUES (%s, 1)
        """, (nombre_modulo,))

        self.stats['modulos_creados'] += 1
        return self.cursor.lastrowid

    def _actualizar_progreso_modulo(self, user_id: str, id_modulo: int,
                                     estado: str, fecha_inicio: Optional[datetime],
                                     fecha_finalizacion: Optional[datetime]):
        """Actualiza o crea registro de progreso de módulo"""

        # Verificar si existe
        self.cursor.execute("""
            SELECT IdInscripcion FROM instituto_ProgresoModulo
            WHERE UserId = %s AND IdModulo = %s
        """, (user_id, id_modulo))

        if self.cursor.fetchone():
            # Actualizar
            self.cursor.execute("""
                UPDATE instituto_ProgresoModulo
                SET EstatusModulo = %s,
                    FechaInicio = COALESCE(%s, FechaInicio),
                    FechaFinalizacion = %s,
                    PorcentajeAvance = CASE WHEN %s = 'Terminado' THEN 100 ELSE PorcentajeAvance END
                WHERE UserId = %s AND IdModulo = %s
            """, (estado, fecha_inicio, fecha_finalizacion, estado, user_id, id_modulo))
        else:
            # Crear
            self.cursor.execute("""
                INSERT INTO instituto_ProgresoModulo
                (UserId, IdModulo, EstatusModulo, FechaInicio, FechaFinalizacion,
                 PorcentajeAvance, FechaAsignacion)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (user_id, id_modulo, estado, fecha_inicio, fecha_finalizacion,
                  100 if estado == 'Terminado' else 0))

    def _registrar_calificacion(self, user_id: str, id_modulo: int, puntuacion: float):
        """Registra calificación de evaluación"""

        # Obtener IdInscripcion
        self.cursor.execute("""
            SELECT IdInscripcion FROM instituto_ProgresoModulo
            WHERE UserId = %s AND IdModulo = %s
        """, (user_id, id_modulo))

        result = self.cursor.fetchone()
        if not result:
            # Crear progreso si no existe
            self._actualizar_progreso_modulo(user_id, id_modulo, 'En progreso', None, None)
            self.cursor.execute("""
                SELECT IdInscripcion FROM instituto_ProgresoModulo
                WHERE UserId = %s AND IdModulo = %s
            """, (user_id, id_modulo))
            result = self.cursor.fetchone()

        id_inscripcion = result[0]

        # Obtener o crear evaluación
        id_evaluacion = self._get_or_create_evaluacion(id_modulo)

        # Verificar si ya existe resultado
        self.cursor.execute("""
            SELECT IdResultado FROM instituto_ResultadoEvaluacion
            WHERE IdInscripcion = %s AND IdEvaluacion = %s
        """, (id_inscripcion, id_evaluacion))

        aprobado = 1 if puntuacion >= 70 else 0

        if self.cursor.fetchone():
            # Actualizar
            self.cursor.execute("""
                UPDATE instituto_ResultadoEvaluacion
                SET PuntajeObtenido = %s,
                    Aprobado = %s
                WHERE IdInscripcion = %s AND IdEvaluacion = %s
            """, (puntuacion, aprobado, id_inscripcion, id_evaluacion))
        else:
            # Crear
            self.cursor.execute("""
                INSERT INTO instituto_ResultadoEvaluacion
                (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado,
                 IntentoNumero, FechaRealizacion)
                VALUES (%s, %s, %s, %s, 1, NOW())
            """, (id_inscripcion, id_evaluacion, puntuacion, aprobado))

    def _get_or_create_evaluacion(self, id_modulo: int) -> int:
        """Obtiene o crea evaluación para un módulo"""
        self.cursor.execute("""
            SELECT IdEvaluacion FROM instituto_Evaluacion
            WHERE IdModulo = %s
        """, (id_modulo,))

        result = self.cursor.fetchone()
        if result:
            return result[0]

        # Crear evaluación por defecto
        self.cursor.execute("""
            INSERT INTO instituto_Evaluacion
            (IdModulo, NombreEvaluacion, PuntajeMinimoAprobatorio, Activo)
            VALUES (%s, %s, 70, 1)
        """, (id_modulo, f'Evaluación Módulo {id_modulo}'))

        return self.cursor.lastrowid

    def _actualizar_usuario_depto_cargo(self, user_id: str, departamento: str, cargo: str):
        """Actualiza departamento y cargo del usuario"""
        self.cursor.execute("""
            UPDATE instituto_Usuario
            SET Position = %s
            WHERE UserId = %s
        """, (cargo, user_id))

    def _usuario_existe(self, user_id: str) -> bool:
        """Verifica si un usuario existe"""
        self.cursor.execute("""
            SELECT 1 FROM instituto_Usuario WHERE UserId = %s
        """, (user_id,))
        return self.cursor.fetchone() is not None

    def _crear_usuario_org_planning(self, user_id, nombre, email, cargo,
                                     departamento, ubicacion, ciudad, pais):
        """Crea nuevo usuario desde org planning"""
        self.cursor.execute("""
            INSERT INTO instituto_Usuario
            (UserId, NombreCompleto, UserEmail, Position, Ubicacion, Activo)
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (user_id, nombre, email, cargo, ubicacion))

    def _actualizar_usuario_org_planning(self, user_id, nombre, email, cargo,
                                          departamento, ubicacion, ciudad, pais):
        """Actualiza usuario desde org planning"""
        self.cursor.execute("""
            UPDATE instituto_Usuario
            SET NombreCompleto = %s,
                UserEmail = %s,
                Position = %s,
                Ubicacion = %s
            WHERE UserId = %s
        """, (nombre, email, cargo, ubicacion, user_id))

    def generar_reporte(self) -> str:
        """Genera reporte de estadísticas de la importación"""
        reporte = f"""
{'='*70}
REPORTE DE IMPORTACIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

📊 ESTADÍSTICAS:
  • Usuarios nuevos:           {self.stats['usuarios_nuevos']}
  • Usuarios actualizados:      {self.stats['usuarios_actualizados']}
  • Módulos creados:            {self.stats['modulos_creados']}
  • Progresos actualizados:     {self.stats['progresos_actualizados']}
  • Calificaciones registradas: {self.stats['calificaciones_registradas']}
  • Errores:                    {len(self.stats['errores'])}

"""
        if self.stats['errores']:
            reporte += "❌ ERRORES ENCONTRADOS:\n"
            for error in self.stats['errores'][:10]:  # Mostrar máximo 10 errores
                reporte += f"  • {error}\n"

            if len(self.stats['errores']) > 10:
                reporte += f"  ... y {len(self.stats['errores']) - 10} errores más\n"

        reporte += f"\n{'='*70}\n"
        return reporte
