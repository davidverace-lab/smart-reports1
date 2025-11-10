# 🏗️ PROPUESTA: Arquitectura Escalable para Smart Reports

## 📋 Análisis Actual vs. Propuesto

### **Estructura Actual (Monolítica simple)**
```
smart-reports1/
├── ejecutar_app.py          # Punto de entrada
├── interfaz/                # UI mezclada
├── nucleo/                  # Lógica mezclada
└── database/                # Persistencia
```

**Problemas**:
- ❌ Acoplamiento fuerte entre capas
- ❌ Lógica de negocio mezclada con infraestructura
- ❌ Difícil de testear (no hay interfaces)
- ❌ No escalable a microservicios

---

## 🎯 Estructura Propuesta (DDD + Hexagonal)

### **Reorganización Completa**
```
smart-reports1/
├── main.py                           # 🚀 Punto de entrada único
├── config/                           # ⚙️ Configuración centralizada
│   ├── __init__.py
│   ├── settings.py                   # Variables de entorno, configuración
│   ├── database.py                   # Config BD
│   └── themes.py                     # Config temas UI
│
├── src/                              # 📦 Código fuente principal
│   │
│   ├── domain/                       # 🧠 CAPA DE DOMINIO (Lógica de negocio pura)
│   │   ├── entities/                 # Entidades del negocio
│   │   │   ├── usuario.py            # Usuario (con sus reglas de negocio)
│   │   │   ├── modulo.py             # Módulo de capacitación
│   │   │   ├── progreso.py           # Progreso del usuario
│   │   │   └── reporte.py            # Reporte
│   │   │
│   │   ├── value_objects/            # Objetos de valor inmutables
│   │   │   ├── email.py              # Email validado
│   │   │   ├── calificacion.py       # Calificación (0-100)
│   │   │   └── fecha_progreso.py     # Fecha con validaciones
│   │   │
│   │   ├── repositories/             # 🔌 Interfaces de repositorios (SOLO INTERFACES)
│   │   │   ├── usuario_repository.py
│   │   │   ├── modulo_repository.py
│   │   │   └── progreso_repository.py
│   │   │
│   │   └── services/                 # Servicios de dominio (lógica compleja)
│   │       └── calculador_metricas.py
│   │
│   ├── application/                  # 💼 CAPA DE APLICACIÓN (Casos de uso)
│   │   ├── use_cases/                # Casos de uso (orquestación)
│   │   │   ├── usuarios/
│   │   │   │   ├── crear_usuario.py
│   │   │   │   ├── actualizar_usuario.py
│   │   │   │   ├── obtener_usuario.py
│   │   │   │   └── eliminar_usuario.py
│   │   │   │
│   │   │   ├── reportes/
│   │   │   │   ├── generar_reporte_usuario.py
│   │   │   │   ├── generar_reporte_unidad.py
│   │   │   │   └── generar_reporte_global.py
│   │   │   │
│   │   │   └── importacion/
│   │   │       └── importar_excel.py
│   │   │
│   │   ├── dtos/                     # Data Transfer Objects
│   │   │   ├── usuario_dto.py
│   │   │   ├── reporte_dto.py
│   │   │   └── estadisticas_dto.py
│   │   │
│   │   └── services/                 # Servicios de aplicación
│   │       ├── autenticacion_service.py
│   │       └── sincronizacion_service.py
│   │
│   ├── infrastructure/               # 🔧 CAPA DE INFRAESTRUCTURA (Implementaciones)
│   │   ├── persistence/              # Persistencia de datos
│   │   │   ├── mysql/
│   │   │   │   ├── connection.py     # Conexión MySQL
│   │   │   │   ├── repositories/     # Implementaciones concretas
│   │   │   │   │   ├── mysql_usuario_repository.py
│   │   │   │   │   ├── mysql_modulo_repository.py
│   │   │   │   │   └── mysql_progreso_repository.py
│   │   │   │   └── migrations/       # Scripts SQL
│   │   │   │       ├── create_tables.sql
│   │   │   │       └── seed_data.sql
│   │   │   │
│   │   │   └── excel/                # Importación Excel
│   │   │       └── excel_importer.py
│   │   │
│   │   ├── external_services/        # Servicios externos
│   │   │   └── cornerstone_api.py    # API Cornerstone (Fase 2)
│   │   │
│   │   └── visualization/            # Generación de gráficos
│   │       ├── d3_generator.py       # Motor D3.js
│   │       └── pdf_generator.py      # Generador PDF
│   │
│   └── interfaces/                   # 🎨 CAPA DE INTERFACES (Adaptadores externos)
│       ├── ui/                       # Interfaz de usuario (Desktop)
│       │   ├── app.py                # Aplicación principal CTk
│       │   │
│       │   ├── presenters/           # Presentadores (MVP pattern)
│       │   │   ├── dashboard_presenter.py
│       │   │   ├── usuarios_presenter.py
│       │   │   └── reportes_presenter.py
│       │   │
│       │   ├── views/                # Vistas (UI pura)
│       │   │   ├── windows/
│       │   │   │   ├── login_window.py
│       │   │   │   └── main_window.py
│       │   │   │
│       │   │   ├── panels/
│       │   │   │   ├── dashboard_panel.py
│       │   │   │   ├── usuarios_panel.py
│       │   │   │   └── reportes_panel.py
│       │   │   │
│       │   │   └── components/       # Componentes reutilizables
│       │   │       ├── charts/
│       │   │       │   └── d3_chart_card.py
│       │   │       ├── forms/
│       │   │       └── navigation/
│       │   │           ├── sidebar.py
│       │   │           └── tab_button.py
│       │   │
│       │   └── state/                # Estado de la UI (opcional)
│       │       └── app_state.py
│       │
│       └── cli/                      # Interfaz CLI (futuro)
│           └── commands.py
│
├── tests/                            # 🧪 Tests organizados por capa
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   │
│   └── integration/
│       └── ui/
│
└── docs/                             # 📚 Documentación
    ├── architecture.md
    └── deployment.md
```

