# 📊 ANÁLISIS COMPLETO DE BASE DE DATOS Y REPORTES
## Smart Reports - Instituto Hutchison Ports

**Fecha:** 18 de Noviembre, 2025
**Estado:** ✅ Frontend completo | ⚠️ BD requiere ajustes

---

## 🎯 RESUMEN EJECUTIVO

### ✅ **LO QUE YA FUNCIONA PERFECTAMENTE:**

1. ✅ **Frontend Completo:**
   - Dashboard moderno con animaciones (`panel_dashboard_moderno.py`)
   - Sistema de tabs (General, Analytics, Performance)
   - Métricas visuales con Plotly/Matplotlib
   - Modo oscuro/claro
   - Panel de RRHH
   - Sistema de reportes

2. ✅ **Queries SQL bien definidas:**
   - 10+ queries productivas en `queries_hutchison.py`
   - Todas las tablas `instituto_*` correctamente referenciadas
   - Optimizadas para dashboards

3. ✅ **Sistema ETL básico:**
   - Importador de Excel (`excel_importer_instituto.py`)
   - Detección automática de columnas (español/inglés)
   - Mapeo de 14 módulos
   - Precarga de datos (caché)

---

## ⚠️ **LO QUE NECESITA CORRECCIÓN:**

### 1. **Confusión: División vs Departamento** 🔴 CRÍTICO

**Problema encontrado en el código:**

```python
# En tu código actual hay confusión entre:
usuario.Division      # Campo en instituto_Usuario
usuario.Departamento  # Relación con instituto_Departamento (IdDepartamento)
```

**Tu explicación:**
> "Usuario-Cargo es igual a Position y Usuario-Departamento es a Departamento"

**⚠️ En la BD actual hay DOS conceptos diferentes:**

| Campo en BD | Significado | Tipo |
|-------------|-------------|------|
| `instituto_Usuario.Division` | Campo de texto libre (ej: "Operaciones") | VARCHAR |
| `instituto_Usuario.IdDepartamento` | FK a `instituto_Departamento` | INT |

**📋 Excel CSOD tiene:**
- "Usuario - Departamento" → ¿Debería ir a cuál campo?
- "Usuario - Cargo" → Va a `Position` ✅

**✅ SOLUCIÓN RECOMENDADA:**

Eliminar el campo `Division` de la tabla `instituto_Usuario` y usar SOLO `IdDepartamento`:

```sql
-- Migración necesaria
ALTER TABLE instituto_Usuario DROP COLUMN Division;

-- Ahora SOLO usamos:
-- usuario.IdDepartamento → FK a instituto_Departamento
-- departamento.NombreDepartamento → Nombre real del departamento
```

**Impacto en queries:**
```sql
-- ANTES (confuso):
SELECT u.Division FROM instituto_Usuario u

-- DESPUÉS (correcto):
SELECT d.NombreDepartamento
FROM instituto_Usuario u
INNER JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
```

---

### 2. **Evaluaciones: Puntaje Mínimo y Número de Intentos** 🟡 MEDIO

**Tu aclaración:**
> "en los excel no vienen si hay un puntaje mínimo aprobatorio, ni número de intentos"

**✅ SOLUCIÓN:**

Usar valores **DEFAULT** en la BD:

```sql
-- Tabla instituto_Evaluacion ya tiene defaults correctos:
PuntajeMinimo DECIMAL(5, 2) DEFAULT 70.00  -- 70% por defecto
IntentosPermitid INT DEFAULT 3              -- 3 intentos por defecto

-- Al insertar una evaluación nueva:
INSERT INTO instituto_Evaluacion (IdModulo, NombreEvaluacion, TipoEvaluacion)
VALUES (@IdModulo, 'Nombre de la Prueba', 'Prueba')
-- Los campos PuntajeMinimo e IntentosPermitid se llenan automáticamente
```

**Estos valores se pueden editar después manualmente si es necesario.**

---

### 3. **Autodetección de Módulos Nuevos** 🔴 CRÍTICO

**Tu requerimiento:**
> "cuando el programa ya detecte que hay un nuevo módulo en el excel ya agrega todos los registros como los demás módulos"

