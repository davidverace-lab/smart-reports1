# 🚀 Guía Completa de Migración a PyQt6

## 📋 Estado de la Migración

### ✅ **COMPLETADO** - Infraestructura Base
- [x] Sistema de temas QSS (oscuro/claro)
- [x] main_pyqt6.py - Punto de entrada
- [x] LoginWindow - Ventana de login funcional
- [x] MainWindow - Ventana principal con navegación
- [x] D3ChartWidget - Gráficos D3.js con QWebEngineView
- [x] Estructura de directorios PyQt6

### 🚧 **PENDIENTE** - Migración de Paneles (55 archivos)
Los siguientes componentes necesitan ser migrados de CustomTkinter a PyQt6:

#### Paneles Principales (5):
- [ ] Dashboard (panel_control_ejecutivo, panel_dashboards_gerenciales, panel_rrhh)
- [ ] Gráficos
- [ ] Consultas
- [ ] Reportes
- [ ] Configuración

#### Componentes de UI (50+ archivos):
- [ ] Componentes de gráficos (tarjetas, visualizadores)
- [ ] Herramientas de importación
- [ ] Componentes de navegación
- [ ] Modales y diálogos
- [ ] Tablas y formularios

---

## 🎯 Arquitectura de la Nueva Aplicación

```
smart-reports1/
├── main_pyqt6.py                          # ✅ Nuevo punto de entrada PyQt6
├── main.py                                 # ❌ Antiguo (CustomTkinter) - DEPRECADO
├── requirements.txt                        # ✅ Actualizado con PyQt6
│
├── smart_reports_pyqt6/                    # ✅ NUEVA estructura PyQt6
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── themes.py                       # ✅ Temas QSS (oscuro/claro)
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   │
│   │   ├── windows/
│   │   │   ├── __init__.py
│   │   │   ├── login_window.py             # ✅ Login funcional
│   │   │   └── main_window.py              # ✅ Ventana principal con navegación
│   │   │
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   └── d3_chart_widget.py          # ✅ Gráficos D3.js con QWebEngineView
│   │   │
│   │   └── views/                          # 🚧 AQUÍ VAN LOS PANELES MIGRADOS
│   │       ├── __init__.py
│   │       ├── panel_dashboard.py          # ⏳ Por migrar
│   │       ├── panel_graficos.py           # ⏳ Por migrar
│   │       ├── panel_consultas.py          # ⏳ Por migrar
│   │       ├── panel_reportes.py           # ⏳ Por migrar
│   │       └── panel_config.py             # ⏳ Por migrar
│   │
│   └── templates/
│       └── d3_charts/                      # Templates HTML/JS/CSS externos
│           ├── styles.css
│           ├── chart-bar.js
│           ├── chart-donut.js
│           └── chart-line.js
│
└── smart_reports/                          # ❌ Antigua estructura (CustomTkinter)
    └── ...                                 # Se mantendrá como referencia

```

---

## 🛠️ Cómo Usar la Aplicación Ahora

### Opción 1: Ejecutar con PyQt6 (RECOMENDADO)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar versión PyQt6
python main_pyqt6.py
```

### Opción 2: Ejecutar versión antigua (CustomTkinter - solo referencia)
```bash
python main.py  # Antigua versión
```

---

## 📝 Cómo Migrar un Panel

### Ejemplo: Migrar Panel de Dashboard

#### Paso 1: Analizar el panel actual (CustomTkinter)
```python
# smart_reports/ui/views/dashboard/panel_control_ejecutivo.py (ANTIGUO)
import customtkinter as ctk

