-- ═════════════════════════════════════════════════════════════════════════════
-- SCRIPT DDL - DATA MART DE CAPACITACIÓN (SQL SERVER)
-- Optimizado para ETL desde Excel y Reportería
-- Versión: 3.0 - Análisis completo de requerimientos
-- Compatible con: SQL Server 2016 o superior
-- ═════════════════════════════════════════════════════════════════════════════

USE master;
GO

-- Crear base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'InstitutoHutchison')
BEGIN
    CREATE DATABASE InstitutoHutchison;
    PRINT 'Base de datos InstitutoHutchison creada exitosamente.';
END
ELSE
BEGIN
    PRINT 'Base de datos InstitutoHutchison ya existe.';
END
GO

USE InstitutoHutchison;
GO

-- =========================================
-- CONFIGURACIÓN INICIAL
-- =========================================

-- Deshabilitar restricciones de FK temporalmente para creación de tablas
EXEC sp_msforeachtable "ALTER TABLE ? NOCHECK CONSTRAINT ALL";
GO

PRINT '======================================================================';
PRINT 'INICIO DE CREACIÓN DE ESQUEMA - INSTITUTO HUTCHISON PORTS';
PRINT '======================================================================';
GO

-- ==========================================
-- 1. MÓDULO DE SEGURIDAD Y USUARIOS
-- ==========================================

PRINT 'Creando tablas del módulo de seguridad...';

-- Tabla: instituto_Rol
IF OBJECT_ID('instituto_Rol', 'U') IS NOT NULL
    DROP TABLE instituto_Rol;
GO

CREATE TABLE instituto_Rol (
    IdRol INT IDENTITY(1,1) NOT NULL,
    NombreRol VARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Rol PRIMARY KEY (IdRol),
    CONSTRAINT UQ_instituto_Rol_NombreRol UNIQUE (NombreRol)
);
GO

-- Tabla: instituto_Permiso
IF OBJECT_ID('instituto_Permiso', 'U') IS NOT NULL
    DROP TABLE instituto_Permiso;
GO

CREATE TABLE instituto_Permiso (
    IdPermiso INT IDENTITY(1,1) NOT NULL,
    NombrePermiso VARCHAR(150) NOT NULL,
    Recurso VARCHAR(255) NOT NULL,
    Accion VARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(MAX),
    CONSTRAINT PK_instituto_Permiso PRIMARY KEY (IdPermiso),
    CONSTRAINT UQ_instituto_Permiso_RecursoAccion UNIQUE (Recurso, Accion)
);
GO

-- Tabla: instituto_RolPermiso
IF OBJECT_ID('instituto_RolPermiso', 'U') IS NOT NULL
    DROP TABLE instituto_RolPermiso;
GO

CREATE TABLE instituto_RolPermiso (
    IdRolPermiso INT IDENTITY(1,1) NOT NULL,
    IdRol INT NOT NULL,
    IdPermiso INT NOT NULL,
    Permitir BIT DEFAULT 1,
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_RolPermiso PRIMARY KEY (IdRolPermiso)
);
GO

-- Tabla: instituto_Nivel
IF OBJECT_ID('instituto_Nivel', 'U') IS NOT NULL
    DROP TABLE instituto_Nivel;
GO

CREATE TABLE instituto_Nivel (
    IdNivel INT IDENTITY(1,1) NOT NULL,
    NombreNivel VARCHAR(100) NOT NULL,
    Jerarquia INT,
    Descripcion NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_Nivel PRIMARY KEY (IdNivel)
);
GO

-- Tabla: instituto_Posicion
IF OBJECT_ID('instituto_Posicion', 'U') IS NOT NULL
    DROP TABLE instituto_Posicion;
GO

CREATE TABLE instituto_Posicion (
    IdPosicion INT IDENTITY(1,1) NOT NULL,
    NombrePosicion VARCHAR(150) NOT NULL, -- Viene del Excel 'Cargo'
    Descripcion NVARCHAR(MAX),
    IdDepartamento INT,
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_Posicion PRIMARY KEY (IdPosicion)
);
GO

