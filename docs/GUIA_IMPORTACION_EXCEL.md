# 📥 Guía de Importación de Excel CSOD

Sistema de importación de archivos Excel CSOD a la base de datos Instituto Hutchison Ports.

---

## 🚀 Inicio Rápido

### 1. **Instalación de Dependencias**

```bash
pip install pandas mysql-connector-python openpyxl
```

### 2. **Configurar Base de Datos**

Editar `src/main/res/config/database.py`:

```python
# Para MySQL (casa/desarrollo)
DB_TYPE = 'mysql'

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tngcore',
    'user': 'root',
    'password': 'TU_PASSWORD',  # ⚠️ CAMBIAR
    'charset': 'utf8mb4',
    'autocommit': False
}
```

### 3. **Ejecutar Importación**

```bash
# Training Report (Progreso y Calificaciones)
python scripts/importar_excel_csod.py training data/training_report.xlsx

# Org Planning (Usuarios)
python scripts/importar_excel_csod.py usuarios data/org_planning.xlsx
```

---

## 📂 Tipos de Archivos Soportados

### 1️⃣ Training Report (Enterprise Training Report)

**Contiene:**
- Progreso de módulos por usuario
- Calificaciones de evaluaciones
- Estados de finalización
- Fechas de inicio y fin

**Columnas esperadas:**
- Título de la capacitación / Training Title
- Identificación de usuario / User ID
- Estado del expediente / Record Status
- Fecha de inicio / Training Start Date
- Fecha de finalización / Completion Date
- Puntuación / Score
- Tipo de capacitación / Training Type

**Uso:**
```bash
python scripts/importar_excel_csod.py training archivo_training.xlsx
```

---

### 2️⃣ Org Planning (CSOD Org Planning)

**Contiene:**
- Datos de usuarios
- Información organizacional
- Departamentos y unidades
- Cargos y ubicaciones

**Columnas esperadas:**
- Usuario - Identificación / User - User ID
- Usuario - Nombre completo / User - Full Name
- Usuario - Correo electrónico / User - Email Address
- Usuario - Cargo / User - Job Title
- Usuario - Departamento / User - Department
- Usuario - División / User - Division
- Usuario - Ubicación / User - Location

**Uso:**
```bash
python scripts/importar_excel_csod.py usuarios archivo_usuarios.xlsx
```

---

## ⚙️ Características del Importador

### ✅ Detección Automática de Columnas

El sistema detecta automáticamente si el Excel está en:
- **Español**: "Título de la capacitación", "Identificación de usuario", etc.
- **Inglés**: "Training Title", "User ID", etc.

### ✅ Detección de Headers

Si el Excel tiene filas de título/logo antes de los headers reales, el sistema:
1. Detecta automáticamente dónde están los headers
2. Lee el Excel saltando las filas superiores
3. Muestra un mensaje informativo

### ✅ Optimización de Rendimiento

- **Precarga de datos** en memoria (evita N+1 queries)
- **Batch operations** (executemany en lugar de execute en loop)
- **Caché de módulos** y usuarios

**Mejora de rendimiento**: ~15x-20x más rápido que versión anterior

### ✅ Manejo de Errores

- Registra todos los errores sin detener la importación
- Muestra resumen de errores al final
- Usa transacciones (COMMIT/ROLLBACK)

---

## 🗂️ Estructura de la Base de Datos

El sistema trabaja con la estructura `instituto_*`:

```
instituto_UnidadDeNegocio (ICAVE, EIT, LCT, TIMSA, HPMX, TNG)
    └── instituto_Departamento
        └── instituto_Usuario
            └── instituto_ProgresoModulo (IdInscripcion)
                ├── instituto_ResultadoEvaluacion
                └── instituto_Certificado

instituto_Modulo
    ├── instituto_Evaluacion
    └── instituto_RecursoModulo
```

---

## 📊 Flujo de Importación

### Training Report

1. **Lee Excel** y detecta columnas
2. **Filtra módulos** (registros que contienen "MÓDULO")
3. **Precarga** módulos y progresos existentes
4. **Procesa en batch**:
   - INSERT para nuevos progresos
   - UPDATE para progresos existentes
