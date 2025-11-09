# 🔄 Guía de Migración - Tablas instituto_ en tngcore

## 📋 RESUMEN

Este documento explica cómo usar los scripts para trabajar con la base de datos **tngcore** usando el prefijo **instituto_**.

---

## 📁 ARCHIVOS INCLUIDOS

| Archivo | Propósito | Cuándo Usar |
|---------|-----------|-------------|
| `drop_tables_instituto.sql` | Eliminar tablas existentes | Antes de migrar o limpiar |
| `create_tables_instituto.sql` | Crear tablas nuevas | Primera instalación o después de limpiar |
| `migrate_instituto.sql` | Eliminar + Crear (completo) | Migración completa en un paso |
| `database_manager_instituto.py` | Gestor Python | Integración con Python |

---

## 🚀 OPCIÓN 1: Migración Completa (Recomendado)

Este script elimina las tablas existentes y crea las nuevas en un solo paso.

### **Desde MySQL Workbench:**

```
1. Abrir MySQL Workbench
2. Conectar a tu servidor MySQL
3. Abrir: database/migrate_instituto.sql
4. Cambiar línea 43 a: SOURCE /ruta/completa/a/create_tables_instituto.sql
5. Ejecutar (⚡ icono Execute)
```

### **Desde Línea de Comandos:**

```bash
# Opción A: Ejecutar script completo
mysql -u root -p tngcore < database/migrate_instituto.sql

# Opción B: Paso por paso
# 1. Eliminar tablas existentes
mysql -u root -p tngcore < database/drop_tables_instituto.sql

# 2. Crear tablas nuevas
mysql -u root -p tngcore < database/create_tables_instituto.sql
```

---

## 🔧 OPCIÓN 2: Paso por Paso

### **Paso 1: Eliminar Tablas Existentes**

**¿Cuándo usar?**
- Tienes tablas antiguas con prefijo `instituto_`
- Quieres limpiar antes de crear nuevas
- Necesitas empezar desde cero

**Ejecución:**

```bash
mysql -u root -p tngcore < database/drop_tables_instituto.sql
```

**Verificar:**

```sql
-- En MySQL Workbench o línea de comandos
USE tngcore;
SHOW TABLES LIKE 'instituto_%';
-- Debería mostrar 0 tablas
```

### **Paso 2: Crear Tablas Nuevas**

**¿Cuándo usar?**
- Después de eliminar tablas antiguas
- Primera instalación en base de datos limpia
- Actualizar estructura de tablas

**Ejecución:**

```bash
mysql -u root -p tngcore < database/create_tables_instituto.sql
```

**Verificar:**

```sql
USE tngcore;

-- Ver tablas creadas
SHOW TABLES LIKE 'instituto_%';

-- Ver vistas creadas
SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW' AND Tables_in_tngcore LIKE 'vw_instituto_%';

-- Ver procedimientos
SHOW PROCEDURE STATUS WHERE Db = 'tngcore' AND Name LIKE 'sp_instituto_%';
```

---

## 📊 VERIFICACIÓN

Después de ejecutar los scripts, verificar que todo se creó correctamente:

### **Método 1: SQL**

```sql
USE tngcore;

-- Contar tablas (debería ser 14)
SELECT COUNT(*) as TablasCreadas
FROM information_schema.tables
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'instituto_%';

-- Contar vistas (debería ser 3)
SELECT COUNT(*) as VistasCreadas
FROM information_schema.views
WHERE table_schema = 'tngcore' AND TABLE_NAME LIKE 'vw_instituto_%';

-- Contar procedimientos (debería ser 3)
SELECT COUNT(*) as ProcedimientosCreados
FROM information_schema.routines
WHERE routine_schema = 'tngcore' AND ROUTINE_NAME LIKE 'sp_instituto_%';

-- Ver datos iniciales
SELECT * FROM instituto_Rol;
SELECT * FROM instituto_UnidadDeNegocio;
```

### **Método 2: Python**

```bash
python database/database_manager_instituto.py
```

Salida esperada:
```
=========================================================
INSTITUTO SMART REPORTS - DATABASE MANAGER
Base de datos: tngcore
Prefijo de tablas: instituto_
=========================================================

📊 Consultando unidades de negocio...
✅ Encontradas 6 unidades de negocio:
   - ICAVE (ICAVE)
   - EIT (EIT)
   - LCT (LCT)
   - TIMSA (TIMSA)
   - HPMX (HPMX)
   - TNG (TNG)

✅ SISTEMA FUNCIONANDO CORRECTAMENTE
```