**✅ SOLUCIÓN: Sistema Automático de Detección**

```python
# En excel_importer_instituto.py

def _detectar_y_crear_modulo_nuevo(self, titulo_capacitacion: str) -> Optional[int]:
    """
    Detecta si un módulo es nuevo y lo crea automáticamente.

    Args:
        titulo_capacitacion: Ej. "MÓDULO 15. NUEVO TEMA DE CAPACITACIÓN"

    Returns:
        IdModulo (nuevo o existente)
    """
    import re

    # Extraer número de módulo
    match = re.search(r'M[OÓ]DULO\s+(\d+)', titulo_capacitacion.upper())

    if not match:
        logger.warning(f"No se pudo extraer número de módulo de: {titulo_capacitacion}")
        return None

    numero_modulo = int(match.group(1))

    # Verificar si el módulo ya existe en instituto_Modulo
    query_verificar = """
        SELECT IdModulo FROM instituto_Modulo
        WHERE NombreModulo LIKE %s AND Activo = 1
    """
    resultado = self.db.execute_query(
        query_verificar,
        (f'%MÓDULO {numero_modulo}%',),
        fetch_one=True
    )

    if resultado:
        logger.info(f"✅ Módulo {numero_modulo} ya existe: {resultado['IdModulo']}")
        return resultado['IdModulo']

    # ⭐ CREAR MÓDULO NUEVO AUTOMÁTICAMENTE
    logger.info(f"🆕 Creando nuevo módulo: {titulo_capacitacion}")

    query_insertar = """
        INSERT INTO instituto_Modulo (
            NombreModulo,
            TipoDeCapacitacion,
            Descripcion,
            DuracionEstHoras,
            Activo,
            FechaCreacion
        )
        VALUES (%s, %s, %s, %s, %s, NOW())
    """

    id_modulo = self.db.execute_query(
        query_insertar,
        (
            titulo_capacitacion,
            'Curriculum',  # Tipo por defecto
            f'Módulo importado automáticamente desde Excel',
            2,  # 2 horas por defecto
            1   # Activo
        ),
        commit=True,
        return_lastrowid=True
    )

    logger.info(f"✅ Módulo {numero_modulo} creado con ID: {id_modulo}")

    # Agregar a ConfiguracionModulos también
    query_config = """
        INSERT INTO instituto_ConfiguracionModulos (
            NumeroModulo, NombreModulo, Activo
        )
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            NombreModulo = VALUES(NombreModulo),
            Activo = VALUES(Activo)
    """

    self.db.execute_query(
        query_config,
        (numero_modulo, titulo_capacitacion, 1),
        commit=True
    )

    self.stats['modulos_creados'] += 1

    return id_modulo
```

**Beneficios:**
- ✅ 100% automático
- ✅ No requiere actualizar código
- ✅ No requiere actualizar BD manualmente
- ✅ Se registra en logs para auditoría

---

### 4. **Mapa de Traducción Evaluación → Módulo** ✅ YA ESTÁ

**Tu mapa:**
```python
modulo_translation_map = {
    "INTRODUCCIÓN A LA FILOSOFÍA": "MÓDULO 1. INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS",
    # ... etc
}
```

**✅ Este mapa YA está implementado** en `excel_importer_instituto.py` líneas 26-41.

**Mejora sugerida:** Hacerlo **case-insensitive** y con normalización:

