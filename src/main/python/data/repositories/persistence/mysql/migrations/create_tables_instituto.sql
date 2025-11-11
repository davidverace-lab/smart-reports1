-- ============================================
-- SMART REPORTS - BASE DE DATOS tngcore
-- Sistema de Gestión de Capacitación - Instituto Hutchison Ports
-- Prefijo de tablas: instituto_
-- Version: 2.0
-- ============================================

USE tngcore;

-- ============================================
-- TABLAS MAESTRAS
-- ============================================

-- Tabla: instituto_Rol
CREATE TABLE IF NOT EXISTS instituto_Rol (
    IdRol INT PRIMARY KEY AUTO_INCREMENT,
    NombreRol VARCHAR(50) UNIQUE NOT NULL,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_rol_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Roles de usuario del sistema';

-- Tabla: instituto_UnidadDeNegocio
CREATE TABLE IF NOT EXISTS instituto_UnidadDeNegocio (
    IdUnidadDeNegocio INT PRIMARY KEY AUTO_INCREMENT,
    NombreUnidad VARCHAR(100) UNIQUE NOT NULL,
    Codigo VARCHAR(20) UNIQUE,
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_unidad_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Unidades de negocio (ICAVE, EIT, LCT, TIMSA, HPMX, TNG)';

-- Tabla: instituto_Departamento
CREATE TABLE IF NOT EXISTS instituto_Departamento (
    IdDepartamento INT PRIMARY KEY AUTO_INCREMENT,
    IdUnidadDeNegocio INT NOT NULL,
    NombreDepartamento VARCHAR(150) NOT NULL,
    Codigo VARCHAR(20),
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    INDEX idx_depto_unidad (IdUnidadDeNegocio),
    INDEX idx_depto_activo (Activo),
    UNIQUE KEY uq_depto_unidad (IdUnidadDeNegocio, NombreDepartamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Departamentos dentro de cada unidad de negocio';

-- ============================================
-- TABLA DE USUARIOS
-- ============================================

CREATE TABLE IF NOT EXISTS instituto_Usuario (
    IdUsuario INT PRIMARY KEY AUTO_INCREMENT,
    UserId VARCHAR(50) UNIQUE NOT NULL,
    IdUnidadDeNegocio INT,
    IdDepartamento INT,
    IdRol INT,
    NombreCompleto VARCHAR(255),
    UserEmail VARCHAR(255),
    PasswordHash VARCHAR(255),
    TipoDeCorreo VARCHAR(50),
    Nivel VARCHAR(50),
    Division VARCHAR(100),
    Position VARCHAR(100),
    UserStatus VARCHAR(50) DEFAULT 'Activo',
    Grupo VARCHAR(100),
    Ubicacion VARCHAR(100),
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    UltimoAcceso DATETIME,

    FOREIGN KEY (IdUnidadDeNegocio) REFERENCES instituto_UnidadDeNegocio(IdUnidadDeNegocio)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento(IdDepartamento)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (IdRol) REFERENCES instituto_Rol(IdRol)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_usuario_email (UserEmail),
    INDEX idx_usuario_status (UserStatus),
    INDEX idx_usuario_nivel (Nivel),
    INDEX idx_usuario_unidad (IdUnidadDeNegocio),
    INDEX idx_usuario_depto (IdDepartamento),
    INDEX idx_usuario_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Usuarios del sistema con información completa';

-- ============================================
-- MÓDULOS Y CAPACITACIÓN
-- ============================================

-- Tabla: instituto_Modulo
CREATE TABLE IF NOT EXISTS instituto_Modulo (
    IdModulo INT PRIMARY KEY AUTO_INCREMENT,
    NombreModulo VARCHAR(255) UNIQUE NOT NULL,
    FechaInicioModulo DATE,
    FechaCierre DATE,
    Descripcion TEXT,
    DuracionEstimadaHoras INT,
    CategoriaModulo VARCHAR(100),
    IdCreador INT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdCreador) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT chk_fechas_modulo
        CHECK (FechaCierre IS NULL OR FechaCierre >= FechaInicioModulo),

    INDEX idx_modulo_activo (Activo),
    INDEX idx_modulo_categoria (CategoriaModulo),
    INDEX idx_modulo_fechas (FechaInicioModulo, FechaCierre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Módulos de capacitación disponibles';

-- Tabla: instituto_ModuloDepartamento
CREATE TABLE IF NOT EXISTS instituto_ModuloDepartamento (
    IdModuloDepto INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    IdDepartamento INT NOT NULL,
    Obligatorio TINYINT(1) DEFAULT 0,
    FechaAsignacion DATE,
    FechaVencimiento DATE,
    Activo TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo(IdModulo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento(IdDepartamento)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    UNIQUE KEY uq_modulo_depto (IdModulo, IdDepartamento),
    INDEX idx_modulo_depto_obligatorio (Obligatorio),
    INDEX idx_modulo_depto_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Asignación de módulos a departamentos';

-- ============================================
-- PROGRESO Y EVALUACIONES
-- ============================================

-- Tabla: instituto_ProgresoModulo
CREATE TABLE IF NOT EXISTS instituto_ProgresoModulo (
    IdInscripcion INT PRIMARY KEY AUTO_INCREMENT,
    UserId VARCHAR(50) NOT NULL,
    IdModulo INT NOT NULL,
    EstatusModulo VARCHAR(50) DEFAULT 'No iniciado',
    PorcentajeAvance DECIMAL(5,2) DEFAULT 0.00,
    TiempoInvertidoMinutos INT DEFAULT 0,
    FechaAsignacion DATETIME,
    FechaVencimiento DATETIME,
    FechaInicio DATETIME,
    FechaFinalizacion DATETIME,

    FOREIGN KEY (UserId) REFERENCES instituto_Usuario(UserId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo(IdModulo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    UNIQUE KEY uq_usuario_modulo (UserId, IdModulo),
    INDEX idx_progreso_estatus (EstatusModulo),
    INDEX idx_progreso_vencimiento (FechaVencimiento),
    INDEX idx_progreso_usuario (UserId),
    INDEX idx_progreso_modulo (IdModulo),

    CONSTRAINT chk_porcentaje_avance
        CHECK (PorcentajeAvance >= 0 AND PorcentajeAvance <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Progreso de usuarios en módulos';

-- Tabla: instituto_Evaluacion
CREATE TABLE IF NOT EXISTS instituto_Evaluacion (
    IdEvaluacion INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    NombreEvaluacion VARCHAR(255),
    Descripcion TEXT,
    PuntajeMinimoAprobatorio DECIMAL(5,2) DEFAULT 70.00,
    PuntajeMaximo DECIMAL(5,2) DEFAULT 100.00,
    IntentosPermitidos INT DEFAULT 3,
    TiempoLimiteMinutos INT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo(IdModulo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_puntaje_minimo
        CHECK (PuntajeMinimoAprobatorio >= 0 AND PuntajeMinimoAprobatorio <= PuntajeMaximo),

    CONSTRAINT chk_puntaje_maximo
        CHECK (PuntajeMaximo > 0 AND PuntajeMaximo <= 100),

    INDEX idx_evaluacion_modulo (IdModulo),
    INDEX idx_evaluacion_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Evaluaciones asociadas a módulos';

-- Tabla: instituto_ResultadoEvaluacion
CREATE TABLE IF NOT EXISTS instituto_ResultadoEvaluacion (
    IdResultado INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    IdEvaluacion INT NOT NULL,
    PuntajeObtenido DECIMAL(5,2),
    Aprobado TINYINT(1),
    IntentoNumero INT,
    FechaRealizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    TiempoInvertidoMinutos INT,

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_ProgresoModulo(IdInscripcion)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdEvaluacion) REFERENCES instituto_Evaluacion(IdEvaluacion)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_intento
        CHECK (IntentoNumero > 0),

    CONSTRAINT chk_puntaje_obtenido
        CHECK (PuntajeObtenido >= 0 AND PuntajeObtenido <= 100),

    INDEX idx_resultado_inscripcion (IdInscripcion),
    INDEX idx_resultado_evaluacion (IdEvaluacion),
    INDEX idx_resultado_aprobado (Aprobado),
    INDEX idx_resultado_fecha (FechaRealizacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Resultados de evaluaciones de usuarios';

-- ============================================
-- AUDITORÍA E HISTORIAL
-- ============================================

-- Tabla: instituto_HistorialProgreso
CREATE TABLE IF NOT EXISTS instituto_HistorialProgreso (
    IdHistorial INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    EstatusAnterior VARCHAR(50),
    EstatusNuevo VARCHAR(50),
    PorcentajeAnterior DECIMAL(5,2),
    PorcentajeNuevo DECIMAL(5,2),
    FechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    Comentario TEXT,
    IdUsuarioModificador INT,

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_ProgresoModulo(IdInscripcion)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdUsuarioModificador) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_historial_inscripcion (IdInscripcion),
    INDEX idx_historial_fecha (FechaCambio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Historial de cambios en el progreso de módulos';

-- Tabla: instituto_AuditoriaAcceso
CREATE TABLE IF NOT EXISTS instituto_AuditoriaAcceso (
    IdAuditoria INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT,
    Accion VARCHAR(255),
    Modulo VARCHAR(100),
    Detalle TEXT,
    DireccionIP VARCHAR(45),
    UserAgent TEXT,
    Exito TINYINT(1),
    FechaAccion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_auditoria_usuario (IdUsuario),
    INDEX idx_auditoria_fecha (FechaAccion),
    INDEX idx_auditoria_accion (Accion),
    INDEX idx_auditoria_exito (Exito)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Auditoría de accesos y acciones del sistema';

-- ============================================
-- SOPORTE Y REPORTES
-- ============================================

-- Tabla: instituto_Soporte
CREATE TABLE IF NOT EXISTS instituto_Soporte (
    IdSoporte INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT,
    FechaSolicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
    Asunto VARCHAR(255),
    Descripcion TEXT,
    Categoria VARCHAR(50),
    Prioridad VARCHAR(20) DEFAULT 'Media',
    Estatus VARCHAR(50) DEFAULT 'Abierto',
    IdUsuarioAsignado INT,
    FechaRespuesta DATETIME,
    FechaCierre DATETIME,
    Respuesta TEXT,

    FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (IdUsuarioAsignado) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_soporte_usuario (IdUsuario),
    INDEX idx_soporte_estatus (Estatus),
    INDEX idx_soporte_prioridad (Prioridad),
    INDEX idx_soporte_fecha (FechaSolicitud)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tickets de soporte del sistema';

-- Tabla: instituto_ReporteGuardado
CREATE TABLE IF NOT EXISTS instituto_ReporteGuardado (
    IdReporte INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuarioCreador INT,
    NombreReporte VARCHAR(255),
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    TipoReporte VARCHAR(100),
    Descripcion TEXT,
    FiltrosJSON JSON,
    Compartido TINYINT(1) DEFAULT 0,
    Favorito TINYINT(1) DEFAULT 0,

    FOREIGN KEY (IdUsuarioCreador) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_reporte_creador (IdUsuarioCreador),
    INDEX idx_reporte_tipo (TipoReporte),
    INDEX idx_reporte_fecha (FechaCreacion),
    INDEX idx_reporte_compartido (Compartido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Reportes guardados por usuarios';

-- ============================================
-- TABLAS ADICIONALES
-- ============================================

-- Tabla: instituto_Notificacion
CREATE TABLE IF NOT EXISTS instituto_Notificacion (
    IdNotificacion INT PRIMARY KEY AUTO_INCREMENT,
    IdUsuario INT NOT NULL,
    TipoNotificacion VARCHAR(50),
    Titulo VARCHAR(255),
    Mensaje TEXT,
    Prioridad VARCHAR(20) DEFAULT 'Media',
    Leida TINYINT(1) DEFAULT 0,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaLectura DATETIME,
    UrlDestino VARCHAR(500),

    FOREIGN KEY (IdUsuario) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_notif_usuario (IdUsuario),
    INDEX idx_notif_leida (Leida),
    INDEX idx_notif_tipo (TipoNotificacion),
    INDEX idx_notif_fecha (FechaCreacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Notificaciones para usuarios';

-- Tabla: instituto_Certificado
CREATE TABLE IF NOT EXISTS instituto_Certificado (
    IdCertificado INT PRIMARY KEY AUTO_INCREMENT,
    IdInscripcion INT NOT NULL,
    CodigoCertificado VARCHAR(50) UNIQUE,
    FechaEmision DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaVencimiento DATE,
    UrlPDF VARCHAR(500),
    HashVerificacion VARCHAR(64),
    Valido TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdInscripcion) REFERENCES instituto_ProgresoModulo(IdInscripcion)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_cert_inscripcion (IdInscripcion),
    INDEX idx_cert_codigo (CodigoCertificado),
    INDEX idx_cert_valido (Valido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Certificados de finalización de módulos';

-- Tabla: instituto_RecursoModulo
CREATE TABLE IF NOT EXISTS instituto_RecursoModulo (
    IdRecurso INT PRIMARY KEY AUTO_INCREMENT,
    IdModulo INT NOT NULL,
    NombreRecurso VARCHAR(255),
    TipoRecurso VARCHAR(50),
    UrlRecurso VARCHAR(500),
    Descripcion TEXT,
    TamanoBytes BIGINT,
    Orden INT DEFAULT 0,
    Obligatorio TINYINT(1) DEFAULT 0,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Activo TINYINT(1) DEFAULT 1,

    FOREIGN KEY (IdModulo) REFERENCES instituto_Modulo(IdModulo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_recurso_modulo (IdModulo),
    INDEX idx_recurso_tipo (TipoRecurso),
    INDEX idx_recurso_orden (Orden)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Recursos asociados a módulos';

-- ============================================
-- VISTAS ÚTILES
-- ============================================

CREATE OR REPLACE VIEW vw_instituto_UsuarioProgresoCompleto AS
SELECT
    u.IdUsuario,
    u.UserId,
    u.NombreCompleto,
    u.UserEmail,
    un.NombreUnidad,
    d.NombreDepartamento,
    r.NombreRol,
    m.NombreModulo,
    m.CategoriaModulo,
    p.EstatusModulo,
    p.PorcentajeAvance,
    p.FechaAsignacion,
    p.FechaVencimiento,
    p.FechaFinalizacion,
    CASE
        WHEN p.FechaFinalizacion IS NOT NULL THEN 'Completado'
        WHEN p.FechaVencimiento < NOW() AND p.EstatusModulo != 'Completado' THEN 'Vencido'
        WHEN p.EstatusModulo = 'En progreso' THEN 'En Progreso'
        ELSE 'Pendiente'
    END AS EstadoReal
FROM instituto_Usuario u
LEFT JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_Rol r ON u.IdRol = r.IdRol
LEFT JOIN instituto_ProgresoModulo p ON u.UserId = p.UserId
LEFT JOIN instituto_Modulo m ON p.IdModulo = m.IdModulo;

CREATE OR REPLACE VIEW vw_instituto_ModulosPorDepartamento AS
SELECT
    un.NombreUnidad,
    d.NombreDepartamento,
    m.NombreModulo,
    m.CategoriaModulo,
    md.Obligatorio,
    md.FechaAsignacion,
    md.FechaVencimiento,
    COUNT(DISTINCT p.UserId) as UsuariosInscritos,
    SUM(CASE WHEN p.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as UsuariosCompletados
FROM instituto_ModuloDepartamento md
JOIN instituto_Modulo m ON md.IdModulo = m.IdModulo
JOIN instituto_Departamento d ON md.IdDepartamento = d.IdDepartamento
JOIN instituto_UnidadDeNegocio un ON d.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_ProgresoModulo p ON m.IdModulo = p.IdModulo
WHERE md.Activo = 1 AND m.Activo = 1
GROUP BY md.IdModuloDepto, un.NombreUnidad, d.NombreDepartamento, m.NombreModulo;

CREATE OR REPLACE VIEW vw_instituto_EstadisticasEvaluaciones AS
SELECT
    m.NombreModulo,
    e.NombreEvaluacion,
    e.PuntajeMinimoAprobatorio,
    COUNT(DISTINCT re.IdResultado) as TotalIntentos,
    COUNT(DISTINCT re.IdInscripcion) as UsuariosEvaluados,
    AVG(re.PuntajeObtenido) as PromedioGeneral,
    SUM(CASE WHEN re.Aprobado = 1 THEN 1 ELSE 0 END) as TotalAprobados,
    ROUND(SUM(CASE WHEN re.Aprobado = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT re.IdInscripcion), 2) as PorcentajeAprobacion
FROM instituto_Evaluacion e
JOIN instituto_Modulo m ON e.IdModulo = m.IdModulo
LEFT JOIN instituto_ResultadoEvaluacion re ON e.IdEvaluacion = re.IdEvaluacion
GROUP BY e.IdEvaluacion, m.NombreModulo, e.NombreEvaluacion;

-- ============================================
-- PROCEDIMIENTOS ALMACENADOS
-- ============================================

DELIMITER //

CREATE PROCEDURE sp_instituto_AsignarModuloUsuario(
    IN p_UserId VARCHAR(50),
    IN p_IdModulo INT,
    IN p_FechaVencimiento DATETIME
)
BEGIN
    DECLARE v_Existe INT;

    SELECT COUNT(*) INTO v_Existe
    FROM instituto_ProgresoModulo
    WHERE UserId = p_UserId AND IdModulo = p_IdModulo;

    IF v_Existe = 0 THEN
        INSERT INTO instituto_ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento)
        VALUES (p_UserId, p_IdModulo, 'No iniciado', NOW(), p_FechaVencimiento);

        SELECT 'Módulo asignado exitosamente' AS Resultado;
    ELSE
        SELECT 'El usuario ya tiene este módulo asignado' AS Resultado;
    END IF;
END //

CREATE PROCEDURE sp_instituto_ActualizarProgreso(
    IN p_IdInscripcion INT,
    IN p_NuevoEstatus VARCHAR(50),
    IN p_PorcentajeAvance DECIMAL(5,2),
    IN p_Comentario TEXT
)
BEGIN
    DECLARE v_EstatusAnterior VARCHAR(50);
    DECLARE v_PorcentajeAnterior DECIMAL(5,2);

    SELECT EstatusModulo, PorcentajeAvance
    INTO v_EstatusAnterior, v_PorcentajeAnterior
    FROM instituto_ProgresoModulo
    WHERE IdInscripcion = p_IdInscripcion;

    UPDATE instituto_ProgresoModulo
    SET EstatusModulo = p_NuevoEstatus,
        PorcentajeAvance = p_PorcentajeAvance,
        FechaInicio = CASE WHEN FechaInicio IS NULL AND p_PorcentajeAvance > 0 THEN NOW() ELSE FechaInicio END,
        FechaFinalizacion = CASE WHEN p_NuevoEstatus = 'Completado' AND FechaFinalizacion IS NULL THEN NOW() ELSE FechaFinalizacion END
    WHERE IdInscripcion = p_IdInscripcion;

    INSERT INTO instituto_HistorialProgreso (IdInscripcion, EstatusAnterior, EstatusNuevo, PorcentajeAnterior, PorcentajeNuevo, Comentario)
    VALUES (p_IdInscripcion, v_EstatusAnterior, p_NuevoEstatus, v_PorcentajeAnterior, p_PorcentajeAvance, p_Comentario);

    SELECT 'Progreso actualizado exitosamente' AS Resultado;
END //

CREATE PROCEDURE sp_instituto_RegistrarResultadoEvaluacion(
    IN p_IdInscripcion INT,
    IN p_IdEvaluacion INT,
    IN p_PuntajeObtenido DECIMAL(5,2),
    IN p_IntentoNumero INT
)
BEGIN
    DECLARE v_PuntajeMinimo DECIMAL(5,2);
    DECLARE v_Aprobado TINYINT(1);

    SELECT PuntajeMinimoAprobatorio INTO v_PuntajeMinimo
    FROM instituto_Evaluacion
    WHERE IdEvaluacion = p_IdEvaluacion;

    SET v_Aprobado = IF(p_PuntajeObtenido >= v_PuntajeMinimo, 1, 0);

    INSERT INTO instituto_ResultadoEvaluacion (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado, IntentoNumero)
    VALUES (p_IdInscripcion, p_IdEvaluacion, p_PuntajeObtenido, v_Aprobado, p_IntentoNumero);

    IF v_Aprobado = 1 THEN
        UPDATE instituto_ProgresoModulo
        SET EstatusModulo = 'Completado',
            PorcentajeAvance = 100,
            FechaFinalizacion = NOW()
        WHERE IdInscripcion = p_IdInscripcion;
    END IF;

    SELECT v_Aprobado AS Aprobado, 'Resultado registrado exitosamente' AS Mensaje;
END //

DELIMITER ;

-- ============================================
-- TRIGGERS
-- ============================================

DELIMITER //

CREATE TRIGGER trg_instituto_ActualizarUltimoAcceso
AFTER INSERT ON instituto_AuditoriaAcceso
FOR EACH ROW
BEGIN
    IF NEW.Exito = 1 AND NEW.Accion = 'Login' THEN
        UPDATE instituto_Usuario
        SET UltimoAcceso = NEW.FechaAccion
        WHERE IdUsuario = NEW.IdUsuario;
    END IF;
END //

CREATE TRIGGER trg_instituto_NotificarAsignacionModulo
AFTER INSERT ON instituto_ProgresoModulo
FOR EACH ROW
BEGIN
    DECLARE v_NombreModulo VARCHAR(255);
    DECLARE v_IdUsuario INT;

    SELECT NombreModulo INTO v_NombreModulo
    FROM instituto_Modulo WHERE IdModulo = NEW.IdModulo;

    SELECT IdUsuario INTO v_IdUsuario
    FROM instituto_Usuario WHERE UserId = NEW.UserId;

    INSERT INTO instituto_Notificacion (IdUsuario, TipoNotificacion, Titulo, Mensaje)
    VALUES (v_IdUsuario, 'Asignación',
            'Nuevo módulo asignado',
            CONCAT('Se te ha asignado el módulo: ', v_NombreModulo));
END //

CREATE TRIGGER trg_instituto_NotificarVencimiento
AFTER UPDATE ON instituto_ProgresoModulo
FOR EACH ROW
BEGIN
    DECLARE v_DiasRestantes INT;
    DECLARE v_IdUsuario INT;
    DECLARE v_NombreModulo VARCHAR(255);

    IF NEW.EstatusModulo != 'Completado' AND NEW.FechaVencimiento IS NOT NULL THEN
        SET v_DiasRestantes = DATEDIFF(NEW.FechaVencimiento, NOW());

        IF v_DiasRestantes > 0 AND v_DiasRestantes <= 3 THEN
            SELECT IdUsuario INTO v_IdUsuario
            FROM instituto_Usuario WHERE UserId = NEW.UserId;

            SELECT NombreModulo INTO v_NombreModulo
            FROM instituto_Modulo WHERE IdModulo = NEW.IdModulo;

            INSERT INTO instituto_Notificacion (IdUsuario, TipoNotificacion, Titulo, Mensaje, Prioridad)
            VALUES (v_IdUsuario, 'Vencimiento',
                    'Módulo próximo a vencer',
                    CONCAT('El módulo "', v_NombreModulo, '" vence en ', v_DiasRestantes, ' días'),
                    'Alta');
        END IF;
    END IF;
END //

DELIMITER ;

-- ============================================
-- DATOS INICIALES
-- ============================================

INSERT IGNORE INTO instituto_Rol (NombreRol, Descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Gerente', 'Gestión de módulos y reportes'),
('Instructor', 'Creación y evaluación de módulos'),
('Usuario', 'Acceso a módulos asignados'),
('Soporte', 'Atención de tickets de soporte');

INSERT IGNORE INTO instituto_UnidadDeNegocio (NombreUnidad, Codigo) VALUES
('ICAVE', 'ICAVE'),
('EIT', 'EIT'),
('LCT', 'LCT'),
('TIMSA', 'TIMSA'),
('HPMX', 'HPMX'),
('TNG', 'TNG');

-- ============================================
-- ÍNDICES ADICIONALES
-- ============================================

CREATE INDEX idx_progreso_usuario_estatus ON instituto_ProgresoModulo(UserId, EstatusModulo);
CREATE INDEX idx_usuario_unidad_depto ON instituto_Usuario(IdUnidadDeNegocio, IdDepartamento);
CREATE INDEX idx_modulo_fechas_activo ON instituto_Modulo(FechaInicioModulo, FechaCierre, Activo);

-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================

SELECT '✅ Tablas instituto_ creadas exitosamente en tngcore!' AS Resultado;

SELECT COUNT(*) AS TablasCreadas
FROM information_schema.tables
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'instituto_%';

SELECT COUNT(*) AS VistasCreadas
FROM information_schema.views
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'vw_instituto_%';

SELECT COUNT(*) AS ProcedimientosCreados
FROM information_schema.routines
WHERE routine_schema = 'tngcore' AND ROUTINE_NAME LIKE 'sp_instituto_%';
