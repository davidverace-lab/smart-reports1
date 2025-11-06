# 📊 PROPUESTA DE MEJORA - BASE DE DATOS SMART REPORTS

## 🎯 ANÁLISIS GENERAL

Tu esquema de base de datos está **bien estructurado** y sigue buenas prácticas. Sin embargo, después de analizar tu código y el funcionamiento real del sistema, encontré varias áreas de mejora que harán tu BD más robusta, escalable y alineada con tu aplicación.

---

## ✅ LO QUE ESTÁ BIEN

1. **Normalización correcta**: Estructura bien normalizada (3FN)
2. **Relaciones claras**: Foreign Keys bien definidas
3. **Campos de auditoría**: Incluyes campos de tracking (fechas, activo/inactivo)
4. **Constraints únicos**: Evitas duplicados con UNIQUE
5. **Identity para PKs**: Uso correcto de IDENTITY para IDs autoincrementales

---

## 🔧 MEJORAS CRÍTICAS NECESARIAS

### 1. **INCONSISTENCIA DE PREFIJOS Y NOMBRES**

**Problema detectado:**
- Tu código Python usa tablas con prefijo `Instituto_` (ej: `Instituto_Usuario`, `Instituto_Modulo`)
- Tu esquema propone tablas SIN prefijo (ej: `Usuario`, `Modulo`)
- Esto causará errores de "tabla no encontrada"

**Solución propuesta:**
```sql
-- ✅ USAR PREFIJO Instituto_ en TODAS las tablas
CREATE TABLE Instituto_Usuario (...);
CREATE TABLE Instituto_Rol (...);
-- etc.
```

---

### 2. **CAMPOS FALTANTES EN USUARIO**

**Problema:** Tu tabla Usuario no coincide con los campos que tu código Python espera.

**Campos que USA tu código pero NO están en tu esquema:**
- `Nombre` (tu esquema tiene `NombreCompleto`)
- `Email` (tu esquema tiene `UserEmail`)
- `Activo` (falta en tu esquema)

**Solución:**
```sql
CREATE TABLE Instituto_Usuario (
    IdUsuario INT PRIMARY KEY IDENTITY(1,1),
    UserId VARCHAR(50) UNIQUE NOT NULL,  -- ID externo (de Cornerstone)
    IdUnidadDeNegocio INT,
    IdRol INT,

    -- CAMPOS BÁSICOS (usa nombres simples)
    Nombre VARCHAR(255) NOT NULL,  -- ✅ Nombre usado en código
    Email VARCHAR(255),             -- ✅ Email usado en código

    -- CAMPOS OPCIONALES ADICIONALES
    NombreCompleto VARCHAR(255),    -- Nombre completo si difiere
    UserEmail VARCHAR(255),          -- Email alternativo si hay

    -- CAMPOS ORGANIZACIONALES
    Nivel VARCHAR(50),               -- Mandos Gerenciales, Medios, Operativos
    Division VARCHAR(100),
    Position VARCHAR(100),
    Grupo VARCHAR(100),
    Ubicacion VARCHAR(100),

    -- CAMPOS DE SEGURIDAD
    PasswordHash VARCHAR(255),       -- Hash BCrypt para passwords
    UltimoAcceso DATETIME,           -- Para auditoría

    -- CAMPOS DE ESTADO
    UserStatus VARCHAR(50) DEFAULT 'Activo',
    Activo BIT DEFAULT 1,            -- ✅ CRÍTICO: falta en tu esquema

    -- AUDITORÍA
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES Instituto_UnidadDeNegocio(IdUnidadDeNegocio),
    FOREIGN KEY (IdRol) REFERENCES Instituto_Rol(IdRol)
);
```

---

### 3. **CAMPOS FALTANTES EN PROGRESO DE MÓDULO**

**Problema:** Tu código busca campos que no existen en tu esquema.

**Campos usados por el código:**
- `EstatusModuloUsuario` (tu esquema tiene `EstatusModulo`)
- `CalificacionModuloUsuario` (falta completamente)
- `FechaInicio` (falta)
- `PorcentajeProgreso` (falta)

