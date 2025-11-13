# 📊 Mapeo de Columnas Excel → Base de Datos

Este documento describe cómo las columnas de los archivos Excel de CSOD se mapean a los campos de la base de datos del Instituto Hutchison Ports.

---

## 🏗️ Estructura de la Base de Datos

La base de datos utiliza el prefijo `instituto_` para todas las tablas y sigue esta jerarquía:

```
instituto_UnidadDeNegocio (ICAVE, EIT, LCT, TIMSA, HPMX, TNG)
    └── instituto_Departamento
        └── instituto_Usuario
            └── instituto_ProgresoModulo (IdInscripcion)
                ├── instituto_ResultadoEvaluacion
                └── instituto_Certificado

instituto_Modulo
    ├── instituto_Evaluacion
    └── instituto_RecursoModulo
```

---

## 🎯 Archivo 1: Enterprise Training Report (Estatus y Calificaciones)

### Columnas de Excel → Campos de Base de Datos

| Columna Excel (Español) | Columna Excel (Inglés) | Campo Base de Datos | Tabla | Tipo | Descripción |
|------------------------|------------------------|---------------------|-------|------|-------------|
| **Título de la capacitación** | Training Title / Course Title | - | - | Control | Se usa para identificar módulos (contiene "MÓDULO") y buscar en `instituto_Modulo` |
| **Identificación de usuario** | User ID / User Identification | `UserId` | `instituto_Usuario` | VARCHAR(50) | ID único del usuario (FK) |
| **Estado del expediente** | Record Status / Completion Status | `EstatusModulo` | `instituto_ProgresoModulo` | VARCHAR(50) | Estado del módulo (Terminado, En progreso, etc.) |
| **Fecha de registro de la transcripción** | Transcript Registration Date | `FechaAsignacion` | `instituto_ProgresoModulo` | DATETIME | Fecha de registro inicial |
| **Fecha de inicio de la capacitación** | Training Start Date | `FechaInicio` | `instituto_ProgresoModulo` | DATETIME | Cuando el usuario comenzó el módulo |
| **Fecha de finalización de expediente** | Record Completion Date / Completion Date | `FechaFinalizacion` | `instituto_ProgresoModulo` | DATETIME | Cuando el usuario terminó el módulo |
| **Tipo de capacitación** | Training Type / Content Type | - | - | Control | Distingue entre "Módulo" y "Prueba" |
| **Puntuación de la transcripción** | Transcript Score / Score | `PuntajeObtenido` | `instituto_ResultadoEvaluacion` | DECIMAL(5,2) | Calificación obtenida en pruebas (0-100) |
| **Departamento** | Department / Organization | `NombreDepartamento` | `instituto_Departamento` | VARCHAR(150) | Departamento del usuario (se busca/crea) |
| **Cargo** | Position / Job Title | `Position` | `instituto_Usuario` | VARCHAR(100) | Puesto de trabajo del usuario |

### Procesamiento de Datos

#### 1. **Procesamiento de Módulos**

**Flujo de procesamiento:**

1. **Extraer el título del módulo** del Excel (ej: "MÓDULO 8 - PROCESOS DE RECURSOS HUMANOS")
2. **Buscar el módulo** en `instituto_Modulo` por nombre normalizado
3. **Verificar que el usuario existe** en `instituto_Usuario` usando `UserId`
4. **Buscar si ya existe un progreso** en `instituto_ProgresoModulo` para ese usuario y módulo
5. **Insertar o actualizar** el registro de progreso