5. **Filtra evaluaciones** (registros con tipo "Prueba"/"Test")
6. **Inserta calificaciones** en `instituto_ResultadoEvaluacion`
7. **Actualiza estado** a "Terminado" si aprobó
8. **Commit** de transacción

### Org Planning

1. **Lee Excel** y detecta columnas
2. **Precarga** unidades, departamentos y usuarios
3. **Para cada usuario**:
   - Busca/crea Unidad de Negocio
   - Busca/crea Departamento
   - INSERT o UPDATE en `instituto_Usuario`
4. **Commit** de transacción

---

## 🔍 Ejemplo de Salida

```
======================================================================
📊 IMPORTANDO TRAINING REPORT
======================================================================

📖 Leyendo archivo Excel...
  ✓ Registros leídos: 2500

🔍 Detectando columnas...
✅ Columnas detectadas: 10/12
⚠️  Columnas no encontradas: level, location

📋 Procesando progreso de módulos...
  ✅ Módulos precargados: 14
  ✅ Progresos existentes precargados: 1250
  📊 Registros de módulos: 2200
  ✅ Actualizados: 1250
  ✅ Insertados: 950

📝 Procesando calificaciones...
  📊 Calificaciones a procesar: 300
  ✅ Calificaciones registradas: 300

======================================================================
✅ IMPORTACIÓN COMPLETADA
======================================================================
📊 ESTADÍSTICAS FINALES
======================================================================
  • Usuarios nuevos:             0
  • Usuarios actualizados:       0
  • Progresos actualizados:      2200
  • Calificaciones registradas:  300
  • Módulos creados:             0
  • Errores:                     5
======================================================================
```

---

## 🛠️ Uso Programático

### Importar Training Report desde Python

```python
from src.main.python.data.repositories.persistence.mysql.repositories.database_manager_instituto import (
    DatabaseConfig,
    InstitutoSmartReportsDB
)
from src.main.python.domain.services.excel_importer_instituto import ExcelImporterInstituto

# Configurar BD
config = DatabaseConfig(
    host='localhost',
    database='tngcore',
    user='root',
    password='tu_password',
    port=3306
)

# Conectar
db_system = InstitutoSmartReportsDB(config)

# Crear importador
importador = ExcelImporterInstituto(db_system)

# Importar Training Report
stats = importador.importar_training_report('data/training_report.xlsx')

# Mostrar estadísticas
print(f"Progresos actualizados: {stats['progresos_actualizados']}")
print(f"Calificaciones registradas: {stats['calificaciones_registradas']}")

# Cerrar
db_system.close()
```

### Importar Org Planning desde Python

```python
# (Misma configuración que arriba)

# Importar Org Planning
stats = importador.importar_org_planning('data/org_planning.xlsx')

# Mostrar estadísticas
print(f"Usuarios nuevos: {stats['usuarios_nuevos']}")
print(f"Usuarios actualizados: {stats['usuarios_actualizados']}")
```

---

## 🔄 Soporte SQL Server

El sistema incluye un adaptador de queries para SQL Server.

### Configurar para SQL Server

Editar `src/main/res/config/database.py`:

```python
# Para SQL Server (trabajo)
DB_TYPE = 'sqlserver'

SQLSERVER_CONFIG = {
    'server': '10.133.18.111',
    'port': 1433,
    'database': 'TNGCORE',
    'username': 'tngdatauser',
    'password': 'Password1',
    'driver': 'ODBC Driver 17 for SQL Server'
}
```

### Usar Query Adapter

```python
from src.main.python.data.repositories.persistence.sqlserver.query_adapter import (
    QueryAdapter,
    CommonQueriesSQLServer
)

# Convertir query MySQL a SQL Server
mysql_query = "SELECT * FROM instituto_Usuario LIMIT 10"
sqlserver_query = QueryAdapter.adapt_query(mysql_query)
# Resultado: "SELECT TOP 10 * FROM instituto_Usuario"

# Usar queries ya adaptadas
query = CommonQueriesSQLServer.SELECT_MODULOS
```

