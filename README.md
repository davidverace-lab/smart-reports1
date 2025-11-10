# 🚀 Smart Reports - Instituto Hutchison Ports

Sistema de reportes y dashboards para capacitación con **arquitectura DDD + Hexagonal escalable**.

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

## 📂 Nueva Arquitectura

```
smart-reports1/
├── main.py                  # 🚀 Punto de entrada único
├── config/                  # ⚙️ Configuración centralizada
├── src/                     # 📦 Código fuente
│   ├── domain/              # 🧠 Lógica de negocio
│   ├── application/         # 💼 Casos de uso
│   ├── infrastructure/      # 🔧 Implementaciones
│   └── interfaces/ui/       # 🎨 Desktop UI
├── tests/                   # 🧪 Tests
└── data/                    # 📊 Excel para importar
```

---

## 🎨 Pestañas del Sistema

- **📊 Dashboards**: Métricas y gráficos D3.js interactivos
- **👥 Consulta Usuarios**: Búsqueda y filtros avanzados
- **🔄 Cruce de Datos**: Sincronización Cornerstone
- **📄 Reportes**: PDF profesionales (usuario, unidad, global, período)
- **⚙️ Configuración**: Gestión de usuarios y ajustes

---

## 📥 Importar Excel

```bash
# 1. Coloca 3 archivos en data/
# 2. Configura MySQL en config/database.py
# 3. Ejecuta:
python src/infrastructure/persistence/excel/excel_importer.py
```

---

## ✅ Características

- ✅ D3.js interactivo (azules navy)
- ✅ Reportes HTML estilo Word
- ✅ Transiciones fluidas
- ✅ Arquitectura escalable
- ✅ Temas claro/oscuro

---

**v2.0** - Instituto Hutchison Ports © 2025