```sql
-- 1. Buscar el módulo en la base de datos
SELECT IdModulo
FROM instituto_Modulo
WHERE NombreModulo LIKE '%MÓDULO 8%'
  AND Activo = 1;

-- 2. Verificar si ya existe un progreso (usando UNIQUE KEY: UserId + IdModulo)
SELECT IdInscripcion
FROM instituto_ProgresoModulo
WHERE UserId = 'USER123' AND IdModulo = 8;

-- 3. Si no existe, INSERT; si existe, UPDATE
INSERT INTO instituto_ProgresoModulo (
    UserId,                    -- Del Excel
    IdModulo,                  -- Obtenido del paso 1
    EstatusModulo,            -- Del Excel (normalizado)
    FechaAsignacion,          -- Del Excel "Transcript Registration Date"
    FechaInicio,              -- Del Excel "Training Start Date"
    FechaFinalizacion,        -- Del Excel "Record Completion Date"
    PorcentajeAvance          -- Calculado según estado (100 si terminado, etc.)
) VALUES (...)
ON DUPLICATE KEY UPDATE
    EstatusModulo = VALUES(EstatusModulo),
    FechaInicio = VALUES(FechaInicio),
    FechaFinalizacion = VALUES(FechaFinalizacion),
    PorcentajeAvance = VALUES(PorcentajeAvance);
```

**Estados posibles (mapeo automático):**
- `Terminado` → `PorcentajeAvance = 100`, `FechaFinalizacion` se registra
- `En progreso` → `PorcentajeAvance < 100`, `FechaInicio` se registra
- `En progreso / Vencido` → Similar a "En progreso" pero se verifica vencimiento
- `Registrado` → `PorcentajeAvance = 0`, solo `FechaAsignacion`
- `Registrado / Vencido` → Similar a "Registrado" pero se verifica vencimiento
- `No iniciado` → `PorcentajeAvance = 0`, sin fechas

#### 2. **Procesamiento de Calificaciones**

**Flujo de procesamiento:**

1. **Identificar registros de evaluación** donde "Tipo de capacitación" contiene "Prueba" o "Test"
2. **Obtener el IdInscripcion** de `instituto_ProgresoModulo` usando `UserId` y `IdModulo`
3. **Buscar la evaluación** en `instituto_Evaluacion` asociada al módulo
4. **Insertar el resultado** en `instituto_ResultadoEvaluacion`

```sql
-- 1. Obtener IdInscripcion (necesario como FK)
SELECT IdInscripcion
FROM instituto_ProgresoModulo
WHERE UserId = 'USER123' AND IdModulo = 8;

-- 2. Buscar la evaluación del módulo
SELECT IdEvaluacion, PuntajeMinimoAprobatorio
FROM instituto_Evaluacion
WHERE IdModulo = 8 AND Activo = 1
LIMIT 1;

-- 3. Insertar resultado de evaluación
INSERT INTO instituto_ResultadoEvaluacion (
    IdInscripcion,            -- Obtenido del paso 1
    IdEvaluacion,            -- Obtenido del paso 2
    PuntajeObtenido,         -- Del Excel "Transcript Score"
    Aprobado,                -- 1 si PuntajeObtenido >= PuntajeMinimoAprobatorio (default: 70)
    IntentoNumero,           -- Contar intentos previos + 1
    FechaRealizacion,        -- Del Excel "Record Completion Date"
    TiempoInvertidoMinutos   -- Opcional, calculado si está disponible
) VALUES (...);

-- 4. Si la evaluación fue aprobada, actualizar el progreso
UPDATE instituto_ProgresoModulo
SET EstatusModulo = 'Terminado',
    PorcentajeAvance = 100,
    FechaFinalizacion = NOW()
WHERE IdInscripcion = @IdInscripcion AND PuntajeObtenido >= 70;
```

**Lógica de aprobación:**
- **Aprobado = 1** si `PuntajeObtenido >= PuntajeMinimoAprobatorio` (default: 70.00)
- **Aprobado = 0** si `PuntajeObtenido < PuntajeMinimoAprobatorio`

#### 3. **Actualización de Información de Usuarios**

**Flujo de procesamiento:**

1. **Verificar si el usuario existe** en `instituto_Usuario` usando `UserId`
2. **Buscar/crear el departamento** si viene en el Excel
3. **Actualizar campos** del usuario

