# 🐬 Guía Completa para MySQL - Hutchison Ports

Esta guía te explica cómo insertar datos y añadir usuarios en **MySQL**.

---

## 📋 Tabla de Contenidos

1. [Ejecutar Scripts SQL](#1-ejecutar-scripts-sql)
2. [Añadir Usuario Único](#2-añadir-usuario-único)
3. [Añadir Múltiples Usuarios](#3-añadir-múltiples-usuarios)
4. [Comandos Útiles](#4-comandos-útiles)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Ejecutar Scripts SQL

### Opción A: Desde la Terminal

```bash
# 1. Conectar a MySQL
mysql -u root -p

# 2. Crear base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS SmartReports;
USE SmartReports;

# 3. Ejecutar scripts en orden
source /ruta/a/smart-reports1/database/sql/mysql/01_datos_base_mysql.sql
source /ruta/a/smart-reports1/database/sql/mysql/02_usuarios_30_mysql.sql

# 4. Verificar
SELECT COUNT(*) AS TotalUsuarios FROM Usuario;
```

### Opción B: Usando MySQL Workbench

1. Abre **MySQL Workbench**
2. Conecta a tu servidor MySQL
3. Ve a **File → Open SQL Script**
4. Selecciona `01_datos_base_mysql.sql`
5. Click en el rayo ⚡ (Execute)
6. Repite con `02_usuarios_30_mysql.sql`

### Opción C: Comando en una línea

```bash
mysql -u root -p SmartReports < database/sql/mysql/01_datos_base_mysql.sql
mysql -u root -p SmartReports < database/sql/mysql/02_usuarios_30_mysql.sql
```

---

## 2. Añadir Usuario Único

### Método Rápido (Copy-Paste)

```bash
mysql -u root -p
```

Luego copia y pega:

```sql
USE SmartReports;

-- Ver IDs disponibles
SELECT IdUnidadDeNegocio, NombreUnidad FROM UnidadDeNegocio;
SELECT IdRol, NombreRol FROM Rol;

-- Insertar nuevo usuario (EDITA LOS VALORES)
INSERT INTO Usuario (
    UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail,
    PasswordHash, Division, Position, UserStatus, ManagerId, FechaCreacion
)
VALUES (
    'U033',                           -- ← Tu UserId
    5,                                -- ← IdUnidadDeNegocio (1-10)
    3,                                -- ← IdRol (1=Admin, 2=RRHH, 3=Gerente, 4=Usuario)
    'Ana Gabriela Fernández López',   -- ← Nombre completo
    'afernandez@hutchison.com',       -- ← Email
    'password123',                    -- ← Contraseña
    'Operaciones',                    -- ← División
    'Supervisor de Logística',        -- ← Puesto
    'Active',
    NULL,                             -- ← UserId del jefe (o NULL)
    NOW()
);

-- Verificar
SELECT UserId, NombreCompleto, UserEmail FROM Usuario WHERE UserId = 'U033';
```

### Usando el Script Pre-hecho

```bash
# 1. Edita el archivo
nano database/sql/mysql/add_single_user_mysql.sql

# 2. Cambia los valores:
#    - UserId: 'U033'
#    - IdUnidadDeNegocio: 5 (HPMX)
#    - IdRol: 3 (Gerente)
#    - NombreCompleto, UserEmail, etc.

# 3. Ejecuta
mysql -u root -p SmartReports < database/sql/mysql/add_single_user_mysql.sql
```

---

## 3. Añadir Múltiples Usuarios

### Script Python para Batch Insert

Crea `add_users_batch.py`:

```python
import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tu_password',  # ← CAMBIAR
    database='SmartReports'
)
cursor = conn.cursor()

# Lista de usuarios a insertar
usuarios = [
    ('U033', 5, 3, 'Ana Fernández', 'afernandez@hutchison.com', 'pass123', 'Operaciones', 'Supervisor'),
    ('U034', 2, 4, 'Roberto Muñoz', 'rmunoz@hutchison.com', 'pass123', 'Logística', 'Analista'),
    ('U035', 7, 4, 'Carla Gómez', 'cgomez@hutchison.com', 'pass123', 'Administración', 'Asistente'),
    # Añade más usuarios aquí...
]

# Query de inserción
query = """
    INSERT INTO Usuario (
        UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail,
        PasswordHash, Division, Position, UserStatus, FechaCreacion
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active', NOW())
"""

# Insertar todos
try:
    cursor.executemany(query, usuarios)
    conn.commit()
    print(f"✅ {cursor.rowcount} usuarios insertados correctamente")
except mysql.connector.Error as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
```

Ejecutar:
```bash
pip install mysql-connector-python
python add_users_batch.py
```

---

## 4. Comandos Útiles

### Ver Todos los Usuarios

```sql
USE SmartReports;

SELECT
    u.UserId,
    u.NombreCompleto,
    u.UserEmail,
    r.NombreRol AS Rol,
    un.NombreUnidad AS Unidad,
    u.Position,
    u.UserStatus
FROM Usuario u
LEFT JOIN Rol r ON u.IdRol = r.IdRol
LEFT JOIN UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
ORDER BY u.UserId;
```

### Ver Usuarios por Rol

```sql
SELECT
    r.NombreRol,
    COUNT(u.IdUsuario) AS Total
FROM Rol r
LEFT JOIN Usuario u ON r.IdRol = u.IdRol
GROUP BY r.NombreRol;
```

### Ver Usuarios por Unidad

```sql
SELECT
    un.NombreUnidad,
    COUNT(u.IdUsuario) AS Total
FROM UnidadDeNegocio un
LEFT JOIN Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
GROUP BY un.NombreUnidad
ORDER BY Total DESC;
```

### Buscar Usuario por Email

```sql
SELECT * FROM Usuario WHERE UserEmail LIKE '%fernandez%';
```

### Actualizar Usuario

```sql
-- Cambiar rol de un usuario
UPDATE Usuario
SET IdRol = 3  -- 3 = Gerente
WHERE UserId = 'U033';

-- Cambiar unidad de negocio
UPDATE Usuario
SET IdUnidadDeNegocio = 5  -- 5 = HPMX
WHERE UserId = 'U033';

-- Cambiar contraseña
UPDATE Usuario
SET PasswordHash = 'nueva_password123'
WHERE UserId = 'U033';
```

### Desactivar Usuario (no eliminar)

```sql
UPDATE Usuario
SET UserStatus = 'Inactive'
WHERE UserId = 'U033';
```

### Eliminar Usuario (⚠️ Cuidado)

```sql
DELETE FROM Usuario WHERE UserId = 'U033';
```

---

## 5. Troubleshooting

### Error: "Table doesn't exist"

```sql
-- Verificar que la tabla existe
SHOW TABLES;

-- Ver estructura de la tabla
DESCRIBE Usuario;
```

### Error: "Duplicate entry"

El UserId ya existe. Usa otro:

```sql
-- Ver último UserId
SELECT UserId FROM Usuario ORDER BY UserId DESC LIMIT 1;

-- Si el último es U032, usa U033
```

### Error: "Foreign key constraint fails"

El IdUnidadDeNegocio o IdRol no existe:

```sql
-- Ver IDs válidos
SELECT IdUnidadDeNegocio FROM UnidadDeNegocio;
SELECT IdRol FROM Rol;
```

### Ver Logs de MySQL

```bash
# Ubuntu/Debian
sudo tail -f /var/log/mysql/error.log

# CentOS/RHEL
sudo tail -f /var/log/mysqld.log

# macOS (Homebrew)
tail -f /usr/local/var/mysql/*.err
```

---

## 📊 Referencia Rápida

### IDs de Unidades de Negocio

| ID | Nombre       | Descripción                    |
|----|--------------|--------------------------------|
| 1  | CCI          | Contecon Cartagena             |
| 2  | ECV          | Ensenada Containers Terminal   |
| 3  | EIT          | Ensenada International Term.   |
| 4  | HPML         | Hutchison Ports Manzanillo     |
| 5  | HPMX         | Hutchison Ports Mexico         |
| 6  | ICAVE        | Icave Veracruz                 |
| 7  | LCTM         | Lázaro Cárdenas Container T.   |
| 8  | LCT TILH     | LCT Tuxpan                     |
| 9  | TIMSA        | Terminal Internacional Multi.  |
| 10 | TNG          | Terminal Norte de Grupo H.     |

### IDs de Roles

| ID | Nombre            | Permisos                        |
|----|-------------------|---------------------------------|
| 1  | Administrador     | Acceso total                    |
| 2  | Recursos Humanos  | Gestión de personal             |
| 3  | Gerente           | Supervisión y análisis          |
| 4  | Usuario           | Acceso operativo básico         |

---

## 🔐 Usuarios de Prueba Pre-creados

| UserId | Email                      | Password | Rol         | Unidad |
|--------|----------------------------|----------|-------------|--------|
| U001   | cmendoza@hutchison.com     | admin123 | Admin       | HPMX   |
| U002   | plopez@hutchison.com       | rrhh123  | RRHH        | HPMX   |
| U003   | jmendez@hutchison.com      | port123  | Gerente     | CCI    |
| U004   | mcastro@hutchison.com      | port123  | Gerente     | HPML   |
| U005   | rhernandez@hutchison.com   | port123  | Gerente     | LCTM   |
| U006+  | (ver 02_usuarios_30_mysql.sql) | port123  | Usuario     | Varias |

---

## 🚀 Inicio Rápido (3 comandos)

```bash
# 1. Conectar
mysql -u root -p

# 2. Cargar datos base
USE SmartReports;
source database/sql/mysql/01_datos_base_mysql.sql;
source database/sql/mysql/02_usuarios_30_mysql.sql;

# 3. Verificar
SELECT COUNT(*) FROM Usuario;
```

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs de MySQL
2. Verifica la estructura de tus tablas con `DESCRIBE Usuario`
3. Asegúrate de tener permisos adecuados
4. Consulta la documentación de MySQL: https://dev.mysql.com/doc/

---

✅ **Todo listo!** Ahora puedes añadir usuarios en MySQL sin problemas.