-- ==========================================
-- 2. MÓDULO ORGANIZACIONAL
-- ==========================================

PRINT 'Creando tablas del módulo organizacional...';

-- Tabla: instituto_UnidadDeNegocio
IF OBJECT_ID('instituto_UnidadDeNegocio', 'U') IS NOT NULL
    DROP TABLE instituto_UnidadDeNegocio;
GO

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
GO

-- Tabla: instituto_Departamento
IF OBJECT_ID('instituto_Departamento', 'U') IS NOT NULL
    DROP TABLE instituto_Departamento;
GO

CREATE TABLE instituto_Departamento (
    IdDepartamento INT IDENTITY(1,1) NOT NULL,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(255) NOT NULL, -- Viene del Excel 'Departamento'
    Codigo VARCHAR(50),
    Descripcion NVARCHAR(MAX),
    IdResponsable INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Departamento PRIMARY KEY (IdDepartamento),
    CONSTRAINT UQ_instituto_Departamento_Codigo UNIQUE (Codigo)
);
GO

-- Tabla: instituto_Usuario
IF OBJECT_ID('instituto_Usuario', 'U') IS NOT NULL
    DROP TABLE instituto_Usuario;
GO

CREATE TABLE instituto_Usuario (
    IdUsuario INT IDENTITY(1,1) NOT NULL,
    UserId VARCHAR(100) NOT NULL, -- ID del Excel (Llave Maestra)
    IdUnidadDeNegocio INT,
    IdDepartamento INT,
    IdRol INT NOT NULL,
    IdNivel INT,
    IdPosicion INT,
    NombreCompleto VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL, -- Puede ser genérico si usan SSO
    TipoDeCorreo VARCHAR(50),
    UserStatus VARCHAR(50),
    Ubicacion VARCHAR(255), -- Viene del Excel
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    UltimoAcceso DATETIME,
    CONSTRAINT PK_instituto_Usuario PRIMARY KEY (IdUsuario),
    CONSTRAINT UQ_instituto_Usuario_UserId UNIQUE (UserId),
    CONSTRAINT UQ_instituto_Usuario_UserEmail UNIQUE (UserEmail)
);
GO

-- ==========================================
-- 3. MÓDULO DE CAPACITACIÓN (Catálogos)
-- ==========================================

PRINT 'Creando tablas del módulo de capacitación...';

-- Tabla: instituto_Modulo
IF OBJECT_ID('instituto_Modulo', 'U') IS NOT NULL
    DROP TABLE instituto_Modulo;
GO

CREATE TABLE instituto_Modulo (
    IdModulo INT IDENTITY(1,1) NOT NULL,
    NombreModulo VARCHAR(255) NOT NULL,
    TipoDeCapacitacion VARCHAR(50), -- 'Curriculum' o 'Prueba'
    FechaInicio DATETIME,
    FechaCierre DATETIME,
    Descripcion NVARCHAR(MAX),
    DuracionEstHoras DECIMAL(5, 2),
    IdCreador INT,
    Prerequisitos NVARCHAR(MAX), -- JSON con IDs de módulos requeridos
    Obligatorio BIT DEFAULT 0,
    NivelDificultad INT,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Modulo PRIMARY KEY (IdModulo)
);
GO

-- Tabla: instituto_ModuloDepartamento
IF OBJECT_ID('instituto_ModuloDepartamento', 'U') IS NOT NULL
    DROP TABLE instituto_ModuloDepartamento;
GO

CREATE TABLE instituto_ModuloDepartamento (
    IdModuloDepto INT IDENTITY(1,1) NOT NULL,
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio BIT DEFAULT 0,
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    FechaVencimiento DATETIME,
    Activo BIT DEFAULT 1,
    CONSTRAINT PK_instituto_ModuloDepartamento PRIMARY KEY (IdModuloDepto)
);
GO