```sql
-- 1. Verificar si el usuario existe
SELECT IdUsuario, IdDepartamento
FROM instituto_Usuario
WHERE UserId = 'USER123';

-- 2. Si viene departamento en el Excel, buscar/crear en instituto_Departamento
-- (Requiere tener IdUnidadDeNegocio, se puede inferir o asignar por defecto)
INSERT IGNORE INTO instituto_Departamento (
    IdUnidadDeNegocio,       -- Se debe configurar (ej: TNG por defecto)
    NombreDepartamento,
    Activo
) VALUES (6, 'Recursos Humanos', 1);

SELECT IdDepartamento
FROM instituto_Departamento
WHERE NombreDepartamento = 'Recursos Humanos';

-- 3. Actualizar información del usuario
UPDATE instituto_Usuario
SET
    Position = 'Cargo del Excel',
    IdDepartamento = @IdDepartamento,  -- Si se encontró/creó
    Ubicacion = 'Ubicacion del Excel'  -- Si está disponible
WHERE UserId = 'USER123';
```

---

## 👥 Archivo 2: CSOD Org Planning (Datos de Usuarios)

### Columnas de Excel → Campos de Base de Datos

| Columna Excel (Español) | Columna Excel (Inglés) | Campo Base de Datos | Tabla | Tipo | Descripción |
|------------------------|------------------------|---------------------|-------|------|-------------|
| **Usuario - Identificación de usuario** | User - User ID | `UserId` | `instituto_Usuario` | VARCHAR(50) | ID único del usuario (UNIQUE KEY) |
| **Usuario - Nombre completo del usuario** | User - Full Name | `NombreCompleto` | `instituto_Usuario` | VARCHAR(255) | Nombre y apellidos del usuario |
| **Usuario - Correo electrónico del usuario** | User - Email Address | `UserEmail` | `instituto_Usuario` | VARCHAR(255) | Email corporativo |
| **Usuario - Cargo** | User - Job Title / Position | `Position` | `instituto_Usuario` | VARCHAR(100) | Puesto de trabajo |
| **Usuario - Departamento** | User - Department | `NombreDepartamento` | `instituto_Departamento` | VARCHAR(150) | Departamento (se busca/crea automáticamente) |
| **Usuario - División/Unidad** | User - Division / Business Unit | `NombreUnidad` | `instituto_UnidadDeNegocio` | VARCHAR(100) | Unidad de negocio (ICAVE, EIT, LCT, TIMSA, HPMX, TNG) |
| **Usuario - Ubicación** | User - Location | `Ubicacion` | `instituto_Usuario` | VARCHAR(100) | Oficina o sede |
| **Usuario - Nivel** | User - Level | `Nivel` | `instituto_Usuario` | VARCHAR(50) | Nivel jerárquico del usuario |
| **Usuario - Ciudad** | User - City | - | - | - | Ciudad (no se mapea actualmente) |
| **Usuario - País del usuario** | User - Country | - | - | - | País (no se mapea actualmente) |

### Procesamiento de Datos

#### Creación de Nuevos Usuarios

**Flujo de procesamiento:**

1. **Verificar si el usuario ya existe** usando `UserId`
2. **Buscar/crear la Unidad de Negocio** si viene en el Excel
3. **Buscar/crear el Departamento** si viene en el Excel (requiere IdUnidadDeNegocio)
4. **Asignar rol por defecto** (ej: "Usuario" = IdRol 4)
5. **Insertar el nuevo usuario** con todas las relaciones

