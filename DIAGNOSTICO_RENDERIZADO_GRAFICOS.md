# 🔍 Diagnóstico de Renderizado de Gráficos D3.js

## Fecha: 2025-11-30

---

## ✅ Mejoras Implementadas para Diagnóstico

### 1. Logging Detallado Agregado

He agregado logging completo en el componente `D3InteractiveChartCard` para identificar exactamente dónde falla el renderizado.

**Archivo modificado:** `smart_reports/ui/components/charts/d3_interactive_chart_card.py`

#### Logging en `set_chart()` (líneas 247-286):
```python
print(f"\n📊 [D3InteractiveChartCard] set_chart() llamado")
print(f"  🔹 Título: {self._title}")
print(f"  🔹 Tipo: {chart_type}")
print(f"  🔹 Datos: {datos}")
print(f"  🔹 Subtítulo: {subtitulo}")
print(f"  🔹 Tema: {tema}")
print(f"  🔹 HTML generado: {len(self.html_content)} caracteres")
print(f"  🔹 Archivo guardado: {self.chart_filepath}")
print(f"  🔹 URL: {self.chart_url}")
```

#### Logging en `_render_embedded()` (líneas 329-368):
```python
print(f"  🔍 [DEBUG] Intentando renderizar embebido...")
print(f"  🔍 [DEBUG] Chart URL: {self.chart_url}")
print(f"  🔍 [DEBUG] Chart File: {self.chart_filepath}")
print(f"  🔍 [DEBUG] TKINTERWEB_AVAILABLE: {TKINTERWEB_AVAILABLE}")
print(f"  ✅ Archivo HTML existe ({os.path.getsize(self.chart_filepath)} bytes)")
print(f"  ✅ Frame creado")
print(f"  ✅ HtmlFrame creado")
print(f"  ✅ D3.js Interactivo renderizado embebido en: {self.chart_url}")
```

#### Logging de Errores con Traceback:
```python
except Exception as e:
    import traceback
    print(f"  ❌ Error embebiendo: {e}")
    print(f"  ❌ Traceback: {traceback.format_exc()}")
```

---

## 🧪 Cómo Ejecutar el Diagnóstico

### Paso 1: Ejecutar la Aplicación

```bash
cd "C:\Users\david\OneDrive\Documentos\smart-reports1-main (2)\smart-reports1-main"
python main.py
```

### Paso 2: Navegar a los Dashboards

1. Abrir cualquier dashboard (Gerencial, RRHH, Control Ejecutivo)
2. Observar la **consola/terminal** donde ejecutaste `python main.py`

### Paso 3: Analizar la Salida

Busca en la consola los siguientes mensajes:

#### ✅ **Inicio del Servidor HTTP:**
```
✅ Servidor D3.js: http://127.0.0.1:8050
```

**Si NO aparece:** El servidor HTTP no está corriendo. Esto es CRÍTICO.

#### ✅ **Al cargar un gráfico:**
```
📊 [D3InteractiveChartCard] set_chart() llamado
  🔹 Título: [nombre del gráfico]
  🔹 Tipo: bar / donut / line / area
  🔹 Datos: {'labels': [...], 'values': [...]}
  🔹 Tema: dark / light
  🔹 HTML generado: [número] caracteres
  🔹 Archivo guardado: [ruta al archivo HTML]
  🔹 URL: http://127.0.0.1:8050/chart_XXX.html
```

**Si NO aparece:** El método `set_chart()` nunca se está llamando.

#### ✅ **Al renderizar:**
```
  🔍 [DEBUG] Intentando renderizar embebido...
  🔍 [DEBUG] Chart URL: http://127.0.0.1:8050/chart_XXX.html
  🔍 [DEBUG] Chart File: C:\Users\david\AppData\Local\Temp\smartreports_d3\chart_XXX.html
  🔍 [DEBUG] TKINTERWEB_AVAILABLE: True / False
  ✅ Archivo HTML existe (XXXX bytes)
  ✅ Frame creado
  ✅ HtmlFrame creado
  ✅ D3.js Interactivo renderizado embebido en: http://127.0.0.1:8050/chart_XXX.html
```

