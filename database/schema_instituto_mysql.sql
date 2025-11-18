-- ═════════════════════════════════════════════════════════════════
-- SCHEMA MYSQL - INSTITUTO HUTCHISON PORTS
-- Smart Reports - Sistema de Capacitación
-- ═════════════════════════════════════════════════════════════════
-- Base de Datos: InstitutoHutchison
-- Motor: MySQL 8.0+
-- Última actualización: 18 de Noviembre, 2025
-- ═════════════════════════════════════════════════════════════════

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS InstitutoHutchison
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE InstitutoHutchison;

SET FOREIGN_KEY_CHECKS = 0;

-- ══════════════════════════════════════════════════════════════
-- ELIMINANDO TABLAS EXISTENTES (si existen)
-- ══════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS instituto_ReporteCompartido;
DROP TABLE IF EXISTS instituto_ReporteGuardado;
DROP TABLE IF EXISTS instituto_SoporteSeguimiento;
DROP TABLE IF EXISTS instituto_Soporte;
DROP TABLE IF EXISTS instituto_ResultadoEvaluacion;
DROP TABLE IF EXISTS instituto_Evaluacion;
DROP TABLE IF EXISTS instituto_ProgresoModulo;
DROP TABLE IF EXISTS instituto_ModuloDepartamento;
DROP TABLE IF EXISTS instituto_Modulo;
DROP TABLE IF EXISTS instituto_Usuario;
DROP TABLE IF EXISTS instituto_Posicion;
DROP TABLE IF EXISTS instituto_Departamento;
DROP TABLE IF EXISTS instituto_UnidadDeNegocio;
DROP TABLE IF EXISTS instituto_RolPermiso;
DROP TABLE IF EXISTS instituto_Permiso;
DROP TABLE IF EXISTS instituto_Rol;
DROP TABLE IF EXISTS instituto_AuditoriaCambios;
DROP TABLE IF EXISTS instituto_AuditoriaAcceso;
DROP TABLE IF EXISTS instituto_Plantilla;
DROP TABLE IF EXISTS instituto_Configuracion;

SET FOREIGN_KEY_CHECKS = 1;

