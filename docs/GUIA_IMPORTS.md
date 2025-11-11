# 📋 Guía Rápida de Imports - Android Studio Structure

## ✅ Imports Correctos (Nueva Estructura)

### 🎨 Config y Temas
```python
# Config
from src.main.res.config.settings import UI_CONFIG, APP_NAME
from src.main.res.config.themes import HUTCHISON_COLORS, DARK_THEME
from src.main.res.config.gestor_temas import get_theme_manager
```

### 📱 Activities (Ventanas Principales)
```python
from src.main.python.ui.activities.ventana_login import LoginWindow
from src.main.python.ui.activities.ventana_principal_view import VentanaPrincipalView
```

### 📦 Fragments (Paneles Modulares)
```python
# Imports individuales
from src.main.python.ui.fragments.menu_dashboard import show_dashboard_menu
from src.main.python.ui.fragments.menu_reportes import show_reportes_menu
from src.main.python.ui.fragments.menu_actualizar import show_actualizar_menu

# O import global (recomendado)
from src.main.python.ui.fragments import (
    show_dashboard_menu,
    show_reportes_menu,
    show_actualizar_menu,
    show_configuracion_menu,
    show_consultas_menu
)
```

### 🧩 Widgets (Custom Views)
```python
# Navegación
from src.main.python.ui.widgets.navigation.barra_lateral import ModernSidebar
from src.main.python.ui.widgets.navigation.barra_superior import TopBar

# Charts
from src.main.python.ui.widgets.charts.interactive_chart_card import InteractiveChartCard
from src.main.python.ui.widgets.charts.tarjeta_metrica import TarjetaMetrica

# Forms
from src.main.python.ui.widgets.forms.selector_unidad import SelectorUnidad
```

### 🧠 ViewModels (Lógica de UI)
```python
from src.main.python.viewmodels.database_query_controller import DatabaseQueryController
from src.main.python.viewmodels.file_import_controller import FileImportController
from src.main.python.viewmodels.reports_controller import ReportsController
from src.main.python.viewmodels.navigation_controller import NavigationController
```

### 💾 Data Layer
```python
# Database connection
from src.main.python.data.repositories.persistence.mysql.connection import DatabaseConnection

# Queries
from src.main.python.data.database.queries_hutchison import (
    QUERY_TOTAL_USUARIOS,
    QUERY_USUARIOS_POR_UNIDAD,
    ejecutar_query_simple,
    ejecutar_query_lista
)
```

### 🏗️ Domain Services
```python
from src.main.python.domain.services.importador_capacitacion import ImportadorCapacitacion
from src.main.python.domain.services.metricas_gerenciales_service import MetricasGerencialesService
```

### 🛠️ Utils
```python
from src.main.python.utils.visualization.d3_generator import D3ChartGenerator
from src.main.python.utils.visualization.pdf_generator import PDFGenerator
```

---

## ❌ Imports Antiguos (NO USAR)

```python
# ❌ OBSOLETO - NO USAR
from config.themes import HUTCHISON_COLORS
from config.gestor_temas import get_theme_manager
from src.infrastructure.persistence.mysql.connection import DatabaseConnection
from src.interfaces.ui.controllers.database_query_controller import DatabaseQueryController
from src.interfaces.ui.views.components.navigation.barra_lateral import ModernSidebar
from src.interfaces.ui.views.menus import show_dashboard_menu
```

---

## 🔄 Tabla de Migración

| ❌ Import Antiguo | ✅ Import Nuevo |
|-------------------|-----------------|
| `from config.themes import ...` | `from src.main.res.config.themes import ...` |
| `from config.gestor_temas import ...` | `from src.main.res.config.gestor_temas import ...` |
| `from src.infrastructure.persistence.mysql.connection import ...` | `from src.main.python.data.repositories.persistence.mysql.connection import ...` |
| `from src.interfaces.ui.controllers.* import ...` | `from src.main.python.viewmodels.* import ...` |
| `from src.interfaces.ui.views.components.* import ...` | `from src.main.python.ui.widgets.* import ...` |
| `from src.interfaces.ui.views.menus import ...` | `from src.main.python.ui.fragments import ...` |
| `from src.interfaces.ui.views.windows.* import ...` | `from src.main.python.ui.activities.* import ...` |
| `from src.application.services.* import ...` | `from src.main.python.domain.services.* import ...` |
| `from src.infrastructure.database.* import ...` | `from src.main.python.data.database.* import ...` |

---

## 📝 Ejemplos Completos

### main.py (MainActivity)
```python
import customtkinter as ctk
from src.main.res.config.settings import UI_CONFIG, APP_NAME
from src.main.python.ui.activities.ventana_login import LoginWindow
from src.main.python.ui.activities.ventana_principal_view import VentanaPrincipalView as MainWindow

def main():
    ctk.set_appearance_mode(UI_CONFIG["appearance_mode"])
    root = ctk.CTk()

    def on_login_success(username, role):
        app = MainWindow(root, username=username, user_role=role)

    login_window = LoginWindow(root, on_login_success)
    root.mainloop()
```

### Crear un Fragment nuevo
```python
# src/main/python/ui/fragments/mi_nuevo_panel.py

import customtkinter as ctk
from src.main.res.config.themes import HUTCHISON_COLORS
from src.main.python.viewmodels.database_query_controller import DatabaseQueryController

class MiNuevoPanel(ctk.CTkFrame):
    def __init__(self, parent, db_controller):
        super().__init__(parent)
        self.db_controller = db_controller
        self._create_ui()

    def _create_ui(self):
        # Tu UI aquí
        pass
```

### Crear un ViewModel nuevo
```python
# src/main/python/viewmodels/mi_controller.py

class MiController:
    def __init__(self, db_connection):
        self.conn = db_connection

    def mi_logica(self, parametros):
        # Tu lógica aquí
        return resultado
```

---

## 🎯 Recordatorios

1. **SIEMPRE** usar rutas desde `src.main.*`
2. **Fragments** = Paneles modulares (antes "menus" o "panels")
3. **Activities** = Ventanas completas (antes "windows")
4. **Widgets** = Componentes reutilizables (antes "components")
5. **ViewModels** = Lógica de UI (antes "controllers")
6. **Config** ahora está en `src.main.res.config.*`

---

## 🚀 Testing de Imports

Para verificar que tus imports funcionan:

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from src.main.res.config.settings import UI_CONFIG, APP_NAME
print(f'✅ Imports OK: {APP_NAME}')
"
```

---

**Última actualización**: 2025-11-11
**Versión**: 2.1 - Android Studio Structure
