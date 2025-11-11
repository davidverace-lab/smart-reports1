-- ============================================================
-- SCRIPT: Insertar 32 usuarios de prueba (MYSQL)
-- Descripción: Admin, RRHH + 30 usuarios reales
-- Base de datos: MySQL
-- Esquema: REAL (Usuario)
-- ============================================================

USE SmartReports;

-- ============================================================
-- OBTENER IDs DE UNIDADES (guardar en variables)
-- ============================================================
-- En MySQL las variables se usan con @variable

SET @IdCCI = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'CCI' LIMIT 1);
SET @IdECV = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'ECV' LIMIT 1);
SET @IdEIT = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'EIT' LIMIT 1);
SET @IdHPML = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'HPML' LIMIT 1);
SET @IdHPMX = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'HPMX' LIMIT 1);
SET @IdICAVE = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'ICAVE' LIMIT 1);
SET @IdLCTM = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'LCTM' LIMIT 1);
SET @IdTILH = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'LCT TILH' LIMIT 1);
SET @IdTIMSA = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'TIMSA' LIMIT 1);
SET @IdTNG = (SELECT IdUnidadDeNegocio FROM UnidadDeNegocio WHERE NombreUnidad = 'TNG' LIMIT 1);

-- ============================================================
-- OBTENER IDs DE ROLES
-- ============================================================

SET @IdAdmin = (SELECT IdRol FROM Rol WHERE NombreRol = 'Administrador' LIMIT 1);
SET @IdRRHH = (SELECT IdRol FROM Rol WHERE NombreRol = 'Recursos Humanos' LIMIT 1);
SET @IdGerente = (SELECT IdRol FROM Rol WHERE NombreRol = 'Gerente' LIMIT 1);
SET @IdUsuario = (SELECT IdRol FROM Rol WHERE NombreRol = 'Usuario' LIMIT 1);

-- ============================================================
-- INSERTAR USUARIOS
-- ============================================================

