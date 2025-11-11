# 📊 Mapeo de Columnas Excel → Base de Datos

Este documento describe cómo las columnas de los archivos Excel de CSOD se mapean a los campos de la base de datos del Instituto Hutchison Ports.

---

## 🎯 Archivo 1: Enterprise Training Report (Estatus y Calificaciones)

### Columnas de Excel → Campos de Base de Datos

| Columna Excel (Español) | Columna Excel (Inglés) | Campo Base de Datos | Tabla | Descripción |
|------------------------|------------------------|---------------------|-------|-------------|
| **Título de la capacitación** | Training Title / Course Title | - | - | Se usa para identificar módulos (contiene "MÓDULO") |
| **Identificación de usuario** | User ID / User Identification | `UserId` | `instituto_Usuario` | ID único del usuario |
| **Estado del expediente** | Record Status / Completion Status | `EstatusModulo` | `instituto_ProgresoModulo` | Estado del módulo (Terminado, En progreso, etc.) |
| **Fecha de registro de la transcripción** | Transcript Registration Date | `FechaAsignacion` | `instituto_ProgresoModulo` | Fecha de registro inicial |
| **Fecha de inicio de la capacitación** | Training Start Date | `FechaInicio` | `instituto_ProgresoModulo` | Cuando el usuario comenzó el módulo |
| **Fecha de finalización de expediente** | Record Completion Date / Completion Date | `FechaFinalizacion` | `instituto_ProgresoModulo` | Cuando el usuario terminó el módulo |
| **Tipo de capacitación** | Training Type / Content Type | - | - | Distingue entre "Módulo" y "Prueba" |
| **Puntuación de la transcripción** | Transcript Score / Score | `PuntajeObtenido` | `instituto_ResultadoEvaluacion` | Calificación obtenida en pruebas |
| **Departamento** | Department / Organization | - | `instituto_Usuario` | Departamento del usuario (opcional) |
| **Cargo** | Position / Job Title | `Position` | `instituto_Usuario` | Puesto de trabajo del usuario |

### Procesamiento de Datos

#### 1. **Procesamiento de Módulos**
```sql
-- Se filtran registros donde "Título de la capacitación" contiene "MÓDULO"
-- Ejemplo: "MÓDULO 8 - PROCESOS DE RECURSOS HUMANOS"

-- Se inserta/actualiza en instituto_ProgresoModulo:
INSERT INTO instituto_ProgresoModulo (
    UserId,
    IdModulo,
    EstatusModulo,
    FechaInicio,
    FechaFinalizacion,
    PorcentajeAvance,
    FechaAsignacion
) VALUES (...);
```

**Estados posibles:**
- `Terminado` - Módulo completado
- `En progreso` - Iniciado pero no terminado
- `En progreso / Vencido` - Iniciado pero pasó fecha límite
- `Registrado` - Asignado pero no iniciado
- `Registrado / Vencido` - Asignado pero pasó fecha límite
- `No iniciado` - Sin asignar

#### 2. **Procesamiento de Calificaciones**
```sql
-- Se filtran registros donde "Tipo de capacitación" contiene "Prueba" o "Test"
-- Se extrae la calificación de "Puntuación de la transcripción"

-- Se inserta/actualiza en instituto_ResultadoEvaluacion:
INSERT INTO instituto_ResultadoEvaluacion (
    IdInscripcion,
    IdEvaluacion,
    PuntajeObtenido,
    Aprobado,  -- 1 si >=70, 0 si <70
    IntentoNumero,
    FechaRealizacion
) VALUES (...);
```

#### 3. **Actualización de Información de Usuarios**
```sql
-- Se actualiza información básica del usuario
UPDATE instituto_Usuario
SET Position = 'Cargo del Excel'
WHERE UserId = 'ID del usuario';
```

---

## 👥 Archivo 2: CSOD Org Planning (Datos de Usuarios)

### Columnas de Excel → Campos de Base de Datos

| Columna Excel (Español) | Columna Excel (Inglés) | Campo Base de Datos | Tabla | Descripción |
|------------------------|------------------------|---------------------|-------|-------------|
| **Usuario - Identificación de usuario** | User - User ID | `UserId` | `instituto_Usuario` | ID único del usuario (PRIMARY KEY) |
| **Usuario - Nombre completo del usuario** | User - Full Name | `NombreCompleto` | `instituto_Usuario` | Nombre y apellidos del usuario |
| **Usuario - Correo electrónico del usuario** | User - Email Address | `UserEmail` | `instituto_Usuario` | Email corporativo |
| **Usuario - Cargo** | User - Job Title / Position | `Position` | `instituto_Usuario` | Puesto de trabajo |
| **Usuario - Departamento** | User - Department | - | - | Departamento (no se usa actualmente) |
| **Usuario - Ubicación** | User - Location | `Ubicacion` | `instituto_Usuario` | Oficina o sede |
| **Usuario - Ciudad** | User - City | - | - | Ciudad (no se usa actualmente) |
| **Usuario - País del usuario** | User - Country | - | - | País (no se usa actualmente) |

### Procesamiento de Datos

#### Creación de Nuevos Usuarios
```sql
INSERT INTO instituto_Usuario (
    UserId,
    NombreCompleto,
    UserEmail,
    Position,
    Ubicacion,
    Activo
) VALUES (
    'ID del Excel',
    'Nombre completo',
    'email@hutchison.com',
    'Cargo',
    'Ubicación',
    1
);
```

#### Actualización de Usuarios Existentes
```sql
UPDATE instituto_Usuario
SET
    NombreCompleto = 'Nombre del Excel',
    UserEmail = 'Email del Excel',
    Position = 'Cargo del Excel',
    Ubicacion = 'Ubicación del Excel'
WHERE UserId = 'ID del usuario';
```

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

**Última actualización:** 10 de Noviembre, 2025
**Versión del sistema:** Smart Reports v2.0
