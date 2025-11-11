-- ============================================================
-- SCRIPT: Añadir UN SOLO usuario en MySQL
-- USO: Edita los valores y ejecuta este script
-- ============================================================

USE SmartReports;

-- ============================================================
-- PASO 1: Ver IDs disponibles
-- ============================================================

-- Ver unidades de negocio
SELECT IdUnidadDeNegocio, NombreUnidad FROM UnidadDeNegocio;

-- Ver roles
SELECT IdRol, NombreRol FROM Rol;

-- Ver último UserId usado
SELECT UserId FROM Usuario ORDER BY UserId DESC LIMIT 1;

-- ============================================================
-- PASO 2: Insertar nuevo usuario
-- EDITA LOS VALORES AQUÍ ↓
-- ============================================================

INSERT INTO Usuario (
    UserId,                   -- EDITAR: Siguiente ID disponible (ej: 'U033')
    IdUnidadDeNegocio,        -- EDITAR: ID de la unidad (ver arriba)
    IdRol,                    -- EDITAR: ID del rol (1=Admin, 2=RRHH, 3=Gerente, 4=Usuario)
    NombreCompleto,           -- EDITAR: Nombre completo
    UserEmail,                -- EDITAR: Email corporativo
    PasswordHash,             -- EDITAR: Contraseña (cambiar en producción)
    Division,                 -- EDITAR: División/Departamento
    Position,                 -- EDITAR: Puesto
    UserStatus,               -- DEJAR: 'Active'
    ManagerId,                -- EDITAR: UserId del jefe (NULL si no aplica)
    FechaCreacion             -- DEJAR: NOW()
)
VALUES (
    'U033',                           -- ← EDITAR UserId
    5,                                -- ← EDITAR IdUnidadDeNegocio
    3,                                -- ← EDITAR IdRol
    'Tu Nombre Completo',             -- ← EDITAR
    'tunombre@hutchison.com',         -- ← EDITAR
    'password123',                    -- ← EDITAR (usar hash en producción)
    'Operaciones',                    -- ← EDITAR
    'Supervisor',                     -- ← EDITAR
    'Active',
    NULL,                             -- ← EDITAR ManagerId si tiene jefe
    NOW()
);

-- ============================================================
-- PASO 3: Verificar que se insertó correctamente
-- ============================================================

SELECT
    UserId,
    NombreCompleto,
    UserEmail,
    (SELECT NombreRol FROM Rol WHERE Rol.IdRol = Usuario.IdRol) AS Rol,
    (SELECT NombreUnidad FROM UnidadDeNegocio WHERE UnidadDeNegocio.IdUnidadDeNegocio = Usuario.IdUnidadDeNegocio) AS Unidad,
    Position,
    UserStatus,
    FechaCreacion
FROM Usuario
WHERE UserId = 'U033';  -- ← Cambiar al UserId que insertaste

-- ============================================================
-- EJEMPLO DE USO:
--
-- 1. Conectar a MySQL:
--    mysql -u root -p
--
-- 2. Ejecutar este script:
--    source /ruta/a/add_single_user_mysql.sql
--
-- 3. O copiar y pegar en MySQL Workbench
-- ============================================================
