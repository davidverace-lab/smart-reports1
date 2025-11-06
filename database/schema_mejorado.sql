-- =====================================================================
-- SMART REPORTS - INSTITUTO HUTCHISON PORTS
-- ESQUEMA DE BASE DE DATOS MEJORADO Y CORREGIDO
-- Versión: 2.0
-- Fecha: 2024
-- =====================================================================

-- =====================================================================
-- SECCIÓN 1: TABLAS BASE (Sin dependencias)
-- =====================================================================

-- 1. Tabla Rol
CREATE TABLE Instituto_Rol (
    IdRol INT PRIMARY KEY IDENTITY(1,1),
    NombreRol VARCHAR(50) UNIQUE NOT NULL,
    Descripcion VARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE()
);

-- 2. Tabla UnidadDeNegocio
CREATE TABLE Instituto_UnidadDeNegocio (
    IdUnidadDeNegocio INT PRIMARY KEY IDENTITY(1,1),
    NombreUnidad VARCHAR(100) UNIQUE NOT NULL,
    Codigo VARCHAR(20),  -- Código corto para la unidad
    Descripcion VARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE()
);

-- 3. Tabla Modulo
CREATE TABLE Instituto_Modulo (
    IdModulo INT PRIMARY KEY IDENTITY(1,1),
    NombreModulo VARCHAR(255) UNIQUE NOT NULL,

    -- Fechas
    FechaInicioModulo DATE,
    FechaCierre DATE,

    -- Información
    Descripcion VARCHAR(MAX),
    DuracionEstimadaHoras DECIMAL(5,2),

    -- Configuración de evaluación
    PuntajeMinimoAprobatorio DECIMAL(5,2) DEFAULT 70.00,
    PermiteReintentos BIT DEFAULT 1,
    NumeroMaximoIntentos INT DEFAULT 3,
    ObligatorioParaTodos BIT DEFAULT 0,

    -- Estado
    Activo BIT DEFAULT 1,

    -- Auditoría
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE()
);

-- 4. Tabla NivelMando (NUEVA)
CREATE TABLE Instituto_NivelMando (
    IdNivelMando INT PRIMARY KEY IDENTITY(1,1),
    NombreNivel VARCHAR(100) UNIQUE NOT NULL,
    Orden INT NOT NULL,  -- Para ordenamiento jerárquico
    Descripcion VARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE()
);

-- =====================================================================
-- SECCIÓN 2: TABLAS CON DEPENDENCIAS DE NIVEL 1
-- =====================================================================

-- 5. Tabla Departamento (Depende de UnidadDeNegocio)
CREATE TABLE Instituto_Departamento (
    IdDepartamento INT PRIMARY KEY IDENTITY(1,1),
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(150) NOT NULL,
    Codigo VARCHAR(20),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES Instituto_UnidadDeNegocio(IdUnidadDeNegocio)
);

-- 6. Tabla Usuario (Depende de UnidadDeNegocio, Rol, NivelMando)
CREATE TABLE Instituto_Usuario (
    IdUsuario INT PRIMARY KEY IDENTITY(1,1),

    -- Identificadores
    UserId VARCHAR(50) UNIQUE NOT NULL,  -- ID externo (de Cornerstone LMS)

    -- Relaciones
    IdUnidadDeNegocio INT,
    IdRol INT,
    IdNivelMando INT,

    -- Información básica (nombres simples usados en código)
    Nombre VARCHAR(255) NOT NULL,       -- Nombre completo del usuario
    Email VARCHAR(255),                  -- Email principal

    -- Campos adicionales opcionales
    NombreCompleto VARCHAR(255),         -- Si difiere de Nombre
    UserEmail VARCHAR(255),              -- Email alternativo

    -- Información organizacional
    Nivel VARCHAR(50),                   -- Ej: "Gerente", "Coordinador"
    Division VARCHAR(100),
    Position VARCHAR(100),               -- Puesto/Cargo
    Grupo VARCHAR(100),
    Ubicacion VARCHAR(100),
    TipoDeCorreo VARCHAR(50),

    -- Seguridad
    PasswordHash VARCHAR(255),           -- Hash BCrypt para autenticación
    UltimoAcceso DATETIME,

    -- Estado
    UserStatus VARCHAR(50) DEFAULT 'Activo',
    Activo BIT DEFAULT 1,                -- Campo crítico para filtrado

    -- Auditoría
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES Instituto_UnidadDeNegocio(IdUnidadDeNegocio),
    FOREIGN KEY (IdRol) REFERENCES Instituto_Rol(IdRol),
    FOREIGN KEY (IdNivelMando) REFERENCES Instituto_NivelMando(IdNivelMando)
);