**Solución:**
```sql
CREATE TABLE Instituto_ProgresoModulo (
    IdInscripcion INT PRIMARY KEY IDENTITY(1,1),
    UserId VARCHAR(50) NOT NULL,     -- FK a Usuario.UserId
    IdModulo INT NOT NULL,

    -- ESTADOS DEL PROGRESO
    EstatusModuloUsuario VARCHAR(50) DEFAULT 'Registrado',  -- ✅ Nombre correcto
    -- Valores: 'Registrado', 'En Proceso', 'Completado', 'Vencido', 'No Iniciado'

    -- FECHAS
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    FechaInicio DATETIME,            -- ✅ NUEVO: Cuando el usuario inicia
    FechaVencimiento DATETIME,
    FechaFinalizacion DATETIME,

    -- CALIFICACIONES Y PROGRESO
    CalificacionModuloUsuario DECIMAL(5,2),  -- ✅ NUEVO: Calificación obtenida
    PorcentajeProgreso INT DEFAULT 0,         -- ✅ NUEVO: 0-100
    IntentosRealizados INT DEFAULT 0,

    -- AUDITORÍA
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (UserId) REFERENCES Instituto_Usuario(UserId) ON DELETE CASCADE,
    FOREIGN KEY (IdModulo) REFERENCES Instituto_Modulo(IdModulo) ON DELETE CASCADE,
    CONSTRAINT UQ_Usuario_Modulo UNIQUE (UserId, IdModulo)
);
```

---

### 4. **ÍNDICES FALTANTES (CRÍTICO PARA PERFORMANCE)**

**Problema:** Sin índices, tus reportes serán LENTOS con muchos datos.

**Solución:**
```sql
-- ÍNDICES PARA BÚSQUEDAS FRECUENTES

-- Usuario: búsquedas por email, nombre, unidad
CREATE INDEX IX_Usuario_Email ON Instituto_Usuario(Email);
CREATE INDEX IX_Usuario_Nombre ON Instituto_Usuario(Nombre);
CREATE INDEX IX_Usuario_Unidad ON Instituto_Usuario(IdUnidadDeNegocio);
CREATE INDEX IX_Usuario_Activo ON Instituto_Usuario(Activo);
CREATE INDEX IX_Usuario_Nivel ON Instituto_Usuario(Nivel);  -- Para reportes por niveles

-- ProgresoModulo: reportes por estado, fechas, usuario
CREATE INDEX IX_ProgresoModulo_Estado ON Instituto_ProgresoModulo(EstatusModuloUsuario);
CREATE INDEX IX_ProgresoModulo_Usuario ON Instituto_ProgresoModulo(UserId);
CREATE INDEX IX_ProgresoModulo_Modulo ON Instituto_ProgresoModulo(IdModulo);
CREATE INDEX IX_ProgresoModulo_FechaFin ON Instituto_ProgresoModulo(FechaFinalizacion);
CREATE INDEX IX_ProgresoModulo_FechaVenc ON Instituto_ProgresoModulo(FechaVencimiento);

-- Índice compuesto para reportes por periodo
CREATE INDEX IX_ProgresoModulo_Reporte
ON Instituto_ProgresoModulo(IdModulo, EstatusModuloUsuario, FechaFinalizacion);

-- Módulo: búsquedas por estado y fechas
CREATE INDEX IX_Modulo_Activo ON Instituto_Modulo(Activo);
CREATE INDEX IX_Modulo_FechaInicio ON Instituto_Modulo(FechaInicioModulo);

-- Unidad de Negocio
CREATE INDEX IX_UnidadNegocio_Activo ON Instituto_UnidadDeNegocio(Activo);

-- Departamento
CREATE INDEX IX_Departamento_Unidad ON Instituto_Departamento(IdUnidadDeNegocio);
CREATE INDEX IX_Departamento_Activo ON Instituto_Departamento(Activo);

-- AuditoriaAcceso: consultas por usuario y fecha
CREATE INDEX IX_Auditoria_Usuario ON Instituto_AuditoriaAcceso(IdUsuario);
CREATE INDEX IX_Auditoria_Fecha ON Instituto_AuditoriaAcceso(FechaAccion);

-- Soporte: consultas por usuario y estado
CREATE INDEX IX_Soporte_Usuario ON Instituto_Soporte(IdUsuario);
CREATE INDEX IX_Soporte_Estado ON Instituto_Soporte(Estatus);
```

---

### 5. **MEJORAS EN MÓDULO**

