-- ═══════════════════════════════════════════════════════════════════════════
-- FIX 2: Migrar datos de Division a Departamento (OPCIONAL)
-- Ejecutar ANTES de eliminar el campo Division si quieres preservar los datos
-- ═══════════════════════════════════════════════════════════════════════════

USE InstitutoHutchison;
GO

PRINT '═══════════════════════════════════════════════════════════════════════';
PRINT 'MIGRACIÓN: Division → Departamento';
PRINT '═══════════════════════════════════════════════════════════════════════';
GO

-- Paso 1: Crear departamentos desde valores únicos de Division
PRINT 'Paso 1: Creando departamentos desde valores de Division...';
GO

INSERT INTO instituto_Departamento (IdUnidadDeNegocio, NombreDepartamento, Descripcion, Activo)
SELECT DISTINCT
    6 AS IdUnidadDeNegocio,  -- TNG por defecto (puedes cambiar)
    u.Division AS NombreDepartamento,
    'Departamento importado desde campo Division' AS Descripcion,
    1 AS Activo
FROM instituto_Usuario u
WHERE u.Division IS NOT NULL
  AND u.Division != ''
  AND NOT EXISTS (
      SELECT 1 FROM instituto_Departamento d
      WHERE d.NombreDepartamento = u.Division
  );

DECLARE @DepartamentosCreados INT = @@ROWCOUNT;
PRINT '✅ Departamentos creados: ' + CAST(@DepartamentosCreados AS VARCHAR);
GO

-- Paso 2: Actualizar IdDepartamento de usuarios
PRINT 'Paso 2: Actualizando IdDepartamento de usuarios...';
GO

UPDATE u
SET u.IdDepartamento = d.IdDepartamento
FROM instituto_Usuario u
INNER JOIN instituto_Departamento d ON d.NombreDepartamento = u.Division
WHERE u.Division IS NOT NULL
  AND u.Division != ''
  AND u.IdDepartamento IS NULL;  -- Solo si no tiene departamento asignado

DECLARE @UsuariosActualizados INT = @@ROWCOUNT;
PRINT '✅ Usuarios actualizados: ' + CAST(@UsuariosActualizados AS VARCHAR);
GO

-- Paso 3: Reporte de usuarios con conflictos
PRINT 'Paso 3: Verificando conflictos...';
GO

SELECT
    u.UserId,
    u.NombreCompleto,
    u.Division AS DivisionAntigua,
    d.NombreDepartamento AS DepartamentoActual,
    'CONFLICTO: Tiene ambos campos' AS Nota
FROM instituto_Usuario u
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
WHERE u.Division IS NOT NULL
  AND u.Division != ''
  AND u.IdDepartamento IS NOT NULL
  AND u.Division != d.NombreDepartamento;

IF @@ROWCOUNT > 0
BEGIN
    PRINT '⚠️  Hay usuarios con valores diferentes en Division y Departamento';
    PRINT '    Revisa el resultado de la query arriba para resolver manualmente';
END
ELSE
BEGIN
    PRINT '✅ No hay conflictos';
END
GO

PRINT '';
PRINT '═══════════════════════════════════════════════════════════════════════';
PRINT 'MIGRACIÓN COMPLETADA';
PRINT 'Ahora puedes ejecutar: 01_eliminar_division_field.sql';
PRINT '═══════════════════════════════════════════════════════════════════════';
GO