---

## 🔄 Mapeo de Archivos Actuales → Nuevos

| Actual | Nuevo | Razón |
|--------|-------|-------|
| `ejecutar_app.py` | `main.py` | Punto de entrada estándar |
| `interfaz/ventanas/` | `src/interfaces/ui/views/windows/` | Separación UI |
| `interfaz/componentes/` | `src/interfaces/ui/views/components/` | Componentes UI |
| `nucleo/configuracion/` | `config/` | Configuración externa |
| `nucleo/servicios/` | `src/application/services/` o `src/domain/services/` | Según tipo |
| `nucleo/base_datos/` | `src/infrastructure/persistence/mysql/` | Infraestructura |
| `database/` | `src/infrastructure/persistence/mysql/migrations/` | Scripts SQL |

---

## 📐 Principios Aplicados

### 1. **Inversión de Dependencias** (SOLID)
```python
# ❌ ANTES (Acoplamiento fuerte)
class UserReportPanel:
    def __init__(self):
        self.db = mysql.connector.connect(...)  # Depende de MySQL directo

# ✅ DESPUÉS (Interfaz)
class UserReportPanel:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuarios = usuario_repository  # Depende de interfaz
```

### 2. **Separación de Responsabilidades**
```python
# Domain: Lógica pura
class Usuario:
    def puede_generar_certificado(self) -> bool:
        return self.progreso >= 80.0

# Application: Caso de uso
class GenerarCertificado:
    def execute(self, user_id: str) -> Certificado:
        usuario = self.repo.find(user_id)
        if usuario.puede_generar_certificado():
            return self.cert_service.generar(usuario)

# Infrastructure: Implementación
class MySQLUsuarioRepository:
    def find(self, user_id: str) -> Usuario:
        # SQL query aquí
```

### 3. **Testeable**
```python
# Test unitario fácil (sin BD real)
def test_usuario_puede_certificar():
    usuario = Usuario(progreso=85.0)
    assert usuario.puede_generar_certificado() == True
```

---

## 🚀 Plan de Migración (Sin Romper Nada)

### **Fase 1: Estructura Base** (1-2 horas)
```bash
# Crear carpetas nuevas
mkdir -p src/{domain,application,infrastructure,interfaces}
mkdir -p config tests/unit tests/integration

# Mover archivos gradualmente (sin borrar originales)
# Primero copiamos, luego borramos
```

### **Fase 2: Capa de Dominio** (2-3 horas)
- Extraer entidades puras (Usuario, Módulo, Progreso)
- Crear interfaces de repositorios
- Mover lógica de negocio a servicios de dominio

### **Fase 3: Capa de Aplicación** (2-3 horas)
- Crear casos de uso
- Crear DTOs para comunicación entre capas

### **Fase 4: Capa de Infraestructura** (2-3 horas)
- Implementar repositorios MySQL
- Mover generadores (D3.js, PDF)

### **Fase 5: Capa de Interfaces** (3-4 horas)
- Reorganizar UI manteniendo funcionalidad
- Crear presentadores si es necesario

### **Fase 6: Limpieza** (1 hora)
- Borrar carpetas antiguas
- Actualizar imports
- Tests de integración

---

## ✅ Beneficios Inmediatos

1. **Testeable**: Puedes testear lógica sin BD ni UI
2. **Mantenible**: Cambios aislados en cada capa
3. **Escalable**: Fácil migrar a microservicios después
4. **Cambiar BD**: Solo cambias `infrastructure/persistence/`
5. **Cambiar UI**: Solo cambias `interfaces/ui/`
6. **API REST**: Añadir `interfaces/api/` sin tocar lógica

---

## 🎯 ¿Quieres que lo implemente?

Si dices **SÍ**, ejecuto la migración completa en ~2 horas de trabajo manteniendo TODO funcionando.

**¿Procedemos?** 🚀