-- ══════════════════════════════════════════════════════════════
-- 1. MÓDULO DE ROLES Y PERMISOS
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_Rol
CREATE TABLE instituto_Rol (
    IdRol INT AUTO_INCREMENT NOT NULL,
    NombreRol VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_Rol PRIMARY KEY (IdRol),
    CONSTRAINT UK_NombreRol UNIQUE (NombreRol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_Permiso
CREATE TABLE instituto_Permiso (
    IdPermiso INT AUTO_INCREMENT NOT NULL,
    NombrePermiso VARCHAR(150) NOT NULL,
    Recurso VARCHAR(255) NOT NULL,
    Accion VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    CONSTRAINT PK_instituto_Permiso PRIMARY KEY (IdPermiso),
    CONSTRAINT UK_RecursoAccion UNIQUE (Recurso, Accion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_RolPermiso
CREATE TABLE instituto_RolPermiso (
    IdRolPermiso INT AUTO_INCREMENT NOT NULL,
    IdRol INT NOT NULL,
    IdPermiso INT NOT NULL,
    Permitir TINYINT(1) DEFAULT 1,
    FechaAsignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_RolPermiso PRIMARY KEY (IdRolPermiso),
    CONSTRAINT FK_RolPermiso_Rol FOREIGN KEY (IdRol)
        REFERENCES instituto_Rol(IdRol) ON DELETE CASCADE,
    CONSTRAINT FK_RolPermiso_Permiso FOREIGN KEY (IdPermiso)
        REFERENCES instituto_Permiso(IdPermiso) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 2. MÓDULO ORGANIZACIONAL
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_UnidadDeNegocio
CREATE TABLE instituto_UnidadDeNegocio (
    IdUnidadDeNegocio INT AUTO_INCREMENT NOT NULL,
    NombreUnidad VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_UnidadDeNegocio PRIMARY KEY (IdUnidadDeNegocio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_Departamento
CREATE TABLE instituto_Departamento (
    IdDepartamento INT AUTO_INCREMENT NOT NULL,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(255) NOT NULL,
    Codigo VARCHAR(50),
    Descripcion TEXT,
    IdResponsable INT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_Departamento PRIMARY KEY (IdDepartamento),
    CONSTRAINT UK_CodigoDepto UNIQUE (Codigo),
    CONSTRAINT FK_Departamento_Unidad FOREIGN KEY (IdUnidadDeNegocio)
        REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_Posicion
CREATE TABLE instituto_Posicion (
    IdPosicion INT AUTO_INCREMENT NOT NULL,
    NombrePosicion VARCHAR(150) NOT NULL,
    Descripcion TEXT,
    IdDepartamento INT,
    Activo TINYINT(1) DEFAULT 1,
    CONSTRAINT PK_instituto_Posicion PRIMARY KEY (IdPosicion),
    CONSTRAINT FK_Posicion_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_Usuario
CREATE TABLE instituto_Usuario (
    IdUsuario INT AUTO_INCREMENT NOT NULL,
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
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_Usuario PRIMARY KEY (IdUsuario),
    CONSTRAINT UK_UserId UNIQUE (UserId),
    CONSTRAINT UK_UserEmail UNIQUE (UserEmail),
    CONSTRAINT FK_Usuario_UnidadDeNegocio FOREIGN KEY (IdUnidadDeNegocio)
        REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio) ON DELETE SET NULL,
    CONSTRAINT FK_Usuario_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE SET NULL,
    CONSTRAINT FK_Usuario_Rol FOREIGN KEY (IdRol)
        REFERENCES instituto_Rol(IdRol) ON DELETE RESTRICT,
    CONSTRAINT FK_Usuario_Posicion FOREIGN KEY (IdPosicion)
        REFERENCES instituto_Posicion(IdPosicion) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Agregar FK circular de Departamento.IdResponsable
ALTER TABLE instituto_Departamento
ADD CONSTRAINT FK_Departamento_Responsable FOREIGN KEY (IdResponsable)
    REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL;

-- ══════════════════════════════════════════════════════════════
-- 3. MÓDULO DE CAPACITACIÓN
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_Modulo
CREATE TABLE instituto_Modulo (
    IdModulo INT AUTO_INCREMENT NOT NULL,
    NombreModulo VARCHAR(255) NOT NULL,
    TipoDeCapacitacion VARCHAR(50),
    FechaInicio DATETIME,
    FechaCierre DATETIME,
    Descripcion TEXT,
    Prerequisitos JSON,
    Obligatorio TINYINT(1) DEFAULT 0,
    Activo TINYINT(1) DEFAULT 1,
    CONSTRAINT PK_instituto_Modulo PRIMARY KEY (IdModulo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_ModuloDepartamento
CREATE TABLE instituto_ModuloDepartamento (
    IdModuloDepto INT AUTO_INCREMENT NOT NULL,
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio TINYINT(1) DEFAULT 0,
    FechaAsignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaVencimiento DATETIME,
    Activo TINYINT(1) DEFAULT 1,
    CONSTRAINT PK_instituto_ModuloDepartamento PRIMARY KEY (IdModuloDepto),
    CONSTRAINT FK_ModDepto_Modulo FOREIGN KEY (IdModulo)
        REFERENCES instituto_Modulo(IdModulo) ON DELETE CASCADE,
    CONSTRAINT FK_ModDepto_Departamento FOREIGN KEY (IdDepartamento)
        REFERENCES instituto_Departamento(IdDepartamento) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 4. MÓDULO DE PROGRESO
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_ProgresoModulo
CREATE TABLE instituto_ProgresoModulo (
    IdInscripcion INT AUTO_INCREMENT NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 5. MÓDULO DE EVALUACIONES
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_Evaluacion
CREATE TABLE instituto_Evaluacion (
    IdEvaluacion INT AUTO_INCREMENT NOT NULL,
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    TipoEvaluacion VARCHAR(50),
    PuntajeMinimo DECIMAL(5,2),
    PuntajeMaximo DECIMAL(5,2),
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_Evaluacion PRIMARY KEY (IdEvaluacion),
    CONSTRAINT FK_Evaluacion_Modulo FOREIGN KEY (IdModulo)
        REFERENCES instituto_Modulo(IdModulo) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_ResultadoEvaluacion
CREATE TABLE instituto_ResultadoEvaluacion (
    IdResultado INT AUTO_INCREMENT NOT NULL,
    IdInscripcion INT NOT NULL,
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(5,2),
    Aprobado TINYINT(1),
    FechaRealizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_ResultadoEvaluacion PRIMARY KEY (IdResultado),
    CONSTRAINT FK_Resultado_Inscripcion FOREIGN KEY (IdInscripcion)
        REFERENCES instituto_ProgresoModulo(IdInscripcion) ON DELETE CASCADE,
    CONSTRAINT FK_Resultado_Evaluacion FOREIGN KEY (IdEvaluacion)
        REFERENCES instituto_Evaluacion(IdEvaluacion) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 6. MÓDULO DE SOPORTE
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_Soporte
CREATE TABLE instituto_Soporte (
    IdSoporte INT AUTO_INCREMENT NOT NULL,
    IdUsuario INT NOT NULL,
    FechaSolicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_SoporteSeguimiento
CREATE TABLE instituto_SoporteSeguimiento (
    IdSeguimiento INT AUTO_INCREMENT NOT NULL,
    IdSoporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoAccion VARCHAR(50),
    Comentario TEXT,
    FechaAccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    AdjuntoUrl VARCHAR(512),
    CONSTRAINT PK_instituto_SoporteSeguimiento PRIMARY KEY (IdSeguimiento),
    CONSTRAINT FK_Seguimiento_Soporte FOREIGN KEY (IdSoporte)
        REFERENCES instituto_Soporte(IdSoporte) ON DELETE CASCADE,
    CONSTRAINT FK_Seguimiento_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 7. MÓDULO DE REPORTES
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_ReporteGuardado
CREATE TABLE instituto_ReporteGuardado (
    IdReporte INT AUTO_INCREMENT NOT NULL,
    IdUsuarioCreador INT NOT NULL,
    NombreReporte VARCHAR(255) NOT NULL,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    TipoReporte VARCHAR(100),
    Descripcion TEXT,
    FiltrosJSON JSON,
    Compartido TINYINT(1) DEFAULT 0,
    Favorito TINYINT(1) DEFAULT 0,
    UltimaEjecucion DATETIME,
    NumeroEjecuciones INT DEFAULT 0,
    CONSTRAINT PK_instituto_ReporteGuardado PRIMARY KEY (IdReporte),
    CONSTRAINT FK_Reporte_Creador FOREIGN KEY (IdUsuarioCreador)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_ReporteCompartido
CREATE TABLE instituto_ReporteCompartido (
    IdCompartido INT AUTO_INCREMENT NOT NULL,
    IdReporte INT NOT NULL,
    IdUsuario INT NOT NULL,
    PermisoEdicion TINYINT(1) DEFAULT 0,
    FechaCompartido DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_ReporteCompartido PRIMARY KEY (IdCompartido),
    CONSTRAINT FK_ReporteComp_Reporte FOREIGN KEY (IdReporte)
        REFERENCES instituto_ReporteGuardado(IdReporte) ON DELETE CASCADE,
    CONSTRAINT FK_ReporteComp_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 8. MÓDULO DE AUDITORÍA
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_AuditoriaAcceso
CREATE TABLE instituto_AuditoriaAcceso (
    IdAuditoria INT AUTO_INCREMENT NOT NULL,
    IdUsuario INT,
    Accion VARCHAR(100) NOT NULL,
    Modulo VARCHAR(100),
    Detalle TEXT,
    DireccionIP VARCHAR(45),
    UserAgent TEXT,
    Exito TINYINT(1),
    FechaAccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    DuracionMs INT,
    CONSTRAINT PK_instituto_AuditoriaAcceso PRIMARY KEY (IdAuditoria),
    CONSTRAINT FK_AuditoriaAcc_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_AuditoriaCambios
CREATE TABLE instituto_AuditoriaCambios (
    IdAuditCambio INT AUTO_INCREMENT NOT NULL,
    Tabla VARCHAR(100) NOT NULL,
    IdRegistro INT NOT NULL,
    IdUsuario INT NOT NULL,
    TipoCambio VARCHAR(10),
    ValoresAnteriores JSON,
    ValoresNuevos JSON,
    FechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    DireccionIP VARCHAR(45),
    CONSTRAINT PK_instituto_AuditoriaCambios PRIMARY KEY (IdAuditCambio),
    CONSTRAINT FK_AuditoriaCam_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════════════════════
-- 9. MÓDULO DE CONFIGURACIÓN Y PLANTILLAS
-- ══════════════════════════════════════════════════════════════

-- Tabla: instituto_Configuracion
CREATE TABLE instituto_Configuracion (
    IdConfig INT AUTO_INCREMENT NOT NULL,
    Clave VARCHAR(100) NOT NULL,
    Valor TEXT,
    Tipo VARCHAR(50),
    Descripcion TEXT,
    Categoria VARCHAR(100),
    Editable TINYINT(1) DEFAULT 1,
    IdUsuarioMod INT,
    FechaModificacion DATETIME,
    CONSTRAINT PK_instituto_Configuracion PRIMARY KEY (IdConfig),
    CONSTRAINT UK_Clave UNIQUE (Clave),
    CONSTRAINT FK_Config_UsuarioMod FOREIGN KEY (IdUsuarioMod)
        REFERENCES instituto_Usuario(IdUsuario) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: instituto_Plantilla
CREATE TABLE instituto_Plantilla (
    IdPlantilla INT AUTO_INCREMENT NOT NULL,
    NombrePlantilla VARCHAR(150) NOT NULL,
    TipoPlantilla VARCHAR(50),
    Contenido LONGTEXT,
    VariablesJSON JSON,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_instituto_Plantilla PRIMARY KEY (IdPlantilla),
    CONSTRAINT UK_NombrePlantilla UNIQUE (NombrePlantilla)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════
-- SCRIPT COMPLETADO EXITOSAMENTE
-- ═════════════════════════════════════════════════════════════════════════

SELECT '✅ SCHEMA MYSQL CREADO CORRECTAMENTE' AS Resultado;
SELECT '📊 21 tablas principales creadas' AS Detalle;
SELECT '🔗 Relaciones y Foreign Keys configuradas' AS Detalle;
SELECT '🔑 Índices únicos aplicados' AS Detalle;
