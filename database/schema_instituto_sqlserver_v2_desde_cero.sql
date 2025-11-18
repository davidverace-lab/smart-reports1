-- ═════════════════════════════════════════════════════════════════════════════
-- SCRIPT DDL COMPLETO - DATA MART DE CAPACITACIÓN (SQL SERVER)
-- Versión 2.0 - DESDE CERO (Sin tablas previas)
-- Compatible con: SQL Server 2016 o superior
-- ═════════════════════════════════════════════════════════════════════════════
--
-- IMPORTANTE: Este script elimina TODAS las tablas instituto_* existentes
-- y las recrea desde cero. Asegúrate de tener un backup si hay datos previos.
--
-- ═════════════════════════════════════════════════════════════════════════════

USE master;
GO

-- ═════════════════════════════════════════════════════════════════════════════
-- PASO 1: CREAR BASE DE DATOS (si no existe)
-- ═════════════════════════════════════════════════════════════════════════════

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'InstitutoHutchison')
BEGIN
    CREATE DATABASE InstitutoHutchison
    COLLATE SQL_Latin1_General_CP1_CI_AS;
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
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT 'INICIO: Creación de esquema desde cero';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT '';
GO

-- ═════════════════════════════════════════════════════════════════════════════
-- PASO 2: ELIMINAR TODAS LAS TABLAS EXISTENTES (en orden correcto)
-- ═════════════════════════════════════════════════════════════════════════════

PRINT 'Eliminando tablas existentes...';
GO

-- Eliminar en orden inverso a las dependencias de FK
IF OBJECT_ID('instituto_ReporteCompartido', 'U') IS NOT NULL DROP TABLE instituto_ReporteCompartido;
IF OBJECT_ID('instituto_ReporteGuardado', 'U') IS NOT NULL DROP TABLE instituto_ReporteGuardado;
IF OBJECT_ID('instituto_SoporteSeguimiento', 'U') IS NOT NULL DROP TABLE instituto_SoporteSeguimiento;
IF OBJECT_ID('instituto_Soporte', 'U') IS NOT NULL DROP TABLE instituto_Soporte;
IF OBJECT_ID('instituto_ResultadoEvaluacion', 'U') IS NOT NULL DROP TABLE instituto_ResultadoEvaluacion;
IF OBJECT_ID('instituto_Evaluacion', 'U') IS NOT NULL DROP TABLE instituto_Evaluacion;
IF OBJECT_ID('instituto_ProgresoModulo', 'U') IS NOT NULL DROP TABLE instituto_ProgresoModulo;
IF OBJECT_ID('instituto_ModuloDepartamento', 'U') IS NOT NULL DROP TABLE instituto_ModuloDepartamento;
IF OBJECT_ID('instituto_Modulo', 'U') IS NOT NULL DROP TABLE instituto_Modulo;
IF OBJECT_ID('instituto_ConfiguracionModulos', 'U') IS NOT NULL DROP TABLE instituto_ConfiguracionModulos;
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

PRINT '✅ Tablas antiguas eliminadas';
PRINT '';
GO

-- ═════════════════════════════════════════════════════════════════════════════
-- PASO 3: CREAR TABLAS (en orden correcto según dependencias)
-- ═════════════════════════════════════════════════════════════════════════════

PRINT '══════════════════════════════════════════════════════════════';
PRINT '1. MÓDULO DE SEGURIDAD';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Rol
CREATE TABLE instituto_Rol (
    IdRol INT IDENTITY(1,1) NOT NULL,
    NombreRol VARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Rol PRIMARY KEY (IdRol),
    CONSTRAINT UQ_instituto_Rol_NombreRol UNIQUE (NombreRol)
);
PRINT '✅ Tabla instituto_Rol creada';
GO