---

## 🐍 USO DESDE PYTHON

### **Configuración:**

```python
from database.database_manager_instituto import InstitutoSmartReportsDB, DatabaseConfig

# Configurar conexión a tngcore
config = DatabaseConfig(
    host='localhost',
    database='tngcore',
    user='root',
    password='tu_password',
    port=3306
)

# Inicializar
db = InstitutoSmartReportsDB(config)
```

### **Ejemplos de Uso:**

```python
# Listar usuarios
usuarios = db.usuarios.listar_usuarios()
print(f"Total usuarios: {len(usuarios)}")

# Obtener progreso de un usuario
progreso = db.progreso.obtener_progreso_usuario('jperez')
for p in progreso:
    print(f"{p['NombreModulo']}: {p['PorcentajeAvance']}%")

# Listar módulos
modulos = db.modulos.listar_modulos()
for m in modulos:
    print(f"- {m['NombreModulo']}")

# Generar reporte
reporte = db.reportes.reporte_cumplimiento_unidad()
for r in reporte:
    print(f"{r['NombreUnidad']}: {r['PorcentajeCumplimiento']}% cumplimiento")

# Cerrar al terminar
db.close()
```

---

## 📝 ESTRUCTURA CREADA

### **Tablas (14):**

```
instituto_Rol
instituto_UnidadDeNegocio
instituto_Departamento
instituto_Usuario
instituto_Modulo
instituto_ModuloDepartamento
instituto_ProgresoModulo
instituto_Evaluacion
instituto_ResultadoEvaluacion
instituto_HistorialProgreso
instituto_AuditoriaAcceso
instituto_Soporte
instituto_ReporteGuardado
instituto_Notificacion
instituto_Certificado
instituto_RecursoModulo
```

### **Vistas (3):**

```
vw_instituto_UsuarioProgresoCompleto
vw_instituto_ModulosPorDepartamento
vw_instituto_EstadisticasEvaluaciones
```

### **Procedimientos (3):**

```
sp_instituto_AsignarModuloUsuario
sp_instituto_ActualizarProgreso
sp_instituto_RegistrarResultadoEvaluacion
```

### **Triggers (3):**

```
trg_instituto_ActualizarUltimoAcceso
trg_instituto_NotificarAsignacionModulo
trg_instituto_NotificarVencimiento
```

---

## 🔐 DATOS INICIALES

El script crea automáticamente:

### **Roles:**
- Administrador
- Gerente
- Instructor
- Usuario
- Soporte

### **Unidades de Negocio:**
- ICAVE
- EIT
- LCT
- TIMSA
- HPMX
- TNG

---

## ⚠️ IMPORTANTE - ANTES DE EJECUTAR

### **1. Backup de Datos**

Si ya tienes datos en tablas `instituto_*`, haz backup:

```bash
# Backup de todas las tablas instituto_
mysqldump -u root -p tngcore \
  instituto_Rol \
  instituto_UnidadDeNegocio \
  instituto_Departamento \
  instituto_Usuario \
  instituto_Modulo \
  instituto_ProgresoModulo \
  > backup_instituto_$(date +%Y%m%d).sql

# Restaurar si es necesario
mysql -u root -p tngcore < backup_instituto_20250709.sql
```

### **2. Verificar Conexión**

```bash
# Probar conexión a MySQL
mysql -u root -p -e "SHOW DATABASES;"

# Verificar que existe tngcore
mysql -u root -p -e "USE tngcore; SHOW TABLES;"
```

### **3. Permisos**

Asegurar que tienes permisos para:
- Crear/eliminar tablas
- Crear vistas
- Crear procedimientos almacenados
- Crear triggers

```sql
-- Verificar permisos
SHOW GRANTS FOR 'root'@'localhost';
```

---

## 🐛 TROUBLESHOOTING

### **Error: Database doesn't exist**

```sql
-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS tngcore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

### **Error: Access denied**

```bash
# Verificar usuario y password
mysql -u root -p

# Si olvidaste el password
# Windows: mysql --defaults-file="C:\ProgramData\MySQL\MySQL Server 8.0\my.ini" -u root
# Linux: sudo mysql -u root
```

### **Error: Table already exists**

```bash
# Usar script de limpieza primero
mysql -u root -p tngcore < database/drop_tables_instituto.sql