-- ==========================================
-- 4. MÓDULO DE PROGRESO (Estatus y Fechas)
-- ==========================================

PRINT 'Creando tablas del módulo de progreso...';

-- Tabla: instituto_ProgresoModulo
IF OBJECT_ID('instituto_ProgresoModulo', 'U') IS NOT NULL
    DROP TABLE instituto_ProgresoModulo;
GO

CREATE TABLE instituto_ProgresoModulo (
    IdInscripcion INT IDENTITY(1,1) NOT NULL,
    IdUsuario INT NOT NULL,
    IdModulo INT NOT NULL,
    EstatusModulo VARCHAR(50), -- Viene del Excel 'Estado del expediente'
    PorcentajeAvance INT DEFAULT 0,
    TiempoInvertido INT DEFAULT 0,
    FechaAsignacion DATETIME, -- Viene del Excel 'Fecha de registro'
    FechaVencimiento DATETIME,
    FechaInicio DATETIME,
    FechaFinalizacion DATETIME, -- Viene del Excel 'Fecha de finalización'
    IntentoActual INT DEFAULT 1,
    IntentosPermitido INT,
    CONSTRAINT PK_instituto_ProgresoModulo PRIMARY KEY (IdInscripcion)
);
GO

-- ==========================================
-- 5. MÓDULO DE EVALUACIONES (Calificaciones)
-- ==========================================

PRINT 'Creando tablas del módulo de evaluaciones...';

-- Tabla: instituto_Evaluacion
IF OBJECT_ID('instituto_Evaluacion', 'U') IS NOT NULL
    DROP TABLE instituto_Evaluacion;
GO

CREATE TABLE instituto_Evaluacion (
    IdEvaluacion INT IDENTITY(1,1) NOT NULL,
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255) NOT NULL,
    Descripcion NVARCHAR(MAX),
    TipoEvaluacion VARCHAR(50),
    PuntajeMinimo DECIMAL(5, 2),
    PuntajeMaximo DECIMAL(5, 2),
    IntentosPermitid INT,
    TiempoLimite INT,
    MostrarRespuestas BIT DEFAULT 0,
    Aleatorizar BIT DEFAULT 0,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Evaluacion PRIMARY KEY (IdEvaluacion)
);
GO

-- Tabla: instituto_ResultadoEvaluacion
IF OBJECT_ID('instituto_ResultadoEvaluacion', 'U') IS NOT NULL
    DROP TABLE instituto_ResultadoEvaluacion;
GO

CREATE TABLE instituto_ResultadoEvaluacion (
    IdResultado INT IDENTITY(1,1) NOT NULL,
    IdInscripcion INT NOT NULL, -- Relaciona con el progreso del usuario
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(5, 2), -- Viene del Excel 'Puntuación'
    Aprobado BIT,
    IntentoNumero INT,
    FechaRealizacion DATETIME DEFAULT GETDATE(),
    TiempoInvertido INT,
    RespuestasJSON NVARCHAR(MAX), -- JSON con respuestas
    CONSTRAINT PK_instituto_ResultadoEvaluacion PRIMARY KEY (IdResultado)
);
GO

-- ==========================================
-- 6. MÓDULO DE SOPORTE
-- ==========================================

PRINT 'Creando tablas del módulo de soporte...';

-- Tabla: instituto_Soporte
IF OBJECT_ID('instituto_Soporte', 'U') IS NOT NULL
    DROP TABLE instituto_Soporte;
GO

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
    CONSTRAINT PK_instituto_Soporte PRIMARY KEY (IdSoporte)
);
GO

-- Tabla: instituto_SoporteSeguimiento
IF OBJECT_ID('instituto_SoporteSeguimiento', 'U') IS NOT NULL
    DROP TABLE instituto_SoporteSeguimiento;
GO