```sql
-- 1. Verificar si el usuario existe
SELECT IdUsuario
FROM instituto_Usuario
WHERE UserId = 'USER123';

-- 2. Buscar/crear Unidad de Negocio
INSERT IGNORE INTO instituto_UnidadDeNegocio (
    NombreUnidad,
    Codigo,
    Activo
) VALUES ('TNG', 'TNG', 1);

SELECT IdUnidadDeNegocio
FROM instituto_UnidadDeNegocio
WHERE NombreUnidad = 'TNG';

-- 3. Buscar/crear Departamento
INSERT IGNORE INTO instituto_Departamento (
    IdUnidadDeNegocio,       -- Del paso 2
    NombreDepartamento,
    Activo
) VALUES (@IdUnidadDeNegocio, 'Recursos Humanos', 1);

SELECT IdDepartamento
FROM instituto_Departamento
WHERE IdUnidadDeNegocio = @IdUnidadDeNegocio
  AND NombreDepartamento = 'Recursos Humanos';

-- 4. Insertar nuevo usuario
INSERT INTO instituto_Usuario (
    UserId,                  -- Del Excel
    IdUnidadDeNegocio,      -- Del paso 2
    IdDepartamento,         -- Del paso 3
    IdRol,                  -- 4 = "Usuario" por defecto
    NombreCompleto,         -- Del Excel
    UserEmail,              -- Del Excel
    Position,               -- Del Excel
    Nivel,                  -- Del Excel (opcional)
    Ubicacion,              -- Del Excel (opcional)
    Activo,                 -- 1 por defecto
    FechaCreacion           -- CURRENT_TIMESTAMP automático
) VALUES (
    'USER123',
    @IdUnidadDeNegocio,
    @IdDepartamento,
    4,
    'Juan Pérez García',
    'juan.perez@hutchison.com',
    'Analista de Capacitación',
    'Nivel 3',
    'Ciudad de México',
    1
);
```

#### Actualización de Usuarios Existentes

**Flujo de procesamiento:**

1. **Verificar que el usuario existe**
2. **Buscar/actualizar Unidad de Negocio** si cambió en el Excel
3. **Buscar/actualizar Departamento** si cambió en el Excel
4. **Actualizar campos** del usuario

```sql
-- 1. Buscar usuario existente
SELECT IdUsuario, IdUnidadDeNegocio, IdDepartamento
FROM instituto_Usuario
WHERE UserId = 'USER123';

-- 2. Si cambió la unidad de negocio, buscar nueva
SELECT IdUnidadDeNegocio
FROM instituto_UnidadDeNegocio
WHERE NombreUnidad = 'Nueva Unidad';

-- 3. Si cambió el departamento, buscar/crear nuevo
INSERT IGNORE INTO instituto_Departamento (
    IdUnidadDeNegocio,
    NombreDepartamento,
    Activo
) VALUES (@NuevoIdUnidadDeNegocio, 'Nuevo Departamento', 1);

-- 4. Actualizar usuario
UPDATE instituto_Usuario
SET
    NombreCompleto = 'Nombre del Excel',
    UserEmail = 'email.actualizado@hutchison.com',
    Position = 'Nuevo Cargo',
    IdUnidadDeNegocio = @NuevoIdUnidadDeNegocio,
    IdDepartamento = @NuevoIdDepartamento,
    Nivel = 'Nivel del Excel',
    Ubicacion = 'Nueva Ubicación'
WHERE UserId = 'USER123';
```

**⚠️ Notas importantes:**
- Si no viene **Unidad de Negocio** en el Excel, se puede asignar una por defecto (ej: TNG)
- Si no viene **Departamento**, se deja `NULL` en `IdDepartamento`
- El **Rol** se asigna por defecto a `4 = "Usuario"`, pero puede ser actualizado manualmente
- Se usa `INSERT IGNORE` para evitar duplicados en Unidades y Departamentos

---

## 🔍 Detección Automática de Columnas

El sistema detecta automáticamente si el Excel está en **Español** o **Inglés** buscando estas variaciones:

### Ejemplo de Detección

```python
# El sistema busca cualquiera de estas variaciones:
'training_title': [
    'Título de la capacitación',  # Español
    'Training Title',              # Inglés formal
    'Course Title',                # Inglés alternativo
    'Title'                        # Inglés corto
]
```

Si el Excel usa nombres diferentes, el sistema mostrará:
```
⚠️  Columnas no encontradas: training_title, user_id, ...
```

---

## 📋 Normalización de Módulos

El sistema reconoce estos 14 módulos (case-insensitive):

| # | Nombre del Módulo |
|---|-------------------|
| 1 | MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS |
| 2 | MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO |
| 3 | MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES |
| 4 | MÓDULO 4 . RELACIONES LABORALES |
| 5 | MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES |
| 6 | MÓDULO 6 . CIBERSEGURIDAD |
| 7 | MÓDULO 7 . ENTORNO LABORAL SALUDABLE |
| 8 | MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS |
| 9 | MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL |
| 10 | MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS |
| 11 | MÓDULO 11 . PRODUCTOS DIGITALES DE HP |
| 12 | MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD |
| 13 | MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA |
| 14 | MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA |

