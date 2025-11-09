# 🗄️ Smart Reports - Base de Datos

Sistema de gestión de base de datos MySQL para módulos de capacitación empresarial.

---

## 📁 Archivos Incluidos

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `ANALISIS_MODELO_ER.md` | Análisis completo del modelo ER | Documentación |
| `create_database_mysql.sql` | Script SQL completo | Crear base de datos |
| `database_manager.py` | Gestor Python de base de datos | Integración con Python |
| `README.md` | Este archivo | Guía de uso |

---

## 🚀 Inicio Rápido

### **1. Crear la Base de Datos**

```bash
# Opción A: Desde MySQL Workbench
# - Abrir MySQL Workbench
# - File → Open SQL Script → create_database_mysql.sql
# - Ejecutar (⚡ icono)

# Opción B: Desde línea de comandos
mysql -u root -p < create_database_mysql.sql
```

### **2. Usar desde Python**

```python
from database.database_manager import SmartReportsDB, DatabaseConfig

# Configurar conexión
config = DatabaseConfig(
    host='localhost',
    database='SmartReportsDB',
    user='root',
    password='tu_password',
    port=3306
)

# Inicializar sistema
db = SmartReportsDB(config)

# Usar los managers
usuarios = db.usuarios.listar_usuarios()
modulos = db.modulos.listar_modulos()
progreso = db.progreso.obtener_progreso_usuario('jperez')

# Cerrar al terminar
db.close()
```

---

## 📊 Estructura de la Base de Datos

### **Tablas Principales**

```
📦 SmartReportsDB
 ┣ 👥 Usuarios y Organización
 ┃ ┣ Rol (roles de usuario)
 ┃ ┣ UnidadDeNegocio (ICAVE, EIT, LCT, etc.)
 ┃ ┣ Departamento (por unidad de negocio)
 ┃ ┗ Usuario (usuarios del sistema)
 ┃
 ┣ 📚 Módulos de Capacitación
 ┃ ┣ Modulo (cursos/capacitaciones)
 ┃ ┣ ModuloDepartamento (asignación a departamentos)
 ┃ ┣ ProgresoModulo (progreso de usuarios)
 ┃ ┗ RecursoModulo (PDFs, videos, etc.)
 ┃
 ┣ 📝 Evaluaciones
 ┃ ┣ Evaluacion (evaluaciones de módulos)
 ┃ ┗ ResultadoEvaluacion (resultados de usuarios)
 ┃
 ┣ 📈 Auditoría e Historial
 ┃ ┣ HistorialProgreso (cambios de estado)
 ┃ ┗ AuditoriaAcceso (acciones del sistema)
 ┃
 ┗ 🔧 Soporte y Reportes
   ┣ Soporte (tickets de soporte)
   ┣ ReporteGuardado (reportes personalizados)
   ┣ Notificacion (notificaciones a usuarios)
   ┗ Certificado (certificados de finalización)
```

---

## 💡 Ejemplos de Uso

### **Crear un Usuario**

```python
nuevo_usuario = {
    'UserId': 'jperez',
    'NombreCompleto': 'Juan Pérez',
    'UserEmail': 'juan.perez@hutchison.com',
    'Password': 'password123',
    'IdUnidadDeNegocio': 1,
    'IdDepartamento': 1,
    'IdRol': 4,
    'UserStatus': 'Activo'
}

user_id = db.usuarios.crear_usuario(nuevo_usuario)
```

### **Crear un Módulo**

```python
from datetime import datetime, timedelta

nuevo_modulo = {
    'NombreModulo': 'Seguridad Industrial',
    'FechaInicioModulo': datetime.now().date(),
    'FechaCierre': (datetime.now() + timedelta(days=30)).date(),
    'Descripcion': 'Curso de seguridad',
    'DuracionEstimadaHoras': 8,
    'CategoriaModulo': 'Seguridad',
    'IdCreador': 1
}

modulo_id = db.modulos.crear_modulo(nuevo_modulo)
```

### **Asignar Módulo a Departamento**

```python
# Asignar módulo obligatorio con vencimiento
fecha_vencimiento = datetime.now() + timedelta(days=30)

db.modulos.asignar_a_departamento(
    id_modulo=1,
    id_departamento=1,
    obligatorio=True,
    fecha_vencimiento=fecha_vencimiento
)

# Esto automáticamente asigna el módulo a todos los usuarios del departamento
```

### **Consultar Progreso de Usuario**

