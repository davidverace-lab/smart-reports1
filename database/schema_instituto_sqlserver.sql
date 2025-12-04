-- ═════════════════════════════════════════════════════════════════
-- SCHEMA SQL SERVER - INSTITUTO HUTCHISON PORTS
-- Smart Reports - Sistema de Capacitación
-- ═════════════════════════════════════════════════════════════════
-- Base de Datos: InstitutoHutchison
-- Motor: Microsoft SQL Server 2019+
-- Última actualización: 18 de Noviembre, 2025
-- ═════════════════════════════════════════════════════════════════

USE master;
GO

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'InstitutoHutchison')
BEGIN
    CREATE DATABASE InstitutoHutchison;
    PRINT '✅ Base de datos InstitutoHutchison creada';
END
ELSE
BEGIN
    PRINT 'ℹ️  Base de datos InstitutoHutchison ya existe';
END
GO

USE InstitutoHutchison;
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT 'ELIMINANDO TABLAS EXISTENTES (si existen)';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Eliminar tablas en orden correcto (respetando FKs)
IF OBJECT_ID('instituto_ReporteCompartido', 'U') IS NOT NULL DROP TABLE instituto_ReporteCompartido;
IF OBJECT_ID('instituto_ReporteGuardado', 'U') IS NOT NULL DROP TABLE instituto_ReporteGuardado;
IF OBJECT_ID('instituto_SoporteSeguimiento', 'U') IS NOT NULL DROP TABLE instituto_SoporteSeguimiento;
IF OBJECT_ID('instituto_Soporte', 'U') IS NOT NULL DROP TABLE instituto_Soporte;
IF OBJECT_ID('instituto_ResultadoEvaluacion', 'U') IS NOT NULL DROP TABLE instituto_ResultadoEvaluacion;
IF OBJECT_ID('instituto_Evaluacion', 'U') IS NOT NULL DROP TABLE instituto_Evaluacion;
IF OBJECT_ID('instituto_ProgresoModulo', 'U') IS NOT NULL DROP TABLE instituto_ProgresoModulo;
IF OBJECT_ID('instituto_ModuloDepartamento', 'U') IS NOT NULL DROP TABLE instituto_ModuloDepartamento;
IF OBJECT_ID('instituto_Modulo', 'U') IS NOT NULL DROP TABLE instituto_Modulo;
IF OBJECT_ID('instituto_Usuario', 'U') IS NOT NULL DROP TABLE instituto_Usuario;
IF OBJECT_ID('instituto_Posicion', 'U') IS NOT NULL DROP TABLE instituto_Posicion;
IF OBJECT_ID('instituto_Departamento', 'U') IS NOT NULL DROP TABLE instituto_Departamento;
IF OBJECT_ID('instituto_UnidadDeNegocio', 'U') IS NOT NULL DROP TABLE instituto_UnidadDeNegocio;
IF OBJECT_ID('instituto_RolPermiso', 'U') IS NOT NULL DROP TABLE instituto_RolPermiso;
IF OBJECT_ID('instituto_Permiso', 'U') IS NOT NULL DROP TABLE instituto_Permiso;
IF OBJECT_ID('instituto_Rol', 'U') IS NOT NULL DROP TABLE instituto_Rol;
IF OBJECT_ID('instituto_AuditoriaCambios', 'U') IS NOT NULL DROP TABLE instituto_AuditoriaCambios;
IF OBJECT_ID('instituto_AuditoriaAcceso', 'U') IS NOT NULL DROP TABLE instituto_AuditoriaAcceso;
IF OBJECT_ID('instituto_Plantilla', 'U') IS NOT NULL DROP TABLE instituto_Plantilla;
IF OBJECT_ID('instituto_Configuracion', 'U') IS NOT NULL DROP TABLE instituto_Configuracion;

PRINT '✅ Tablas eliminadas';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '1. MÓDULO DE ROLES Y PERMISOS';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Rol
CREATE TABLE instituto_Rol (
    IdRol INT IDENTITY(1,1) NOT NULL,
    NombreRol VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Rol PRIMARY KEY (IdRol),
    CONSTRAINT UK_NombreRol UNIQUE (NombreRol)
);
PRINT '✅ Tabla instituto_Rol creada';
GO

-- Tabla: instituto_Permiso
CREATE TABLE instituto_Permiso (
    IdPermiso INT IDENTITY(1,1) NOT NULL,
    NombrePermiso VARCHAR(150) NOT NULL,
    Recurso VARCHAR(255) NOT NULL,
    Accion VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    CONSTRAINT PK_instituto_Permiso PRIMARY KEY (IdPermiso),
    CONSTRAINT UK_RecursoAccion UNIQUE (Recurso, Accion)
);
PRINT '✅ Tabla instituto_Permiso creada';
GO