**Agregar campos útiles:**
```sql
CREATE TABLE Instituto_Modulo (
    IdModulo INT PRIMARY KEY IDENTITY(1,1),
    NombreModulo VARCHAR(255) UNIQUE NOT NULL,

    -- FECHAS
    FechaInicioModulo DATE,
    FechaCierre DATE,

    -- INFORMACIÓN ADICIONAL
    Descripcion VARCHAR(MAX),
    DuracionEstimadaHoras DECIMAL(5,2),      -- ✅ NUEVO: Para estimaciones
    PuntajeMinimoAprobatorio DECIMAL(5,2),   -- ✅ NUEVO: % mínimo para aprobar

    -- CONFIGURACIÓN
    PermiteReintentos BIT DEFAULT 1,         -- ✅ NUEVO: ¿Se puede reintentar?
    NumeroMaximoIntentos INT DEFAULT 3,      -- ✅ NUEVO: Límite de intentos
    ObligatorioParaTodos BIT DEFAULT 0,      -- ✅ NUEVO: ¿Es obligatorio?

    -- ESTADO
    Activo BIT DEFAULT 1,

    -- AUDITORÍA
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE()
);
```

---

### 6. **TABLA DE NIVELES DE MANDO (NUEVA)**

**Razón:** Tu aplicación genera reportes por niveles de mando, pero no tienes una tabla para gestionarlos.

```sql
CREATE TABLE Instituto_NivelMando (
    IdNivelMando INT PRIMARY KEY IDENTITY(1,1),
    NombreNivel VARCHAR(100) UNIQUE NOT NULL,
    -- Ej: 'Mandos Gerenciales', 'Mandos Medios', 'Mandos Administrativos Operativos'
    Orden INT,  -- Para ordenamiento: 1, 2, 3
    Descripcion VARCHAR(MAX),
    Activo BIT DEFAULT 1
);

-- Insertar niveles predeterminados
INSERT INTO Instituto_NivelMando (NombreNivel, Orden, Descripcion) VALUES
('Mandos Gerenciales', 1, 'Dirección y alta gerencia'),
('Mandos Medios', 2, 'Jefaturas y coordinaciones'),
('Mandos Administrativos Operativos', 3, 'Personal operativo y administrativo');
```

**Modificar Usuario para usar esta tabla:**
```sql
ALTER TABLE Instituto_Usuario
ADD IdNivelMando INT,
    FOREIGN KEY (IdNivelMando) REFERENCES Instituto_NivelMando(IdNivelMando);
```

---

### 7. **TRIGGERS PARA AUDITORÍA AUTOMÁTICA**

**Implementar triggers para actualización automática de campos:**

```sql
-- Trigger para actualizar FechaModificacion en Usuario
CREATE TRIGGER TR_Usuario_UpdateModified
ON Instituto_Usuario
AFTER UPDATE
AS
BEGIN
    UPDATE Instituto_Usuario
    SET FechaModificacion = GETDATE()
    FROM Instituto_Usuario u
    INNER JOIN inserted i ON u.IdUsuario = i.IdUsuario;
END;
GO

-- Trigger para actualizar FechaModificacion en ProgresoModulo
CREATE TRIGGER TR_ProgresoModulo_UpdateModified
ON Instituto_ProgresoModulo
AFTER UPDATE
AS
BEGIN
    UPDATE Instituto_ProgresoModulo
    SET FechaModificacion = GETDATE()
    FROM Instituto_ProgresoModulo pm
    INNER JOIN inserted i ON pm.IdInscripcion = i.IdInscripcion;
END;
GO

-- Trigger para registrar cambios de estado en HistorialProgreso
CREATE TRIGGER TR_ProgresoModulo_LogChanges
ON Instituto_ProgresoModulo
AFTER UPDATE
AS
BEGIN
    INSERT INTO Instituto_HistorialProgreso
        (IdInscripcion, EstatusAnterior, EstatusNuevo, Comentario)
    SELECT
        i.IdInscripcion,
        d.EstatusModuloUsuario,
        i.EstatusModuloUsuario,
        'Cambio automático de estado'
    FROM inserted i
    INNER JOIN deleted d ON i.IdInscripcion = d.IdInscripcion
    WHERE i.EstatusModuloUsuario != d.EstatusModuloUsuario;
END;
GO
```

---

### 8. **VISTAS PARA REPORTES (PERFORMANCE)**

**Crear vistas materializadas para reportes comunes:**