---

## ⚙️ Detección Automática de Headers

Si el Excel tiene filas de título/logo antes de los headers, el sistema:

1. Detecta que las columnas son "Unnamed: 0, Unnamed: 1, ..."
2. Busca automáticamente en las filas 1-5 dónde están los headers reales
3. Lee el Excel saltando esas filas superiores

```
⚠️  Headers no detectados en fila 0, buscando headers reales...
  ✓ Headers encontrados en fila 3
```

---

## 🚨 Troubleshooting

### Problema: "Columnas no encontradas"

**Causa:** Los nombres de las columnas en tu Excel no coinciden con ninguna variante conocida.

**Solución:**
1. Abre el Excel
2. Verifica el nombre exacto de las columnas (fila de headers)
3. Compara con las variantes en las tablas de arriba
4. Si son diferentes, reporta los nombres exactos para agregar soporte

### Problema: "Headers no detectados"

**Causa:** El Excel tiene más de 5 filas antes de los headers reales.

**Solución:**
1. Elimina las filas de título/logo superiores
2. O ajusta el parámetro `skiprows` en el código manualmente

### Problema: "Módulo no reconocido"

**Causa:** El nombre del módulo en el Excel no coincide con los 14 módulos conocidos.

**Solución:**
1. Verifica que el título contenga "MÓDULO X" donde X es 1-14
2. El sistema busca la palabra "MÓDULO" (case-insensitive)
3. Reporta módulos nuevos para agregar soporte

---

## 📊 Estadísticas de Importación

Después de cada importación, el sistema muestra:

```
======================================================================
REPORTE DE IMPORTACIÓN - 2025-11-10 14:05:30
======================================================================

📊 ESTADÍSTICAS:
  • Usuarios nuevos:           150
  • Usuarios actualizados:      1375
  • Módulos creados:            0
  • Progresos actualizados:     12200
  • Calificaciones registradas: 8540
  • Errores:                    3

❌ ERRORES ENCONTRADOS:
  • Error procesando fila 1250: ...
  • Error procesando fila 3840: ...

======================================================================
```

---

## 💾 Sistema de Backups

Antes de cada importación, se crea un backup automático:

```
📦 Creando backup: 20251110_140541
  ✓ instituto_Usuario: 1525 registros
  ✓ instituto_ProgresoModulo: 12150 registros
  ✓ instituto_Modulo: 8 registros
✅ Backup creado: C:\Users\...\smartreports_backups\backup_20251110_140541.json
```

Para restaurar un backup: Usar la opción "Ver Backups" en el panel de importación.

---

## 🔗 Relaciones entre Tablas y Restricciones

### Claves Foráneas (Foreign Keys)

La base de datos implementa integridad referencial mediante las siguientes relaciones:

```
instituto_Usuario
├── IdUnidadDeNegocio → instituto_UnidadDeNegocio.IdUnidadDeNegocio (ON DELETE SET NULL)
├── IdDepartamento → instituto_Departamento.IdDepartamento (ON DELETE SET NULL)
└── IdRol → instituto_Rol.IdRol (ON DELETE SET NULL)

instituto_Departamento
└── IdUnidadDeNegocio → instituto_UnidadDeNegocio.IdUnidadDeNegocio (ON DELETE RESTRICT)

instituto_ProgresoModulo
├── UserId → instituto_Usuario.UserId (ON DELETE CASCADE)
└── IdModulo → instituto_Modulo.IdModulo (ON DELETE CASCADE)

instituto_ResultadoEvaluacion
├── IdInscripcion → instituto_ProgresoModulo.IdInscripcion (ON DELETE CASCADE)
└── IdEvaluacion → instituto_Evaluacion.IdEvaluacion (ON DELETE CASCADE)

instituto_Evaluacion
└── IdModulo → instituto_Modulo.IdModulo (ON DELETE CASCADE)
```