-- Tabla: instituto_RolPermiso
CREATE TABLE instituto_RolPermiso (
    IdRolPermiso INT IDENTITY(1,1) NOT NULL,
    IdRol INT NOT NULL,
    IdPermiso INT NOT NULL,
    Permitir BIT DEFAULT 1,
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_RolPermiso PRIMARY KEY (IdRolPermiso),
    CONSTRAINT FK_RolPermiso_Rol FOREIGN KEY (IdRol) REFERENCES instituto_Rol(IdRol) ON DELETE CASCADE,
    CONSTRAINT FK_RolPermiso_Permiso FOREIGN KEY (IdPermiso) REFERENCES instituto_Permiso(IdPermiso) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_RolPermiso creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '2. MÓDULO ORGANIZACIONAL';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_UnidadDeNegocio
CREATE TABLE instituto_UnidadDeNegocio (
    IdUnidadDeNegocio INT IDENTITY(1,1) NOT NULL,
    NombreUnidad VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_UnidadDeNegocio PRIMARY KEY (IdUnidadDeNegocio)
);
PRINT '✅ Tabla instituto_UnidadDeNegocio creada';
GO

-- Tabla: instituto_Departamento
CREATE TABLE instituto_Departamento (
    IdDepartamento INT IDENTITY(1,1) NOT NULL,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(255) NOT NULL,
    Codigo VARCHAR(50),
    Descripcion TEXT,
    IdResponsable INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Departamento PRIMARY KEY (IdDepartamento),
    CONSTRAINT UK_CodigoDepto UNIQUE (Codigo),
    CONSTRAINT FK_Departamento_Unidad FOREIGN KEY (IdUnidadDeNegocio)
        REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_Departamento creada';
GO

-- Tabla: instituto_Posicion
CREATE TABLE instituto_Posicion (
    IdPosicion INT IDENTITY(1,1) NOT NULL,
    NombrePosicion VARCHAR(150) NOT NULL,
    Descripcion TEXT,
    IdDepartamento INT,
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_Posicion PRIMARY KEY (IdPosicion),
    CONSTRAINT FK_Posicion_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_Posicion creada';
GO

-- Tabla: instituto_Usuario
CREATE TABLE instituto_Usuario (
    IdUsuario INT IDENTITY(1,1) NOT NULL,
    UserId VARCHAR(100) NOT NULL,
    IdUnidadDeNegocio INT,
    IdDepartamento INT,
    IdRol INT NOT NULL,
    Nivel INT, -- ⭐ Ahora es INT en lugar de VARCHAR
    IdPosicion INT,
    NombreCompleto VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    TipoDeCorreo VARCHAR(50),
    UserStatus VARCHAR(50),
    Ubicacion VARCHAR(255),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Usuario PRIMARY KEY (IdUsuario),
    CONSTRAINT UK_UserId UNIQUE (UserId),
    CONSTRAINT UK_UserEmail UNIQUE (UserEmail),
    CONSTRAINT FK_Usuario_UnidadDeNegocio FOREIGN KEY (IdUnidadDeNegocio)
        REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio) ON DELETE SET NULL,
    CONSTRAINT FK_Usuario_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE SET NULL,
    CONSTRAINT FK_Usuario_Rol FOREIGN KEY (IdRol)
        REFERENCES instituto_Rol(IdRol),
    CONSTRAINT FK_Usuario_Posicion FOREIGN KEY (IdPosicion)
        REFERENCES instituto_Posicion(IdPosicion) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_Usuario creada';
GO

-- Agregar FK circular de Departamento.IdResponsable
ALTER TABLE instituto_Departamento
ADD CONSTRAINT FK_Departamento_Responsable FOREIGN KEY (IdResponsable)
    REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL;
PRINT '✅ FK circular Departamento.IdResponsable agregada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '3. MÓDULO DE CAPACITACIÓN';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Modulo
CREATE TABLE instituto_Modulo (
    IdModulo INT IDENTITY(1,1) NOT NULL,
    NombreModulo VARCHAR(255) NOT NULL,
    TipoDeCapacitacion VARCHAR(50),
    FechaInicio DATETIME,
    FechaCierre DATETIME,
    Descripcion TEXT,
    Prerequisitos NVARCHAR(MAX), -- JSON en SQL Server
    Obligatorio BIT DEFAULT 0,
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_Modulo PRIMARY KEY (IdModulo)
);
PRINT '✅ Tabla instituto_Modulo creada';
GO

-- Tabla: instituto_ModuloDepartamento
CREATE TABLE instituto_ModuloDepartamento (
    IdModuloDepto INT IDENTITY(1,1) NOT NULL,
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio BIT DEFAULT 0,
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    FechaVencimiento DATETIME,
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_ModuloDepartamento PRIMARY KEY (IdModuloDepto),
    CONSTRAINT FK_ModDepto_Modulo FOREIGN KEY (IdModulo)
        REFERENCES instituto_Modulo(IdModulo) ON DELETE CASCADE,
    CONSTRAINT FK_ModDepto_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_ModuloDepartamento creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '4. MÓDULO DE PROGRESO';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_ProgresoModulo
CREATE TABLE instituto_ProgresoModulo (
    IdInscripcion INT IDENTITY(1,1) NOT NULL,
    IdUsuario INT NOT NULL, -- ⭐ Ahora es FK a instituto_Usuario
    IdModulo INT NOT NULL,
    EstatusModulo VARCHAR(50),
    FechaAsignacion DATETIME,
    FechaVencimiento DATETIME,
    FechaInicio DATETIME,
    FechaFinalizacion DATETIME,
    CONSTRAINT PK_instituto_ProgresoModulo PRIMARY KEY (IdInscripcion),
    CONSTRAINT FK_ProgresoMod_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE,
    CONSTRAINT FK_ProgresoMod_Modulo FOREIGN KEY (IdModulo)
        REFERENCES instituto_Modulo(IdModulo) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_ProgresoModulo creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '5. MÓDULO DE EVALUACIONES';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Evaluacion
CREATE TABLE instituto_Evaluacion (
    IdEvaluacion INT IDENTITY(1,1) NOT NULL,
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    TipoEvaluacion VARCHAR(50),
    PuntajeMinimo DECIMAL(5,2),
    PuntajeMaximo DECIMAL(5,2),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Evaluacion PRIMARY KEY (IdEvaluacion),
    CONSTRAINT FK_Evaluacion_Modulo FOREIGN KEY (IdModulo)
        REFERENCES instituto_Modulo(IdModulo) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_Evaluacion creada';
GO

-- Tabla: instituto_ResultadoEvaluacion
CREATE TABLE instituto_ResultadoEvaluacion (
    IdResultado INT IDENTITY(1,1) NOT NULL,
    IdInscripcion INT NOT NULL,
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(5,2),
    Aprobado BIT,
    FechaRealizacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_ResultadoEvaluacion PRIMARY KEY (IdResultado),
    CONSTRAINT FK_Resultado_Inscripcion FOREIGN KEY (IdInscripcion)
        REFERENCES instituto_ProgresoModulo(IdInscripcion) ON DELETE CASCADE,
    CONSTRAINT FK_Resultado_Evaluacion FOREIGN KEY (IdEvaluacion)
        REFERENCES instituto_Evaluacion(IdEvaluacion) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_ResultadoEvaluacion creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '6. MÓDULO DE SOPORTE';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Soporte
CREATE TABLE instituto_Soporte (
    IdSoporte INT IDENTITY(1,1) NOT NULL,
    IdUsuario INT NOT NULL,
    FechaSolicitud DATETIME DEFAULT GETDATE(),
    Asunto VARCHAR(255) NOT NULL,
    Descripcion TEXT NOT NULL,
    Categoria VARCHAR(100),
    Prioridad INT DEFAULT 2,
    Estatus VARCHAR(50),
    IdAsignado INT,
    FechaRespuesta DATETIME,
    FechaCierre DATETIME,
    Respuesta TEXT,
    SatisfaccionUser INT,
    CONSTRAINT PK_instituto_Soporte PRIMARY KEY (IdSoporte),
    CONSTRAINT FK_Soporte_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE,
    CONSTRAINT FK_Soporte_Asignado FOREIGN KEY (IdAsignado)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_Soporte creada';
GO

-- Tabla: instituto_SoporteSeguimiento
CREATE TABLE instituto_SoporteSeguimiento (
    IdSeguimiento INT IDENTITY(1,1) NOT NULL,
    IdSoporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoAccion VARCHAR(50),
    Comentario TEXT,
    FechaAccion DATETIME DEFAULT GETDATE(),
    AdjuntoUrl VARCHAR(512),
    CONSTRAINT PK_instituto_SoporteSeguimiento PRIMARY KEY (IdSeguimiento),
    CONSTRAINT FK_Seguimiento_Soporte FOREIGN KEY (IdSoporte)
        REFERENCES instituto_Soporte(IdSoporte) ON DELETE CASCADE,
    CONSTRAINT FK_Seguimiento_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_SoporteSeguimiento creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '7. MÓDULO DE REPORTES';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_ReporteGuardado
CREATE TABLE instituto_ReporteGuardado (
    IdReporte INT IDENTITY(1,1) NOT NULL,
    IdUsuarioCreador INT NOT NULL,
    NombreReporte VARCHAR(255) NOT NULL,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    TipoReporte VARCHAR(100),
    Descripcion TEXT,
    FiltrosJSON NVARCHAR(MAX), -- JSON
    Compartido BIT DEFAULT 0,
    Favorito BIT DEFAULT 0,
    UltimaEjecucion DATETIME,
    NumeroEjecuciones INT DEFAULT 0,
    CONSTRAINT PK_instituto_ReporteGuardado PRIMARY KEY (IdReporte),
    CONSTRAINT FK_Reporte_Creador FOREIGN KEY (IdUsuarioCreador)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_ReporteGuardado creada';
GO

-- Tabla: instituto_ReporteCompartido
CREATE TABLE instituto_ReporteCompartido (
    IdCompartido INT IDENTITY(1,1) NOT NULL,
    IdReporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    PermisoEdicion BIT DEFAULT 0,
    FechaCompartido DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_ReporteCompartido PRIMARY KEY (IdCompartido),
    CONSTRAINT FK_ReporteComp_Reporte FOREIGN KEY (IdReporte)
        REFERENCES instituto_ReporteGuardado(IdReporte) ON DELETE CASCADE,
    CONSTRAINT FK_ReporteComp_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_ReporteCompartido creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '8. MÓDULO DE AUDITORÍA';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_AuditoriaAcceso
CREATE TABLE instituto_AuditoriaAcceso (
    IdAuditoria INT IDENTITY(1,1) NOT NULL,
    IdUsuario INT,
    Accion VARCHAR(100) NOT NULL,
    Modulo VARCHAR(100),
    Detalle TEXT,
    DireccionIP VARCHAR(45),
    UserAgent TEXT,
    Exito BIT,
    FechaAccion DATETIME DEFAULT GETDATE(),
    DuracionMs INT,
    CONSTRAINT PK_instituto_AuditoriaAcceso PRIMARY KEY (IdAuditoria),
    CONSTRAINT FK_AuditoriaAcc_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_AuditoriaAcceso creada';
GO

-- Tabla: instituto_AuditoriaCambios
CREATE TABLE instituto_AuditoriaCambios (
    IdAuditCambio INT IDENTITY(1,1) NOT NULL,
    Tabla VARCHAR(100) NOT NULL,
    IdRegistro INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoCambio VARCHAR(10),
    ValoresAnteriores NVARCHAR(MAX), -- JSON
    ValoresNuevos NVARCHAR(MAX), -- JSON
    FechaCambio DATETIME DEFAULT GETDATE(),
    DireccionIP VARCHAR(45),
    CONSTRAINT PK_instituto_AuditoriaCambios PRIMARY KEY (IdAuditCambio),
    CONSTRAINT FK_AuditoriaCam_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
);
PRINT '✅ Tabla instituto_AuditoriaCambios creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '9. MÓDULO DE CONFIGURACIÓN Y PLANTILLAS';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Configuracion
CREATE TABLE instituto_Configuracion (
    IdConfig INT IDENTITY(1,1) NOT NULL,
    Clave VARCHAR(100) NOT NULL,
    Valor TEXT,
    Tipo VARCHAR(50),
    Descripcion TEXT,
    Categoria VARCHAR(100),
    Editable BIT DEFAULT 1,
    IdUsuarioMod INT,
    FechaModificacion DATETIME,
    CONSTRAINT PK_instituto_Configuracion PRIMARY KEY (IdConfig),
    CONSTRAINT UK_Clave UNIQUE (Clave),
    CONSTRAINT FK_Config_UsuarioMod FOREIGN KEY (IdUsuarioMod)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_Configuracion creada';
GO

-- Tabla: instituto_Plantilla
CREATE TABLE instituto_Plantilla (
    IdPlantilla INT IDENTITY(1,1) NOT NULL,
    NombrePlantilla VARCHAR(150) NOT NULL,
    TipoPlantilla VARCHAR(50),
    Contenido NVARCHAR(MAX), -- LONGTEXT equivalente
    VariablesJSON NVARCHAR(MAX), -- JSON
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Plantilla PRIMARY KEY (IdPlantilla),
    CONSTRAINT UK_NombrePlantilla UNIQUE (NombrePlantilla)
);
PRINT '✅ Tabla instituto_Plantilla creada';
GO

PRINT '';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT 'SCRIPT COMPLETADO EXITOSAMENTE';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Tablas creadas:';
PRINT '  ✅ 21 tablas principales';
PRINT '  ✅ Relaciones y Foreign Keys configuradas';
PRINT '  ✅ Índices únicos aplicados';
PRINT '';
PRINT 'Próximos pasos:';
PRINT '  1. Insertar datos maestros (Roles, Permisos, Unidades)';
PRINT '  2. Configurar usuarios administradores';
PRINT '  3. Ejecutar ETL para importar datos de CSOD';
PRINT '═════════════════════════════════════════════════════════════════════════';
GO