CREATE TABLE instituto_SoporteSeguimiento (
    IdSeguimiento INT IDENTITY(1,1) NOT NULL,
    IdSoporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoAccion VARCHAR(50),
    Comentario NVARCHAR(MAX),
    FechaAccion DATETIME DEFAULT GETDATE(),
    AdjuntoUrl VARCHAR(512),
    CONSTRAINT PK_instituto_SoporteSeguimiento PRIMARY KEY (IdSeguimiento)
);
GO

-- ==========================================
-- 7. MÓDULO DE REPORTES (Dashboards)
-- ==========================================

PRINT 'Creando tablas del módulo de reportes...';

-- Tabla: instituto_ReporteGuardado
IF OBJECT_ID('instituto_ReporteGuardado', 'U') IS NOT NULL
    DROP TABLE instituto_ReporteGuardado;
GO

CREATE TABLE instituto_ReporteGuardado (
    IdReporte INT IDENTITY(1,1) NOT NULL,
    IdUsuarioCreador INT NOT NULL,
    NombreReporte VARCHAR(255) NOT NULL,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    TipoReporte VARCHAR(100),
    Descripcion NVARCHAR(MAX),
    FiltrosJSON NVARCHAR(MAX), -- Guarda la configuración del dashboard
    Compartido BIT DEFAULT 0,
    Favorito BIT DEFAULT 0,
    UltimaEjecucion DATETIME,
    NumeroEjecuciones INT DEFAULT 0,
    CONSTRAINT PK_instituto_ReporteGuardado PRIMARY KEY (IdReporte)
);
GO

-- Tabla: instituto_ReporteCompartido
IF OBJECT_ID('instituto_ReporteCompartido', 'U') IS NOT NULL
    DROP TABLE instituto_ReporteCompartido;
GO

CREATE TABLE instituto_ReporteCompartido (
    IdCompartido INT IDENTITY(1,1) NOT NULL,
    IdReporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    PermisoEdicion BIT DEFAULT 0,
    FechaCompartido DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_ReporteCompartido PRIMARY KEY (IdCompartido)
);
GO

-- ==========================================
-- 8. MÓDULO DE AUDITORÍA (Seguridad de Datos)
-- ==========================================

PRINT 'Creando tablas del módulo de auditoría...';

-- Tabla: instituto_AuditoriaAcceso
IF OBJECT_ID('instituto_AuditoriaAcceso', 'U') IS NOT NULL
    DROP TABLE instituto_AuditoriaAcceso;
GO

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
    CONSTRAINT PK_instituto_AuditoriaAcceso PRIMARY KEY (IdAuditoria)
);
GO

-- Tabla: instituto_AuditoriaCambios
IF OBJECT_ID('instituto_AuditoriaCambios', 'U') IS NOT NULL
    DROP TABLE instituto_AuditoriaCambios;
GO

CREATE TABLE instituto_AuditoriaCambios (
    IdAuditCambio INT IDENTITY(1,1) NOT NULL,
    Tabla VARCHAR(100) NOT NULL,
    IdRegistro INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoCambio VARCHAR(10), -- INSERT, UPDATE, DELETE
    ValoresAnteriores NVARCHAR(MAX), -- JSON
    ValoresNuevos NVARCHAR(MAX), -- JSON
    FechaCambio DATETIME DEFAULT GETDATE(),
    DireccionIP VARCHAR(45),
    CONSTRAINT PK_instituto_AuditoriaCambios PRIMARY KEY (IdAuditCambio)
);
GO

-- ==========================================
-- 9. MÓDULO DE CONFIGURACIÓN
-- ==========================================

PRINT 'Creando tablas del módulo de configuración...';

-- Tabla: instituto_Configuracion
IF OBJECT_ID('instituto_Configuracion', 'U') IS NOT NULL
    DROP TABLE instituto_Configuracion;
GO

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
    CONSTRAINT UQ_instituto_Configuracion_Clave UNIQUE (Clave)
);
GO

-- Tabla: instituto_Plantilla
IF OBJECT_ID('instituto_Plantilla', 'U') IS NOT NULL
    DROP TABLE instituto_Plantilla;
