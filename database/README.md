# 🗄️ Base de Datos - Smart Reports Instituto

Sistema de base de datos MySQL para **tngcore** con prefijo **instituto_**

---

## 📁 ARCHIVOS

| Archivo | Descripción |
|---------|-------------|
| `create_tables_instituto.sql` | Crea todas las tablas con prefijo instituto_ |
| `drop_tables_instituto.sql` | Elimina todas las tablas instituto_ |
| `database_manager_instituto.py` | Gestor Python para base de datos |
| `importar_usuarios_excel.py` | Importa usuarios desde Excel a CSV |
| `GUIA_MIGRACION_INSTITUTO.md` | Guía completa de uso |

---

## 🚀 INICIO RÁPIDO

### **1. Crear Tablas**

```bash
mysql -u root -p tngcore < create_tables_instituto.sql
```

### **2. Importar Usuarios desde Excel**

```bash
# Coloca tu archivo Excel en esta carpeta
python importar_usuarios_excel.py archivo_usuarios.xlsx
```

Esto genera:
- ✅ `usuarios_importacion.csv` - Archivo CSV listo
- ✅ `usuarios_importacion.sql` - Script de importación

### **3. Importar CSV a MySQL**

**Opción A: MySQL Workbench**
```
1. Clic derecho en tabla instituto_Usuario
2. Table Data Import Wizard
3. Seleccionar usuarios_importacion.csv
4. Importar
```

**Opción B: Línea de comandos**
```bash
mysql -u root -p tngcore < usuarios_importacion.sql
```

---

## 📊 ESTRUCTURA

### **Tablas (14)**
```
instituto_Rol
instituto_UnidadDeNegocio (ICAVE, EIT, LCT, TIMSA, HPMX, TNG)
instituto_Departamento
instituto_Usuario ⭐
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

### **Vistas (3)**
```
vw_instituto_UsuarioProgresoCompleto
vw_instituto_ModulosPorDepartamento
vw_instituto_EstadisticasEvaluaciones
```

### **Procedimientos (3)**
```
sp_instituto_AsignarModuloUsuario
sp_instituto_ActualizarProgreso
sp_instituto_RegistrarResultadoEvaluacion
```

---

## 🐍 USO CON PYTHON

```python
from database_manager_instituto import InstitutoSmartReportsDB, DatabaseConfig

# Configurar
config = DatabaseConfig(
    host='localhost',
    database='tngcore',
    user='root',
    password='tu_password'
)

# Inicializar
db = InstitutoSmartReportsDB(config)

# Listar usuarios
usuarios = db.usuarios.listar_usuarios()

# Listar módulos
modulos = db.modulos.listar_modulos()

# Obtener progreso
progreso = db.progreso.obtener_progreso_usuario('jperez')

# Cerrar
db.close()
```

---

## 📝 COMANDOS ÚTILES

### **Ver Estado**

```sql
USE tngcore;

-- Contar usuarios
SELECT COUNT(*) FROM instituto_Usuario;

-- Ver unidades de negocio
SELECT * FROM instituto_UnidadDeNegocio;

-- Ver usuarios activos
SELECT UserId, NombreCompleto, UserEmail
FROM instituto_Usuario
WHERE Activo = 1
LIMIT 10;
```

### **Limpiar y Recrear**

```bash
# 1. Eliminar tablas
mysql -u root -p tngcore < drop_tables_instituto.sql

# 2. Crear tablas nuevas
mysql -u root -p tngcore < create_tables_instituto.sql
```

---

## ⚠️ IMPORTANTE

### **Antes de Eliminar Tablas**

```bash
# Hacer backup
mysqldump -u root -p tngcore \
  --tables instituto_Usuario instituto_Modulo instituto_ProgresoModulo \
  > backup_$(date +%Y%m%d).sql
```

### **Restaurar Backup**

```bash
mysql -u root -p tngcore < backup_20250709.sql
```

---

## 🔐 SEGURIDAD

### **Cambiar Passwords por Defecto**

Los usuarios importados tienen passwords temporales. Cambiar en primer login:

```sql
-- Actualizar password de un usuario
UPDATE instituto_Usuario
SET PasswordHash = SHA2('nueva_contraseña', 256)
WHERE UserId = 'jperez';
```

### **Crear Usuario de Aplicación**

```sql
CREATE USER 'smartreports_app'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT SELECT, INSERT, UPDATE, DELETE ON tngcore.instituto_* TO 'smartreports_app'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Ver **`GUIA_MIGRACION_INSTITUTO.md`** para:
- Instrucciones detalladas
- Troubleshooting
- Ejemplos avanzados
- Queries útiles

---

## 🐛 TROUBLESHOOTING

### **Error: Table already exists**

```bash
mysql -u root -p tngcore < drop_tables_instituto.sql
mysql -u root -p tngcore < create_tables_instituto.sql
```

### **Error: Access denied**

```bash
# Verificar usuario y password
mysql -u root -p
```

### **Error: Database doesn't exist**

```sql
CREATE DATABASE tngcore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

**¡Sistema listo!** 🚀

Para ayuda: Consulta `GUIA_MIGRACION_INSTITUTO.md`
