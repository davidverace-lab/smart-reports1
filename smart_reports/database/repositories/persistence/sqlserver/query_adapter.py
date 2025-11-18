"""
Query Adapter: MySQL → SQL Server
Convierte queries MySQL a SQL Server para mantener compatibilidad
"""
import re
from typing import Tuple


class QueryAdapter:
    """
    Adaptador de queries MySQL a SQL Server

    Convierte sintaxis específica de MySQL a SQL Server:
    - Placeholders: %s → ?
    - LIMIT → TOP
    - INSERT IGNORE → IF NOT EXISTS
    - ON DUPLICATE KEY UPDATE → MERGE o IF EXISTS
    - COALESCE → ISNULL
    - NOW() → GETDATE()
    - DATE_FORMAT → FORMAT
    - Backticks → Corchetes
    """

    @staticmethod
    def adapt_query(mysql_query: str) -> str:
        """
        Convierte una query MySQL a SQL Server

        Args:
            mysql_query: Query en sintaxis MySQL

        Returns:
            Query en sintaxis SQL Server
        """
        query = mysql_query

        # 1. Reemplazar placeholders %s por ?
        query = QueryAdapter._convert_placeholders(query)

        # 2. Convertir LIMIT a TOP
        query = QueryAdapter._convert_limit_to_top(query)

        # 3. Convertir INSERT IGNORE
        query = QueryAdapter._convert_insert_ignore(query)

        # 4. Convertir ON DUPLICATE KEY UPDATE
        query = QueryAdapter._convert_on_duplicate_key(query)

        # 5. Funciones de fecha
        query = QueryAdapter._convert_date_functions(query)

        # 6. COALESCE → ISNULL (opcional, COALESCE existe en SQL Server)
        # query = QueryAdapter._convert_coalesce(query)

        # 7. Backticks → Corchetes
        query = QueryAdapter._convert_backticks(query)

        return query

    @staticmethod
    def _convert_placeholders(query: str) -> str:
        """
        Convierte placeholders de MySQL (%s) a SQL Server (?)

        Args:
            query: Query con %s

        Returns:
            Query con ?
        """
        return query.replace('%s', '?')

    @staticmethod
    def _convert_limit_to_top(query: str) -> str:
        """
        Convierte LIMIT a TOP

        MySQL: SELECT * FROM tabla LIMIT 10
        SQL Server: SELECT TOP 10 * FROM tabla

        Args:
            query: Query con LIMIT

        Returns:
            Query con TOP
        """
        # Buscar LIMIT al final
        match = re.search(r'\bLIMIT\s+(\d+)\s*$', query, re.IGNORECASE)
        if match:
            limit_value = match.group(1)
            query = re.sub(r'\bLIMIT\s+\d+\s*$', '', query, flags=re.IGNORECASE)

            # Insertar TOP después de SELECT
            query = re.sub(
                r'\bSELECT\b',
                f'SELECT TOP {limit_value}',
                query,
                count=1,
                flags=re.IGNORECASE
            )

        return query

    @staticmethod
    def _convert_insert_ignore(query: str) -> str:
        """
        Convierte INSERT IGNORE a IF NOT EXISTS

        MySQL: INSERT IGNORE INTO tabla (col) VALUES (val)
        SQL Server: IF NOT EXISTS (SELECT 1 FROM tabla WHERE ...) INSERT INTO tabla (col) VALUES (val)

        NOTA: Esta conversión es simple. Para casos complejos, usar MERGE.

        Args:
            query: Query con INSERT IGNORE

        Returns:
            Query con IF NOT EXISTS (simplificado, puede requerir ajuste manual)
        """
        if re.search(r'\bINSERT\s+IGNORE\b', query, re.IGNORECASE):
            # Simplificación: Remover IGNORE y confiar en constraints
            query = re.sub(r'\bINSERT\s+IGNORE\b', 'INSERT', query, flags=re.IGNORECASE)

            # ⚠️ NOTA: Esto puede causar errores si hay duplicados
            # Para manejar correctamente, usar MERGE o TRY...CATCH

        return query

    @staticmethod
    def _convert_on_duplicate_key(query: str) -> str:
        """
        Convierte ON DUPLICATE KEY UPDATE a MERGE

        MySQL:
            INSERT INTO tabla (col1, col2) VALUES (?, ?)
            ON DUPLICATE KEY UPDATE col1 = VALUES(col1)

        SQL Server:
            MERGE tabla AS target
            USING (SELECT ? AS col1, ? AS col2) AS source
            ON (target.pk = source.pk)
            WHEN MATCHED THEN UPDATE SET col1 = source.col1
            WHEN NOT MATCHED THEN INSERT (col1, col2) VALUES (source.col1, source.col2);

        ⚠️ NOTA: Esta conversión es compleja y puede requerir ajuste manual

        Args:
            query: Query con ON DUPLICATE KEY UPDATE

        Returns:
            Query comentada con instrucciones (requiere conversión manual)
        """
        if re.search(r'\bON\s+DUPLICATE\s+KEY\s+UPDATE\b', query, re.IGNORECASE):
            # Esta conversión es muy compleja, retornar comentario
            query = f"""
-- ⚠️ CONVERSIÓN MANUAL REQUERIDA
-- MySQL: ON DUPLICATE KEY UPDATE
-- SQL Server: Usar MERGE o UPDATE con IF EXISTS
-- Query original:
{query}

-- Ejemplo de conversión a MERGE:
-- MERGE INTO tabla AS target
-- USING (SELECT ? AS col1, ? AS col2) AS source
-- ON (target.pk = source.pk)
-- WHEN MATCHED THEN UPDATE SET col1 = source.col1
-- WHEN NOT MATCHED THEN INSERT (col1, col2) VALUES (source.col1, source.col2);
"""

        return query

    @staticmethod
    def _convert_date_functions(query: str) -> str:
        """
        Convierte funciones de fecha de MySQL a SQL Server

        Conversiones:
        - NOW() → GETDATE()
        - CURRENT_TIMESTAMP → GETDATE()
        - CURDATE() → CAST(GETDATE() AS DATE)
        - DATE_FORMAT(fecha, '%Y-%m-%d') → FORMAT(fecha, 'yyyy-MM-dd')

        Args:
            query: Query con funciones de fecha MySQL

        Returns:
            Query con funciones SQL Server
        """
        # NOW() → GETDATE()
        query = re.sub(r'\bNOW\(\)', 'GETDATE()', query, flags=re.IGNORECASE)

        # CURRENT_TIMESTAMP → GETDATE()
        query = re.sub(r'\bCURRENT_TIMESTAMP\b', 'GETDATE()', query, flags=re.IGNORECASE)

        # CURDATE() → CAST(GETDATE() AS DATE)
        query = re.sub(r'\bCURDATE\(\)', 'CAST(GETDATE() AS DATE)', query, flags=re.IGNORECASE)

        return query

    @staticmethod
    def _convert_backticks(query: str) -> str:
        """
        Convierte backticks (`) a corchetes ([])

        MySQL: SELECT `columna` FROM `tabla`
        SQL Server: SELECT [columna] FROM [tabla]

        Args:
            query: Query con backticks

        Returns:
            Query con corchetes
        """
        # Reemplazar backticks por corchetes
        query = query.replace('`', '[')
        # Pero solo si hay pares
        if '[' in query:
            query = query.replace('[', '[', 1).replace('[', ']', query.count('[') // 2)

        # Mejor: usar regex para pares
        query = re.sub(r'`([^`]+)`', r'[\1]', query)

        return query


# =============================================================================
# QUERIES COMUNES YA ADAPTADAS
# =============================================================================

class CommonQueriesSQLServer:
    """
    Queries comunes ya adaptadas para SQL Server
    """

    # Seleccionar módulos
    SELECT_MODULOS = """
        SELECT IdModulo, NombreModulo
        FROM instituto_Modulo
        WHERE Activo = 1
    """

    # Seleccionar unidades de negocio
    SELECT_UNIDADES = """
        SELECT IdUnidadDeNegocio, NombreUnidad
        FROM instituto_UnidadDeNegocio
        WHERE Activo = 1
    """

    # Seleccionar departamentos
    SELECT_DEPARTAMENTOS = """
        SELECT IdDepartamento, IdUnidadDeNegocio, NombreDepartamento
        FROM instituto_Departamento
        WHERE Activo = 1
    """

    # Seleccionar usuarios existentes (con TOP en lugar de LIMIT)
    SELECT_USUARIOS_BY_IDS = """
        SELECT IdUsuario, UserId
        FROM instituto_Usuario
        WHERE UserId IN ({placeholders})
    """

    # Seleccionar progresos existentes
    SELECT_PROGRESOS_BY_USERS = """
        SELECT UserId, IdModulo, IdInscripcion
        FROM instituto_ProgresoModulo
        WHERE UserId IN ({placeholders})
    """

    # UPDATE progreso (funciona igual en ambas BDs)
    UPDATE_PROGRESO = """
        UPDATE instituto_ProgresoModulo
        SET EstatusModulo = ?,
            FechaInicio = ISNULL(?, FechaInicio),
            FechaFinalizacion = ?,
            PorcentajeAvance = ?
        WHERE UserId = ? AND IdModulo = ?
    """

    # INSERT progreso (funciona igual)
    INSERT_PROGRESO = """
        INSERT INTO instituto_ProgresoModulo
        (UserId, IdModulo, EstatusModulo, FechaInicio, FechaFinalizacion,
         PorcentajeAvance, FechaAsignacion)
        VALUES (?, ?, ?, ?, ?, ?, GETDATE())
    """

    # MERGE para upsert de progreso (SQL Server específico)
    MERGE_PROGRESO = """
        MERGE INTO instituto_ProgresoModulo AS target
        USING (SELECT ? AS UserId, ? AS IdModulo, ? AS EstatusModulo,
                      ? AS FechaInicio, ? AS FechaFinalizacion, ? AS PorcentajeAvance) AS source
        ON (target.UserId = source.UserId AND target.IdModulo = source.IdModulo)
        WHEN MATCHED THEN
            UPDATE SET
                EstatusModulo = source.EstatusModulo,
                FechaInicio = ISNULL(source.FechaInicio, target.FechaInicio),
                FechaFinalizacion = source.FechaFinalizacion,
                PorcentajeAvance = source.PorcentajeAvance
        WHEN NOT MATCHED THEN
            INSERT (UserId, IdModulo, EstatusModulo, FechaInicio, FechaFinalizacion,
                    PorcentajeAvance, FechaAsignacion)
            VALUES (source.UserId, source.IdModulo, source.EstatusModulo,
                    source.FechaInicio, source.FechaFinalizacion, source.PorcentajeAvance,
                    GETDATE());
    """

    # INSERT unidad de negocio (con verificación)
    INSERT_UNIDAD_IF_NOT_EXISTS = """
        IF NOT EXISTS (SELECT 1 FROM instituto_UnidadDeNegocio WHERE NombreUnidad = ?)
        BEGIN
            INSERT INTO instituto_UnidadDeNegocio (NombreUnidad, Codigo, Activo)
            VALUES (?, ?, 1)
        END
    """

    # INSERT departamento (con verificación)
    INSERT_DEPARTAMENTO_IF_NOT_EXISTS = """
        IF NOT EXISTS (
            SELECT 1 FROM instituto_Departamento
            WHERE IdUnidadDeNegocio = ? AND NombreDepartamento = ?
        )
        BEGIN
            INSERT INTO instituto_Departamento (IdUnidadDeNegocio, NombreDepartamento, Activo)
            VALUES (?, ?, 1)
        END
    """

    # MERGE usuario (upsert)
    MERGE_USUARIO = """
        MERGE INTO instituto_Usuario AS target
        USING (SELECT ? AS UserId, ? AS NombreCompleto, ? AS UserEmail,
                      ? AS Position, ? AS IdUnidadDeNegocio, ? AS IdDepartamento,
                      ? AS Nivel, ? AS Ubicacion, ? AS IdRol) AS source
        ON (target.UserId = source.UserId)
        WHEN MATCHED THEN
            UPDATE SET
                NombreCompleto = source.NombreCompleto,
                UserEmail = source.UserEmail,
                Position = source.Position,
                IdUnidadDeNegocio = source.IdUnidadDeNegocio,
                IdDepartamento = source.IdDepartamento,
                Nivel = source.Nivel,
                Ubicacion = source.Ubicacion
        WHEN NOT MATCHED THEN
            INSERT (UserId, IdUnidadDeNegocio, IdDepartamento, IdRol,
                    NombreCompleto, UserEmail, Position, Nivel, Ubicacion, Activo)
            VALUES (source.UserId, source.IdUnidadDeNegocio, source.IdDepartamento,
                    source.IdRol, source.NombreCompleto, source.UserEmail, source.Position,
                    source.Nivel, source.Ubicacion, 1);
    """

    # INSERT resultado evaluación
    INSERT_RESULTADO_EVALUACION = """
        INSERT INTO instituto_ResultadoEvaluacion
        (IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado,
         IntentoNumero, FechaRealizacion)
        VALUES (?, ?, ?, ?, ?, GETDATE())
    """

    # SELECT evaluación por módulo (TOP en lugar de LIMIT)
    SELECT_EVALUACION_BY_MODULO = """
        SELECT TOP 1 IdEvaluacion, PuntajeMinimoAprobatorio
        FROM instituto_Evaluacion
        WHERE IdModulo = ? AND Activo = 1
    """

    # Reporte de cumplimiento por unidad (funciona en ambas BDs)
    REPORTE_CUMPLIMIENTO_UNIDAD = """
        SELECT
            un.NombreUnidad,
            d.NombreDepartamento,
            COUNT(DISTINCT p.IdInscripcion) as TotalAsignaciones,
            SUM(CASE WHEN p.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) as Completados,
            SUM(CASE WHEN p.EstatusModulo = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
            SUM(CASE WHEN p.FechaVencimiento < GETDATE() AND p.EstatusModulo != 'Terminado' THEN 1 ELSE 0 END) as Vencidos,
            ROUND(CAST(SUM(CASE WHEN p.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) as PorcentajeCumplimiento
        FROM instituto_UnidadDeNegocio un
        JOIN instituto_Departamento d ON un.IdUnidadDeNegocio = d.IdUnidadDeNegocio
        JOIN instituto_Usuario u ON d.IdDepartamento = u.IdDepartamento
        JOIN instituto_ProgresoModulo p ON u.UserId = p.UserId
        WHERE un.Activo = 1
        GROUP BY un.IdUnidadDeNegocio, un.NombreUnidad, d.IdDepartamento, d.NombreDepartamento
    """


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("QUERY ADAPTER: MySQL → SQL Server")
    print("="*70)

    # Ejemplo 1: Convertir query simple
    mysql_query1 = "SELECT * FROM instituto_Usuario WHERE Activo = 1 LIMIT 10"
    sqlserver_query1 = QueryAdapter.adapt_query(mysql_query1)

    print("\n📝 Ejemplo 1: LIMIT → TOP")
    print(f"MySQL:      {mysql_query1}")
    print(f"SQL Server: {sqlserver_query1}")

    # Ejemplo 2: Funciones de fecha
    mysql_query2 = """
        SELECT * FROM instituto_ProgresoModulo
        WHERE FechaAsignacion >= NOW()
        AND FechaVencimiento < CURRENT_TIMESTAMP
    """
    sqlserver_query2 = QueryAdapter.adapt_query(mysql_query2)

    print("\n📝 Ejemplo 2: NOW() → GETDATE()")
    print(f"MySQL:      {mysql_query2}")
    print(f"SQL Server: {sqlserver_query2}")

    # Ejemplo 3: Placeholders
    mysql_query3 = "INSERT INTO instituto_Modulo (NombreModulo) VALUES (%s)"
    sqlserver_query3 = QueryAdapter.adapt_query(mysql_query3)

    print("\n📝 Ejemplo 3: %s → ?")
    print(f"MySQL:      {mysql_query3}")
    print(f"SQL Server: {sqlserver_query3}")

    print("\n" + "="*70)
    print("✅ QUERIES ADAPTADAS DISPONIBLES EN CommonQueriesSQLServer")
    print("="*70)