GO

CREATE TABLE instituto_Plantilla (
    IdPlantilla INT IDENTITY(1,1) NOT NULL,
    NombrePlantilla VARCHAR(150) NOT NULL,
    TipoPlantilla VARCHAR(50),
    Contenido NVARCHAR(MAX),
    VariablesJSON NVARCHAR(MAX), -- JSON
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_Plantilla PRIMARY KEY (IdPlantilla),
    CONSTRAINT UQ_instituto_Plantilla_Nombre UNIQUE (NombrePlantilla)
);
GO

-- ==========================================
-- 10. TABLA DE CONFIGURACIÓN DE MÓDULOS (NUEVA)
-- ==========================================

PRINT 'Creando tabla de configuración de módulos...';

-- Tabla: instituto_ConfiguracionModulos
IF OBJECT_ID('instituto_ConfiguracionModulos', 'U') IS NOT NULL
    DROP TABLE instituto_ConfiguracionModulos;
GO

CREATE TABLE instituto_ConfiguracionModulos (
    IdConfigModulo INT IDENTITY(1,1) NOT NULL,
    NumeroModulo INT NOT NULL,
    NombreModulo VARCHAR(255) NOT NULL,
    NombrePrueba VARCHAR(255), -- Nombre de la evaluación en Excel
    Activo BIT DEFAULT 1,
    FechaActivacion DATETIME DEFAULT GETDATE(),
    FechaCreacion DATETIME DEFAULT GETDATE(),
    CONSTRAINT PK_instituto_ConfiguracionModulos PRIMARY KEY (IdConfigModulo),
    CONSTRAINT UQ_instituto_ConfiguracionModulos_NumeroModulo UNIQUE (NumeroModulo)
);
GO

-- ==========================================
-- SECCIÓN DE LLAVES FORÁNEAS (FOREIGN KEYS)
-- ==========================================

PRINT 'Creando llaves foráneas...';

-- Seguridad
ALTER TABLE instituto_RolPermiso
    ADD CONSTRAINT FK_RolPermiso_Rol FOREIGN KEY (IdRol) REFERENCES instituto_Rol (IdRol) ON DELETE CASCADE;

ALTER TABLE instituto_RolPermiso
    ADD CONSTRAINT FK_RolPermiso_Permiso FOREIGN KEY (IdPermiso) REFERENCES instituto_Permiso (IdPermiso) ON DELETE CASCADE;

ALTER TABLE instituto_RolPermiso
    ADD CONSTRAINT UQ_RolPermiso UNIQUE (IdRol, IdPermiso);

ALTER TABLE instituto_Posicion
    ADD CONSTRAINT FK_Posicion_Departamento FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento (IdDepartamento) ON DELETE SET NULL;

ALTER TABLE instituto_Usuario
    ADD CONSTRAINT FK_Usuario_UnidadDeNegocio FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_UnidadDeNegocio (IdUnidadDeNegocio) ON DELETE SET NULL;

ALTER TABLE instituto_Usuario
    ADD CONSTRAINT FK_Usuario_Departamento FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento (IdDepartamento) ON DELETE SET NULL;

ALTER TABLE instituto_Usuario
    ADD CONSTRAINT FK_Usuario_Rol FOREIGN KEY (IdRol) REFERENCES instituto_Rol (IdRol);

ALTER TABLE instituto_Usuario
    ADD CONSTRAINT FK_Usuario_Nivel FOREIGN KEY (IdNivel) REFERENCES instituto_Nivel (IdNivel) ON DELETE SET NULL;

ALTER TABLE instituto_Usuario
    ADD CONSTRAINT FK_Usuario_Posicion FOREIGN KEY (IdPosicion) REFERENCES instituto_Posicion (IdPosicion) ON DELETE SET NULL;

-- Organizacional
ALTER TABLE instituto_UnidadDeNegocio
    ADD CONSTRAINT FK_Unidad_Responsable FOREIGN KEY (IdResponsable) REFERENCES instituto_Usuario (IdUsuario);

