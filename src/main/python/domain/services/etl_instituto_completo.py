"""
Sistema ETL Completo - Instituto Hutchison Ports
================================================

Sistema de Extracción, Transformación y Carga (ETL) para procesar archivos Excel
de CSOD (Cornerstone OnDemand) y cargarlos en SQL Server.

Características:
- ✅ Soporte para SQL Server (pyodbc)
- ✅ Validación de datos con Pydantic
- ✅ Auto-detección de módulos nuevos (escalable a 14+ módulos)
- ✅ Batch operations para alto rendimiento
- ✅ Detección automática de columnas (Español/Inglés)
- ✅ Matching case-insensitive para módulos y evaluaciones
- ✅ Manejo robusto de errores y logging
- ✅ Soporte para ambos archivos: Training Report y Org Planning

Archivos soportados:
1. Enterprise_Training_Report{timestamp}.xlsx
2. CSOD_Data_Source_for_Org_Planning_{timestamp}.xlsx

Autor: Claude AI
Fecha: 2025-01-18
Versión: 1.0.0
"""

import pandas as pd
import pyodbc
import re
import unicodedata
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging
from difflib import SequenceMatcher

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC MODELS - VALIDACIÓN DE DATOS
# ============================================================================

try:
    from pydantic import BaseModel, Field, validator, ValidationError
except ImportError:
    logger.warning("⚠️  Pydantic no instalado. Instalando con: pip install pydantic")
    # Fallback a dataclasses si no hay Pydantic
    BaseModel = object


class EstatusModulo(str, Enum):
    """Estados posibles de un módulo"""
    TERMINADO = "Terminado"
    EN_PROGRESO = "En progreso"
    REGISTRADO = "Registrado"
    NO_INICIADO = "No iniciado"


class TipoCapacitacion(str, Enum):
    """Tipos de capacitación"""
    CURRICULUM = "Curriculum"
    PRUEBA = "Prueba"


class UsuarioExcel(BaseModel):
    """Modelo de validación para datos de usuario del Excel"""
    user_id: str = Field(..., min_length=1, description="ID único de usuario (MASTER KEY)")
    nombre_completo: Optional[str] = None
    email: Optional[str] = None
    cargo: Optional[str] = None  # Position
    unidad_negocio: Optional[str] = None
    departamento: Optional[str] = None
    ubicacion: Optional[str] = None
    nivel: Optional[str] = None

    @validator('user_id')
    def user_id_no_vacio(cls, v):
        if not v or v.strip() == '':
            raise ValueError('user_id no puede estar vacío')
        return v.strip()

    @validator('email')
    def validar_email(cls, v):
        if v and '@' not in v:
            logger.warning(f"Email potencialmente inválido: {v}")
        return v