**Conversiones automáticas:**
- `LIMIT` → `TOP`
- `%s` → `?`
- `NOW()` → `GETDATE()`
- `CURRENT_TIMESTAMP` → `GETDATE()`
- `INSERT IGNORE` → `IF NOT EXISTS` (simplificado)
- `` `tabla` `` → `[tabla]`

---

## 📈 Validación Post-Importación

Después de cada importación, ejecutar estas queries para validar:

```sql
-- 1. Usuarios sin unidad de negocio
SELECT COUNT(*) AS UsuariosSinUnidad
FROM instituto_Usuario
WHERE IdUnidadDeNegocio IS NULL;

-- 2. Progreso sin fechas consistentes
SELECT COUNT(*) AS ProgresoInconsistente
FROM instituto_ProgresoModulo
WHERE FechaFinalizacion IS NOT NULL
  AND FechaFinalizacion < FechaInicio;

-- 3. Calificaciones sin inscripción válida
SELECT COUNT(*) AS CalificacionesHuérfanas
FROM instituto_ResultadoEvaluacion re
LEFT JOIN instituto_ProgresoModulo pm ON re.IdInscripcion = pm.IdInscripcion
WHERE pm.IdInscripcion IS NULL;

-- 4. Resumen por unidad de negocio
SELECT
    un.NombreUnidad,
    COUNT(DISTINCT u.IdUsuario) AS TotalUsuarios,
    COUNT(DISTINCT pm.IdInscripcion) AS TotalInscripciones,
    SUM(CASE WHEN pm.EstatusModulo = 'Terminado' THEN 1 ELSE 0 END) AS Completados
FROM instituto_UnidadDeNegocio un
LEFT JOIN instituto_Usuario u ON un.IdUnidadDeNegocio = u.IdUnidadDeNegocio
LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
WHERE un.Activo = 1
GROUP BY un.IdUnidadDeNegocio;
```

---

## ⚠️ Troubleshooting

### Problema: "Columnas no encontradas"

**Causa:** Los nombres de columnas del Excel no coinciden con las variaciones conocidas.

**Solución:**
1. Verifica los nombres exactos de las columnas en el Excel
2. Compara con las variaciones en `excel_importer_instituto.py` → `COLUMN_VARIATIONS`
3. Si son diferentes, agrega las nuevas variaciones al código

### Problema: "Headers no detectados"

**Causa:** El Excel tiene más de 5 filas antes de los headers reales.

**Solución:**
1. Elimina las filas de título/logo superiores manualmente
2. O ajusta el código en `_leer_excel_con_deteccion_headers()` para buscar en más filas

### Problema: "Módulo no encontrado"

**Causa:** El título del módulo en el Excel no coincide con los nombres en `MODULOS_MAPPING`.

**Solución:**
1. Verifica que el título contenga "MÓDULO X" donde X es 1-14
2. El sistema busca la palabra "MÓDULO" (case-insensitive)
3. Si hay módulos nuevos, agrégalos a `MODULOS_MAPPING`

### Problema: "Usuario no existe"

**Causa:** Se intentó importar Training Report sin haber importado Org Planning primero.

**Solución:**
1. **Importar primero** Org Planning (usuarios)
2. **Luego** importar Training Report (progreso y calificaciones)

---

## 📚 Documentación Relacionada

- [MAPEO_COLUMNAS_EXCEL_BD.md](./MAPEO_COLUMNAS_EXCEL_BD.md) - Mapeo detallado de columnas
- [ER_MODELS.md](./ER_MODELS.md) - Modelos entidad-relación
- [database_manager_instituto.py](../src/main/python/data/repositories/persistence/mysql/repositories/database_manager_instituto.py) - Manager de BD
- [excel_importer_instituto.py](../src/main/python/domain/services/excel_importer_instituto.py) - Importador completo

---

**Última actualización:** 13 de Noviembre, 2025
**Versión:** Smart Reports v2.0
**Autor:** Sistema Smart Reports - Instituto Hutchison Ports
