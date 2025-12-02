# 📦 GUÍA DE INSTALACIÓN - SMART REPORTS PyQt6

## 🚀 Instalación Rápida

### 1️⃣ Pre-requisitos

**Python 3.11+ requerido**

Verificar versión de Python:
```bash
python --version
# o
python3 --version
```

---

### 2️⃣ Clonar Repositorio (si aún no lo tienes)

```bash
git clone <URL_DEL_REPOSITORIO>
cd smart-reports1
```

---

### 3️⃣ Crear Entorno Virtual (RECOMENDADO)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4️⃣ Instalar Dependencias

**Instalación completa:**
```bash
pip install -r requirements.txt
```

**O instalación paso a paso:**

#### **A) Dependencias Core (OBLIGATORIAS)**
```bash
# PyQt6 - Interfaz gráfica
pip install PyQt6>=6.6.0
pip install PyQt6-WebEngine>=6.6.0

# Procesamiento de datos
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install openpyxl>=3.1.0

# Base de datos
pip install pyodbc>=5.0.0
pip install mysql-connector-python>=8.0.33

# Validación
pip install pydantic>=2.0.0
```

#### **B) Dependencias de Visualización**
```bash
# Gráficos
pip install matplotlib>=3.7.0
pip install plotly>=5.18.0
pip install kaleido>=0.2.1

# Reportes PDF
pip install reportlab>=4.0.0

# Imágenes
pip install pillow>=10.0.0
```

#### **C) Utilidades**
```bash
pip install python-dateutil>=2.8.2
pip install colorama>=0.4.6
pip install colorlog>=6.7.0
pip install python-dotenv>=1.0.0
```

#### **D) Testing (OPCIONAL)**
```bash
pip install pytest>=7.4.0
pip install pytest-cov>=4.1.0
```

#### **E) Empaquetado (OPCIONAL)**
```bash
pip install pyinstaller>=6.0.0
```

---

### 5️⃣ Instalar Driver ODBC para SQL Server (si usas SQL Server)

#### **Windows:**
1. Descargar e instalar [Microsoft ODBC Driver 17 para SQL Server](https://go.microsoft.com/fwlink/?linkid=2249004)
2. Ejecutar el instalador y seguir instrucciones

#### **Linux (Ubuntu/Debian):**
```bash
# Instalar unixODBC
sudo apt-get install unixodbc unixodbc-dev

# Agregar repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Actualizar e instalar driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

#### **macOS:**
```bash
# Instalar con Homebrew
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17
```

---

### 6️⃣ Configurar Variables de Entorno (OPCIONAL)

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env
DB_HOST=localhost
DB_PORT=1433
DB_NAME=smart_reports
DB_USER=tu_usuario
DB_PASSWORD=tu_password
```

---

### 7️⃣ Ejecutar la Aplicación

```bash
python main_pyqt6.py
```

**O directamente:**
```bash
cd /home/user/smart-reports1
python3 main_pyqt6.py
```

---

## 🔍 Verificar Instalación

### Verificar que PyQt6 esté correctamente instalado:

```bash
python -c "from PyQt6.QtWidgets import QApplication; print('✅ PyQt6 instalado correctamente')"
```

### Verificar que PyQt6-WebEngine esté instalado:

```bash
python -c "from PyQt6.QtWebEngineWidgets import QWebEngineView; print('✅ PyQt6-WebEngine instalado correctamente')"
```

### Verificar todas las dependencias:

```bash
python -c "
import PyQt6
import pandas
import numpy
import openpyxl
import reportlab
import matplotlib
import plotly
print('✅ Todas las dependencias core instaladas correctamente')
"
```

---

## 📊 Dependencias por Funcionalidad

| Funcionalidad | Dependencias | Obligatoria |
|--------------|--------------|-------------|
| **Interfaz Gráfica** | PyQt6, PyQt6-WebEngine | ✅ Sí |
| **Gráficos D3.js** | PyQt6-WebEngine | ✅ Sí |
| **Procesamiento de Datos** | pandas, numpy, openpyxl | ✅ Sí |
| **Base de Datos SQL Server** | pyodbc, ODBC Driver 17 | ⚠️ Si usas SQL Server |
| **Base de Datos MySQL** | mysql-connector-python | ⚠️ Si usas MySQL |
| **Exportar PDF** | reportlab | ✅ Sí (para gráficos) |
| **Gráficos Matplotlib** | matplotlib | ✅ Sí |
| **Testing** | pytest, pytest-cov | ❌ Opcional |
| **Empaquetado .exe** | pyinstaller | ❌ Opcional |

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'PyQt6'"
```bash
pip install PyQt6 PyQt6-WebEngine
```

### Error: "QtWebEngineWidgets must be imported before QApplication"
✅ **YA CORREGIDO** en `main_pyqt6.py`

### Error: "No se puede conectar a SQL Server"
1. Verificar que ODBC Driver 17 esté instalado
2. Verificar credenciales de conexión
3. Verificar firewall/red

### Error: "ImportError: reportlab"
```bash
pip install reportlab
```

### Error en Linux: "libQt6WebEngineCore.so.6: cannot open shared object file"
```bash
sudo apt-get install libqt6webengine6
```

---

## 📝 Notas Adicionales

### **Migración desde CustomTkinter**
- ✅ La migración a PyQt6 está **100% completa**
- ❌ CustomTkinter ya **NO se usa** en el proyecto
- ✅ Todas las funcionalidades migradas a PyQt6
- ✅ Mejor rendimiento y capacidades profesionales

### **Logo del Instituto**
Para que aparezca el logo del Instituto Hutchison Ports:
1. Colocar `LogoInstitutoHP-blanco.png` en: `assets/images/`
2. El sistema tiene fallback automático si no se encuentra

### **Temas**
- Login siempre inicia en **modo claro**
- Dentro de la app puedes cambiar entre **claro/oscuro**
- Todos los componentes se actualizan automáticamente

---

## ✅ Checklist de Instalación

- [ ] Python 3.11+ instalado
- [ ] Entorno virtual creado y activado
- [ ] `requirements.txt` instalado completamente
- [ ] ODBC Driver instalado (si usas SQL Server)
- [ ] Variables de entorno configuradas (opcional)
- [ ] Verificación de imports exitosa
- [ ] Aplicación ejecutándose correctamente

---

## 🆘 Soporte

Si tienes problemas:
1. Verificar versión de Python (`python --version`)
2. Verificar que el entorno virtual esté activado
3. Reinstalar dependencias: `pip install -r requirements.txt --upgrade`
4. Verificar logs en consola al ejecutar

---

## 📚 Documentación Adicional

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt Documentation](https://doc.qt.io/qt-6/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**¡Listo para usar Smart Reports con PyQt6! 🎉**
