-- ============================================
-- MIGRACIONES FASE 1 - URGENTE
-- Smart Reports - Instituto Hutchison Ports
-- ============================================
USE tngcore;

-- ============================================
-- 1. TABLA DE CATEGORÍAS (NORMALIZACIÓN)
-- ============================================

CREATE TABLE IF NOT EXISTS instituto_Categoria (
    IdCategoria INT PRIMARY KEY AUTO_INCREMENT,
    NombreCategoria VARCHAR(100) UNIQUE NOT NULL,
    Descripcion TEXT,
    ColorHex VARCHAR(7) DEFAULT '#009BDE' COMMENT 'Color hex para UI',
    IconoUrl VARCHAR(255) COMMENT 'URL del ícono',
    Orden INT DEFAULT 0,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_categoria_activo (Activo),
    INDEX idx_categoria_orden (Orden)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Categorías de módulos de capacitación';

-- Insertar categorías basadas en los módulos actuales
INSERT INTO instituto_Categoria (NombreCategoria, Descripcion, ColorHex, Orden) VALUES
('Filosofía Corporativa', 'Módulos sobre valores y cultura organizacional', '#003D82', 1),
('Sostenibilidad', 'Capacitación en sostenibilidad ambiental y social', '#00B5E2', 2),
('Operaciones Portuarias', 'Procesos operativos del puerto', '#009BDE', 3),
('Relaciones Laborales', 'Gestión de relaciones con sindicatos y empleados', '#33C7F0', 4),
('Seguridad Industrial', 'Normas y protocolos de seguridad', '#FF6B6B', 5),
('Ciberseguridad', 'Protección de sistemas y datos', '#6C63FF', 6),
('Salud Laboral', 'Salud ocupacional y bienestar', '#51CF66', 7),
('Recursos Humanos', 'Procesos de gestión de personas', '#FFA94D', 8);

-- Agregar columna IdCategoria a instituto_Modulo
ALTER TABLE instituto_Modulo
ADD COLUMN IdCategoria INT AFTER NombreModulo,
ADD COLUMN Prerequisitos JSON COMMENT 'IDs de módulos requeridos',
ADD COLUMN Obligatorio TINYINT(1) DEFAULT 0 COMMENT 'Obligatorio para todos',
ADD COLUMN NivelDificultad TINYINT(1) DEFAULT 1 COMMENT '1=Básico, 2=Intermedio, 3=Avanzado',
ADD FOREIGN KEY fk_modulo_categoria (IdCategoria)
    REFERENCES instituto_Categoria(IdCategoria)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- Migrar datos existentes de CategoriaModulo a IdCategoria
UPDATE instituto_Modulo m
JOIN instituto_Categoria c ON m.CategoriaModulo = c.NombreCategoria
SET m.IdCategoria = c.IdCategoria
WHERE m.CategoriaModulo IS NOT NULL;

-- Crear índice en la nueva columna
CREATE INDEX idx_modulo_categoria ON instituto_Modulo(IdCategoria);


-- ============================================
-- 2. SISTEMA DE PERMISOS GRANULARES
-- ============================================

CREATE TABLE IF NOT EXISTS instituto_Permiso (
    IdPermiso INT PRIMARY KEY AUTO_INCREMENT,
    NombrePermiso VARCHAR(100) UNIQUE NOT NULL,
    Recurso VARCHAR(50) NOT NULL COMMENT 'Módulo, Usuario, Reporte, etc.',
    Accion VARCHAR(50) NOT NULL COMMENT 'Crear, Leer, Actualizar, Eliminar',
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_permiso_recurso (Recurso),
    INDEX idx_permiso_accion (Accion),
    INDEX idx_permiso_activo (Activo),
    UNIQUE KEY uq_permiso_recurso_accion (Recurso, Accion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Permisos granulares del sistema';

CREATE TABLE IF NOT EXISTS instituto_RolPermiso (
    IdRolPermiso INT PRIMARY KEY AUTO_INCREMENT,
    IdRol INT NOT NULL,
    IdPermiso INT NOT NULL,
    Permitir TINYINT(1) DEFAULT 1 COMMENT '1=Permitir, 0=Denegar',
    FechaAsignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    IdUsuarioAsignador INT COMMENT 'Quién asignó el permiso',

    FOREIGN KEY (IdRol) REFERENCES instituto_Rol(IdRol)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdPermiso) REFERENCES instituto_Permiso(IdPermiso)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (IdUsuarioAsignador) REFERENCES instituto_Usuario(IdUsuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    UNIQUE KEY uq_rol_permiso (IdRol, IdPermiso),
    INDEX idx_rolpermiso_rol (IdRol),
    INDEX idx_rolpermiso_permiso (IdPermiso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Relación N:N entre roles y permisos';

-- Insertar permisos básicos del sistema
INSERT INTO instituto_Permiso (NombrePermiso, Recurso, Accion, Descripcion) VALUES
-- Usuarios
('ver_usuarios', 'Usuario', 'Leer', 'Ver listado de usuarios'),
('crear_usuarios', 'Usuario', 'Crear', 'Crear nuevos usuarios'),
('editar_usuarios', 'Usuario', 'Actualizar', 'Editar información de usuarios'),
('eliminar_usuarios', 'Usuario', 'Eliminar', 'Eliminar usuarios'),

-- Módulos
('ver_modulos', 'Modulo', 'Leer', 'Ver módulos disponibles'),
('crear_modulos', 'Modulo', 'Crear', 'Crear nuevos módulos'),
('editar_modulos', 'Modulo', 'Actualizar', 'Editar módulos'),
('eliminar_modulos', 'Modulo', 'Eliminar', 'Eliminar módulos'),
('asignar_modulos', 'Modulo', 'Asignar', 'Asignar módulos a usuarios/departamentos'),

-- Evaluaciones
('ver_evaluaciones', 'Evaluacion', 'Leer', 'Ver evaluaciones'),
('crear_evaluaciones', 'Evaluacion', 'Crear', 'Crear evaluaciones'),
('editar_evaluaciones', 'Evaluacion', 'Actualizar', 'Editar evaluaciones'),
('calificar_evaluaciones', 'Evaluacion', 'Calificar', 'Calificar evaluaciones'),

-- Reportes
('ver_reportes', 'Reporte', 'Leer', 'Ver reportes'),
('crear_reportes', 'Reporte', 'Crear', 'Crear reportes personalizados'),
('exportar_reportes', 'Reporte', 'Exportar', 'Exportar reportes a PDF/Excel'),

-- Dashboards
('ver_dashboard_gerencial', 'Dashboard', 'Leer', 'Acceso a dashboards gerenciales'),
('ver_dashboard_rrhh', 'Dashboard', 'Leer', 'Acceso a dashboard de RRHH'),

-- Certificados
('ver_certificados', 'Certificado', 'Leer', 'Ver certificados'),
('emitir_certificados', 'Certificado', 'Crear', 'Emitir certificados'),
('revocar_certificados', 'Certificado', 'Revocar', 'Revocar certificados'),

-- Configuración
('ver_configuracion', 'Configuracion', 'Leer', 'Ver configuración del sistema'),
('editar_configuracion', 'Configuracion', 'Actualizar', 'Modificar configuración'),

-- Auditoría
('ver_auditoria', 'Auditoria', 'Leer', 'Ver logs de auditoría'),

-- Soporte
('ver_soporte', 'Soporte', 'Leer', 'Ver tickets de soporte'),
('crear_soporte', 'Soporte', 'Crear', 'Crear tickets de soporte'),
('gestionar_soporte', 'Soporte', 'Gestionar', 'Gestionar y responder tickets');

-- Asignar permisos a rol Administrador (todos los permisos)
INSERT INTO instituto_RolPermiso (IdRol, IdPermiso, Permitir)
SELECT
    r.IdRol,
    p.IdPermiso,
    1
FROM instituto_Rol r
CROSS JOIN instituto_Permiso p
WHERE r.NombreRol = 'Administrador';

-- Asignar permisos a rol Gerente (mayoría de permisos excepto configuración)
INSERT INTO instituto_RolPermiso (IdRol, IdPermiso, Permitir)
SELECT
    r.IdRol,
    p.IdPermiso,
    1
FROM instituto_Rol r
CROSS JOIN instituto_Permiso p
WHERE r.NombreRol = 'Gerente'
  AND p.Recurso NOT IN ('Configuracion', 'Auditoria');

-- Asignar permisos a rol Usuario (solo lectura y su propio progreso)
INSERT INTO instituto_RolPermiso (IdRol, IdPermiso, Permitir)
SELECT
    r.IdRol,
    p.IdPermiso,
    1
FROM instituto_Rol r
CROSS JOIN instituto_Permiso p
WHERE r.NombreRol = 'Usuario'
  AND p.Accion IN ('Leer', 'Crear')
  AND p.Recurso IN ('Modulo', 'Certificado', 'Soporte');


-- ============================================
-- 3. NORMALIZACIÓN DE NIVELES Y POSICIONES
-- ============================================

CREATE TABLE IF NOT EXISTS instituto_Nivel (
    IdNivel INT PRIMARY KEY AUTO_INCREMENT,
    NombreNivel VARCHAR(100) UNIQUE NOT NULL,
    Jerarquia INT NOT NULL COMMENT 'Nivel jerárquico 1-10 (1=más alto)',
    Descripcion TEXT,
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_nivel_jerarquia (Jerarquia),
    INDEX idx_nivel_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Niveles jerárquicos de la organización';

-- Insertar niveles jerárquicos
INSERT INTO instituto_Nivel (NombreNivel, Jerarquia, Descripcion) VALUES
('Director General', 1, 'Máximo nivel ejecutivo'),
('Director de Área', 2, 'Dirección de áreas funcionales'),
('Gerente Senior', 3, 'Gerencia de alto nivel'),
('Gerente', 4, 'Gerencia media'),
('Subgerente', 5, 'Apoyo a gerencia'),
('Supervisor', 6, 'Supervisión de equipos'),
('Coordinador', 7, 'Coordinación de procesos'),
('Analista Senior', 8, 'Análisis especializado'),
('Analista', 9, 'Análisis general'),
('Asistente', 10, 'Apoyo administrativo');

CREATE TABLE IF NOT EXISTS instituto_Posicion (
    IdPosicion INT PRIMARY KEY AUTO_INCREMENT,
    NombrePosicion VARCHAR(150) UNIQUE NOT NULL,
    IdDepartamento INT COMMENT 'Departamento al que pertenece',
    IdNivel INT COMMENT 'Nivel jerárquico de la posición',
    Descripcion TEXT,
    ResponsabilidadesJSON JSON COMMENT 'Lista de responsabilidades',
    CompetenciasRequeridas JSON COMMENT 'Competencias necesarias',
    Activo TINYINT(1) DEFAULT 1,
    FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (IdDepartamento) REFERENCES instituto_Departamento(IdDepartamento)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (IdNivel) REFERENCES instituto_Nivel(IdNivel)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_posicion_departamento (IdDepartamento),
    INDEX idx_posicion_nivel (IdNivel),
    INDEX idx_posicion_activo (Activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Posiciones laborales en la organización';

-- Agregar columnas a Usuario
ALTER TABLE instituto_Usuario
ADD COLUMN IdNivel INT AFTER IdRol,
ADD COLUMN IdPosicion INT AFTER IdNivel,
ADD FOREIGN KEY fk_usuario_nivel (IdNivel)
    REFERENCES instituto_Nivel(IdNivel)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
ADD FOREIGN KEY fk_usuario_posicion (IdPosicion)
    REFERENCES instituto_Posicion(IdPosicion)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

CREATE INDEX idx_usuario_nivel_posicion ON instituto_Usuario(IdNivel, IdPosicion);


-- ============================================
-- 4. ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================

-- Búsquedas por email y estado
CREATE INDEX idx_usuario_email_activo
ON instituto_Usuario(UserEmail, Activo);

-- Progreso por usuario, estatus y módulo
CREATE INDEX idx_progreso_usuario_estatus_modulo
ON instituto_ProgresoModulo(UserId, EstatusModulo, IdModulo);

-- Evaluaciones por módulo y estado
CREATE INDEX idx_evaluacion_modulo_activo
ON instituto_Evaluacion(IdModulo, Activo);

-- Resultados ordenados por fecha descendente
CREATE INDEX idx_resultado_fecha_desc
ON instituto_ResultadoEvaluacion(FechaRealizacion DESC);

-- Notificaciones no leídas por usuario
CREATE INDEX idx_notif_usuario_leida_fecha
ON instituto_Notificacion(IdUsuario, Leida, FechaCreacion DESC);

-- Certificados válidos por código
CREATE INDEX idx_cert_codigo_valido
ON instituto_Certificado(CodigoCertificado, Valido);

-- Auditoría por fecha descendente y usuario
CREATE INDEX idx_audit_fecha_usuario
ON instituto_AuditoriaAcceso(FechaAccion DESC, IdUsuario);

-- Módulos activos con fechas
CREATE INDEX idx_modulo_fechas_activo
ON instituto_Modulo(FechaInicioModulo, FechaCierre, Activo);

-- Usuarios por unidad y departamento
CREATE INDEX idx_usuario_unidad_depto
ON instituto_Usuario(IdUnidadDeNegocio, IdDepartamento, Activo);


-- ============================================
-- 5. VISTAS ADICIONALES PARA DASHBOARDS
-- ============================================

CREATE OR REPLACE VIEW vw_instituto_DashboardUsuario AS
SELECT
    u.IdUsuario,
    u.UserId,
    u.NombreCompleto,
    u.UserEmail,
    un.NombreUnidad,
    d.NombreDepartamento,
    r.NombreRol,
    n.NombreNivel,
    p.NombrePosicion,
    COUNT(DISTINCT pm.IdModulo) as ModulosAsignados,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados,
    ROUND(AVG(pm.PorcentajeAvance), 2) as ProgresoPromedio,
    COUNT(DISTINCT c.IdCertificado) as CertificadosObtenidos,
    MAX(pm.FechaFinalizacion) as UltimaFinalizacion,
    u.UltimoAcceso
FROM instituto_Usuario u
LEFT JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_Rol r ON u.IdRol = r.IdRol
LEFT JOIN instituto_Nivel n ON u.IdNivel = n.IdNivel
LEFT JOIN instituto_Posicion p ON u.IdPosicion = p.IdPosicion
LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
LEFT JOIN instituto_Certificado c ON pm.IdInscripcion = c.IdInscripcion AND c.Valido = 1
WHERE u.Activo = 1
GROUP BY u.IdUsuario;

CREATE OR REPLACE VIEW vw_instituto_EstadisticasModulo AS
SELECT
    m.IdModulo,
    m.NombreModulo,
    cat.NombreCategoria as Categoria,
    m.DuracionEstimadaHoras,
    m.NivelDificultad,
    COUNT(DISTINCT pm.UserId) as UsuariosInscritos,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as UsuariosCompletados,
    ROUND(100.0 * SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) /
        NULLIF(COUNT(DISTINCT pm.UserId), 0), 2) as PorcentajeCompletado,
    ROUND(AVG(CASE WHEN pm.EstatusModulo = 'Completado' THEN pm.TiempoInvertidoMinutos END), 0) as TiempoPromedioMinutos,
    ROUND(AVG(CASE WHEN re.Aprobado = 1 THEN re.PuntajeObtenido END), 2) as PromedioCalificacion,
    COUNT(DISTINCT e.IdEvaluacion) as NumeroEvaluaciones,
    COUNT(DISTINCT rec.IdRecurso) as NumeroRecursos
FROM instituto_Modulo m
LEFT JOIN instituto_Categoria cat ON m.IdCategoria = cat.IdCategoria
LEFT JOIN instituto_ProgresoModulo pm ON m.IdModulo = pm.IdModulo
LEFT JOIN instituto_Evaluacion e ON m.IdModulo = e.IdModulo
LEFT JOIN instituto_RecursoModulo rec ON m.IdModulo = rec.IdModulo AND rec.Activo = 1
LEFT JOIN instituto_ResultadoEvaluacion re ON e.IdEvaluacion = re.IdEvaluacion
WHERE m.Activo = 1
GROUP BY m.IdModulo;

CREATE OR REPLACE VIEW vw_instituto_AlertasVencimiento AS
SELECT
    u.IdUsuario,
    u.NombreCompleto,
    u.UserEmail,
    un.NombreUnidad,
    d.NombreDepartamento,
    m.NombreModulo,
    pm.FechaAsignacion,
    pm.FechaVencimiento,
    DATEDIFF(pm.FechaVencimiento, NOW()) as DiasRestantes,
    pm.PorcentajeAvance,
    pm.EstatusModulo,
    CASE
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) < 0 THEN 'Vencido'
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) <= 3 THEN 'Urgente'
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) <= 7 THEN 'Próximo'
        ELSE 'Normal'
    END as Prioridad
FROM instituto_ProgresoModulo pm
JOIN instituto_Usuario u ON pm.UserId = u.UserId
JOIN instituto_Modulo m ON pm.IdModulo = m.IdModulo
LEFT JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
WHERE pm.EstatusModulo != 'Completado'
  AND pm.FechaVencimiento IS NOT NULL
  AND u.Activo = 1
  AND m.Activo = 1
ORDER BY pm.FechaVencimiento;


-- ============================================
-- 6. PROCEDIMIENTO PARA VERIFICAR PERMISOS
-- ============================================

DELIMITER //

CREATE PROCEDURE sp_instituto_VerificarPermiso(
    IN p_IdUsuario INT,
    IN p_Recurso VARCHAR(50),
    IN p_Accion VARCHAR(50)
)
BEGIN
    DECLARE v_TienePermiso INT DEFAULT 0;

    SELECT COUNT(*) INTO v_TienePermiso
    FROM instituto_Usuario u
    JOIN instituto_RolPermiso rp ON u.IdRol = rp.IdRol
    JOIN instituto_Permiso p ON rp.IdPermiso = p.IdPermiso
    WHERE u.IdUsuario = p_IdUsuario
      AND p.Recurso = p_Recurso
      AND p.Accion = p_Accion
      AND rp.Permitir = 1
      AND p.Activo = 1;

    SELECT v_TienePermiso as TienePermiso;
END //

DELIMITER ;


-- ============================================
-- 7. TRIGGER PARA AUDITAR CAMBIOS EN MÓDULOS
-- ============================================

DELIMITER //

CREATE TRIGGER trg_instituto_AuditarCambiosModulo
AFTER UPDATE ON instituto_Modulo
FOR EACH ROW
BEGIN
    IF OLD.NombreModulo != NEW.NombreModulo
       OR OLD.Activo != NEW.Activo
       OR OLD.FechaInicioModulo != NEW.FechaInicioModulo THEN

        INSERT INTO instituto_AuditoriaAcceso (IdUsuario, Accion, Modulo, Detalle, Exito)
        VALUES (
            NEW.IdCreador,
            'Modificación de Módulo',
            'Modulo',
            CONCAT('Módulo ID ', NEW.IdModulo, ' modificado'),
            1
        );
    END IF;
END //

DELIMITER ;


-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================

SELECT '✅ FASE 1 - MIGRACIONES URGENTES COMPLETADAS' AS Resultado;

SELECT
    'Categorías' as Tabla,
    COUNT(*) as Registros
FROM instituto_Categoria
UNION ALL
SELECT
    'Permisos' as Tabla,
    COUNT(*) as Registros
FROM instituto_Permiso
UNION ALL
SELECT
    'Roles-Permisos' as Tabla,
    COUNT(*) as Registros
FROM instituto_RolPermiso
UNION ALL
SELECT
    'Niveles' as Tabla,
    COUNT(*) as Registros
FROM instituto_Nivel;

SELECT COUNT(*) as IndicesCreados
FROM information_schema.statistics
WHERE table_schema = 'tngcore'
  AND table_name LIKE 'instituto_%'
  AND index_name LIKE 'idx_%';

SELECT COUNT(*) as VistasCreadas
FROM information_schema.views
WHERE table_schema = 'tngcore'
  AND table_name LIKE 'vw_instituto_%';