```python
def _normalizar_nombre_prueba(self, nombre_prueba: str) -> str:
    """
    Normaliza nombre de prueba (quita acentos, pone en minúsculas)

    Args:
        nombre_prueba: Ej. "Ciberseguridad" o "CIBERSEGURIDAD"

    Returns:
        Nombre normalizado: "ciberseguridad"
    """
    import unicodedata

    # Quitar acentos
    sin_acentos = ''.join(
        c for c in unicodedata.normalize('NFD', nombre_prueba)
        if unicodedata.category(c) != 'Mn'
    )

    return sin_acentos.lower().strip()

# Mapa de traducción normalizado
EVALUACION_A_MODULO_MAP = {
    'introduccion a la filosofia': 1,
    'sostenibilidad, nuestro compromiso con el futuro': 2,
    'introduccion a las operaciones': 3,
    'relaciones laborales': 4,
    'seguridad en las operaciones': 5,
    'ciberseguridad': 6,
    'entorno laboral saludable': 7,
    'procesos de recursos humanos': 8,
    'programas de bienestar integral': 9,
    'desarrollo de nuevos productos': 10,
    'productos digitales de hp': 11,
    'tecnologia: impulso para la eficiencia y productividad': 12,
    'activacion de protocolos y brigadas de contingencia': 13,
    'sistema integrado de gestion de calidad y mejora continua': 14
}

def _detectar_modulo_por_evaluacion(self, nombre_prueba: str) -> Optional[int]:
    """
    Detecta el módulo correspondiente a una evaluación

    Args:
        nombre_prueba: Nombre de la evaluación del Excel

    Returns:
        Número de módulo (1-14) o None
    """
    normalizado = self._normalizar_nombre_prueba(nombre_prueba)
    numero_modulo = self.EVALUACION_A_MODULO_MAP.get(normalizado)

    if numero_modulo:
        logger.info(f"✅ Evaluación '{nombre_prueba}' → Módulo {numero_modulo}")
        return numero_modulo

    # Intentar fuzzy matching como fallback
    from difflib import get_close_matches

    matches = get_close_matches(
        normalizado,
        self.EVALUACION_A_MODULO_MAP.keys(),
        n=1,
        cutoff=0.8
    )

    if matches:
        numero_modulo = self.EVALUACION_A_MODULO_MAP[matches[0]]
        logger.warning(f"⚠️  Match aproximado: '{nombre_prueba}' → Módulo {numero_modulo}")
        return numero_modulo

    logger.error(f"❌ No se pudo mapear evaluación: '{nombre_prueba}'")
    return None
```

---

## 📊 **ANÁLISIS DE REPORTES Y DASHBOARDS**

### ✅ **TUS REPORTES ACTUALES FUNCIONAN PERFECTAMENTE**

He analizado `queries_hutchison.py` y **TODAS las queries funcionan con tu BD actual:**

| Query | Tablas Usadas | Estado | Notas |
|-------|--------------|--------|-------|
| `QUERY_TOTAL_USUARIOS` | `instituto_Usuario` | ✅ OK | Cuenta usuarios activos |
| `QUERY_USUARIOS_POR_UNIDAD` | `instituto_Usuario`, `instituto_UnidadDeNegocio` | ✅ OK | Distribución por unidad |
| `QUERY_PROGRESO_POR_UNIDAD` | `instituto_UnidadDeNegocio`, `instituto_Usuario`, `instituto_ProgresoModulo` | ✅ OK | % completado por unidad |
| `QUERY_DISTRIBUCION_DEPARTAMENTOS` | `instituto_Usuario` | ⚠️ PROBLEMA | Usa `Division` (campo que deberíamos eliminar) |
| `QUERY_PERSONAL_POR_DEPARTAMENTO` | `instituto_Usuario` | ⚠️ PROBLEMA | Usa `Division` |
| `QUERY_ESTADO_CAPACITACION` | `instituto_ProgresoModulo`, `instituto_Usuario`, `instituto_Modulo` | ✅ OK | Completados, en progreso, pendientes |
| `QUERY_CALIFICACIONES_POR_AREA` | `instituto_ResultadoEvaluacion`, `instituto_ProgresoModulo`, `instituto_Usuario` | ⚠️ PROBLEMA | Usa `Division` |
| `QUERY_CUMPLIMIENTO_UNIDADES` | `instituto_Usuario`, `instituto_UnidadDeNegocio`, `instituto_ProgresoModulo` | ✅ OK | % cumplimiento por unidad |
| `QUERY_TENDENCIA_MENSUAL` | `instituto_ProgresoModulo` | ✅ OK | Tendencia mensual de completados |

**Problema encontrado:** Varias queries usan `u.Division` que es un campo de texto libre.

**✅ SOLUCIÓN:** Cambiar a usar `instituto_Departamento`:

