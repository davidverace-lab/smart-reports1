-- ============================================
-- SMART REPORTS - 30 USUARIOS DE EJEMPLO REALES
-- Instituto Hutchison Ports v2.0
-- ============================================

USE SmartReports;
GO

-- Insertar 30 usuarios reales con datos completos
DELETE FROM instituto_UsuarioModulo WHERE UsuarioID > 2; -- Mantener admin y rrhh
DELETE FROM instituto_Usuario WHERE UsuarioID > 2;
GO

-- Resetear identity
DBCC CHECKIDENT ('instituto_Usuario', RESEED, 2);
GO

INSERT INTO instituto_Usuario (Nombre, Email, Departamento, Cargo, UnidadNegocioID, RolID, Activo, Contraseña, FechaIngreso)
VALUES
    -- Terminal Portuaria 1 (6 usuarios)
    ('Juan Carlos Méndez', 'jmendez@hutchison.com', 'Operaciones', 'Supervisor de Operaciones', 1, 3, 1, 'port123', '2022-03-15'),
    ('María Elena Soto', 'msoto@hutchison.com', 'Operaciones', 'Operador de Grúa Pórtico', 1, 4, 1, 'port123', '2021-07-22'),
    ('Roberto Vargas', 'rvargas@hutchison.com', 'Logística', 'Coordinador Logístico', 1, 4, 1, 'port123', '2023-01-10'),
    ('Ana Patricia Rojas', 'arojas@hutchison.com', 'Mantenimiento', 'Técnico de Mantenimiento', 1, 4, 1, 'port123', '2022-09-05'),
    ('Carlos Enrique Díaz', 'cdiaz@hutchison.com', 'Seguridad', 'Jefe de Seguridad Industrial', 1, 3, 1, 'port123', '2020-11-30'),
    ('Lucía Fernández', 'lfernandez@hutchison.com', 'Administración', 'Asistente Administrativa', 1, 4, 1, 'port123', '2023-04-12'),

    -- Terminal Portuaria 2 (5 usuarios)
    ('Pedro Antonio Silva', 'psilva@hutchison.com', 'Operaciones', 'Jefe de Operaciones', 2, 3, 1, 'port123', '2021-02-18'),
    ('Carmen Rosa López', 'clopez@hutchison.com', 'Operaciones', 'Operador de Reach Stacker', 2, 4, 1, 'port123', '2022-06-25'),
    ('Diego Alejandro Cruz', 'dcruz@hutchison.com', 'Calidad', 'Inspector de Calidad', 2, 4, 1, 'port123', '2023-02-14'),
    ('Valentina Gómez', 'vgomez@hutchison.com', 'Comercial', 'Ejecutiva Comercial', 2, 4, 1, 'port123', '2022-10-08'),
    ('Javier Morales', 'jmorales@hutchison.com', 'Mantenimiento', 'Supervisor de Mantenimiento', 2, 3, 1, 'port123', '2021-12-01'),

    -- Logística y Almacenamiento (5 usuarios)
    ('Sandra Patricia Herrera', 'sherrera@hutchison.com', 'Logística', 'Gerente de Logística', 3, 3, 1, 'port123', '2020-08-20'),
    ('Miguel Ángel Ramírez', 'mramirez@hutchison.com', 'Almacenes', 'Jefe de Almacén', 3, 3, 1, 'port123', '2021-05-16'),
    ('Patricia Jiménez', 'pjimenez@hutchison.com', 'Inventario', 'Analista de Inventarios', 3, 4, 1, 'port123', '2022-11-22'),
    ('Fernando Castro', 'fcastro@hutchison.com', 'Distribución', 'Coordinador de Distribución', 3, 4, 1, 'port123', '2023-03-07'),
    ('Mónica Ortiz', 'mortiz@hutchison.com', 'Planificación', 'Planificador Logístico', 3, 4, 1, 'port123', '2022-07-19'),

    -- Operaciones Terrestres (4 usuarios)
    ('Andrés Felipe Torres', 'atorres@hutchison.com', 'Patio', 'Supervisor de Patio', 4, 3, 1, 'port123', '2021-09-12'),
    ('Gabriela Martínez', 'gmartinez@hutchison.com', 'Transporte', 'Coordinadora de Transporte', 4, 4, 1, 'port123', '2022-12-05'),
    ('Ricardo Sánchez', 'rsanchez@hutchison.com', 'Operaciones Terrestres', 'Operador de Montacargas', 4, 4, 1, 'port123', '2023-05-20'),
    ('Diana Carolina Pérez', 'dperez@hutchison.com', 'Despacho', 'Analista de Despacho', 4, 4, 1, 'port123', '2022-08-14'),

    -- Administración Central (3 usuarios)
    ('Luis Fernando Ríos', 'lrios@hutchison.com', 'Finanzas', 'Contador General', 5, 3, 1, 'port123', '2020-06-10'),
    ('Carolina Gutiérrez', 'cgutierrez@hutchison.com', 'Compras', 'Jefe de Compras', 5, 3, 1, 'port123', '2021-10-28'),
    ('Hernán Paredes', 'hparedes@hutchison.com', 'Administración', 'Asistente Contable', 5, 4, 1, 'port123', '2023-01-25'),

    -- Recursos Humanos (3 usuarios)
    ('Daniela Campos', 'dcampos@hutchison.com', 'Recursos Humanos', 'Analista de Selección', 6, 4, 1, 'port123', '2022-04-15'),
    ('Sergio Mendoza', 'smendoza@hutchison.com', 'Recursos Humanos', 'Especialista en Capacitación', 6, 4, 1, 'port123', '2021-11-08'),
    ('Isabel Reyes', 'ireyes@hutchison.com', 'Recursos Humanos', 'Coordinadora de Nómina', 6, 4, 1, 'port123', '2023-02-20'),

    -- Tecnología e Innovación (2 usuarios)
    ('Esteban Varela', 'evarela@hutchison.com', 'Sistemas', 'Analista de Sistemas', 7, 4, 1, 'port123', '2022-09-10'),
    ('Claudia Romero', 'cromero@hutchison.com', 'Soporte Técnico', 'Técnico de Soporte', 7, 4, 1, 'port123', '2023-03-18'),

    -- Seguridad y Medio Ambiente (2 usuarios)
    ('Oscar Mauricio León', 'oleon@hutchison.com', 'Seguridad Industrial', 'Coordinador SST', 8, 3, 1, 'port123', '2021-08-05'),
    ('Verónica Navarro', 'vnavarro@hutchison.com', 'Medio Ambiente', 'Analista Ambiental', 8, 4, 1, 'port123', '2022-05-30');

