# D3.js vs NVD3.js - Guía de Uso

## 📊 Resumen Ejecutivo

Smart Reports ahora soporta **dos motores de renderizado** para gráficos interactivos:

| Motor | Descripción | Cuándo Usar |
|-------|-------------|-------------|
| **NVD3.js** ⭐ | Componentes reutilizables sobre D3.js | **Default** - Gráficos estándar, desarrollo rápido |
| **D3.js** | Librería D3 pura v7 | Personalización avanzada, efectos especiales |

---

## 🚀 Uso Rápido

### Opción 1: NVD3.js (Recomendado - Default)

```python
from smart_reports.ui.components.charts.modal_d3_fullscreen import show_d3_chart

# Por defecto usa NVD3.js
show_d3_chart(
    parent=root,
    title="Ventas por Producto",
    chart_type="bar",
    chart_data={'labels': ['A', 'B', 'C'], 'values': [120, 250, 180]},
    engine='nvd3'  # ← Opcional, es el default
)
```

### Opción 2: D3.js Puro

```python
show_d3_chart(
    parent=root,
    title="Ventas por Producto",
    chart_type="bar",
    chart_data={'labels': ['A', 'B', 'C'], 'values': [120, 250, 180]},
    engine='d3'  # ← Usar D3.js puro
)
```

---

## 📋 Comparación Detallada

### 🔵 NVD3.js

**✅ Ventajas:**
- **Menos código**: Componentes pre-construidos
- **Desarrollo rápido**: API simple y directa
- **Consistencia**: Estilos unificados
- **Tooltips avanzados**: Interactividad mejorada out-of-the-box
- **Ideal para**: Dashboards empresariales, reportes estándar

**❌ Limitaciones:**
- Usa D3.js v3.5.17 (versión estable pero antigua)
- Menos personalización que D3 puro
- Dependencia adicional (NVD3.js CDN)

**Tipos de gráficos soportados:**
- `bar` - Gráfico de barras discreto
- `donut` - Gráfico de dona (pie chart con hueco)
- `line` - Gráfico de líneas con guía interactiva
- `area` - Gráfico de área apilada (stack/stream/expand)

**Código generado:**
```javascript
nv.addGraph(function() {
    var chart = nv.models.discreteBarChart()
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; })
        .showValues(true)
        .color(['#002E6D', '#003D82', ...]);

    d3.select('#chart')
        .datum(chartData)
        .call(chart);

    return chart;
});
```

---

### 🟣 D3.js Puro

**✅ Ventajas:**
- **Máxima flexibilidad**: Control total sobre cada elemento
- **D3.js v7**: Versión más moderna y optimizada
- **Personalización**: Animaciones, transiciones, efectos custom
- **Sin dependencias extra**: Solo D3.js core
- **Ideal para**: Visualizaciones únicas, dashboards creativos

**❌ Limitaciones:**
- Más código requerido
- Mayor complejidad
- Desarrollo más lento

**Tipos de gráficos soportados:**
- `bar` - Gráfico de barras con ordenamiento interactivo
- `donut` - Gráfico de dona con animaciones SVG
- `line` - Gráfico de líneas multi-serie
- `area` - Gráfico de área con zoom/pan

**Código generado:**
```javascript
const svg = d3.select("#chart-container").append("svg")...
const x = d3.scaleBand().range([0, width])...
const y = d3.scaleLinear().range([height, 0])...

svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d.label))
    .attr("y", d => y(d.value))
    .transition().duration(1000)...
```

---

## 🎯 ¿Cuál Usar?

### Usa **NVD3.js** si:
- ✅ Necesitas gráficos estándar rápidamente
- ✅ Quieres componentes consistentes y probados
- ✅ Priorizas velocidad de desarrollo
- ✅ Trabajas en dashboards empresariales
- ✅ No necesitas personalización extrema

### Usa **D3.js** si:
- ✅ Necesitas animaciones personalizadas
- ✅ Quieres efectos visuales únicos
- ✅ Requieres D3.js v7 (última versión)
- ✅ Tienes requisitos de visualización muy específicos
- ✅ Priorizas control total sobre flexibilidad

---

## 🔧 Implementación Técnica

### Arquitectura

```
smart_reports/
├── utils/visualization/
│   ├── d3_generator.py          # Motor D3.js puro (v7)
│   └── nvd3_generator.py        # Motor NVD3.js (sobre D3 v3)
└── ui/components/charts/
    └── modal_d3_fullscreen.py   # Modal dual (soporta ambos)
```

### Clases Generadoras