INSERT INTO Usuario (
    UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail,
    PasswordHash, Division, Position, UserStatus, ManagerId, FechaCreacion
)
VALUES
    -- ===== USUARIOS ESPECIALES =====
    ('U001', @IdHPMX, @IdAdmin, 'Carlos Mendoza Rivera', 'cmendoza@hutchison.com',
     'admin123', 'Administración', 'Administrador General', 'Active', NULL, NOW()),

    ('U002', @IdHPMX, @IdRRHH, 'Patricia López Sánchez', 'plopez@hutchison.com',
     'rrhh123', 'Recursos Humanos', 'Jefe de RRHH', 'Active', NULL, NOW()),

    -- ===== GERENTES (3) =====
    ('U003', @IdCCI, @IdGerente, 'José Luis Méndez García', 'jmendez@hutchison.com',
     'port123', 'Operaciones', 'Gerente de Operaciones', 'Active', NULL, NOW()),

    ('U004', @IdHPML, @IdGerente, 'María Fernanda Castro Ruiz', 'mcastro@hutchison.com',
     'port123', 'Logística', 'Gerente de Logística', 'Active', NULL, NOW()),

    ('U005', @IdLCTM, @IdGerente, 'Roberto Carlos Hernández', 'rhernandez@hutchison.com',
     'port123', 'Comercial', 'Gerente Comercial', 'Active', NULL, NOW()),

    -- ===== USUARIOS OPERATIVOS (27) =====
    -- CCI (3 usuarios)
    ('U006', @IdCCI, @IdUsuario, 'Ana Gabriela Torres López', 'atorres@hutchison.com',
     'port123', 'Operaciones', 'Supervisor de Área', 'Active', 'U003', NOW()),

    ('U007', @IdCCI, @IdUsuario, 'Luis Fernando Ramírez Cruz', 'lramirez@hutchison.com',
     'port123', 'Logística', 'Coordinador Logístico', 'Active', 'U003', NOW()),

    ('U008', @IdCCI, @IdUsuario, 'Carmen Sofía Díaz Morales', 'cdiaz@hutchison.com',
     'port123', 'Administración', 'Asistente Administrativo', 'Active', 'U003', NOW()),

    -- ECV (3 usuarios)
    ('U009', @IdECV, @IdUsuario, 'Miguel Ángel Vargas Soto', 'mvargas@hutchison.com',
     'port123', 'Operaciones', 'Operador de Grúa', 'Active', NULL, NOW()),

    ('U010', @IdECV, @IdUsuario, 'Daniela Patricia Flores Vega', 'dflores@hutchison.com',
     'port123', 'Seguridad', 'Inspector de Seguridad', 'Active', NULL, NOW()),

    ('U011', @IdECV, @IdUsuario, 'Javier Alejandro Guzmán Pérez', 'jguzman@hutchison.com',
     'port123', 'IT', 'Técnico de Sistemas', 'Active', NULL, NOW()),

    -- EIT (3 usuarios)
    ('U012', @IdEIT, @IdUsuario, 'Laura Melissa Rojas Delgado', 'lrojas@hutchison.com',
     'port123', 'Finanzas', 'Contador Junior', 'Active', NULL, NOW()),

    ('U013', @IdEIT, @IdUsuario, 'Diego Armando Silva Campos', 'dsilva@hutchison.com',
     'port123', 'Operaciones', 'Supervisor de Turno', 'Active', NULL, NOW()),

    ('U014', @IdEIT, @IdUsuario, 'Mónica Elizabeth Moreno Ortiz', 'mmoreno@hutchison.com',
     'port123', 'RRHH', 'Analista de Capacitación', 'Active', 'U002', NOW()),

    -- HPML (3 usuarios)
    ('U015', @IdHPML, @IdUsuario, 'Fernando José Castillo Navarro', 'fcastillo@hutchison.com',
     'port123', 'Logística', 'Coordinador de Despacho', 'Active', 'U004', NOW()),

    ('U016', @IdHPML, @IdUsuario, 'Gabriela Alejandra Reyes Santos', 'greyes@hutchison.com',
     'port123', 'Operaciones', 'Operador de Terminal', 'Active', 'U004', NOW()),

    ('U017', @IdHPML, @IdUsuario, 'Ricardo Enrique Núñez Jiménez', 'rnunez@hutchison.com',
     'port123', 'Mantenimiento', 'Técnico Mecánico', 'Active', 'U004', NOW()),

    -- HPMX (3 usuarios)
    ('U018', @IdHPMX, @IdUsuario, 'Valeria Carolina Paredes Aguilar', 'vparedes@hutchison.com',
     'port123', 'Comercial', 'Ejecutivo de Ventas', 'Active', NULL, NOW()),

    ('U019', @IdHPMX, @IdUsuario, 'Alberto Francisco Salazar Mendoza', 'asalazar@hutchison.com',
     'port123', 'Operaciones', 'Jefe de Cuadrilla', 'Active', NULL, NOW()),

    ('U020', @IdHPMX, @IdUsuario, 'Natalia Fernanda Gómez Luna', 'ngomez@hutchison.com',
     'port123', 'Administración', 'Asistente de Gerencia', 'Active', NULL, NOW()),

    -- ICAVE (3 usuarios)
    ('U021', @IdICAVE, @IdUsuario, 'Andrés Felipe Martínez Ramos', 'amartinez@hutchison.com',
     'port123', 'Operaciones', 'Operador de Montacargas', 'Active', NULL, NOW()),

    ('U022', @IdICAVE, @IdUsuario, 'Paola Cristina Herrera Valdez', 'pherrera@hutchison.com',
     'port123', 'Calidad', 'Inspector de Calidad', 'Active', NULL, NOW()),

    ('U023', @IdICAVE, @IdUsuario, 'Héctor Manuel Sánchez Ríos', 'hsanchez@hutchison.com',
     'port123', 'Logística', 'Almacenista', 'Active', NULL, NOW()),

    -- LCTM (3 usuarios)
    ('U024', @IdLCTM, @IdUsuario, 'Brenda Guadalupe Ortega Cruz', 'bortega@hutchison.com',
     'port123', 'RRHH', 'Reclutador', 'Active', 'U002', NOW()),

    ('U025', @IdLCTM, @IdUsuario, 'Omar Eduardo Velázquez Torres', 'ovelazquez@hutchison.com',
     'port123', 'Operaciones', 'Supervisor de Patio', 'Active', 'U005', NOW()),

    ('U026', @IdLCTM, @IdUsuario, 'Claudia Ximena Fuentes Maldonado', 'cfuentes@hutchison.com',
     'port123', 'Finanzas', 'Analista Financiero', 'Active', 'U005', NOW()),

    -- LCT TILH (3 usuarios)
    ('U027', @IdTILH, @IdUsuario, 'Samuel Rodrigo Estrada Pacheco', 'sestrada@hutchison.com',
     'port123', 'Operaciones', 'Coordinador Operativo', 'Active', NULL, NOW()),

    ('U028', @IdTILH, @IdUsuario, 'Karla Yadira Muñoz Ochoa', 'kmunoz@hutchison.com',
     'port123', 'Seguridad', 'Jefe de Seguridad', 'Active', NULL, NOW()),

    ('U029', @IdTILH, @IdUsuario, 'Sergio Iván Domínguez Lara', 'sdominguez@hutchison.com',
     'port123', 'IT', 'Administrador de Redes', 'Active', NULL, NOW()),

    -- TIMSA (2 usuarios)
    ('U030', @IdTIMSA, @IdUsuario, 'Diana Carolina Peña Cortés', 'dpena@hutchison.com',
     'port123', 'Operaciones', 'Operador de Reach Stacker', 'Active', NULL, NOW()),

    ('U031', @IdTIMSA, @IdUsuario, 'Marco Antonio Ávila Serrano', 'mavila@hutchison.com',
     'port123', 'Mantenimiento', 'Electricista', 'Active', NULL, NOW()),

    -- TNG (1 usuario)
    ('U032', @IdTNG, @IdUsuario, 'Erika Alejandra Campos Navarro', 'ecampos@hutchison.com',
     'port123', 'Comercial', 'Asistente Comercial', 'Active', NULL, NOW())

ON DUPLICATE KEY UPDATE
    NombreCompleto = VALUES(NombreCompleto),
    UserEmail = VALUES(UserEmail);

-- ============================================================
-- VERIFICACIÓN
-- ============================================================

SELECT '=== USUARIOS INSERTADOS ===' AS '';
SELECT
    UserId,
    NombreCompleto,
    UserEmail,
    (SELECT NombreRol FROM Rol WHERE Rol.IdRol = Usuario.IdRol) AS Rol,
    (SELECT NombreUnidad FROM UnidadDeNegocio WHERE UnidadDeNegocio.IdUnidadDeNegocio = Usuario.IdUnidadDeNegocio) AS Unidad,
    Position
FROM Usuario
ORDER BY UserId;

SELECT '=== RESUMEN POR ROL ===' AS '';
SELECT
    r.NombreRol,
    COUNT(u.IdUsuario) AS Total
FROM Rol r
LEFT JOIN Usuario u ON r.IdRol = u.IdRol
GROUP BY r.NombreRol
ORDER BY r.IdRol;

SELECT '=== RESUMEN POR UNIDAD ===' AS '';
SELECT
    un.NombreUnidad,
    COUNT(u.IdUsuario) AS Total
FROM UnidadDeNegocio un
LEFT JOIN Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
GROUP BY un.NombreUnidad
ORDER BY Total DESC;