-- Tabla: instituto_Permiso
CREATE TABLE instituto_Permiso (
    IdPermiso INT IDENTITY(1,1) NOT NULL,
    NombrePermiso VARCHAR(150) NOT NULL,
    Recurso VARCHAR(255) NOT NULL,
    Accion VARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(MAX),
    CONSTRAINT PK_instituto_Permiso PRIMARY KEY (IdPermiso),
    CONSTRAINT UQ_instituto_Permiso_RecursoAccion UNIQUE (Recurso, Accion)
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
    CONSTRAINT FK_RolPermiso_Permiso FOREIGN KEY (IdPermiso) REFERENCES instituto_Permiso(IdPermiso) ON DELETE CASCADE,
    CONSTRAINT UQ_RolPermiso UNIQUE (IdRol, IdPermiso)
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
    Codigo VARCHAR(50),
    Descripcion NVARCHAR(MAX),
    IdResponsable INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_UnidadDeNegocio PRIMARY KEY (IdUnidadDeNegocio),
    CONSTRAINT UQ_instituto_UnidadDeNegocio_Codigo UNIQUE (Codigo)
);
PRINT '✅ Tabla instituto_UnidadDeNegocio creada';
GO

-- Tabla: instituto_Departamento
CREATE TABLE instituto_Departamento (
    IdDepartamento INT IDENTITY(1,1) NOT NULL,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(255) NOT NULL,
    Codigo VARCHAR(50),
    Descripcion NVARCHAR(MAX),
    IdResponsable INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Departamento PRIMARY KEY (IdDepartamento),
    CONSTRAINT FK_Departamento_Unidad FOREIGN KEY (IdUnidadDeNegocio)
        REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio) ON DELETE CASCADE,
    CONSTRAINT UQ_instituto_Departamento_Codigo UNIQUE (Codigo)
);
PRINT '✅ Tabla instituto_Departamento creada';
GO

-- Tabla: instituto_Posicion
CREATE TABLE instituto_Posicion (
    IdPosicion INT IDENTITY(1,1) NOT NULL,
    NombrePosicion VARCHAR(150) NOT NULL,
    Descripcion NVARCHAR(MAX),
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
    IdPosicion INT,
    NombreCompleto VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Position VARCHAR(150), -- ⭐ Mapea a "Usuario - Cargo" del Excel
    Nivel VARCHAR(100), -- ⭐ Mapea a "Usuario - Nivel" del Excel
    TipoDeCorreo VARCHAR(50),
    UserStatus VARCHAR(50),
    Ubicacion VARCHAR(255),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    UltimoAcceso DATETIME,
    CONSTRAINT PK_instituto_Usuario PRIMARY KEY (IdUsuario),
    CONSTRAINT UQ_instituto_Usuario_UserId UNIQUE (UserId),
    CONSTRAINT UQ_instituto_Usuario_UserEmail UNIQUE (UserEmail),
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

-- Agregar FKs de responsables (circular references)
ALTER TABLE instituto_UnidadDeNegocio
    ADD CONSTRAINT FK_Unidad_Responsable FOREIGN KEY (IdResponsable)
    REFERENCES instituto_Usuario(IdUsuario);

ALTER TABLE instituto_Departamento
    ADD CONSTRAINT FK_Departamento_Responsable FOREIGN KEY (IdResponsable)
    REFERENCES instituto_Usuario(IdUsuario);

PRINT '✅ Foreign Keys de responsables agregadas';
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
    TipoDeCapacitacion VARCHAR(50), -- ⭐ 'Curriculum' o 'Prueba' (mapea a "Tipo de capacitación" del Excel)
    FechaInicio DATETIME,
    FechaCierre DATETIME,
    Descripcion NVARCHAR(MAX),
    DuracionEstHoras DECIMAL(5, 2),
    IdCreador INT,
    Prerequisitos NVARCHAR(MAX),
    Obligatorio BIT DEFAULT 0,
    NivelDificultad INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Modulo PRIMARY KEY (IdModulo),
    CONSTRAINT FK_Modulo_Creador FOREIGN KEY (IdCreador)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
);
PRINT '✅ Tabla instituto_Modulo creada';
GO

