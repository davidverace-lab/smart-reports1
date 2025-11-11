# 📱 Estructura Android Studio - Smart Reports

## 🎯 Estructura Visual Completa

```
smart-reports/
│
├── 📱 src/main/                               # COMO ANDROID STUDIO
│   │
│   ├── 🐍 python/                             # = java/ en Android
│   │   │
│   │   ├── 🎨 ui/                             # INTERFAZ DE USUARIO
│   │   │   ├── activities/                    # 📱 Ventanas principales (MainActivity)
│   │   │   │   ├── ventana_login.py           # LoginActivity
│   │   │   │   └── ventana_principal_view.py  # MainActivity
│   │   │   │
│   │   │   ├── fragments/                     # 📦 Paneles modulares (Fragment)
│   │   │   │   ├── dashboard/                 # DashboardFragment
│   │   │   │   ├── reportes/                  # ReportesFragment
│   │   │   │   ├── configuracion/             # ConfigFragment
│   │   │   │   ├── menu_dashboard.py          # MenuFragment
│   │   │   │   ├── menu_reportes.py
│   │   │   │   ├── menu_actualizar.py
│   │   │   │   └── menu_configuracion.py
│   │   │   │
│   │   │   └── widgets/                       # 🧩 Componentes (Custom Views)
│   │   │       ├── charts/                    # Gráficos personalizados
│   │   │       ├── navigation/                # Barras de navegación
│   │   │       └── forms/                     # Formularios reutilizables
│   │   │
│   │   ├── 🧠 viewmodels/                     # LÓGICA DE UI (ViewModels)
│   │   │   ├── database_query_controller.py   # DatabaseViewModel
│   │   │   ├── file_import_controller.py      # FileImportViewModel
│   │   │   ├── reports_controller.py          # ReportsViewModel
│   │   │   └── navigation_controller.py       # NavigationViewModel
│   │   │
│   │   ├── 💾 data/                           # CAPA DE DATOS
│   │   │   ├── repositories/                  # Repository pattern
│   │   │   │   └── persistence/               # Conexiones BD
│   │   │   │       └── mysql/
│   │   │   │           ├── connection.py
│   │   │   │           └── repositories/
│   │   │   │
│   │   │   └── database/                      # SQL Queries
│   │   │       └── queries_hutchison.py       # Queries específicas
│   │   │
│   │   ├── 🏗️ domain/                         # LÓGICA DE NEGOCIO
│   │   │   ├── models/                        # Modelos del dominio
│   │   │   └── services/                      # Servicios
│   │   │       ├── importador_capacitacion.py
│   │   │       └── metricas_gerenciales_service.py
│   │   │
│   │   └── 🛠️ utils/                          # UTILIDADES
│   │       └── visualization/                 # Herramientas visualización
│   │
│   └── 📦 res/                                # RECURSOS (como Android)
│       ├── config/                            # = values/ (settings)
│       │   ├── settings.py                    # App config
│       │   └── themes.py                      # Theme definitions
│       │
│       └── themes/                            # = themes.xml
│           └── gestor_temas.py                # Theme manager
│
├── 📚 docs/                                   # DOCUMENTACIÓN
│   ├── ARQUITECTURA.md                        # Arquitectura detallada
│   ├── ESTRUCTURA_ANDROID.md                  # Este archivo
│   ├── FIXES_APPLIED.md                       # Historial de cambios
│   ├── README_OLD.md                          # README anterior
│   └── assets/                                # Recursos de docs
│       └── MATRIZ INSTITUTO HP.xlsx           # Modelo de datos
│
├── 🧪 tests/                                  # TESTS
│   └── java/                                  # = androidTest/
│       ├── unit/                              # Unit tests
│       └── integration/                       # Integration tests
│
├── 🗄️ database/                               # SCRIPTS SQL
│   └── sql/
│       └── mysql/
│
├── 📝 config/                                 # Config legado (compatibilidad)
│
├── 📦 _archive/                               # Código archivado
│
└── 🚀 main.py                                 # MainActivity (punto de entrada)
```

---

## 🔄 Comparación Directa

| **Archivo Android** | **Equivalente Python** | **Propósito** |
|---------------------|------------------------|---------------|
| `MainActivity.java` | `main.py` | Punto de entrada |
| `LoginActivity.java` | `activities/ventana_login.py` | Pantalla login |
| `DashboardFragment.java` | `fragments/dashboard/panel_*.py` | Panel dashboard |
| `CustomChartView.java` | `widgets/charts/interactive_chart_card.py` | Gráfico custom |
| `UserViewModel.java` | `viewmodels/database_query_controller.py` | Lógica usuarios |
| `UserRepository.java` | `data/repositories/persistence/mysql/` | Acceso datos |
| `res/values/strings.xml` | `res/config/settings.py` | Configuración |
| `res/values/themes.xml` | `res/themes/gestor_temas.py` | Temas |
| `AndroidManifest.xml` | `main.py` (config inicial) | Manifest |

---

## 📊 Flujo de Navegación

