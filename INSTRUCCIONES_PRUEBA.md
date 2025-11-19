# 🔧 Instrucciones para Probar la Aplicación

## ⚠️ IMPORTANTE - Antes de Ejecutar

La aplicación **requiere** las siguientes dependencias instaladas:

```bash
pip install -r requirements.txt
```

Si no las tienes instaladas, la aplicación NO funcionará.

---

## 🧪 Paso 1: Ejecutar Script de Diagnóstico

Antes de ejecutar la aplicación principal, ejecuta el script de diagnóstico:

```bash
python test_menus.py
```

### ✅ Resultado Esperado:

```
================================================================================
PRUEBA DE MENÚS - SMART REPORTS
================================================================================

[1] Verificando dependencias...
  ✓ customtkinter instalado
  ✓ matplotlib instalado

[2] Verificando imports de configuración...
  ✓ Themes OK (31 colores)
    - aqua_green: ✓
    - danger: ✓
  ✓ Gestor de temas OK (modo: dark)

[3] Verificando componentes UI...
  ✓ CustomTabView
  ✓ ModernSidebar

[4] Verificando imports de menús...
  ✓ Dashboard
  ✓ Consultas
  ✓ Importación
  ✓ Reportes
  ✓ Configuración

[5] Creando ventana de prueba...
  ✓ Ventana creada

  Probando crear Dashboard...
    ✓ Dashboard se crea correctamente

================================================================================
RESUMEN
================================================================================
Menús funcionando: 5/5
  ✓ Dashboard
  ✓ Consultas
  ✓ Importación
  ✓ Reportes
  ✓ Configuración

================================================================================
✅ TODOS LOS MENÚS ESTÁN OK - La aplicación debería funcionar
================================================================================
```

### ❌ Si Ves Errores:

1. **"customtkinter NO instalado"** → Ejecuta: `pip install customtkinter`
2. **"matplotlib NO instalado"** → Ejecuta: `pip install matplotlib`
3. **Errores de import** → Copia el error completo y repórtalo

---

## 🚀 Paso 2: Ejecutar la Aplicación

```bash
python main.py
```

### 📊 Logging en Consola

La aplicación ahora muestra mensajes detallados en consola:

```
🚀 Iniciando SMART REPORTS - INSTITUTO HUTCHISON PORTS
✓ Usuario autenticado: admin - Rol: Administrador
Navegando a: dashboard
📊 Cargando Dashboard...
🚀 Inicializando Panel de Dashboards Gerenciales...
✅ Panel de Dashboards Gerenciales inicializado correctamente
✅ Dashboard cargado exitosamente
```

---

## 🎨 Funcionalidades Verificadas

### ✅ Sin Conexión a Base de Datos

La aplicación funciona **completamente** sin base de datos:

1. **Dashboard** - Muestra gráficas con datos estáticos de ejemplo
2. **Consultas** - Interfaz completa, muestra mensaje al buscar
3. **Importación** - Interfaz completa visible
4. **Reportes** - Todas las opciones de reportes visibles
5. **Configuración** - Interfaz completa accesible

### ✅ Modo Claro y Oscuro

- **Modo Oscuro**: Fondo `#1a1a1a`, texto blanco
- **Modo Claro**: Fondo `#f5f5f5`, texto negro
- Cambio entre modos usando el switch en la barra lateral

---

## 🐛 Reportar Problemas

### Si un menú NO se muestra:

1. **Revisa la consola** - Verás el error exacto
2. **Copia el traceback completo** - Desde donde dice "Traceback" hasta el final
3. **Incluye qué menú intentabas abrir**

### Ejemplo de reporte de error:

```
Menú: Dashboard
Error en consola:
❌ Error cargando dashboard: No module named 'matplotlib'
Traceback (most recent call last):
  File "ventana_principal_view.py", line 202, in show_dashboard
    panel = show_dashboard_menu(...)
  File "menu_dashboard.py", line 6, in <module>
    import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'
```

---

## 📋 Checklist de Pruebas

Verifica que puedas:

- [ ] Abrir la aplicación sin errores
- [ ] Hacer login (cualquier usuario/contraseña en modo demo)
- [ ] Ver la barra lateral con todos los menús
- [ ] Hacer clic en "Dashboard" y ver gráficas
- [ ] Hacer clic en "Consultas" y ver el panel de búsquedas
- [ ] Hacer clic en "Importación de Datos" y ver el panel
- [ ] Hacer clic en "Reportes" y ver las opciones
- [ ] Hacer clic en "Configuración" y ver las opciones
- [ ] Cambiar entre modo claro y oscuro con el switch
- [ ] Ver que los cambios de tema se aplican correctamente

---

## 🎯 Resultado Esperado

**TODOS los menús deben mostrarse** con su interfaz completa, aunque no haya base de datos conectada.

Si algún menú muestra una pantalla en blanco, revisa la consola para ver el error específico.
