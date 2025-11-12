-- ═══════════════════════════════════════════════════════════════════════════════
-- ESQUEMA DE BASE DE DATOS CORREGIDO - INSTITUTO HUTCHISON PORTS
-- Versión: 2.0 (Con prefijo instituto_ y FKs corregidas)
-- ═══════════════════════════════════════════════════════════════════════════════

-- -----------------------------------------------------------------------------
-- TABLA: instituto_rol
-- Roles de usuarios en el sistema
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_rol (
    IdRol INT PRIMARY KEY AUTO_INCREMENT,
    NombreRol VARCHAR(150) NOT NULL,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Roles de usuarios del sistema';

-- Insertar roles por defecto
INSERT INTO instituto_rol (NombreRol, Descripcion) VALUES
('Administrador', 'Acceso completo al sistema'),
('Instructor', 'Puede crear y gestionar módulos'),
('Empleado', 'Usuario estándar del sistema'),
('RRHH', 'Gestión de personal y reportes');


-- -----------------------------------------------------------------------------
-- TABLA: instituto_unidaddenegocio
-- Unidades de negocio del grupo Hutchison
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_unidaddenegocio (
    IdUnidadDeNegocio INT PRIMARY KEY AUTO_INCREMENT,
    NombreUnidad VARCHAR(100) NOT NULL,
    Codigo VARCHAR(50) UNIQUE,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_codigo (Codigo),
    INDEX idx_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Unidades de negocio Hutchison Ports';

-- Insertar unidades de negocio conocidas
INSERT INTO instituto_unidaddenegocio (NombreUnidad, Codigo, Descripcion) VALUES
('ICAVE', 'ICAVE', 'Infraestructura y Concesiones de Alta Velocidad del Este'),
('EIT', 'EIT', 'Empresa de Infraestructura y Transporte'),
('LCT', 'LCT', 'Lázaro Cárdenas Terminal'),
('TIMSA', 'TIMSA', 'Terminal de Importación y Maniobras SA'),
('HPMX', 'HPMX', 'Hutchison Ports México'),
('TNG', 'TNG', 'TNG Container Terminal'),
('CCI', 'CCI', 'Container Corporation International'),
('TILH', 'TILH', 'Terminal de Importación Lázaro Hermanos'),
('ECV', 'ECV', 'Empresa de Contenedores del Valle'),
('HPLM', 'HPLM', 'Hutchison Ports Lázaro México'),
('LCMT', 'LCMT', 'Lázaro Cárdenas Multimodal Terminal');


-- -----------------------------------------------------------------------------
-- TABLA: instituto_departamento
-- Departamentos dentro de las unidades de negocio
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_departamento (
    IdDepartamento INT PRIMARY KEY AUTO_INCREMENT,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(255) NOT NULL,
    Codigo VARCHAR(100),
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_unidaddenegocio(IdUnidadDeNegocio)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_unidad (IdUnidadDeNegocio),
    INDEX idx_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Departamentos por unidad de negocio';

-- Insertar departamentos comunes
INSERT INTO instituto_departamento (IdUnidadDeNegocio, NombreDepartamento, Codigo) VALUES
(1, 'Recursos Humanos', 'RRHH'),
(1, 'Operaciones', 'OPS'),
(1, 'Tecnología de la Información', 'TI'),
(1, 'Finanzas', 'FIN'),
(1, 'Seguridad', 'SEC');


-- -----------------------------------------------------------------------------
-- TABLA: instituto_modulo
-- Módulos de capacitación
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_modulo (
    IdModulo INT PRIMARY KEY AUTO_INCREMENT,
    NombreModulo VARCHAR(255) NOT NULL UNIQUE,
    FechaInicioModulo DATETIME,
    FechaCierre DATETIME,
    Descripcion TEXT,
    DuracionEstimadaHoras INT DEFAULT 2,
    CategoriaModulo VARCHAR(150) DEFAULT 'General',
    IdCreador INT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_activo (Activo),
    INDEX idx_categoria (CategoriaModulo),
    INDEX idx_creador (IdCreador)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Módulos de capacitación del instituto';

-- Insertar los 12 módulos estándar
INSERT INTO instituto_modulo (NombreModulo, CategoriaModulo, DuracionEstimadaHoras, Descripcion) VALUES
('Módulo 1 - Código de Ética', 'Ética y Compliance', 2, 'Fundamentos del código de ética corporativo'),
('Módulo 2 - Anti-corrupción', 'Ética y Compliance', 2, 'Prácticas anti-corrupción y transparencia'),
('Módulo 3 - Conflicto de Interés', 'Ética y Compliance', 2, 'Identificación y manejo de conflictos de interés'),
('Módulo 4 - Relaciones Laborales', 'Recursos Humanos', 3, 'Normativa laboral y relaciones interpersonales'),
('Módulo 5 - Seguridad Industrial', 'Seguridad', 4, 'Protocolos de seguridad en operaciones industriales'),
('Módulo 6 - Ciberseguridad', 'Tecnología', 3, 'Protección de datos y seguridad informática'),
('Módulo 7 - Salud Ocupacional', 'Seguridad', 3, 'Prevención de riesgos y salud en el trabajo'),
('Módulo 8 - Procesos de RRHH', 'Recursos Humanos', 4, 'Procesos de recursos humanos y gestión de personal'),
('Módulo 9 - Prevención de Riesgos', 'Seguridad', 3, 'Identificación y mitigación de riesgos'),
('Módulo 10 - Gestión Ambiental', 'Medio Ambiente', 2, 'Responsabilidad ambiental corporativa'),
('Módulo 11 - Protección de Datos', 'Tecnología', 2, 'GDPR y protección de datos personales'),
('Módulo 12 - Liderazgo', 'Desarrollo Profesional', 5, 'Habilidades de liderazgo y gestión de equipos');


-- -----------------------------------------------------------------------------
-- TABLA: instituto_usuario
-- Usuarios del sistema (empleados)
-- CORRECCIÓN: UserId → IdUsuario en FK
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_usuario (
    IdUsuario INT PRIMARY KEY AUTO_INCREMENT,
    UserID VARCHAR(100) UNIQUE NOT NULL COMMENT 'Número de empleado/nómina',
    IdUnidadDeNegocio INT,
    IdDepartamento INT,
    IdRol INT DEFAULT 3 COMMENT 'Por defecto: Empleado',

    -- Información personal
    NombreCompleto VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) UNIQUE,
    PasswordHash VARCHAR(500) COMMENT 'Hash de contraseña si se usa auth local',

    -- Información organizacional adicional
    TipoDeCorreo VARCHAR(100) DEFAULT 'Corporativo',
    Nivel VARCHAR(100) COMMENT 'Junior, Senior, Manager, etc.',
    Division VARCHAR(255),
    Position VARCHAR(255),
    UserStatus VARCHAR(100) DEFAULT 'Active',
    Grupo VARCHAR(100),
    Ubicacion VARCHAR(255),

    -- Control
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    UltimoAcceso DATETIME,

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_unidaddenegocio(IdUnidadDeNegocio)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (IdDepartamento) REFERENCES instituto_departamento(IdDepartamento)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (IdRol) REFERENCES instituto_rol(IdRol)
        ON DELETE SET NULL ON UPDATE CASCADE,

    INDEX idx_user_id (UserID),
    INDEX idx_email (UserEmail),
    INDEX idx_unidad (IdUnidadDeNegocio),
    INDEX idx_departamento (IdDepartamento),
    INDEX idx_status (UserStatus),
    INDEX idx_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Usuarios del sistema (empleados)';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_auditoriaacceso
-- Auditoría de accesos al sistema
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_auditoriaacceso (
    IdAuditoria INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT,
    Accion VARCHAR(100) NOT NULL COMMENT 'Login, Logout, Export, etc.',
    Modulo VARCHAR(100) COMMENT 'Dashboard, Configuración, etc.',
    Detalle TEXT,
    DireccionIP VARCHAR(45),
    UserAgent VARCHAR(255),
    Exito TINYINT(1) DEFAULT 1,
    FechaAccion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdUsuario) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE SET NULL ON UPDATE CASCADE,

    INDEX idx_usuario (IdUsuario),
    INDEX idx_accion (Accion),
    INDEX idx_fecha (FechaAccion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Auditoría de accesos y acciones del sistema';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_progresomodulo
-- Progreso de usuarios en módulos
-- CORRECCIÓN CRÍTICA: UserId → IdUsuario para coincidir con FK
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_progresomodulo (
    IdInscripcion INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL COMMENT 'CORREGIDO: antes era UserId',
    IdModulo INT NOT NULL,

    -- Estado y progreso
    EstatusModulo VARCHAR(100) DEFAULT 'Registrado' COMMENT 'Registrado, En Progreso, Completado, Vencido',
    PorcentajeAvance DECIMAL(5, 2) DEFAULT 0.00,
    TiempoInvertidoMinutos INT DEFAULT 0,

    -- Fechas importantes
    FechaAsignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaVencimiento DATETIME,
    FechaInicio DATETIME,
    FechaFinalizado DATETIME,

    FOREIGN KEY (IdUsuario) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (IdModulo) REFERENCES instituto_modulo(IdModulo)
        ON DELETE CASCADE ON UPDATE CASCADE,

    UNIQUE KEY unique_usuario_modulo (IdUsuario, IdModulo),
    INDEX idx_usuario (IdUsuario),
    INDEX idx_modulo (IdModulo),
    INDEX idx_estatus (EstatusModulo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Progreso de usuarios en módulos de capacitación';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_certificado
-- Certificados emitidos
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_certificado (
    IdCertificado INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    CodigoCertificado VARCHAR(255) UNIQUE NOT NULL,
    FechaEmision DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaVencimiento DATETIME COMMENT 'NULL si no vence',
    UrlPDF VARCHAR(500),
    HashVerificacion VARCHAR(255) COMMENT 'Hash para validación de autenticidad',
    Valido TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_progresomodulo(IdInscripcion)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_codigo (CodigoCertificado),
    INDEX idx_inscripcion (IdInscripcion),
    INDEX idx_fecha_emision (FechaEmision)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Certificados emitidos por módulos completados';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_evaluacion
-- Evaluaciones asociadas a módulos
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_evaluacion (
    IdEvaluacion INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    PuntajeMinimoAprobatorio DECIMAL(10, 2) DEFAULT 70.00,
    PuntajeMaximo DECIMAL(10, 2) DEFAULT 100.00,
    IntentosPermitidos INT DEFAULT 3,
    TiempoLimiteMinutos INT DEFAULT 60,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdModulo) REFERENCES instituto_modulo(IdModulo)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_modulo (IdModulo),
    INDEX idx_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Evaluaciones de módulos';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_historialprogreso
-- Historial de cambios en progreso de módulos
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_historialprogreso (
    IdHistorial INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    EstatusAnterior VARCHAR(100),
    EstatusNuevo VARCHAR(100),
    PorcentajeAnterior DECIMAL(5, 2),
    PorcentajeNuevo DECIMAL(5, 2),
    FechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    Comentario TEXT,
    IdUsuarioModificador INT COMMENT 'Quien realizó el cambio',

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_progresomodulo(IdInscripcion)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (IdUsuarioModificador) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE SET NULL ON UPDATE CASCADE,

    INDEX idx_inscripcion (IdInscripcion),
    INDEX idx_fecha (FechaCambio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Historial de cambios en progreso de módulos';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_modulodepartamento
-- Asignación de módulos obligatorios por departamento
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_modulodepartamento (
    IdModuloDepto INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio TINYINT(1) DEFAULT 0,
    FechaAsignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaVencimiento DATETIME,
    Activo TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdModulo) REFERENCES instituto_modulo(IdModulo)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (IdDepartamento) REFERENCES instituto_departamento(IdDepartamento)
        ON DELETE CASCADE ON UPDATE CASCADE,

    UNIQUE KEY unique_modulo_depto (IdModulo, IdDepartamento),
    INDEX idx_modulo (IdModulo),
    INDEX idx_departamento (IdDepartamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Módulos asignados a departamentos';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_notificacion
-- Sistema de notificaciones
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_notificacion (
    IdNotificacion INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL,
    TipoNotificacion VARCHAR(100) NOT NULL COMMENT 'Asignación, Recordatorio, Vencimiento, etc.',
    Titulo VARCHAR(255) NOT NULL,
    Mensaje TEXT,
    Prioridad VARCHAR(50) DEFAULT 'Normal' COMMENT 'Alta, Normal, Baja',
    Leida TINYINT(1) DEFAULT 0,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaLectura DATETIME,
    UrlDestino VARCHAR(500) COMMENT 'URL para redirección al hacer clic',

    FOREIGN KEY (IdUsuario) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_usuario_leida (IdUsuario, Leida),
    INDEX idx_fecha (FechaCreacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Notificaciones del sistema';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_recursomodulo
-- Recursos educativos asociados a módulos
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_recursomodulo (
    IdRecurso INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    NombreRecurso VARCHAR(255) NOT NULL,
    TipoRecurso VARCHAR(100) COMMENT 'PDF, Video, Link, Documento, etc.',
    UrlRecurso VARCHAR(500),
    Descripcion TEXT,
    TamanoBytes BIGINT,
    Orden INT DEFAULT 0,
    Obligatorio TINYINT(1) DEFAULT 0,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Activo TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdModulo) REFERENCES instituto_modulo(IdModulo)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_modulo (IdModulo),
    INDEX idx_tipo (TipoRecurso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Recursos educativos de módulos';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_reporteguardado
-- Reportes guardados por usuarios
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_reporteguardado (
    IdReporte INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuarioCreador INT NOT NULL,
    NombreReporte VARCHAR(255) NOT NULL,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    TipoReporte VARCHAR(100) COMMENT 'General, Por Departamento, Por Usuario, etc.',
    Descripcion TEXT,
    FiltrosJSON JSON COMMENT 'Filtros aplicados al reporte en formato JSON',
    Compartido TINYINT(1) DEFAULT 0,
    Favorito TINYINT(1) DEFAULT 0,

    FOREIGN KEY (IdUsuarioCreador) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_usuario (IdUsuarioCreador),
    INDEX idx_tipo (TipoReporte)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Reportes guardados del sistema';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_resultadoevaluacion
-- Resultados de evaluaciones realizadas
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_resultadoevaluacion (
    IdResultado INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(10, 2) NOT NULL,
    Aprobado TINYINT(1) GENERATED ALWAYS AS (
        PuntajeObtenido >= (
            SELECT PuntajeMinimoAprobatorio
            FROM instituto_evaluacion
            WHERE IdEvaluacion = instituto_resultadoevaluacion.IdEvaluacion
        )
    ) STORED,
    IntentoNumero INT DEFAULT 1,
    FechaRealizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    TiempoInvertidoMinutos INT,

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_progresomodulo(IdInscripcion)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (IdEvaluacion) REFERENCES instituto_evaluacion(IdEvaluacion)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_inscripcion (IdInscripcion),
    INDEX idx_evaluacion (IdEvaluacion),
    INDEX idx_aprobado (Aprobado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Resultados de evaluaciones';


-- -----------------------------------------------------------------------------
-- TABLA: instituto_soporte
-- Tickets de soporte
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS instituto_soporte (
    IdSoporte INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL,
    FechaSolicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
    Asunto VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Categoria VARCHAR(150) DEFAULT 'General',
    Prioridad VARCHAR(100) DEFAULT 'Normal',
    Estatus VARCHAR(100) DEFAULT 'Pendiente',
    IdUsuarioAsignado INT COMMENT 'Agente de soporte asignado',
    FechaRespuesta DATETIME,
    FechaCierre DATETIME,
    Respuesta TEXT,

    FOREIGN KEY (IdUsuario) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (IdUsuarioAsignado) REFERENCES instituto_usuario(IdUsuario)
        ON DELETE SET NULL ON UPDATE CASCADE,

    INDEX idx_usuario (IdUsuario),
    INDEX idx_estatus (Estatus),
    INDEX idx_prioridad (Prioridad),
    INDEX idx_fecha (FechaSolicitud)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tickets de soporte técnico';


-- ═══════════════════════════════════════════════════════════════════════════
-- VISTAS ÚTILES PARA REPORTES Y DASHBOARDS
-- ═══════════════════════════════════════════════════════════════════════════

-- Vista: Progreso completo por usuario
CREATE OR REPLACE VIEW vista_progreso_completo_usuario AS
SELECT
    u.IdUsuario,
    u.UserID,
    u.NombreCompleto,
    u.UserEmail,
    un.NombreUnidad as UnidadNegocio,
    d.NombreDepartamento as Departamento,
    u.Position,

    COUNT(pm.IdModulo) as ModulosAsignados,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados,
    SUM(CASE WHEN pm.EstatusModulo = 'En Progreso' THEN 1 ELSE 0 END) as ModulosEnProgreso,
    SUM(CASE WHEN pm.EstatusModulo = 'Registrado' THEN 1 ELSE 0 END) as ModulosRegistrados,

    ROUND(
        (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
        NULLIF(COUNT(pm.IdModulo), 0),
        2
    ) as PorcentajeCompletado

FROM instituto_usuario u
LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
WHERE u.Activo = 1
GROUP BY u.IdUsuario;


-- Vista: Top usuarios por progreso
CREATE OR REPLACE VIEW vista_top_usuarios_progreso AS
SELECT
    u.UserID,
    u.NombreCompleto,
    un.NombreUnidad,
    COUNT(pm.IdModulo) as TotalModulos,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as Completados,
    ROUND(
        (SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) * 100.0) /
        NULLIF(COUNT(pm.IdModulo), 0),
        1
    ) as PorcentajeCompletado
FROM instituto_usuario u
JOIN instituto_progresomodulo pm ON u.IdUsuario = pm.IdUsuario
LEFT JOIN instituto_unidaddenegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
WHERE u.Activo = 1
GROUP BY u.IdUsuario
HAVING TotalModulos > 0
ORDER BY PorcentajeCompletado DESC, Completados DESC;