```python
# Obtener progreso de un usuario
progreso = db.progreso.obtener_progreso_usuario('jperez')

for p in progreso:
    print(f"{p['NombreModulo']}: {p['EstatusModulo']} ({p['PorcentajeAvance']}%)")
```

### **Actualizar Progreso**

```python
# Actualizar estado y porcentaje
db.progreso.actualizar_progreso(
    id_inscripcion=1,
    estatus='En progreso',
    porcentaje=50.0,
    comentario='Usuario completó primera evaluación'
)
```

### **Registrar Resultado de Evaluación**

```python
resultado = db.evaluaciones.registrar_resultado(
    id_inscripcion=1,
    id_evaluacion=1,
    puntaje=85.0,
    intento=1
)

# Retorna: {'Aprobado': 1, 'Mensaje': 'Resultado registrado exitosamente'}
```

### **Generar Reportes**

```python
# Reporte de cumplimiento por unidad de negocio
reporte = db.reportes.reporte_cumplimiento_unidad(id_unidad=1)

for r in reporte:
    print(f"{r['NombreUnidad']} / {r['NombreDepartamento']}")
    print(f"  Cumplimiento: {r['PorcentajeCumplimiento']}%")
    print(f"  Completados: {r['Completados']} / {r['TotalAsignaciones']}")
    print(f"  Vencidos: {r['Vencidos']}")
```

### **Módulos Próximos a Vencer**

```python
# Obtener módulos que vencen en los próximos 7 días
vencidos = db.progreso.obtener_modulos_vencidos(dias_anticipacion=7)

for v in vencidos:
    print(f"{v['NombreCompleto']}: {v['NombreModulo']}")
    print(f"  Vence en: {v['DiasRestantes']} días")
    print(f"  Email: {v['UserEmail']}")
```

---

## 🔐 Seguridad

### **Configuración Recomendada**

```python
# ❌ NO HACER EN PRODUCCIÓN
config = DatabaseConfig(user='root', password='')

# ✅ HACER EN PRODUCCIÓN
config = DatabaseConfig(
    host='tu-servidor.com',
    database='SmartReportsDB',
    user='smartreports_app',  # Usuario con permisos limitados
    password=os.environ.get('DB_PASSWORD'),  # Desde variable de entorno
    port=3306
)
```

### **Crear Usuario de Aplicación**

```sql
-- Ejecutar en MySQL
CREATE USER 'smartreports_app'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT SELECT, INSERT, UPDATE, DELETE ON SmartReportsDB.* TO 'smartreports_app'@'localhost';
FLUSH PRIVILEGES;
```

### **Hash de Passwords**

El sistema usa SHA-256 para demostración. **En producción, usar bcrypt:**

```python
# Instalar: pip install bcrypt
import bcrypt

# Generar hash
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verificar
bcrypt.checkpw(password.encode(), password_hash)
```

---

## 📈 Vistas Predefinidas

El sistema incluye vistas útiles para reportes:

```sql
-- Vista: Progreso completo de usuarios
SELECT * FROM vw_UsuarioProgresoCompleto
WHERE NombreUnidad = 'ICAVE';

-- Vista: Módulos por departamento con estadísticas
SELECT * FROM vw_ModulosPorDepartamento
WHERE Obligatorio = 1;

-- Vista: Estadísticas de evaluaciones
SELECT * FROM vw_EstadisticasEvaluaciones
WHERE PorcentajeAprobacion < 70;
```

---

## 🔧 Procedimientos Almacenados

### **sp_AsignarModuloUsuario**

```sql
CALL sp_AsignarModuloUsuario('jperez', 1, '2025-12-31');
-- Asigna módulo 1 a usuario jperez con vencimiento
```

### **sp_ActualizarProgreso**

```sql
CALL sp_ActualizarProgreso(1, 'Completado', 100.0, 'Módulo finalizado exitosamente');
-- Actualiza progreso y registra en historial automáticamente
```

### **sp_RegistrarResultadoEvaluacion**

```sql
CALL sp_RegistrarResultadoEvaluacion(1, 1, 85.0, 1);
-- Registra resultado, determina si aprobó, actualiza progreso
```

---

## 🎓 Casos de Uso Comunes

### **1. Flujo de Asignación de Módulo**

```python
# 1. Crear módulo
modulo_id = db.modulos.crear_modulo(datos_modulo)

# 2. Asignar a departamento (asigna automáticamente a usuarios)
db.modulos.asignar_a_departamento(modulo_id, departamento_id, obligatorio=True)

# 3. Los usuarios ya tienen el módulo asignado con estado "No iniciado"
```

### **2. Flujo de Completación de Módulo**