class ProgresoModuloExcel(BaseModel):
    """Modelo de validación para progreso de módulo"""
    user_id: str = Field(..., min_length=1)
    titulo_capacitacion: str = Field(..., min_length=1)
    tipo_capacitacion: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_finalizacion: Optional[datetime] = None
    fecha_registro: Optional[datetime] = None
    puntuacion: Optional[float] = None

    @validator('puntuacion')
    def validar_puntuacion(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError(f'Puntuación fuera de rango: {v}')
        return v


# ============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================================

@dataclass
class ETLConfig:
    """Configuración del ETL"""
    # SQL Server
    server: str = "localhost"
    database: str = "InstitutoHutchison"
    username: Optional[str] = None  # Si es None, usa autenticación Windows
    password: Optional[str] = None
    driver: str = "ODBC Driver 17 for SQL Server"

    # ETL Settings
    batch_size: int = 1000
    enable_validation: bool = True
    auto_create_modules: bool = True

    # Defaults
    default_puntaje_minimo: float = 70.0
    default_intentos_permitidos: int = 3
    default_rol_id: int = 4  # Usuario


# Mapeo completo de los 14 módulos
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

# Mapeo de evaluaciones a módulos (case-insensitive)
EVALUACIONES_A_MODULOS = {
    # Módulo 1
    "introducción a la filosofía": 1,
    "filosofía hutchinson": 1,

    # Módulo 2
    "sostenibilidad": 2,
    "compromiso con el futuro": 2,

    # Módulo 3
    "introducción a las operaciones": 3,
    "operaciones portuarias": 3,

    # Módulo 4
    "relaciones laborales": 4,

    # Módulo 5
    "seguridad en las operaciones": 5,
    "seguridad operacional": 5,

    # Módulo 6
    "ciberseguridad": 6,
    "seguridad informática": 6,

    # Módulo 7
    "entorno laboral saludable": 7,
    "salud laboral": 7,

    # Módulo 8
    "procesos de recursos humanos": 8,
    "recursos humanos": 8,
    "rrhh": 8,

    # Módulo 9
    "programas de bienestar": 9,
    "bienestar integral": 9,

    # Módulo 10
    "desarrollo de nuevos productos": 10,
    "nuevos productos": 10,

    # Módulo 11
    "productos digitales": 11,
    "digitales de hp": 11,

    # Módulo 12
    "tecnología": 12,
    "eficiencia y productividad": 12,

    # Módulo 13
    "protocolos y brigadas": 13,
    "brigadas de contingencia": 13,

    # Módulo 14
    "sistema integrado": 14,
    "gestión de calidad": 14,
    "mejora continua": 14
}

# Variaciones de columnas (Español/Inglés)
COLUMN_VARIATIONS = {
    'user_id': [
        'Identificación de usuario',
        'User ID',
        'User Identification',
        'ID',
        'UserId'
    ],
    'training_title': [
        'Título de la capacitación',
        'Título de capacitación',
        'Training Title',
        'Course Title',
        'Title'
    ],
    'training_type': [
        'Tipo de capacitación',
        'Training Type',
        'Content Type',
        'Type'
    ],
    'record_status': [
        'Estado del expediente',
        'Record Status',
        'Completion Status',
        'Status',
        'Estatus'
    ],
    'transcript_date': [
        'Fecha de registro de la transcripción',
        'Transcript Registration Date',
        'Registration Date',
        'Fecha de Registro'
    ],
    'start_date': [
        'Fecha de inicio de la capacitación',
        'Training Start Date',
        'Start Date',
        'Fecha de Inicio'
    ],
    'completion_date': [
        'Fecha de finalización de expediente',
        'Record Completion Date',
        'Completion Date',
        'Finished Date',
        'Fecha de Finalización'
    ],
    'score': [
        'Puntuación de la transcripción',
        'Transcript Score',
        'Score',
        'Grade',
        'Calificación'
    ],
    'full_name': [
        'Nombre completo del usuario',
        'User - Full Name',
        'Full Name',
        'Name',
        'Nombre Completo'
    ],
    'email': [
        'Correo electrónico del usuario',
        'User - Email Address',
        'Email',
        'E-mail',
        'Correo'
    ],
    'position': [
        'Usuario - Cargo',
        'Cargo',
        'Position',
        'Job Title'
    ],
    'business_unit': [
        'Usuario - División',
        'División',
        'Unidad de negocio',
        'User - Division',
        'Business Unit',
        'Division'
    ],
    'department': [
        'Usuario - Departamento',
        'Departamento',
        'Department',
        'Organization'
    ],
    'location': [
        'Usuario - Ubicación',
        'Ubicación',
        'User - Location',
        'Location',
        'Site'
    ],
    'level': [
        'Usuario - Nivel',
        'Nivel',
        'User - Level',
        'Level'
    ]
}

# Mapeo de estados del Excel a estados de BD
ESTADO_MAPPING = {
    'terminado': EstatusModulo.TERMINADO,
    'completado': EstatusModulo.TERMINADO,
    'completed': EstatusModulo.TERMINADO,
    'finished': EstatusModulo.TERMINADO,
    'en progreso': EstatusModulo.EN_PROGRESO,
    'in progress': EstatusModulo.EN_PROGRESO,
    'progress': EstatusModulo.EN_PROGRESO,
    'registrado': EstatusModulo.REGISTRADO,
    'registered': EstatusModulo.REGISTRADO,
    'enrolled': EstatusModulo.REGISTRADO,
    'no iniciado': EstatusModulo.NO_INICIADO,
    'not started': EstatusModulo.NO_INICIADO,
    'pending': EstatusModulo.NO_INICIADO
}

# Porcentaje por estado
PORCENTAJE_POR_ESTADO = {
    EstatusModulo.TERMINADO: 100,
    EstatusModulo.EN_PROGRESO: 50,
    EstatusModulo.REGISTRADO: 0,
    EstatusModulo.NO_INICIADO: 0
}


# ============================================================================
# CLASE PRINCIPAL ETL
# ============================================================================

class ETLInstitutoCompleto:
    """
    Sistema ETL completo para procesar archivos Excel de CSOD

    Flujo del proceso:
    1. Extracción: Leer Excel con detección automática de headers
    2. Validación: Validar datos con Pydantic
    3. Transformación: Normalizar, mapear y enriquecer datos
    4. Carga: Insertar/actualizar en SQL Server con batch operations
    5. Reporte: Generar estadísticas de la importación
    """

    def __init__(self, config: ETLConfig):
        """
        Inicializa el sistema ETL

        Args:
            config: Configuración del ETL
        """
        self.config = config
        self.connection: Optional[pyodbc.Connection] = None
        self.cursor: Optional[pyodbc.Cursor] = None

        # Columnas detectadas en el Excel
        self.detected_columns: Dict[str, str] = {}

        # Cachés para optimización (evitar N+1 queries)
        self._cache_modulos: Dict[str, int] = {}
        self._cache_evaluaciones: Dict[int, int] = {}
        self._cache_unidades: Dict[str, int] = {}
        self._cache_departamentos: Dict[Tuple[int, str], int] = {}
        self._cache_usuarios: Dict[str, int] = {}
        self._cache_progresos: Dict[Tuple[str, int], int] = {}

        # Estadísticas
        self.stats = {
            'usuarios_nuevos': 0,
            'usuarios_actualizados': 0,
            'progresos_insertados': 0,
            'progresos_actualizados': 0,
            'calificaciones_registradas': 0,
            'modulos_creados': 0,
            'evaluaciones_creadas': 0,
            'unidades_creadas': 0,
            'departamentos_creados': 0,
            'errores': [],
            'tiempo_inicio': None,
            'tiempo_fin': None
        }

        # Conectar a BD
        self._conectar_bd()

    # ========================================================================
    # CONEXIÓN A BASE DE DATOS
    # ========================================================================

    def _conectar_bd(self):
        """Establece conexión con SQL Server"""
        try:
            # Construir connection string
            if self.config.username and self.config.password:
                # Autenticación SQL Server
                conn_str = (
                    f"DRIVER={{{self.config.driver}}};"
                    f"SERVER={self.config.server};"
                    f"DATABASE={self.config.database};"
                    f"UID={self.config.username};"
                    f"PWD={self.config.password};"
                )
            else:
                # Autenticación Windows
                conn_str = (
                    f"DRIVER={{{self.config.driver}}};"
                    f"SERVER={self.config.server};"
                    f"DATABASE={self.config.database};"
                    f"Trusted_Connection=yes;"
                )

            self.connection = pyodbc.connect(conn_str, autocommit=False)
            self.cursor = self.connection.cursor()

            logger.info(f"✅ Conectado a SQL Server: {self.config.server}/{self.config.database}")

        except Exception as e:
            logger.error(f"❌ Error conectando a SQL Server: {e}")
            raise

    def cerrar_conexion(self):
        """Cierra la conexión a la BD"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("🔒 Conexión cerrada")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cerrar_conexion()

    # ========================================================================
    # EXTRACCIÓN: LECTURA Y DETECCIÓN DE EXCEL
    # ========================================================================

    def _leer_excel_con_deteccion_headers(self, archivo_excel: str) -> pd.DataFrame:
        """
        Lee Excel detectando automáticamente dónde están los headers reales

        CSOD a veces pone metadatos en las primeras filas. Esta función
        detecta automáticamente dónde comienzan los datos reales.

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            DataFrame con los datos
        """
        try:
            # Intentar lectura normal
            df = pd.read_excel(archivo_excel, engine='openpyxl')

            # Verificar si los headers son válidos
            if any('Unnamed' in str(col) for col in df.columns):
                logger.warning("⚠️  Headers no detectados en fila 0, buscando headers reales...")

                # Buscar headers reales en las primeras 10 filas
                for skip_rows in range(1, 11):
                    try:
                        df_test = pd.read_excel(archivo_excel, skiprows=skip_rows, engine='openpyxl')

                        # Verificar si encontramos columnas conocidas
                        cols_str = ' '.join(str(c).lower() for c in df_test.columns)
                        keywords = ['usuario', 'user', 'módulo', 'module', 'training', 'capacitación']

                        if any(kw in cols_str for kw in keywords):
                            logger.info(f"✅ Headers encontrados en fila {skip_rows}")
                            return df_test
                    except:
                        continue

                logger.warning("⚠️  No se pudieron detectar headers automáticamente. Usando fila 0.")
                return df

            return df

        except Exception as e:
            logger.error(f"❌ Error leyendo Excel {archivo_excel}: {e}")
            raise

    def _detectar_columnas(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Detecta automáticamente las columnas del Excel (Español/Inglés)

        Args:
            df: DataFrame de pandas

        Returns:
            Diccionario con columnas detectadas {key: nombre_columna_excel}
        """
        self.detected_columns = {}
        columnas_excel = df.columns.tolist()

        for key, variations in COLUMN_VARIATIONS.items():
            for variation in variations:
                for col_excel in columnas_excel:
                    # Matching case-insensitive y con tolerancia a espacios
                    if variation.lower().strip() in str(col_excel).lower().strip():
                        self.detected_columns[key] = col_excel
                        break
                if key in self.detected_columns:
                    break

        logger.info(f"✅ Columnas detectadas: {len(self.detected_columns)}/{len(COLUMN_VARIATIONS)}")

        # Mostrar columnas no detectadas
        no_detectadas = set(COLUMN_VARIATIONS.keys()) - set(self.detected_columns.keys())
        if no_detectadas:
            logger.info(f"ℹ️  Columnas opcionales no encontradas: {', '.join(no_detectadas)}")

        return self.detected_columns

    # ========================================================================
    # TRANSFORMACIÓN: NORMALIZACIÓN Y UTILIDADES
    # ========================================================================

    @staticmethod
    def _normalizar_texto(texto: str) -> str:
        """
        Normaliza texto para matching case-insensitive

        - Convierte a minúsculas
        - Quita acentos
        - Quita espacios extras

        Args:
            texto: Texto a normalizar

        Returns:
            Texto normalizado
        """
        if not texto or pd.isna(texto):
            return ""

        # Convertir a string y minúsculas
        texto = str(texto).lower().strip()

        # Quitar acentos
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto)

        return texto

    @staticmethod
    def _extraer_numero_modulo(titulo: str) -> Optional[int]:
        """
        Extrae el número de módulo del título usando regex

        Soporta variaciones como:
        - "MÓDULO 8 - PROCESOS DE RRHH"
        - "Modulo 8: Procesos"
        - "MODULE 8 Procesos"

        Args:
            titulo: Título del módulo/capacitación

        Returns:
            Número del módulo (1-14) o None si no se encuentra
        """
        if not titulo or pd.isna(titulo):
            return None

        # Buscar "MÓDULO X" o "MODULE X" (case-insensitive)
        match = re.search(r'M[OÓ]DULO\s+(\d+)', str(titulo), re.IGNORECASE)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 14:
                return num

        return None

    def _identificar_modulo_fuzzy(self, titulo: str) -> Optional[int]:
        """
        Identifica módulo usando fuzzy matching si regex falla

        Útil para títulos que no tienen "MÓDULO X" pero mencionan el tema
        Ejemplo: "Ciberseguridad - Prueba Final" → Módulo 6

        Args:
            titulo: Título de la capacitación

        Returns:
            Número del módulo o None
        """
        titulo_norm = self._normalizar_texto(titulo)

        # Buscar en mapeo de evaluaciones
        for key, num_modulo in EVALUACIONES_A_MODULOS.items():
            if key in titulo_norm:
                return num_modulo

        # Fuzzy matching con nombres de módulos (umbral 80%)
        best_match_score = 0
        best_match_num = None

        for num, nombre in MODULOS_MAPPING.items():
            nombre_norm = self._normalizar_texto(nombre)
            score = SequenceMatcher(None, titulo_norm, nombre_norm).ratio()

            if score > best_match_score and score >= 0.8:
                best_match_score = score
                best_match_num = num

        if best_match_num:
            logger.info(f"🔍 Fuzzy match: '{titulo}' → Módulo {best_match_num} (score: {best_match_score:.2f})")

        return best_match_num

    def _normalizar_estatus(self, estatus_excel: str) -> str:
        """
        Normaliza el estado del Excel al formato de la BD

        Args:
            estatus_excel: Estado del Excel

        Returns:
            Estado normalizado (enum)
        """
        if not estatus_excel or pd.isna(estatus_excel):
            return EstatusModulo.NO_INICIADO.value

        estatus_norm = self._normalizar_texto(estatus_excel)

        for key, enum_value in ESTADO_MAPPING.items():
            if key in estatus_norm:
                return enum_value.value

        # Default
        return EstatusModulo.NO_INICIADO.value

    def _calcular_porcentaje_por_estado(self, estatus: str) -> int:
        """
        Calcula el porcentaje de avance según el estado

        Args:
            estatus: Estado normalizado

        Returns:
            Porcentaje (0-100)
        """
        for enum_value, porcentaje in PORCENTAJE_POR_ESTADO.items():
            if estatus == enum_value.value:
                return porcentaje
        return 0

    def _parse_fecha(self, fecha_valor) -> Optional[datetime]:
        """
        Parsea fecha de múltiples formatos

        Args:
            fecha_valor: String de fecha, objeto datetime, o pandas Timestamp

        Returns:
            datetime o None
        """
        if pd.isna(fecha_valor) or not fecha_valor:
            return None

        # Si ya es datetime
        if isinstance(fecha_valor, (datetime, pd.Timestamp)):
            return fecha_valor if isinstance(fecha_valor, datetime) else fecha_valor.to_pydatetime()

        # Intentar múltiples formatos
        formatos = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y',
            '%Y/%m/%d',
            '%d-%m-%Y'
        ]

        fecha_str = str(fecha_valor).strip()

        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except:
                continue

        logger.warning(f"⚠️  No se pudo parsear fecha: {fecha_valor}")
        return None

    # ========================================================================
    # PRECARGA DE DATOS (Optimización - Evita N+1 queries)
    # ========================================================================

    def _precargar_modulos(self):
        """Precarga módulos en caché"""
        if self._cache_modulos:
            return  # Ya está cargado

        query = "SELECT IdModulo, NombreModulo FROM instituto_Modulo WHERE Activo = 1"
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            self._cache_modulos[row.NombreModulo] = row.IdModulo

        logger.info(f"✅ Módulos precargados: {len(self._cache_modulos)}")

    def _precargar_unidades_negocio(self):
        """Precarga unidades de negocio"""
        if self._cache_unidades:
            return

        query = "SELECT IdUnidadDeNegocio, NombreUnidad FROM instituto_UnidadDeNegocio WHERE Activo = 1"
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            self._cache_unidades[row.NombreUnidad] = row.IdUnidadDeNegocio

        logger.info(f"✅ Unidades de negocio precargadas: {len(self._cache_unidades)}")

    def _precargar_departamentos(self):
        """Precarga departamentos con clave (IdUnidad, NombreDepto)"""
        if self._cache_departamentos:
            return

        query = """
            SELECT IdDepartamento, IdUnidadDeNegocio, NombreDepartamento
            FROM instituto_Departamento
            WHERE Activo = 1
        """
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            key = (row.IdUnidadDeNegocio, row.NombreDepartamento)
            self._cache_departamentos[key] = row.IdDepartamento

        logger.info(f"✅ Departamentos precargados: {len(self._cache_departamentos)}")

    def _precargar_usuarios(self, user_ids: List[str]):
        """
        Precarga usuarios existentes

        Args:
            user_ids: Lista de UserIds a precargar
        """
        if not user_ids:
            return

        # SQL Server usa ? como placeholder
        placeholders = ','.join(['?'] * len(user_ids))
        query = f"""
            SELECT IdUsuario, UserId
            FROM instituto_Usuario
            WHERE UserId IN ({placeholders})
        """

        self.cursor.execute(query, user_ids)

        for row in self.cursor.fetchall():
            self._cache_usuarios[row.UserId] = row.IdUsuario

        logger.info(f"✅ Usuarios precargados: {len(self._cache_usuarios)}")

    def _precargar_progresos(self, user_ids: List[str]):
        """
        Precarga progresos existentes

        Args:
            user_ids: Lista de UserIds
        """
        if not user_ids:
            return

        placeholders = ','.join(['?'] * len(user_ids))
        query = f"""
            SELECT UserId, IdModulo, IdInscripcion
            FROM instituto_ProgresoModulo
            WHERE UserId IN ({placeholders})
        """

        self.cursor.execute(query, user_ids)

        for row in self.cursor.fetchall():
            key = (row.UserId, row.IdModulo)
            self._cache_progresos[key] = row.IdInscripcion

        logger.info(f"✅ Progresos existentes precargados: {len(self._cache_progresos)}")

    def _precargar_evaluaciones(self):
        """Precarga evaluaciones por módulo"""
        if self._cache_evaluaciones:
            return

        query = """
            SELECT IdEvaluacion, IdModulo
            FROM instituto_Evaluacion
            WHERE Activo = 1
        """
        self.cursor.execute(query)

        for row in self.cursor.fetchall():
            # Solo guarda la primera evaluación por módulo
            if row.IdModulo not in self._cache_evaluaciones:
                self._cache_evaluaciones[row.IdModulo] = row.IdEvaluacion

        logger.info(f"✅ Evaluaciones precargadas: {len(self._cache_evaluaciones)}")

    # ========================================================================
    # CARGA: AUTO-CREACIÓN DE ENTIDADES
    # ========================================================================

    def _crear_modulo_si_no_existe(self, num_modulo: int) -> int:
        """
        Crea un módulo nuevo si no existe (AUTO-DETECCIÓN)

        Args:
            num_modulo: Número del módulo (1-14)

        Returns:
            IdModulo
        """
        nombre_modulo = MODULOS_MAPPING.get(num_modulo)

        if not nombre_modulo:
            logger.warning(f"⚠️  Número de módulo desconocido: {num_modulo}")
            return None

        # Verificar si ya existe en caché
        if nombre_modulo in self._cache_modulos:
            return self._cache_modulos[nombre_modulo]

        # Verificar si existe en BD
        self.cursor.execute(
            "SELECT IdModulo FROM instituto_Modulo WHERE NombreModulo = ?",
            (nombre_modulo,)
        )
        row = self.cursor.fetchone()

        if row:
            id_modulo = row.IdModulo
            self._cache_modulos[nombre_modulo] = id_modulo
            return id_modulo

        # Crear nuevo módulo
        logger.info(f"🆕 Creando nuevo módulo: {nombre_modulo}")

        self.cursor.execute("""
            INSERT INTO instituto_Modulo
            (NombreModulo, TipoDeCapacitacion, Activo, FechaCreacion)
            VALUES (?, ?, 1, GETDATE())
        """, (nombre_modulo, TipoCapacitacion.CURRICULUM.value))

        # SQL Server devuelve lastrowid diferente
        self.cursor.execute("SELECT @@IDENTITY AS id")
        id_modulo = self.cursor.fetchone().id

        self._cache_modulos[nombre_modulo] = id_modulo
        self.stats['modulos_creados'] += 1

        # Crear evaluación por defecto para el módulo
        self._crear_evaluacion_para_modulo(id_modulo, nombre_modulo)

        return id_modulo

    def _crear_evaluacion_para_modulo(self, id_modulo: int, nombre_modulo: str):
        """
        Crea evaluación por defecto para un módulo

        Args:
            id_modulo: ID del módulo
            nombre_modulo: Nombre del módulo
        """
        nombre_evaluacion = f"Evaluación {nombre_modulo}"

        self.cursor.execute("""
            INSERT INTO instituto_Evaluacion
            (IdModulo, NombreEvaluacion, TipoEvaluacion,
             PuntajeMinimo, IntentosPermitid, Activo, FechaCreacion)
            VALUES (?, ?, ?, ?, ?, 1, GETDATE())
        """, (
            id_modulo,
            nombre_evaluacion,
            TipoCapacitacion.PRUEBA.value,
            self.config.default_puntaje_minimo,
            self.config.default_intentos_permitidos
        ))

        self.stats['evaluaciones_creadas'] += 1
        logger.info(f"✅ Evaluación creada para módulo {id_modulo}")

    def _obtener_o_crear_unidad_negocio(self, nombre_unidad: str) -> Optional[int]:
        """
        Obtiene o crea una unidad de negocio

        Args:
            nombre_unidad: Nombre de la unidad

        Returns:
            IdUnidadDeNegocio
        """
        if not nombre_unidad or pd.isna(nombre_unidad):
            return None

        nombre_unidad = str(nombre_unidad).strip()

        # Verificar caché
        if nombre_unidad in self._cache_unidades:
            return self._cache_unidades[nombre_unidad]

        # Verificar BD
        self.cursor.execute(
            "SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE NombreUnidad = ?",
            (nombre_unidad,)
        )
        row = self.cursor.fetchone()

        if row:
            id_unidad = row.IdUnidadDeNegocio
            self._cache_unidades[nombre_unidad] = id_unidad
            return id_unidad

        # Crear nueva
        codigo = nombre_unidad[:20].upper().replace(' ', '_')

        self.cursor.execute("""
            INSERT INTO instituto_UnidadDeNegocio
            (NombreUnidad, Codigo, Activo, FechaCreacion)
            VALUES (?, ?, 1, GETDATE())
        """, (nombre_unidad, codigo))

        self.cursor.execute("SELECT @@IDENTITY AS id")
        id_unidad = self.cursor.fetchone().id

        self._cache_unidades[nombre_unidad] = id_unidad
        self.stats['unidades_creadas'] += 1

        logger.info(f"🆕 Unidad de negocio creada: {nombre_unidad}")

        return id_unidad

    def _obtener_o_crear_departamento(self, id_unidad: int, nombre_depto: str) -> Optional[int]:
        """
        Obtiene o crea un departamento

        Args:
            id_unidad: ID de la unidad de negocio
            nombre_depto: Nombre del departamento

        Returns:
            IdDepartamento
        """
        if not nombre_depto or pd.isna(nombre_depto) or not id_unidad:
            return None

        nombre_depto = str(nombre_depto).strip()
        key = (id_unidad, nombre_depto)

        # Verificar caché
        if key in self._cache_departamentos:
            return self._cache_departamentos[key]

        # Verificar BD
        self.cursor.execute("""
            SELECT IdDepartamento
            FROM instituto_Departamento
            WHERE IdUnidadDeNegocio = ? AND NombreDepartamento = ?
        """, (id_unidad, nombre_depto))
        row = self.cursor.fetchone()

        if row:
            id_depto = row.IdDepartamento
            self._cache_departamentos[key] = id_depto
            return id_depto

        # Crear nuevo
        self.cursor.execute("""
            INSERT INTO instituto_Departamento
            (IdUnidadDeNegocio, NombreDepartamento, Activo, FechaCreacion)
            VALUES (?, ?, 1, GETDATE())
        """, (id_unidad, nombre_depto))

        self.cursor.execute("SELECT @@IDENTITY AS id")
        id_depto = self.cursor.fetchone().id

        self._cache_departamentos[key] = id_depto
        self.stats['departamentos_creados'] += 1

        logger.info(f"🆕 Departamento creado: {nombre_depto} (Unidad: {id_unidad})")

        return id_depto

    # ========================================================================
    # PROCESAMIENTO: ORG PLANNING (USUARIOS)
    # ========================================================================

    def importar_org_planning(self, archivo_excel: str) -> Dict[str, Any]:
        """
        Importa archivo CSOD Org Planning (Datos de Usuarios)

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            Estadísticas de la importación
        """
        logger.info("="*80)
        logger.info("👥 IMPORTANDO ORG PLANNING (DATOS DE USUARIOS)")
        logger.info("="*80)

        self.stats['tiempo_inicio'] = datetime.now()

        try:
            # 1. EXTRACCIÓN
            logger.info("\n📖 Paso 1/4: Leyendo archivo Excel...")
            df = self._leer_excel_con_deteccion_headers(archivo_excel)
            logger.info(f"✅ Registros leídos: {len(df):,}")

            # 2. DETECCIÓN DE COLUMNAS
            logger.info("\n🔍 Paso 2/4: Detectando columnas...")
            self._detectar_columnas(df)

            # Verificar columna crítica
            if 'user_id' not in self.detected_columns:
                raise ValueError("❌ Columna 'user_id' no encontrada. No se puede continuar.")

            # 3. PRECARGA DE DATOS
            logger.info("\n⚡ Paso 3/4: Precargando datos para optimización...")
            self._precargar_unidades_negocio()
            self._precargar_departamentos()

            user_ids = df[self.detected_columns['user_id']].astype(str).str.strip().unique().tolist()
            self._precargar_usuarios(user_ids)

            # 4. PROCESAMIENTO
            logger.info(f"\n📊 Paso 4/4: Procesando {len(df):,} usuarios...")
            self._procesar_usuarios_batch(df)

            # COMMIT
            self.connection.commit()
            logger.info("✅ Transacción confirmada")

            self.stats['tiempo_fin'] = datetime.now()
            self._mostrar_estadisticas()

            return self.stats

        except Exception as e:
            logger.error(f"❌ Error en importación Org Planning: {e}")
            self.connection.rollback()
            logger.info("🔄 Transacción revertida")
            self.stats['errores'].append(f"Error fatal: {e}")
            raise

    def _procesar_usuarios_batch(self, df: pd.DataFrame):
        """
        Procesa usuarios en batch (INSERT/UPDATE)

        Args:
            df: DataFrame con datos de usuarios
        """
        col_user_id = self.detected_columns['user_id']
        col_nombre = self.detected_columns.get('full_name')
        col_email = self.detected_columns.get('email')
        col_cargo = self.detected_columns.get('position')
        col_unidad = self.detected_columns.get('business_unit')
        col_depto = self.detected_columns.get('department')
        col_ubicacion = self.detected_columns.get('location')
        col_nivel = self.detected_columns.get('level')

        batch_updates = []
        batch_inserts = []

        for idx, row in df.iterrows():
            try:
                user_id = str(row[col_user_id]).strip()

                if not user_id:
                    continue

                # Extraer datos
                nombre_completo = str(row[col_nombre]) if col_nombre and not pd.isna(row.get(col_nombre)) else None
                email = str(row[col_email]) if col_email and not pd.isna(row.get(col_email)) else None
                cargo = str(row[col_cargo]) if col_cargo and not pd.isna(row.get(col_cargo)) else None
                ubicacion = str(row[col_ubicacion]) if col_ubicacion and not pd.isna(row.get(col_ubicacion)) else None
                nivel = str(row[col_nivel]) if col_nivel and not pd.isna(row.get(col_nivel)) else None

                # Obtener/crear unidad y departamento
                nombre_unidad = str(row[col_unidad]) if col_unidad and not pd.isna(row.get(col_unidad)) else None
                nombre_depto = str(row[col_depto]) if col_depto and not pd.isna(row.get(col_depto)) else None

                id_unidad = self._obtener_o_crear_unidad_negocio(nombre_unidad) if nombre_unidad else None
                id_depto = self._obtener_o_crear_departamento(id_unidad, nombre_depto) if nombre_depto and id_unidad else None

                # Verificar si existe
                if user_id in self._cache_usuarios:
                    # UPDATE
                    batch_updates.append((
                        nombre_completo,
                        email,
                        cargo,
                        id_unidad,
                        id_depto,
                        nivel,
                        ubicacion,
                        user_id
                    ))
                else:
                    # INSERT
                    batch_inserts.append((
                        user_id,
                        id_unidad,
                        id_depto,
                        self.config.default_rol_id,
                        nombre_completo,
                        email,
                        cargo,
                        nivel,
                        ubicacion
                    ))

            except Exception as e:
                error_msg = f"Error en fila {idx} (UserId: {user_id if 'user_id' in locals() else 'N/A'}): {e}"
                self.stats['errores'].append(error_msg)
                logger.warning(f"⚠️  {error_msg}")

        # Ejecutar BATCH UPDATES
        if batch_updates:
            self.cursor.executemany("""
                UPDATE instituto_Usuario
                SET NombreCompleto = ?,
                    UserEmail = ?,
                    Position = ?,
                    IdUnidadDeNegocio = ?,
                    IdDepartamento = ?,
                    Nivel = ?,
                    Ubicacion = ?
                WHERE UserId = ?
            """, batch_updates)

            self.stats['usuarios_actualizados'] = len(batch_updates)
            logger.info(f"✅ Usuarios actualizados: {len(batch_updates):,}")

        # Ejecutar BATCH INSERTS
        if batch_inserts:
            self.cursor.executemany("""
                INSERT INTO instituto_Usuario
                (UserId, IdUnidadDeNegocio, IdDepartamento, IdRol,
                 NombreCompleto, UserEmail, Position, Nivel, Ubicacion, UserStatus, FechaCreacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active', GETDATE())
            """, batch_inserts)

            self.stats['usuarios_nuevos'] = len(batch_inserts)
            logger.info(f"✅ Usuarios nuevos: {len(batch_inserts):,}")

    # ========================================================================
    # PROCESAMIENTO: TRAINING REPORT (PROGRESO Y CALIFICACIONES)
    # ========================================================================

    def importar_training_report(self, archivo_excel: str) -> Dict[str, Any]:
        """
        Importa archivo Enterprise Training Report (Progreso y Calificaciones)

        Args:
            archivo_excel: Ruta al archivo Excel

        Returns:
            Estadísticas de la importación
        """
        logger.info("="*80)
        logger.info("📊 IMPORTANDO TRAINING REPORT (PROGRESO Y CALIFICACIONES)")
        logger.info("="*80)

        self.stats['tiempo_inicio'] = datetime.now()

        try:
            # 1. EXTRACCIÓN
            logger.info("\n📖 Paso 1/5: Leyendo archivo Excel...")
            df = self._leer_excel_con_deteccion_headers(archivo_excel)
            logger.info(f"✅ Registros leídos: {len(df):,}")

            # 2. DETECCIÓN DE COLUMNAS
            logger.info("\n🔍 Paso 2/5: Detectando columnas...")
            self._detectar_columnas(df)

            # Verificar columnas críticas
            if 'user_id' not in self.detected_columns or 'training_title' not in self.detected_columns:
                raise ValueError("❌ Columnas críticas no encontradas (user_id, training_title)")

            # 3. PRECARGA DE DATOS
            logger.info("\n⚡ Paso 3/5: Precargando datos para optimización...")
            self._precargar_modulos()
            self._precargar_evaluaciones()

            user_ids = df[self.detected_columns['user_id']].astype(str).str.strip().unique().tolist()
            self._precargar_usuarios(user_ids)
            self._precargar_progresos(user_ids)

            # 4. PROCESAMIENTO DE MÓDULOS
            logger.info("\n📋 Paso 4/5: Procesando progreso de módulos...")
            self._procesar_modulos_batch(df)

            # 5. PROCESAMIENTO DE CALIFICACIONES
            logger.info("\n📝 Paso 5/5: Procesando calificaciones de evaluaciones...")
            self._procesar_calificaciones_batch(df)

            # COMMIT
            self.connection.commit()
            logger.info("✅ Transacción confirmada")

            self.stats['tiempo_fin'] = datetime.now()
            self._mostrar_estadisticas()

            return self.stats

        except Exception as e:
            logger.error(f"❌ Error en importación Training Report: {e}")
            self.connection.rollback()
            logger.info("🔄 Transacción revertida")
            self.stats['errores'].append(f"Error fatal: {e}")
            raise

    def _procesar_modulos_batch(self, df: pd.DataFrame):
        """
        Procesa progreso de módulos en batch

        Args:
            df: DataFrame con datos de training
        """
        col_user_id = self.detected_columns['user_id']
        col_titulo = self.detected_columns['training_title']
        col_tipo = self.detected_columns.get('training_type')
        col_estado = self.detected_columns.get('record_status')
        col_fecha_inicio = self.detected_columns.get('start_date')
        col_fecha_fin = self.detected_columns.get('completion_date')
        col_fecha_registro = self.detected_columns.get('transcript_date')

        # Filtrar solo módulos (no pruebas)
        df_modulos = df[df[col_titulo].str.contains('MÓDULO|MODULE', case=False, na=False, regex=True)].copy()

        if len(df_modulos) == 0:
            logger.info("ℹ️  No se encontraron módulos en el archivo")
            return

        logger.info(f"📊 Registros de módulos a procesar: {len(df_modulos):,}")

        batch_updates = []
        batch_inserts = []

        modulos_no_identificados = set()

        for idx, row in df_modulos.iterrows():
            try:
                user_id = str(row[col_user_id]).strip()
                titulo = row[col_titulo]

                # Identificar módulo
                num_modulo = self._extraer_numero_modulo(titulo)

                if not num_modulo:
                    # Intentar fuzzy matching
                    num_modulo = self._identificar_modulo_fuzzy(titulo)

                if not num_modulo:
                    if titulo not in modulos_no_identificados:
                        modulos_no_identificados.add(titulo)
                        logger.warning(f"⚠️  No se pudo identificar módulo: '{titulo}'")
                    continue

                # Obtener/crear módulo
                id_modulo = self._crear_modulo_si_no_existe(num_modulo)

                if not id_modulo:
                    continue

                # Parsear fechas
                fecha_inicio = self._parse_fecha(row.get(col_fecha_inicio)) if col_fecha_inicio else None
                fecha_fin = self._parse_fecha(row.get(col_fecha_fin)) if col_fecha_fin else None
                fecha_registro = self._parse_fecha(row.get(col_fecha_registro)) if col_fecha_registro else None

                # Normalizar estado
                estado_excel = row.get(col_estado, '') if col_estado else ''
                estado = self._normalizar_estatus(estado_excel)
                porcentaje = self._calcular_porcentaje_por_estado(estado)

                # Verificar si existe progreso
                key = (user_id, id_modulo)

                if key in self._cache_progresos:
                    # UPDATE
                    batch_updates.append((
                        estado,
                        fecha_inicio or fecha_registro,
                        fecha_fin,
                        porcentaje,
                        user_id,
                        id_modulo
                    ))
                else:
                    # INSERT
                    batch_inserts.append((
                        user_id,
                        id_modulo,
                        estado,
                        fecha_inicio or fecha_registro or datetime.now(),
                        fecha_fin,
                        porcentaje,
                        datetime.now()
                    ))

            except Exception as e:
                error_msg = f"Error en fila {idx}: {e}"
                self.stats['errores'].append(error_msg)
                logger.warning(f"⚠️  {error_msg}")

        # Ejecutar BATCH UPDATES
        if batch_updates:
            self.cursor.executemany("""
                UPDATE instituto_ProgresoModulo
                SET EstatusModulo = ?,
                    FechaInicio = COALESCE(?, FechaInicio),
                    FechaFinalizacion = ?,
                    PorcentajeAvance = ?
                WHERE UserId = ? AND IdModulo = ?
            """, batch_updates)

            self.stats['progresos_actualizados'] = len(batch_updates)
            logger.info(f"✅ Progresos actualizados: {len(batch_updates):,}")

        # Ejecutar BATCH INSERTS
        if batch_inserts:
            self.cursor.executemany("""
                INSERT INTO instituto_ProgresoModulo
                (UserId, IdModulo, EstatusModulo, FechaInicio, FechaFinalizacion,
                 PorcentajeAvance, FechaAsignacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, batch_inserts)

            self.stats['progresos_insertados'] = len(batch_inserts)
            logger.info(f"✅ Progresos insertados: {len(batch_inserts):,}")

    def _procesar_calificaciones_batch(self, df: pd.DataFrame):
        """
        Procesa calificaciones de evaluaciones en batch

        Args:
            df: DataFrame con datos de training
        """
        col_user_id = self.detected_columns['user_id']
        col_titulo = self.detected_columns['training_title']
        col_tipo = self.detected_columns.get('training_type')
        col_puntaje = self.detected_columns.get('score')

        if not col_tipo or not col_puntaje:
            logger.info("ℹ️  Columnas de tipo o puntaje no encontradas. Saltando calificaciones.")
            return

        # Filtrar solo pruebas/evaluaciones
        df_pruebas = df[
            df[col_tipo].str.contains('Prueba|Test|Assessment|Exam', case=False, na=False, regex=True)
        ].copy()

        if len(df_pruebas) == 0:
            logger.info("ℹ️  No se encontraron evaluaciones en el archivo")
            return

        logger.info(f"📊 Calificaciones a procesar: {len(df_pruebas):,}")

        calificaciones_registradas = 0

        for idx, row in df_pruebas.iterrows():
            try:
                user_id = str(row[col_user_id]).strip()
                titulo = row[col_titulo]
                puntaje = row.get(col_puntaje)

                if pd.isna(puntaje):
                    continue

                try:
                    puntaje_decimal = float(puntaje)
                except:
                    continue

                # Identificar módulo
                num_modulo = self._extraer_numero_modulo(titulo)

                if not num_modulo:
                    num_modulo = self._identificar_modulo_fuzzy(titulo)

                if not num_modulo:
                    continue

                # Obtener/crear módulo
                id_modulo = self._crear_modulo_si_no_existe(num_modulo)

                if not id_modulo:
                    continue

                # Obtener IdInscripcion
                key = (user_id, id_modulo)
                id_inscripcion = self._cache_progresos.get(key)

                if not id_inscripcion:
                    logger.warning(f"⚠️  No se encontró inscripción para {user_id} - Módulo {id_modulo}")
                    continue

                # Obtener/crear evaluación
                id_evaluacion = self._cache_evaluaciones.get(id_modulo)

                if not id_evaluacion:
                    # Crear evaluación
                    nombre_modulo = MODULOS_MAPPING.get(num_modulo)
                    self._crear_evaluacion_para_modulo(id_modulo, nombre_modulo)

                    # Actualizar caché
                    self.cursor.execute("""
                        SELECT IdEvaluacion
                        FROM instituto_Evaluacion
                        WHERE IdModulo = ? AND Activo = 1
                    """, (id_modulo,))
                    row_eval = self.cursor.fetchone()

                    if row_eval:
                        id_evaluacion = row_eval.IdEvaluacion
                        self._cache_evaluaciones[id_modulo] = id_evaluacion

                # Obtener puntaje mínimo
                self.cursor.execute("""
                    SELECT PuntajeMinimo
                    FROM instituto_Evaluacion
                    WHERE IdEvaluacion = ?
                """, (id_evaluacion,))
                row_eval = self.cursor.fetchone()
                puntaje_minimo = row_eval.PuntajeMinimo if row_eval else self.config.default_puntaje_minimo

                # Determinar si aprobó
                aprobado = 1 if puntaje_decimal >= puntaje_minimo else 0

                # Contar intentos previos
                self.cursor.execute("""
                    SELECT COUNT(*) as total
                    FROM instituto_ResultadoEvaluacion
                    WHERE IdInscripcion = ? AND IdEvaluacion = ?
                """, (id_inscripcion, id_evaluacion))

                intento_numero = self.cursor.fetchone().total + 1

                # Insertar resultado
                self.cursor.execute("""
                    INSERT INTO instituto_ResultadoEvaluacion
                    (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado,
                     IntentoNumero, FechaRealizacion)
                    VALUES (?, ?, ?, ?, ?, GETDATE())
                """, (id_inscripcion, id_evaluacion, puntaje_decimal, aprobado, intento_numero))

                calificaciones_registradas += 1

                # Si aprobó, actualizar progreso a Terminado
                if aprobado:
                    self.cursor.execute("""
                        UPDATE instituto_ProgresoModulo
                        SET EstatusModulo = 'Terminado',
                            PorcentajeAvance = 100,
                            FechaFinalizacion = GETDATE()
                        WHERE IdInscripcion = ?
                    """, (id_inscripcion,))

            except Exception as e:
                error_msg = f"Error en calificación {idx}: {e}"
                self.stats['errores'].append(error_msg)
                logger.warning(f"⚠️  {error_msg}")

        self.stats['calificaciones_registradas'] = calificaciones_registradas
        logger.info(f"✅ Calificaciones registradas: {calificaciones_registradas:,}")

    # ========================================================================
    # REPORTES Y ESTADÍSTICAS
    # ========================================================================

    def _mostrar_estadisticas(self):
        """Muestra estadísticas finales de la importación"""
        logger.info("\n" + "="*80)
        logger.info("📊 ESTADÍSTICAS FINALES DE LA IMPORTACIÓN")
        logger.info("="*80)

        tiempo_total = None
        if self.stats['tiempo_inicio'] and self.stats['tiempo_fin']:
            tiempo_total = self.stats['tiempo_fin'] - self.stats['tiempo_inicio']
            logger.info(f"\n⏱️  Tiempo total: {tiempo_total}")

        logger.info("\n👥 USUARIOS:")
        logger.info(f"  • Nuevos:               {self.stats['usuarios_nuevos']:,}")
        logger.info(f"  • Actualizados:         {self.stats['usuarios_actualizados']:,}")

        logger.info("\n📋 MÓDULOS Y PROGRESO:")
        logger.info(f"  • Módulos creados:      {self.stats['modulos_creados']:,}")
        logger.info(f"  • Progresos insertados: {self.stats['progresos_insertados']:,}")
        logger.info(f"  • Progresos actualizados: {self.stats['progresos_actualizados']:,}")

        logger.info("\n📝 EVALUACIONES:")
        logger.info(f"  • Evaluaciones creadas: {self.stats['evaluaciones_creadas']:,}")
        logger.info(f"  • Calificaciones registradas: {self.stats['calificaciones_registradas']:,}")

        logger.info("\n🏢 ORGANIZACIÓN:")
        logger.info(f"  • Unidades creadas:     {self.stats['unidades_creadas']:,}")
        logger.info(f"  • Departamentos creados: {self.stats['departamentos_creados']:,}")

        logger.info(f"\n❌ ERRORES:")
        logger.info(f"  • Total:                {len(self.stats['errores']):,}")

        if self.stats['errores']:
            logger.info("\n⚠️  PRIMEROS 10 ERRORES:")
            for i, error in enumerate(self.stats['errores'][:10], 1):
                logger.info(f"  {i}. {error}")

            if len(self.stats['errores']) > 10:
                logger.info(f"  ... y {len(self.stats['errores']) - 10:,} errores más")

        logger.info("\n" + "="*80)
        logger.info("✅ IMPORTACIÓN COMPLETADA")
        logger.info("="*80)


# ============================================================================
# FUNCIÓN PRINCIPAL DE USO
# ============================================================================

def main():
    """
    Ejemplo de uso del ETL
    """
    # Configuración
    config = ETLConfig(
        server="localhost",
        database="InstitutoHutchison",
        username=None,  # None = Windows Authentication
        password=None,
        batch_size=1000,
        enable_validation=True,
        auto_create_modules=True
    )

    # Crear instancia del ETL
    with ETLInstitutoCompleto(config) as etl:
        # Importar Org Planning (usuarios)
        etl.importar_org_planning("path/to/CSOD_Data_Source_for_Org_Planning.xlsx")

        # Importar Training Report (progreso y calificaciones)
        etl.importar_training_report("path/to/Enterprise_Training_Report.xlsx")


if __name__ == "__main__":
    main()