**Si aparece error:**
```
  ❌ Error embebiendo: [descripción del error]
  ❌ Traceback: [stack trace completo]
```

---

## 🔎 Posibles Problemas y Soluciones

### Problema 1: `tkinterweb` no está disponible

**Síntoma:**
```
⚠️ tkinterweb no disponible (No module named 'tkinterweb') - D3.js se abrirá en navegador
🔍 [DEBUG] TKINTERWEB_AVAILABLE: False
⚠️ tkinterweb no disponible, usando vista de botón
```

**Solución:**
```bash
pip install tkinterweb
```

---

### Problema 2: Servidor HTTP no inicia

**Síntoma:**
```
❌ Error iniciando servidor: [Address already in use]
```

**Solución 1 - Puerto ocupado:**
```bash
# Windows
netstat -ano | findstr :8050
taskkill /PID [PID_DEL_PROCESO] /F
```

**Solución 2 - Cambiar puerto:**
Modificar `d3_interactive_chart_card.py` línea 63:
```python
self.port = 8051  # Cambiar a otro puerto
```

---

### Problema 3: Archivo HTML no se genera

**Síntoma:**
```
  ❌ ERROR: Archivo HTML no existe: [ruta]
```

**Solución:**
1. Verificar permisos de escritura en `C:\Users\david\AppData\Local\Temp\`
2. Verificar que la carpeta `smartreports_d3` se cree correctamente
3. Verificar que el método `_generate_d3_interactive_html()` no lance excepciones

**Verificación manual:**
```bash
# Verificar que la carpeta existe
dir C:\Users\david\AppData\Local\Temp\smartreports_d3

# Ver archivos HTML generados
dir C:\Users\david\AppData\Local\Temp\smartreports_d3\*.html
```

---

### Problema 4: No hay datos

**Síntoma en consola:**
```
🔍 [DEBUG] generar_grafico_barras_interactivo - Título: [título]
🔍 [DEBUG] Labels: []
🔍 [DEBUG] Values: []
⚠️ [WARNING] No hay datos para generar el gráfico de barras
```

**Solución:**
El problema NO es de renderizado, sino que los datos no llegan al componente.

**Verificar:**
1. La consulta SQL en el panel está obteniendo datos
2. El método que llama a `set_chart()` está pasando datos correctos
3. Verificar en `panel_dashboards_gerenciales.py` el método `_create_mini_chart()` (línea 366)

---

### Problema 5: HtmlFrame no renderiza JavaScript

**Síntoma:**
- Se muestra espacio en blanco
- No hay errores en consola
- El archivo HTML existe y es correcto

**Posibles causas:**
1. **tkinterweb versión antigua:** Actualizar a la última versión
   ```bash
   pip install --upgrade tkinterweb
   ```

2. **Problemas con CEF (Chromium Embedded Framework):**
   tkinterweb usa CEF internamente. Verificar que esté correctamente instalado.

3. **JavaScript bloqueado:** Verificar configuración de tkinterweb
   ```python
   # En d3_interactive_chart_card.py, línea 355-360
   html_widget = HtmlFrame(
       html_frame,
       messages_enabled=True,  # Cambiar a True para ver errores JS
       vertical_scrollbar=False,
       horizontal_scrollbar=False
   )
   ```

---

## 🧪 Prueba Manual del HTML

Si los logs muestran que el archivo HTML se genera correctamente, prueba abrirlo manualmente:

### Paso 1: Obtener la ruta del archivo
Busca en la consola:
```
  🔹 Archivo guardado: C:\Users\david\AppData\Local\Temp\smartreports_d3\chart_XXX.html
```

### Paso 2: Abrir en navegador
```bash
# Opción 1: Desde el explorador
start C:\Users\david\AppData\Local\Temp\smartreports_d3\chart_XXX.html