```python
# 1. Usuario inicia módulo
db.progreso.actualizar_progreso(inscripcion_id, 'En progreso', 10.0)

# 2. Usuario avanza
db.progreso.actualizar_progreso(inscripcion_id, 'En progreso', 50.0)

# 3. Usuario toma evaluación
resultado = db.evaluaciones.registrar_resultado(inscripcion_id, evaluacion_id, 85.0, 1)

# 4. Si aprobó, el progreso se marca automáticamente como "Completado"
```

### **3. Monitoreo de Vencimientos**

```python
# Ejecutar diariamente (cronjob)
vencidos = db.progreso.obtener_modulos_vencidos(dias_anticipacion=3)

for modulo in vencidos:
    # Enviar email de recordatorio
    enviar_email(
        to=modulo['UserEmail'],
        subject=f"Recordatorio: {modulo['NombreModulo']} vence en {modulo['DiasRestantes']} días",
        body=generar_template_recordatorio(modulo)
    )
```

### **4. Dashboard de Gerencia**

```python
# Obtener métricas para dashboard
reporte = db.reportes.reporte_cumplimiento_unidad(id_unidad)

metricas = {
    'total_usuarios': sum(r['TotalAsignaciones'] for r in reporte),
    'completados': sum(r['Completados'] for r in reporte),
    'en_progreso': sum(r['EnProgreso'] for r in reporte),
    'vencidos': sum(r['Vencidos'] for r in reporte),
    'porcentaje_global': calcular_promedio_ponderado(reporte)
}

# Mostrar en gráficos
mostrar_graficos(metricas)
```

---

## 🐛 Troubleshooting

### **Error: Access denied for user**

```bash
# Verificar usuario y password
mysql -u root -p

# Crear usuario si no existe
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON SmartReportsDB.* TO 'tu_usuario'@'localhost';
```

### **Error: Can't connect to MySQL server**

```python
# Verificar que MySQL está corriendo
# Windows: services.msc → MySQL → Start
# Linux: sudo systemctl start mysql

# Verificar host y puerto
config = DatabaseConfig(
    host='127.0.0.1',  # En lugar de 'localhost'
    port=3306
)
```

### **Error: Table doesn't exist**

```bash
# Verificar que la base de datos fue creada
mysql -u root -p
USE SmartReportsDB;
SHOW TABLES;

# Si no existe, ejecutar el script nuevamente
mysql -u root -p < create_database_mysql.sql
```

### **Warnings sobre utf8mb4**

```sql
-- Configurar MySQL para usar utf8mb4
[mysqld]
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
```

---

## 📚 Documentación Adicional

- **Análisis Completo**: `ANALISIS_MODELO_ER.md`
- **Modelo Original**: Ver diagrama DBML en el análisis
- **API Reference**: Docstrings en `database_manager.py`

---

## 🔄 Actualización y Migración

### **Backup de Datos**

```bash
# Backup completo
mysqldump -u root -p SmartReportsDB > backup_$(date +%Y%m%d).sql

# Restaurar
mysql -u root -p SmartReportsDB < backup_20250709.sql
```

### **Migración de Datos**

```python
# Script de migración de ejemplo
from database_manager import SmartReportsDB, DatabaseConfig

# Base de datos origen
db_origen = SmartReportsDB(DatabaseConfig(database='OldDB'))

# Base de datos destino
db_destino = SmartReportsDB(DatabaseConfig(database='SmartReportsDB'))

# Migrar usuarios
usuarios_old = db_origen.db.execute_query("SELECT * FROM OldUsuarios", fetch_all=True)

for usuario in usuarios_old:
    nuevo_usuario = mapear_usuario(usuario)
    db_destino.usuarios.crear_usuario(nuevo_usuario)
```

---

## 📞 Soporte

Para preguntas o problemas:

1. Revisar `ANALISIS_MODELO_ER.md`
2. Consultar ejemplos en `database_manager.py`
3. Verificar logs de MySQL: `/var/log/mysql/error.log`
4. Contactar al equipo de desarrollo

---

## 📊 Estadísticas del Sistema

```sql
-- Ver estadísticas de la base de datos
SELECT
    table_name AS Tabla,
    table_rows AS Filas,
    ROUND(data_length / 1024 / 1024, 2) AS 'Tamaño (MB)'
FROM information_schema.tables
WHERE table_schema = 'SmartReportsDB'
ORDER BY data_length DESC;
```

---

**¡Sistema listo para usar!** 🚀

Para comenzar, ejecuta:
```bash
mysql -u root -p < create_database_mysql.sql
python database_manager.py
```