class PanelControlEjecutivo(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # ... código CustomTkinter
```

#### Paso 2: Crear panel nuevo (PyQt6)
```python
# smart_reports_pyqt6/ui/views/panel_dashboard.py (NUEVO)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DashboardPanel(QWidget):
    """Panel de Dashboard migrado a PyQt6"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz de usuario"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("📊 Panel de Control Ejecutivo")
        title.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        # Aquí va el resto del contenido del panel...

        # Ejemplo: Botón
        btn = QPushButton("📈 Ver Reporte")
        btn.setFixedHeight(50)
        btn.clicked.connect(self._on_button_click)
        layout.addWidget(btn)

    def _on_button_click(self):
        """Manejar click del botón"""
        print("Botón clickeado")
```

#### Paso 3: Integrar en MainWindow
```python
# smart_reports_pyqt6/ui/windows/main_window.py

# Importar el nuevo panel
from smart_reports_pyqt6.ui.views.panel_dashboard import DashboardPanel

# En _create_content_area(), reemplazar placeholder:
def _create_content_area(self):
    # ...

    # Crear panel de dashboard real (en lugar del placeholder)
    dashboard_panel = DashboardPanel(parent=self, theme_manager=self.theme_manager)
    self.panels['dashboard'] = dashboard_panel
    self.panel_stack.addWidget(dashboard_panel)
```

---

## 🎨 Tabla de Conversión: CustomTkinter → PyQt6

| CustomTkinter | PyQt6 | Notas |
|---------------|-------|-------|
| `CTkFrame` | `QFrame` o `QWidget` | Usar `QFrame` para contenedores con borde |
| `CTkLabel` | `QLabel` | Idéntico en uso básico |
| `CTkButton` | `QPushButton` | `.clicked.connect()` en lugar de `command=` |
| `CTkEntry` | `QLineEdit` | `.textChanged.connect()` para cambios |
| `CTkTextbox` | `QTextEdit` | Multiline text |
| `CTkComboBox` | `QComboBox` | Dropdown/select |
| `CTkCheckBox` | `QCheckBox` | Checkbox |
| `CTkRadioButton` | `QRadioButton` | Radio buttons |
| `CTkScrollableFrame` | `QScrollArea` + `QWidget` | Área scrolleable |
| `CTkTabview` | `QTabWidget` | Pestañas |
| `.grid()` / `.pack()` | `QVBoxLayout`, `QHBoxLayout`, `QGridLayout` | Layouts de PyQt |
| `.configure(fg_color=...)` | `.setStyleSheet("background-color: ...")` | Estilos con QSS |
| `command=callback` | `.clicked.connect(callback)` | Señales y slots |

---

## 🎯 Pasos para Migrar cada Componente

### 1. **Estructura Básica**
```python
# CustomTkinter (ANTIGUO)
import customtkinter as ctk

class MiComponente(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill='both', expand=True)

# PyQt6 (NUEVO)
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class MiComponente(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        # Agregar widgets al layout
```

### 2. **Botones y Callbacks**
```python
# CustomTkinter (ANTIGUO)
btn = ctk.CTkButton(self, text="Click", command=self.on_click)

# PyQt6 (NUEVO)
btn = QPushButton("Click", self)
btn.clicked.connect(self.on_click)
```

### 3. **Layouts**
```python
# CustomTkinter (ANTIGUO)
widget1.pack(side='top', fill='x', padx=10, pady=5)
widget2.pack(side='bottom')

# PyQt6 (NUEVO)
layout = QVBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)
layout.setContentsMargins(10, 5, 10, 5)
self.setLayout(layout)
```

### 4. **Campos de Texto**
```python
# CustomTkinter (ANTIGUO)
entry = ctk.CTkEntry(self, placeholder_text="Nombre")
value = entry.get()

# PyQt6 (NUEVO)
entry = QLineEdit(self)
entry.setPlaceholderText("Nombre")
value = entry.text()
```

### 5. **Listas y Tablas**
```python
# CustomTkinter (ANTIGUO)
# Usualmente con CTkScrollableFrame + Labels

# PyQt6 (NUEVO)
from PyQt6.QtWidgets import QListWidget, QTableWidget

# Lista
list_widget = QListWidget()
list_widget.addItem("Item 1")
list_widget.addItem("Item 2")

# Tabla
table = QTableWidget(10, 3)  # 10 filas, 3 columnas
table.setHorizontalHeaderLabels(["Col1", "Col2", "Col3"])
```

### 6. **Gráficos D3.js**
```python
# CustomTkinter (ANTIGUO)
from smart_reports.ui.components.charts.d3_interactive_chart_card import D3InteractiveChartCard

chart = D3InteractiveChartCard(parent, title="Ventas")
chart.set_chart('bar', datos, subtitulo="Mensuales")

# PyQt6 (NUEVO)
from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget

chart = D3ChartWidget(parent)
chart.set_chart('bar', "Ventas", datos, subtitle="Mensuales", tema='dark')
```

---

## 🎨 Personalización de Temas

Los temas se definen en `smart_reports_pyqt6/config/themes.py` usando QSS (Qt StyleSheets).

### Modificar colores del tema oscuro:
```python
# Editar smart_reports_pyqt6/config/themes.py

DARK_THEME_QSS = f"""
QPushButton {{
    background-color: #TU_COLOR;  # Cambiar aquí
    color: white;
}}

QLabel {{
    color: #TU_COLOR_TEXTO;  # Cambiar aquí
}}
"""
```

### Aplicar estilos inline a un widget específico:
```python
widget.setStyleSheet("""
    QPushButton {
        background-color: #FF0000;
        color: white;
        border-radius: 10px;
    }
""")
```

---

## 🔧 Problemas Comunes y Soluciones

### Error: "ModuleNotFoundError: No module named 'PyQt6'"
```bash
pip install PyQt6 PyQt6-WebEngine
```

### Error: "QtWebEngineProcess no se encuentra"
```bash
# Linux
sudo apt-get install qt6-webengine

# macOS
brew install qt6

# Windows
pip install --upgrade PyQt6-WebEngine
```

### Los gráficos D3.js no se muestran
1. Verificar que `PyQt6-WebEngine` esté instalado
2. Verificar que JavaScript esté habilitado en QWebEngineSettings
3. Revisar la consola para errores de JavaScript

### Los estilos no se aplican
1. Verificar que el tema esté aplicado: `theme_manager.set_theme(app, 'dark')`
2. Para aplicar estilos inline, usar `.setStyleSheet()`
3. Para propiedades dinámicas, usar `.setProperty("class", "value")` y luego `.style().unpolish()` y `.style().polish()`

---

## 📊 Ejemplo Completo: Migrar Panel de Consultas

```python
# smart_reports_pyqt6/ui/views/panel_consultas.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConsultasPanel(QWidget):
    """Panel de Consultas SQL"""

    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)

        self.theme_manager = theme_manager

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("🔍 Consultas SQL")
        title.setFont(QFont("Montserrat", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        layout.addSpacing(20)

        # Campo de búsqueda
        search_layout = QHBoxLayout()

        search_label = QLabel("Buscar:")
        search_label.setFont(QFont("Montserrat", 11, QFont.Weight.Bold))
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escribe para filtrar...")
        self.search_input.textChanged.connect(self._filter_results)
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        layout.addSpacing(10)

        # Tabla de resultados
        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Valor", "Fecha"
        ])
        self.results_table.setAlternatingRowColors(True)
        layout.addWidget(self.results_table)

        # Cargar datos iniciales
        self._load_data()

    def _load_data(self):
        """Cargar datos (conectar a tu BD aquí)"""

        # Ejemplo con datos dummy
        data = [
            ("1", "Item A", "Categoría 1", "100", "2024-01-01"),
            ("2", "Item B", "Categoría 2", "200", "2024-01-02"),
            ("3", "Item C", "Categoría 1", "150", "2024-01-03"),
        ]

        self.results_table.setRowCount(len(data))

        for row, (id, name, cat, val, date) in enumerate(data):
            self.results_table.setItem(row, 0, QTableWidgetItem(id))
            self.results_table.setItem(row, 1, QTableWidgetItem(name))
            self.results_table.setItem(row, 2, QTableWidgetItem(cat))
            self.results_table.setItem(row, 3, QTableWidgetItem(val))
            self.results_table.setItem(row, 4, QTableWidgetItem(date))

    def _filter_results(self, text):
        """Filtrar resultados según búsqueda"""

        for row in range(self.results_table.rowCount()):
            match = False
            for col in range(self.results_table.columnCount()):
                item = self.results_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break

            self.results_table.setRowHidden(row, not match)

    def _refresh_data(self):
        """Actualizar datos"""

        print("🔄 Actualizando datos...")
        self._load_data()
```

Luego en `main_window.py`:
```python
from smart_reports_pyqt6.ui.views.panel_consultas import ConsultasPanel

# En _create_content_area():
consultas_panel = ConsultasPanel(parent=self, theme_manager=self.theme_manager)
self.panels['consultas'] = consultas_panel
self.panel_stack.addWidget(consultas_panel)
```

---

## ✅ Checklist de Migración

Para cada panel/componente:

- [ ] Crear archivo en `smart_reports_pyqt6/ui/views/` o `smart_reports_pyqt6/ui/widgets/`
- [ ] Convertir `CTk*` widgets a `Q*` widgets
- [ ] Cambiar `.pack()`/`.grid()` a Layouts de PyQt
- [ ] Actualizar callbacks: `command=` → `.clicked.connect()`
- [ ] Actualizar acceso a valores: `.get()` → `.text()` / `.value()`
- [ ] Probar con tema oscuro
- [ ] Probar con tema claro
- [ ] Integrar en `main_window.py`
- [ ] Probar funcionalidad completa

---

## 🚀 Próximos Pasos

1. **Instalar dependencias PyQt6**
   ```bash
   pip install -r requirements.txt
   ```

2. **Probar la aplicación base**
   ```bash
   python main_pyqt6.py
   ```

3. **Migrar paneles uno por uno**
   - Empezar con el panel de Dashboard
   - Luego Consultas
   - Luego Reportes
   - Etc.

4. **Actualizar lógica de negocio**
   - La lógica en `smart_reports/core/` se mantiene igual
   - Solo cambiar la capa de presentación (UI)

---

## 📚 Recursos Útiles

- **Documentación PyQt6**: https://doc.qt.io/qtforpython-6/
- **Qt StyleSheets (QSS)**: https://doc.qt.io/qt-6/stylesheet.html
- **Signals & Slots**: https://doc.qt.io/qt-6/signalsandslots.html
- **QWebEngineView**: https://doc.qt.io/qt-6/qwebengineview.html

---

**¡Migración lista para comenzar! 🎉**

La infraestructura base está completa y funcional. Ahora puedes migrar los 55 paneles progresivamente siguiendo esta guía.
