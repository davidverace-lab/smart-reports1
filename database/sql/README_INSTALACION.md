# 🚀 Instalación de Base de Datos - Smart Reports

## 📋 Scripts SQL incluidos

Este directorio contiene los scripts SQL para configurar completamente la base de datos de Smart Reports:

### 1. **01_unidades_negocio.sql**
Crea y configura las Unidades de Negocio de Hutchison Ports:
- ✅ Tabla `instituto_UnidadNegocio`
- ✅ 8 unidades de negocio (terminales, logística, admin, RRHH, TI, seguridad)
- ✅ Vinculación con tabla de usuarios
- ✅ Vista `vw_UsuariosConUnidad`

### 2. **02_sistema_roles.sql**
Implementa el sistema completo de roles y permisos:
- ✅ Tabla `instituto_Rol`
- ✅ Tabla `instituto_Permiso`
- ✅ Tabla `instituto_RolPermiso`
- ✅ 4 roles: Admin, RRHH, Gerente, Operador
- ✅ 16 permisos granulares
- ✅ 2 usuarios por defecto:
  - **Admin**: `admin@hutchison.com` / `admin123`
  - **RRHH**: `rrhh@hutchison.com` / `rrhh123`
- ✅ Vista `vw_UsuariosConRoles`
- ✅ Función `fn_UsuarioTienePermiso`

### 3. **03_usuarios_ejemplo_30.sql**
Genera 30 usuarios de ejemplo con datos reales:
- ✅ 30 empleados distribuidos en 8 unidades de negocio
- ✅ Nombres, cargos y departamentos realistas
- ✅ 3-8 módulos completados por usuario
- ✅ Calificaciones entre 80-98 puntos
- ✅ Fechas de capacitación Enero-Julio 2024
- ✅ ~180+ registros de módulos finalizados

---

## ⚙️ Orden de Ejecución

**IMPORTANTE**: Ejecutar los scripts en este orden:

```sql
-- 1. Crear unidades de negocio
:r 01_unidades_negocio.sql
GO

-- 2. Crear sistema de roles
:r 02_sistema_roles.sql
GO

-- 3. Insertar usuarios de ejemplo
:r 03_usuarios_ejemplo_30.sql
GO
```

---

## 📝 Instrucciones de Instalación

### Opción A: SQL Server Management Studio (SSMS)

1. Abrir SSMS y conectarse a tu servidor
2. Abrir cada archivo .sql en el orden indicado
3. Verificar que estás en la base de datos correcta: `USE SmartReports;`
4. Ejecutar (F5) cada script
5. Verificar los mensajes de éxito: `✅ CONFIGURADO`

### Opción B: Línea de comandos (sqlcmd)

```bash
# Ejecutar todos los scripts en orden
sqlcmd -S localhost -d SmartReports -i 01_unidades_negocio.sql
sqlcmd -S localhost -d SmartReports -i 02_sistema_roles.sql
sqlcmd -S localhost -d SmartReports -i 03_usuarios_ejemplo_30.sql
```

### Opción C: Ejecutar todo de una vez

Crear un archivo `install_all.sql`:

```sql
USE SmartReports;
GO

:r 01_unidades_negocio.sql
:r 02_sistema_roles.sql
:r 03_usuarios_ejemplo_30.sql

PRINT '';
PRINT '============================================';
PRINT '✅ INSTALACIÓN COMPLETA FINALIZADA';
PRINT '============================================';
```

Luego ejecutar:
```bash
sqlcmd -S localhost -d SmartReports -i install_all.sql
```

---

## ✅ Verificación de Instalación

Ejecutar estas consultas para verificar:

```sql
-- Verificar unidades de negocio
SELECT COUNT(*) as TotalUnidades FROM instituto_UnidadNegocio;
-- Esperado: 8

-- Verificar roles
SELECT COUNT(*) as TotalRoles FROM instituto_Rol;
-- Esperado: 4

-- Verificar permisos
SELECT COUNT(*) as TotalPermisos FROM instituto_Permiso;
-- Esperado: 16

-- Verificar usuarios
SELECT COUNT(*) as TotalUsuarios FROM instituto_Usuario WHERE Activo = 1;
-- Esperado: 32 (30 ejemplo + admin + rrhh)

-- Verificar módulos completados
SELECT COUNT(*) as ModulosCompletados FROM instituto_UsuarioModulo WHERE Progreso = 100;
-- Esperado: 180+

-- Ver usuarios con roles
SELECT * FROM vw_UsuariosConRoles;
```