### Restricciones Únicas (UNIQUE KEYS)

Estas restricciones previenen duplicados:

- **instituto_Usuario**: `UserId` (UNIQUE)
- **instituto_Rol**: `NombreRol` (UNIQUE)
- **instituto_UnidadDeNegocio**: `NombreUnidad` (UNIQUE), `Codigo` (UNIQUE)
- **instituto_Departamento**: `(IdUnidadDeNegocio, NombreDepartamento)` (UNIQUE compuesta)
- **instituto_ProgresoModulo**: `(UserId, IdModulo)` (UNIQUE compuesta)
- **instituto_Modulo**: `NombreModulo` (UNIQUE)

**⚠️ Implicación para la importación:**
- Al importar, si se intenta insertar un registro con una combinación `UserId + IdModulo` que ya existe en `instituto_ProgresoModulo`, se debe usar `ON DUPLICATE KEY UPDATE` para actualizar en lugar de fallar.

---

## 🔄 Flujo Completo de Importación

### Orden de Procesamiento

Para garantizar la integridad referencial, el procesamiento debe seguir este orden:

```
1. TABLAS MAESTRAS (si no existen)
   ├── instituto_UnidadDeNegocio
   ├── instituto_Rol
   └── instituto_Departamento

2. USUARIOS
   └── instituto_Usuario
       ├── Crear/actualizar Unidad de Negocio
       ├── Crear/actualizar Departamento
       └── Insertar/actualizar Usuario

3. MÓDULOS (si no existen)
   └── instituto_Modulo

4. PROGRESO DE MÓDULOS
   └── instituto_ProgresoModulo
       ├── Verificar que existe UserId
       ├── Verificar que existe IdModulo
       └── INSERT ... ON DUPLICATE KEY UPDATE

5. EVALUACIONES
   ├── instituto_Evaluacion (si no existe para el módulo)
   └── instituto_ResultadoEvaluacion
       ├── Obtener IdInscripcion de ProgresoModulo
       ├── Obtener IdEvaluacion
       ├── Insertar resultado
       └── Actualizar ProgresoModulo si aprobó
```

### Algoritmo de Importación (Pseudocódigo)

