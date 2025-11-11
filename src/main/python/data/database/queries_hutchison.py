"""
Queries SQL adaptadas al esquema REAL de Hutchison Ports
Usar estas queries en los paneles de dashboards
"""

# ============================================
# QUERIES PARA DASHBOARDS GERENCIALES
# ============================================

# Total de usuarios activos
QUERY_TOTAL_USUARIOS = """
    SELECT COUNT(*) as total
    FROM instituto_Usuario
    WHERE UserStatus = 'Active'
"""

# Usuarios por Unidad de Negocio
QUERY_USUARIOS_POR_UNIDAD = """
    SELECT
        COALESCE(un.NombreUnidad, 'SIN UNIDAD') as unidad,
        COUNT(u.IdUsuario) as cantidad
    FROM instituto_Usuario u
    LEFT JOIN instituto_UnidadDeNegocio un
        ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
    WHERE u.UserStatus = 'Active'
    GROUP BY un.NombreUnidad
    ORDER BY cantidad DESC
"""

# Progreso por Unidad de Negocio (% de módulos completados)
QUERY_PROGRESO_POR_UNIDAD = """
    SELECT
        un.NombreUnidad as unidad,
        ROUND(
            CAST(SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) AS FLOAT) /
            NULLIF(COUNT(pm.IdInscripcion), 0) * 100,
            1
        ) as porcentaje
    FROM instituto_UnidadDeNegocio un
    LEFT JOIN instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
    LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
    WHERE un.Activo = 1 AND u.UserStatus = 'Active'
    GROUP BY un.NombreUnidad
    HAVING COUNT(pm.IdInscripcion) > 0
    ORDER BY porcentaje DESC
"""

# Distribución por Departamentos
QUERY_DISTRIBUCION_DEPARTAMENTOS = """
    SELECT
        COALESCE(u.Division, 'Sin División') as departamento,
        COUNT(u.IdUsuario) as cantidad
    FROM instituto_Usuario u
    WHERE u.UserStatus = 'Active'
    GROUP BY u.Division
    ORDER BY cantidad DESC
"""

# ============================================
# QUERIES PARA DASHBOARDS RRHH
# ============================================

# Personal por Departamento
QUERY_PERSONAL_POR_DEPARTAMENTO = """
    SELECT
        COALESCE(u.Division, 'Sin División') as departamento,
        COUNT(*) as Total
    FROM instituto_Usuario u
    WHERE u.UserStatus = 'Active'
    GROUP BY u.Division
    ORDER BY Total DESC
"""

# Estado de Capacitación (Completados, En Progreso, Pendientes)
QUERY_ESTADO_CAPACITACION = """
    -- Completados
    SELECT COUNT(*) as Completados
    FROM instituto_ProgresoModulo
    WHERE EstatusModulo = 'Completado';

    -- En Progreso
    SELECT COUNT(*) as EnProgreso
    FROM instituto_ProgresoModulo
    WHERE EstatusModulo = 'En Progreso';

    -- Pendientes (usuarios activos * módulos - asignados)
    SELECT
        (SELECT COUNT(*) FROM instituto_Usuario WHERE UserStatus = 'Active') *
        (SELECT COUNT(*) FROM instituto_Modulo WHERE Activo = 1) -
        (SELECT COUNT(*) FROM instituto_ProgresoModulo) as Pendientes;
"""

# Promedio de calificaciones por área
QUERY_CALIFICACIONES_POR_AREA = """
    SELECT
        COALESCE(u.Division, 'Sin División') as area,
        AVG(CAST(re.PuntajeObtenido AS FLOAT)) as PromedioCalif
    FROM instituto_ResultadoEvaluacion re
    INNER JOIN instituto_ProgresoModulo pm ON re.IdInscripcion = pm.IdInscripcion
    INNER JOIN instituto_Usuario u ON pm.UserId = u.UserId
    WHERE re.Aprobado = 1 AND u.UserStatus = 'Active'
    GROUP BY u.Division
    ORDER BY PromedioCalif DESC
"""

# Cumplimiento por Unidad de Negocio (% con al menos 1 módulo completado)
QUERY_CUMPLIMIENTO_UNIDADES = """
    SELECT
        un.NombreUnidad,
        CAST(COUNT(DISTINCT CASE WHEN pm.EstatusModulo = 'Completado' THEN u.IdUsuario END) AS FLOAT) /
        NULLIF(COUNT(DISTINCT u.IdUsuario), 0) * 100.0 as PorcentajeCumplimiento
    FROM instituto_Usuario u
    INNER JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
    LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
    WHERE u.UserStatus = 'Active' AND un.Activo = 1
    GROUP BY un.NombreUnidad
    ORDER BY PorcentajeCumplimiento DESC
"""

# Tendencia de módulos completados por mes
QUERY_TENDENCIA_MENSUAL = """
    SELECT
        FORMAT(FechaFinalizacion, 'yyyy-MM') as Mes,
        COUNT(*) as Total
    FROM instituto_ProgresoModulo
    WHERE EstatusModulo = 'Completado' AND FechaFinalizacion IS NOT NULL
    GROUP BY FORMAT(FechaFinalizacion, 'yyyy-MM')
    ORDER BY Mes
"""

# ============================================
# HELPER FUNCTIONS
# ============================================

def ejecutar_query_simple(db_connection, query):
    """
    Ejecutar query que retorna un solo valor

    Args:
        db_connection: Conexión a BD
        query: Query SQL

    Returns:
        Valor único o None
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return None

def ejecutar_query_lista(db_connection, query):
    """
    Ejecutar query que retorna múltiples filas

    Args:
        db_connection: Conexión a BD
        query: Query SQL

    Returns:
        Lista de tuplas con resultados
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return []

def query_to_chart_data(results, label_index=0, value_index=1):
    """
    Convertir resultados de query a formato de datos para gráficos

    Args:
        results: Lista de tuplas desde fetchall()
        label_index: Índice de la columna de labels
        value_index: Índice de la columna de valores

    Returns:
        Dict con 'labels' y 'values'
    """
    if not results:
        return {'labels': [], 'values': []}

    labels = [row[label_index] for row in results]
    values = [row[value_index] for row in results]

    return {'labels': labels, 'values': values}
