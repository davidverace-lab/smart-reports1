# 📊 Gráficos D3.js Interactivos - Guía de Uso

## ✨ Características

Los dashboards ahora incluyen gráficos D3.js interactivos que se abren en un modal fullscreen cuando haces clic en el botón **"⛶ Ver Grande"**.

### Tipos de Gráficos Disponibles:

1. **📊 Gráfico de Barras** - Con ordenamiento ascendente/descendente
2. **🍩 Gráfico de Dona** - Con porcentajes y hover interactivo
3. **📈 Gráfico de Líneas** - Con tooltips y animaciones suaves
4. **📉 Gráfico de Área** - Con zoom y pan interactivo

### Interactividad:

- **Hover**: Pasa el mouse sobre los elementos para ver tooltips con valores detallados
- **Ordenamiento**: En gráficos de barras, usa los botones para ordenar ascendente/descendente
- **Zoom**: En gráficos de área, activa el zoom con el botón y usa la rueda del mouse
- **Pan**: Arrastra el gráfico para moverte por los datos
- **Animaciones**: Transiciones suaves al cargar y actualizar los gráficos

---

## 🚀 Cómo Usar

### 1. Acceder a los Dashboards

Navega a cualquiera de los siguientes dashboards:

- **📊 Dashboards Gerenciales** - Panel principal con 6 gráficos
- **📈 Panel de Control Ejecutivo** - Dashboard ejecutivo con métricas clave
- **👥 Dashboard RRHH** - Visualizaciones de recursos humanos

### 2. Expandir un Gráfico

1. Encuentra el gráfico que deseas ver en detalle
2. Haz clic en el botón **"⛶ Ver Grande"** en la esquina superior derecha
3. Se abrirá un modal fullscreen con el gráfico D3.js interactivo

### 3. Interactuar con el Gráfico

- **Gráficos de Barras**:
  - Haz hover sobre las barras para ver valores
  - Usa los botones "📈 Ordenar Ascendente" y "📉 Ordenar Descendente"
  - Presiona "🔄 Restablecer" para volver al orden original

- **Gráficos de Dona**:
  - Haz hover sobre las secciones para ver porcentajes
  - Las secciones se expanden al pasar el mouse

- **Gráficos de Líneas**:
  - Haz hover sobre los puntos para ver valores exactos
  - Observa las animaciones suaves de trazado

- **Gráficos de Área**:
  - Haz clic en "🔍 Activar Zoom" para habilitar zoom/pan
  - Usa la rueda del mouse para hacer zoom
  - Arrastra para mover el gráfico

### 4. Cerrar el Modal

- Haz clic en el botón **"✕"** en la esquina superior izquierda
- O presiona la tecla **ESC**

---

## 🔧 Requisitos Técnicos

### Dependencias Requeridas:

```bash
# Instalar tkinterweb (para embeber HTML/D3.js)
pip install tkinterweb>=3.23.0

# O instalar todas las dependencias del proyecto
pip install -r requirements.txt
```

### Requisitos del Sistema:

- **Python**: 3.8 o superior
- **Conexión a Internet**: Requerida para cargar D3.js desde CDN
- **Sistema Operativo**: Windows, Linux o macOS

---

## 🧪 Probar la Funcionalidad

### Script de Prueba Rápida:

```bash
# Ejecutar el script de prueba
python test_d3_modal.py
```

Este script verificará:
1. ✅ Que tkinterweb esté instalado
2. ✅ Que el modal D3.js se importe correctamente
3. ✅ Que el generador D3.js funcione
4. ✅ Que se genere HTML válido
5. ✅ Prueba interactiva con ventana de ejemplo

### Probar en la Aplicación:

1. Inicia la aplicación principal:
   ```bash
   python main.py
   ```

2. Navega a **Dashboards Gerenciales**

3. Haz clic en **"⛶ Ver Grande"** en cualquier gráfico

4. Verifica que se abra el modal D3.js interactivo

---

## 🐛 Troubleshooting

### Problema: "tkinterweb no disponible"

**Solución:**
```bash
pip install tkinterweb>=3.23.0
```

Si el problema persiste:
```bash
pip uninstall tkinterweb
pip install tkinterweb --upgrade
```

### Problema: "Error al cargar gráfico D3.js"

**Posibles causas:**

