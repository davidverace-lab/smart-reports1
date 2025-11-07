# 🔄 PLAN DE REFACTORIZACIÓN COMPLETO
# Smart Reports - Cambio a snake_case y español

## 📋 OBJETIVOS
1. ✅ Cambiar TODO el código a snake_case
2. ✅ Renombrar archivos a español
3. ✅ Identación consistente de 4 espacios
4. ✅ Comentarios descriptivos en español
5. ✅ Mantener 100% de funcionalidad
6. ✅ Mantener 100% de diseño

## 📁 PLAN DE RENOMBRADO DE ARCHIVOS

### Módulo: config/
- settings.py → configuracion.py
- theme_manager.py → gestor_temas.py

### Módulo: database/
- connection.py → conexion.py
- queries.py → consultas.py
- table_detector.py → detector_tablas.py

### Módulo: services/
- data_processor.py → procesador_datos.py
- data_sync.py → sincronizador_datos.py
- chart_generator.py → generador_graficos.py
- chart_exporter.py → exportador_graficos.py
- pdf_generator.py → generador_pdf.py

### Módulo: ui/components/ → ui/componentes/
- modern_sidebar.py → barra_lateral.py
- top_bar.py → barra_superior.py
- metric_card.py → tarjeta_metrica.py
- chart_card.py → tarjeta_grafico.py
- config_card.py → tarjeta_configuracion.py
- custom_tab_button.py → boton_pestana.py
- unit_selector.py → selector_unidad.py
- matplotlib_chart_card.py → tarjeta_grafico_matplotlib.py
- plotly_chart_card.py → tarjeta_grafico_plotly.py
- plotly_interactive_chart.py → grafico_interactivo_plotly.py

### Módulo: ui/dialogs/ → ui/dialogos/
- user_management_dialog.py → dialogo_gestion_usuarios.py

### Módulo: ui/panels/ → ui/paneles/
- modern_dashboard.py → panel_dashboard.py
- modern_dashboard_backup.py → panel_dashboard_backup.py
- configuracion_panel.py → panel_configuracion.py
- global_report_panel.py → panel_reporte_global.py
- period_report_panel.py → panel_reporte_periodo.py
- user_report_panel.py → panel_reporte_usuario.py
- unit_report_panel.py → panel_reporte_unidad.py
- management_levels_panel.py → panel_niveles_mando.py
- chart_examples_panel.py → panel_ejemplos_graficos.py
- interactive_charts_panel.py → panel_graficos_interactivos.py
- matplotlib_interactive_panel.py → panel_matplotlib_interactivo.py

### Módulo: ui/ (raíz)
- login_window.py → ventana_login.py
- main_window_modern.py → ventana_principal.py

### Archivos raíz
- main.py → main.py (mantener)
- run_app.py → ejecutar_app.py

## 🔧 CAMBIOS DE CÓDIGO

### Convenciones snake_case:

**Clases:**
- DatabaseConnection → ConexionBaseDatos
- ThemeManager → GestorTemas
- ModernSidebar → BarraLateral

**Funciones:**
- getUserData() → obtener_datos_usuario()
- connectToDatabase() → conectar_base_datos()
- generateReport() → generar_reporte()

**Variables:**
- currentUser → usuario_actual
- moduleList → lista_modulos
- isDarkMode → es_modo_oscuro

**Constantes:**
- APP_CONFIG → APP_CONFIG (mantener)
- HUTCHISON_COLORS → HUTCHISON_COLORS (mantener)

## 📝 ORDEN DE EJECUCIÓN

### Fase 1: Módulos Base (sin dependencias UI)
1. config/configuracion.py
2. config/gestor_temas.py
3. database/conexion.py
4. database/consultas.py
5. database/detector_tablas.py
6. services/procesador_datos.py
7. services/sincronizador_datos.py
8. services/generador_graficos.py
9. services/exportador_graficos.py
10. services/generador_pdf.py

### Fase 2: Componentes UI
11. ui/componentes/* (todos)

### Fase 3: Diálogos y Paneles
12. ui/dialogos/*
13. ui/paneles/*

### Fase 4: Ventanas Principales
14. ui/ventana_login.py
15. ui/ventana_principal.py

### Fase 5: Archivos Raíz
16. main.py
17. ejecutar_app.py

## ⚠️ CONSIDERACIONES IMPORTANTES

1. **Imports:** Actualizar TODOS los imports en cada archivo
2. **Referencias:** Buscar y reemplazar nombres de clases/funciones
3. **Strings:** NO cambiar strings de UI (textos visibles)
4. **Comentarios:** Agregar comentarios descriptivos en español
5. **Identación:** 4 espacios consistentes
6. **Testing:** Verificar después de cada fase

## 🎯 MÉTRICAS DE ÉXITO

- ✅ 0 errores de import
- ✅ 0 errores de sintaxis
- ✅ 100% funcionalidad mantenida
- ✅ 100% diseño mantenido
- ✅ Código más legible y mantenible

## 📊 ESTADÍSTICAS

- Total archivos a refactorizar: 35
- Total carpetas a renombrar: 3
- Tiempo estimado: 2-3 horas
- Complejidad: ALTA

---

**NOTA:** Este es un cambio masivo. Se recomienda hacer commit frecuentes por fase.
