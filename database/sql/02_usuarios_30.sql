-- ============================================
-- SMART REPORTS - 30 USUARIOS DE EJEMPLO
-- Adaptado al esquema REAL del usuario
-- ============================================

USE SmartReports;
GO

PRINT '=== INSERTANDO 30 USUARIOS DE EJEMPLO ===';

-- Obtener IDs de roles
DECLARE @IdAdmin INT = (SELECT IdRol FROM Rol WHERE NombreRol = 'Administrador');
DECLARE @IdRRHH INT = (SELECT IdRol FROM Rol WHERE NombreRol = 'Recursos Humanos');
DECLARE @IdGerente INT = (SELECT IdRol FROM Rol WHERE NombreRol = 'Gerente');
DECLARE @IdUsuario INT = (SELECT IdRol FROM Rol WHERE NombreRol = 'Usuario');

-- Obtener IDs de unidades
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

-- Nota: PasswordHash en texto plano para desarrollo
-- En producción usar HASHBYTES('SHA2_256', 'password')

-- ============================================
-- USUARIOS ADMINISTRADORES Y RRHH (2)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U001', @IdHPMX, @IdAdmin, 'Carlos Mendoza Rivera', 'cmendoza@hutchison.com', 'admin123', 'Corporativo', 'Ejecutivo', 'TI', 'Director de Sistemas', 'Active', 'Administradores', 'Ciudad de México'),
    ('U002', @IdHPMX, @IdRRHH, 'Patricia López Sánchez', 'plopez@hutchison.com', 'rrhh123', 'Corporativo', 'Gerencial', 'RRHH', 'Gerente de Recursos Humanos', 'Active', 'RRHH', 'Ciudad de México');

PRINT '✓ 2 usuarios admin/RRHH insertados';
GO

