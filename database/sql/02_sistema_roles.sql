-- ============================================
-- SMART REPORTS - SISTEMA DE ROLES Y PERMISOS
-- Instituto Hutchison Ports v2.0
-- ============================================

USE SmartReports;
GO

-- Tabla de Roles
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'instituto_Rol')
BEGIN
    CREATE TABLE instituto_Rol (
        RolID INT PRIMARY KEY IDENTITY(1,1),
        Codigo NVARCHAR(20) NOT NULL UNIQUE,
        Nombre NVARCHAR(50) NOT NULL,
        Descripcion NVARCHAR(500),
        Nivel INT NOT NULL, -- 1=Admin, 2=Gerencial, 3=Operativo
        PermisoTotal BIT DEFAULT 0, -- Admin tiene permiso total
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE()
    );

    PRINT '✓ Tabla instituto_Rol creada';
END
GO

-- Tabla de Permisos
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'instituto_Permiso')
BEGIN
    CREATE TABLE instituto_Permiso (
        PermisoID INT PRIMARY KEY IDENTITY(1,1),
        Codigo NVARCHAR(50) NOT NULL UNIQUE,
        Nombre NVARCHAR(100) NOT NULL,
        Modulo NVARCHAR(50) NOT NULL, -- 'Usuarios', 'Reportes', 'Dashboards', etc.
        Accion NVARCHAR(50) NOT NULL, -- 'Ver', 'Crear', 'Editar', 'Eliminar', 'Exportar'
        Descripcion NVARCHAR(500),
        Activo BIT DEFAULT 1
    );

    PRINT '✓ Tabla instituto_Permiso creada';
END
GO

-- Tabla intermedia Rol-Permiso
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'instituto_RolPermiso')
BEGIN
    CREATE TABLE instituto_RolPermiso (
        RolID INT NOT NULL,
        PermisoID INT NOT NULL,
        PRIMARY KEY (RolID, PermisoID),
        CONSTRAINT FK_RolPermiso_Rol FOREIGN KEY (RolID) REFERENCES instituto_Rol(RolID),
        CONSTRAINT FK_RolPermiso_Permiso FOREIGN KEY (PermisoID) REFERENCES instituto_Permiso(PermisoID)
    );

    PRINT '✓ Tabla instituto_RolPermiso creada';
END
GO

-- Agregar RolID a tabla de Usuarios
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'RolID' AND object_id = OBJECT_ID('instituto_Usuario'))
BEGIN
    ALTER TABLE instituto_Usuario
    ADD RolID INT NULL,
    CONSTRAINT FK_Usuario_Rol FOREIGN KEY (RolID)
        REFERENCES instituto_Rol(RolID);

    PRINT '✓ Columna RolID agregada a instituto_Usuario';
END
GO

-- Insertar Roles
DELETE FROM instituto_Rol;
GO

INSERT INTO instituto_Rol (Codigo, Nombre, Descripcion, Nivel, PermisoTotal, Activo)
VALUES
    ('ADMIN', 'Administrador', 'Acceso total al sistema, gestión de usuarios, configuración', 1, 1, 1),
    ('RRHH', 'Recursos Humanos', 'Vista especializada de RRHH, reportes de personal, capacitación', 2, 0, 1),
    ('GERENTE', 'Gerente', 'Vista gerencial, dashboards estratégicos, reportes consolidados', 2, 0, 1),
    ('OPERADOR', 'Operador', 'Vista operativa, gestión de cursos propios, consulta de progreso', 3, 0, 1);

PRINT '✓ 4 Roles insertados';
GO

-- Insertar Permisos
DELETE FROM instituto_Permiso;
GO