-- 7. Tabla Evaluacion (Depende de Modulo)
CREATE TABLE Instituto_Evaluacion (
    IdEvaluacion INT PRIMARY KEY IDENTITY(1,1),
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255) NOT NULL,
    TipoEvaluacion VARCHAR(50),  -- Ej: "Quiz", "Examen Final", "Práctica"
    PuntajeMinimoAprobatorio DECIMAL(5,2) DEFAULT 70.00,
    TiempoLimiteMinutos INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdModulo) REFERENCES Instituto_Modulo(IdModulo)
);

-- =====================================================================
-- SECCIÓN 3: TABLAS CON DEPENDENCIAS DE NIVEL 2
-- =====================================================================

-- 8. Tabla ModuloDepartamento (Depende de Modulo y Departamento)
CREATE TABLE Instituto_ModuloDepartamento (
    IdModuloDepto INT PRIMARY KEY IDENTITY(1,1),
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio BIT DEFAULT 0,
    FechaAsignacion DATE DEFAULT CONVERT(DATE, GETDATE()),
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdModulo) REFERENCES Instituto_Modulo(IdModulo),
    FOREIGN KEY (IdDepartamento) REFERENCES Instituto_Departamento(IdDepartamento),
    CONSTRAINT UQ_Modulo_Depto UNIQUE (IdModulo, IdDepartamento)
);

-- 9. Tabla ProgresoModulo (Depende de Usuario y Modulo)
-- NOMBRES DE CAMPOS CORREGIDOS PARA COINCIDIR CON EL CÓDIGO
CREATE TABLE Instituto_ProgresoModulo (
    IdInscripcion INT PRIMARY KEY IDENTITY(1,1),
    UserId VARCHAR(50) NOT NULL,         -- FK a Usuario.UserId
    IdModulo INT NOT NULL,

    -- Estados (nombre correcto usado en código)
    EstatusModuloUsuario VARCHAR(50) DEFAULT 'Registrado',
    -- Valores posibles: 'Registrado', 'En Proceso', 'Completado', 'Vencido', 'No Iniciado'

    -- Fechas
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    FechaInicio DATETIME,                -- Cuando el usuario inicia el módulo
    FechaVencimiento DATETIME,
    FechaFinalizacion DATETIME,

    -- Calificaciones y progreso (campos usados en código)
    CalificacionModuloUsuario DECIMAL(5,2),  -- Calificación final obtenida
    PorcentajeProgreso INT DEFAULT 0,        -- 0-100%
    IntentosRealizados INT DEFAULT 0,

    -- Auditoría
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (UserId) REFERENCES Instituto_Usuario(UserId) ON DELETE CASCADE,
    FOREIGN KEY (IdModulo) REFERENCES Instituto_Modulo(IdModulo) ON DELETE CASCADE,
    CONSTRAINT UQ_Usuario_Modulo UNIQUE (UserId, IdModulo)
);

-- 10. Tabla ResultadoEvaluacion (Depende de ProgresoModulo y Evaluacion)
CREATE TABLE Instituto_ResultadoEvaluacion (
    IdResultado INT PRIMARY KEY IDENTITY(1,1),
    IdInscripcion INT NOT NULL,
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(5,2),
    PuntajeMaximo DECIMAL(5,2),
    Aprobado BIT,
    IntentoNumero INT DEFAULT 1,
    TiempoEmpleadoMinutos INT,
    FechaRealizacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdInscripcion) REFERENCES Instituto_ProgresoModulo(IdInscripcion) ON DELETE CASCADE,
    FOREIGN KEY (IdEvaluacion) REFERENCES Instituto_Evaluacion(IdEvaluacion)
);

-- 11. Tabla HistorialProgreso (Depende de ProgresoModulo)
CREATE TABLE Instituto_HistorialProgreso (
    IdHistorial INT PRIMARY KEY IDENTITY(1,1),
    IdInscripcion INT NOT NULL,
    EstatusAnterior VARCHAR(50),
    EstatusNuevo VARCHAR(50),
    FechaCambio DATETIME DEFAULT GETDATE(),
    Comentario VARCHAR(MAX),
    UsuarioQueModifico VARCHAR(100),  -- Usuario del sistema que hizo el cambio
    FOREIGN KEY (IdInscripcion) REFERENCES Instituto_ProgresoModulo(IdInscripcion) ON DELETE CASCADE
);

