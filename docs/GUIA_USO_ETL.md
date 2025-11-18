# Guía de Uso - Sistema ETL Instituto Hutchison Ports

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso Básico](#uso-básico)
5. [Casos de Uso Avanzados](#casos-de-uso-avanzados)
6. [Troubleshooting](#troubleshooting)
7. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📖 Descripción General

El sistema ETL (Extract, Transform, Load) de Instituto Hutchison Ports procesa archivos Excel de CSOD (Cornerstone OnDemand) y los carga en SQL Server.

### Características Principales

✅ **Soporte para SQL Server** (pyodbc)
✅ **Validación de datos** con Pydantic
✅ **Auto-detección de módulos nuevos** (escalable a 14+ módulos)
✅ **Batch operations** para alto rendimiento
✅ **Detección automática de columnas** (Español/Inglés)
✅ **Matching case-insensitive** para módulos y evaluaciones
✅ **Manejo robusto de errores** y logging completo

### Archivos Soportados

1. **Enterprise_Training_Report{timestamp}.xlsx** - Progreso de capacitación y calificaciones
2. **CSOD_Data_Source_for_Org_Planning_{timestamp}.xlsx** - Datos organizacionales de usuarios

---

## 🚀 Instalación

### Paso 1: Instalar Python (3.8+)

Verifica tu versión de Python:

```bash
python --version
# Debe ser Python 3.8 o superior
```

### Paso 2: Instalar dependencias de Python

```bash
cd /ruta/a/smart-reports1
pip install -r requirements_etl.txt
```

### Paso 3: Instalar ODBC Driver para SQL Server

#### Windows

1. Descargar e instalar: [ODBC Driver 17 para SQL Server](https://go.microsoft.com/fwlink/?linkid=2249004)
2. Reiniciar el sistema

#### Linux (Ubuntu/Debian)

```bash
# Instalar ODBC
sudo apt-get install unixodbc unixodbc-dev

# Agregar repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Instalar driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

#### macOS

```bash
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17
```

### Paso 4: Verificar instalación

```bash
python -c "import pyodbc; print('✅ pyodbc instalado correctamente')"
python -c "import pandas; print('✅ pandas instalado correctamente')"
python -c "import pydantic; print('✅ pydantic instalado correctamente')"
```

---

## ⚙️ Configuración

### Configuración de la Base de Datos

Edita el archivo de configuración o crea un archivo `config_etl.py`:

```python
from src.main.python.domain.services.etl_instituto_completo import ETLConfig

# Configuración para Autenticación Windows
config = ETLConfig(
    server="localhost",              # O tu servidor SQL Server
    database="InstitutoHutchison",
    username=None,                   # None = Windows Authentication
    password=None,
    driver="ODBC Driver 17 for SQL Server",
    batch_size=1000,
    enable_validation=True,
    auto_create_modules=True
)

# Configuración para Autenticación SQL Server
config_sql_auth = ETLConfig(
    server="mi-servidor.database.windows.net",
    database="InstitutoHutchison",
    username="usuario_sql",
    password="password_seguro",
    driver="ODBC Driver 17 for SQL Server",
    batch_size=1000,
    enable_validation=True,
    auto_create_modules=True
)
```

### Parámetros de Configuración

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `server` | str | Nombre o IP del servidor SQL Server | `"localhost"` |
| `database` | str | Nombre de la base de datos | `"InstitutoHutchison"` |
| `username` | str o None | Usuario SQL Server (None = Windows Auth) | `None` |
| `password` | str o None | Contraseña SQL Server | `None` |
| `driver` | str | Driver ODBC a usar | `"ODBC Driver 17 for SQL Server"` |
| `batch_size` | int | Tamaño de batch para operaciones | `1000` |
| `enable_validation` | bool | Activar validación con Pydantic | `True` |
| `auto_create_modules` | bool | Crear módulos automáticamente si no existen | `True` |
| `default_puntaje_minimo` | float | Puntaje mínimo por defecto para evaluaciones | `70.0` |
| `default_intentos_permitidos` | int | Intentos permitidos por defecto | `3` |
| `default_rol_id` | int | ID del rol por defecto para usuarios nuevos | `4` |

---

## 💻 Uso Básico

### Ejemplo 1: Importar Datos de Usuarios (Org Planning)

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig

# Configurar
config = ETLConfig(
    server="localhost",
    database="InstitutoHutchison"
)

# Crear instancia del ETL (context manager para manejo automático de conexiones)
with ETLInstitutoCompleto(config) as etl:
    # Importar archivo Org Planning
    stats = etl.importar_org_planning(
        "data/CSOD_Data_Source_for_Org_Planning_2025-01-18.xlsx"
    )

    # Revisar estadísticas
    print(f"Usuarios nuevos: {stats['usuarios_nuevos']}")
    print(f"Usuarios actualizados: {stats['usuarios_actualizados']}")
    print(f"Errores: {len(stats['errores'])}")
```

### Ejemplo 2: Importar Progreso de Capacitación (Training Report)

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig

config = ETLConfig(
    server="localhost",
    database="InstitutoHutchison"
)

with ETLInstitutoCompleto(config) as etl:
    # Importar archivo Training Report
    stats = etl.importar_training_report(
        "data/Enterprise_Training_Report_2025-01-18.xlsx"
    )

    # Revisar estadísticas
    print(f"Progresos insertados: {stats['progresos_insertados']}")
    print(f"Progresos actualizados: {stats['progresos_actualizados']}")
    print(f"Calificaciones registradas: {stats['calificaciones_registradas']}")
    print(f"Módulos creados automáticamente: {stats['modulos_creados']}")
```

### Ejemplo 3: Importar Ambos Archivos Secuencialmente

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig

config = ETLConfig(
    server="localhost",
    database="InstitutoHutchison"
)

with ETLInstitutoCompleto(config) as etl:
    # Primero importar usuarios (Org Planning)
    print("📥 Importando usuarios...")
    etl.importar_org_planning("data/CSOD_Org_Planning.xlsx")

    # Luego importar progreso (Training Report)
    print("\n📥 Importando progreso de capacitación...")
    etl.importar_training_report("data/Enterprise_Training_Report.xlsx")
```

---

## 🔧 Casos de Uso Avanzados

### Caso 1: Procesar Múltiples Archivos con Manejo de Errores

```python
import glob
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = ETLConfig(server="localhost", database="InstitutoHutchison")

# Buscar todos los archivos Training Report
archivos_training = glob.glob("data/Enterprise_Training_Report_*.xlsx")

with ETLInstitutoCompleto(config) as etl:
    for archivo in archivos_training:
        try:
            logger.info(f"📥 Procesando: {archivo}")
            stats = etl.importar_training_report(archivo)

            if len(stats['errores']) > 0:
                logger.warning(f"⚠️  Archivo procesado con {len(stats['errores'])} errores")
            else:
                logger.info(f"✅ Archivo procesado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error procesando {archivo}: {e}")
            continue  # Continuar con el siguiente archivo
```

### Caso 2: Validación Pre-Importación

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig
import pandas as pd

config = ETLConfig(server="localhost", database="InstitutoHutchison")

# Leer Excel sin importar
df = pd.read_excel("data/Training_Report.xlsx", engine='openpyxl')

# Validaciones previas
print(f"Total de registros: {len(df)}")
print(f"Columnas encontradas: {list(df.columns)}")

# Verificar si tiene columnas críticas
required_cols = ['Identificación de usuario', 'Título de la capacitación']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    print(f"❌ Faltan columnas: {missing_cols}")
else:
    print("✅ Todas las columnas requeridas están presentes")

    # Proceder con importación
    with ETLInstitutoCompleto(config) as etl:
        stats = etl.importar_training_report("data/Training_Report.xlsx")
```

### Caso 3: Guardar Log de Errores en Archivo

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig
import json
from datetime import datetime

config = ETLConfig(server="localhost", database="InstitutoHutchison")

with ETLInstitutoCompleto(config) as etl:
    stats = etl.importar_training_report("data/Training_Report.xlsx")

    # Guardar errores en JSON
    if stats['errores']:
        error_log = {
            'fecha': datetime.now().isoformat(),
            'archivo': 'Training_Report.xlsx',
            'total_errores': len(stats['errores']),
            'errores': stats['errores']
        }

        with open(f"logs/errores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(error_log, f, indent=2)

        print(f"📝 Log de errores guardado")
```

### Caso 4: Desactivar Auto-Creación de Módulos

```python
from src.main.python.domain.services.etl_instituto_completo import ETLInstitutoCompleto, ETLConfig

# Configuración conservadora (no crear nada nuevo)
config = ETLConfig(
    server="localhost",
    database="InstitutoHutchison",
    auto_create_modules=False,  # ⚠️ Solo actualizar módulos existentes
    enable_validation=True
)

with ETLInstitutoCompleto(config) as etl:
    # Si encuentra un módulo que no existe, lo saltará
    stats = etl.importar_training_report("data/Training_Report.xlsx")
```

---

## 🐛 Troubleshooting

### Error: "pyodbc.OperationalError: Unable to connect to SQL Server"

**Causa:** No se puede conectar al servidor SQL Server

**Solución:**
1. Verificar que SQL Server esté corriendo
2. Verificar nombre del servidor en la configuración
3. Verificar firewall y puertos (puerto 1433 por defecto)
4. Verificar autenticación (Windows vs SQL Server)

```bash
# Probar conexión desde consola
sqlcmd -S localhost -U sa -P password
```

### Error: "pyodbc.InterfaceError: ('IM002', '[IM002] ...')"

**Causa:** Driver ODBC no instalado o no encontrado

**Solución:**
1. Verificar drivers disponibles:
   ```python
   import pyodbc
   print(pyodbc.drivers())
   ```
2. Instalar ODBC Driver 17 (ver sección de instalación)
3. Actualizar parámetro `driver` en la configuración

### Error: "ModuleNotFoundError: No module named 'pydantic'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
pip install -r requirements_etl.txt
```

### Error: "pandas.errors.ParserError: Error tokenizing data"

**Causa:** Archivo Excel corrupto o formato incorrecto

**Solución:**
1. Abrir archivo en Excel y guardarlo nuevamente
2. Verificar que sea formato `.xlsx` (no `.xls`)
3. Verificar que no tenga contraseña

### Advertencia: "Columnas opcionales no encontradas"

**Causa:** Algunas columnas no se encontraron en el Excel

**Solución:**
- Es normal si el archivo no tiene todas las columnas
- Verificar el log para ver qué columnas faltan
- Si son columnas críticas (`user_id`, `training_title`), revisar el archivo

### Error: "No se pudo identificar módulo"

**Causa:** Título del módulo no contiene "MÓDULO X" ni coincide con fuzzy matching

**Solución:**
1. Revisar títulos en el Excel
2. Agregar mapeo en `EVALUACIONES_A_MODULOS` si es evaluación
3. Crear módulo manualmente en la BD si es nuevo

---

## ❓ Preguntas Frecuentes

### ¿Qué pasa si un módulo no existe en la BD?

Si `auto_create_modules=True` (default), el ETL creará automáticamente el módulo y su evaluación por defecto. Si es `False`, saltará ese registro.

### ¿Cómo se manejan los duplicados?

- **Usuarios:** Se actualizan si ya existen (basado en `UserId`)
- **Progreso:** Se actualiza si ya existe (basado en `UserId` + `IdModulo`)
- **Calificaciones:** Se insertan como nuevos intentos

### ¿Qué sucede si falla en medio de la importación?

El ETL usa transacciones. Si hay un error fatal, se hace ROLLBACK automático y no se guarda nada. Los errores no fatales se registran pero permiten continuar.

### ¿Puedo procesar el mismo archivo varias veces?

Sí, es seguro. El ETL es **idempotente**: procesar el mismo archivo múltiples veces actualiza los datos en lugar de duplicarlos.

### ¿Cómo personalizo el mapeo de módulos?

Edita el diccionario `MODULOS_MAPPING` en `etl_instituto_completo.py`:

```python
MODULOS_MAPPING = {
    1: "MÓDULO 1 . MI TÍTULO PERSONALIZADO",
    # ...
}
```

### ¿Cómo agrego un nuevo estado de módulo?

1. Agrega el estado en el enum `EstatusModulo`
2. Agrega el mapeo en `ESTADO_MAPPING`
3. Agrega el porcentaje en `PORCENTAJE_POR_ESTADO`

### ¿Qué formato de fecha soporta?

Soporta múltiples formatos automáticamente:
- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DD`
- `DD/MM/YYYY`
- `MM/DD/YYYY`
- Y más...

### ¿Cómo optimizo para archivos muy grandes (>100,000 filas)?

1. Aumentar `batch_size` en la configuración:
   ```python
   config = ETLConfig(batch_size=5000)  # Default: 1000
   ```

2. Procesar en chunks:
   ```python
   import pandas as pd

   for chunk in pd.read_excel("archivo_grande.xlsx", chunksize=10000):
       # Procesar chunk
       pass
   ```

3. Desactivar validación si hay problemas de rendimiento:
   ```python
   config = ETLConfig(enable_validation=False)
   ```

---

## 📞 Soporte

Si encuentras problemas no cubiertos en esta guía:

1. Revisa los logs del ETL (nivel INFO)
2. Revisa el archivo de errores generado
3. Consulta la documentación técnica completa en `docs/MAPEO_COMPLETO_ETL_EXCEL.md`
4. Contacta al equipo de desarrollo

---

## 📚 Documentación Adicional

- [Mapeo Completo ETL](MAPEO_COMPLETO_ETL_EXCEL.md) - Mapeo detallado de columnas Excel a BD
- [Análisis de Base de Datos](ANALISIS_COMPLETO_BD_REPORTES.md) - Estructura de la BD
- [Recomendaciones Técnicas](RECOMENDACIONES_TECNICAS.md) - Optimizaciones y mejores prácticas

---

**Última actualización:** 2025-01-18
**Versión del ETL:** 1.0.0
