# 📘 GUÍA COMPLETA: SISTEMA ETL + BASE DE DATOS - SMART REPORTS

## 📋 TABLA DE CONTENIDOS

1. [Introducción al Sistema ETL](#1-introducción-al-sistema-etl)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Base de Datos - Estructura Completa](#3-base-de-datos---estructura-completa)
4. [Scripts SQL/MySQL](#4-scripts-sqlmysql)
5. [Cómo Funciona el Mapeo de Datos](#5-cómo-funciona-el-mapeo-de-datos)
6. [Guía Paso a Paso para Importar Datos](#6-guía-paso-a-paso-para-importar-datos)
7. [Sistema de Cruce de Datos](#7-sistema-de-cruce-de-datos)
8. [Troubleshooting](#8-troubleshooting)

---

# 1. INTRODUCCIÓN AL SISTEMA ETL

## ¿Qué es ETL?

**ETL** significa **E**xtract, **T**ransform, **L**oad (Extraer, Transformar, Cargar):

- **Extract (Extraer)**: Lee archivos Excel de CSOD (Cornerstone OnDemand)
- **Transform (Transformar)**: Limpia, valida y mapea los datos al formato de la BD
- **Load (Cargar)**: Inserta los datos en MySQL/SQL Server

## Archivos que Procesa

El sistema ETL procesa **2 archivos Excel** de CSOD:

### 1. Enterprise Training Report
**Nombre**: `Enterprise_Training_Report_YYYYMMDD_HHMMSS.xlsx`

**Contiene**:
- Progreso de capacitaciones de cada usuario
- Calificaciones de módulos
- Fechas de inicio/finalización
- Estados (Terminado, En Progreso, etc.)

**Columnas principales**:
- User ID (ID único del usuario)
- Training Title (Nombre del módulo)
- Completion Status (Estado)
- Start Date (Fecha de inicio)
- Completion Date (Fecha de finalización)
- Score (Calificación 0-100)

### 2. CSOD Org Planning
**Nombre**: `CSOD_Data_Source_for_Org_Planning_YYYYMMDD.xlsx`

**Contiene**:
- Información de usuarios (empleados)
- Cargos y departamentos
- Unidades de negocio
- Estructura organizacional

**Columnas principales**:
- User ID
- Full Name (Nombre completo)
- Email
- Position (Cargo)
- Department (Departamento)
- Division (Unidad de negocio)
- Location (Ubicación)

---

# 2. ARQUITECTURA DEL SISTEMA

## Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                  ARCHIVOS EXCEL (CSOD)                      │
│  Enterprise_Training_Report.xlsx  +  Org_Planning.xlsx     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              1. EXTRACCIÓN (Extract)                        │
│  • Lee archivos Excel con pandas                            │
│  • Detecta columnas automáticamente (ESP/ENG)               │
│  • Valida estructura de archivos                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            2. TRANSFORMACIÓN (Transform)                    │
│  • Limpia datos (espacios, acentos, mayúsculas)            │
│  • Mapea módulos (matching inteligente)                    │
│  • Valida con Pydantic (tipos, rangos)                     │
│  • Normaliza fechas y calificaciones                       │
│  • Crea registros faltantes automáticamente                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                3. CARGA (Load)                              │
│  • Inserta empleados en tabla `empleados`                   │
│  • Crea módulos en tabla `modulos` (si no existen)         │
│  • Registra progreso en `progreso_modulos`                  │
│  • Batch inserts (1000 registros a la vez)                 │
│  • Transacciones con rollback automático si falla          │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. **ETL Core** (`smart_reports/etl/etl_instituto_completo.py`)
- Motor principal del ETL
- Clases:
  - `InstitutoETL`: Clase principal que orquesta todo
  - `UsuarioExcel`: Modelo de validación para usuarios
  - `ProgresoModuloExcel`: Modelo de validación para progreso

### 2. **Panel de Importación** (`panel_importacion_datos.py`)
- Interfaz gráfica para el ETL
- Funciones:
  - Preview de archivos Excel
  - Validación de estructura
  - Matching de columnas (mapeo manual)
  - Botones de importación
  - Sistema de logs en tiempo real

### 3. **Sistema de Rollback** (`sistema_rollback.py`)
- Crea backups antes de importar
- Permite restaurar datos anteriores
- Historial de importaciones

---

# 3. BASE DE DATOS - ESTRUCTURA COMPLETA

## Diagrama Entidad-Relación

```
┌──────────────┐          ┌──────────────┐          ┌────────────────┐
│   EMPLEADOS  │          │   MODULOS    │          │ PROGRESO_      │
│              │          │              │          │ MODULOS        │
├──────────────┤          ├──────────────┤          ├────────────────┤
│ id (PK)      │          │ id (PK)      │          │ id (PK)        │
│ user_id (UK) │◄────┐    │ numero       │◄────┐    │ empleado_id(FK)│
│ nombre       │     │    │ titulo       │     │    │ modulo_id (FK) │
│ email        │     │    │ descripcion  │     │    │ estado         │
│ cargo        │     │    │ orden        │     │    │ calificacion   │
│ departamento │     │    │ puntaje_min  │     │    │ fecha_inicio   │
│ unidad       │     │    │ activo       │     │    │ fecha_fin      │
│ ubicacion    │     │    │ ...          │     │    │ intentos       │
│ activo       │     │    └──────────────┘     │    │ aprobado       │
│ rol_id       │     │                         │    │ ...            │
└──────────────┘     │                         │    └────────────────┘
       │             └─────────────────────────┴───────────┘
       │                    (relaciones FK)
       │
       ▼
┌──────────────┐
│    ROLES     │
│              │
├──────────────┤
│ id (PK)      │
│ nombre       │
│ descripcion  │
│ nivel_acceso │
└──────────────┘
```

## Tablas Principales

### 1. **empleados** (Tabla de Usuarios)
Almacena toda la información de los empleados que toman capacitaciones.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT AUTO_INCREMENT | ID interno (PK) |
| `user_id` | VARCHAR(100) | ID de CSOD - **MASTER KEY** |
| `nombre_completo` | VARCHAR(200) | Nombre del empleado |
| `email` | VARCHAR(200) | Email corporativo |
| `cargo` | VARCHAR(150) | Puesto/posición |
| `departamento` | VARCHAR(150) | Departamento |
| `unidad_negocio` | VARCHAR(150) | División/Unidad |
| `ubicacion` | VARCHAR(150) | Oficina/sede |
| `nivel` | VARCHAR(100) | Nivel jerárquico |
| `activo` | TINYINT(1) | 1=activo, 0=inactivo |
| `rol_id` | INT | FK a tabla roles |
| `fecha_creacion` | DATETIME | Timestamp de creación |
| `fecha_actualizacion` | DATETIME | Última modificación |

**Índices**:
- PRIMARY KEY: `id`
- UNIQUE KEY: `user_id` (no se permiten duplicados)
- INDEX: `email`, `unidad_negocio`, `activo`

### 2. **modulos** (Catálogo de Módulos)
Catálogo de los 14 módulos de capacitación del Instituto.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT AUTO_INCREMENT | ID interno (PK) |
| `numero_modulo` | INT | Número del módulo (1-14) |
| `titulo` | VARCHAR(300) | Nombre completo |
| `descripcion` | TEXT | Descripción detallada |
| `orden` | INT | Orden de visualización |
| `duracion_estimada` | INT | Horas estimadas |
| `puntaje_minimo` | DECIMAL(5,2) | Calificación mínima (70.0) |
| `intentos_permitidos` | INT | Intentos máximos (3) |
| `activo` | TINYINT(1) | 1=activo, 0=inactivo |
| `fecha_creacion` | DATETIME | Timestamp de creación |

**Módulos Existentes**:
1. INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS
2. SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO
3. INTRODUCCIÓN A LAS OPERACIONES
4. RELACIONES LABORALES
5. SEGURIDAD EN LAS OPERACIONES
6. CIBERSEGURIDAD
7. ENTORNO LABORAL SALUDABLE
8. PROCESOS DE RECURSOS HUMANOS
9. PROGRAMAS DE BIENESTAR INTEGRAL
10. DESARROLLO DE NUEVOS PRODUCTOS
11. PRODUCTOS DIGITALES DE HP
12. TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD
13. ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA
14. SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA

### 3. **progreso_modulos** (Progreso de Capacitaciones)
Registra el progreso de cada empleado en cada módulo.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT AUTO_INCREMENT | ID interno (PK) |
| `empleado_id` | INT | FK a empleados.id |
| `modulo_id` | INT | FK a modulos.id |
| `estado` | ENUM | Terminado/En progreso/etc. |
| `calificacion` | DECIMAL(5,2) | Puntaje 0-100 |
| `fecha_inicio` | DATETIME | Cuándo empezó |
| `fecha_finalizacion` | DATETIME | Cuándo terminó |
| `fecha_registro` | DATETIME | Cuándo se registró |
| `intentos_realizados` | INT | Número de intentos |
| `aprobado` | TINYINT(1) | 1=aprobado, 0=reprobado |
| `tipo_capacitacion` | VARCHAR(50) | Curriculum/Prueba |
| `fecha_creacion` | DATETIME | Timestamp de creación |
| `fecha_actualizacion` | DATETIME | Última modificación |

**Estados Posibles**:
- `Terminado`: Completado con calificación
- `En progreso`: Iniciado pero no terminado
- `Registrado`: Asignado pero no iniciado
- `No iniciado`: No ha empezado

### 4. **roles** (Roles de Usuario)
Catálogo de roles del sistema.

| ID | Nombre | Nivel Acceso |
|----|--------|--------------|
| 1 | Super Administrador | 100 |
| 2 | Administrador | 80 |
| 3 | Supervisor | 60 |
| 4 | Usuario | 40 |
| 5 | Invitado | 20 |

---

# 4. SCRIPTS SQL/MySQL

## 4.1. Script Completo para MySQL

```sql
-- ============================================================================
-- SMART REPORTS - INSTITUTO HUTCHISON PORTS
-- Script de Creación de Base de Datos - MySQL
-- ============================================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS InstitutoHutchison
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE InstitutoHutchison;

-- ============================================================================
-- TABLA: roles
-- ============================================================================
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    nivel_acceso INT NOT NULL DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE INDEX idx_nombre (nombre),
    INDEX idx_nivel (nivel_acceso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de roles del sistema';

-- Insertar roles por defecto
INSERT INTO roles (id, nombre, descripcion, nivel_acceso) VALUES
(1, 'Super Administrador', 'Acceso total al sistema', 100),
(2, 'Administrador', 'Gestión de usuarios y reportes', 80),
(3, 'Supervisor', 'Visualización y reportes', 60),
(4, 'Usuario', 'Acceso básico al sistema', 40),
(5, 'Invitado', 'Solo lectura', 20)
ON DUPLICATE KEY UPDATE 
    descripcion = VALUES(descripcion),
    nivel_acceso = VALUES(nivel_acceso);

-- ============================================================================
-- TABLA: empleados
-- ============================================================================
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL UNIQUE COMMENT 'ID de CSOD - MASTER KEY',
    nombre_completo VARCHAR(200),
    email VARCHAR(200),
    cargo VARCHAR(150) COMMENT 'Position/Puesto',
    departamento VARCHAR(150),
    unidad_negocio VARCHAR(150) COMMENT 'Division/Business Unit',
    ubicacion VARCHAR(150) COMMENT 'Location/Office',
    nivel VARCHAR(100) COMMENT 'Nivel jerárquico',
    activo TINYINT(1) DEFAULT 1 COMMENT '1=activo, 0=inactivo',
    rol_id INT DEFAULT 4 COMMENT 'FK a roles (4=Usuario por defecto)',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE INDEX idx_user_id (user_id),
    INDEX idx_email (email),
    INDEX idx_unidad (unidad_negocio),
    INDEX idx_activo (activo),
    INDEX idx_departamento (departamento),
    
    FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Empleados del Instituto Hutchison Ports';

-- ============================================================================
-- TABLA: modulos
-- ============================================================================
CREATE TABLE IF NOT EXISTS modulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_modulo INT NOT NULL UNIQUE COMMENT 'Número del módulo (1-14)',
    titulo VARCHAR(300) NOT NULL COMMENT 'Título completo del módulo',
    descripcion TEXT COMMENT 'Descripción detallada',
    orden INT DEFAULT 0 COMMENT 'Orden de visualización',
    duracion_estimada INT DEFAULT 0 COMMENT 'Duración en horas',
    puntaje_minimo DECIMAL(5,2) DEFAULT 70.00 COMMENT 'Calificación mínima aprobatoria',
    intentos_permitidos INT DEFAULT 3 COMMENT 'Número máximo de intentos',
    activo TINYINT(1) DEFAULT 1 COMMENT '1=activo, 0=inactivo',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE INDEX idx_numero (numero_modulo),
    INDEX idx_titulo (titulo(100)),
    INDEX idx_activo (activo),
    INDEX idx_orden (orden)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de módulos de capacitación';

-- Insertar los 14 módulos
INSERT INTO modulos (numero_modulo, titulo, descripcion, orden, puntaje_minimo, intentos_permitidos) VALUES
(1, 'MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS', 'Introducción a la filosofía y valores corporativos', 1, 70.00, 3),
(2, 'MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', 'Compromiso ambiental y sostenibilidad', 2, 70.00, 3),
(3, 'MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES', 'Fundamentos de operaciones portuarias', 3, 70.00, 3),
(4, 'MÓDULO 4 . RELACIONES LABORALES', 'Gestión de relaciones laborales', 4, 70.00, 3),
(5, 'MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES', 'Protocolos y normativas de seguridad', 5, 70.00, 3),
(6, 'MÓDULO 6 . CIBERSEGURIDAD', 'Seguridad informática y protección de datos', 6, 70.00, 3),
(7, 'MÓDULO 7 . ENTORNO LABORAL SALUDABLE', 'Salud ocupacional y bienestar laboral', 7, 70.00, 3),
(8, 'MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS', 'Gestión de recursos humanos y talento', 8, 70.00, 3),
(9, 'MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL', 'Programas de bienestar para empleados', 9, 70.00, 3),
(10, 'MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS', 'Innovación y desarrollo de productos', 10, 70.00, 3),
(11, 'MÓDULO 11 . PRODUCTOS DIGITALES DE HP', 'Plataformas y herramientas digitales', 11, 70.00, 3),
(12, 'MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD', 'Tecnología aplicada a operaciones', 12, 70.00, 3),
(13, 'MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA', 'Protocolos de emergencia y contingencia', 13, 70.00, 3),
(14, 'MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA', 'Gestión de calidad y mejora continua', 14, 70.00, 3)
ON DUPLICATE KEY UPDATE 
    titulo = VALUES(titulo),
    descripcion = VALUES(descripcion),
    orden = VALUES(orden);

-- ============================================================================
-- TABLA: progreso_modulos
-- ============================================================================
CREATE TABLE IF NOT EXISTS progreso_modulos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL COMMENT 'FK a empleados',
    modulo_id INT NOT NULL COMMENT 'FK a modulos',
    estado ENUM('Terminado', 'En progreso', 'Registrado', 'No iniciado') DEFAULT 'No iniciado',
    calificacion DECIMAL(5,2) DEFAULT NULL COMMENT 'Puntaje 0-100',
    fecha_inicio DATETIME DEFAULT NULL,
    fecha_finalizacion DATETIME DEFAULT NULL,
    fecha_registro DATETIME DEFAULT NULL,
    intentos_realizados INT DEFAULT 0,
    aprobado TINYINT(1) DEFAULT 0 COMMENT '1=aprobado, 0=no aprobado',
    tipo_capacitacion VARCHAR(50) DEFAULT 'Curriculum' COMMENT 'Curriculum/Prueba',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_empleado (empleado_id),
    INDEX idx_modulo (modulo_id),
    INDEX idx_estado (estado),
    INDEX idx_aprobado (aprobado),
    INDEX idx_fecha_fin (fecha_finalizacion),
    UNIQUE INDEX idx_empleado_modulo (empleado_id, modulo_id),
    
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Progreso de capacitaciones de empleados';

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Progreso general por empleado
CREATE OR REPLACE VIEW vista_progreso_empleados AS
SELECT 
    e.id AS empleado_id,
    e.user_id,
    e.nombre_completo,
    e.email,
    e.unidad_negocio,
    e.departamento,
    COUNT(DISTINCT m.id) AS total_modulos,
    COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN m.id END) AS modulos_completados,
    COUNT(DISTINCT CASE WHEN p.aprobado = 1 THEN m.id END) AS modulos_aprobados,
    ROUND(
        (COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN m.id END) * 100.0) / 
        NULLIF(COUNT(DISTINCT m.id), 0), 
        2
    ) AS porcentaje_completado,
    AVG(CASE WHEN p.calificacion IS NOT NULL THEN p.calificacion END) AS calificacion_promedio
FROM empleados e
CROSS JOIN modulos m
LEFT JOIN progreso_modulos p ON e.id = p.empleado_id AND m.id = p.modulo_id
WHERE e.activo = 1 AND m.activo = 1
GROUP BY e.id, e.user_id, e.nombre_completo, e.email, e.unidad_negocio, e.departamento;

-- Vista: Progreso por unidad de negocio
CREATE OR REPLACE VIEW vista_progreso_unidades AS
SELECT 
    e.unidad_negocio,
    COUNT(DISTINCT e.id) AS total_empleados,
    COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN p.id END) AS capacitaciones_completadas,
    ROUND(AVG(CASE WHEN p.calificacion IS NOT NULL THEN p.calificacion END), 2) AS calificacion_promedio,
    ROUND(
        (COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN CONCAT(e.id, '-', m.id) END) * 100.0) / 
        NULLIF(COUNT(DISTINCT CONCAT(e.id, '-', m.id)), 0),
        2
    ) AS porcentaje_completado
FROM empleados e
CROSS JOIN modulos m
LEFT JOIN progreso_modulos p ON e.id = p.empleado_id AND m.id = p.modulo_id
WHERE e.activo = 1 AND m.activo = 1 AND e.unidad_negocio IS NOT NULL
GROUP BY e.unidad_negocio
ORDER BY porcentaje_completado DESC;

-- ============================================================================
-- CONSULTAS ÚTILES PARA REPORTES
-- ============================================================================

-- Ejemplo 1: Top 10 empleados con mejor progreso
-- SELECT * FROM vista_progreso_empleados 
-- ORDER BY porcentaje_completado DESC, calificacion_promedio DESC 
-- LIMIT 10;

-- Ejemplo 2: Módulos con menor tasa de aprobación
-- SELECT 
--     m.numero_modulo,
--     m.titulo,
--     COUNT(p.id) AS total_intentos,
--     COUNT(CASE WHEN p.aprobado = 1 THEN 1 END) AS aprobados,
--     ROUND((COUNT(CASE WHEN p.aprobado = 1 THEN 1 END) * 100.0) / COUNT(p.id), 2) AS tasa_aprobacion
-- FROM modulos m
-- LEFT JOIN progreso_modulos p ON m.id = p.modulo_id
-- WHERE m.activo = 1
-- GROUP BY m.id, m.numero_modulo, m.titulo
-- ORDER BY tasa_aprobacion ASC;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
```

## 4.2. Script Completo para SQL Server

```sql
-- ============================================================================
-- SMART REPORTS - INSTITUTO HUTCHISON PORTS
-- Script de Creación de Base de Datos - SQL Server
-- ============================================================================

-- Crear base de datos
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'InstitutoHutchison')
BEGIN
    CREATE DATABASE InstitutoHutchison;
END
GO

USE InstitutoHutchison;
GO

-- ============================================================================
-- TABLA: roles
-- ============================================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'roles')
BEGIN
    CREATE TABLE roles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(50) NOT NULL UNIQUE,
        descripcion NVARCHAR(MAX),
        nivel_acceso INT NOT NULL DEFAULT 0,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        INDEX idx_nombre (nombre),
        INDEX idx_nivel (nivel_acceso)
    );
END
GO

-- Insertar roles por defecto
IF NOT EXISTS (SELECT * FROM roles WHERE id = 1)
BEGIN
    SET IDENTITY_INSERT roles ON;
    
    INSERT INTO roles (id, nombre, descripcion, nivel_acceso) VALUES
    (1, 'Super Administrador', 'Acceso total al sistema', 100),
    (2, 'Administrador', 'Gestión de usuarios y reportes', 80),
    (3, 'Supervisor', 'Visualización y reportes', 60),
    (4, 'Usuario', 'Acceso básico al sistema', 40),
    (5, 'Invitado', 'Solo lectura', 20);
    
    SET IDENTITY_INSERT roles OFF;
END
GO

-- ============================================================================
-- TABLA: empleados
-- ============================================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'empleados')
BEGIN
    CREATE TABLE empleados (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id NVARCHAR(100) NOT NULL UNIQUE,
        nombre_completo NVARCHAR(200),
        email NVARCHAR(200),
        cargo NVARCHAR(150),
        departamento NVARCHAR(150),
        unidad_negocio NVARCHAR(150),
        ubicacion NVARCHAR(150),
        nivel NVARCHAR(100),
        activo BIT DEFAULT 1,
        rol_id INT DEFAULT 4,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_actualizacion DATETIME DEFAULT GETDATE(),
        
        INDEX idx_user_id (user_id),
        INDEX idx_email (email),
        INDEX idx_unidad (unidad_negocio),
        INDEX idx_activo (activo),
        INDEX idx_departamento (departamento),
        
        FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE SET NULL
    );
END
GO

-- ============================================================================
-- TABLA: modulos
-- ============================================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'modulos')
BEGIN
    CREATE TABLE modulos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        numero_modulo INT NOT NULL UNIQUE,
        titulo NVARCHAR(300) NOT NULL,
        descripcion NVARCHAR(MAX),
        orden INT DEFAULT 0,
        duracion_estimada INT DEFAULT 0,
        puntaje_minimo DECIMAL(5,2) DEFAULT 70.00,
        intentos_permitidos INT DEFAULT 3,
        activo BIT DEFAULT 1,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        
        INDEX idx_numero (numero_modulo),
        INDEX idx_titulo (titulo),
        INDEX idx_activo (activo),
        INDEX idx_orden (orden)
    );
END
GO

-- Insertar los 14 módulos
IF NOT EXISTS (SELECT * FROM modulos WHERE numero_modulo = 1)
BEGIN
    SET IDENTITY_INSERT modulos ON;
    
    INSERT INTO modulos (numero_modulo, titulo, descripcion, orden, puntaje_minimo, intentos_permitidos) VALUES
    (1, N'MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS', N'Introducción a la filosofía y valores corporativos', 1, 70.00, 3),
    (2, N'MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO', N'Compromiso ambiental y sostenibilidad', 2, 70.00, 3),
    (3, N'MÓDULO 3 . INTRODUCCIÓN A LAS OPERACIONES', N'Fundamentos de operaciones portuarias', 3, 70.00, 3),
    (4, N'MÓDULO 4 . RELACIONES LABORALES', N'Gestión de relaciones laborales', 4, 70.00, 3),
    (5, N'MÓDULO 5 . SEGURIDAD EN LAS OPERACIONES', N'Protocolos y normativas de seguridad', 5, 70.00, 3),
    (6, N'MÓDULO 6 . CIBERSEGURIDAD', N'Seguridad informática y protección de datos', 6, 70.00, 3),
    (7, N'MÓDULO 7 . ENTORNO LABORAL SALUDABLE', N'Salud ocupacional y bienestar laboral', 7, 70.00, 3),
    (8, N'MÓDULO 8 . PROCESOS DE RECURSOS HUMANOS', N'Gestión de recursos humanos y talento', 8, 70.00, 3),
    (9, N'MÓDULO 9 . PROGRAMAS DE BIENESTAR INTEGRAL', N'Programas de bienestar para empleados', 9, 70.00, 3),
    (10, N'MÓDULO 10 . DESARROLLO DE NUEVOS PRODUCTOS', N'Innovación y desarrollo de productos', 10, 70.00, 3),
    (11, N'MÓDULO 11 . PRODUCTOS DIGITALES DE HP', N'Plataformas y herramientas digitales', 11, 70.00, 3),
    (12, N'MÓDULO 12 . TECNOLOGÍA: IMPULSO PARA LA EFICIENCIA Y PRODUCTIVIDAD', N'Tecnología aplicada a operaciones', 12, 70.00, 3),
    (13, N'MÓDULO 13 . ACTIVACIÓN DE PROTOCOLOS Y BRIGADAS DE CONTINGENCIA', N'Protocolos de emergencia y contingencia', 13, 70.00, 3),
    (14, N'MÓDULO 14 . SISTEMA INTEGRADO DE GESTIÓN DE CALIDAD Y MEJORA CONTINUA', N'Gestión de calidad y mejora continua', 14, 70.00, 3);
    
    SET IDENTITY_INSERT modulos OFF;
END
GO

-- ============================================================================
-- TABLA: progreso_modulos
-- ============================================================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'progreso_modulos')
BEGIN
    CREATE TABLE progreso_modulos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        empleado_id INT NOT NULL,
        modulo_id INT NOT NULL,
        estado NVARCHAR(50) DEFAULT 'No iniciado',
        calificacion DECIMAL(5,2) DEFAULT NULL,
        fecha_inicio DATETIME DEFAULT NULL,
        fecha_finalizacion DATETIME DEFAULT NULL,
        fecha_registro DATETIME DEFAULT NULL,
        intentos_realizados INT DEFAULT 0,
        aprobado BIT DEFAULT 0,
        tipo_capacitacion NVARCHAR(50) DEFAULT 'Curriculum',
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_actualizacion DATETIME DEFAULT GETDATE(),
        
        INDEX idx_empleado (empleado_id),
        INDEX idx_modulo (modulo_id),
        INDEX idx_estado (estado),
        INDEX idx_aprobado (aprobado),
        INDEX idx_fecha_fin (fecha_finalizacion),
        UNIQUE INDEX idx_empleado_modulo (empleado_id, modulo_id),
        
        FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
        FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE,
        
        CONSTRAINT chk_estado CHECK (estado IN ('Terminado', 'En progreso', 'Registrado', 'No iniciado'))
    );
END
GO

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: Progreso general por empleado
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vista_progreso_empleados')
    DROP VIEW vista_progreso_empleados;
GO

CREATE VIEW vista_progreso_empleados AS
SELECT 
    e.id AS empleado_id,
    e.user_id,
    e.nombre_completo,
    e.email,
    e.unidad_negocio,
    e.departamento,
    COUNT(DISTINCT m.id) AS total_modulos,
    COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN m.id END) AS modulos_completados,
    COUNT(DISTINCT CASE WHEN p.aprobado = 1 THEN m.id END) AS modulos_aprobados,
    ROUND(
        (COUNT(DISTINCT CASE WHEN p.estado = 'Terminado' THEN m.id END) * 100.0) / 
        NULLIF(COUNT(DISTINCT m.id), 1), 
        2
    ) AS porcentaje_completado,
    AVG(CASE WHEN p.calificacion IS NOT NULL THEN p.calificacion END) AS calificacion_promedio
FROM empleados e
CROSS JOIN modulos m
LEFT JOIN progreso_modulos p ON e.id = p.empleado_id AND m.id = p.modulo_id
WHERE e.activo = 1 AND m.activo = 1
GROUP BY e.id, e.user_id, e.nombre_completo, e.email, e.unidad_negocio, e.departamento;
GO

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
```

---

# 5. CÓMO FUNCIONA EL MAPEO DE DATOS

## 5.1. Mapeo de Módulos (Inteligente)

El sistema tiene un **mapeo inteligente** que asocia los nombres de capacitaciones del Excel con los 14 módulos de la base de datos.

### Diccionario de Mapeo

```python
MODULOS_MAPPING = {
    1: "MÓDULO 1 . INTRODUCCIÓN A LA FILOSOFÍA HUTCHINSON PORTS",
    2: "MÓDULO 2 . SOSTENIBILIDAD, NUESTRO COMPROMISO CON EL FUTURO",
    # ... hasta 14
}

EVALUACIONES_A_MODULOS = {
    "introducción a la filosofía": 1,
    "filosofía hutchinson": 1,
    "sostenibilidad": 2,
    "compromiso con el futuro": 2,
    "relaciones laborales": 4,
    "recursos humanos": 8,
    "rrhh": 8,
    # ... etc
}
```

### Algoritmo de Matching

El sistema usa **múltiples técnicas** para encontrar coincidencias:

#### 1. **Matching Exacto** (100% coincidencia)
```python
titulo_normalizado = "módulo 8 procesos de recursos humanos"
# Busca coincidencia exacta en MODULOS_MAPPING
```

#### 2. **Matching por Palabras Clave** (parcial)
```python
titulo = "Evaluación: Procesos de RRHH"
# Busca "recursos humanos" o "rrhh" en EVALUACIONES_A_MODULOS
# Resultado: Módulo 8
```

#### 3. **Matching por Similitud** (fuzzy matching)
```python
from difflib import SequenceMatcher

titulo = "Modulo 8 - Recursos Humanos"
# Calcula similitud con cada módulo
# Si similitud > 80% → Match encontrado
```

#### 4. **Extracción de Número**
```python
titulo = "Módulo 8 . Cualquier cosa"
# Extrae el número "8" con regex
# Busca en MODULOS_MAPPING[8]
```

### Ejemplo Práctico de Mapeo

**Entrada del Excel**:
```
Training Title: "MÓDULO 8 - Procesos de RRHH - Evaluación Final"
```

**Proceso de Mapeo**:

1. **Normalización**:
   ```
   "módulo 8 procesos de rrhh evaluación final"
   ```

2. **Extracción de número**:
   ```
   Encuentra "8" → Módulo 8
   ```

3. **Verificación con palabras clave**:
   ```
   Busca "recursos humanos" o "rrhh" → Módulo 8 ✓
   ```

4. **Resultado**:
   ```
   modulo_id = 8 (PROCESOS DE RECURSOS HUMANOS)
   ```

## 5.2. Mapeo de Columnas (Excel → Base de Datos)

### Training Report → progreso_modulos

| Columna Excel | Columna BD | Transformación |
|---------------|------------|----------------|
| User ID | empleado_id | Busca en empleados.user_id |
| Training Title | modulo_id | Mapeo inteligente (ver arriba) |
| Completion Status | estado | Mapeo de estados |
| Start Date | fecha_inicio | Conversión de fecha |
| Completion Date | fecha_finalizacion | Conversión de fecha |
| Score | calificacion | DECIMAL(5,2) |
| Training Type | tipo_capacitacion | "Curriculum"/"Prueba" |

### Org Planning → empleados

| Columna Excel | Columna BD | Transformación |
|---------------|------------|----------------|
| User ID | user_id | Sin cambios (MASTER KEY) |
| Full Name | nombre_completo | Sin cambios |
| Email | email | Validación de formato |
| Position | cargo | Sin cambios |
| Department | departamento | Sin cambios |
| Division | unidad_negocio | Sin cambios |
| Location | ubicacion | Sin cambios |
| Level | nivel | Sin cambios |

## 5.3. Transformaciones de Datos

### Normalización de Textos

```python
def normalizar_texto(texto):
    # 1. Convertir a minúsculas
    texto = texto.lower()
    
    # 2. Eliminar acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    
    # 3. Limpiar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # 4. Eliminar caracteres especiales (opcional)
    texto = re.sub(r'[^\w\s]', '', texto)
    
    return texto
```

**Ejemplo**:
```
Entrada:  "MÓDULO 8   .   Procesos de RRHH"
Salida:   "modulo 8 procesos de rrhh"
```

### Conversión de Fechas

```python
def convertir_fecha(fecha_str):
    # Formatos soportados:
    # - "2025-01-18" (ISO)
    # - "18/01/2025" (DD/MM/YYYY)
    # - "01/18/2025" (MM/DD/YYYY)
    # - Timestamps de Excel (números)
    
    if isinstance(fecha_str, (int, float)):
        # Excel timestamp
        return datetime(1899, 12, 30) + timedelta(days=fecha_str)
    
    # Intentar múltiples formatos
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
        try:
            return datetime.strptime(fecha_str, fmt)
        except:
            continue
    
    return None
```

### Mapeo de Estados

```python
MAPEO_ESTADOS = {
    "completed": "Terminado",
    "terminado": "Terminado",
    "in progress": "En progreso",
    "en progreso": "En progreso",
    "registered": "Registrado",
    "registrado": "Registrado",
    "not started": "No iniciado",
    "no iniciado": "No iniciado"
}
```

---

# 6. GUÍA PASO A PASO PARA IMPORTAR DATOS

## 6.1. Preparación

### Paso 1: Verificar Archivos Excel

**Asegúrate de tener los 2 archivos**:

1. **Enterprise_Training_Report_YYYYMMDD_HHMMSS.xlsx**
   - Debe tener columnas: User ID, Training Title, Completion Status, Score, etc.

2. **CSOD_Data_Source_for_Org_Planning_YYYYMMDD.xlsx**
   - Debe tener columnas: User ID, Full Name, Email, Position, Department, etc.

### Paso 2: Verificar Base de Datos

1. **Abrir MySQL Workbench** (o SQL Server Management Studio)

2. **Ejecutar el script de creación** (sección 4.1 o 4.2 de esta guía)

3. **Verificar que las tablas existan**:
   ```sql
   USE InstitutoHutchison;
   SHOW TABLES;  -- MySQL
   -- o
   SELECT * FROM sys.tables;  -- SQL Server
   ```

4. **Verificar que los módulos estén insertados**:
   ```sql
   SELECT numero_modulo, titulo FROM modulos ORDER BY numero_modulo;
   -- Debe mostrar los 14 módulos
   ```

## 6.2. Importación con la Interfaz Gráfica

### Paso 1: Abrir Smart Reports

```powershell
python main.py
```

### Paso 2: Ir al Menú de Importación

1. Login con usuario `admin`
2. Click en **"Importación de Datos"** en la sidebar

### Paso 3: Seleccionar Archivos

**Panel izquierdo - Training Report**:
1. Click en "📂 Seleccionar Archivo"
2. Navega a tu carpeta de archivos
3. Selecciona `Enterprise_Training_Report_*.xlsx`
4. Verás:
   - ✓ Archivo seleccionado
   - Nombre del archivo
   - Número de filas detectadas

**Panel derecho - Org Planning**:
1. Click en "📂 Seleccionar Archivo"
2. Selecciona `CSOD_Data_Source_for_Org_Planning_*.xlsx`
3. Verás:
   - ✓ Archivo seleccionado
   - Nombre del archivo
   - Número de filas detectadas

### Paso 4: Ver Preview

1. Click en **"👁 Ver Preview"** (Training Report)
   - Se abrirá una ventana mostrando las primeras 5 filas
   - Verás las columnas detectadas
   - Verás muestra de datos

2. Click en **"👁 Ver Preview"** (Org Planning)
   - Igual que arriba

### Paso 5: Validar Datos

1. Click en **"✓ Validar Datos"**
2. El sistema verificará:
   - ✓ Estructura de archivos correcta
   - ✓ Columnas necesarias presentes
   - ✓ Tipos de datos válidos
   - ✓ No hay duplicados de User ID
   - ⚠ Advertencias (si las hay)

3. Revisa el **Log de Actividad** (parte inferior):
   ```
   ✓ Training Report validado correctamente
   ✓ Org Planning validado correctamente
   ℹ 1,525 usuarios únicos detectados
   ℹ 21,350 registros de progreso detectados
   ```

### Paso 6: Importar

**Opción A - Importar Todo** (Recomendado):
1. Click en **"📥 Importar Todo"**
2. Confirma en el diálogo:
   ```
   ¿Deseas importar ambos archivos?
   
   Esto puede tomar varios minutos...
   ¿Continuar?
   ```
3. Click en **"Sí"**

**Opción B - Importar Individual**:
1. Click en **"📥 Importar Training"** (solo progreso)
   - O click en **"📥 Importar Org"** (solo usuarios)

### Paso 7: Monitorear Progreso

Durante la importación verás en el Log:

```
🔄 Iniciando importación...
📂 Leyendo archivos Excel...
✓ Archivos leídos correctamente

🔄 Procesando usuarios (Org Planning)...
  ├─ Insertados: 1,200 empleados nuevos
  ├─ Actualizados: 325 empleados existentes
  └─ Errores: 0

🔄 Procesando progreso (Training Report)...
  ├─ Módulo 1: 1,525 registros
  ├─ Módulo 2: 1,520 registros
  ├─ Módulo 3: 1,485 registros
  ...
  ├─ Total procesado: 21,350 registros
  └─ Errores: 12 registros (ver detalles)

✓ Importación completada exitosamente
⏱ Tiempo total: 2 minutos 35 segundos
```

### Paso 8: Verificar Resultados

1. **En la aplicación**:
   - Ve a **"Consultas"**
   - Busca algunos usuarios por ID
   - Verifica que aparezcan con sus datos

2. **En la base de datos**:
   ```sql
   -- Contar empleados
   SELECT COUNT(*) AS total_empleados FROM empleados;
   
   -- Contar registros de progreso
   SELECT COUNT(*) AS total_progreso FROM progreso_modulos;
   
   -- Ver progreso general
   SELECT * FROM vista_progreso_empleados LIMIT 10;
   ```

## 6.3. Troubleshooting de Importación

### Error: "Columna no encontrada"

**Causa**: El Excel tiene nombres de columnas diferentes.

**Solución**:
1. Abre el archivo Excel
2. Verifica los nombres de las columnas en la primera fila
3. El sistema detecta automáticamente en español e inglés, pero si son muy diferentes:
   - Usa el **"Configurador de Columnas"** (botón en el panel)
   - Mapea manualmente cada columna

### Error: "Usuarios duplicados"

**Causa**: El mismo User ID aparece múltiples veces.

**Solución**:
1. El sistema usa **UPSERT** (UPDATE + INSERT)
2. Si un usuario ya existe, se actualiza su información
3. No es un error crítico

### Error: "Módulo no encontrado para: XXXX"

**Causa**: El título de capacitación no coincide con ningún módulo conocido.

**Solución**:
1. Revisa el título exacto en el Log
2. Agrega un mapeo manual en el código:
   ```python
   EVALUACIONES_A_MODULOS = {
       "tu nuevo título": 8,  # Número del módulo
       # ...
   }
   ```
3. O ignora ese registro (se registrará en el log de errores)

### La Importación es Muy Lenta

**Causas posibles**:
- Archivos muy grandes (>50,000 registros)
- Conexión lenta a la BD
- Validaciones muy estrictas

**Soluciones**:
1. **Aumentar batch_size**:
   ```python
   # En etl_instituto_completo.py
   config = ETLConfig(batch_size=5000)  # Default: 1000
   ```

2. **Desactivar validaciones temporalmente**:
   ```python
   config = ETLConfig(enable_validation=False)
   ```

3. **Usar importación por partes**:
   - Divide el Excel en archivos más pequeños
   - Importa uno por uno

---

# 7. SISTEMA DE CRUCE DE DATOS

## 7.1. ¿Qué es el Cruce de Datos?

El **cruce de datos** es el proceso de **combinar información** de los 2 archivos Excel usando el `User ID` como **llave maestra** (MASTER KEY).

### Objetivo

**Enriquecer** los datos de capacitación con información de usuario:

- **Sin cruce**: Solo sabemos que el usuario "12345" completó el Módulo 8 con 85%
- **Con cruce**: Sabemos que "Juan Pérez" (ICAVE, Gerente de Operaciones) completó el Módulo 8 con 85%

## 7.2. Proceso de Cruce

### Paso 1: Identificación de User ID

```
Training Report:
┌─────────┬───────────────────┬──────────┐
│ User ID │  Training Title   │  Score   │
├─────────┼───────────────────┼──────────┤
│  12345  │  Módulo 8 - RRHH  │   85%    │
│  67890  │  Módulo 8 - RRHH  │   92%    │
└─────────┴───────────────────┴──────────┘

Org Planning:
┌─────────┬──────────────┬─────────────────┬──────────┐
│ User ID │  Full Name   │   Position      │ Division │
├─────────┼──────────────┼─────────────────┼──────────┤
│  12345  │ Juan Pérez   │ Gerente Ops     │  ICAVE   │
│  67890  │ María López  │ Analista        │  TNG     │
└─────────┴──────────────┴─────────────────┴──────────┘
```

### Paso 2: Merge en Pandas

```python
# Leer archivos
df_training = pd.read_excel("Training_Report.xlsx")
df_org = pd.read_excel("Org_Planning.xlsx")

# Cruce usando User ID
df_cruzado = pd.merge(
    df_training,
    df_org,
    left_on='User ID',
    right_on='User ID',
    how='left'  # Mantener todos los registros de training
)
```

**Resultado**:
```
┌─────────┬─────────────┬───────┬──────────────┬─────────┬──────────┐
│ User ID │   Title     │ Score │  Full Name   │Position │ Division │
├─────────┼─────────────┼───────┼──────────────┼─────────┼──────────┤
│  12345  │ Módulo 8    │  85%  │ Juan Pérez   │Gerente  │  ICAVE   │
│  67890  │ Módulo 8    │  92%  │ María López  │Analista │  TNG     │
└─────────┴─────────────┴───────┴──────────────┴─────────┴──────────┘
```

### Paso 3: Inserción en Base de Datos

```python
# Para cada fila del DataFrame cruzado:
for index, row in df_cruzado.iterrows():
    # 1. Insertar/Actualizar empleado
    empleado_id = insertar_empleado(
        user_id=row['User ID'],
        nombre=row['Full Name'],
        cargo=row['Position'],
        unidad=row['Division']
    )
    
    # 2. Obtener módulo_id
    modulo_id = mapear_modulo(row['Training Title'])
    
    # 3. Insertar progreso
    insertar_progreso(
        empleado_id=empleado_id,
        modulo_id=modulo_id,
        estado=row['Completion Status'],
        calificacion=row['Score']
    )
```

## 7.3. Manejo de Inconsistencias

### Caso 1: Usuario en Training pero NO en Org Planning

**Situación**:
```
Training Report: User ID = 99999 (existe)
Org Planning: User ID = 99999 (NO existe)
```

**Solución del ETL**:
1. Crea un usuario "fantasma" con información mínima:
   ```python
   {
       "user_id": "99999",
       "nombre_completo": "Usuario 99999 (Sin datos)",
       "email": None,
       "cargo": "No especificado",
       "unidad_negocio": "Sin asignar"
   }
   ```
2. Registra una advertencia en el log
3. Continúa con la importación

### Caso 2: Usuario en Org Planning pero NO en Training

**Situación**:
```
Org Planning: User ID = 88888 (existe)
Training Report: User ID = 88888 (NO existe)
```

**Solución del ETL**:
1. Inserta el usuario normalmente
2. NO crea registros de progreso (el usuario aún no ha tomado capacitaciones)
3. Queda listo para futuras importaciones

### Caso 3: User ID Duplicado

**Situación**:
```
Training Report:
  User ID = 12345, Módulo 8, Score = 85%
  User ID = 12345, Módulo 8, Score = 92%  ← DUPLICADO
```

**Solución del ETL**:
1. **Estrategia: Mantener el registro más reciente**
   ```python
   # Ordenar por fecha_finalizacion DESC
   # Tomar solo el primer registro por (user_id, modulo_id)
   df_sin_duplicados = df.sort_values('fecha_finalizacion', ascending=False)
   df_sin_duplicados = df_sin_duplicados.drop_duplicates(['User ID', 'Training Title'], keep='first')
   ```

2. **Alternativa: Promediar calificaciones**
   ```python
   df_promediado = df.groupby(['User ID', 'Training Title']).agg({
       'Score': 'mean',  # Promedio de calificaciones
       'fecha_finalizacion': 'max'  # Fecha más reciente
   }).reset_index()
   ```

---

# 8. TROUBLESHOOTING

## 8.1. Errores Comunes de Base de Datos

### Error: "Access denied for user 'root'"

**Causa**: Contraseña incorrecta o usuario sin permisos.

**Solución**:
```sql
-- MySQL: Resetear contraseña de root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password';
FLUSH PRIVILEGES;
```

### Error: "Table 'empleados' doesn't exist"

**Causa**: No se ejecutó el script de creación.

**Solución**:
1. Abre MySQL Workbench
2. Copia el script completo de la sección 4.1
3. Ejecuta todo el script
4. Verifica: `SHOW TABLES;`

### Error: "Duplicate entry for key 'user_id'"

**Causa**: Intentas insertar un usuario que ya existe.

**Solución**:
```sql
-- MySQL: Usar INSERT ... ON DUPLICATE KEY UPDATE
INSERT INTO empleados (user_id, nombre_completo, email)
VALUES ('12345', 'Juan Pérez', 'juan@example.com')
ON DUPLICATE KEY UPDATE
    nombre_completo = VALUES(nombre_completo),
    email = VALUES(email);
```

## 8.2. Errores de Importación ETL

### Error: "No module named 'pandas'"

**Solución**:
```bash
pip install pandas openpyxl
```

### Error: "xlrd not installed"

**Solución**:
```bash
pip install openpyxl  # Para .xlsx (recomendado)
# O
pip install xlrd  # Para .xls (legacy)
```

### Error: "ValueError: Puntuación fuera de rango"

**Causa**: Calificación < 0 o > 100 en el Excel.

**Solución**:
1. Abre el Excel
2. Busca la calificación inválida
3. Corrígela manualmente
4. O modifica el validador:
   ```python
   @validator('puntuacion')
   def validar_puntuacion(cls, v):
       if v is not None:
           if v < 0: return 0
           if v > 100: return 100
       return v
   ```

## 8.3. Problemas de Rendimiento

### La Consulta es Muy Lenta

**Síntoma**: `SELECT * FROM vista_progreso_empleados` tarda >30 segundos.

**Causa**: Falta índice o la vista hace muchos JOINs.

**Solución**:
```sql
-- Crear índices faltantes
CREATE INDEX idx_progreso_empleado_modulo ON progreso_modulos(empleado_id, modulo_id);
CREATE INDEX idx_empleado_activo ON empleados(activo);

-- O usar consulta más optimizada
SELECT e.*, p.* 
FROM empleados e
LEFT JOIN progreso_modulos p ON e.id = p.empleado_id
WHERE e.activo = 1
LIMIT 100;  -- Limitar resultados
```

### La Importación Falla por Timeout

**Síntoma**: Error "Timeout expired" durante importación.

**Solución**:
```python
# Aumentar timeout de conexión
config = ETLConfig()
connection = pyodbc.connect(
    connection_string,
    timeout=300  # 5 minutos
)
```

---

# 9. APÉNDICE: CONSULTAS SQL ÚTILES

## Consultas de Análisis

### 1. Top 10 Empleados con Mejor Progreso

```sql
SELECT 
    user_id,
    nombre_completo,
    unidad_negocio,
    porcentaje_completado,
    calificacion_promedio
FROM vista_progreso_empleados
ORDER BY porcentaje_completado DESC, calificacion_promedio DESC
LIMIT 10;
```

### 2. Progreso por Unidad de Negocio

```sql
SELECT * FROM vista_progreso_unidades
ORDER BY porcentaje_completado DESC;
```

### 3. Módulos con Menor Tasa de Aprobación

```sql
SELECT 
    m.numero_modulo,
    m.titulo,
    COUNT(p.id) AS total_intentos,
    COUNT(CASE WHEN p.aprobado = 1 THEN 1 END) AS aprobados,
    ROUND((COUNT(CASE WHEN p.aprobado = 1 THEN 1 END) * 100.0) / COUNT(p.id), 2) AS tasa_aprobacion
FROM modulos m
LEFT JOIN progreso_modulos p ON m.id = p.modulo_id
WHERE m.activo = 1
GROUP BY m.id, m.numero_modulo, m.titulo
ORDER BY tasa_aprobacion ASC;
```

### 4. Empleados Sin Capacitaciones

```sql
SELECT 
    e.user_id,
    e.nombre_completo,
    e.email,
    e.unidad_negocio
FROM empleados e
LEFT JOIN progreso_modulos p ON e.id = p.empleado_id
WHERE e.activo = 1 
AND p.id IS NULL;
```

### 5. Promedio de Calificaciones por Módulo

```sql
SELECT 
    m.numero_modulo,
    m.titulo,
    ROUND(AVG(p.calificacion), 2) AS promedio_calificacion,
    COUNT(p.id) AS total_completados
FROM modulos m
LEFT JOIN progreso_modulos p ON m.id = p.modulo_id AND p.estado = 'Terminado'
GROUP BY m.id, m.numero_modulo, m.titulo
ORDER BY m.numero_modulo;
```

---

# 10. CONCLUSIÓN

Esta guía cubre TODO lo necesario para:

✅ Entender el sistema ETL  
✅ Crear la base de datos en MySQL/SQL Server  
✅ Importar datos de archivos Excel de CSOD  
✅ Realizar cruces de datos inteligentes  
✅ Mapear módulos automáticamente  
✅ Solucionar problemas comunes  

**Para mañana**:
1. Lee esta guía completa
2. Ejecuta el script SQL (sección 4)
3. Prueba una importación de prueba
4. Verifica los resultados con las consultas de la sección 9

**¡BUENA SUERTE EN TU PRESENTACIÓN!** 🚀

---

**Autor**: Claude AI  
**Fecha**: 2025-01-19  
**Versión**: 1.0  
**Proyecto**: Smart Reports - Instituto Hutchison Ports