**MotorTemplatesD3** (`d3_generator.py`):
```python
class MotorTemplatesD3:
    @staticmethod
    def generar_grafico_barras(titulo, datos, subtitulo, tema, interactivo)

    @staticmethod
    def generar_grafico_donut(titulo, datos, subtitulo, tema)

    @staticmethod
    def generar_grafico_lineas(titulo, datos, subtitulo, tema)

    @staticmethod
    def generar_grafico_area(titulo, datos, subtitulo, tema)
```

**MotorTemplatesNVD3** (`nvd3_generator.py`):
```python
class MotorTemplatesNVD3:
    @staticmethod
    def generar_grafico_barras(titulo, datos, subtitulo, tema)

    @staticmethod
    def generar_grafico_donut(titulo, datos, subtitulo, tema)

    @staticmethod
    def generar_grafico_lineas(titulo, datos, subtitulo, tema)

    @staticmethod
    def generar_grafico_area(titulo, datos, subtitulo, tema)
```

### Modal Dual

El `ModalD3Fullscreen` selecciona el motor automáticamente:

```python
def _generate_d3_html(self) -> str:
    # Seleccionar motor según parámetro 'engine'
    Motor = MotorTemplatesNVD3 if self.engine == 'nvd3' else MotorTemplatesD3

    html = Motor.generar_grafico_barras(
        titulo=self.title_text,
        datos=self.chart_data,
        tema=chart_theme
    )
    return html
```

---

## 📦 Dependencias

### NVD3.js (CDN)
```html
<!-- D3.js v3.5.17 (requerido por NVD3) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>

<!-- NVD3.js v1.8.6 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css">
```

### D3.js Puro (CDN)
```html
<!-- D3.js v7 -->
<script src="https://d3js.org/d3.v7.min.js"></script>
```

---

## 🧪 Testing

### Test NVD3.js
```bash
python test_nvd3_generator.py
```

### Test D3.js
```bash
python test_html_generation.py
```

### Test Modal Completo
```bash
python test_d3_modal.py
```

---

## 📝 Ejemplos Completos

### Gráfico de Barras NVD3

```python
from smart_reports.utils.visualization.nvd3_generator import MotorTemplatesNVD3

html = MotorTemplatesNVD3.generar_grafico_barras(
    titulo="Ventas Mensuales",
    datos={
        'labels': ['Ene', 'Feb', 'Mar', 'Abr'],
        'values': [120, 180, 150, 220]
    },
    subtitulo="Primer Trimestre 2025",
    tema='dark'
)
```

### Gráfico de Dona D3

```python
from smart_reports.utils.visualization.d3_generator import MotorTemplatesD3

html = MotorTemplatesD3.generar_grafico_donut(
    titulo="Distribución de Ventas",
    datos={
        'labels': ['Producto A', 'Producto B', 'Producto C'],
        'values': [45, 35, 20]
    },
    subtitulo="Por categoría",
    tema='light'
)
```

---

## 🎨 Personalización

### Paleta de Colores Hutchison

Ambos motores usan la misma paleta corporativa:

```python
PALETA_COLORES = [
    '#002E6D',  # Navy (Hutchison Ports)
    '#003D82',  # Navy blue
    '#004C97',  # Royal blue oscuro
    '#0066CC',  # Royal blue
    '#0080FF',  # Azure blue
    '#009BDE',  # Sky blue (Hutchison Ports)
    '#00B5E2',  # Horizon blue (Hutchison Ports)
    '#33C7F0',  # Light blue
    '#66D4F5',  # Lighter blue
    '#99E1FA',  # Very light blue
]
```

---

## 🔍 Diferencias de Rendimiento

| Aspecto | NVD3.js | D3.js |
|---------|---------|-------|
| **Tamaño HTML** | ~5-6 KB | ~11-12 KB |
| **Velocidad de carga** | ⚡ Más rápido | 🐢 Más lento |
| **Tiempo desarrollo** | ⚡⚡⚡ Muy rápido | 🐢🐢 Lento |
| **Personalización** | ⭐⭐ Limitada | ⭐⭐⭐⭐⭐ Total |
| **Compatibilidad** | D3 v3 | D3 v7 |

---

## 🚦 Recomendación Final

**Default: NVD3.js** ⭐
- Para el 90% de los casos de uso
- Componentes robustos y probados
- Desarrollo ágil

**Especial: D3.js**
- Para casos que requieren personalización avanzada
- Visualizaciones únicas
- Efectos especiales

---

## 📚 Referencias

- **D3.js Oficial**: https://d3js.org/
- **NVD3.js Oficial**: http://nvd3.org/
- **D3.js v7 Docs**: https://github.com/d3/d3/blob/main/CHANGES.md
- **NVD3 Examples**: http://nvd3.org/examples/index.html

---

**Última actualización**: 2025-11-21
**Versión**: 1.0
**Motor default**: NVD3.js