-- =====================================================================
-- SECCIÓN 4: TABLAS DE AUDITORÍA Y SOPORTE
-- =====================================================================

-- 12. Tabla AuditoriaAcceso (Depende de Usuario)
CREATE TABLE Instituto_AuditoriaAcceso (
    IdAuditoria INT PRIMARY KEY IDENTITY(1,1),
    IdUsuario INT,
    Accion VARCHAR(255),                 -- Ej: "Login", "Logout", "Update", "Delete"
    Modulo VARCHAR(100),                 -- Módulo de la aplicación
    Detalle VARCHAR(MAX),
    DireccionIP VARCHAR(50),
    Exito BIT DEFAULT 1,
    FechaAccion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdUsuario) REFERENCES Instituto_Usuario(IdUsuario)
);

-- 13. Tabla Soporte (Depende de Usuario)
CREATE TABLE Instituto_Soporte (
    IdSoporte INT PRIMARY KEY IDENTITY(1,1),
    IdUsuario INT,
    FechaSolicitud DATETIME DEFAULT GETDATE(),
    Asunto VARCHAR(255) NOT NULL,
    Descripcion VARCHAR(MAX),
    Prioridad VARCHAR(20) DEFAULT 'Media',  -- Alta, Media, Baja
    Categoria VARCHAR(50),                   -- Técnico, Académico, Otro
    Estatus VARCHAR(50) DEFAULT 'Abierto',   -- Abierto, En Proceso, Resuelto, Cerrado
    FechaCierre DATETIME,
    RespuestaAdmin VARCHAR(MAX),
    FOREIGN KEY (IdUsuario) REFERENCES Instituto_Usuario(IdUsuario)
);

-- 14. Tabla ReporteGuardado (Depende de Usuario)
CREATE TABLE Instituto_ReporteGuardado (
    IdReporte INT PRIMARY KEY IDENTITY(1,1),
    IdUsuarioCreador INT NOT NULL,
    NombreReporte VARCHAR(255) NOT NULL,
    TipoReporte VARCHAR(100),            -- Ej: "Usuario", "Periodo", "Global", "NivelesMando"
    FiltrosJSON VARCHAR(MAX),            -- JSON con los filtros aplicados
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaUltimoAcceso DATETIME,
    FOREIGN KEY (IdUsuarioCreador) REFERENCES Instituto_Usuario(IdUsuario)
);

-- =====================================================================
-- SECCIÓN 5: TABLA DE CONFIGURACIÓN DEL SISTEMA (NUEVA)
-- =====================================================================

CREATE TABLE Instituto_ConfiguracionSistema (
    IdConfig INT PRIMARY KEY IDENTITY(1,1),
    Clave VARCHAR(100) UNIQUE NOT NULL,  -- Ej: "SMTP_SERVER", "MAX_FILE_SIZE"
    Valor VARCHAR(MAX),
    Tipo VARCHAR(50),                    -- String, Integer, Boolean, JSON
    Descripcion VARCHAR(MAX),
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaModificacion DATETIME DEFAULT GETDATE()
);

-- =====================================================================
-- SECCIÓN 6: ÍNDICES PARA PERFORMANCE
-- =====================================================================

-- Índices en Usuario
CREATE INDEX IX_Usuario_Email ON Instituto_Usuario(Email);
CREATE INDEX IX_Usuario_Nombre ON Instituto_Usuario(Nombre);
CREATE INDEX IX_Usuario_Unidad ON Instituto_Usuario(IdUnidadDeNegocio);
CREATE INDEX IX_Usuario_Activo ON Instituto_Usuario(Activo);
CREATE INDEX IX_Usuario_Nivel ON Instituto_Usuario(Nivel);
CREATE INDEX IX_Usuario_NivelMando ON Instituto_Usuario(IdNivelMando);

-- Índices en ProgresoModulo (críticos para reportes)
CREATE INDEX IX_ProgresoModulo_Estado ON Instituto_ProgresoModulo(EstatusModuloUsuario);
CREATE INDEX IX_ProgresoModulo_Usuario ON Instituto_ProgresoModulo(UserId);
CREATE INDEX IX_ProgresoModulo_Modulo ON Instituto_ProgresoModulo(IdModulo);
CREATE INDEX IX_ProgresoModulo_FechaFin ON Instituto_ProgresoModulo(FechaFinalizacion);
CREATE INDEX IX_ProgresoModulo_FechaVenc ON Instituto_ProgresoModulo(FechaVencimiento);

