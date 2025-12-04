# ReportCardGitHub - Widget Personalizado PyQt6

## Descripción

`ReportCardGitHub` es un widget personalizado en PyQt6 que replica el diseño de las tarjetas de selección de **GitHub Actions**. Ofrece un diseño profesional y moderno con soporte completo para temas claro y oscuro.

## Características Principales

✅ **Diseño tipo GitHub Actions**: Réplica exacta del estilo visual de las tarjetas de GitHub
✅ **Esquinas redondeadas**: Border-radius de 8px para un aspecto moderno
✅ **Soporte de temas**: Cambio dinámico entre modo claro y oscuro
✅ **Iconos adaptativos**: Los iconos SVG cambian de color automáticamente según el tema
✅ **Layout de 3 filas**:
   - Fila superior: Título (izquierda) + Icono circular (derecha)
   - Fila central: Descripción
   - Fila inferior: Botón de acción (izquierda) + Etiqueta de formato con indicador (derecha)

## Paleta de Colores

### Modo Oscuro
- **Fondo del contenedor**: `#21262d` (gris oscuro)
- **Borde**: `#30363d` (gris más claro)
- **Texto del título**: `#ffffff` (blanco)
- **Texto de descripción**: `#8b949e` (gris claro)
- **Color del icono**: `#FFFFFF` (BLANCO PURO)

### Modo Claro
- **Fondo del contenedor**: `#ffffff` (blanco)
- **Borde**: `#d0d7de` (gris claro)
- **Texto del título**: `#002E6D` (Azul Navy)
- **Texto de descripción**: `#57606a` (gris oscuro)
- **Color del icono**: `#002E6D` (AZUL NAVY)

## Instalación

El componente está ubicado en:
```
smart_reports_pyqt6/ui/components/report_card_github.py
```

## Uso Básico

### Ejemplo Simple

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from smart_reports_pyqt6.ui.components import ReportCardGitHub

app = QApplication([])

# Crear ventana principal
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# Crear tarjeta de reporte
card = ReportCardGitHub(
    title="Reporte de Ventas Mensual",
    description="Genera un PDF detallado con gráficos de rendimiento.",
    button_text="Generar",
    format_label="Formato: PDF",
    icon_name="report",
    theme="dark"  # o "light"
)

# Conectar señal de clic
card.action_clicked.connect(lambda: print("Botón clickeado!"))

# Agregar al layout
layout.addWidget(card)
window.setCentralWidget(central_widget)
window.show()

app.exec()
```

### Cambiar Tema Dinámicamente

```python
# Cambiar a tema claro
card.set_theme("light")

# Cambiar a tema oscuro
card.set_theme("dark")
```

## Iconos Disponibles

El componente incluye los siguientes iconos SVG:

| Nombre del Icono | Descripción | Uso |
|------------------|-------------|-----|
| `report` | Documento con gráfico de barras | Reportes generales |
| `pdf` | Documento PDF | Exportación a PDF |
| `printer` | Impresora | Impresión directa |
| `analytics` | Gráfico de barras | Análisis y estadísticas |
| `calendar` | Calendario | Reportes por período |

### Ejemplo con Diferentes Iconos

```python
# Reporte de análisis
card_analytics = ReportCardGitHub(
    title="Análisis de Usuario",
    description="Reporte completo del progreso de usuarios.",
    button_text="Configurar",
    format_label="Formato: Excel",
    icon_name="analytics",
    theme="dark"
)

# Reporte por período
card_calendar = ReportCardGitHub(
    title="Reporte por Período",
    description="Genera reportes para rangos de fechas específicos.",
    button_text="Seleccionar Fechas",
    format_label="Formato: PDF",
    icon_name="calendar",
    theme="dark"
)
```

## Métodos Disponibles

### `set_title(title: str)`
Cambia el título de la tarjeta.

```python
card.set_title("Nuevo Título")
```

### `set_description(description: str)`
Cambia la descripción de la tarjeta.

```python
card.set_description("Nueva descripción más detallada.")
```

### `set_button_text(text: str)`
Cambia el texto del botón de acción.

```python
card.set_button_text("Descargar")
```

### `set_format_label(text: str)`
Cambia la etiqueta de formato.

```python
card.set_format_label("Formato: Excel")
```

### `set_icon(icon_name: str)`
Cambia el icono de la tarjeta.

```python
card.set_icon("printer")
```

### `set_theme(theme: str)`
Cambia el tema de la tarjeta ("dark" o "light").

```python
card.set_theme("light")
```

## Señales (Signals)

### `action_clicked`
Se emite cuando se hace clic en el botón de acción.

```python
def on_action():
    print("Acción ejecutada!")