# Luego crear
mysql -u root -p tngcore < database/create_tables_instituto.sql
```

### **Error: Foreign key constraint fails**

El script desactiva temporalmente foreign keys durante la eliminación. Si tienes problemas:

```sql
SET FOREIGN_KEY_CHECKS = 0;
-- Ejecutar tus queries
SET FOREIGN_KEY_CHECKS = 1;
```

---

## 📊 QUERIES ÚTILES

### **Ver Estructura de Tabla:**

```sql
DESCRIBE instituto_Usuario;
SHOW CREATE TABLE instituto_Usuario;
```

### **Ver Datos de Ejemplo:**

```sql
-- Ver roles
SELECT * FROM instituto_Rol;

-- Ver unidades de negocio
SELECT * FROM instituto_UnidadDeNegocio;

-- Ver usuarios con sus relaciones
SELECT
    u.UserId,
    u.NombreCompleto,
    un.NombreUnidad,
    d.NombreDepartamento,
    r.NombreRol
FROM instituto_Usuario u
LEFT JOIN instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
LEFT JOIN instituto_Departamento d ON u.IdDepartamento = d.IdDepartamento
LEFT JOIN instituto_Rol r ON u.IdRol = r.IdRol;
```

### **Ver Estadísticas:**

```sql
-- Contar registros por tabla
SELECT 'Usuarios' AS Tabla, COUNT(*) AS Total FROM instituto_Usuario
UNION ALL
SELECT 'Módulos', COUNT(*) FROM instituto_Modulo
UNION ALL
SELECT 'Departamentos', COUNT(*) FROM instituto_Departamento
UNION ALL
SELECT 'Unidades', COUNT(*) FROM instituto_UnidadDeNegocio;
```

---

## 🎯 PRÓXIMOS PASOS

Después de ejecutar la migración:

1. **Insertar tus datos:**
   ```sql
   -- Ejemplo: Agregar departamentos
   INSERT INTO instituto_Departamento (IdUnidadDeNegocio, NombreDepartamento, Codigo)
   VALUES (1, 'Recursos Humanos', 'RH');
   ```

2. **Crear usuarios:**
   ```python
   from database.database_manager_instituto import InstitutoSmartReportsDB, DatabaseConfig

   db = InstitutoSmartReportsDB(config)

   nuevo_usuario = {
       'UserId': 'jperez',
       'NombreCompleto': 'Juan Pérez',
       'UserEmail': 'jperez@hutchison.com',
       'Password': 'temp123',
       'IdUnidadDeNegocio': 1,
       'IdDepartamento': 1,
       'IdRol': 4
   }

   db.usuarios.crear_usuario(nuevo_usuario)
   ```

3. **Integrar con tu aplicación:**
   ```python
   # En tu main.py
   from database.database_manager_instituto import InstitutoSmartReportsDB, DatabaseConfig

   # Configurar
   db_config = DatabaseConfig(
       host='localhost',
       database='tngcore',
       user='root',
       password=os.environ.get('DB_PASSWORD')
   )

   # Inicializar
   db = InstitutoSmartReportsDB(db_config)

   # Usar en toda la aplicación
   usuarios = db.usuarios.listar_usuarios()
   ```

---

## 📚 RECURSOS ADICIONALES

- **Análisis del Modelo:** `ANALISIS_MODELO_ER.md`
- **Script Original:** `create_database_mysql.sql`
- **Manager Original:** `database_manager.py`
- **Documentación General:** `README.md`

---

## ✅ CHECKLIST

Antes de considerar completada la migración, verifica:

- [ ] Base de datos tngcore existe
- [ ] Script de eliminación ejecutado sin errores
- [ ] Script de creación ejecutado sin errores
- [ ] 14 tablas creadas con prefijo instituto_
- [ ] 3 vistas creadas con prefijo vw_instituto_
- [ ] 3 procedimientos creados con prefijo sp_instituto_
- [ ] 3 triggers creados
- [ ] Datos iniciales insertados (roles, unidades)
- [ ] Script Python funciona correctamente
- [ ] Backup de datos antiguo guardado (si aplica)

---

**¡Migración lista! Tu base de datos tngcore está configurada con el prefijo instituto_** 🚀
