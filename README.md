# 🏢 Smart Reports - Instituto Hutchison Ports

Sistema de gestión y análisis de capacitación empresarial con dashboards interactivos.

---

## 📐 Arquitectura del Proyecto

Este proyecto sigue la estructura **EXACTA de Android Studio**, adaptada para Python/CustomTkinter:

```
smart-reports/
│
├── src/main/                         # Como Android Studio
│   ├── python/                       # Como "java/" en Android
│   │   ├── ui/                       # UI Components
│   │   │   ├── activities/           # Ventanas principales (MainActivity, etc.)
│   │   │   ├── fragments/            # Paneles y menús (Fragments)
│   │   │   └── widgets/              # Componentes reutilizables (Custom Views)
│   │   │
│   │   ├── viewmodels/               # Lógica de UI (ViewModels)
│   │   ├── data/                     # Capa de datos
│   │   │   ├── repositories/         # Repositorios (acceso a datos)
│   │   │   └── database/             # Queries SQL
│   │   │
│   │   ├── domain/                   # Lógica de negocio
│   │   │   ├── models/               # Modelos de dominio
│   │   │   └── services/             # Servicios de negocio
│   │   │
│   │   └── utils/                    # Utilidades
│   │
│   └── res/                          # Recursos (como Android)
│       ├── config/                   # Configuración (strings.xml equivalente)
│       └── themes/                   # Temas (themes.xml equivalente)
│
├── docs/                             # Documentación completa
│   ├── ARQUITECTURA.md
│   ├── FIXES_APPLIED.md
│   └── assets/
│
├── tests/                            # Tests (como Android)
│   └── java/
│       ├── unit/
│       └── integration/
│
├── config/                           # Config legado (mantener por compatibilidad)
├── database/                         # Scripts SQL
│
└── main.py                           # Punto de entrada (MainActivity equivalente)
```

---

## 🎯 Comparación con Android Studio

| Android Studio | Smart Reports (Python) |
|----------------|------------------------|
| `src/main/java/` | `src/main/python/` |
| `Activity` | `activities/ventana_*.py` |
| `Fragment` | `fragments/panel_*.py` |
| `Custom View` | `widgets/` |
| `ViewModel` | `viewmodels/` |
| `Repository` | `data/repositories/` |
| `res/values/` | `res/config/` |
| `res/drawable/` | (no usado - CustomTkinter) |
| `AndroidManifest.xml` | `main.py` |

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar base de datos
Edita `src/main/res/config/settings.py` con tus credenciales:
```python
DATABASE_CONFIG = {
    'server': 'tu_servidor',
    'database': 'tu_bd',
    'username': 'usuario',
    'password': 'contraseña'
}
```

### 3. Ejecutar aplicación
```bash
python main.py
```

---

## 📁 Estructura Detallada

### 🎨 UI Layer (`src/main/python/ui/`)

#### **activities/** - Ventanas Principales
Como `MainActivity`, `LoginActivity` en Android
- `ventana_login.py` - Pantalla de inicio de sesión
- `ventana_principal_view.py` - Ventana principal de la app

#### **fragments/** - Paneles y Módulos
Como `Fragment` en Android (reutilizables, pueden agregarse/quitarse)
- `dashboard/` - Dashboards gerenciales
- `reportes/` - Generación de reportes
- `configuracion/` - Configuración del sistema
- `menu_*.py` - Módulos de menú

#### **widgets/** - Componentes Personalizados
Como `Custom View` en Android
- `charts/` - Gráficos interactivos
- `navigation/` - Barras de navegación
- `forms/` - Formularios reutilizables

---

### 🧠 ViewModels (`src/main/python/viewmodels/`)

Lógica de UI separada de la vista (patrón MVVM)
- `database_query_controller.py` - Consultas a BD
- `file_import_controller.py` - Importación de archivos
- `reports_controller.py` - Generación de reportes
- `navigation_controller.py` - Navegación entre pantallas

---

### 💾 Data Layer (`src/main/python/data/`)

#### **repositories/** - Acceso a Datos
- `persistence/` - Conexiones a BD
- Patrón Repository para abstraer acceso a datos

#### **database/** - SQL Queries
- `queries_hutchison.py` - Queries específicas del proyecto

---

### 🏗️ Domain Layer (`src/main/python/domain/`)

#### **models/** - Modelos de Negocio
Entidades del dominio (si existen)

#### **services/** - Servicios de Negocio
- `importador_capacitacion.py` - Lógica de importación
- `metricas_gerenciales_service.py` - Cálculo de métricas

---

### ⚙️ Res (`src/main/res/`)

Recursos de configuración (como `res/values/` en Android)
- `config/` - Configuración de la app (settings, themes)
- `themes/` - Definición de temas visuales

---

## 🔄 Flujo de Datos (MVVM)

```
User Interaction
    ↓
Activity/Fragment (View)
    ↓
ViewModel (Lógica)
    ↓
Repository (Acceso a datos)
    ↓
Database/API
```

**Ejemplo concreto**:
1. Usuario hace clic en "Generar Reporte" → `fragments/menu_reportes.py`
2. Fragment llama a ViewModel → `viewmodels/reports_controller.py`
3. ViewModel consulta Repository → `data/repositories/`
4. Repository ejecuta query → `data/database/queries_hutchison.py`
5. Datos regresan por la cadena hasta el Fragment
6. Fragment actualiza la UI con los resultados

---

## 🎓 Para Desarrolladores

### Si vienes de **Android Studio**:
- ✅ Estructura **idéntica** a Android
- `activities/` = Activities
- `fragments/` = Fragments
- `widgets/` = Custom Views
- `viewmodels/` = ViewModels
- `res/` = Resources

### Si vienes de **React**:
- `activities/` = Pages (páginas completas)
- `fragments/` = Containers (secciones de páginas)
- `widgets/` = Components (componentes reutilizables)
- `viewmodels/` = Custom Hooks (lógica separada)

---

## 📝 Cómo Agregar Nueva Funcionalidad

### Agregar nueva pantalla (Activity):
1. Crear `src/main/python/ui/activities/ventana_NOMBRE.py`
2. Importar en `main.py`

### Agregar nuevo panel (Fragment):
1. Crear `src/main/python/ui/fragments/panel_NOMBRE.py`
2. Importar en activity correspondiente

### Agregar nueva lógica (ViewModel):
1. Agregar método en ViewModel existente
2. O crear nuevo: `src/main/python/viewmodels/NOMBRE_controller.py`

---

## 🛠️ Tecnologías

- **UI Framework**: CustomTkinter (Python)
- **Gráficos**: Matplotlib
- **Base de Datos**: SQL Server (ODBC Driver 17)
- **Arquitectura**: MVVM + Repository Pattern
- **Estructura**: Android Studio Style

---

## 📚 Documentación

Toda la documentación está en `/docs/`:
- `ARQUITECTURA.md` - Arquitectura detallada
- `FIXES_APPLIED.md` - Historial de correcciones
- `MAPEO_COLUMNAS_EXCEL_BD.md` - Mapeo de columnas

---

## 🧪 Testing

```bash
# Ejecutar tests unitarios
python -m pytest tests/java/unit/

# Ejecutar tests de integración
python -m pytest tests/java/integration/
```

---

## 📞 Soporte

Para consultas o issues:
1. Revisa la documentación en `/docs/`
2. Consulta el código en estructura Android Studio
3. Sigue los patrones establecidos

---

**Versión**: 2.1 - Android Studio Structure
**Última actualización**: 2025-11-11
**Arquitectura**: MVVM + Repository Pattern + Android Studio Layout