INSERT INTO instituto_Permiso (Codigo, Nombre, Modulo, Accion, Descripcion)
VALUES
    -- Módulo Usuarios
    ('USR_VER', 'Ver Usuarios', 'Usuarios', 'Ver', 'Consultar lista de usuarios'),
    ('USR_CREAR', 'Crear Usuarios', 'Usuarios', 'Crear', 'Registrar nuevos usuarios'),
    ('USR_EDITAR', 'Editar Usuarios', 'Usuarios', 'Editar', 'Modificar datos de usuarios'),
    ('USR_ELIMINAR', 'Eliminar Usuarios', 'Usuarios', 'Eliminar', 'Eliminar usuarios del sistema'),
    ('USR_IMPORTAR', 'Importar Usuarios', 'Usuarios', 'Importar', 'Importar usuarios desde Excel'),

    -- Módulo Reportes
    ('RPT_VER', 'Ver Reportes', 'Reportes', 'Ver', 'Ver reportes generados'),
    ('RPT_GENERAR', 'Generar Reportes', 'Reportes', 'Crear', 'Generar nuevos reportes'),
    ('RPT_EXPORTAR', 'Exportar Reportes', 'Reportes', 'Exportar', 'Exportar reportes a PDF/Excel'),
    ('RPT_TODOS', 'Ver Todos los Reportes', 'Reportes', 'Ver', 'Ver reportes de todas las áreas'),
    ('RPT_DEPTO', 'Ver Reportes de Departamento', 'Reportes', 'Ver', 'Ver solo reportes del propio departamento'),

    -- Módulo Dashboards
    ('DASH_GERENCIAL', 'Dashboards Gerenciales', 'Dashboards', 'Ver', 'Ver dashboards estratégicos'),
    ('DASH_RRHH', 'Dashboards RRHH', 'Dashboards', 'Ver', 'Ver dashboards especializados de RRHH'),
    ('DASH_OPERATIVO', 'Dashboards Operativos', 'Dashboards', 'Ver', 'Ver dashboards operativos'),

    -- Módulo Configuración
    ('CFG_SISTEMA', 'Configurar Sistema', 'Configuracion', 'Editar', 'Modificar configuración del sistema'),
    ('CFG_ROLES', 'Gestionar Roles', 'Configuracion', 'Editar', 'Administrar roles y permisos'),
    ('CFG_BACKUP', 'Gestionar Respaldos', 'Configuracion', 'Crear', 'Crear y restaurar respaldos');

PRINT '✓ 16 Permisos insertados';
GO

-- Asignar permisos a rol ADMIN (todos los permisos)
DELETE FROM instituto_RolPermiso WHERE RolID = 1;
INSERT INTO instituto_RolPermiso (RolID, PermisoID)
SELECT 1, PermisoID FROM instituto_Permiso;

PRINT '✓ Permisos asignados a rol ADMIN';
GO

-- Asignar permisos a rol RRHH
DELETE FROM instituto_RolPermiso WHERE RolID = 2;
INSERT INTO instituto_RolPermiso (RolID, PermisoID)
SELECT RolID = 2, PermisoID FROM instituto_Permiso
WHERE Codigo IN (
    'USR_VER', 'USR_CREAR', 'USR_EDITAR', 'USR_IMPORTAR',  -- Usuarios (sin eliminar)
    'RPT_VER', 'RPT_GENERAR', 'RPT_EXPORTAR', 'RPT_TODOS',  -- Reportes (todos)
    'DASH_RRHH', 'DASH_OPERATIVO'  -- Dashboards RRHH
);

PRINT '✓ Permisos asignados a rol RRHH';
GO

-- Asignar permisos a rol GERENTE
DELETE FROM instituto_RolPermiso WHERE RolID = 3;
INSERT INTO instituto_RolPermiso (RolID, PermisoID)
SELECT RolID = 3, PermisoID FROM instituto_Permiso
WHERE Codigo IN (
    'USR_VER',  -- Solo ver usuarios
    'RPT_VER', 'RPT_GENERAR', 'RPT_EXPORTAR', 'RPT_DEPTO',  -- Reportes de su depto
    'DASH_GERENCIAL', 'DASH_OPERATIVO'  -- Dashboards gerenciales
);

PRINT '✓ Permisos asignados a rol GERENTE';
GO

-- Asignar permisos a rol OPERADOR
DELETE FROM instituto_RolPermiso WHERE RolID = 4;
INSERT INTO instituto_RolPermiso (RolID, PermisoID)
SELECT RolID = 4, PermisoID FROM instituto_Permiso
WHERE Codigo IN (
    'RPT_VER', 'RPT_EXPORTAR',  -- Solo ver y exportar reportes propios
    'DASH_OPERATIVO'  -- Solo dashboards operativos
);

PRINT '✓ Permisos asignados a rol OPERADOR';
GO