card.action_clicked.connect(on_action)
```

## Demo Completa

Para ver una demostración completa con múltiples tarjetas y cambio de tema, ejecuta:

```bash
python demo_report_cards_github.py
```

Este archivo de demostración incluye:
- 6 tarjetas de reporte diferentes
- Botón para alternar entre tema claro y oscuro
- Grid layout con 3 columnas
- Ejemplos de todos los iconos disponibles

## Integración con el Panel de Reportes

### Reemplazar la ReportCard Existente

Puedes usar `ReportCardGitHub` en lugar de la `ReportCard` actual en `pyqt6_panel_reportes.py`:

```python
from smart_reports_pyqt6.ui.components import ReportCardGitHub

# En lugar de:
# card = ReportCard(title, desc, icon, self.theme_manager)

# Usa:
card = ReportCardGitHub(
    title=title,
    description=desc,
    button_text="Generar Reporte",
    format_label="Formato: PDF",
    icon_name="report",
    theme="dark" if self.theme_manager.is_dark_mode() else "light"
)

# Conectar al theme manager
self.theme_manager.theme_changed.connect(
    lambda new_theme: card.set_theme(new_theme)
)
```

## Personalización Avanzada

### Crear Iconos Personalizados

Puedes extender la clase `IconWidget` para agregar tus propios iconos SVG:

```python
from smart_reports_pyqt6.ui.components.report_card_github import IconWidget

class CustomIconWidget(IconWidget):
    def _get_svg_content(self) -> str:
        if self.icon_name == "custom_icon":
            return f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <!-- Tu SVG aquí -->
            </svg>
            '''
        return super()._get_svg_content()
```

### Personalizar Colores

Puedes modificar los colores en el método `set_theme()` de la clase `ReportCardGitHub` para adaptarlos a tu paleta corporativa.

## Requisitos

- Python 3.8+
- PyQt6
- PyQt6-SVG (para el soporte de iconos SVG)

## Instalación de Dependencias

```bash
pip install PyQt6 PyQt6-SVG
```

## Estructura de Archivos

```
smart_reports_pyqt6/
└── ui/
    └── components/
        ├── __init__.py
        └── report_card_github.py

demo_report_cards_github.py
REPORT_CARD_GITHUB_README.md
```

## Notas Técnicas

1. **Iconos SVG**: Los iconos son renderizados dinámicamente usando `QSvgRenderer`, lo que permite cambiar su color en tiempo real.

2. **Responsive**: El widget se adapta automáticamente al ancho disponible con un mínimo de 320px y máximo de 400px.

3. **Hover Effects**: Las tarjetas incluyen efectos hover que cambian el borde al pasar el cursor.

4. **Señales Qt**: Utiliza el sistema de señales de Qt para comunicación entre componentes.

## Ejemplos de Casos de Uso

### 1. Panel de Reportes con Grid

```python
grid_layout = QGridLayout()
row, col = 0, 0

for report_config in reports_list:
    card = ReportCardGitHub(**report_config)
    grid_layout.addWidget(card, row, col)
    col += 1
    if col > 2:  # 3 columnas
        col = 0
        row += 1
```

### 2. Actualización Dinámica de Contenido

```python
# Cambiar contenido basado en la selección del usuario
def update_card_content(report_type):
    if report_type == "ventas":
        card.set_title("Reporte de Ventas")
        card.set_description("Análisis completo de ventas del período")
        card.set_icon("analytics")
    elif report_type == "usuarios":
        card.set_title("Reporte de Usuarios")
        card.set_description("Progreso individual de usuarios")
        card.set_icon("report")
```

### 3. Sincronización con Theme Manager

```python
class MyPanel(QWidget):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager

        # Crear tarjeta
        current_theme = "dark" if theme_manager.is_dark_mode() else "light"
        self.card = ReportCardGitHub(theme=current_theme)

        # Sincronizar cambios de tema
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _on_theme_changed(self, new_theme):
        self.card.set_theme(new_theme)
```

## Soporte

Para problemas, sugerencias o mejoras, consulta el repositorio del proyecto.

## Licencia

Este componente es parte del proyecto Smart Reports.