1. **Sin conexión a internet**
   - D3.js se carga desde CDN (https://d3js.org/d3.v7.min.js)
   - Verifica tu conexión a internet

2. **Datos inválidos**
   - Verifica que los datos tengan el formato correcto:
     ```python
     datos = {
         'labels': ['A', 'B', 'C'],
         'values': [10, 20, 30]
     }
     ```

3. **Error en tkinterweb**
   - Reinstala tkinterweb (ver arriba)

### Problema: "El gráfico no se muestra"

**Solución:**

1. Abre la consola y verifica los logs:
   ```
   🔧 Generando HTML D3.js para tipo: bar
   ✅ HTML generado: XXXX caracteres
   🔧 Creando HtmlFrame...
   🔧 Cargando HTML en HtmlFrame...
   ✅ Gráfico D3.js renderizado exitosamente
   ```

2. Si ves errores, copia el mensaje completo y repórtalo

### Problema: "Fallback a Matplotlib"

**Causa:**
- tkinterweb no está instalado o hay un error al cargar el modal

**Solución:**
- El sistema automáticamente usa una vista expandida con Matplotlib
- Para habilitar D3.js, instala tkinterweb (ver arriba)

---

## 📝 Archivos Modificados

### Dashboards Actualizados:

1. **`panel_dashboards_gerenciales.py`**
   - ✅ Ahora usa modal D3.js al expandir gráficos
   - ✅ Fallback automático a Matplotlib si tkinterweb no disponible

2. **`panel_control_ejecutivo.py`**
   - ✅ Integración completa con modal D3.js
   - ✅ Mapeo correcto de tipos de gráfico

3. **`panel_rrhh.py`**
   - ✅ Soporte completo para gráficos D3.js interactivos

### Componentes Mejorados:

1. **`modal_d3_fullscreen.py`**
   - ✅ Mejor manejo de errores y debug
   - ✅ Mensajes informativos detallados
   - ✅ Validación de HTML generado

2. **`d3_generator.py`**
   - ✅ Generación de HTML D3.js optimizada
   - ✅ Soporte para 4 tipos de gráficos
   - ✅ Paleta de colores Hutchison integrada

---

## 🎨 Personalización

### Cambiar Tema (Dark/Light):

El modal D3.js detecta automáticamente el tema actual y ajusta los colores.

### Cambiar Paleta de Colores:

Edita `smart_reports/utils/visualization/d3_generator.py`:

```python
PALETA_COLORES = [
    '#002E6D',  # Navy (Hutchison Ports)
    '#003D82',  # Navy blue
    # ... más colores
]
```

### Agregar Nuevos Tipos de Gráficos:

1. Agrega el método en `MotorTemplatesD3`:
   ```python
   @staticmethod
   def generar_grafico_nuevo_tipo(titulo, datos, subtitulo, tema):
       # Tu implementación aquí
       return html
   ```

2. Actualiza `_generate_d3_html()` en `modal_d3_fullscreen.py`:
   ```python
   elif self.chart_type == 'nuevo_tipo':
       html = MotorTemplatesD3.generar_grafico_nuevo_tipo(...)
   ```

---

## 📞 Soporte

Si encuentras problemas:

1. Ejecuta el script de prueba: `python test_d3_modal.py`
2. Revisa los logs en la consola
3. Verifica que todas las dependencias estén instaladas
4. Si el problema persiste, reporta el error con los logs completos

---

## ✅ Checklist de Verificación

- [ ] tkinterweb instalado (`pip install tkinterweb>=3.23.0`)
- [ ] Script de prueba ejecutado exitosamente (`python test_d3_modal.py`)
- [ ] Dashboards abren correctamente
- [ ] Botón "⛶ Ver Grande" visible en los gráficos
- [ ] Modal D3.js se abre al hacer clic
- [ ] Gráficos son interactivos (hover, tooltips, etc.)
- [ ] Modal se cierra con "✕" o ESC
- [ ] Sin errores en la consola

---

## 🎉 ¡Listo!

Ahora tienes gráficos D3.js completamente interactivos en tus dashboards. Disfruta de la experiencia de visualización mejorada con:

- ✨ Animaciones suaves
- 🎯 Interactividad completa
- 🎨 Diseño profesional
- ⚡ Rendimiento optimizado

**¡Feliz visualización de datos!** 📊