-- Tabla: instituto_ConfiguracionModulos (para escalabilidad)
CREATE TABLE instituto_ConfiguracionModulos (
    IdConfigModulo INT IDENTITY(1,1) NOT NULL,
    NumeroModulo INT NOT NULL,
    NombreModulo VARCHAR(255) NOT NULL,
    NombrePrueba VARCHAR(255),
    Activo BIT DEFAULT 1,
    FechaActivacion DATETIME DEFAULT GETDATE(),
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_ConfiguracionModulos PRIMARY KEY (IdConfigModulo),
    CONSTRAINT UQ_instituto_ConfiguracionModulos_NumeroModulo UNIQUE (NumeroModulo)
);
PRINT '✅ Tabla instituto_ConfiguracionModulos creada';
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
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE CASCADE,
    CONSTRAINT UQ_ModuloDepartamento UNIQUE (IdModulo, IdDepartamento)
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
    UserId VARCHAR(100) NOT NULL, -- ⭐ Usar UserId directamente para compatibilidad con Excel
    IdModulo INT NOT NULL,
    EstatusModulo VARCHAR(50), -- ⭐ Mapea a "Estado del expediente" del Excel
    TiempoInvertido INT DEFAULT 0,
    FechaAsignacion DATETIME,
    FechaVencimiento DATETIME,
    FechaInicio DATETIME, -- ⭐ Mapea a "Fecha de inicio de la capacitación" del Excel
    FechaFinalizacion DATETIME, -- ⭐ Mapea a "Fecha de finalización de expediente" del Excel
    CONSTRAINT PK_instituto_ProgresoModulo PRIMARY KEY (IdInscripcion),
    CONSTRAINT UQ_UsuarioModulo UNIQUE (UserId, IdModulo)
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
    Descripcion NVARCHAR(MAX),
    TipoEvaluacion VARCHAR(50),
    PuntajeMinimo DECIMAL(5, 2) DEFAULT 70.00, -- ⭐ Default 70% (no viene en Excel)
    PuntajeMaximo DECIMAL(5, 2) DEFAULT 100.00,
    IntentosPermitid INT DEFAULT 3, -- ⭐ Default 3 intentos (no viene en Excel)
    TiempoLimite INT,
    MostrarRespuestas BIT DEFAULT 0,
    Aleatorizar BIT DEFAULT 0,
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
    PuntajeObtenido DECIMAL(5, 2), -- ⭐ Viene del Excel "Puntuación de la transcripción"
    Aprobado BIT,
    IntentoNumero INT,
    FechaRealizacion DATETIME DEFAULT GETDATE(),
    TiempoInvertido INT,
    RespuestasJSON NVARCHAR(MAX),
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
    Descripcion NVARCHAR(MAX) NOT NULL,
    Categoria VARCHAR(100),
    Prioridad INT DEFAULT 2,
    Estatus VARCHAR(50),
    IdAsignado INT,
    FechaRespuesta DATETIME,
    FechaCierre DATETIME,
    Respuesta NVARCHAR(MAX),
    SatisfaccionUser INT,
    CONSTRAINT PK_instituto_Soporte PRIMARY KEY (IdSoporte),
    CONSTRAINT FK_Soporte_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE,
    CONSTRAINT FK_Soporte_Asignado FOREIGN KEY (IdAsignado)
        REFERENCES instituto_Usuario(IdUsuario)
);
PRINT '✅ Tabla instituto_Soporte creada';
GO

