# 🪟 Instalacion Rapida - Windows

Guia especifica para instalar Smart Reports en Windows.

---

## ⚡ Pasos Rapidos (5 minutos)

### PASO 1: Verificar Python

Abre **PowerShell** y ejecuta:

```powershell
python --version
```

Debes tener **Python 3.9 o superior**. Si no:
- Descarga: https://www.python.org/downloads/
- Durante instalacion: ✅ Marcar "Add Python to PATH"

---

### PASO 2: Instalar Dependencias

En PowerShell, en la carpeta del proyecto:

```powershell
# Navegar a la carpeta del proyecto
cd C:\Users\tu_usuario\OneDrive\Documentos\smart-reports1-main\smart-reports1-main

# Instalar dependencias
pip install -r requirements.txt
```

**IMPORTANTE:** Si te da error de permisos:
```powershell
pip install --user -r requirements.txt
```

---

### PASO 3: Configurar Base de Datos

Abre el archivo `config\database.py` con Notepad y cambia la **linea 11**:

**Para MySQL (casa - pruebas):**
```python
DB_TYPE = 'mysql'
```

**Para SQL Server (trabajo - produccion):**
```python
DB_TYPE = 'sqlserver'
```

**Luego configura tus credenciales:**
- SQL Server: lineas 16-26
- MySQL: lineas 31-39

---

### PASO 4: Ejecutar

```powershell
python main.py
```

**Login:**
- Usuario: `admin`
- Password: `1234`

---

## 🐛 Errores Comunes en Windows

### Error: "python no se reconoce como comando"

**Solucion:** Agrega Python al PATH manualmente:
1. Busca "Variables de entorno" en Windows
2. Edita "Path" en Variables del sistema
3. Agrega: `C:\Users\tu_usuario\AppData\Local\Programs\Python\Python311`

### Error: "pip no se reconoce como comando"

**Solucion:**
```powershell
python -m pip install -r requirements.txt
```

### Error: "UnicodeDecodeError" o "charmap codec"

**YA RESUELTO** en la ultima version. Si persiste:
```powershell
# Asegurate de tener la version mas reciente
git pull
```

### Error: "pyodbc no se puede instalar"

**Solucion:** Instala ODBC Driver 17 for SQL Server:
- Descarga: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Luego: `pip install pyodbc`

### Error: "tkinterweb no funciona"

**Solucion alternativa:**
```powershell
pip install tkhtmlview
```

Los graficos seguiran funcionando con una version simplificada.

### Error: Puerto 8050 en uso

**Solucion:** Cambia el puerto en `config\settings.py`:
```python
D3_CONFIG = {
    "http_server_port": 8051,  # Cambiar a otro puerto
}
```

---

## 📦 Dependencias Opcionales

### Solo lo Basico (minimo para funcionar):

```powershell
pip install customtkinter pandas openpyxl reportlab matplotlib
```

### Para SQL Server (trabajo):

```powershell
pip install pyodbc
```

**IMPORTANTE:** Tambien necesitas **ODBC Driver 17 for SQL Server** instalado en Windows.

### Para MySQL (casa):

```powershell
pip install mysql-connector-python
```

### Para D3.js Interactivo (recomendado):

```powershell
pip install tkinterweb
```

---

## 🚀 Verificacion Completa

Ejecuta este script para verificar todo:

```powershell
python verificar_dependencias.py
```

Te mostrara que falta instalar.

---

## 🎯 Checklist de Instalacion

- [ ] Python 3.9+ instalado
- [ ] `pip install -r requirements.txt` ejecutado sin errores
- [ ] `config\database.py` configurado (linea 11)
- [ ] Credenciales de BD configuradas
- [ ] `python verificar_dependencias.py` todo ✅
- [ ] `python main.py` abre la aplicacion
- [ ] Login: admin / 1234 funciona
- [ ] Ir a "Dashboards Gerenciales" muestra graficos

---

## 📁 Estructura del Proyecto

```
smart-reports1-main\
├── main.py                    ← Ejecutar este archivo
├── config\
│   ├── database.py            ← Configurar aqui (linea 11)
│   └── settings.py
├── src\
├── requirements.txt           ← Archivo limpio (ASCII)
└── verificar_dependencias.py ← Verificar instalacion
```

---

## 🔧 Configuracion SQL Server vs MySQL

### SQL Server (Trabajo):

En `config\database.py`:

```python
DB_TYPE = 'sqlserver'

SQLSERVER_CONFIG = {
    'server': 'tu_servidor',        # Ejemplo: 'localhost' o '192.168.1.100'
    'port': 1433,
    'database': 'tngcore',
    'username': 'tu_usuario',
    'password': 'tu_password',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'no',     # 'yes' para Windows Auth
}
```

### MySQL (Casa):

En `config\database.py`:

```python
DB_TYPE = 'mysql'

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'tu_password',
    'database': 'tngcore',
}
```

---

## ⚡ Ejecutar en PowerShell

```powershell
# Opcion 1: Ejecutar directamente
python main.py

# Opcion 2: Con Python launcher
py main.py

# Opcion 3: Si Python no esta en PATH
C:\Users\tu_usuario\AppData\Local\Programs\Python\Python311\python.exe main.py
```

---

## 🐍 Actualizar pip (si es necesario)

```powershell
python -m pip install --upgrade pip
```

---

## 📚 Archivos de Ayuda

- `INSTALACION_RAPIDA.md` - Guia general multiplataforma
- `GUIA_CONFIGURACION.md` - Configuracion detallada de BD
- `ESTRUCTURA_MODULAR.md` - Estructura de archivos divididos
- `README.md` - Documentacion completa

---

## ✅ Todo Listo!

Si todos los pasos funcionaron:

```powershell
python main.py
```

**Login:** `admin` / `1234`

**Ve a:** "Dashboards Gerenciales" y disfruta de 20 graficos D3.js interactivos!

---

**v2.0.1** - Optimizado para Windows