-- Índice compuesto para reportes por periodo (optimización crítica)
CREATE INDEX IX_ProgresoModulo_Reporte
ON Instituto_ProgresoModulo(IdModulo, EstatusModuloUsuario, FechaFinalizacion)
INCLUDE (UserId, CalificacionModuloUsuario);

-- Índices en Módulo
CREATE INDEX IX_Modulo_Activo ON Instituto_Modulo(Activo);
CREATE INDEX IX_Modulo_FechaInicio ON Instituto_Modulo(FechaInicioModulo);
CREATE INDEX IX_Modulo_FechaCierre ON Instituto_Modulo(FechaCierre);

-- Índices en UnidadDeNegocio
CREATE INDEX IX_UnidadNegocio_Activo ON Instituto_UnidadDeNegocio(Activo);

-- Índices en Departamento
CREATE INDEX IX_Departamento_Unidad ON Instituto_Departamento(IdUnidadDeNegocio);
CREATE INDEX IX_Departamento_Activo ON Instituto_Departamento(Activo);

-- Índices en AuditoriaAcceso (para consultas de seguridad)
CREATE INDEX IX_Auditoria_Usuario ON Instituto_AuditoriaAcceso(IdUsuario);
CREATE INDEX IX_Auditoria_Fecha ON Instituto_AuditoriaAcceso(FechaAccion);
CREATE INDEX IX_Auditoria_Accion ON Instituto_AuditoriaAcceso(Accion);

-- Índices en Soporte
CREATE INDEX IX_Soporte_Usuario ON Instituto_Soporte(IdUsuario);
CREATE INDEX IX_Soporte_Estado ON Instituto_Soporte(Estatus);
CREATE INDEX IX_Soporte_Fecha ON Instituto_Soporte(FechaSolicitud);

-- Índices en ResultadoEvaluacion
CREATE INDEX IX_ResultadoEval_Inscripcion ON Instituto_ResultadoEvaluacion(IdInscripcion);
CREATE INDEX IX_ResultadoEval_Evaluacion ON Instituto_ResultadoEvaluacion(IdEvaluacion);

-- =====================================================================
-- SECCIÓN 7: TRIGGERS PARA AUDITORÍA AUTOMÁTICA
-- =====================================================================

-- Trigger: Actualizar FechaModificacion en Usuario
CREATE TRIGGER TR_Usuario_UpdateModified
ON Instituto_Usuario
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Instituto_Usuario
    SET FechaModificacion = GETDATE()
    FROM Instituto_Usuario u
    INNER JOIN inserted i ON u.IdUsuario = i.IdUsuario;
END;
GO

-- Trigger: Actualizar FechaModificacion en ProgresoModulo
CREATE TRIGGER TR_ProgresoModulo_UpdateModified
ON Instituto_ProgresoModulo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Instituto_ProgresoModulo
    SET FechaModificacion = GETDATE()
    FROM Instituto_ProgresoModulo pm
    INNER JOIN inserted i ON pm.IdInscripcion = i.IdInscripcion;
END;
GO

-- Trigger: Registrar cambios de estado en HistorialProgreso
CREATE TRIGGER TR_ProgresoModulo_LogChanges
ON Instituto_ProgresoModulo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Instituto_HistorialProgreso
        (IdInscripcion, EstatusAnterior, EstatusNuevo, Comentario, UsuarioQueModifico)
    SELECT
        i.IdInscripcion,
        d.EstatusModuloUsuario,
        i.EstatusModuloUsuario,
        'Cambio automático de estado',
        SUSER_SNAME()
    FROM inserted i
    INNER JOIN deleted d ON i.IdInscripcion = d.IdInscripcion
    WHERE i.EstatusModuloUsuario != d.EstatusModuloUsuario;
END;
GO

-- Trigger: Actualizar FechaInicio cuando cambia a "En Proceso"
CREATE TRIGGER TR_ProgresoModulo_SetFechaInicio
ON Instituto_ProgresoModulo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Instituto_ProgresoModulo
    SET FechaInicio = GETDATE()
    FROM Instituto_ProgresoModulo pm
    INNER JOIN inserted i ON pm.IdInscripcion = i.IdInscripcion
    INNER JOIN deleted d ON i.IdInscripcion = d.IdInscripcion
    WHERE i.EstatusModuloUsuario = 'En Proceso'
      AND (d.EstatusModuloUsuario != 'En Proceso' OR d.FechaInicio IS NULL)
      AND i.FechaInicio IS NULL;