PRINT '✓ 30 usuarios insertados';
GO

-- Insertar progreso de módulos para los 30 usuarios
-- Cada usuario tendrá entre 2-8 módulos completados con fechas y calificaciones realistas

-- Usuario 3: Juan Carlos Méndez (8 módulos completados)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (3, 1, 100, 1, '2024-01-15', '2024-01-25', 92),
    (3, 2, 100, 1, '2024-02-01', '2024-02-10', 88),
    (3, 3, 100, 1, '2024-02-15', '2024-02-28', 95),
    (3, 4, 100, 1, '2024-03-05', '2024-03-18', 90),
    (3, 5, 100, 1, '2024-04-01', '2024-04-12', 87),
    (3, 6, 100, 1, '2024-05-10', '2024-05-22', 93),
    (3, 7, 100, 1, '2024-06-01', '2024-06-15', 91),
    (3, 8, 100, 1, '2024-07-05', '2024-07-20', 89);

-- Usuario 4: María Elena Soto (6 módulos completados)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (4, 1, 100, 1, '2024-01-20', '2024-02-02', 85),
    (4, 2, 100, 1, '2024-02-10', '2024-02-25', 83),
    (4, 3, 100, 1, '2024-03-01', '2024-03-15', 88),
    (4, 4, 100, 1, '2024-04-05', '2024-04-20', 86),
    (4, 5, 100, 1, '2024-05-01', '2024-05-18', 82),
    (4, 6, 100, 1, '2024-06-10', '2024-06-28', 90);

