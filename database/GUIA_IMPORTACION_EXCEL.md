# 📥 GUÍA: Importación de Excel - Fase 1

## 🎯 OBJETIVO

Importar datos de capacitación desde 3 archivos Excel a la base de datos MySQL `tngcore`:

1. **Usuarios** (1,529 usuarios activos)
2. **Asignaciones** (módulos asignados por usuario con fechas)
3. **Finalizaciones** (módulos completados con fechas y estatus)

---

## 📂 ESTRUCTURA DE ARCHIVOS

### **Scripts Creados**

```
database/
├── importar_usuarios_excel.py        # Importa usuarios desde Excel → CSV
├── importar_asignaciones_excel.py    # Importa asignaciones directamente a MySQL
├── importar_finalizaciones_excel.py  # Importa finalizaciones directamente a MySQL
└── importar_todo_excel.py            # Script maestro (ejecuta los 3 en orden)
```

---

## 🚀 OPCIÓN 1: Importación Completa Automática (RECOMENDADO)

### **Paso 1: Preparar archivos**

Coloca los 3 archivos Excel en la carpeta `data/`:

```
smart-reports1/
└── data/
    ├── usuarios.xlsx         (o archivo con "usuario" en el nombre)
    ├── asignaciones.xlsx     (o archivo con "asignacion" en el nombre)
    └── finalizaciones.xlsx   (o archivo con "finalizacion" en el nombre)
```

### **Paso 2: Configurar MySQL**

Edita `importar_todo_excel.py` línea ~240:

```python
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'TU_PASSWORD_AQUI',  # ⚠️ CAMBIAR
    'database': 'tngcore'
}
```

### **Paso 3: Ejecutar importación completa**

```bash
cd database
python importar_todo_excel.py
```

O especificando rutas:

```bash
python importar_todo_excel.py usuarios.xlsx asignaciones.xlsx finalizaciones.xlsx
```

### **Resultado**

El script ejecutará automáticamente:
1. ✅ Generación de CSV para usuarios
2. ✅ Importación de asignaciones a MySQL
3. ✅ Importación de finalizaciones a MySQL
4. ✅ Reporte consolidado final

---

## 🔧 OPCIÓN 2: Importación Manual (Paso a Paso)

### **1. Importar Usuarios**

```bash
python importar_usuarios_excel.py usuarios.xlsx
```

**Salida:**
- `usuarios_importacion.csv` - Archivo CSV listo para importar
- `usuarios_importacion_importacion.sql` - Script SQL con instrucciones

**Importar CSV a MySQL:**

**Opción A: MySQL Workbench (GUI)**
1. Abrir MySQL Workbench
2. Clic derecho en tabla `instituto_Usuario`
3. "Table Data Import Wizard"
4. Seleccionar `usuarios_importacion.csv`
5. Mapear columnas (automático)
6. Importar

**Opción B: Línea de comandos**
```bash
mysql -u root -p tngcore < usuarios_importacion_importacion.sql
```

### **2. Importar Asignaciones**

```bash
python importar_asignaciones_excel.py asignaciones.xlsx
```

**¿Qué hace?**
- Busca cada usuario en `instituto_Usuario`
- Crea módulos si no existen en `instituto_Modulo`
- Crea/actualiza registros en `instituto_ProgresoModulo`
- Establece `EstatusModulo = 'No iniciado'`

### **3. Importar Finalizaciones**

```bash
python importar_finalizaciones_excel.py finalizaciones.xlsx
```

**¿Qué hace?**
- Busca registros existentes en `instituto_ProgresoModulo`
- Actualiza `FechaFinalizacion`
- Cambia `EstatusModulo` a `'Completado'` o `'Incompleto'`
- Establece `PorcentajeAvance = 100.0` si completado

---

## 📋 FORMATO DE ARCHIVOS EXCEL

### **Excel 1: Usuarios**

