-- ============================================================
-- SCRIPT: Insertar datos base para Hutchison Ports (MYSQL)
-- Descripción: Unidades de negocio, roles y departamentos
-- Base de datos: MySQL
-- Esquema: REAL (Usuario, UnidadDeNegocio, Rol)
-- ============================================================

USE SmartReports;

-- ============================================================
-- 1. INSERTAR UNIDADES DE NEGOCIO
-- ============================================================

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
    ('TNG', 1)
ON DUPLICATE KEY UPDATE NombreUnidad = VALUES(NombreUnidad);

-- ============================================================
-- 2. INSERTAR ROLES
-- ============================================================

INSERT INTO Rol (NombreRol, Descripcion)
VALUES
    ('Administrador', 'Acceso total al sistema'),
    ('Recursos Humanos', 'Gestión de personal y capacitación'),
    ('Gerente', 'Supervisión y análisis gerencial'),
    ('Usuario', 'Acceso operativo básico')
ON DUPLICATE KEY UPDATE Descripcion = VALUES(Descripcion);

-- ============================================================
-- 3. INSERTAR DEPARTAMENTOS
-- ============================================================

INSERT INTO Departamento (NombreDepartamento, Activo)
VALUES
    ('Operaciones', 1),
    ('Administración', 1),
    ('Logística', 1),
    ('Recursos Humanos', 1),
    ('Finanzas', 1),
    ('IT', 1),
    ('Comercial', 1),
    ('Seguridad', 1)
ON DUPLICATE KEY UPDATE NombreDepartamento = VALUES(NombreDepartamento);

-- ============================================================
-- VERIFICACIÓN
-- ============================================================

SELECT '=== UNIDADES DE NEGOCIO ===' AS '';
SELECT IdUnidadDeNegocio, NombreUnidad FROM UnidadDeNegocio ORDER BY IdUnidadDeNegocio;

SELECT '=== ROLES ===' AS '';
SELECT IdRol, NombreRol FROM Rol ORDER BY IdRol;

SELECT '=== DEPARTAMENTOS ===' AS '';
SELECT IdDepartamento, NombreDepartamento FROM Departamento ORDER BY IdDepartamento;