-- Usuario 5: Roberto Vargas (7 módulos completados)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (5, 1, 100, 1, '2024-01-10', '2024-01-22', 91),
    (5, 2, 100, 1, '2024-02-05', '2024-02-18', 89),
    (5, 3, 100, 1, '2024-03-02', '2024-03-16', 94),
    (5, 4, 100, 1, '2024-04-01', '2024-04-15', 88),
    (5, 5, 100, 1, '2024-05-05', '2024-05-20', 85),
    (5, 6, 100, 1, '2024-06-15', '2024-06-30', 92),
    (5, 7, 100, 1, '2024-07-10', '2024-07-25', 87);

-- Usuario 6: Ana Patricia Rojas (5 módulos completados)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (6, 1, 100, 1, '2024-02-01', '2024-02-15', 84),
    (6, 2, 100, 1, '2024-03-01', '2024-03-14', 86),
    (6, 3, 100, 1, '2024-04-05', '2024-04-20', 88),
    (6, 4, 100, 1, '2024-05-10', '2024-05-25', 83),
    (6, 5, 100, 1, '2024-06-15', '2024-07-02', 90);

-- Usuario 7: Carlos Enrique Díaz (8 módulos - supervisor experimentado)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (7, 1, 100, 1, '2024-01-08', '2024-01-20', 96),
    (7, 2, 100, 1, '2024-01-25', '2024-02-08', 94),
    (7, 3, 100, 1, '2024-02-12', '2024-02-26', 97),
    (7, 4, 100, 1, '2024-03-01', '2024-03-14', 95),
    (7, 5, 100, 1, '2024-03-20', '2024-04-05', 93),
    (7, 6, 100, 1, '2024-04-10', '2024-04-25', 98),
    (7, 7, 100, 1, '2024-05-01', '2024-05-16', 96),
    (7, 8, 100, 1, '2024-05-22', '2024-06-08', 94);

-- Usuario 8: Lucía Fernández (4 módulos - nuevo en la empresa)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (8, 1, 100, 1, '2024-04-20', '2024-05-05', 82),
    (8, 2, 100, 1, '2024-05-12', '2024-05-28', 85),
    (8, 3, 100, 1, '2024-06-05', '2024-06-22', 87),
    (8, 4, 100, 1, '2024-07-01', '2024-07-18', 84);

-- Continuar con los demás usuarios (9-32)...
-- Usuario 9: Pedro Antonio Silva (7 módulos)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (9, 1, 100, 1, '2024-01-12', '2024-01-28', 93),
    (9, 2, 100, 1, '2024-02-05', '2024-02-20', 91),
    (9, 3, 100, 1, '2024-03-01', '2024-03-18', 95),
    (9, 4, 100, 1, '2024-04-02', '2024-04-17', 89),
    (9, 5, 100, 1, '2024-05-05', '2024-05-22', 92),
    (9, 6, 100, 1, '2024-06-10', '2024-06-26', 94),
    (9, 7, 100, 1, '2024-07-08', '2024-07-24', 90);

-- Usuario 10: Carmen Rosa López (5 módulos)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (10, 1, 100, 1, '2024-02-15', '2024-03-02', 86),
    (10, 2, 100, 1, '2024-03-10', '2024-03-26', 84),
    (10, 3, 100, 1, '2024-04-08', '2024-04-25', 88),
    (10, 4, 100, 1, '2024-05-12', '2024-05-30', 85),
    (10, 5, 100, 1, '2024-06-18', '2024-07-05', 89);

-- Usuario 11: Diego Alejandro Cruz (6 módulos)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (11, 1, 100, 1, '2024-03-01', '2024-03-16', 87),
    (11, 2, 100, 1, '2024-03-22', '2024-04-08', 89),
    (11, 3, 100, 1, '2024-04-15', '2024-05-02', 91),
    (11, 4, 100, 1, '2024-05-10', '2024-05-26', 86),
    (11, 5, 100, 1, '2024-06-05', '2024-06-22', 90),
    (11, 6, 100, 1, '2024-07-01', '2024-07-18', 88);

-- Usuario 12: Valentina Gómez (4 módulos)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (12, 1, 100, 1, '2024-03-05', '2024-03-22', 83),
    (12, 2, 100, 1, '2024-04-02', '2024-04-20', 85),
    (12, 3, 100, 1, '2024-05-08', '2024-05-26', 87),
    (12, 4, 100, 1, '2024-06-12', '2024-06-30', 84);

