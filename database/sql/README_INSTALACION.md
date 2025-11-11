# 🚀 Instalación de Datos - Smart Reports Hutchison Ports

## 📋 Scripts SQL Adaptados a TU Base de Datos

Estos scripts están diseñados para trabajar con **TU esquema existente** de base de datos.
**NO crean tablas**, solo insertan datos.

---

## 📦 Archivos Incluidos

### 1. **01_datos_base.sql**
Inserta datos base en tu esquema existente:
- ✅ **10 Unidades de Negocio** de Hutchison Ports:
  - CCI, ECV, EIT, HPML, HPMX, ICAVE, LCTM, LCT TILH, TIMSA, TNG
- ✅ **4 Roles**:
  - Administrador (acceso total)
  - Recursos Humanos (vista RRHH)
  - Gerente (vista gerencial)
  - Usuario (vista operativa)
- ✅ **40 Departamentos** (4 por unidad)

**Usa las tablas existentes:**
- `UnidadDeNegocio` (IdUnidadDeNegocio, NombreUnidad, Activo)
- `Rol` (IdRol, NombreRol, Descripcion, Activo)
- `Departamento` (IdDepartamento, IdUnidadDeNegocio, NombreDepartamento, Activo)

### 2. **02_usuarios_30.sql**
Inserta 32 usuarios de ejemplo:
- ✅ **2 usuarios del sistema**:
  - Admin: `U001` - cmendoza@hutchison.com / admin123
  - RRHH: `U002` - plopez@hutchison.com / rrhh123
- ✅ **30 usuarios operativos** (U003-U032)
  - Distribuidos en las 10 unidades de negocio
  - 10 gerentes (1 por unidad)
  - 20 usuarios operativos
  - Contraseña: port123

**Usa la tabla existente:**
- `Usuario` (IdUsuario, UserId, IdUnidadDeNegocio, IdRol, NombreCompleto, UserEmail, PasswordHash, Division, Position, UserStatus, etc.)

### 3. **03_modulos_progreso.sql**
Inserta módulos de capacitación y progreso:
- ✅ **8 Módulos** de capacitación
- ✅ **~150+ registros de progreso** (3-8 módulos por usuario)
- ✅ **Evaluaciones** (1 por módulo)
- ✅ **Resultados** con calificaciones 80-98 puntos

**Usa las tablas existentes:**
- `Modulo` (IdModulo, NombreModulo, FechaInicioModulo, FechaCierre, Activo)
- `ProgresoModulo` (IdInscripcion, UserId, IdModulo, EstatusModulo, FechaAsignacion, FechaFinalizacion)
- `Evaluacion` (IdEvaluacion, IdModulo, NombreEvaluacion, PuntajeMinimoAprobatorio)
- `ResultadoEvaluacion` (IdResultado, IdInscripcion, IdEvaluacion, PuntajeObtenido, Aprobado)

---

## ⚙️ Orden de Ejecución

**IMPORTANTE**: Ejecutar en este orden:

```sql
-- 1. Datos base (unidades, roles, departamentos)
USE SmartReports;
GO
:r 01_datos_base.sql
GO

-- 2. Usuarios
:r 02_usuarios_30.sql
GO

-- 3. Módulos y progreso
:r 03_modulos_progreso.sql
GO
```

---

## 📝 Instrucciones Paso a Paso

### Opción A: SQL Server Management Studio (SSMS)

1. Abrir SSMS y conectarse al servidor
2. Abrir script `01_datos_base.sql`
3. Asegurarse de que esté seleccionada la base de datos **SmartReports**
4. Ejecutar (F5)
5. Repetir con `02_usuarios_30.sql` y `03_modulos_progreso.sql`
6. Verificar mensajes de éxito: `✅ CONFIGURADO`

### Opción B: Línea de comandos (sqlcmd)

```bash
# Navegar a la carpeta de scripts
cd database/sql

# Ejecutar cada script en orden
sqlcmd -S localhost -d SmartReports -i 01_datos_base.sql
sqlcmd -S localhost -d SmartReports -i 02_usuarios_30.sql
sqlcmd -S localhost -d SmartReports -i 03_modulos_progreso.sql
```

### Opción C: Todo de una vez

Crear archivo `install_all.sql`:

```sql
USE SmartReports;
GO

:r 01_datos_base.sql
:r 02_usuarios_30.sql
:r 03_modulos_progreso.sql

PRINT '';
PRINT '============================================';
PRINT '✅ INSTALACIÓN COMPLETA';
PRINT '============================================';
```

Ejecutar:
```bash
sqlcmd -S localhost -d SmartReports -i install_all.sql
```

---

## ✅ Verificación de Instalación

Ejecutar estas consultas para verificar:

```sql
-- Verificar unidades de negocio
SELECT COUNT(*) as TotalUnidades FROM UnidadDeNegocio;
-- Esperado: 10

-- Verificar roles
SELECT COUNT(*) as TotalRoles FROM Rol;
-- Esperado: 4

-- Verificar departamentos
SELECT COUNT(*) as TotalDepartamentos FROM Departamento;
-- Esperado: 40

-- Verificar usuarios
SELECT COUNT(*) as TotalUsuarios FROM Usuario WHERE UserStatus = 'Active';
-- Esperado: 32

-- Verificar módulos
SELECT COUNT(*) as TotalModulos FROM Modulo WHERE Activo = 1;
-- Esperado: 8

-- Verificar progreso
SELECT COUNT(*) as ProgresoRegistrado FROM ProgresoModulo WHERE EstatusModulo = 'Completado';
-- Esperado: 150+

-- Ver usuarios creados
SELECT UserId, NombreCompleto, UserEmail FROM Usuario ORDER BY IdUsuario;
```