ALTER TABLE instituto_Departamento
    ADD CONSTRAINT FK_Departamento_Unidad FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_UnidadDeNegocio (IdUnidadDeNegocio) ON DELETE CASCADE;

ALTER TABLE instituto_Departamento
    ADD CONSTRAINT FK_Departamento_Responsable FOREIGN KEY (IdResponsable) REFERENCES instituto_Usuario (IdUsuario);

-- Capacitación
ALTER TABLE instituto_Modulo
    ADD CONSTRAINT FK_Modulo_Creador FOREIGN KEY (IdCreador) REFERENCES instituto_Usuario (IdUsuario) ON DELETE SET NULL;

ALTER TABLE instituto_ModuloDepartamento
    ADD CONSTRAINT FK_ModDepto_Modulo FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo (IdModulo) ON DELETE CASCADE;

ALTER TABLE instituto_ModuloDepartamento
    ADD CONSTRAINT FK_ModDepto_Departamento FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento (IdDepartamento) ON DELETE CASCADE;

ALTER TABLE instituto_ModuloDepartamento
    ADD CONSTRAINT UQ_ModuloDepartamento UNIQUE (IdModulo, IdDepartamento);

-- Progreso
ALTER TABLE instituto_ProgresoModulo
    ADD CONSTRAINT FK_ProgresoMod_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario) ON DELETE CASCADE;

ALTER TABLE instituto_ProgresoModulo
    ADD CONSTRAINT FK_ProgresoMod_Modulo FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo (IdModulo) ON DELETE CASCADE;

ALTER TABLE instituto_ProgresoModulo
    ADD CONSTRAINT UQ_UsuarioModulo UNIQUE (IdUsuario, IdModulo);

-- Evaluaciones
ALTER TABLE instituto_Evaluacion
    ADD CONSTRAINT FK_Evaluacion_Modulo FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo (IdModulo) ON DELETE CASCADE;

ALTER TABLE instituto_ResultadoEvaluacion
    ADD CONSTRAINT FK_Resultado_Inscripcion FOREIGN KEY (IdInscripcion) REFERENCES instituto_ProgresoModulo (IdInscripcion) ON DELETE CASCADE;

ALTER TABLE instituto_ResultadoEvaluacion
    ADD CONSTRAINT FK_Resultado_Evaluacion FOREIGN KEY (IdEvaluacion) REFERENCES instituto_Evaluacion (IdEvaluacion) ON DELETE CASCADE;

-- Soporte
ALTER TABLE instituto_Soporte
    ADD CONSTRAINT FK_Soporte_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario) ON DELETE CASCADE;

ALTER TABLE instituto_Soporte
    ADD CONSTRAINT FK_Soporte_Asignado FOREIGN KEY (IdAsignado) REFERENCES instituto_Usuario (IdUsuario);

ALTER TABLE instituto_SoporteSeguimiento
    ADD CONSTRAINT FK_Seguimiento_Soporte FOREIGN KEY (IdSoporte) REFERENCES instituto_Soporte (IdSoporte) ON DELETE CASCADE;

ALTER TABLE instituto_SoporteSeguimiento
    ADD CONSTRAINT FK_Seguimiento_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario);

-- Reportes
ALTER TABLE instituto_ReporteGuardado
    ADD CONSTRAINT FK_Reporte_Creador FOREIGN KEY (IdUsuarioCreador) REFERENCES instituto_Usuario (IdUsuario) ON DELETE CASCADE;

ALTER TABLE instituto_ReporteCompartido
    ADD CONSTRAINT FK_ReporteComp_Reporte FOREIGN KEY (IdReporte) REFERENCES instituto_ReporteGuardado (IdReporte) ON DELETE CASCADE;

ALTER TABLE instituto_ReporteCompartido
    ADD CONSTRAINT FK_ReporteComp_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario);