```python
def importar_excel_csod(archivo_excel, tipo_reporte):
    """
    Importa datos de Excel CSOD a la base de datos.

    Args:
        archivo_excel: Ruta al archivo Excel
        tipo_reporte: 'training_report' o 'org_planning'
    """

    # 1. Leer Excel y detectar columnas
    df = detectar_y_leer_excel(archivo_excel)

    # 2. Normalizar nombres de columnas (español/inglés)
    columnas_mapeadas = mapear_columnas(df.columns)

    if tipo_reporte == 'org_planning':
        # IMPORTAR USUARIOS
        for fila in df.iterrows():
            # 2.1 Extraer datos
            user_id = fila['user_id']
            nombre = fila['full_name']
            email = fila['email']
            cargo = fila['position']
            unidad = fila['business_unit']  # Opcional
            departamento = fila['department']  # Opcional

            # 2.2 Buscar/crear Unidad de Negocio
            if unidad:
                id_unidad = obtener_o_crear_unidad_negocio(unidad)
            else:
                id_unidad = None

            # 2.3 Buscar/crear Departamento
            if departamento and id_unidad:
                id_depto = obtener_o_crear_departamento(
                    id_unidad, departamento
                )
            else:
                id_depto = None

            # 2.4 Insertar/actualizar usuario
            usuario_existe = verificar_usuario_existe(user_id)
            if usuario_existe:
                actualizar_usuario(
                    user_id, nombre, email, cargo,
                    id_unidad, id_depto
                )
            else:
                crear_usuario(
                    user_id, nombre, email, cargo,
                    id_unidad, id_depto, id_rol=4  # "Usuario"
                )

    elif tipo_reporte == 'training_report':
        # IMPORTAR PROGRESO Y CALIFICACIONES
        for fila in df.iterrows():
            # 3.1 Extraer datos
            user_id = fila['user_id']
            titulo_capacitacion = fila['training_title']
            tipo_capacitacion = fila['training_type']
            estatus = fila['record_status']
            fecha_asignacion = fila['registration_date']
            fecha_inicio = fila['start_date']
            fecha_fin = fila['completion_date']
            puntaje = fila['score']

            # 3.2 Verificar que el usuario existe
            if not verificar_usuario_existe(user_id):
                log_error(f"Usuario {user_id} no existe")
                continue

            # 3.3 Identificar si es módulo o evaluación
            if 'MÓDULO' in titulo_capacitacion.upper():
                # ES UN MÓDULO
                # 3.3.1 Buscar el módulo por nombre
                id_modulo = buscar_modulo_por_nombre(
                    titulo_capacitacion
                )
                if not id_modulo:
                    log_error(f"Módulo no encontrado: {titulo_capacitacion}")
                    continue

                # 3.3.2 Calcular porcentaje según estado
                porcentaje = calcular_porcentaje_por_estado(estatus)

                # 3.3.3 Insertar/actualizar progreso
                insertar_actualizar_progreso(
                    user_id=user_id,
                    id_modulo=id_modulo,
                    estatus=normalizar_estatus(estatus),
                    fecha_asignacion=fecha_asignacion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    porcentaje=porcentaje
                )

            elif 'PRUEBA' in tipo_capacitacion.upper() or 'TEST' in tipo_capacitacion.upper():
                # ES UNA EVALUACIÓN
                # 3.4.1 Obtener IdInscripcion
                id_inscripcion = obtener_id_inscripcion(
                    user_id, id_modulo
                )
                if not id_inscripcion:
                    log_error(f"No se encontró inscripción para {user_id}")
                    continue

                # 3.4.2 Buscar evaluación del módulo
                id_evaluacion = obtener_evaluacion_del_modulo(id_modulo)
                if not id_evaluacion:
                    # Crear evaluación por defecto si no existe
                    id_evaluacion = crear_evaluacion_default(
                        id_modulo, titulo_capacitacion
                    )

                # 3.4.3 Contar intentos previos
                intento_numero = contar_intentos_evaluacion(
                    id_inscripcion, id_evaluacion
                ) + 1

                # 3.4.4 Determinar si aprobó
                puntaje_minimo = obtener_puntaje_minimo(id_evaluacion)
                aprobado = 1 if puntaje >= puntaje_minimo else 0

                # 3.4.5 Insertar resultado
                insertar_resultado_evaluacion(
                    id_inscripcion=id_inscripcion,
                    id_evaluacion=id_evaluacion,
                    puntaje=puntaje,
                    aprobado=aprobado,
                    intento_numero=intento_numero,
                    fecha_realizacion=fecha_fin
                )

                # 3.4.6 Si aprobó, actualizar progreso a "Terminado"
                if aprobado:
                    actualizar_progreso_terminado(
                        id_inscripcion, fecha_fin
                    )

def calcular_porcentaje_por_estado(estatus):
    """Mapea el estado del Excel a un porcentaje."""
    mapeo = {
        'Terminado': 100,
        'Completado': 100,
        'Completed': 100,
        'En progreso': 50,  # Puede ajustarse según lógica
        'In Progress': 50,
        'Registrado': 0,
        'Registered': 0,
        'No iniciado': 0,
        'Not Started': 0
    }
    return mapeo.get(estatus, 0)

def normalizar_estatus(estatus_excel):
    """Normaliza el estado del Excel al formato de la BD."""
    mapeo = {
        'Terminado': 'Terminado',
        'Completado': 'Terminado',
        'Completed': 'Terminado',
        'En progreso': 'En progreso',
        'In Progress': 'En progreso',
        'En progreso / Vencido': 'En progreso',
        'Registrado': 'Registrado',
        'Registered': 'Registrado',
        'Registrado / Vencido': 'Registrado',
        'No iniciado': 'No iniciado',
        'Not Started': 'No iniciado'
    }
    return mapeo.get(estatus_excel, 'No iniciado')
```

---

## 🛡️ Manejo de Errores y Validaciones

### Validaciones Críticas