| Columna | Tipo | Requerido | Ejemplo |
|---------|------|-----------|---------|
| UserId | Texto | ✅ Sí | jperez |
| Email | Texto | ✅ Sí | jperez@hutchison.com |
| Nombre | Texto | ✅ Sí | Juan Pérez |
| Account enabled | Texto | ⚠️ Opcional | True |
| Department | Texto | ⚠️ Opcional | Operaciones |
| Job title | Texto | ⚠️ Opcional | Supervisor |

**Notas:**
- El script detecta automáticamente variaciones de nombres de columnas
- Genera password temporal (usuario debe cambiar en primer login)
- Determina `Activo` según "Account enabled"

### **Excel 2: Asignaciones**

| Columna | Tipo | Requerido | Ejemplo |
|---------|------|-----------|---------|
| UserId | Texto | ✅ Sí | jperez |
| Módulo | Texto | ✅ Sí | Seguridad Industrial Básica |
| Fecha Asignación | Fecha | ✅ Sí | 2024-01-15 |
| Fecha Vencimiento | Fecha | ⚠️ Opcional | 2024-02-15 |

**Notas:**
- Si el usuario no existe, se salta (no se crea)
- Si el módulo no existe, se crea automáticamente
- Fechas pueden estar en cualquier formato (se parsean automáticamente)

### **Excel 3: Finalizaciones**

| Columna | Tipo | Requerido | Ejemplo |
|---------|------|-----------|---------|
| UserId | Texto | ✅ Sí | jperez |
| Módulo | Texto | ✅ Sí | Seguridad Industrial Básica |
| Fecha Finalización | Fecha | ✅ Sí | 2024-02-10 |
| Estatus | Texto | ⚠️ Opcional | Completado |
| Calificación | Número | ⚠️ Opcional | 95.5 |

**Notas:**
- Debe existir asignación previa (usuario + módulo)
- Si no se especifica estatus, se asume "Completado"
- Estatus acepta: Completado, Incompleto, Complete, Incomplete, etc.

---

## 🔍 VALIDACIONES Y ERRORES

### **Errores Comunes**

**1. "Usuario no encontrado"**
- **Causa**: UserId no existe en `instituto_Usuario`
- **Solución**: Importar usuarios primero

**2. "Progreso no encontrado"**
- **Causa**: No existe asignación previa para ese usuario + módulo
- **Solución**: Importar asignaciones primero

**3. "Columna faltante"**
- **Causa**: Excel no tiene columnas requeridas
- **Solución**: Verificar nombres de columnas (ver mapeo automático)

**4. "Error parseando fecha"**
- **Causa**: Formato de fecha no reconocido
- **Solución**: Usar formato estándar (YYYY-MM-DD o DD/MM/YYYY)

### **Logs Detallados**

Todos los scripts imprimen logs útiles:

```
✅ Éxito
⚠️ Advertencia (no bloquea)
❌ Error (bloquea)
📊 Estadística
🔄 Procesando
```

---

## 📊 REPORTE DE IMPORTACIÓN

Al finalizar, se muestra un reporte como:

```
============================================================
📊 REPORTE FINAL DE IMPORTACIÓN
============================================================
🕐 Fecha: 2024-11-09 15:30:00
============================================================

✅ USUARIOS:
   CSV generado: usuarios_importacion.csv
   SQL generado: usuarios_importacion_importacion.sql

✅ ASIGNACIONES:
   Registros leídos:              2,450
   Usuarios encontrados:          2,380
   Usuarios no encontrados:       70
   Módulos creados:               45
   Asignaciones creadas:          2,320
   Asignaciones actualizadas:     60

✅ FINALIZACIONES:
   Registros leídos:              1,890
   Progresos encontrados:         1,850
   Progresos no encontrados:      40
   Completados registrados:       1,720
   Incompletos registrados:       130

============================================================
✅ IMPORTACIÓN COMPLETA FINALIZADA
============================================================
```

---

## 🐛 DEBUGGING

### **Verificar datos importados**

