# 🔧 Solución al Error de Tabla Instituto_Soporte

## ❌ Error que te aparece

Cuando intentas buscar o seleccionar un usuario en **Gestionar Empleados**, la aplicación falla o muestra un error relacionado con la tabla `Instituto_Soporte`.

## 📋 Causa del Error

La tabla `Instituto_Soporte` todavía **no existe** en tu base de datos. Esta tabla es necesaria para almacenar el historial de soportes brindados a los usuarios.

## ✅ Solución (Elige una opción)

### **Opción 1: Script Python Automático** (Recomendado)

La forma más fácil es ejecutar el script Python que crea la tabla automáticamente:

```bash
python crear_tabla_soporte.py
```

Este script:
- Se conecta a tu base de datos
- Verifica si la tabla existe
- Crea la tabla con todos los campos necesarios
- Crea los índices para mejor performance
- Te muestra la estructura de la tabla creada

### **Opción 2: Script SQL Manual**

Si prefieres usar SQL Server Management Studio:

1. Abre **SQL Server Management Studio**
2. Conéctate a tu servidor de base de datos
3. Abre el archivo: `database/create_soporte_table.sql`
4. Selecciona tu base de datos (por defecto: `SmartReportsDB`)
5. Ejecuta el script (F5)

## 🎯 ¿Qué hace la tabla?

La tabla `Instituto_Soporte` almacena:

| Campo | Descripción |
|-------|-------------|
| SoporteId | ID único del registro (auto-incremental) |
| UserId | ID del usuario que recibió el soporte |
| Asunto | Título del soporte brindado |
| Descripcion | Detalles del problema y solución |
| Categoria | Tipo: Técnico, Funcional, Acceso/Permisos, Datos, Otro |
| FechaRegistro | Fecha y hora del registro |
| RegistradoPor | Usuario que registró el soporte (opcional) |

## 🔍 Verificar que funcionó

Después de crear la tabla:

1. Abre la aplicación Smart Reports v2.0
2. Ve a **Configuración → Gestionar Empleados**
3. Busca cualquier usuario
4. Haz clic en el usuario en la tabla
5. Deberías ver la sección **"📋 Historial de Soportes"** sin errores

## ⚠️ Comportamiento con y sin la tabla

### ✓ CON la tabla creada:
- Puedes registrar soportes en **Registro de Soporte**
- Al seleccionar un usuario, ves su historial de soportes
- Si no tiene soportes, muestra: "No hay registros de soporte para este usuario"

### ⚠️ SIN la tabla creada:
- Al seleccionar un usuario, muestra: "Tabla de soportes no creada. Ejecuta create_soporte_table.sql"
- Si intentas guardar un soporte, aparece mensaje de error con instrucciones
- Las demás funciones de gestión de usuarios funcionan normalmente

## 📝 Notas Importantes

- **Seguro de ejecutar**: El script verifica si la tabla existe antes de crearla
- **No afecta datos**: Solo crea una nueva tabla, no modifica tablas existentes
- **Foreign Key**: La tabla está vinculada a `Instituto_Usuario` para integridad de datos
- **Índices**: Se crean automáticamente para búsquedas rápidas por usuario y fecha

## 🆘 ¿Necesitas ayuda?

Si tienes problemas ejecutando el script:

1. Verifica que tienes permisos de CREATE TABLE en la base de datos
2. Asegúrate de que la tabla `Instituto_Usuario` existe
3. Revisa que la conexión a la base de datos funciona correctamente
4. Consulta el archivo `test_connection.py` para probar la conexión

---

**¿Todo listo?** Una vez creada la tabla, la aplicación funcionará perfectamente sin más configuración.