1. **Usuario no existe**: Antes de insertar progreso o calificaciones, verificar que el `UserId` existe en `instituto_Usuario`
2. **Módulo no encontrado**: Si el título del módulo no coincide, registrar error y continuar
3. **Duplicados**: Usar `ON DUPLICATE KEY UPDATE` para evitar errores de clave única
4. **Fechas inválidas**: Validar que `FechaFinalizacion >= FechaInicio`
5. **Puntajes fuera de rango**: Validar que `PuntajeObtenido` esté entre 0 y 100

### Transacciones

Para garantizar consistencia, cada importación debe ejecutarse en una transacción:

```sql
START TRANSACTION;

-- Importar todos los registros del Excel
-- ...

-- Si todo fue exitoso:
COMMIT;

-- Si hubo algún error crítico:
ROLLBACK;
```

### Log de Errores

Cada error debe ser registrado con:
- Número de fila del Excel
- Campo que causó el error
- Mensaje descriptivo
- Timestamp

---

## 📈 Métricas y Validación Post-Importación

Después de cada importación, ejecutar estas consultas para validar:

```sql
-- 1. Usuarios sin unidad de negocio
SELECT COUNT(*) AS UsuariosSinUnidad
FROM instituto_Usuario
WHERE IdUnidadDeNegocio IS NULL;

-- 2. Progreso sin fechas consistentes
SELECT COUNT(*) AS ProgresoInconsistente
FROM instituto_ProgresoModulo
WHERE FechaFinalizacion IS NOT NULL
  AND FechaFinalizacion < FechaInicio;

-- 3. Calificaciones sin inscripción válida
SELECT COUNT(*) AS CalificacionesHuérfanas
FROM instituto_ResultadoEvaluacion re
LEFT JOIN instituto_ProgresoModulo pm ON re.IdInscripcion = pm.IdInscripcion
WHERE pm.IdInscripcion IS NULL;

-- 4. Usuarios con progreso "Terminado" sin calificación
SELECT COUNT(*) AS TerminadosSinCalificacion
FROM instituto_ProgresoModulo pm
LEFT JOIN instituto_ResultadoEvaluacion re ON pm.IdInscripcion = re.IdInscripcion
WHERE pm.EstatusModulo = 'Terminado'
  AND pm.PorcentajeAvance = 100
  AND re.IdResultado IS NULL;

-- 5. Resumen por unidad de negocio
SELECT
    un.NombreUnidad,
    COUNT(DISTINCT u.IdUsuario) AS TotalUsuarios,
    COUNT(DISTINCT pm.IdInscripcion) AS TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) AS Completados
FROM instituto_UnidadDeNegocio un
LEFT JOIN instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE un.Activo = 1
GROUP BY un.IdUnidadDeNegocio;
```

---

## 🎯 Resumen de la Lógica de Funcionamiento

### Principios Clave

1. **Integridad Referencial**: Siempre crear/verificar registros padre antes de crear hijos
   - UnidadDeNegocio → Departamento → Usuario → ProgresoModulo → ResultadoEvaluacion

2. **Idempotencia**: La importación debe ser repetible sin crear duplicados
   - Usar `INSERT IGNORE` para tablas maestras
   - Usar `ON DUPLICATE KEY UPDATE` para progreso de usuarios

3. **Normalización de Datos**: Convertir variaciones del Excel a formato estándar
   - Estados: "Completed"/"Terminado" → "Terminado"
   - Módulos: Buscar por coincidencia parcial (LIKE '%MÓDULO 8%')

4. **Manejo de Opcionales**: Campos que pueden ser NULL
   - `IdUnidadDeNegocio`, `IdDepartamento`, `IdRol` en `instituto_Usuario`
   - `FechaVencimiento` en `instituto_ProgresoModulo`

5. **Auditoría**: Registrar cada operación importante
   - Usar `instituto_HistorialProgreso` para cambios en progreso
   - Usar `instituto_AuditoriaAcceso` para operaciones de importación

---

**Última actualización:** 13 de Noviembre, 2025
**Versión del sistema:** Smart Reports v2.0
**Estructura de BD:** instituto_* (prefijo)