---

## 👥 Usuarios Creados

### Usuarios del Sistema

| UserId | Email | Contraseña | Rol | Unidad |
|--------|-------|------------|-----|--------|
| U001 | cmendoza@hutchison.com | admin123 | Administrador | HPMX |
| U002 | plopez@hutchison.com | rrhh123 | Recursos Humanos | HPMX |

### Usuarios Operativos (30 usuarios)

| Unidad | Usuarios | Gerente | Email Ejemplo |
|--------|----------|---------|---------------|
| CCI | 3 | Juan Carlos Méndez | jmendez@hutchison.com |
| ECV | 3 | Ana Patricia Rojas | arojas@hutchison.com |
| EIT | 3 | Carlos Enrique Díaz | cdiaz@hutchison.com |
| HPML | 3 | Pedro Antonio Silva | psilva@hutchison.com |
| HPMX | 3 | Sandra Patricia Herrera | sherrera@hutchison.com |
| ICAVE | 3 | Andrés Felipe Torres | atorres@hutchison.com |
| LCTM | 3 | Diana Carolina Pérez | dperez@hutchison.com |
| LCT TILH | 3 | Hernán Paredes | hparedes@hutchison.com |
| TIMSA | 3 | Isabel Reyes | ireyes@hutchison.com |
| TNG | 3 | Oscar Mauricio León | oleon@hutchison.com |

**Contraseña para todos los usuarios:** `port123`

---

## 🎯 Unidades de Negocio Insertadas

1. **CCI** - Contecon Cartagena
2. **ECV** - Ensenada Containers Terminal
3. **EIT** - Ensenada International Terminal
4. **HPML** - Hutchison Ports Manzanillo (Lazaro Cardenas)
5. **HPMX** - Hutchison Ports Mexico
6. **ICAVE** - Icave Veracruz
7. **LCTM** - Lázaro Cárdenas Container Terminal
8. **LCT TILH** - LCT Tuxpan
9. **TIMSA** - Terminal Internacional Multiservicios
10. **TNG** - Terminal Norte de Grupo Hutchison

---

## 📊 Roles y Permisos

### 1. Administrador
- ✅ Acceso TOTAL al sistema
- ✅ Gestión de usuarios completa
- ✅ Configuración del sistema
- ✅ Todos los reportes y dashboards

### 2. Recursos Humanos
- ✅ Vista especializada RRHH
- ✅ Dashboards de personal y capacitación
- ✅ Gestión limitada de usuarios
- ✅ Reportes de todos los departamentos

### 3. Gerente
- ✅ Vista gerencial
- ✅ Dashboards estratégicos
- ✅ Reportes de su departamento
- ❌ No puede gestionar usuarios

### 4. Usuario
- ✅ Vista operativa básica
- ✅ Consulta de progreso propio
- ✅ Reportes personales
- ❌ No puede ver otros usuarios

---

## 📚 Módulos de Capacitación

1. Seguridad Industrial Básica
2. Operación de Equipos Portuarios
3. Manejo de Cargas Peligrosas
4. Gestión Logística Portuaria
5. Sistemas de Información Portuaria
6. Atención al Cliente
7. Liderazgo y Trabajo en Equipo
8. Normativa Aduanera y Comercio Exterior

---

## 🔧 Solución de Problemas

### Error: "Violation of PRIMARY KEY constraint"
Las tablas ya tienen datos. Puedes:
- Comentar las líneas `DELETE FROM` en los scripts si quieres mantener datos existentes
- O limpiar las tablas manualmente antes de ejecutar

### Error: "Cannot insert NULL into column"
Verifica que tu esquema de base de datos coincida con el esperado (campos obligatorios).

### Error: "Foreign key constraint"
Ejecuta los scripts en el orden correcto: 01 → 02 → 03

### Usuarios no aparecen
- Verifica que el script 02 se ejecutó sin errores
- Consulta: `SELECT * FROM Usuario`

---

## 🎨 Integración con la Aplicación

Los scripts están diseñados para funcionar con:
- ✅ Panel de Dashboards Gerenciales
- ✅ Panel de Dashboards RRHH
- ✅ Sistema de reportes
- ✅ Queries en `queries_hutchison.py`

Todas las consultas SQL en Python están adaptadas al esquema REAL.

---

## 📞 Notas Importantes

1. **Contraseñas en texto plano**: Los scripts usan contraseñas sin hash para desarrollo. En producción, usar `HASHBYTES('SHA2_256', 'password')`.

2. **UserId formato**: Se usa formato `U001`, `U002`, etc. (VARCHAR(50))

3. **UserStatus**: Los usuarios activos tienen `UserStatus = 'Active'`

4. **EstatusModulo**: Los módulos completados tienen `EstatusModulo = 'Completado'`

5. **Fechas**: Todas las fechas están en formato `YYYY-MM-DD` o `DATETIME`

---

**Última actualización**: 2024-11-11
**Versión**: 2.0 - Adaptado al esquema REAL de Hutchison Ports
