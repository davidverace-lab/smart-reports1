-- ═══════════════════════════════════════════════════════════════════════════
-- FIX 3: Queries Corregidas (sin usar campo Division)
-- Actualizar en: queries_hutchison.py
-- ═══════════════════════════════════════════════════════════════════════════

USE InstitutoHutchison;
GO

-- ════════════════════════════════════════════════════════════════
-- QUERY 1: Distribución por Departamentos (CORREGIDA)
-- ════════════════════════════════════════════════════════════════

-- ANTES (queries_hutchison.py líneas 49-57):
/*
SELECT
    COALESCE(u.Division, 'Sin División') as departamento,
    COUNT(u.IdUsuario) as cantidad
FROM instituto_Usuario u
WHERE u.UserStatus = 'Active'
GROUP BY u.Division
ORDER BY cantidad DESC
*/

-- DESPUÉS (CORRECTO):
SELECT
    COALESCE(d.NombreDepartamento, 'Sin Departamento') as departamento,
    COUNT(u.IdUsuario) as cantidad
FROM instituto_Usuario u
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
WHERE u.UserStatus = 'Active'
GROUP BY d.NombreDepartamento, d.IdDepartamento
ORDER BY cantidad DESC;


-- ════════════════════════════════════════════════════════════════
-- QUERY 2: Personal por Departamento (CORREGIDA)
-- ════════════════════════════════════════════════════════════════

-- ANTES (queries_hutchison.py líneas 64-72):
/*
SELECT
    COALESCE(u.Division, 'Sin División') as departamento,
    COUNT(*) as Total
FROM instituto_Usuario u
WHERE u.UserStatus = 'Active'
GROUP BY u.Division
ORDER BY Total DESC
*/

-- DESPUÉS (CORRECTO):
SELECT
    COALESCE(d.NombreDepartamento, 'Sin Departamento') as departamento,
    un.NombreUnidad as unidad,
    COUNT(*) as Total
FROM instituto_Usuario u
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_UnidadDeNegocio un ON d.IdUnidadDeNegocio = un.IdUnidadDeNegocio
WHERE u.UserStatus = 'Active'
GROUP BY d.NombreDepartamento, un.NombreUnidad, d.IdDepartamento
ORDER BY Total DESC;


-- ════════════════════════════════════════════════════════════════
-- QUERY 3: Calificaciones por Área (CORREGIDA)
-- ════════════════════════════════════════════════════════════════

-- ANTES (queries_hutchison.py líneas 93-104):
/*
SELECT
    COALESCE(u.Division, 'Sin División') as area,
    AVG(CAST(re.PuntajeObtenido AS FLOAT)) as PromedioCalif
FROM instituto_ResultadoEvaluacion re
INNER JOIN instituto_ProgresoModulo pm ON re.IdInscripcion = pm.IdInscripcion
INNER JOIN instituto_Usuario u ON pm.IdUsuario = u.IdUsuario
WHERE re.Aprobado = 1 AND u.UserStatus = 'Active'
GROUP BY u.Division
ORDER BY PromedioCalif DESC
*/

-- DESPUÉS (CORRECTO):
SELECT
    COALESCE(d.NombreDepartamento, 'Sin Departamento') as area,
    un.NombreUnidad as unidad,
    AVG(CAST(re.PuntajeObtenido AS FLOAT)) as PromedioCalif,
    COUNT(re.IdResultado) as TotalEvaluaciones
FROM instituto_ResultadoEvaluacion re
INNER JOIN instituto_ProgresoModulo pm ON re.IdInscripcion = pm.IdInscripcion
INNER JOIN instituto_Usuario u ON pm.IdUsuario = u.IdUsuario
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_UnidadDeNegocio un ON d.IdUnidadDeNegocio = un.IdUnidadDeNegocio
WHERE re.Aprobado = 1 AND u.UserStatus = 'Active'
GROUP BY d.NombreDepartamento, un.NombreUnidad, d.IdDepartamento
HAVING COUNT(re.IdResultado) > 0
ORDER BY PromedioCalif DESC;


-- ════════════════════════════════════════════════════════════════
-- QUERY BONUS: Reporte Completo por Departamento
-- ════════════════════════════════════════════════════════════════

SELECT
    un.NombreUnidad as Unidad,
    d.NombreDepartamento as Departamento,
    COUNT(DISTINCT u.IdUsuario) as TotalUsuarios,
    COUNT(DISTINCT CASE WHEN pm.EstatusModulo = 'Terminado' THEN u.IdUsuario END) as UsuariosConModulosCompletados,
    COUNT(pm.IdInscripcion) as TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) as ModulosCompletados,
    ROUND(
        CAST(SUM(CASE WHEN pm.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) AS FLOAT) /
        NULLIF(COUNT(pm.IdInscripcion), 0) * 100,
        1
    ) as PorcentajeCompletado,
    AVG(CASE WHEN re.Aprobado = 1 THEN re.PuntajeObtenido ELSE NULL END) as PromedioCalificacion
FROM instituto_Departamento d
INNER JOIN instituto_UnidadDeNegocio un ON d.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_Usuario u ON d.IdDepartamento = u.IdDepartamento AND u.UserStatus = 'Active'
LEFT JOIN instituto_ProgresoModulo pm ON u.IdUsuario = pm.IdUsuario
LEFT JOIN instituto_ResultadoEvaluacion re ON pm.IdInscripcion = re.IdInscripcion
WHERE d.Activo = 1
GROUP BY un.IdUnidadDeNegocio, un.NombreUnidad, d.IdDepartamento, d.NombreDepartamento
HAVING COUNT(DISTINCT u.IdUsuario) > 0
ORDER BY un.NombreUnidad, d.NombreDepartamento;

GO

PRINT '✅ Queries corregidas listas para copiar a queries_hutchison.py';
GO