```sql
-- Vista: Resumen de usuarios con su progreso
CREATE VIEW VW_ResumenUsuarioProgreso AS
SELECT
    u.IdUsuario,
    u.UserId,
    u.Nombre,
    u.Email,
    u.Nivel,
    un.NombreUnidad,
    nm.NombreNivel as NivelMando,
    COUNT(pm.IdInscripcion) as TotalModulosAsignados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as ModulosEnProceso,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as ModulosRegistrados,
    AVG(pm.CalificacionModuloUsuario) as PromedioCalificacion
FROM Instituto_Usuario u
LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN Instituto_NivelMando nm ON u.IdNivelMando = nm.IdNivelMando
LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE u.Activo = 1
GROUP BY u.IdUsuario, u.UserId, u.Nombre, u.Email, u.Nivel,
         un.NombreUnidad, nm.NombreNivel;
GO

-- Vista: Resumen de módulos con estadísticas
CREATE VIEW VW_ResumenModuloEstadisticas AS
SELECT
    m.IdModulo,
    m.NombreModulo,
    m.FechaInicioModulo,
    m.FechaCierre,
    COUNT(pm.IdInscripcion) as TotalInscritos,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as EnProceso,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrados,
    AVG(pm.CalificacionModuloUsuario) as PromedioCalificacion,
    CAST(SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) * 100.0
         / NULLIF(COUNT(pm.IdInscripcion), 0) AS DECIMAL(5,2)) as PorcentajeCompletado
FROM Instituto_Modulo m
LEFT JOIN Instituto_ProgresoModulo pm ON m.IdModulo = pm.IdModulo
WHERE m.Activo = 1
GROUP BY m.IdModulo, m.NombreModulo, m.FechaInicioModulo, m.FechaCierre;
GO

-- Vista: Progreso por unidad de negocio
CREATE VIEW VW_ProgresoUnidadNegocio AS
SELECT
    un.IdUnidadDeNegocio,
    un.NombreUnidad,
    COUNT(DISTINCT u.IdUsuario) as TotalUsuarios,
    COUNT(pm.IdInscripcion) as TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as TotalCompletados,
    CAST(SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) * 100.0
         / NULLIF(COUNT(pm.IdInscripcion), 0) AS DECIMAL(5,2)) as PorcentajeCompletado
FROM Instituto_UnidadDeNegocio un
LEFT JOIN Instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE un.Activo = 1
GROUP BY un.IdUnidadDeNegocio, un.NombreUnidad;
GO
```

---

### 9. **STORED PROCEDURES PARA OPERACIONES COMUNES**

```sql
-- SP: Obtener reporte de usuario por ID
CREATE PROCEDURE SP_ObtenerReporteUsuario
    @UserId VARCHAR(50)
AS
BEGIN
    SELECT
        u.UserId,
        u.Nombre,
        u.Email,
        un.NombreUnidad,
        u.Nivel,
        m.NombreModulo,
        pm.EstatusModuloUsuario,
        pm.CalificacionModuloUsuario,
        pm.PorcentajeProgreso,
        pm.FechaAsignacion,
        pm.FechaFinalizacion
    FROM Instituto_Usuario u
    LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
    LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
    LEFT JOIN Instituto_Modulo m ON pm.IdModulo = m.IdModulo
    WHERE u.UserId = @UserId
    ORDER BY m.NombreModulo;
END;
GO

-- SP: Obtener reporte por periodo
CREATE PROCEDURE SP_ObtenerReportePeriodo
    @FechaInicio DATE,
    @FechaFin DATE,
    @IdModulo INT = NULL
AS
BEGIN
    SELECT
        u.UserId,
        u.Nombre,
        m.NombreModulo,
        pm.EstatusModuloUsuario,
        pm.FechaFinalizacion,
        pm.CalificacionModuloUsuario
    FROM Instituto_ProgresoModulo pm
    INNER JOIN Instituto_Usuario u ON pm.UserId = u.UserId
    INNER JOIN Instituto_Modulo m ON pm.IdModulo = m.IdModulo
    WHERE pm.FechaFinalizacion BETWEEN @FechaInicio AND @FechaFin
        AND (@IdModulo IS NULL OR pm.IdModulo = @IdModulo)
    ORDER BY pm.FechaFinalizacion DESC;
END;
GO

-- SP: Obtener estadísticas globales
CREATE PROCEDURE SP_ObtenerEstadisticasGlobales
AS
BEGIN
    SELECT
        (SELECT COUNT(*) FROM Instituto_Usuario WHERE Activo = 1) as TotalUsuarios,
        (SELECT COUNT(*) FROM Instituto_Modulo WHERE Activo = 1) as TotalModulos,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo) as TotalInscripciones,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo WHERE EstatusModuloUsuario = 'Completado') as TotalCompletados,
        (SELECT AVG(CalificacionModuloUsuario) FROM Instituto_ProgresoModulo WHERE CalificacionModuloUsuario IS NOT NULL) as PromedioGeneral;
END;
GO
```

