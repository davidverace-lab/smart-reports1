-- ═══════════════════════════════════════════════════════════════════════════
-- FIX 1: Eliminar campo Division de instituto_Usuario
-- Razón: Causa confusión con instituto_Departamento
-- ═══════════════════════════════════════════════════════════════════════════

USE InstitutoHutchison;
GO

PRINT '═══════════════════════════════════════════════════════════════════════';
PRINT 'FIX: Eliminar campo Division (confusión con Departamento)';
PRINT '═══════════════════════════════════════════════════════════════════════';
GO

-- Verificar si el campo existe
IF EXISTS (
    SELECT * FROM sys.columns
    WHERE object_id = OBJECT_ID('instituto_Usuario')
    AND name = 'Division'
)
BEGIN
    PRINT 'Campo Division encontrado. Eliminando...';

    -- Verificar si hay datos en Division que deberíamos migrar
    DECLARE @RegistrosConDivision INT;

    SELECT @RegistrosConDivision = COUNT(*)
    FROM instituto_Usuario
    WHERE Division IS NOT NULL AND Division != '';

    IF @RegistrosConDivision > 0
    BEGIN
        PRINT '⚠️  ADVERTENCIA: Hay ' + CAST(@RegistrosConDivision AS VARCHAR) + ' usuarios con campo Division lleno';
        PRINT '    Estos datos se perderán al eliminar el campo.';
        PRINT '    Si deseas migrarlos a Departamento, cancela este script y ejecuta primero:';
        PRINT '    02_migrar_division_a_departamento.sql';
        PRINT '';
    END

    -- Eliminar el campo
    ALTER TABLE instituto_Usuario DROP COLUMN Division;

    PRINT '✅ Campo Division eliminado exitosamente';
END
ELSE
BEGIN
    PRINT 'ℹ️  Campo Division no existe (ya fue eliminado o nunca existió)';
END
GO

PRINT '';
PRINT '═══════════════════════════════════════════════════════════════════════';
PRINT 'FIX COMPLETADO';
PRINT '═══════════════════════════════════════════════════════════════════════';
GO
