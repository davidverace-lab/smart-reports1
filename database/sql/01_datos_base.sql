-- ============================================
-- SMART REPORTS - DATOS PARA BASE DE DATOS EXISTENTE
-- Hutchison Ports - Unidades de Negocio REALES
-- ============================================

USE SmartReports;
GO

-- ============================================
-- 1. INSERTAR UNIDADES DE NEGOCIO
-- ============================================
-- Nota: La tabla UnidadDeNegocio YA EXISTE

PRINT '=== INSERTANDO UNIDADES DE NEGOCIO ===';

-- Limpiar datos anteriores (opcional, comentar si quieres mantener)
-- DELETE FROM UnidadDeNegocio;
-- GO

-- Insertar las 10 unidades de negocio de Hutchison Ports
INSERT INTO UnidadDeNegocio (NombreUnidad, Activo)
VALUES
    ('CCI', 1),
    ('ECV', 1),
    ('EIT', 1),
    ('HPML', 1),
    ('HPMX', 1),
    ('ICAVE', 1),
    ('LCTM', 1),
    ('LCT TILH', 1),
    ('TIMSA', 1),
    ('TNG', 1);

PRINT '✓ 10 Unidades de Negocio insertadas';
GO

-- ============================================
-- 2. INSERTAR ROLES
-- ============================================
-- Nota: La tabla Rol YA EXISTE

PRINT '=== INSERTANDO ROLES ===';

-- Limpiar roles anteriores (opcional)
-- DELETE FROM Rol;
-- GO

INSERT INTO Rol (NombreRol, Descripcion, Activo)
VALUES
    ('Administrador', 'Acceso total al sistema, gestión completa de usuarios y configuración', 1),
    ('Recursos Humanos', 'Vista especializada de RRHH, gestión de personal y capacitación', 1),
    ('Gerente', 'Vista gerencial con dashboards estratégicos y reportes consolidados', 1),
    ('Usuario', 'Vista operativa básica, consulta de progreso propio', 1);

PRINT '✓ 4 Roles insertados';
GO

-- ============================================
-- 3. INSERTAR DEPARTAMENTOS POR UNIDAD
-- ============================================

PRINT '=== INSERTANDO DEPARTAMENTOS ===';

-- Obtener IDs de unidades de negocio
DECLARE @IdCCI INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'CCI');
DECLARE @IdECV INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'ECV');
DECLARE @IdEIT INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'EIT');
DECLARE @IdHPML INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'HPML');
DECLARE @IdHPMX INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'HPMX');
DECLARE @IdICAVE INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'ICAVE');
DECLARE @IdLCTM INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'LCTM');
DECLARE @IdLCTTILH INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'LCT TILH');
DECLARE @IdTIMSA INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'TIMSA');
DECLARE @IdTNG INT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'TNG');

-- Departamentos comunes para cada unidad
INSERT INTO Departamento (IdUnidadDeNegocio, NombreDepartamento, Activo)
VALUES
    -- CCI
    (@IdCCI, 'Operaciones', 1),
    (@IdCCI, 'Administración', 1),
    (@IdCCI, 'Recursos Humanos', 1),
    (@IdCCI, 'Seguridad Industrial', 1),

    -- ECV
    (@IdECV, 'Operaciones Portuarias', 1),
    (@IdECV, 'Logística', 1),
    (@IdECV, 'Mantenimiento', 1),
    (@IdECV, 'Comercial', 1),

    -- EIT
    (@IdEIT, 'Operaciones Terrestres', 1),
    (@IdEIT, 'Tecnología', 1),
    (@IdEIT, 'Finanzas', 1),
    (@IdEIT, 'Calidad', 1),

    -- HPML
    (@IdHPML, 'Terminal Portuaria', 1),
    (@IdHPML, 'Logística y Almacenamiento', 1),
    (@IdHPML, 'Recursos Humanos', 1),
    (@IdHPML, 'Seguridad', 1),

    -- HPMX
    (@IdHPMX, 'Operaciones', 1),
    (@IdHPMX, 'Administración', 1),
    (@IdHPMX, 'Comercial', 1),
    (@IdHPMX, 'Sistemas', 1),

    -- ICAVE
    (@IdICAVE, 'Operaciones Portuarias', 1),
    (@IdICAVE, 'Mantenimiento', 1),
    (@IdICAVE, 'Recursos Humanos', 1),
    (@IdICAVE, 'Medio Ambiente', 1),

    -- LCTM
    (@IdLCTM, 'Terminal de Contenedores', 1),
    (@IdLCTM, 'Logística', 1),
    (@IdLCTM, 'Administración', 1),
    (@IdLCTM, 'Seguridad Industrial', 1),

    -- LCT TILH
    (@IdLCTTILH, 'Operaciones', 1),
    (@IdLCTTILH, 'Recursos Humanos', 1),
    (@IdLCTTILH, 'Tecnología', 1),
    (@IdLCTTILH, 'Calidad y Mejora', 1),

    -- TIMSA
    (@IdTIMSA, 'Operaciones Terrestres', 1),
    (@IdTIMSA, 'Administración', 1),
    (@IdTIMSA, 'Recursos Humanos', 1),
    (@IdTIMSA, 'Mantenimiento', 1),

    -- TNG
    (@IdTNG, 'Operaciones', 1),
    (@IdTNG, 'Comercial', 1),
    (@IdTNG, 'Finanzas', 1),
    (@IdTNG, 'Recursos Humanos', 1);

PRINT '✓ 40 Departamentos insertados (4 por unidad)';
GO

PRINT '';
PRINT '============================================';
PRINT '✅ UNIDADES, ROLES Y DEPARTAMENTOS CREADOS';
PRINT '============================================';
PRINT '';
PRINT 'Unidades de Negocio: 10';
PRINT '  - CCI, ECV, EIT, HPML, HPMX';
PRINT '  - ICAVE, LCTM, LCT TILH, TIMSA, TNG';
PRINT '';
PRINT 'Roles: 4';
PRINT '  - Administrador';
PRINT '  - Recursos Humanos';
PRINT '  - Gerente';
PRINT '  - Usuario';
PRINT '';
PRINT 'Departamentos: 40 (4 por unidad)';
