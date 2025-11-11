-- ============================================
-- SMART REPORTS - UNIDADES DE NEGOCIO
-- Instituto Hutchison Ports v2.0
-- ============================================

USE SmartReports;
GO

-- Tabla de Unidades de Negocio
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'instituto_UnidadNegocio')
BEGIN
    CREATE TABLE instituto_UnidadNegocio (
        UnidadID INT PRIMARY KEY IDENTITY(1,1),
        Codigo NVARCHAR(20) NOT NULL UNIQUE,
        Nombre NVARCHAR(100) NOT NULL,
        Descripcion NVARCHAR(500),
        GerenteResponsable NVARCHAR(100),
        Email NVARCHAR(100),
        Activo BIT DEFAULT 1,
        FechaCreacion DATETIME DEFAULT GETDATE(),
        FechaModificacion DATETIME DEFAULT GETDATE()
    );

    PRINT '✓ Tabla instituto_UnidadNegocio creada';
END
ELSE
BEGIN
    PRINT '⚠ Tabla instituto_UnidadNegocio ya existe';
END
GO

-- Insertar Unidades de Negocio de Hutchison Ports
DELETE FROM instituto_UnidadNegocio;
GO

INSERT INTO instituto_UnidadNegocio (Codigo, Nombre, Descripcion, GerenteResponsable, Email, Activo)
VALUES
    ('TERM-001', 'Terminal Portuaria 1', 'Terminal de contenedores principal', 'Carlos Mendoza', 'cmendoza@hutchison.com', 1),
    ('TERM-002', 'Terminal Portuaria 2', 'Terminal de carga general', 'Ana Rodríguez', 'arodriguez@hutchison.com', 1),
    ('LOGIS-001', 'Logística y Almacenamiento', 'Gestión logística y almacenes', 'Roberto Silva', 'rsilva@hutchison.com', 1),
    ('OPER-001', 'Operaciones Terrestres', 'Operaciones de patio y terrestres', 'María González', 'mgonzalez@hutchison.com', 1),
    ('ADMIN-001', 'Administración Central', 'Administración y finanzas', 'Jorge Ramírez', 'jramirez@hutchison.com', 1),
    ('RRHH-001', 'Recursos Humanos', 'Gestión de talento y capacitación', 'Patricia López', 'plopez@hutchison.com', 1),
    ('TI-001', 'Tecnología e Innovación', 'Sistemas y transformación digital', 'Luis Fernández', 'lfernandez@hutchison.com', 1),
    ('SEG-001', 'Seguridad y Medio Ambiente', 'SST y gestión ambiental', 'Carmen Torres', 'ctorres@hutchison.com', 1);

PRINT '✓ 8 Unidades de Negocio insertadas';
GO

-- Modificar tabla de Usuarios para vincular Unidad de Negocio
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'UnidadNegocioID' AND object_id = OBJECT_ID('instituto_Usuario'))
BEGIN
    ALTER TABLE instituto_Usuario
    ADD UnidadNegocioID INT NULL,
    CONSTRAINT FK_Usuario_UnidadNegocio FOREIGN KEY (UnidadNegocioID)
        REFERENCES instituto_UnidadNegocio(UnidadID);

    PRINT '✓ Columna UnidadNegocioID agregada a instituto_Usuario';
END
ELSE
BEGIN
    PRINT '⚠ Columna UnidadNegocioID ya existe en instituto_Usuario';
END
GO

-- Actualizar usuarios existentes con unidades de negocio aleatorias
UPDATE usuario_Usuario
SET UnidadNegocioID = (ABS(CHECKSUM(NEWID())) % 8) + 1
WHERE UnidadNegocioID IS NULL;

PRINT '✓ Usuarios actualizados con Unidades de Negocio';
GO

-- Vista para consultar usuarios con unidad de negocio
CREATE OR ALTER VIEW vw_UsuariosConUnidad AS
SELECT
    u.UsuarioID,
    u.Nombre,
    u.Email,
    u.Departamento,
    u.Cargo,
    u.Activo,
    un.UnidadID,
    un.Codigo AS UnidadCodigo,
    un.Nombre AS UnidadNombre,
    un.GerenteResponsable
FROM instituto_Usuario u
LEFT JOIN instituto_UnidadNegocio un ON u.UnidadNegocioID = un.UnidadID;
GO

PRINT '✓ Vista vw_UsuariosConUnidad creada';
PRINT '============================================';
PRINT '✅ UNIDADES DE NEGOCIO CONFIGURADAS';
PRINT '============================================';