-- Tabla: instituto_SoporteSeguimiento
CREATE TABLE instituto_SoporteSeguimiento (
    IdSeguimiento INT IDENTITY(1,1) NOT NULL,
    IdSoporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoAccion VARCHAR(50),
    Comentario NVARCHAR(MAX),
    FechaAccion DATETIME DEFAULT GETDATE(),
    AdjuntoUrl VARCHAR(512),
    CONSTRAINT PK_instituto_SoporteSeguimiento PRIMARY KEY (IdSeguimiento),
    CONSTRAINT FK_Seguimiento_Soporte FOREIGN KEY (IdSoporte)
        REFERENCES instituto_Soporte(IdSoporte) ON DELETE CASCADE,
    CONSTRAINT FK_Seguimiento_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario)
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
    Descripcion NVARCHAR(MAX),
    FiltrosJSON NVARCHAR(MAX),
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
        REFERENCES instituto_Usuario(IdUsuario),
    CONSTRAINT UQ_ReporteUsuario UNIQUE (IdReporte, IdUsuario)
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
    Detalle NVARCHAR(MAX),
    DireccionIP VARCHAR(45),
    UserAgent NVARCHAR(MAX),
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
    ValoresAnteriores NVARCHAR(MAX),
    ValoresNuevos NVARCHAR(MAX),
    FechaCambio DATETIME DEFAULT GETDATE(),
    DireccionIP VARCHAR(45),
    CONSTRAINT PK_instituto_AuditoriaCambios PRIMARY KEY (IdAuditCambio),
    CONSTRAINT FK_AuditoriaCam_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario)
);
PRINT '✅ Tabla instituto_AuditoriaCambios creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '9. MÓDULO DE CONFIGURACIÓN';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Tabla: instituto_Configuracion
CREATE TABLE instituto_Configuracion (
    IdConfig INT IDENTITY(1,1) NOT NULL,
    Clave VARCHAR(100) NOT NULL,
    Valor NVARCHAR(MAX),
    Tipo VARCHAR(50),
    Descripcion NVARCHAR(MAX),
    Categoria VARCHAR(100),
    Editable BIT DEFAULT 1,
    IdUsuarioMod INT,
    FechaModificacion DATETIME,
    CONSTRAINT PK_instituto_Configuracion PRIMARY KEY (IdConfig),
    CONSTRAINT UQ_instituto_Configuracion_Clave UNIQUE (Clave),
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
    Contenido NVARCHAR(MAX),
    VariablesJSON NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Plantilla PRIMARY KEY (IdPlantilla),
    CONSTRAINT UQ_instituto_Plantilla_Nombre UNIQUE (NombrePlantilla)
);
PRINT '✅ Tabla instituto_Plantilla creada';
GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '10. CREAR ÍNDICES OPTIMIZADOS';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Usuario
CREATE INDEX IX_Usuario_UserEmail_Activo ON instituto_Usuario(UserEmail, Activo);
CREATE INDEX IX_Usuario_Activo ON instituto_Usuario(Activo);
CREATE INDEX IX_Usuario_Departamento ON instituto_Usuario(IdDepartamento) WHERE IdDepartamento IS NOT NULL;
PRINT '✅ Índices de Usuario creados';

-- Progreso
CREATE INDEX IX_ProgresoModulo_Usuario_Estatus ON instituto_ProgresoModulo(IdUsuario, EstatusModulo, IdModulo);
CREATE INDEX IX_ProgresoModulo_Estatus ON instituto_ProgresoModulo(EstatusModulo);
CREATE INDEX IX_ProgresoModulo_FechaAsignacion ON instituto_ProgresoModulo(FechaAsignacion DESC);
PRINT '✅ Índices de Progreso creados';

-- Evaluaciones
CREATE INDEX IX_Evaluacion_Modulo_Activo ON instituto_Evaluacion(IdModulo, Activo);
CREATE INDEX IX_ResultadoEvaluacion_FechaRealizacion ON instituto_ResultadoEvaluacion(FechaRealizacion DESC);
CREATE INDEX IX_ResultadoEvaluacion_Inscripcion ON instituto_ResultadoEvaluacion(IdInscripcion);
PRINT '✅ Índices de Evaluaciones creados';

-- Auditoría
CREATE INDEX IX_AuditoriaAcceso_FechaAccion ON instituto_AuditoriaAcceso(FechaAccion DESC);
PRINT '✅ Índices de Auditoría creados';

GO

PRINT '';
PRINT '══════════════════════════════════════════════════════════════';
PRINT '11. INSERTAR DATOS INICIALES';
PRINT '══════════════════════════════════════════════════════════════';
GO

-- Roles
SET IDENTITY_INSERT instituto_Rol ON;
INSERT INTO instituto_Rol (IdRol, NombreRol, Descripcion, Activo) VALUES
(1, 'Administrador', 'Acceso completo al sistema', 1),
(2, 'Instructor', 'Puede crear y gestionar módulos', 1),
(3, 'Empleado', 'Usuario estándar del sistema', 1),
(4, 'RRHH', 'Gestión de personal y reportes', 1);
SET IDENTITY_INSERT instituto_Rol OFF;
PRINT '✅ Roles insertados: 4';

