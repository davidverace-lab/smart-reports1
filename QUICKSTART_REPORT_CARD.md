# 🚀 Guía Rápida: ReportCardGitHub

## ✅ Instalación de Dependencias

Si aún no tienes PyQt6 instalado, ejecuta:

```bash
pip install PyQt6 PyQt6-SVG
```

O si usas el archivo requirements.txt del proyecto:

```bash
pip install -r requirements.txt
```

## 🎨 Ejecutar el Demo

Para ver el componente en acción con múltiples tarjetas y cambio de tema:

```bash
python demo_report_cards_github.py
```

**Características del demo:**
- 6 tarjetas de reporte diferentes con distintos iconos
- Botón para alternar entre tema claro y oscuro en tiempo real
- Grid layout con 3 columnas responsivo
- Demostración de todos los iconos disponibles (report, analytics, calendar, printer, pdf)

## 📋 Uso Rápido

### Ejemplo Mínimo (3 líneas)

```python
from smart_reports_pyqt6.ui.components import ReportCardGitHub

card = ReportCardGitHub(title="Mi Reporte", description="Descripción", theme="dark")
card.action_clicked.connect(lambda: print("Click!"))
```

### Ejemplo con Todas las Opciones

```python
from smart_reports_pyqt6.ui.components import ReportCardGitHub

# Crear tarjeta personalizada
card = ReportCardGitHub(
    title="Reporte de Ventas Mensual",
    description="Genera un PDF detallado con gráficos de rendimiento.",
    button_text="Generar",
    format_label="Formato: PDF",
    icon_name="report",  # Opciones: report, pdf, printer, analytics, calendar
    theme="dark"  # o "light"
)

# Conectar acción del botón
def generar_reporte():
    print("Generando reporte...")
    # Tu lógica aquí

card.action_clicked.connect(generar_reporte)
```

## 🔄 Cambiar Tema Dinámicamente

```python
# Modo oscuro
card.set_theme("dark")

# Modo claro
card.set_theme("light")
```

## 🎯 Iconos Disponibles

```python
# Icono de reporte general (documento con gráfico)
card.set_icon("report")

# Icono de PDF
card.set_icon("pdf")

# Icono de impresora
card.set_icon("printer")

# Icono de análisis (gráfico de barras)
card.set_icon("analytics")

# Icono de calendario
card.set_icon("calendar")
```

## 🔧 Métodos Útiles

```python
# Cambiar título
card.set_title("Nuevo Título")

# Cambiar descripción
card.set_description("Nueva descripción del reporte")

# Cambiar texto del botón
card.set_button_text("Descargar")

# Cambiar etiqueta de formato
card.set_format_label("Formato: Excel")

# Cambiar icono
card.set_icon("analytics")

# Cambiar tema
card.set_theme("light")
```

## 📐 Integración con Grid Layout

```python
from PyQt6.QtWidgets import QGridLayout

grid = QGridLayout()

# Configuraciones de reportes
reports = [
    {"title": "Ventas", "icon": "report"},
    {"title": "Usuarios", "icon": "analytics"},
    {"title": "Período", "icon": "calendar"},
]

# Crear grid de 3 columnas
row, col = 0, 0
for config in reports:
    card = ReportCardGitHub(
        title=config["title"],
        description="Descripción del reporte",
        icon_name=config["icon"],
        theme="dark"
    )
    grid.addWidget(card, row, col)

    col += 1
    if col > 2:  # 3 columnas
        col = 0
        row += 1
```

## 🎭 Alternar Tema con Botón

```python
from PyQt6.QtWidgets import QPushButton

current_theme = "dark"
cards = []  # Lista de tus tarjetas

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    for card in cards:
        card.set_theme(current_theme)

toggle_btn = QPushButton("Cambiar Tema")
toggle_btn.clicked.connect(toggle_theme)
```

## 🎨 Paleta de Colores

### Modo Oscuro (Dark)
- Fondo: `#21262d` (gris oscuro tipo GitHub)
- Borde: `#30363d`
- Título: `#ffffff` (blanco)
- Descripción: `#8b949e` (gris claro)
- **Icono: `#FFFFFF` (BLANCO PURO)**

### Modo Claro (Light)
- Fondo: `#ffffff` (blanco)
- Borde: `#d0d7de`
- Título: `#002E6D` (Azul Navy)
- Descripción: `#57606a` (gris oscuro)
- **Icono: `#002E6D` (AZUL NAVY)**

## 📦 Estructura de Archivos Creados

```
smart_reports_pyqt6/
└── ui/
    └── components/
        ├── __init__.py                    # ✅ Actualizado
        └── report_card_github.py          # ✅ Nuevo componente

demo_report_cards_github.py                # ✅ Demo completo
REPORT_CARD_GITHUB_README.md               # ✅ Documentación completa
QUICKSTART_REPORT_CARD.md                  # ✅ Esta guía
```

## 🔍 Verificación de Instalación

Para verificar que todo está instalado correctamente:

```bash
python -c "from smart_reports_pyqt6.ui.components import ReportCardGitHub; print('✅ Componente instalado correctamente')"
```

## 💡 Tips y Mejores Prácticas

1. **Siempre especifica el tema inicial** al crear la tarjeta
2. **Conecta la señal `action_clicked`** para manejar los clicks del botón
3. **Usa iconos descriptivos** que representen el tipo de reporte
4. **Mantén las descripciones cortas** (1-2 líneas máximo)
5. **Sincroniza con tu theme manager** si tu app ya tiene uno

## 🐛 Solución de Problemas

### Error: "No module named 'PyQt6'"
```bash
pip install PyQt6 PyQt6-SVG
```

### Los iconos no se muestran
Verifica que tienes instalado `PyQt6-SVG`:
```bash
pip install PyQt6-SVG
```

### El tema no cambia
Asegúrate de llamar a `card.set_theme("dark")` o `card.set_theme("light")` después de crear la tarjeta.

## 📞 Soporte

Para documentación completa, consulta `REPORT_CARD_GITHUB_README.md`

## ✨ Siguiente Paso

¡Ejecuta el demo para ver el componente en acción!

```bash
python demo_report_cards_github.py
```

---

**Creado con ❤️ para Smart Reports**