-- Usuario 13: Javier Morales (8 módulos - supervisor experimentado)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (13, 1, 100, 1, '2024-01-05', '2024-01-18', 95),
    (13, 2, 100, 1, '2024-01-24', '2024-02-08', 93),
    (13, 3, 100, 1, '2024-02-14', '2024-03-01', 96),
    (13, 4, 100, 1, '2024-03-08', '2024-03-22', 94),
    (13, 5, 100, 1, '2024-04-01', '2024-04-16', 92),
    (13, 6, 100, 1, '2024-04-24', '2024-05-10', 97),
    (13, 7, 100, 1, '2024-05-18', '2024-06-04', 95),
    (13, 8, 100, 1, '2024-06-12', '2024-06-28', 93);

-- Usuarios 14-32: Similar pattern con 3-7 módulos cada uno
-- Usuario 14: Sandra Patricia Herrera (7 módulos - Gerente)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (14, 1, 100, 1, '2024-01-10', '2024-01-24', 94),
    (14, 2, 100, 1, '2024-02-01', '2024-02-16', 92),
    (14, 3, 100, 1, '2024-02-22', '2024-03-10', 95),
    (14, 4, 100, 1, '2024-03-18', '2024-04-03', 91),
    (14, 5, 100, 1, '2024-04-10', '2024-04-26', 93),
    (14, 6, 100, 1, '2024-05-05', '2024-05-22', 96),
    (14, 7, 100, 1, '2024-06-02', '2024-06-20', 94);

-- Usuario 15-32: Generar patrón similar
-- Por brevedad, aquí van algunos ejemplos más representativos

-- Usuario 15: Miguel Ángel Ramírez (6 módulos)
INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
VALUES
    (15, 1, 100, 1, '2024-01-18', '2024-02-02', 88),
    (15, 2, 100, 1, '2024-02-10', '2024-02-26', 86),
    (15, 3, 100, 1, '2024-03-05', '2024-03-22', 90),
    (15, 4, 100, 1, '2024-04-01', '2024-04-18', 87),
    (15, 5, 100, 1, '2024-05-08', '2024-05-25', 89),
    (15, 6, 100, 1, '2024-06-15', '2024-07-02', 91);

-- Resto de usuarios (16-32) con patrón similar
-- Total: ~180 registros de módulos completados
DECLARE @i INT = 16;
DECLARE @modulos INT;
DECLARE @calif INT;
DECLARE @modId INT;

WHILE @i <= 32
BEGIN
    SET @modulos = 3 + (ABS(CHECKSUM(NEWID())) % 6); -- 3-8 módulos por usuario
    SET @modId = 1;

    WHILE @modId <= @modulos
    BEGIN
        SET @calif = 80 + (ABS(CHECKSUM(NEWID())) % 18); -- Calificación 80-98

        INSERT INTO instituto_UsuarioModulo (UsuarioID, ModuloID, Progreso, Aprobado, FechaInicio, FechaFinalizacion, CalificacionFinal)
        VALUES (
            @i,
            @modId,
            100,
            1,
            DATEADD(day, (@modId - 1) * 20, DATEADD(month, (@i % 6), '2024-01-01')),
            DATEADD(day, (@modId - 1) * 20 + 15, DATEADD(month, (@i % 6), '2024-01-01')),
            @calif
        );

        SET @modId = @modId + 1;
    END

    SET @i = @i + 1;
END

PRINT '✓ Módulos asignados a todos los usuarios';
PRINT '✓ Total ~180+ registros de módulos completados';
GO

PRINT '============================================';
PRINT '✅ 30 USUARIOS DE EJEMPLO CREADOS';
PRINT '============================================';
PRINT 'Usuarios: jmendez@hutchison.com (y 29 más)';
PRINT 'Contraseña: port123 (todos)';
PRINT 'Módulos completados: 3-8 por usuario';
PRINT 'Calificaciones: 80-98 puntos';
PRINT 'Fechas: Enero-Julio 2024';