---

## 📋 RESUMEN DE CAMBIOS RECOMENDADOS

### 🔴 CRÍTICOS (Hazlos YA)
1. ✅ Agregar prefijo `Instituto_` a TODAS las tablas
2. ✅ Agregar campo `Activo` a Usuario
3. ✅ Renombrar `NombreCompleto` → `Nombre` y `UserEmail` → `Email`
4. ✅ Renombrar `EstatusModulo` → `EstatusModuloUsuario`
5. ✅ Agregar `CalificacionModuloUsuario` y `FechaInicio` a ProgresoModulo
6. ✅ Crear índices para performance

### 🟡 IMPORTANTES (Hazlos pronto)
7. ✅ Agregar tabla `Instituto_NivelMando`
8. ✅ Agregar campos de auditoría (FechaCreacion, FechaModificacion)
9. ✅ Crear vistas para reportes
10. ✅ Implementar triggers de auditoría

### 🟢 OPCIONALES (Mejoras futuras)
11. ✅ Crear stored procedures
12. ✅ Agregar campos adicionales a Módulo (duración, intentos)
13. ✅ Implementar políticas de retención de datos
14. ✅ Agregar tabla de configuración del sistema

---

## 📊 DIAGRAMA ENTIDAD-RELACIÓN MEJORADO

```
┌─────────────────────┐
│  Instituto_Rol      │
│─────────────────────│
│ PK: IdRol          │
│     NombreRol      │
│     Descripcion    │
│     Activo         │
└─────────────────────┘
         │
         │ 1:N
         ↓
┌──────────────────────────────┐         ┌─────────────────────────┐
│  Instituto_Usuario           │         │ Instituto_NivelMando    │
│──────────────────────────────│         │─────────────────────────│
│ PK: IdUsuario               │    N:1  │ PK: IdNivelMando       │
│ UK: UserId                  │◄────────│     NombreNivel        │
│ FK: IdUnidadDeNegocio      │         │     Orden              │
│ FK: IdRol                  │         │     Activo             │
│ FK: IdNivelMando           │         └─────────────────────────┘
│     Nombre                 │
│     Email                  │         ┌─────────────────────────┐
│     Nivel                  │    N:1  │ Instituto_Modulo        │
│     Position               │◄────────│─────────────────────────│
│     Activo                 │         │ PK: IdModulo           │
│     FechaCreacion          │         │     NombreModulo       │
└──────────────────────────────┘         │     FechaInicio        │
         │                               │     FechaCierre        │
         │ N:1                           │     Activo             │
         ↓                               └─────────────────────────┘
┌──────────────────────────────┐                │
│ Instituto_UnidadDeNegocio    │                │
│──────────────────────────────│                │
│ PK: IdUnidadDeNegocio       │                │
│     NombreUnidad            │                │ 1:N
│     Activo                  │                ↓
└──────────────────────────────┘         ┌────────────────────────────────┐
         │                               │ Instituto_ProgresoModulo        │
         │ 1:N                           │────────────────────────────────│
         ↓                               │ PK: IdInscripcion              │
┌──────────────────────────────┐         │ FK: UserId                     │
│ Instituto_Departamento       │         │ FK: IdModulo                   │
│──────────────────────────────│         │ UK: (UserId, IdModulo)         │
│ PK: IdDepartamento          │         │     EstatusModuloUsuario       │
│ FK: IdUnidadDeNegocio       │         │     CalificacionModuloUsuario  │
│     NombreDepartamento      │         │     PorcentajeProgreso         │
│     Activo                  │         │     FechaAsignacion            │
└──────────────────────────────┘         │     FechaInicio                │
                                        │     FechaFinalizacion          │
                                        └────────────────────────────────┘
                                                 │
                                                 │ 1:N
                                                 ↓
                                        ┌────────────────────────────────┐
                                        │ Instituto_HistorialProgreso     │
                                        │────────────────────────────────│
                                        │ PK: IdHistorial                │
                                        │ FK: IdInscripcion              │
                                        │     EstatusAnterior            │
                                        │     EstatusNuevo               │
                                        │     FechaCambio                │
                                        └────────────────────────────────┘
```

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

1. **Backup de BD actual** (si ya tienes datos)
2. **Aplicar script SQL corregido** (ver archivo adjunto)
3. **Actualizar código Python** para usar nombres correctos
4. **Crear índices**
5. **Implementar vistas**
6. **Testing completo**

---

¿Quieres que genere el script SQL completo corregido con todos estos cambios?