-- ============================================
-- USUARIOS CCI (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U003', @IdCCI, @IdGerente, 'Juan Carlos Méndez Torres', 'jmendez@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones', 'Gerente de Operaciones', 'Active', 'Gerencia', 'Manzanillo'),
    ('U004', @IdCCI, @IdUsuario, 'María Elena Soto Ramírez', 'msoto@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Operaciones', 'Operador de Grúa Pórtico', 'Active', 'Operadores', 'Manzanillo'),
    ('U005', @IdCCI, @IdUsuario, 'Roberto Vargas Luna', 'rvargas@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Administración', 'Coordinador Administrativo', 'Active', 'Administrativos', 'Manzanillo');

PRINT '✓ 3 usuarios CCI insertados';
GO

-- ============================================
-- USUARIOS ECV (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U006', @IdECV, @IdGerente, 'Ana Patricia Rojas Morales', 'arojas@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Logística', 'Jefe de Logística', 'Active', 'Gerencia', 'Ensenada'),
    ('U007', @IdECV, @IdUsuario, 'Diego Alejandro Cruz Vega', 'dcruz@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Operaciones Portuarias', 'Operador de Reach Stacker', 'Active', 'Operadores', 'Ensenada'),
    ('U008', @IdECV, @IdUsuario, 'Valentina Gómez Herrera', 'vgomez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Comercial', 'Ejecutiva Comercial', 'Active', 'Ventas', 'Ensenada');

PRINT '✓ 3 usuarios ECV insertados';
GO

-- ============================================
-- USUARIOS EIT (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U009', @IdEIT, @IdGerente, 'Carlos Enrique Díaz Ortiz', 'cdiaz@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones Terrestres', 'Gerente de Operaciones', 'Active', 'Gerencia', 'Veracruz'),
    ('U010', @IdEIT, @IdUsuario, 'Lucía Fernández Castro', 'lfernandez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Tecnología', 'Analista de Sistemas', 'Active', 'TI', 'Veracruz'),
    ('U011', @IdEIT, @IdUsuario, 'Fernando Castro Jiménez', 'fcastro@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Finanzas', 'Contador', 'Active', 'Finanzas', 'Veracruz');

PRINT '✓ 3 usuarios EIT insertados';
GO

-- ============================================
-- USUARIOS HPML (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U012', @IdHPML, @IdGerente, 'Pedro Antonio Silva Navarro', 'psilva@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Terminal Portuaria', 'Jefe de Terminal', 'Active', 'Gerencia', 'Lázaro Cárdenas'),
    ('U013', @IdHPML, @IdUsuario, 'Carmen Rosa López Reyes', 'clopez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Logística y Almacenamiento', 'Coordinador de Almacén', 'Active', 'Logística', 'Lázaro Cárdenas'),
    ('U014', @IdHPML, @IdUsuario, 'Javier Morales Gutiérrez', 'jmorales@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Seguridad', 'Inspector de Seguridad', 'Active', 'Seguridad', 'Lázaro Cárdenas');

PRINT '✓ 3 usuarios HPML insertados';
GO

-- ============================================
-- USUARIOS HPMX (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U015', @IdHPMX, @IdGerente, 'Sandra Patricia Herrera Díaz', 'sherrera@hutchison.com', 'port123', 'Corporativo', 'Gerencial', 'Operaciones', 'Gerente de Operaciones', 'Active', 'Gerencia', 'Ciudad de México'),
    ('U016', @IdHPMX, @IdUsuario, 'Miguel Ángel Ramírez Flores', 'mramirez@hutchison.com', 'port123', 'Corporativo', 'Operativo', 'Administración', 'Asistente Administrativo', 'Active', 'Administrativos', 'Ciudad de México'),
    ('U017', @IdHPMX, @IdUsuario, 'Patricia Jiménez Mendoza', 'pjimenez@hutchison.com', 'port123', 'Corporativo', 'Operativo', 'Comercial', 'Ejecutivo de Ventas', 'Active', 'Ventas', 'Ciudad de México');

PRINT '✓ 3 usuarios HPMX insertados';
GO

-- ============================================
-- USUARIOS ICAVE (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U018', @IdICAVE, @IdGerente, 'Andrés Felipe Torres Ramos', 'atorres@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones Portuarias', 'Supervisor de Patio', 'Active', 'Gerencia', 'Veracruz'),
    ('U019', @IdICAVE, @IdUsuario, 'Gabriela Martínez Silva', 'gmartinez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Mantenimiento', 'Técnico de Mantenimiento', 'Active', 'Mantenimiento', 'Veracruz'),
    ('U020', @IdICAVE, @IdUsuario, 'Ricardo Sánchez López', 'rsanchez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Medio Ambiente', 'Analista Ambiental', 'Active', 'Medio Ambiente', 'Veracruz');

PRINT '✓ 3 usuarios ICAVE insertados';
GO

-- ============================================
-- USUARIOS LCTM (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U021', @IdLCTM, @IdGerente, 'Diana Carolina Pérez Vargas', 'dperez@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Terminal de Contenedores', 'Jefe de Terminal', 'Active', 'Gerencia', 'Lázaro Cárdenas'),
    ('U022', @IdLCTM, @IdUsuario, 'Luis Fernando Ríos Cruz', 'lrios@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Logística', 'Planificador Logístico', 'Active', 'Logística', 'Lázaro Cárdenas'),
    ('U023', @IdLCTM, @IdUsuario, 'Carolina Gutiérrez Moreno', 'cgutierrez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Administración', 'Contador', 'Active', 'Finanzas', 'Lázaro Cárdenas');

PRINT '✓ 3 usuarios LCTM insertados';
GO

-- ============================================
-- USUARIOS LCT TILH (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U024', @IdLCTTILH, @IdGerente, 'Hernán Paredes Salazar', 'hparedes@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones', 'Gerente de Operaciones', 'Active', 'Gerencia', 'Tuxpan'),
    ('U025', @IdLCTTILH, @IdUsuario, 'Daniela Campos Romero', 'dcampos@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Recursos Humanos', 'Analista de Selección', 'Active', 'RRHH', 'Tuxpan'),
    ('U026', @IdLCTTILH, @IdUsuario, 'Sergio Mendoza Torres', 'smendoza@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Tecnología', 'Soporte Técnico', 'Active', 'TI', 'Tuxpan');

PRINT '✓ 3 usuarios LCT TILH insertados';
GO

-- ============================================
-- USUARIOS TIMSA (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U027', @IdTIMSA, @IdGerente, 'Isabel Reyes Fernández', 'ireyes@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones Terrestres', 'Supervisor de Patio', 'Active', 'Gerencia', 'Tuxpan'),
    ('U028', @IdTIMSA, @IdUsuario, 'Esteban Varela Castillo', 'evarela@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Administración', 'Asistente Contable', 'Active', 'Finanzas', 'Tuxpan'),
    ('U029', @IdTIMSA, @IdUsuario, 'Claudia Romero Aguilar', 'cromero@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Mantenimiento', 'Técnico de Mantenimiento', 'Active', 'Mantenimiento', 'Tuxpan');

PRINT '✓ 3 usuarios TIMSA insertados';
GO

-- ============================================
-- USUARIOS TNG (3 usuarios)
-- ============================================

INSERT INTO Usuario (UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo, Nivel, Division, Position, UserStatus, Grupo, Ubicacion)
VALUES
    ('U030', @IdTNG, @IdGerente, 'Oscar Mauricio León Parra', 'oleon@hutchison.com', 'port123', 'Operacional', 'Gerencial', 'Operaciones', 'Jefe de Operaciones', 'Active', 'Gerencia', 'Altamira'),
    ('U031', @IdTNG, @IdUsuario, 'Verónica Navarro Delgado', 'vnavarro@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Comercial', 'Ejecutiva de Ventas', 'Active', 'Ventas', 'Altamira'),
    ('U032', @IdTNG, @IdUsuario, 'Alberto González Méndez', 'agonzalez@hutchison.com', 'port123', 'Operacional', 'Operativo', 'Recursos Humanos', 'Coordinador de Nómina', 'Active', 'RRHH', 'Altamira');

PRINT '✓ 3 usuarios TNG insertados';
GO

PRINT '';
PRINT '============================================';
PRINT '✅ 32 USUARIOS CREADOS EXITOSAMENTE';
PRINT '============================================';
PRINT '';
PRINT 'Distribución:';
PRINT '  - Administradores: 1';
PRINT '  - RRHH: 1';
PRINT '  - Gerentes: 10 (1 por unidad)';
PRINT '  - Usuarios: 20';
PRINT '';
PRINT 'Por Unidad de Negocio:';
PRINT '  - CCI: 3 usuarios';
PRINT '  - ECV: 3 usuarios';
PRINT '  - EIT: 3 usuarios';
PRINT '  - HPML: 3 usuarios';
PRINT '  - HPMX: 3 usuarios (+ admin y rrhh)';
PRINT '  - ICAVE: 3 usuarios';
PRINT '  - LCTM: 3 usuarios';
PRINT '  - LCT TILH: 3 usuarios';
PRINT '  - TIMSA: 3 usuarios';
PRINT '  - TNG: 3 usuarios';
PRINT '';
PRINT 'Contraseñas:';
PRINT '  - Admin: admin123';
PRINT '  - RRHH: rrhh123';
PRINT '  - Otros: port123';