END;
GO

-- =====================================================================
-- SECCIÓN 8: VISTAS PARA REPORTES
-- =====================================================================

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
    r.NombreRol,
    COUNT(pm.IdInscripcion) as TotalModulosAsignados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as ModulosEnProceso,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as ModulosRegistrados,
    AVG(pm.CalificacionModuloUsuario) as PromedioCalificacion,
    CAST(SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) * 100.0
         / NULLIF(COUNT(pm.IdInscripcion), 0) AS DECIMAL(5,2)) as PorcentajeCompletado
FROM Instituto_Usuario u
LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN Instituto_NivelMando nm ON u.IdNivelMando = nm.IdNivelMando
LEFT JOIN Instituto_Rol r ON u.IdRol = r.IdRol
LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE u.Activo = 1
GROUP BY u.IdUsuario, u.UserId, u.Nombre, u.Email, u.Nivel,
         un.NombreUnidad, nm.NombreNivel, r.NombreRol;
GO

-- Vista: Resumen de módulos con estadísticas
CREATE VIEW VW_ResumenModuloEstadisticas AS
SELECT
    m.IdModulo,
    m.NombreModulo,
    m.FechaInicioModulo,
    m.FechaCierre,
    m.DuracionEstimadaHoras,
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
GROUP BY m.IdModulo, m.NombreModulo, m.FechaInicioModulo, m.FechaCierre, m.DuracionEstimadaHoras;
GO

-- Vista: Progreso por unidad de negocio
CREATE VIEW VW_ProgresoUnidadNegocio AS
SELECT
    un.IdUnidadDeNegocio,
    un.NombreUnidad,
    COUNT(DISTINCT u.IdUsuario) as TotalUsuarios,
    COUNT(pm.IdInscripcion) as TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as TotalCompletados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as TotalEnProceso,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as TotalRegistrados,
    CAST(SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) * 100.0
         / NULLIF(COUNT(pm.IdInscripcion), 0) AS DECIMAL(5,2)) as PorcentajeCompletado
FROM Instituto_UnidadDeNegocio un
LEFT JOIN Instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio AND u.Activo = 1
LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE un.Activo = 1
GROUP BY un.IdUnidadDeNegocio, un.NombreUnidad;
GO

-- Vista: Progreso por nivel de mando (NUEVA - para reportes)
CREATE VIEW VW_ProgresoNivelMando AS
SELECT
    nm.IdNivelMando,
    nm.NombreNivel,
    nm.Orden,
    COUNT(DISTINCT u.IdUsuario) as TotalUsuarios,
    COUNT(pm.IdInscripcion) as TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as TotalCompletados,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as TotalEnProceso,
    SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as TotalRegistrados,
    CAST(SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) * 100.0
         / NULLIF(COUNT(pm.IdInscripcion), 0) AS DECIMAL(5,2)) as PorcentajeCompletado
FROM Instituto_NivelMando nm
LEFT JOIN Instituto_Usuario u ON nm.IdNivelMando = u.IdNivelMando AND u.Activo = 1
LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE nm.Activo = 1
GROUP BY nm.IdNivelMando, nm.NombreNivel, nm.Orden;
GO

-- =====================================================================
-- SECCIÓN 9: STORED PROCEDURES
-- =====================================================================

-- SP: Obtener reporte de usuario por ID
CREATE PROCEDURE SP_ObtenerReporteUsuario
    @UserId VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        u.UserId,
        u.Nombre,
        u.Email,
        un.NombreUnidad,
        u.Nivel,
        nm.NombreNivel as NivelMando,
        m.NombreModulo,
        pm.EstatusModuloUsuario,
        pm.CalificacionModuloUsuario,
        pm.PorcentajeProgreso,
        pm.FechaAsignacion,
        pm.FechaInicio,
        pm.FechaFinalizacion
    FROM Instituto_Usuario u
    LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
    LEFT JOIN Instituto_NivelMando nm ON u.IdNivelMando = nm.IdNivelMando
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
    SET NOCOUNT ON;
    SELECT
        u.UserId,
        u.Nombre,
        un.NombreUnidad,
        m.NombreModulo,
        pm.EstatusModuloUsuario,
        pm.FechaFinalizacion,
        pm.CalificacionModuloUsuario,
        pm.PorcentajeProgreso
    FROM Instituto_ProgresoModulo pm
    INNER JOIN Instituto_Usuario u ON pm.UserId = u.UserId
    INNER JOIN Instituto_Modulo m ON pm.IdModulo = m.IdModulo
    LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
    WHERE pm.FechaFinalizacion BETWEEN @FechaInicio AND @FechaFin
        AND (@IdModulo IS NULL OR pm.IdModulo = @IdModulo)
        AND u.Activo = 1
    ORDER BY pm.FechaFinalizacion DESC;
