-- ============================================
-- SCRIPT DE MIGRACIÓN COMPLETO
-- Base de datos: tngcore
-- Prefijo: instituto_
--
-- Este script:
-- 1. Elimina tablas existentes con prefijo instituto_
-- 2. Crea todas las tablas nuevas
-- 3. Inserta datos iniciales
-- ============================================

SELECT '🔄 INICIANDO MIGRACIÓN...' AS Estado;

-- ============================================
-- PASO 1: LIMPIEZA (Eliminar tablas existentes)
-- ============================================

SELECT '🗑️ Eliminando tablas existentes...' AS Estado;

USE tngcore;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS instituto_Certificado;
DROP TABLE IF EXISTS instituto_Notificacion;
DROP TABLE IF EXISTS instituto_RecursoModulo;
DROP TABLE IF EXISTS instituto_ReporteGuardado;
DROP TABLE IF EXISTS instituto_Soporte;
DROP TABLE IF EXISTS instituto_AuditoriaAcceso;
DROP TABLE IF EXISTS instituto_HistorialProgreso;
DROP TABLE IF EXISTS instituto_ResultadoEvaluacion;
DROP TABLE IF EXISTS instituto_Evaluacion;
DROP TABLE IF EXISTS instituto_ProgresoModulo;
DROP TABLE IF EXISTS instituto_ModuloDepartamento;
DROP TABLE IF EXISTS instituto_Modulo;
DROP TABLE IF EXISTS instituto_Usuario;
DROP TABLE IF EXISTS instituto_Departamento;
DROP TABLE IF EXISTS instituto_UnidadDeNegocio;
DROP TABLE IF EXISTS instituto_Rol;

DROP VIEW IF EXISTS vw_instituto_UsuarioProgresoCompleto;
DROP VIEW IF EXISTS vw_instituto_ModulosPorDepartamento;
DROP VIEW IF EXISTS vw_instituto_EstadisticasEvaluaciones;

DROP PROCEDURE IF EXISTS sp_instituto_AsignarModuloUsuario;
DROP PROCEDURE IF EXISTS sp_instituto_ActualizarProgreso;
DROP PROCEDURE IF EXISTS sp_instituto_RegistrarResultadoEvaluacion;

DROP TRIGGER IF EXISTS trg_instituto_ActualizarUltimoAcceso;
DROP TRIGGER IF EXISTS trg_instituto_NotificarAsignacionModulo;
DROP TRIGGER IF EXISTS trg_instituto_NotificarVencimiento;

SET FOREIGN_KEY_CHECKS = 1;

SELECT '✅ Limpieza completada' AS Estado;

-- ============================================
-- PASO 2: CREACIÓN (Ejecutar script completo)
-- ============================================

SELECT '🏗️ Creando nuevas tablas...' AS Estado;

SOURCE create_tables_instituto.sql;

SELECT '✅ Tablas creadas exitosamente' AS Estado;

-- ============================================
-- PASO 3: VERIFICACIÓN FINAL
-- ============================================

SELECT '📊 RESUMEN DE MIGRACIÓN' AS Estado;

SELECT
    'Tablas' as Tipo,
    COUNT(*) as Cantidad
FROM information_schema.tables
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'instituto_%'

UNION ALL

SELECT
    'Vistas' as Tipo,
    COUNT(*) as Cantidad
FROM information_schema.views
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'vw_instituto_%'

UNION ALL

SELECT
    'Procedimientos' as Tipo,
    COUNT(*) as Cantidad
FROM information_schema.routines
WHERE routine_schema = 'tngcore' AND ROUTINE_NAME LIKE 'sp_instituto_%';

-- ============================================
-- LISTADO DE OBJETOS CREADOS
-- ============================================

SELECT '📋 TABLAS CREADAS:' AS Info;

SELECT
    TABLE_NAME as Tabla,
    TABLE_ROWS as Filas,
    ROUND(DATA_LENGTH / 1024, 2) as 'Tamaño_KB',
    TABLE_COMMENT as Descripcion
FROM information_schema.tables
WHERE table_schema = 'tngcore'
  AND TABLE_NAME LIKE 'instituto_%'
ORDER BY TABLE_NAME;

SELECT '📋 VISTAS CREADAS:' AS Info;

SELECT
    TABLE_NAME as Vista
FROM information_schema.views
WHERE table_schema = 'tngcore'
  AND TABLE_NAME LIKE 'vw_instituto_%'
ORDER BY TABLE_NAME;

SELECT '📋 PROCEDIMIENTOS CREADOS:' AS Info;

SELECT
    ROUTINE_NAME as Procedimiento,
    ROUTINE_TYPE as Tipo
FROM information_schema.routines
WHERE routine_schema = 'tngcore'
  AND ROUTINE_NAME LIKE 'sp_instituto_%'
ORDER BY ROUTINE_NAME;

SELECT '✅ MIGRACIÓN COMPLETADA EXITOSAMENTE!' AS Resultado;