-- Crear usuario Admin por defecto
IF NOT EXISTS (SELECT * FROM instituto_Usuario WHERE Email = 'admin@hutchison.com')
BEGIN
    INSERT INTO instituto_Usuario (Nombre, Email, Departamento, Cargo, UnidadNegocioID, RolID, Activo, Contraseña)
    VALUES ('Administrador Sistema', 'admin@hutchison.com', 'Tecnología', 'Administrador de Sistemas', 7, 1, 1, 'admin123');

    PRINT '✓ Usuario Admin creado (admin@hutchison.com / admin123)';
END
GO

-- Crear usuario RRHH por defecto
IF NOT EXISTS (SELECT * FROM instituto_Usuario WHERE Email = 'rrhh@hutchison.com')
BEGIN
    INSERT INTO instituto_Usuario (Nombre, Email, Departamento, Cargo, UnidadNegocioID, RolID, Activo, Contraseña)
    VALUES ('Coordinador RRHH', 'rrhh@hutchison.com', 'Recursos Humanos', 'Coordinador de Capacitación', 6, 2, 1, 'rrhh123');

    PRINT '✓ Usuario RRHH creado (rrhh@hutchison.com / rrhh123)';
END
GO

-- Asignar roles a usuarios existentes (aleatorio para demo)
UPDATE instituto_Usuario
SET RolID = CASE
    WHEN Cargo LIKE '%Gerente%' OR Cargo LIKE '%Director%' THEN 3  -- Gerente
    WHEN Departamento = 'Recursos Humanos' THEN 2  -- RRHH
    WHEN Email NOT IN ('admin@hutchison.com', 'rrhh@hutchison.com') THEN 4  -- Operador
    ELSE RolID
END
WHERE RolID IS NULL;

PRINT '✓ Roles asignados a usuarios existentes';
GO

-- Vista para consultar usuarios con roles y permisos
CREATE OR ALTER VIEW vw_UsuariosConRoles AS
SELECT
    u.UsuarioID,
    u.Nombre,
    u.Email,
    u.Departamento,
    u.Cargo,
    r.RolID,
    r.Codigo AS RolCodigo,
    r.Nombre AS RolNombre,
    r.Nivel AS RolNivel,
    r.PermisoTotal,
    un.Nombre AS UnidadNegocio
FROM instituto_Usuario u
LEFT JOIN instituto_Rol r ON u.RolID = r.RolID
LEFT JOIN instituto_UnidadNegocio un ON u.UnidadNegocioID = un.UnidadID;
GO

-- Función para verificar si usuario tiene permiso
CREATE OR ALTER FUNCTION fn_UsuarioTienePermiso
(
    @UsuarioID INT,
    @CodigoPermiso NVARCHAR(50)
)
RETURNS BIT
AS
BEGIN
    DECLARE @TienePermiso BIT = 0;

    -- Si el usuario tiene rol con permiso total (Admin)
    IF EXISTS (
        SELECT 1 FROM instituto_Usuario u
        INNER JOIN instituto_Rol r ON u.RolID = r.RolID
        WHERE u.UsuarioID = @UsuarioID AND r.PermisoTotal = 1
    )
    BEGIN
        SET @TienePermiso = 1;
        RETURN @TienePermiso;
    END

    -- Verificar si tiene el permiso específico
    IF EXISTS (
        SELECT 1 FROM instituto_Usuario u
        INNER JOIN instituto_RolPermiso rp ON u.RolID = rp.RolID
        INNER JOIN instituto_Permiso p ON rp.PermisoID = p.PermisoID
        WHERE u.UsuarioID = @UsuarioID AND p.Codigo = @CodigoPermiso
    )
    BEGIN
        SET @TienePermiso = 1;
    END

    RETURN @TienePermiso;
END
GO

PRINT '✓ Vista vw_UsuariosConRoles creada';
PRINT '✓ Función fn_UsuarioTienePermiso creada';
PRINT '============================================';
PRINT '✅ SISTEMA DE ROLES CONFIGURADO';
PRINT '============================================';
PRINT '';
PRINT 'Usuarios creados:';
PRINT '  Admin: admin@hutchison.com / admin123';
PRINT '  RRHH:  rrhh@hutchison.com / rrhh123';
PRINT '';
PRINT 'Roles disponibles:';
PRINT '  1. ADMIN - Acceso total';
PRINT '  2. RRHH - Vista especializada RRHH';
PRINT '  3. GERENTE - Vista gerencial';
PRINT '  4. OPERADOR - Vista operativa';