### Como Android (Activity → Fragment → ViewModel → Repository):

```
┌─────────────────────────────────────────┐
│   main.py (MainActivity)                │
│   - Inicializa app                      │
│   - Muestra LoginActivity               │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│   activities/ventana_login.py           │
│   (LoginActivity)                       │
│   - Pantalla de login                   │
│   - Autentica usuario                   │
└─────────────────┬───────────────────────┘
                  │ (login exitoso)
                  ↓
┌─────────────────────────────────────────┐
│   activities/ventana_principal_view.py  │
│   (MainActivity principal)              │
│   - Sidebar, TopBar                     │
│   - Contenedor de Fragments            │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│   fragments/menu_dashboard.py           │
│   (DashboardFragment)                   │
│   - Muestra dashboards                  │
│   - Llama a ViewModel                   │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│   viewmodels/database_query_controller  │
│   (DashboardViewModel)                  │
│   - Procesa lógica                      │
│   - Llama a Repository                  │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│   data/repositories/persistence/        │
│   (Repository)                          │
│   - Ejecuta queries SQL                 │
│   - Retorna datos                       │
└─────────────────────────────────────────┘
```

---

## 🎯 Patrones de Diseño Utilizados

### 1. **MVVM (Model-View-ViewModel)**
```
View (activities/fragments)
    ↕️
ViewModel (viewmodels/)
    ↕️
Model (data/repositories)
```

### 2. **Repository Pattern**
```
ViewModel → Repository → Database
```
Abstrae acceso a datos

### 3. **Fragment Pattern**
```
Activity (container)
└── Fragment 1 (dashboard)
└── Fragment 2 (reportes)
└── Fragment 3 (config)
```
Componentes modulares y reutilizables

---

## 🚀 Ejemplo de Implementación

### Agregar nueva pantalla de "Usuarios"

#### 1. Crear Fragment (Panel)
```python
# src/main/python/ui/fragments/usuarios/panel_usuarios.py

class PanelUsuarios(ctk.CTkFrame):
    """Fragment para gestión de usuarios"""

    def __init__(self, parent, viewmodel):
        super().__init__(parent)
        self.viewmodel = viewmodel  # ViewModel inyectado
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz (SOLO UI)"""
        # Crear widgets aquí
        pass

    def on_buscar_click(self):
        """Evento de búsqueda"""
        # Llamar a ViewModel
        resultado = self.viewmodel.buscar_usuario(self.entry.get())
        self.mostrar_resultado(resultado)
```

#### 2. Crear ViewModel (Lógica)
```python
# src/main/python/viewmodels/usuarios_controller.py

class UsuariosController:
    """ViewModel para usuarios"""

    def __init__(self, repository):
        self.repository = repository

    def buscar_usuario(self, user_id):
        """Lógica de búsqueda (NO UI)"""
        # Validaciones
        if not user_id:
            return None

        # Llamar a Repository
        return self.repository.get_user_by_id(user_id)
```

#### 3. Usar Repository (Datos)
```python
# El repository ya existe en:
# src/main/python/data/repositories/persistence/mysql/repositories/
```

#### 4. Agregar a MainActivity
```python
# En ventana_principal_view.py
from src.main.python.ui.fragments.usuarios.panel_usuarios import PanelUsuarios
from src.main.python.viewmodels.usuarios_controller import UsuariosController

def show_usuarios(self):
    # Crear ViewModel
    viewmodel = UsuariosController(self.repository)

    # Crear Fragment con ViewModel
    panel = PanelUsuarios(self.content_area, viewmodel)
    panel.pack(fill='both', expand=True)
```

---

## ✅ Ventajas de Esta Estructura

### 📱 **Familiar para desarrolladores Android**
Si sabes Android Studio, entiendes esta estructura inmediatamente

### 🧩 **Modular**
Cada Fragment es independiente y reutilizable

### 🧪 **Testeable**
ViewModels sin UI se pueden testear fácilmente

### 🔧 **Mantenible**
Código organizado, fácil de encontrar y modificar

### 📈 **Escalable**
Agregar features es simple: nuevo Fragment + ViewModel

---

## 📝 Convenciones de Nombres

### Android → Python
- `MainActivity` → `ventana_principal_view.py`
- `LoginActivity` → `ventana_login.py`
- `DashboardFragment` → `panel_dashboard.py`
- `CustomChartView` → `interactive_chart_card.py`
- `UserViewModel` → `database_query_controller.py`
- `UserRepository` → `persistence/mysql/repositories/`

### Prefijos:
- **ventana_** = Activity (pantalla completa)
- **panel_** = Fragment (panel modular)
- **menu_** = MenuFragment (menú específico)
- ***_controller** = ViewModel (lógica)

---

## 🎓 Referencias

- [Android Architecture Components](https://developer.android.com/topic/architecture)
- [MVVM Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

**Última actualización**: 2025-11-11
**Versión**: 2.1 - Android Studio Structure
**Arquitectura**: MVVM + Repository + Fragment Pattern
