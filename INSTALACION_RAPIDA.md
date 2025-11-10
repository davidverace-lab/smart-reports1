# ⚡ Instalación Rápida - Smart Reports

Esta guía te ayuda a instalar TODO lo necesario en **5 minutos**.

---

## 🚨 ANTES DE EMPEZAR

Verifica qué te falta ejecutando:

```bash
python verificar_dependencias.py
```

---

## 📦 PASO 1: Instalar Dependencias

### Opción A: Instalar TODO (Recomendado)

```bash
pip install -r requirements.txt
```

**Esto instala:**
- ✅ CustomTkinter (UI)
- ✅ Pandas + Openpyxl (Excel)
- ✅ ReportLab (PDFs)
- ✅ pyodbc (SQL Server)
- ✅ mysql-connector-python (MySQL)
- ✅ tkinterweb (D3.js interactivo)
- ✅ Matplotlib (gráficos)

### Opción B: Solo lo Básico

Si solo quieres probar la app:

```bash
# Mínimo para que funcione
pip install customtkinter pandas openpyxl reportlab matplotlib

# Elige UNA base de datos:
pip install mysql-connector-python  # Para MySQL (casa)
# O
pip install pyodbc                  # Para SQL Server (trabajo)

# Para D3.js interactivo (recomendado):
pip install tkinterweb
```

---

## ⚙️ PASO 2: Configurar Base de Datos

Abre `config/database.py` y cambia **línea 11**:

```python
# Para MySQL (casa):
DB_TYPE = 'mysql'

# Para SQL Server (trabajo):
DB_TYPE = 'sqlserver'
```

**Luego configura tus credenciales** en la sección correspondiente:
- MySQL: líneas 31-39
- SQL Server: líneas 16-26

---

## 🚀 PASO 3: Ejecutar

```bash
python main.py
```

**Login:**
- Usuario: `admin`
- Password: `1234`

---

## ❓ Preguntas Frecuentes

### ¿Las carpetas domain/repositories/ están vacías?

**SÍ**, es NORMAL. Son parte de la arquitectura DDD preparada para el futuro:

```
src/domain/
├── entities/      → VACÍA (entidades de negocio - futuro)
├── repositories/  → VACÍA (interfaces - futuro)
├── value_objects/ → VACÍA (objetos de valor - futuro)
└── services/      → VACÍA (servicios de dominio - futuro)
```

**El código real está en:**
- `src/application/services/` → Servicios de métricas ✅
- `src/infrastructure/` → Conexiones BD, D3.js ✅
- `src/interfaces/ui/` → Interfaz desktop ✅

### ¿El servidor HTTP 8050 funciona automáticamente?

**SÍ**, solo ejecuta `python main.py` y el servidor se abre solo.

**NO necesitas:**
- ❌ Abrir un navegador
- ❌ Ejecutar comandos extra
- ❌ Configurar nada

Los gráficos D3.js se ven **DENTRO de la app**.

### ¿Qué hago si no tengo datos en la BD?

El sistema usa **datos de ejemplo (mock)** automáticamente si no hay datos reales.

Puedes probar todos los dashboards sin problema.

### Error: "pyodbc no está instalado"

```bash
pip install pyodbc
```

También necesitas **ODBC Driver 17 for SQL Server**:
- Windows: [Descargar aquí](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Error: "mysql-connector-python no está instalado"

```bash
pip install mysql-connector-python
```

### Error: "customtkinter no está instalado"

```bash
pip install customtkinter
```

---

## 🧪 Verificación Final

```bash
# 1. Verificar dependencias
python verificar_dependencias.py

# 2. Si TODO está ✅, ejecutar:
python main.py

# 3. Login: admin / 1234
# 4. Ir a "📊 Dashboards Gerenciales"
# 5. Ver 20 gráficos D3.js interactivos
```

---

## 🐛 Troubleshooting

### Puerto 8050 ya está en uso

Cambia el puerto en `config/settings.py`:

```python
D3_CONFIG = {
    "http_server_port": 8051,  # Cambiar a otro puerto
}
```

### Gráficos D3.js no se muestran

1. Verifica que tkinterweb esté instalado:
   ```bash
   pip install tkinterweb
   ```

2. Revisa la consola, debe decir:
   ```
   🎨 Cargando dashboards gerenciales con datos reales...
   ✅ Dashboards cargados exitosamente
   ```

### Error de conexión a BD

1. Verifica que el servidor de BD esté corriendo
2. Verifica credenciales en `config/database.py`
3. Verifica que la base de datos `tngcore` exista

**Si no tienes BD configurada**: ¡No hay problema! El sistema usa datos mock.

---

## 📋 Checklist

- [ ] `pip install -r requirements.txt`
- [ ] Configurar `config/database.py` línea 11
- [ ] Configurar credenciales BD (líneas 16-26 o 31-39)
- [ ] `python verificar_dependencias.py` → TODO ✅
- [ ] `python main.py`
- [ ] Login: `admin` / `1234`
- [ ] Ir a "📊 Dashboards Gerenciales"
- [ ] ¡Ver 20 gráficos D3.js interactivos! 🎉

---

**¿Aún tienes problemas?** Lee `GUIA_CONFIGURACION.md` para info detallada.