```sql
-- Ver usuarios importados
SELECT COUNT(*) FROM instituto_Usuario;
SELECT * FROM instituto_Usuario LIMIT 10;

-- Ver asignaciones
SELECT
    u.NombreCompleto,
    m.NombreModulo,
    pm.EstatusModulo,
    pm.FechaAsignacion
FROM instituto_ProgresoModulo pm
JOIN instituto_Usuario u ON pm.UserId = u.UserId
JOIN instituto_Modulo m ON pm.IdModulo = m.IdModulo
LIMIT 10;

-- Ver finalizaciones
SELECT
    u.NombreCompleto,
    m.NombreModulo,
    pm.FechaFinalizacion,
    pm.EstatusModulo
FROM instituto_ProgresoModulo pm
JOIN instituto_Usuario u ON pm.UserId = u.UserId
JOIN instituto_Modulo m ON pm.IdModulo = m.IdModulo
WHERE pm.FechaFinalizacion IS NOT NULL
LIMIT 10;
```

### **Test rápido**

```bash
# Ver ayuda
python importar_todo_excel.py --help

# Modo dry-run (solo validación, no importa)
# TODO: Implementar flag --dry-run
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### **Cambiar puerto MySQL**

Editar en cada script:

```python
config = {
    'host': 'localhost',
    'port': 3307,  # ← Agregar si no es el default (3306)
    'user': 'root',
    'password': '',
    'database': 'tngcore'
}
```

### **Asignar Unidades de Negocio automáticamente**

Después de importar usuarios, ejecutar:

```sql
UPDATE instituto_Usuario
SET IdUnidadDeNegocio = CASE
    WHEN UserEmail LIKE '%@icave.%' THEN 1
    WHEN UserEmail LIKE '%@eit.%' THEN 2
    WHEN UserEmail LIKE '%@lct.%' THEN 3
    WHEN UserEmail LIKE '%@timsa.%' THEN 4
    WHEN UserEmail LIKE '%@hpmx.%' THEN 5
    WHEN UserEmail LIKE '%@tng.%' THEN 6
    ELSE IdUnidadDeNegocio
END
WHERE IdUnidadDeNegocio IS NULL;
```

### **Asignar Rol por defecto**

```sql
UPDATE instituto_Usuario
SET IdRol = 2  -- Rol "Usuario"
WHERE IdRol IS NULL;
```

---

## 🎯 ORDEN DE EJECUCIÓN CORRECTO

**¡IMPORTANTE!** Siempre respetar este orden:

```
1️⃣ USUARIOS      (base de datos, sin ellos nada funciona)
      ↓
2️⃣ ASIGNACIONES  (requiere usuarios existentes)
      ↓
3️⃣ FINALIZACIONES (requiere asignaciones existentes)
```

**NO** importar en otro orden o habrá errores.

---

## 📦 DEPENDENCIAS

```bash
pip install pandas openpyxl mysql-connector-python
```

---

## 🔒 SEGURIDAD

⚠️ **NUNCA** subir archivos con contraseñas a Git:

```bash
# .gitignore
database/*.csv
database/*_importacion.sql
data/*.xlsx
*.pyc
```

---

## ✅ CHECKLIST DE IMPORTACIÓN

- [ ] Base de datos `tngcore` creada
- [ ] Tablas `instituto_*` creadas (ver `create_tables_instituto.sql`)
- [ ] Archivos Excel preparados en carpeta `data/`
- [ ] Contraseña MySQL configurada en scripts
- [ ] Ejecutar `importar_todo_excel.py`
- [ ] Verificar logs (sin errores críticos)
- [ ] Validar datos en MySQL Workbench
- [ ] Asignar unidades de negocio (opcional)
- [ ] Asignar roles (opcional)
- [ ] ✅ ¡Listo para generar dashboards!

---

## 📞 SOPORTE

Si encuentras problemas:

1. Revisar logs en consola (muy descriptivos)
2. Verificar formato de Excel (columnas requeridas)
3. Verificar orden de importación (usuarios → asignaciones → finalizaciones)
4. Verificar conexión a MySQL (host, user, password)

---

**✅ LISTO PARA FASE 1**
**📅 Entrega: Martes**
**🏢 Instituto Hutchison Ports**