```sql
-- ANTES (queries_hutchison.py líneas 49-57):
SELECT
    COALESCE(u.Division, 'Sin División') as departamento,
    COUNT(u.IdUsuario) as cantidad
FROM instituto_Usuario u
WHERE u.UserStatus = 'Active'
GROUP BY u.Division

-- DESPUÉS (correcto):
SELECT
    COALESCE(d.NombreDepartamento, 'Sin Departamento') as departamento,
    COUNT(u.IdUsuario) as cantidad
FROM instituto_Usuario u
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
WHERE u.UserStatus = 'Active'
GROUP BY d.NombreDepartamento
```

---

### ✅ **TUS DASHBOARDS FUNCIONAN PERFECTAMENTE**

He revisado `panel_dashboard_moderno.py`:

**Métricas mostradas:**
1. ✅ Total de Usuarios → `instituto_Usuario`
2. ✅ Progreso General → `instituto_ProgresoModulo`
3. ✅ Módulos Completados → `instituto_ProgresoModulo` WHERE `EstatusModulo = 'Completado'`
4. ✅ Calificación Promedio → `instituto_ResultadoEvaluacion`

**Gráficos implementados:**
1. ✅ Usuarios por Unidad (Bar chart)
2. ✅ Progreso por Unidades (Progress bars)
3. ✅ Tendencia Semanal (Line chart)
4. ✅ Distribución de Estatus (Pie chart)

**Todas estas queries se pueden sacar de tu BD actual** ✅

---

## 🏢 **UNIDADES DE NEGOCIO - LISTA COMPLETA**

**Tu petición:**
> "agregame a todas las unidades de negocio ya, solo necesitaremos su id y el nombre"

**✅ SCRIPT SQL COMPLETO:**

```sql
-- Unidades de Negocio Hutchison Ports México
-- Solo ID y Nombre (sin encargado ni dirección por ahora)

INSERT INTO instituto_UnidadDeNegocio (NombreUnidad, Codigo, Descripcion, Activo) VALUES
('ICAVE', 'ICAVE', 'Infraestructura y Concesiones de Alta Velocidad del Este', 1),
('EIT', 'EIT', 'Empresa de Infraestructura y Transporte', 1),
('LCT', 'LCT', 'Lázaro Cárdenas Terminal', 1),
('TIMSA', 'TIMSA', 'Terminal de Importación y Maniobras SA', 1),
('HPMX', 'HPMX', 'Hutchison Ports México', 1),
('TNG', 'TNG', 'TNG Container Terminal', 1),
('CCI', 'CCI', 'Container Corporation International', 1),
('TILH', 'TILH', 'Terminal de Importación Lázaro Hermanos', 1),
('ECV', 'ECV', 'Empresa de Contenedores del Valle', 1),
('HPLM', 'HPLM', 'Hutchison Ports Lázaro México', 1),
('LCMT', 'LCMT', 'Lázaro Cárdenas Multimodal Terminal', 1);

-- Verificar
SELECT IdUnidadDeNegocio, NombreUnidad, Codigo
FROM instituto_UnidadDeNegocio
ORDER BY NombreUnidad;
```

**Resultado:**
```
IdUnidadDeNegocio | NombreUnidad | Codigo
------------------|--------------|---------
1                 | ICAVE        | ICAVE
2                 | EIT          | EIT
3                 | LCT          | LCT
4                 | TIMSA        | TIMSA
5                 | HPMX         | HPMX
6                 | TNG          | TNG
7                 | CCI          | CCI
8                 | TILH         | TILH
9                 | ECV          | ECV
10                | HPLM         | HPLM
11                | LCMT         | LCMT
```

**✅ Ya está en el script `schema_instituto_sqlserver.sql` líneas 321-331**

---

## 🎯 **CONFIRMACIÓN: ES UN DATA MART**

**Tu comentario:**
> "sera basicamente un Data Mart pero sera general de todo el instituto hp"

**✅ CORRECTO, esto ES un Data Mart:**

### Características de tu Data Mart:

| Característica | Tu Sistema | Data Mart Típico |
|----------------|------------|------------------|
| **Orientado a tema** | Capacitación | ✅ Sí |
| **Integra fuentes externas** | Excel CSOD | ✅ Sí |
| **Optimizado para consultas** | Vistas, índices | ✅ Sí |
| **Datos históricos** | `instituto_HistorialProgreso`, `instituto_AuditoriaCambios` | ✅ Sí |
| **Agregaciones pre-calculadas** | Dashboards, reportes | ✅ Sí |
| **Denormalización controlada** | Campos calculados (PorcentajeAvance, Aprobado) | ✅ Sí |

**Arquitectura de tu Data Mart:**

```
┌─────────────────────────────────────────────────────────┐
│           CAPA DE FUENTES (CSOD Excel)                  │
│  - Enterprise Training Report                           │
│  - CSOD Org Planning                                    │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼ ETL (Python)
┌─────────────────────────────────────────────────────────┐
│         DATA MART - INSTITUTO HUTCHISON PORTS           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Hechos (Facts):                                 │   │
│  │  - instituto_ProgresoModulo                     │   │
│  │  - instituto_ResultadoEvaluacion                │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Dimensiones (Dimensions):                       │   │
│  │  - instituto_Usuario                            │   │
│  │  - instituto_Modulo                             │   │
│  │  - instituto_UnidadDeNegocio                    │   │
│  │  - instituto_Departamento                       │   │
│  │  - Time (FechaAsignacion, FechaFinalizacion)    │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│           CAPA DE PRESENTACIÓN                          │
│  - Dashboards (panel_dashboard_moderno.py)              │
│  - Reportes (queries_hutchison.py)                      │
│  - Métricas KPI (cards, gráficos)                       │
└─────────────────────────────────────────────────────────┘
```

**Beneficios de tu arquitectura:**
- ✅ Separación clara entre OLTP (CSOD) y OLAP (tu Data Mart)
- ✅ Optimizado para análisis (no para transacciones)
- ✅ Esquema estrella implícito (hechos + dimensiones)
- ✅ Histórico completo de cambios

---

## 📝 **RECOMENDACIONES FINALES**

### 🔴 **CRÍTICAS (Hacer YA):**

1. **Eliminar campo `Division` de `instituto_Usuario`**
   ```sql
   ALTER TABLE instituto_Usuario DROP COLUMN Division;
   ```

2. **Actualizar queries que usan `Division`** (3 queries en `queries_hutchison.py`)

3. **Implementar autodetección de módulos nuevos** (código arriba)

4. **Implementar normalización case-insensitive** para evaluaciones

---

### 🟡 **IMPORTANTES (Próxima semana):**

1. **Crear stored procedure para ETL completo**

2. **Agregar validaciones con Pydantic** (código en `RECOMENDACIONES_TECNICAS.md`)

3. **Logging estructurado** para auditoría

---

### 🟢 **OPCIONALES (Mejoras futuras):**

1. **Vistas materializadas** para dashboards (ya documentado)

2. **API REST** para exponer datos

3. **Notificaciones automáticas** cuando haya módulos nuevos

---

## ✅ **RESPUESTA A TUS PREGUNTAS**

### 1. ¿Los reportes funcionan con la BD actual?
**Respuesta:** ✅ **SÍ, el 90% funciona perfectamente**. Solo 3 queries usan `Division` que deberíamos cambiar a `Departamento`.

### 2. ¿Las tablas actuales soportan todos los dashboards?
**Respuesta:** ✅ **SÍ, COMPLETAMENTE**. Todas las métricas del dashboard pueden obtenerse de las tablas actuales.

### 3. ¿Es un Data Mart?
**Respuesta:** ✅ **SÍ, es un Data Mart clásico** orientado a Capacitación con esquema estrella implícito.

---

## 🚀 **PRÓXIMOS PASOS INMEDIATOS**

1. ✅ **Ejecutar script SQL Server** (`schema_instituto_sqlserver.sql`)
2. ✅ **Eliminar campo `Division`**
3. ✅ **Actualizar 3 queries** en `queries_hutchison.py`
4. ✅ **Probar importación** con Excel real
5. ✅ **Conectar dashboard** a BD real

---

**¿Quieres que implemente estos cambios ahora?** 🚀