END;
GO

-- SP: Obtener estadísticas globales
CREATE PROCEDURE SP_ObtenerEstadisticasGlobales
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        (SELECT COUNT(*) FROM Instituto_Usuario WHERE Activo = 1) as TotalUsuarios,
        (SELECT COUNT(*) FROM Instituto_Modulo WHERE Activo = 1) as TotalModulos,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo) as TotalInscripciones,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo WHERE EstatusModuloUsuario = 'Completado') as TotalCompletados,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo WHERE EstatusModuloUsuario = 'En Proceso') as TotalEnProceso,
        (SELECT COUNT(*) FROM Instituto_ProgresoModulo WHERE EstatusModuloUsuario = 'Registrado') as TotalRegistrados,
        (SELECT AVG(CalificacionModuloUsuario) FROM Instituto_ProgresoModulo WHERE CalificacionModuloUsuario IS NOT NULL) as PromedioGeneral;
END;
GO

-- SP: Obtener reporte por niveles de mando
CREATE PROCEDURE SP_ObtenerReporteNivelesMando
    @IdModulo INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        nm.NombreNivel,
        nm.Orden,
        COUNT(DISTINCT u.IdUsuario) as Poblacion,
        SUM(CASE WHEN pm.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completado,
        SUM(CASE WHEN pm.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrado,
        SUM(CASE WHEN pm.EstatusModuloUsuario = 'En Proceso' THEN 1 ELSE 0 END) as EnProceso
    FROM Instituto_NivelMando nm
    LEFT JOIN Instituto_Usuario u ON nm.IdNivelMando = u.IdNivelMando AND u.Activo = 1
    LEFT JOIN Instituto_ProgresoModulo pm ON u.UserId = pm.UserId
        AND (@IdModulo IS NULL OR pm.IdModulo = @IdModulo)
    WHERE nm.Activo = 1
    GROUP BY nm.IdNivelMando, nm.NombreNivel, nm.Orden
    ORDER BY nm.Orden;
END;
GO

-- =====================================================================
-- SECCIÓN 10: DATOS INICIALES
-- =====================================================================

-- Insertar niveles de mando predeterminados
INSERT INTO Instituto_NivelMando (NombreNivel, Orden, Descripcion) VALUES
('Mandos Gerenciales', 1, 'Dirección y alta gerencia del instituto'),
('Mandos Medios', 2, 'Jefaturas, coordinaciones y supervisiones'),
('Mandos Administrativos Operativos', 3, 'Personal administrativo y operativo');
GO

-- Insertar roles predeterminados
INSERT INTO Instituto_Rol (NombreRol, Descripcion) VALUES
('Administrador', 'Acceso completo al sistema'),
('Instructor', 'Puede gestionar módulos y ver progreso de estudiantes'),
('Estudiante', 'Acceso a módulos asignados'),
('Supervisor', 'Puede ver reportes de su unidad de negocio');
GO

-- Insertar configuraciones iniciales del sistema
INSERT INTO Instituto_ConfiguracionSistema (Clave, Valor, Tipo, Descripcion) VALUES
('VERSION_SISTEMA', '2.0', 'String', 'Versión actual del sistema Smart Reports'),
('MAX_INTENTOS_LOGIN', '3', 'Integer', 'Máximo de intentos de login antes de bloquear'),
('DIAS_EXPIRACION_PASSWORD', '90', 'Integer', 'Días antes de que expire una contraseña'),
('SMTP_SERVER', '', 'String', 'Servidor SMTP para envío de correos'),
('EMAIL_NOTIFICACIONES', 'noreply@hutchison.com', 'String', 'Email remitente de notificaciones');
GO

-- =====================================================================
-- FIN DEL SCRIPT
-- =====================================================================

PRINT 'Base de datos Smart Reports creada exitosamente';
PRINT 'Versión: 2.0';
PRINT 'Tablas creadas: 14';
PRINT 'Vistas creadas: 4';
PRINT 'Stored Procedures creados: 4';
PRINT 'Triggers creados: 4';
GO
