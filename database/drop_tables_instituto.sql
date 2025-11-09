-- ============================================
-- SCRIPT DE LIMPIEZA - Eliminar tablas con prefijo instituto_
-- Base de datos: tngcore
-- ============================================

USE tngcore;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- ELIMINAR TABLAS (en orden inverso de dependencias)
-- ============================================

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

-- ============================================
-- ELIMINAR VISTAS
-- ============================================

DROP VIEW IF EXISTS vw_instituto_UsuarioProgresoCompleto;
DROP VIEW IF EXISTS vw_instituto_ModulosPorDepartamento;
DROP VIEW IF EXISTS vw_instituto_EstadisticasEvaluaciones;

-- ============================================
-- ELIMINAR PROCEDIMIENTOS ALMACENADOS
-- ============================================

DROP PROCEDURE IF EXISTS sp_instituto_AsignarModuloUsuario;
DROP PROCEDURE IF EXISTS sp_instituto_ActualizarProgreso;
DROP PROCEDURE IF EXISTS sp_instituto_RegistrarResultadoEvaluacion;

-- ============================================
-- ELIMINAR TRIGGERS
-- ============================================

DROP TRIGGER IF EXISTS trg_instituto_ActualizarUltimoAcceso;
DROP TRIGGER IF EXISTS trg_instituto_NotificarAsignacionModulo;
DROP TRIGGER IF EXISTS trg_instituto_NotificarVencimiento;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- VERIFICACIÓN
-- ============================================

SELECT 'Limpieza completada!' AS Resultado;

SELECT
    TABLE_NAME as TablasRestantes
FROM information_schema.tables
WHERE table_schema = 'tngcore'
  AND TABLE_NAME LIKE 'instituto_%';

SELECT
    TABLE_NAME as VistasRestantes
FROM information_schema.views
WHERE table_schema = 'tngcore'
  AND TABLE_NAME LIKE 'vw_instituto_%';

SELECT
    ROUTINE_NAME as ProcedimientosRestantes
FROM information_schema.routines
WHERE routine_schema = 'tngcore'
  AND ROUTINE_NAME LIKE 'sp_instituto_%';