-- Unidades de Negocio
SET IDENTITY_INSERT instituto_UnidadDeNegocio ON;
INSERT INTO instituto_UnidadDeNegocio (IdUnidadDeNegocio, NombreUnidad, Codigo, Descripcion, Activo) VALUES
(1, 'ICAVE', 'ICAVE', 'Infraestructura y Concesiones de Alta Velocidad del Este', 1),
(2, 'EIT', 'EIT', 'Empresa de Infraestructura y Transporte', 1),
(3, 'LCT', 'LCT', 'Lázaro Cárdenas Terminal', 1),
(4, 'TIMSA', 'TIMSA', 'Terminal de Importación y Maniobras SA', 1),
(5, 'HPMX', 'HPMX', 'Hutchison Ports México', 1),
(6, 'TNG', 'TNG', 'TNG Container Terminal', 1),
(7, 'CCI', 'CCI', 'Container Corporation International', 1),
(8, 'TILH', 'TILH', 'Terminal de Importación Lázaro Hermanos', 1),
(9, 'ECV', 'ECV', 'Empresa de Contenedores del Valle', 1),
(10, 'HPLM', 'HPLM', 'Hutchison Ports Lázaro México', 1),
(11, 'LCMT', 'LCMT', 'Lázaro Cárdenas Multimodal Terminal', 1);
SET IDENTITY_INSERT instituto_UnidadDeNegocio OFF;
PRINT '✅ Unidades de Negocio insertadas: 11';

-- Configuración de Módulos (14 módulos)
SET IDENTITY_INSERT instituto_ConfiguracionModulos ON;
INSERT INTO instituto_ConfiguracionModulos (IdConfigModulo, NumeroModulo, NombreModulo, NombrePrueba, Activo) VALUES
(1, 1, 'MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS', 'INTRODUCCIÓN A LA FILOSOFÍA', 1),
(2, 2, 'MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 'SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 1),
(3, 3, 'MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES', 'INTRODUCCIÓN A LAS OPERACIONES', 1),
(4, 4, 'MÓDULO 4 . RELACIONES LABORALES', 'RELACIONES LABORALES', 1),
(5, 5, 'MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES', 'Seguridad en las Operaciones', 1),
(6, 6, 'MÓDULO 6 . CIBERSEGURIDAD', 'Ciberseguridad', 1),
(7, 7, 'MÓDULO 7 . ENTORNO LABORAL SALUDABLE', 'Entorno Laboral Saludable', 1),
(8, 8, 'MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS', 'Procesos de Recursos Humanos', 1),
(9, 9, 'MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL', NULL, 0),
(10, 10, 'MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS', NULL, 0),
(11, 11, 'MÓDULO 11 . PRODUCTOS DIGITALES DE HP', NULL, 0),
(12, 12, 'MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD', NULL, 0),
(13, 13, 'MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA', NULL, 0),
(14, 14, 'MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA', NULL, 0);
SET IDENTITY_INSERT instituto_ConfiguracionModulos OFF;
PRINT '✅ Configuración de Módulos insertada: 14';

GO

PRINT '';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT '✅ ESQUEMA CREADO EXITOSAMENTE DESDE CERO';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT '';
PRINT 'Resumen:';
PRINT '  • Total de tablas: 22';
PRINT '  • Total de índices: 10';
PRINT '  • Total de foreign keys: 25+';
PRINT '  • Roles iniciales: 4';
PRINT '  • Unidades de negocio: 11';
PRINT '  • Módulos configurados: 14';
PRINT '';
PRINT 'Tablas principales para ETL:';
PRINT '  ✓ instituto_Usuario';
PRINT '  ✓ instituto_Modulo (con campo TipoDeCapacitacion)';
PRINT '  ✓ instituto_ProgresoModulo';
PRINT '  ✓ instituto_Evaluacion (con defaults PuntajeMinimo=70, IntentosPermitid=3)';
PRINT '  ✓ instituto_ResultadoEvaluacion';
PRINT '  ✓ instituto_ConfiguracionModulos (para escalabilidad)';
PRINT '';
PRINT 'Mapeo Excel → BD:';
PRINT '  • "Título de capacitación" → NombreModulo (instituto_Modulo)';
PRINT '  • "Tipo de capacitación" → TipoDeCapacitacion (instituto_Modulo)';
PRINT '  • "Identificación de usuario" → UserId (instituto_Usuario)';
PRINT '  • "Estado del expediente" → EstatusModulo (instituto_ProgresoModulo)';
PRINT '  • "Puntuación de la transcripción" → PuntajeObtenido (instituto_ResultadoEvaluacion)';
PRINT '';
PRINT '═════════════════════════════════════════════════════════════════════════';
PRINT 'SCRIPT COMPLETADO';
PRINT '═════════════════════════════════════════════════════════════════════════';
GO