# Opción 2: Copiar URL y pegar en navegador
# http://127.0.0.1:8050/chart_XXX.html
```

### Paso 3: Verificar en navegador

**Si el gráfico SE VE en el navegador:**
- ✅ El HTML está correcto
- ✅ El servidor HTTP funciona
- ❌ El problema es con `tkinterweb` (HtmlFrame)

**Si el gráfico NO SE VE en el navegador:**
- ❌ Problema con el HTML generado
- ❌ Problema con las librerías D3.js/NVD3.js (CDN)
- ❌ Problema con JavaScript

**Abrir consola del navegador (F12):**
```
Ver errores JavaScript en la pestaña "Console"
```

---

## 📝 Checklist de Verificación

Ejecuta estos pasos en orden:

- [ ] **1. Verificar que tkinterweb está instalado:**
  ```bash
  pip show tkinterweb
  ```

- [ ] **2. Verificar que el servidor HTTP inicia:**
  ```
  ✅ Servidor D3.js: http://127.0.0.1:8050
  ```

- [ ] **3. Navegar a dashboards y verificar logs de set_chart():**
  ```
  📊 [D3InteractiveChartCard] set_chart() llamado
  ```

- [ ] **4. Verificar que se generan archivos HTML:**
  ```bash
  dir C:\Users\david\AppData\Local\Temp\smartreports_d3\*.html
  ```

- [ ] **5. Abrir un archivo HTML en navegador manualmente:**
  - ¿Se ve el gráfico? → Problema con tkinterweb
  - ¿NO se ve? → Problema con HTML/JavaScript

- [ ] **6. Verificar logs de _render_embedded():**
  ```
  ✅ D3.js Interactivo renderizado embebido en: http://...
  ```

- [ ] **7. Si hay error, copiar el traceback completo:**
  ```
  ❌ Traceback: [pegar aquí]
  ```

---

## 🎯 Próximos Pasos según Diagnóstico

### Escenario A: tkinterweb no está disponible
```bash
pip install tkinterweb
# Reiniciar la aplicación
python main.py
```

### Escenario B: tkinterweb disponible pero no renderiza
1. Verificar versión de tkinterweb: `pip show tkinterweb`
2. Actualizar si es antigua: `pip install --upgrade tkinterweb`
3. Habilitar mensajes de error: `messages_enabled=True`
4. Revisar logs del navegador integrado

### Escenario C: HTML no se genera correctamente
1. Copiar el traceback del error
2. Verificar permisos en carpeta temporal
3. Verificar método `_generate_d3_interactive_html()`

### Escenario D: No hay datos
1. Verificar que las consultas SQL retornan datos
2. Verificar que `panel_dashboards_gerenciales.py` pasa datos a `set_chart()`
3. Agregar logging en el método que llama a `D3InteractiveChartCard`

---

## 📤 Reporte de Errores

Si después de ejecutar estos diagnósticos sigues teniendo problemas, proporciona:

1. **Salida completa de la consola** (desde que inicia hasta que intenta renderizar)
2. **Versión de tkinterweb:** `pip show tkinterweb`
3. **¿El HTML funciona en navegador?** (Sí/No)
4. **Errores en consola del navegador** (F12 → Console)
5. **Sistema operativo y versión de Python:**
   ```bash
   python --version
   ```

---

## 🔄 Cambios Realizados en Este Diagnóstico

| Archivo | Cambio | Líneas |
|---------|--------|--------|
| `d3_interactive_chart_card.py` | Logging en `set_chart()` | 247-286 |
| `d3_interactive_chart_card.py` | Logging en `_render_embedded()` | 329-377 |
| `d3_interactive_chart_card.py` | Verificación de archivo HTML antes de renderizar | 340-343 |
| `d3_interactive_chart_card.py` | Verificación de TKINTERWEB_AVAILABLE | 334-337 |
| `d3_interactive_chart_card.py` | Traceback completo en caso de error | 370-373 |

---

## 🎉 Resultado Esperado

Después de aplicar estos diagnósticos, deberías poder identificar exactamente cuál es el problema:

1. ✅ **Problema identificado en logs**
2. ✅ **Solución aplicada según escenario**
3. ✅ **Gráficos renderizando correctamente**

---

**EJECUTA LOS PASOS DE DIAGNÓSTICO Y PROPORCIONA LOS LOGS PARA CONTINUAR**
