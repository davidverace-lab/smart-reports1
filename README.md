# Smart Reports - Instituto Hutchison Ports

Sistema de reportes y dashboards para capacitación.

## 🚀 Ejecutar la Aplicación

```bash
python ejecutar_app.py
```

**Credenciales por defecto:**
- Usuario: `admin` / Contraseña: `1234`
- Usuario: `demo` / Contraseña: `demo`

## 📦 Dependencias

```bash
pip install customtkinter tkinterweb mysql-connector-python pandas openpyxl reportlab
```

## 📂 Estructura

```
smart-reports1/
├── ejecutar_app.py          # ⭐ EJECUTAR AQUÍ
├── database/                 # Scripts SQL e importación
├── interfaz/                 # UI de la aplicación
├── nucleo/                   # Lógica de negocio
└── data/                     # Excel para importar (crear carpeta)
```

## 📥 Importar Datos de Excel

1. Coloca tus 3 archivos Excel en `data/`
2. Ejecuta:
```bash
python database/importar_excel_simple.py
```

## ⚙️ Configuración MySQL

Edita `database/importar_excel_simple.py`:
```python
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'TU_PASSWORD',  # ⚠️ Cambiar
    'database': 'tngcore'
}
```

## 🎨 Características

- ✅ Dashboards D3.js interactivos
- ✅ Reportes PDF profesionales
- ✅ Gestión de usuarios
- ✅ Importación masiva desde Excel
- ✅ Temas claro/oscuro

---

**v2.0** - Instituto Hutchison Ports © 2025
