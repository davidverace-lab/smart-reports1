# 🔧 Guía de Configuración - Smart Reports

Esta guía te explica cómo configurar el sistema para que funcione con **SQL Server (trabajo)** o **MySQL (casa)**.

---

## 📊 Cambiar entre SQL Server y MySQL

### ✅ OPCIÓN 1: Editar config/database.py (MÁS FÁCIL)

Abre el archivo `config/database.py` y cambia la línea 11:

```python
# Para usar MySQL (casa):
DB_TYPE = 'mysql'

# Para usar SQL Server (trabajo):
DB_TYPE = 'sqlserver'
```

**Luego configura los datos de conexión en la misma sección:**

#### Para SQL Server (líneas 16-26):
```python
SQLSERVER_CONFIG = {
    'server': 'tu_servidor',        # Ejemplo: 'localhost' o '192.168.1.100'
    'port': 1433,                   # Puerto SQL Server (normalmente 1433)
    'database': 'tngcore',          # Nombre de tu base de datos
    'username': 'tu_usuario',       # Usuario SQL Server
    'password': 'tu_password',      # Password
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'no',     # 'yes' para Windows Authentication
    'encrypt': 'yes',
    'trust_server_certificate': 'yes'
}
```

#### Para MySQL (líneas 31-39):
```python
MYSQL_CONFIG = {
    'host': 'localhost',            # Servidor MySQL
    'port': 3306,                   # Puerto MySQL (normalmente 3306)
    'user': 'root',                 # Usuario MySQL
    'password': 'tu_password',      # Password
    'database': 'tngcore',          # Nombre de tu base de datos
    'charset': 'utf8mb4',
    'autocommit': False
}
```

---

### ✅ OPCIÓN 2: Usar archivo .env (RECOMENDADO PARA PRODUCCIÓN)

1. **Crea un archivo `.env`** en la raíz del proyecto:

```bash
# En la carpeta smart-reports1/
cp .env.example .env
```

2. **Edita el archivo `.env`** con tus datos:

#### Para MySQL:
```bash
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=tngcore
```

#### Para SQL Server:
```bash
DB_TYPE=sqlserver
DB_HOST=tu_servidor
DB_PORT=1433
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=tngcore
```

3. **El sistema leerá automáticamente el .env** al ejecutar `python main.py`

---

## 🚀 Servidor HTTP 8050 para D3.js

### ¿Qué es el servidor HTTP 8050?

Es un **servidor HTTP local automático** que se ejecuta en segundo plano cuando abres la aplicación. Es NECESARIO para que los gráficos D3.js funcionen dentro de CustomTkinter.

### ¿Cómo funciona?

1. **Al ejecutar `python main.py`**, el sistema:
   - Abre la aplicación Desktop
   - Automáticamente inicia un servidor HTTP en `http://localhost:8050`
   - Guarda los gráficos D3.js como archivos HTML temporales
   - Los carga desde `http://localhost:8050/chart_xxx.html`
   - JavaScript se ejecuta correctamente (NO funciona con `file://`)

2. **Es 100% AUTOMÁTICO:**
   - ❌ NO necesitas abrir nada manualmente
   - ❌ NO necesitas un navegador web
   - ✅ Se ejecuta en background al abrir la app
   - ✅ Se cierra automáticamente al cerrar la app

3. **Los gráficos se ven DENTRO de la aplicación:**
   ```
   ┌─────────────────────────────────────┐
   │  Smart Reports (Desktop App)        │
   ├─────────────────────────────────────┤
   │  📊 Dashboards Gerenciales          │
   │  ┌─────────────────────────────┐   │
   │  │  [Gráfico D3.js interactivo]│   │ ← Renderizado desde http://localhost:8050
   │  │  Barra azul navy...         │   │
   │  └─────────────────────────────┘   │
   └─────────────────────────────────────┘
   ```

### Verificación del servidor:

Si quieres verificar que está corriendo, abre un navegador mientras la app está abierta y ve a:
```
http://localhost:8050
```

Deberías ver archivos HTML de los gráficos.

**IMPORTANTE:** El servidor SOLO funciona mientras la app Desktop está abierta.

---

## 📦 Instalación de Dependencias

### Para MySQL (Casa):
```bash
pip install mysql-connector-python
```

### Para SQL Server (Trabajo):
```bash
pip install pyodbc
```

**IMPORTANTE para SQL Server:**
También necesitas instalar **ODBC Driver 17 for SQL Server**:
- Windows: [Descargar aquí](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Linux: `sudo apt-get install unixodbc-dev`

---

## 🗂️ Carpetas Antiguas

**NO**, aún NO hemos borrado las carpetas antiguas (`interfaz/`, `nucleo/`, `database/`).

Están ahí por si acaso necesitas revisar código antiguo. Una vez que confirmes que todo funciona bien, puedes borrarlas:

```bash
# SOLO SI TODO FUNCIONA BIEN
rm -rf interfaz/
rm -rf nucleo/
# NO borres database/ todavía, tiene importar_excel_simple.py
```

---

## 🧪 Probar el Sistema

### 1. Configurar Base de Datos

Edita `config/database.py` línea 11:
```python
DB_TYPE = 'mysql'  # o 'sqlserver'
```

### 2. Configurar Credenciales

Edita las secciones correspondientes (líneas 16-26 o 31-39)

### 3. Ejecutar

```bash
python main.py
```

### 4. Verificar Dashboards

1. Login con `admin` / `1234`
2. Clic en "📊 Dashboards Gerenciales"
3. Deberías ver 20 gráficos D3.js interactivos
4. Si no hay datos en BD, verás datos de ejemplo (mock)

---

## 🐛 Troubleshooting

### Error: "pyodbc no está instalado"
```bash
pip install pyodbc
# También instala ODBC Driver 17 for SQL Server
```

### Error: "mysql-connector-python no está instalado"
```bash
pip install mysql-connector-python
```

### Error: "Puerto 8050 ya está en uso"
- Cierra cualquier otra aplicación que use el puerto 8050
- O cambia el puerto en `config/settings.py`:
  ```python
  D3_CONFIG = {
      "http_server_port": 8051,  # Cambiar a otro puerto
  }
  ```

### Gráficos D3.js no se muestran
1. Verifica que `tkinterweb` esté instalado: `pip install tkinterweb`
2. Ejecuta la app y verifica en consola que no haya errores 404
3. El servidor HTTP se inicia automáticamente, no hagas nada manualmente

### Error de conexión a BD
1. Verifica que el servidor de BD esté corriendo
2. Verifica credenciales en `config/database.py`
3. Verifica que la base de datos `tngcore` exista
4. Verifica que las tablas `instituto_*` existan

---

## 📋 Checklist Final

- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Configurar tipo de BD en `config/database.py` línea 11
- [ ] Configurar credenciales de conexión (líneas 16-26 o 31-39)
- [ ] Ejecutar: `python main.py`
- [ ] Login: `admin` / `1234`
- [ ] Ir a "📊 Dashboards Gerenciales"
- [ ] Verificar que se vean los 20 gráficos D3.js

---

**¿Necesitas ayuda?** Revisa los logs en la consola cuando ejecutas `python main.py`.
