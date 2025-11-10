# 🚀 Smart Reports - Instituto Hutchison Ports

Sistema de reportes y dashboards para capacitación con **arquitectura DDD + Hexagonal escalable** y **20 dashboards D3.js interactivos**.

---

## ⚡ Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

**Credenciales por defecto:**
- `admin` / `1234` (Administrador)
- `demo` / `demo` (Demo)

---

## 📂 Arquitectura DDD + Hexagonal

```
smart-reports1/
├── main.py                                    # 🚀 Punto de entrada único
├── config/                                    # ⚙️ Configuración centralizada
│   ├── settings.py                            # Configuración general
│   ├── database.py                            # Conexión MySQL
│   └── themes.py                              # Temas UI
├── src/                                       # 📦 Código fuente
│   ├── domain/                                # 🧠 Lógica de negocio pura
│   │   ├── entities/                          # Entidades de dominio
│   │   ├── value_objects/                     # Objetos de valor
│   │   └── repositories/                      # Interfaces de repositorios
│   ├── application/                           # 💼 Casos de uso
│   │   └── services/                          # Servicios de aplicación
│   │       └── metricas_gerenciales_service.py  # ✨ NEW: Servicio de métricas
│   ├── infrastructure/                        # 🔧 Implementaciones técnicas
│   │   ├── persistence/                       # Persistencia de datos
│   │   │   ├── mysql/                         # Implementación MySQL
│   │   │   └── excel/                         # Importación Excel
│   │   └── visualization/                     # Generadores D3.js
│   └── interfaces/ui/                         # 🎨 Interfaz Desktop
│       └── views/                             # Vistas y componentes
│           ├── windows/                       # Ventanas principales
│           ├── panels/                        # Paneles de contenido
│           │   └── dashboard/                 # ✨ 20 Dashboards D3.js
│           └── components/                    # Componentes reutilizables
├── tests/                                     # 🧪 Tests
└── data/                                      # 📊 Excel para importar
```

**Principios aplicados:**
- **Domain-Driven Design (DDD)**: Lógica de negocio separada de infraestructura
- **Hexagonal Architecture**: Puertos y adaptadores para flexibilidad
- **SOLID**: Código mantenible y escalable
- **Separation of Concerns**: Cada capa con responsabilidad única

---

## 🎨 Dashboards Gerenciales (20 Gráficos D3.js)

### 📊 Rendimiento (4 gráficos)
- Rendimiento por Unidad de Negocio
- Top 10 Departamentos
- Progreso Mensual Acumulado
- Comparativa Trimestral

### 📈 Comparativas (4 gráficos)
- Tendencia de Cumplimiento por Unidad
- Distribución de Estatus en el Tiempo
- Progreso vs Meta Mensual
- Evolución Suavizada de Métricas

### 🍩 Distribución (4 gráficos)
- Distribución de Estatus Global
- Usuarios por Categoría de Módulo
- Distribución por Nivel Jerárquico
- Progreso Detallado por Área

### 📉 Tendencias (4 gráficos)
- Serie Temporal - Últimos 12 Meses
- Tendencia con Proyección a 3 Meses
- Variación % Mensual
- Análisis de Cambios Acumulados

### 🔵 Relaciones (4 gráficos)
- Relación Tiempo vs Calificación
- Comparativa Año Actual vs Anterior
- Matriz de Rendimiento por Área
- Análisis Multi-Variable (Burbujas)

**Características técnicas:**
- ✅ Datos reales desde MySQL (`instituto_*` tables)
- ✅ HTTP server local (puerto 8050) para ejecución JavaScript
- ✅ Lazy loading optimizado
- ✅ Fallback a datos mock si no hay conexión
- ✅ Colores navy blue (#002E6D → #99E1FA)
- ✅ 100% interactivo en desktop app

---

## 🎯 Pestañas del Sistema

- **📊 Dashboards Gerenciales**: 20 gráficos D3.js con datos en tiempo real
- **👥 Consulta Usuarios**: Búsqueda y filtros avanzados
- **🔄 Cruce de Datos**: Sincronización Cornerstone (Fase 2)
- **📄 Reportes**: PDF profesionales (usuario, unidad, global, período)
- **⚙️ Configuración**: Gestión de usuarios y ajustes

---

## 📥 Importar Excel (Fase 1)

```bash
# 1. Coloca 3 archivos Excel en data/:
#    - usuarios.xlsx
#    - asignaciones.xlsx
#    - completados.xlsx

# 2. Configura MySQL en config/database.py o .env:
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=tu_password
export DB_NAME=tngcore

# 3. Ejecuta el importador:
python database/importar_excel_simple.py
```

**Tablas MySQL:**
- `instituto_usuarios`
- `instituto_asignaciones`
- `instituto_completados`

---

## 🔧 Configuración

### Base de Datos
Edita `config/database.py`:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'tu_password',
    'database': 'tngcore',
}
```

### D3.js Server
Edita `config/settings.py`:
```python
D3_CONFIG = {
    "http_server_port": 8050,  # Puerto HTTP local
    "cache_enabled": True,
    "temp_dir": "smartreports_d3_charts"
}
```

---

## ✅ Características Implementadas

### Core
- ✅ Arquitectura DDD + Hexagonal completa
- ✅ 20 dashboards D3.js interactivos con datos reales
- ✅ Servicio de métricas gerenciales con queries SQL optimizadas
- ✅ Sistema de temas claro/oscuro
- ✅ Navegación moderna con transiciones fluidas

### Visualización
- ✅ D3.js embebido en CustomTkinter via tkinterweb
- ✅ HTTP server local para JavaScript execution
- ✅ Gráficos de barras, líneas, donut/pie, áreas
- ✅ Colores navy blue corporativos
- ✅ Lazy loading y optimización de performance

### Reportes
- ✅ Previsualizaciones HTML estilo Word
- ✅ Exportación PDF profesional
- ✅ Reportes por usuario, unidad, período, global
- ✅ Análisis de niveles de mando

### Integración
- ✅ MySQL (tngcore database)
- ✅ Excel import/export
- ✅ Cornerstone API ready (Fase 2)

---

## 🚀 Roadmap

### Fase 1 (Actual) ✅
- [x] Importación desde 3 Excel
- [x] 20 Dashboards D3.js interactivos
- [x] Arquitectura DDD + Hexagonal
- [x] Servicio de métricas gerenciales
- [x] Queries SQL optimizadas

### Fase 2 (Próxima)
- [ ] Integración API Cornerstone en tiempo real
- [ ] Sincronización automática
- [ ] Notificaciones push
- [ ] Dashboard en tiempo real

---

## 📚 Documentación Técnica

Ver `PROPUESTA_ARQUITECTURA.md` para análisis completo de la arquitectura DDD + Hexagonal implementada.

---

## 🐛 Troubleshooting

### D3.js no se muestra
1. Verifica que tkinterweb esté instalado: `pip install tkinterweb`
2. Verifica que el puerto 8050 esté disponible
3. Revisa logs en consola para errores 404

### Error de conexión MySQL
1. Verifica credenciales en `config/database.py`
2. Asegúrate de que MySQL esté corriendo
3. Verifica que la base de datos `tngcore` exista

### Dashboards vacíos
- Si no hay datos en BD, se usan datos mock automáticamente
- Verifica que las tablas `instituto_*` tengan datos

---

**v2.0.0** - Instituto Hutchison Ports © 2025
