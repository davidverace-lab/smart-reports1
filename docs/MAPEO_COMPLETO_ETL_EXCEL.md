# 📊 MAPEO COMPLETO ETL - EXCEL A BASE DE DATOS
## Smart Reports - Instituto Hutchison Ports

**Última actualización:** 18 de Noviembre, 2025
**Versión:** 3.0 - Análisis completo de requerimientos ETL

---

## 📋 TABLA DE CONTENIDOS

1. [Introducción](#introducción)
2. [Archivos Excel de Origen](#archivos-excel-de-origen)
3. [Mapeo Detallado - Enterprise Training Report](#mapeo-enterprise-training-report)
4. [Mapeo Detallado - CSOD Org Planning](#mapeo-csod-org-planning)
5. [Lógica de Procesamiento ETL](#lógica-de-procesamiento-etl)
6. [Algoritmo de Cruce de Datos](#algoritmo-de-cruce-de-datos)
7. [Manejo de Estatus y Estados](#manejo-de-estatus-y-estados)
8. [Casos Especiales y Edge Cases](#casos-especiales-y-edge-cases)
9. [Validaciones y Reglas de Negocio](#validaciones-y-reglas-de-negocio)
10. [Escalabilidad a 14 Módulos](#escalabilidad-a-14-módulos)

---

## 🎯 INTRODUCCIÓN

Este documento describe el **mapeo completo y exhaustivo** entre los archivos Excel de CSOD (Cornerstone OnDemand) y la base de datos SQL Server del Instituto Hutchison Ports.

### Objetivo del Sistema ETL

- ✅ **Carga inicial:** Registrar por primera vez todos los usuarios y su progreso
- ✅ **Actualización diaria:** Actualizar estatus de módulos día con día
- ✅ **Sincronización de datos:** Mantener información de usuarios actualizada (correo, departamento, ubicación)
- ✅ **Escalabilidad:** Soportar 14 módulos (actualmente 8 activos)

### Llave Maestra de Identificación

**`UserId`** (Base de Datos) ↔ **`Identificación de usuario`** (Excel)

Esta es la llave primaria de negocio que vincula todos los datos entre sistemas.

---

## 📂 ARCHIVOS EXCEL DE ORIGEN

### 1️⃣ **Enterprise_Training_Report`YYYYMMDD_HH_MM_SS_AM/PM`.xlsx**

**Propósito:** Contiene el estatus, fechas y calificaciones de capacitación de cada usuario.

**Patrón de nombre:**
```
Enterprise_Training_Report20251110_08_27_31_AM.xlsx
Enterprise_Training_Report20251215_02_15_45_PM.xlsx
```

**Columnas:**
- Nombre completo del usuario
- **Identificación de usuario** (LLAVE MAESTRA)
- Tipo de capacitación
- Título de la capacitación
- Versión de capacitación
- Departamento
- Cargo
- Proveedor de capacitación
- Estado del expediente
- Fecha de registro de la transcripción
- Fecha de inicio de la capacitación
- Fecha de finalización de expediente
- Puntuación de la transcripción

---

### 2️⃣ **CSOD_Data_Source_for_Org_Planning_`YYYYMMDD_HH_MM_SS_AM/PM`.xlsx**

**Propósito:** Contiene datos organizacionales y de contacto de usuarios.

**Patrón de nombre:**
```
CSOD_Data_Source_for_Org_Planning_20251110_08_26_04_AM.xlsx
```

**Columnas:**
- **Usuario - Identificación de usuario** (LLAVE MAESTRA)
- Usuario - Gerente - Identificación de usuario
- Usuario - Nombre completo del usuario
- Usuario - Cargo
- Usuario - Departamento
- Usuario - Tipo de usuario
- Usuario - Fecha de contratación original del usuario
- Usuario - Ciudad
- Usuario - País del usuario
- Usuario - Estado/Provincia
- **Usuario - Correo electrónico del usuario**
- Usuario - Número de teléfono del usuario
- **Usuario - Ubicación**
- Usuario - Código postal
- Usuario - GUID del usuario

---

## 📊 MAPEO ENTERPRISE TRAINING REPORT

### 🔍 Sección 1: Obtención de Estatus y Fechas de Módulos (Curriculums)

#### Proceso Manual Actual (a automatizar):

1. **Filtrar** columna `Título de capacitación` → buscar "MÓDULO"
2. **Filtrar** columna `Estado del expediente` → "Terminado"
3. **Extraer** `Fecha de registro de la transcripción`
4. **Extraer** `Fecha de finalización de expediente`

#### Mapeo de Columnas:

| Columna Excel | Campo BD | Tabla BD | Tipo | Notas |
|--------------|----------|----------|------|-------|
| **Identificación de usuario** | `UserID` | `instituto_Usuario` | VARCHAR(100) | ⚠️ **LLAVE MAESTRA** - Se convierte a IdUsuario INT en ProgresoModulo |
| **Título de la capacitación** | `NombreModulo` | `instituto_Modulo` | VARCHAR(255) | Se busca/crea en instituto_Modulo |
| **Tipo de capacitación** | `TipoDeCapacitacion` | `instituto_Modulo` | VARCHAR(50) | 'Curriculum' o 'Prueba' |
| **Estado del expediente** | `EstatusModulo` | `instituto_ProgresoModulo` | VARCHAR(50) | Valores: Ver tabla de estados abajo |
| **Fecha de registro de la transcripción** | `FechaAsignacion` | `instituto_ProgresoModulo` | DATETIME | Cuando se registró el módulo |
| **Fecha de inicio de la capacitación** | `FechaInicio` | `instituto_ProgresoModulo` | DATETIME | Cuando el usuario comenzó |
| **Fecha de finalización de expediente** | `FechaFinalizacion` | `instituto_ProgresoModulo` | DATETIME | ⚠️ Solo si estado = "Terminado" |

#### 🎓 Lista de Módulos (Curriculums)

**⚠️ IMPORTANTE:** Los nombres en el Excel tienen espacios y puntos irregulares.

```
MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS
MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO
MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES
MÓDULO 4 . RELACIONES LABORALES
MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES
MÓDULO 6 . CIBERSEGURIDAD
MÓDULO 7 . ENTORNO LABORAL SALUDABLE
MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS
MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL
MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS
MÓDULO 11 . PRODUCTOS DIGITALES DE HP
MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD
MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA
MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA
```

**Algoritmo de Detección:**
```python
def detectar_modulo(titulo_capacitacion):
    """
    Detecta el módulo a partir del título de capacitación.
    Retorna: IdModulo o None
    """
    titulo_upper = titulo_capacitacion.upper().strip()

    # Buscar patrón "MÓDULO X" donde X es 1-14
    import re
    match = re.search(r'M[OÓ]DULO\s+(\d+)', titulo_upper)

    if match:
        numero_modulo = int(match.group(1))
        if 1 <= numero_modulo <= 14:
            # Buscar en BD: instituto_modulo donde NombreModulo LIKE '%MÓDULO {numero_modulo}%'
            return buscar_modulo_en_bd(numero_modulo)

    return None
```

---

### 📝 Sección 2: Obtención de Calificaciones (Pruebas/Evaluaciones)

#### Proceso Manual Actual (a automatizar):

1. **Filtrar** columna `Tipo de capacitación` → "Prueba"
2. **Extraer** nombre de la prueba (viene sin "MÓDULO X.")
3. **Extraer** `Puntuación de la transcripción`

#### Mapeo de Columnas:

| Columna Excel | Campo BD | Tabla BD | Tipo | Notas |
|--------------|----------|----------|------|-------|
| **Tipo de capacitación** | `TipoDeCapacitacion` | `instituto_Modulo` | VARCHAR(50) | Valor = "Prueba" (para evaluaciones) |
| **Título de la capacitación** | `NombreEvaluacion` | `instituto_Evaluacion` | VARCHAR(255) | Nombre de la evaluación (sin "MÓDULO X.") |
| **Puntuación de la transcripción** | `PuntajeObtenido` | `instituto_ResultadoEvaluacion` | DECIMAL(5,2) | Calificación 0-100 |
| **Fecha de finalización de expediente** | `FechaRealizacion` | `instituto_ResultadoEvaluacion` | DATETIME | Cuando hizo la prueba |

#### 🎯 Lista de Pruebas/Evaluaciones

**⚠️ ADVERTENCIA:** Los nombres de las pruebas vienen en diferentes formatos de capitalización:
- TODO MAYÚSCULAS: `INTRODUCCIÓN A LAS OPERACIONES`
- Todo minúsculas: `ciberseguridad`
- Mixtas: `Seguridad en las Operaciones`

```
INTRODUCCIÓN A LAS OPERACIONES
Seguridad en las Operaciones
Ciberseguridad
RELACIONES LABORALES
Procesos de Recursos Humanos
INTRODUCCIÓN A LA FILOSOFÍA
SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO
Entorno Laboral Saludable
```

**⚠️ MAPEO MANUAL REQUERIDO:**

| Nombre Prueba (Excel) | Módulo Correspondiente |
|----------------------|------------------------|
| INTRODUCCIÓN A LA FILOSOFÍA | MÓDULO 1 |
| SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO | MÓDULO 2 |
| INTRODUCCIÓN A LAS OPERACIONES | MÓDULO 3 |
| RELACIONES LABORALES | MÓDULO 4 |
| Seguridad en las Operaciones | MÓDULO 5 |
| Ciberseguridad | MÓDULO 6 |
| Entorno Laboral Saludable | MÓDULO 7 |
| Procesos de Recursos Humanos | MÓDULO 8 |

**Algoritmo de Detección:**
```python
# Diccionario de normalización (case-insensitive)
MAPEO_PRUEBAS_MODULOS = {
    'introducción a la filosofía': 1,
    'introducción a la filosofia': 1,
    'sostenibilidad, nuestro compromiso con el futuro': 2,
    'introducción a las operaciones': 3,
    'introduccion a las operaciones': 3,
    'relaciones laborales': 4,
    'seguridad en las operaciones': 5,
    'ciberseguridad': 6,
    'entorno laboral saludable': 7,
    'procesos de recursos humanos': 8,
    'programas de bienestar integral': 9,
    'desarrollo de nuevos productos': 10,
    'productos digitales de hp': 11,
    'tecnología: impulso para la eficiencia y productividad': 12,
    'tecnologia: impulso para la eficiencia y productividad': 12,
    'activación de protocolos y brigadas de contingencia': 13,
    'activacion de protocolos y brigadas de contingencia': 13,
    'sistema integrado de gestión de calidad y mejora continua': 14,
    'sistema integrado de gestion de calidad y mejora continua': 14
}

def detectar_prueba(titulo_prueba):
    """
    Detecta el módulo al que pertenece una prueba.
    Retorna: numero_modulo o None
    """
    titulo_normalizado = titulo_prueba.lower().strip()

    # Quitar caracteres especiales y normalizar
    import unicodedata
    titulo_normalizado = unicodedata.normalize('NFKD', titulo_normalizado)

    return MAPEO_PRUEBAS_MODULOS.get(titulo_normalizado)
```

---

### 👤 Sección 3: Actualización de Datos de Usuarios desde Training Report

| Columna Excel | Campo BD | Tabla BD | Tipo | Acción |
|--------------|----------|----------|------|--------|
| **Departamento** | `NombreDepartamento` → `IdDepartamento` | `instituto_Departamento` → `instituto_Usuario` | INT (FK) | Buscar/crear departamento, actualizar FK |
| **Cargo** | Se mapea a `IdPosicion` | `instituto_Posicion` → `instituto_Usuario` | INT (FK) | Buscar/crear posición |

**⚠️ NOTA:** Si el `Departamento` en el Excel no existe en `instituto_Departamento`, se debe crear automáticamente con una unidad de negocio por defecto (ej: TNG).

---

## 🏢 MAPEO CSOD ORG PLANNING

### 👥 Datos Organizacionales de Usuarios

| Columna Excel | Campo BD | Tabla BD | Tipo | Acción |
|--------------|----------|----------|------|--------|
| **Usuario - Identificación de usuario** | `UserId` | `instituto_Usuario` | VARCHAR(100) | ⚠️ LLAVE MAESTRA |
| **Usuario - Nombre completo del usuario** | `NombreCompleto` | `instituto_Usuario` | VARCHAR(255) | INSERT/UPDATE |
| **Usuario - Correo electrónico del usuario** | `UserEmail` | `instituto_Usuario` | VARCHAR(255) | ⚠️ Detectar cambios |
| **Usuario - Cargo** | `IdPosicion` | `instituto_Posicion` → `instituto_Usuario` | INT (FK) | Buscar/crear posición |
| **Usuario - Departamento** | `NombreDepartamento` → `IdDepartamento` | `instituto_Departamento` | INT (FK) | Buscar/crear |
| **Usuario - Ubicación** | `Ubicacion` | `instituto_Usuario` | VARCHAR(255) | ⚠️ Sincronizar |
| **Usuario - Nivel** | `Nivel` | `instituto_Usuario` | INT | Nivel jerárquico (1-10) |

### Columnas No Mapeadas (pero disponibles):

| Columna Excel | Potencial Uso Futuro |
|--------------|---------------------|
| Usuario - Gerente - Identificación de usuario | Jerarquía organizacional |
| Usuario - Tipo de usuario | Clasificación de empleados |
| Usuario - Fecha de contratación original del usuario | Antigüedad/seniority |
| Usuario - Ciudad | Geolocalización |
| Usuario - País del usuario | Expansión internacional |
| Usuario - Estado/Provincia | Análisis regional |
| Usuario - Número de teléfono del usuario | Contacto directo |
| Usuario - Código postal | Análisis geográfico |
| Usuario - GUID del usuario | ID alternativo de CSOD |

---

## ⚙️ LÓGICA DE PROCESAMIENTO ETL

### 🔄 Flujo General del ETL

```
┌─────────────────────────────────────────────────────────────┐
│         PASO 1: CARGAR Y VALIDAR ARCHIVOS EXCEL             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│    PASO 2: PROCESAR CSOD ORG PLANNING (Usuarios nuevos)    │
│    - Crear/actualizar usuarios                              │
│    - Sincronizar departamentos                              │
│    - Actualizar correos y ubicaciones                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 3: PROCESAR ENTERPRISE TRAINING REPORT (Progreso)    │
│    - Actualizar estatus de módulos                          │
│    - Registrar fechas de avance                             │
│    - Insertar calificaciones de evaluaciones                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│        PASO 4: VALIDACIÓN Y REPORTES DE INCONSISTENCIAS     │
└─────────────────────────────────────────────────────────────┘
```

---

### 📝 PASO 2: Procesamiento de CSOD Org Planning

```python
def procesar_org_planning(df_org_planning, conexion_bd):
    """
    Procesa el archivo CSOD Org Planning para crear/actualizar usuarios.

    Returns:
        dict: {
            'usuarios_nuevos': int,
            'usuarios_actualizados': int,
            'departamentos_creados': int,
            'errores': list
        }
    """
    usuarios_nuevos = 0
    usuarios_actualizados = 0
    departamentos_creados = 0
    errores = []

    for index, row in df_org_planning.iterrows():
        try:
            # Extraer datos del Excel
            user_id = row['Usuario - Identificación de usuario']
            nombre_completo = row['Usuario - Nombre completo del usuario']
            email = row['Usuario - Correo electrónico del usuario']
            cargo = row['Usuario - Cargo']
            departamento_nombre = row['Usuario - Departamento']
            ubicacion = row['Usuario - Ubicación']

            # PASO 2.1: Verificar si el usuario ya existe
            usuario_existe = verificar_usuario_existe(conexion_bd, user_id)

            # PASO 2.2: Buscar/crear departamento
            id_departamento = None
            if departamento_nombre and str(departamento_nombre).strip():
                id_departamento = buscar_o_crear_departamento(
                    conexion_bd,
                    nombre_departamento=departamento_nombre,
                    id_unidad_negocio_default=6  # TNG por defecto
                )
                if id_departamento is None:  # Se creó nuevo
                    departamentos_creados += 1

            # PASO 2.3: Crear o actualizar usuario
            if usuario_existe:
                actualizar_usuario(
                    conexion_bd,
                    user_id=user_id,
                    nombre_completo=nombre_completo,
                    email=email,
                    cargo=cargo,
                    id_departamento=id_departamento,
                    ubicacion=ubicacion
                )
                usuarios_actualizados += 1
            else:
                crear_usuario(
                    conexion_bd,
                    user_id=user_id,
                    nombre_completo=nombre_completo,
                    email=email,
                    cargo=cargo,
                    id_departamento=id_departamento,
                    ubicacion=ubicacion,
                    id_rol=3  # Rol "Empleado" por defecto
                )
                usuarios_nuevos += 1

        except Exception as e:
            errores.append({
                'fila': index,
                'user_id': user_id if 'user_id' in locals() else 'N/A',
                'error': str(e)
            })
            continue

    return {
        'usuarios_nuevos': usuarios_nuevos,
        'usuarios_actualizados': usuarios_actualizados,
        'departamentos_creados': departamentos_creados,
        'errores': errores
    }
```

---

### 📚 PASO 3: Procesamiento de Enterprise Training Report

```python
def procesar_training_report(df_training_report, conexion_bd):
    """
    Procesa el archivo Enterprise Training Report para actualizar progreso y calificaciones.

    Returns:
        dict: {
            'progresos_actualizados': int,
            'calificaciones_registradas': int,
            'modulos_no_encontrados': list,
            'usuarios_no_encontrados': list,
            'errores': list
        }
    """
    progresos_actualizados = 0
    calificaciones_registradas = 0
    modulos_no_encontrados = []
    usuarios_no_encontrados = []
    errores = []

    for index, row in df_training_report.iterrows():
        try:
            # Extraer datos básicos
            user_id = row['Identificación de usuario']
            tipo_capacitacion = row['Tipo de capacitación']
            titulo_capacitacion = row['Título de la capacitación']
            estado_expediente = row['Estado del expediente']
            fecha_registro = row['Fecha de registro de la transcripción']
            fecha_inicio = row['Fecha de inicio de la capacitación']
            fecha_finalizacion = row['Fecha de finalización de expediente']

            # PASO 3.1: Verificar que el usuario existe
            id_usuario = obtener_id_usuario_por_userid(conexion_bd, user_id)
            if not id_usuario:
                usuarios_no_encontrados.append(user_id)
                continue

            # PASO 3.2: Determinar si es Módulo (Curriculum) o Prueba (Evaluación)
            if 'MÓDULO' in titulo_capacitacion.upper():
                # ES UN MÓDULO (CURRICULUM)
                resultado = procesar_modulo(
                    conexion_bd,
                    user_id=user_id,
                    id_usuario=id_usuario,
                    titulo_capacitacion=titulo_capacitacion,
                    estado_expediente=estado_expediente,
                    fecha_registro=fecha_registro,
                    fecha_inicio=fecha_inicio,
                    fecha_finalizacion=fecha_finalizacion
                )

                if resultado['exito']:
                    progresos_actualizados += 1
                else:
                    modulos_no_encontrados.append(titulo_capacitacion)

            elif 'PRUEBA' in tipo_capacitacion.upper() or 'TEST' in tipo_capacitacion.upper():
                # ES UNA PRUEBA (EVALUACIÓN)
                puntuacion = row['Puntuación de la transcripción']

                resultado = procesar_evaluacion(
                    conexion_bd,
                    user_id=user_id,
                    id_usuario=id_usuario,
                    titulo_prueba=titulo_capacitacion,
                    puntuacion=puntuacion,
                    fecha_realizacion=fecha_finalizacion
                )

                if resultado['exito']:
                    calificaciones_registradas += 1
                else:
                    modulos_no_encontrados.append(titulo_capacitacion)

        except Exception as e:
            errores.append({
                'fila': index,
                'user_id': user_id if 'user_id' in locals() else 'N/A',
                'titulo': titulo_capacitacion if 'titulo_capacitacion' in locals() else 'N/A',
                'error': str(e)
            })
            continue

    return {
        'progresos_actualizados': progresos_actualizados,
        'calificaciones_registradas': calificaciones_registradas,
        'modulos_no_encontrados': list(set(modulos_no_encontrados)),
        'usuarios_no_encontrados': list(set(usuarios_no_encontrados)),
        'errores': errores
    }
```

---

### 🎯 Función: Procesar Módulo

```sql
-- Stored Procedure para SQL Server
CREATE OR ALTER PROCEDURE sp_UpsertProgresoModulo
    @UserID VARCHAR(100),
    @NumeroModulo INT,
    @EstatusModulo VARCHAR(50),
    @FechaAsignacion DATETIME,
    @FechaInicio DATETIME = NULL,
    @FechaFinalizacion DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @IdUsuario INT;
    DECLARE @IdModulo INT;

    -- 1. Obtener IdUsuario
    SELECT @IdUsuario = IdUsuario
    FROM instituto_Usuario
    WHERE UserId = @UserID;

    IF @IdUsuario IS NULL
    BEGIN
        RAISERROR('Usuario no encontrado: %s', 16, 1, @UserID);
        RETURN;
    END

    -- 2. Obtener IdModulo
    SELECT @IdModulo = IdModulo
    FROM instituto_Modulo
    WHERE NombreModulo LIKE '%MÓDULO ' + CAST(@NumeroModulo AS VARCHAR) + '%'
      AND Activo = 1;

    IF @IdModulo IS NULL
    BEGIN
        RAISERROR('Módulo no encontrado: %d', 16, 1, @NumeroModulo);
        RETURN;
    END

    -- 3. INSERT o UPDATE
    IF EXISTS (
        SELECT 1 FROM instituto_ProgresoModulo
        WHERE IdUsuario = @IdUsuario AND IdModulo = @IdModulo
    )
    BEGIN
        -- UPDATE
        UPDATE instituto_ProgresoModulo
        SET
            EstatusModulo = @EstatusModulo,
            FechaInicio = COALESCE(@FechaInicio, FechaInicio),
            FechaFinalizacion = CASE
                WHEN @EstatusModulo IN ('Terminado', 'Completado') THEN @FechaFinalizacion
                ELSE FechaFinalizacion
            END
        WHERE IdUsuario = @IdUsuario AND IdModulo = @IdModulo;
    END
    ELSE
    BEGIN
        -- INSERT
        INSERT INTO instituto_ProgresoModulo (
            IdUsuario,
            IdModulo,
            EstatusModulo,
            FechaAsignacion,
            FechaInicio,
            FechaFinalizacion
        )
        VALUES (
            @IdUsuario,
            @IdModulo,
            @EstatusModulo,
            @FechaAsignacion,
            @FechaInicio,
            CASE WHEN @EstatusModulo IN ('Terminado', 'Completado') THEN @FechaFinalizacion ELSE NULL END
        );
    END

    RETURN 0;
END;
GO
```

---

## 📋 MANEJO DE ESTATUS Y ESTADOS

### Tabla de Mapeo de Estados

| Estado en Excel | Estado Normalizado BD | FechaFinalizacion | Descripción |
|----------------|----------------------|------------------|-------------|
| **Terminado** | Terminado | ✅ Registrada | Usuario completó el módulo exitosamente |
| **Completado** | Terminado | ✅ Registrada | Sinónimo de "Terminado" |
| **Completed** | Terminado | ✅ Registrada | Versión en inglés |
| **En progreso** | En progreso | ❌ NULL | Usuario está cursando activamente |
| **En progreso / Vencido** | En progreso | ❌ NULL | Usuario está cursando pero pasó la fecha límite |
| **In Progress** | En progreso | ❌ NULL | Versión en inglés |
| **Registrado** | Registrado | ❌ NULL | Usuario asignado pero no ha iniciado |
| **Registrado / Vencido** | Registrado | ❌ NULL | Usuario asignado, no inició, fecha pasada |
| **Registered** | Registrado | ❌ NULL | Versión en inglés |
| **No iniciado** | No iniciado | ❌ NULL | Usuario no ha comenzado |
| **Not Started** | No iniciado | ❌ NULL | Versión en inglés |

### 🔍 Lógica de Relleno de Campos Vacíos

**Requerimiento del usuario:**
> "si un usuario no ha terminado algún módulo, rellenes el campo con el mismo proceso con 'Registrado', 'Registrado/Vencido', 'En progreso/Vencido'"

**Implementación:**

```python
def determinar_estatus_faltante(user_id, id_modulo, fecha_vencimiento, conexion_bd):
    """
    Si un usuario no tiene registro de progreso para un módulo asignado,
    determinar el estatus que debe tener según la lógica de negocio.

    Args:
        user_id: ID del usuario
        id_modulo: ID del módulo
        fecha_vencimiento: Fecha límite del módulo (puede ser None)
        conexion_bd: Conexión a la base de datos

    Returns:
        str: Estatus a asignar ('Registrado', 'Registrado / Vencido', etc.)
    """
    from datetime import datetime

    # Verificar si el módulo está asignado al usuario
    modulo_asignado = verificar_modulo_asignado_a_usuario(
        conexion_bd, user_id, id_modulo
    )

    if not modulo_asignado:
        return None  # No debe tener registro

    # Verificar si hay algún registro de actividad
    tiene_actividad = verificar_actividad_usuario_modulo(
        conexion_bd, user_id, id_modulo
    )

    # Determinar estatus
    ahora = datetime.now()

    if tiene_actividad:
        # Usuario tiene actividad, está en progreso
        if fecha_vencimiento and ahora > fecha_vencimiento:
            return 'En progreso / Vencido'
        else:
            return 'En progreso'
    else:
        # Usuario no tiene actividad, solo registrado
        if fecha_vencimiento and ahora > fecha_vencimiento:
            return 'Registrado / Vencido'
        else:
            return 'Registrado'
```

---

## 🧮 ALGORITMO DE CRUCE DE DATOS

### 🔄 Diagrama de Flujo del ETL

```
┌────────────────────────────────────────────────────────────────┐
│  INICIO: Cargar Archivos Excel                                 │
│  - Enterprise_Training_Report{timestamp}.xlsx                  │
│  - CSOD_Data_Source_for_Org_Planning_{timestamp}.xlsx          │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  FASE 1: NORMALIZACIÓN Y VALIDACIÓN                            │
│  ✓ Detectar columnas (español/inglés)                          │
│  ✓ Validar columnas requeridas                                 │
│  ✓ Limpiar datos (trim, normalizar fechas)                     │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  FASE 2: PROCESAR USUARIOS (Org Planning)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Para cada fila:                                         │  │
│  │  1. Extraer UserID (llave maestra)                       │  │
│  │  2. ¿Usuario existe en BD?                               │  │
│  │     ├─ SÍ → UPDATE (email, ubicación, cargo, depto)      │  │
│  │     └─ NO → INSERT nuevo usuario                         │  │
│  │  3. Buscar/Crear departamento si es nuevo                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  FASE 3: PROCESAR PROGRESO (Training Report)                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Para cada fila:                                         │  │
│  │  1. Extraer UserID                                       │  │
│  │  2. ¿Usuario existe en BD? ─── NO ──→ ERROR / SKIP      │  │
│  │     │                                                     │  │
│  │     └─ SÍ ↓                                              │  │
│  │  3. ¿Tipo = "Prueba"?                                    │  │
│  │     ├─ SÍ → Procesar como EVALUACIÓN (Fase 3B)           │  │
│  │     └─ NO → ¿Contiene "MÓDULO"?                          │  │
│  │         ├─ SÍ → Procesar como MÓDULO (Fase 3A)           │  │
│  │         └─ NO → SKIP                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
          │                                      │
          │ FASE 3A: MÓDULOS                    │ FASE 3B: EVALUACIONES
          ▼                                      ▼
┌─────────────────────────────┐   ┌────────────────────────────────┐
│ 1. Detectar número módulo   │   │ 1. Detectar nombre prueba      │
│ 2. Buscar IdModulo en BD    │   │ 2. Mapear a número módulo      │
│ 3. ¿Existe progreso?        │   │ 3. Obtener IdInscripcion       │
│    ├─ SÍ → UPDATE progreso  │   │ 4. Buscar IdEvaluacion         │
│    └─ NO → INSERT progreso  │   │ 5. INSERT resultado evaluación │
│ 4. Actualizar estatus       │   │ 6. ¿Aprobado?                  │
│ 5. Registrar fechas         │   │    └─ SÍ → UPDATE progreso     │
└─────────────────────────────┘   │         a "Terminado"          │
                                  └────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  FASE 4: COMPLETAR DATOS FALTANTES                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Para cada usuario en BD:                                │  │
│  │  1. Obtener módulos asignados (según departamento)       │  │
│  │  2. Para cada módulo asignado:                           │  │
│  │     ¿Tiene registro en instituto_progresomodulo?         │  │
│  │     └─ NO → INSERT con estatus:                          │  │
│  │         - "Registrado" si no venció                      │  │
│  │         - "Registrado / Vencido" si venció               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  FASE 5: VALIDACIONES Y REPORTES                               │
│  ✓ Usuarios sin progreso                                       │
│  ✓ Módulos no encontrados                                      │
│  ✓ Errores de procesamiento                                    │
│  ✓ Estadísticas de importación                                 │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                         [FIN ETL]
```

---

## 🔧 CASOS ESPECIALES Y EDGE CASES

### ⚠️ Caso 1: Usuario en Training Report pero no en Org Planning

**Escenario:** El Excel de entrenamiento incluye un usuario que no aparece en el Excel organizacional.

**Solución:**
1. ❌ **NO PROCESAR** datos de training de ese usuario
2. ⚠️ **REGISTRAR ADVERTENCIA** en log de errores
3. 📝 **NOTIFICAR** a RRHH que hay un usuario sin datos organizacionales

```python
if user_id not in usuarios_org_planning:
    log_advertencia(f"Usuario {user_id} tiene datos de training pero no existe en Org Planning")
    continue  # Saltar procesamiento
```

---

### ⚠️ Caso 2: Cambio de Departamento

**Escenario:** Un usuario cambia de departamento entre importaciones.

**Solución:**
1. ✅ **ACTUALIZAR** `IdDepartamento` en `instituto_usuario`
2. ✅ **VERIFICAR** si el nuevo departamento tiene módulos obligatorios diferentes
3. ✅ **ASIGNAR** nuevos módulos obligatorios del nuevo departamento
4. 📝 **REGISTRAR** en `instituto_historialprogreso` (comentario: "Cambio de departamento")

---

### ⚠️ Caso 3: Cambio de Correo Electrónico

**Escenario:** El correo del usuario cambió en Org Planning.

**Solución:**
1. ✅ **ACTUALIZAR** `UserEmail` en `instituto_usuario`
2. ⚠️ **VALIDAR** formato de email
3. 📝 **REGISTRAR** en auditoría

---

### ⚠️ Caso 4: Módulo no Encontrado en BD

**Escenario:** El Excel menciona "MÓDULO 10. DESARROLLO DE NUEVOS PRODUCTOS" pero no existe en la BD.

**Solución:**
1. ⚠️ **REGISTRAR ERROR** en log de procesamiento
2. ❌ **NO PROCESAR** esa fila
3. 📝 **GENERAR REPORTE** al final del ETL con módulos faltantes
4. 🔔 **NOTIFICAR** al administrador que debe crear el módulo

---

### ⚠️ Caso 5: Nombre de Prueba No Reconocido

**Escenario:** Aparece una prueba llamada "Examen Final - Seguridad" que no está en el mapeo.

**Solución:**
1. 🔍 **INTENTAR MATCH PARCIAL** usando fuzzy matching
2. ⚠️ Si no hay match > 80%, **REGISTRAR ERROR**
3. 📝 **AGREGAR AL REPORTE** de pruebas no reconocidas
4. 🔧 **ACTUALIZAR MAPEO** manualmente

```python
from fuzzywuzzy import fuzz

def buscar_prueba_fuzzy(titulo_prueba, umbral=80):
    """
    Busca la prueba más similar usando fuzzy matching.
    """
    mejor_match = None
    mejor_score = 0

    for prueba_conocida, numero_modulo in MAPEO_PRUEBAS_MODULOS.items():
        score = fuzz.ratio(titulo_prueba.lower(), prueba_conocida)
        if score > mejor_score:
            mejor_score = score
            mejor_match = numero_modulo

    if mejor_score >= umbral:
        return mejor_match
    else:
        return None
```

---

### ⚠️ Caso 6: Fechas Inválidas o Futuras

**Escenario:** `FechaFinalizacion` es mayor que la fecha actual.

**Solución:**
1. ⚠️ **VALIDAR** fechas antes de insertar
2. ❌ Si fecha es futura, **REGISTRAR ERROR**
3. 🔧 **USAR** fecha de importación como fallback

```python
from datetime import datetime

def validar_fecha(fecha, nombre_campo):
    """
    Valida que la fecha sea válida y no futura.
    """
    if fecha is None or pd.isna(fecha):
        return None

    try:
        fecha_dt = pd.to_datetime(fecha)

        # Verificar que no sea futura
        if fecha_dt > datetime.now():
            log_advertencia(f"{nombre_campo} es futura: {fecha_dt}, usando fecha actual")
            return datetime.now()

        return fecha_dt
    except:
        log_error(f"Fecha inválida en {nombre_campo}: {fecha}")
        return None
```

---

## ✅ VALIDACIONES Y REGLAS DE NEGOCIO

### 1️⃣ Validaciones de Usuario

| Validación | Regla | Acción en Error |
|-----------|-------|-----------------|
| UserID no vacío | `UserID IS NOT NULL AND UserID != ''` | SKIP fila |
| Email válido | Formato `usuario@dominio.com` | Registrar advertencia, continuar |
| Nombre completo no vacío | `NombreCompleto != ''` | SKIP fila |
| UserID único | No duplicados en BD | UPDATE en lugar de INSERT |

---

### 2️⃣ Validaciones de Progreso

| Validación | Regla | Acción en Error |
|-----------|-------|-----------------|
| Usuario existe | `UserId` debe estar en `instituto_Usuario` | SKIP fila, registrar error |
| Módulo existe | `IdModulo` debe existir en `instituto_Modulo` | SKIP fila, registrar módulo faltante |
| Fechas consistentes | `FechaInicio <= FechaFinalizacion` | Ajustar o registrar advertencia |
| Estatus válido | Debe estar en lista de estados permitidos | Normalizar o registrar advertencia |

---

### 3️⃣ Validaciones de Evaluación

| Validación | Regla | Acción en Error |
|-----------|-------|-----------------|
| Puntuación válida | `0 <= PuntajeObtenido <= 100` | SKIP fila, registrar error |
| Evaluación existe | Debe haber evaluación para el módulo | Crear evaluación default |
| IdInscripcion existe | Usuario debe tener progreso en el módulo | SKIP fila, registrar error |
| Aprobación consistente | Si aprobó, progreso debe ser "Terminado" | Actualizar progreso |

---

## 📈 ESCALABILIDAD A 14 MÓDULOS

### 🔧 Configuración Dinámica

Para soportar nuevos módulos sin cambiar código, implementar tabla de configuración:

```sql
-- Tabla de configuración de módulos
CREATE TABLE instituto_configuracion_modulos (
    IdConfigModulo INT IDENTITY(1,1) PRIMARY KEY,
    NumeroModulo INT NOT NULL UNIQUE,
    NombreModulo VARCHAR(255) NOT NULL,
    NombrePrueba VARCHAR(255), -- Nombre de la evaluación en Excel
    Activo BIT DEFAULT 1,
    FechaActivacion DATETIME DEFAULT GETDATE(),
    FechaCreacion DATETIME DEFAULT GETDATE()
);

-- Insertar configuración de 14 módulos
INSERT INTO instituto_configuracion_modulos (NumeroModulo, NombreModulo, NombrePrueba, Activo) VALUES
(1, 'MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS', 'INTRODUCCIÓN A LA FILOSOFÍA', 1),
(2, 'MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 'SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 1),
(3, 'MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES', 'INTRODUCCIÓN A LAS OPERACIONES', 1),
(4, 'MÓDULO 4 . RELACIONES LABORALES', 'RELACIONES LABORALES', 1),
(5, 'MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES', 'Seguridad en las Operaciones', 1),
(6, 'MÓDULO 6 . CIBERSEGURIDAD', 'Ciberseguridad', 1),
(7, 'MÓDULO 7 . ENTORNO LABORAL SALUDABLE', 'Entorno Laboral Saludable', 1),
(8, 'MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS', 'Procesos de Recursos Humanos', 1),
(9, 'MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL', NULL, 0), -- No hay prueba aún
(10, 'MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS', NULL, 0),
(11, 'MÓDULO 11 . PRODUCTOS DIGITALES DE HP', NULL, 0),
(12, 'MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD', NULL, 0),
(13, 'MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA', NULL, 0),
(14, 'MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA', NULL, 0);
```

### 📱 Panel de Administración de Módulos

**Requerimiento del usuario:**
> "Desde el panel de control poder añadir tanto el nuevo nombre de los nuevos módulos como de las evaluaciones para ya no tener que tocar más código"

**Funcionalidades:**

1. ✅ **Agregar Módulo Nuevo**
   - Input: Número de módulo (1-14)
   - Input: Nombre completo del módulo
   - Input: Nombre de la evaluación (opcional)
   - Botón: "Activar Módulo"

2. ✅ **Actualizar Mapeo de Evaluación**
   - Select: Módulo existente
   - Input: Nombre de evaluación en Excel
   - Botón: "Actualizar Mapeo"

3. ✅ **Ver Módulos Activos**
   - Tabla con:
     - Número
     - Nombre Módulo
     - Nombre Evaluación
     - Estado (Activo/Inactivo)
     - Acciones (Editar, Desactivar)

---

## 📝 RESUMEN DE CAMBIOS EN DOCS

### Cambios Principales vs. MAPEO_COLUMNAS_EXCEL_BD.md:

1. ✅ **Mapeo detallado de 14 módulos** con nombres exactos
2. ✅ **Lista de 8 evaluaciones** con variaciones de capitalización
3. ✅ **Algoritmo de detección** de módulos y evaluaciones (fuzzy matching)
4. ✅ **Tabla de mapeo manual** evaluación → módulo
5. ✅ **Proceso de relleno de estatus faltantes** ("Registrado", "Registrado/Vencido", etc.)
6. ✅ **Manejo de casos especiales** (cambio de departamento, correo, etc.)
7. ✅ **Stored Procedures para SQL Server** en lugar de queries MySQL
8. ✅ **Validaciones de negocio** detalladas
9. ✅ **Sistema de configuración dinámica** para escalabilidad

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Implementar** stored procedures en SQL Server
2. ✅ **Crear** tabla `instituto_configuracion_modulos`
3. ✅ **Desarrollar** panel de administración de módulos en frontend
4. ✅ **Actualizar** scripts ETL para usar configuración dinámica
5. ✅ **Crear** sistema de logs y reportes de errores
6. ✅ **Implementar** validaciones de negocio en backend
7. ✅ **Testing** con datos reales de producción

---

**FIN DEL DOCUMENTO**