---

## 👥 Usuarios Creados

### Usuarios del Sistema
| Email | Contraseña | Rol | Descripción |
|-------|------------|-----|-------------|
| admin@hutchison.com | admin123 | Admin | Acceso total |
| rrhh@hutchison.com | rrhh123 | RRHH | Vista RRHH especializada |

### Usuarios de Ejemplo (30 total)
| Email | Contraseña | Departamento | Unidad |
|-------|------------|--------------|--------|
| jmendez@hutchison.com | port123 | Operaciones | Terminal 1 |
| msoto@hutchison.com | port123 | Operaciones | Terminal 1 |
| psilva@hutchison.com | port123 | Operaciones | Terminal 2 |
| sherrera@hutchison.com | port123 | Logística | Logística |
| ... y 26 más | port123 | Varios | Varias |

**Todos los usuarios de ejemplo usan la contraseña: `port123`**

---

## 🎯 Roles y Permisos

### 1. Admin (Nivel 1)
- ✅ Acceso TOTAL al sistema
- ✅ Gestión de usuarios (crear, editar, eliminar)
- ✅ Configuración del sistema
- ✅ Todos los reportes y dashboards
- ✅ Gestión de roles y permisos

### 2. RRHH (Nivel 2)
- ✅ Ver, crear y editar usuarios
- ✅ Importar usuarios desde Excel
- ✅ Ver reportes de TODOS los departamentos
- ✅ Dashboards especializados de RRHH
- ❌ No puede eliminar usuarios
- ❌ No puede modificar configuración

### 3. Gerente (Nivel 2)
- ✅ Ver usuarios
- ✅ Ver y generar reportes de su departamento
- ✅ Dashboards gerenciales
- ❌ No puede crear/editar usuarios
- ❌ No puede ver otros departamentos

### 4. Operador (Nivel 3)
- ✅ Ver y exportar reportes propios
- ✅ Dashboards operativos básicos
- ❌ No puede ver usuarios
- ❌ No puede generar reportes de otros

---

## 📊 Datos Generados

### Unidades de Negocio (8)
1. Terminal Portuaria 1
2. Terminal Portuaria 2
3. Logística y Almacenamiento
4. Operaciones Terrestres
5. Administración Central
6. Recursos Humanos
7. Tecnología e Innovación
8. Seguridad y Medio Ambiente

### Distribución de Usuarios
- Terminal 1: 6 usuarios
- Terminal 2: 5 usuarios
- Logística: 5 usuarios
- Operaciones Terrestres: 4 usuarios
- Administración: 3 usuarios
- RRHH: 3 usuarios
- TI: 2 usuarios
- Seguridad: 2 usuarios

### Módulos de Capacitación
- Total módulos: 8
- Módulos completados por usuario: 3-8 (variable)
- Calificaciones: 80-98 puntos
- Período: Enero 2024 - Julio 2024

---

## 🔧 Solución de Problemas

### Error: "Tabla ya existe"
Los scripts están diseñados para ser idempotentes. Si una tabla ya existe, solo se mostrarán advertencias pero no errores.

### Error: "Foreign key constraint"
Asegúrate de ejecutar los scripts en el orden correcto (01 → 02 → 03).

### Usuarios no aparecen
Verifica que ejecutaste el script 03 completo y que no hubo errores.

### Contraseñas no funcionan
Las contraseñas en los scripts son en texto plano para desarrollo. En producción, deberías hashearlas.

---

## 📞 Soporte

Si encuentras problemas con la instalación:
1. Verifica que tienes permisos de admin en SQL Server
2. Confirma que la base de datos SmartReports existe
3. Revisa los mensajes de error en SSMS
4. Ejecuta las consultas de verificación

---

**Última actualización**: 2024-11-11
**Versión**: 2.0
