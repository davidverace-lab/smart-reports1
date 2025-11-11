-- ============================================
-- SMART REPORTS - MÓDULOS Y PROGRESO
-- Adaptado al esquema REAL del usuario
-- ============================================

USE SmartReports;
GO

PRINT '=== INSERTANDO MÓDULOS ===';

-- ============================================
-- 1. INSERTAR MÓDULOS DE CAPACITACIÓN
-- ============================================

INSERT INTO Modulo (NombreModulo, FechaInicioModulo, FechaCierre, Descripcion, Activo)
VALUES
    ('Seguridad Industrial Básica', '2024-01-01', '2024-12-31', 'Curso básico de seguridad industrial y prevención de riesgos', 1),
    ('Operación de Equipos Portuarios', '2024-01-01', '2024-12-31', 'Capacitación en operación de grúas, reach stackers y montacargas', 1),
    ('Manejo de Cargas Peligrosas', '2024-01-01', '2024-12-31', 'Normativas y procedimientos para manejo seguro de cargas peligrosas', 1),
    ('Gestión Logística Portuaria', '2024-01-01', '2024-12-31', 'Fundamentos de logística y gestión de operaciones portuarias', 1),
    ('Sistemas de Información Portuaria', '2024-01-01', '2024-12-31', 'Uso de sistemas informáticos para gestión portuaria', 1),
    ('Atención al Cliente', '2024-01-01', '2024-12-31', 'Técnicas de servicio al cliente en el sector portuario', 1),
    ('Liderazgo y Trabajo en Equipo', '2024-01-01', '2024-12-31', 'Desarrollo de habilidades de liderazgo y colaboración', 1),
    ('Normativa Aduanera y Comercio Exterior', '2024-01-01', '2024-12-31', 'Regulaciones aduaneras y de comercio internacional', 1);

PRINT '✓ 8 Módulos de capacitación insertados';
GO

PRINT '=== INSERTANDO PROGRESO DE MÓDULOS ===';

-- ============================================
-- 2. INSERTAR PROGRESO PARA LOS 30 USUARIOS
-- ============================================

-- Usuario U003: Juan Carlos Méndez (Gerente) - 8 módulos completados
INSERT INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento, FechaFinalizacion)
VALUES
    ('U003', 1, 'Completado', '2024-01-15', '2024-02-15', '2024-01-25'),
    ('U003', 2, 'Completado', '2024-02-01', '2024-03-01', '2024-02-10'),
    ('U003', 3, 'Completado', '2024-02-15', '2024-03-15', '2024-02-28'),
    ('U003', 4, 'Completado', '2024-03-05', '2024-04-05', '2024-03-18'),
    ('U003', 5, 'Completado', '2024-04-01', '2024-05-01', '2024-04-12'),
    ('U003', 6, 'Completado', '2024-05-10', '2024-06-10', '2024-05-22'),
    ('U003', 7, 'Completado', '2024-06-01', '2024-07-01', '2024-06-15'),
    ('U003', 8, 'Completado', '2024-07-05', '2024-08-05', '2024-07-20');

-- Usuario U004: María Elena Soto - 6 módulos completados
INSERT INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento, FechaFinalizacion)
VALUES
    ('U004', 1, 'Completado', '2024-01-20', '2024-02-20', '2024-02-02'),
    ('U004', 2, 'Completado', '2024-02-10', '2024-03-10', '2024-02-25'),
    ('U004', 3, 'Completado', '2024-03-01', '2024-04-01', '2024-03-15'),
    ('U004', 4, 'Completado', '2024-04-05', '2024-05-05', '2024-04-20'),
    ('U004', 5, 'Completado', '2024-05-01', '2024-06-01', '2024-05-18'),
    ('U004', 6, 'Completado', '2024-06-10', '2024-07-10', '2024-06-28');

-- Usuario U005: Roberto Vargas - 7 módulos completados
INSERT INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento, FechaFinalizacion)
VALUES
    ('U005', 1, 'Completado', '2024-01-10', '2024-02-10', '2024-01-22'),
    ('U005', 2, 'Completado', '2024-02-05', '2024-03-05', '2024-02-18'),
    ('U005', 3, 'Completado', '2024-03-02', '2024-04-02', '2024-03-16'),
    ('U005', 4, 'Completado', '2024-04-01', '2024-05-01', '2024-04-15'),
    ('U005', 5, 'Completado', '2024-05-05', '2024-06-05', '2024-05-20'),
    ('U005', 6, 'Completado', '2024-06-15', '2024-07-15', '2024-06-30'),
    ('U005', 7, 'Completado', '2024-07-10', '2024-08-10', '2024-07-25');