ALTER TABLE instituto_ReporteCompartido
    ADD CONSTRAINT UQ_ReporteUsuario UNIQUE (IdReporte, IdUsuario);

-- Auditoría
ALTER TABLE instituto_AuditoriaAcceso
    ADD CONSTRAINT FK_AuditoriaAcc_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario) ON DELETE SET NULL;

ALTER TABLE instituto_AuditoriaCambios
    ADD CONSTRAINT FK_AuditoriaCam_Usuario FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario (IdUsuario);

-- Configuración
ALTER TABLE instituto_Configuracion
    ADD CONSTRAINT FK_Config_UsuarioMod FOREIGN KEY (IdUsuarioMod) REFERENCES instituto_Usuario (IdUsuario) ON DELETE SET NULL;

GO

-- ==========================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ==========================================

PRINT 'Creando índices adicionales...';

-- Usuario
CREATE INDEX IX_Usuario_UserEmail_Activo ON instituto_Usuario(UserEmail, Activo);
CREATE INDEX IX_Usuario_Activo ON instituto_Usuario(Activo);

-- Progreso
CREATE INDEX IX_ProgresoModulo_Usuario_Estatus_Modulo ON instituto_ProgresoModulo(IdUsuario, EstatusModulo, IdModulo);
CREATE INDEX IX_ProgresoModulo_Estatus ON instituto_ProgresoModulo(EstatusModulo);

-- Evaluaciones
CREATE INDEX IX_Evaluacion_Modulo_Activo ON instituto_Evaluacion(IdModulo, Activo);
CREATE INDEX IX_ResultadoEvaluacion_FechaRealizacion ON instituto_ResultadoEvaluacion(FechaRealizacion DESC);
CREATE INDEX IX_ResultadoEvaluacion_Inscripcion ON instituto_ResultadoEvaluacion(IdInscripcion);

-- Auditoría
CREATE INDEX IX_AuditoriaAcceso_FechaAccion_Usuario ON instituto_AuditoriaAcceso(FechaAccion DESC, IdUsuario);

GO

-- ==========================================
-- DATOS INICIALES
-- ==========================================

PRINT 'Insertando datos iniciales...';

-- Roles
SET IDENTITY_INSERT instituto_Rol ON;
INSERT INTO instituto_Rol (IdRol, NombreRol, Descripcion, Activo) VALUES
(1, 'Administrador', 'Acceso completo al sistema', 1),
(2, 'Instructor', 'Puede crear y gestionar módulos', 1),
(3, 'Empleado', 'Usuario estándar del sistema', 1),
(4, 'RRHH', 'Gestión de personal y reportes', 1);
SET IDENTITY_INSERT instituto_Rol OFF;

-- Unidades de Negocio
SET IDENTITY_INSERT instituto_UnidadDeNegocio ON;
INSERT INTO instituto_UnidadDeNegocio (IdUnidadDeNegocio, NombreUnidad, Codigo, Descripcion, Activo) VALUES
(1, 'ICAVE', 'ICAVE', 'Infraestructura y Concesiones de Alta Velocidad del Este', 1),
(2, 'EIT', 'EIT', 'Empresa de Infraestructura y Transporte', 1),
(3, 'LCT', 'LCT', 'Lázaro Cárdenas Terminal', 1),
(4, 'TIMSA', 'TIMSA', 'Terminal de Importación y Maniobras SA', 1),
(5, 'HPMX', 'HPMX', 'Hutchison Ports México', 1),
(6, 'TNG', 'TNG', 'TNG Container Terminal', 1);
SET IDENTITY_INSERT instituto_UnidadDeNegocio OFF;

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

GO

-- Habilitar restricciones de FK
EXEC sp_msforeachtable "ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL";
GO

PRINT '======================================================================';
PRINT 'ESQUEMA CREADO EXITOSAMENTE';
PRINT '======================================================================';
PRINT 'Total de tablas: 20';
PRINT 'Total de índices: 8';
PRINT 'Total de foreign keys: 30';
PRINT '======================================================================';
GO