-- Usuario U006: Ana Patricia Rojas (Gerente) - 8 módulos completados
INSERT INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento, FechaFinalizacion)
VALUES
    ('U006', 1, 'Completado', '2024-01-08', '2024-02-08', '2024-01-20'),
    ('U006', 2, 'Completado', '2024-01-25', '2024-02-25', '2024-02-08'),
    ('U006', 3, 'Completado', '2024-02-12', '2024-03-12', '2024-02-26'),
    ('U006', 4, 'Completado', '2024-03-01', '2024-04-01', '2024-03-14'),
    ('U006', 5, 'Completado', '2024-03-20', '2024-04-20', '2024-04-05'),
    ('U006', 6, 'Completado', '2024-04-10', '2024-05-10', '2024-04-25'),
    ('U006', 7, 'Completado', '2024-05-01', '2024-06-01', '2024-05-16'),
    ('U006', 8, 'Completado', '2024-05-22', '2024-06-22', '2024-06-08');

-- Continuar con más usuarios...
-- Por brevedad, generar patrón para usuarios restantes

DECLARE @userId VARCHAR(50);
DECLARE @moduloId INT;
DECLARE @numModulos INT;
DECLARE @i INT = 7; -- Empezar desde U007

WHILE @i <= 32
BEGIN
    SET @userId = 'U' + RIGHT('000' + CAST(@i AS VARCHAR), 3);
    SET @numModulos = 3 + (ABS(CHECKSUM(NEWID())) % 6); -- 3-8 módulos
    SET @moduloId = 1;

    WHILE @moduloId <= @numModulos
    BEGIN
        INSERT INTO ProgresoModulo (UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaVencimiento, FechaFinalizacion)
        VALUES (
            @userId,
            @moduloId,
            'Completado',
            DATEADD(day, (@moduloId - 1) * 20, DATEADD(month, (@i % 6), '2024-01-01')),
            DATEADD(day, (@moduloId - 1) * 20 + 30, DATEADD(month, (@i % 6), '2024-01-01')),
            DATEADD(day, (@moduloId - 1) * 20 + 15, DATEADD(month, (@i % 6), '2024-01-01'))
        );

        SET @moduloId = @moduloId + 1;
    END

    SET @i = @i + 1;
END

PRINT '✓ Progreso asignado a todos los usuarios';
PRINT '✓ Total ~150+ registros de módulos completados';
GO

-- ============================================
-- 3. INSERTAR EVALUACIONES Y RESULTADOS
-- ============================================

PRINT '=== INSERTANDO EVALUACIONES ===';

-- Crear evaluación para cada módulo
INSERT INTO Evaluacion (IdModulo, NombreEvaluacion, PuntajeMinimoAprobatorio)
SELECT
    IdModulo,
    'Evaluación Final - ' + NombreModulo,
    70.00
FROM Modulo;

PRINT '✓ 8 Evaluaciones creadas (1 por módulo)';
GO

-- Insertar resultados de evaluaciones para usuarios con progreso
INSERT INTO ResultadoEvaluacion (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado, IntentoNumero, FechaRealizacion)
SELECT
    pm.IdInscripcion,
    e.IdEvaluacion,
    80 + (ABS(CHECKSUM(NEWID())) % 18) AS PuntajeObtenido, -- 80-98
    1 AS Aprobado,
    1 AS IntentoNumero,
    pm.FechaFinalizacion
FROM ProgresoModulo pm
INNER JOIN Evaluacion e ON pm.IdModulo = e.IdModulo
WHERE pm.EstatusModulo = 'Completado' AND pm.FechaFinalizacion IS NOT NULL;

PRINT '✓ Resultados de evaluaciones insertados';
GO

PRINT '';
PRINT '============================================';
PRINT '✅ MÓDULOS Y PROGRESO CONFIGURADOS';
PRINT '============================================';
PRINT '';
PRINT 'Módulos: 8';
PRINT 'Progreso registrado: ~150+ (3-8 por usuario)';
PRINT 'Evaluaciones: 8 (1 por módulo)';
PRINT 'Resultados: ~150+';
PRINT '';
PRINT 'Estados: Completado';
PRINT 'Calificaciones: 80-98 puntos';
PRINT 'Período: Enero-Julio 2024';
