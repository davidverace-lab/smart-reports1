# 📊 MODELO ENTIDAD-RELACIÓN DEFINITIVO
## Smart Reports - Instituto Hutchison Ports

---

## 📋 ANÁLISIS DE TU BASE DE DATOS ACTUAL

### ✅ **LO QUE ESTÁ BIEN:**
1. **18 tablas bien estructuradas** con prefijo `instituto_`
2. **3 vistas útiles** para reportes
3. **3 procedimientos almacenados** para lógica compleja
4. **3 triggers** para automatización
5. **Índices bien definidos** para optimización
6. **Foreign keys con CASCADE/RESTRICT** apropiadas
7. **Constraints y validaciones** en campos críticos

### ⚠️ **PROBLEMAS DETECTADOS:**

1. **INCONSISTENCIA EN QUERIES:**
   - Tus queries en `queries_hutchison.py` usan nombres SIN prefijo `instituto_`
   - La BD real usa prefijo `instituto_` en todas las tablas
   - **Solución:** Actualizar todas las queries para usar el prefijo correcto

2. **FALTA DE NORMALIZACIÓN EN Usuario:**
   - Campos `Division`, `Position`, `Nivel` deberían ser tablas separadas
   - Campos `TipoDeCorreo`, `Grupo` sin validación por FK

3. **FALTA DE GESTIÓN DE PERMISOS:**
   - No hay tabla de permisos granulares
   - Solo hay roles sin definir qué puede hacer cada rol

4. **FALTA DE TRAZABILIDAD COMPLETA:**
   - No se registra quién modificó módulos, departamentos, etc.
   - Solo hay auditoría de accesos

---

## 🎯 MODELO ER OPTIMIZADO - PROPUESTA DEFINITIVA

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MÓDULO DE SEGURIDAD                             │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│  instituto_Rol   │◄─────────►│instituto_Permiso │◄─────────►│instituto_RolPer- │
│                  │  1     N  │                  │  N     N  │     miso         │
├──────────────────┤           ├──────────────────┤           ├──────────────────┤
│ IdRol (PK)       │           │ IdPermiso (PK)   │           │ IdRolPermiso(PK) │
│ NombreRol        │           │ NombrePermiso    │           │ IdRol (FK)       │
│ Descripcion      │           │ Recurso          │           │ IdPermiso (FK)   │
│ Activo           │           │ Accion           │           │ Permitir         │
│ FechaCreacion    │           │ Descripcion      │           │ FechaAsignacion  │
└──────────────────┘           └──────────────────┘           └──────────────────┘
        │
        │ 1:N
        ▼
┌──────────────────┐
│ instituto_Usuario│
│                  │
├──────────────────┤
│ IdUsuario (PK)   │
│ UserId (UQ)      │
│ IdUnidadDeNeg(FK)│
│ IdDepartamento FK│
│ IdRol (FK)       │
│ IdNivel (FK) ◄───────┐
│ IdPosicion (FK) ◄────┤─────────────────────────┐
│ NombreCompleto   │   │                         │
│ UserEmail        │   │                         │
│ PasswordHash     │   │  ┌──────────────────┐  │  ┌──────────────────┐
│ TipoDeCorreo     │   │  │ instituto_Nivel  │  │  │instituto_Posicion│
│ UserStatus       │   │  │                  │  │  │                  │
│ Ubicacion        │   │  ├──────────────────┤  │  ├──────────────────┤
│ Activo           │   └──┤ IdNivel (PK)     │  └──┤ IdPosicion (PK)  │
│ FechaCreacion    │      │ NombreNivel      │     │ NombrePosicion   │
│ UltimoAcceso     │      │ Jerarquia (1-10) │     │ Descripcion      │
└──────────────────┘      │ Descripcion      │     │ IdDepartamento   │
                          │ Activo           │     │ Activo           │
                          └──────────────────┘     └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO ORGANIZACIONAL                                │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────┐
│instituto_UnidadDe- │
│     Negocio        │
├────────────────────┤
│ IdUnidadDeNegocio  │
│   (PK)             │
│ NombreUnidad       │
│ Codigo             │
│ Descripcion        │
│ IdResponsable (FK) │◄─── Usuario responsable
│ Activo             │
│ FechaCreacion      │
└────────────────────┘
        │ 1:N
        ▼
┌────────────────────┐
│instituto_Departa-  │
│      mento         │
├────────────────────┤
│ IdDepartamento(PK) │
│ IdUnidadDeNego(FK) │
│ NombreDepartamento │
│ Codigo             │
│ Descripcion        │
│ IdResponsable (FK) │◄─── Usuario responsable
│ Activo             │
│ FechaCreacion      │
└────────────────────┘
        │ 1:N
        ▼
┌────────────────────┐
│instituto_Equipo    │ ◄─── NUEVA TABLA (sub-departamentos)
├────────────────────┤
│ IdEquipo (PK)      │
│ IdDepartamento(FK) │
│ NombreEquipo       │
│ IdLider (FK)       │◄─── Usuario líder
│ Descripcion        │
│ Activo             │
└────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE CAPACITACIÓN                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_Categoria│ ◄─── NUEVA TABLA (categorías de módulos)
├──────────────────┤
│ IdCategoria (PK) │
│ NombreCategoria  │
│ Descripcion      │
│ ColorHex         │
│ IconoUrl         │
│ Orden            │
│ Activo           │
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Modulo  │
├──────────────────┤
│ IdModulo (PK)    │
│ NombreModulo     │
│ IdCategoria (FK) │◄─── Ahora FK en lugar de texto
│ FechaInicio      │
│ FechaCierre      │
│ Descripcion      │
│ DuracionEstHoras │
│ IdCreador (FK)   │
│ Prerequisitos    │◄─── NUEVO: JSON con IDs de módulos requeridos
│ Obligatorio      │◄─── NUEVO: Si es obligatorio para todos
│ NivelDificultad  │◄─── NUEVO: 1=Básico, 2=Intermedio, 3=Avanzado
│ Activo           │
│ FechaCreacion    │
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐           ┌──────────────────┐
│instituto_Modulo- │           │instituto_Leccion │ ◄─── NUEVA TABLA
│   Departamento   │           │                  │
├──────────────────┤           ├──────────────────┤
│ IdModuloDepto PK │           │ IdLeccion (PK)   │
│ IdModulo (FK)    │────┐      │ IdModulo (FK)    │
│ IdDepartamento FK│    │ 1:N  │ Titulo           │
│ Obligatorio      │    └─────►│ Descripcion      │
│ FechaAsignacion  │           │ TipoLeccion      │◄─── Video, PDF, Quiz, etc.
│ FechaVencimiento │           │ ContenidoUrl     │
│ Activo           │           │ Duracion         │
└──────────────────┘           │ Orden            │
                               │ Obligatoria      │
                               │ Activo           │
                               └──────────────────┘
                                       │ 1:N
                                       ▼
                               ┌──────────────────┐
                               │instituto_Recurso-│ ◄─── MOVIDO AQUÍ
                               │     Leccion      │
                               ├──────────────────┤
                               │ IdRecurso (PK)   │
                               │ IdLeccion (FK)   │
                               │ NombreRecurso    │
                               │ TipoRecurso      │
                               │ UrlRecurso       │
                               │ Descripcion      │
                               │ TamanoBytes      │
                               │ Orden            │
                               │ Descargable      │◄─── NUEVO
                               │ FechaCreacion    │
                               │ Activo           │
                               └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE PROGRESO                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_Progreso│
│     Modulo       │
├──────────────────┤
│ IdInscripcion PK │
│ UserId (FK)      │
│ IdModulo (FK)    │
│ EstatusModulo    │
│ PorcentajeAvance │
│ TiempoInvertido  │
│ FechaAsignacion  │
│ FechaVencimiento │
│ FechaInicio      │
│ FechaFinalizacion│
│ IntentoActual    │◄─── NUEVO: Número de intentos
│ IntentosPermitido│◄─── NUEVO: Max intentos permitidos
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Progreso│ ◄─── NUEVA TABLA (progreso por lección)
│     Leccion      │
├──────────────────┤
│ IdProgresoLecc PK│
│ IdInscripcion FK │
│ IdLeccion (FK)   │
│ Completada       │
│ TiempoInvertido  │
│ UltimaVisita     │
│ NumeroVisitas    │
│ PorcentajeVisto  │◄─── Para videos
│ FechaCompletado  │
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE EVALUACIONES                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_        │
│   Evaluacion     │
├──────────────────┤
│ IdEvaluacion (PK)│
│ IdModulo (FK)    │
│ NombreEvaluacion │
│ Descripcion      │
│ TipoEvaluacion   │◄─── NUEVO: Quiz, Examen, Práctica, etc.
│ PuntajeMinimo    │
│ PuntajeMaximo    │
│ IntentosPermitid │
│ TiempoLimite     │
│ MostrarRespuestas│◄─── NUEVO: Si muestra respuestas correctas
│ Aleatorizar      │◄─── NUEVO: Si aleatoriza preguntas
│ Activo           │
│ FechaCreacion    │
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Pregunta│ ◄─── NUEVA TABLA
├──────────────────┤
│ IdPregunta (PK)  │
│ IdEvaluacion (FK)│
│ TextoPregunta    │
│ TipoPregunta     │◄─── Opción múltiple, V/F, Abierta, etc.
│ Puntaje          │
│ Orden            │
│ Activo           │
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Opcion  │ ◄─── NUEVA TABLA
├──────────────────┤
│ IdOpcion (PK)    │
│ IdPregunta (FK)  │
│ TextoOpcion      │
│ EsCorrecta       │
│ Orden            │
└──────────────────┘


┌──────────────────┐
│instituto_Resultado│
│   Evaluacion     │
├──────────────────┤
│ IdResultado (PK) │
│ IdInscripcion FK │
│ IdEvaluacion (FK)│
│ PuntajeObtenido  │
│ Aprobado         │
│ IntentoNumero    │
│ FechaRealizacion │
│ TiempoInvertido  │
│ RespuestasJSON   │◄─── NUEVO: JSON con respuestas del usuario
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE CERTIFICADOS                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_        │
│  Certificado     │
├──────────────────┤
│ IdCertificado PK │
│ IdInscripcion FK │
│ CodigoCertificado│
│ FechaEmision     │
│ FechaVencimiento │
│ UrlPDF           │
│ HashVerificacion │
│ Valido           │
│ IdFirmante (FK)  │◄─── NUEVO: Usuario que firma el certificado
│ PlantillaUsada   │◄─── NUEVO: Qué plantilla se usó
│ MetadataJSON     │◄─── NUEVO: Info adicional (duración, puntaje, etc.)
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE COMUNICACIÓN                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_        │
│  Notificacion    │
├──────────────────┤
│ IdNotificacion PK│
│ IdUsuario (FK)   │
│ TipoNotificacion │
│ Titulo           │
│ Mensaje          │
│ Prioridad        │
│ Leida            │
│ FechaCreacion    │
│ FechaLectura     │
│ UrlDestino       │
│ AccionPrimaria   │◄─── NUEVO: Texto del botón de acción
│ AccionUrl        │◄─── NUEVO: URL de la acción
└──────────────────┘


┌──────────────────┐
│instituto_        │ ◄─── NUEVA TABLA (anuncios generales)
│   Anuncio        │
├──────────────────┤
│ IdAnuncio (PK)   │
│ Titulo           │
│ Contenido        │
│ TipoAnuncio      │
│ Prioridad        │
│ IdCreador (FK)   │
│ FechaInicio      │
│ FechaFin         │
│ DestinatariosJSON│◄─── JSON con filtros (roles, unidades, etc.)
│ Activo           │
│ FechaCreacion    │
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE SOPORTE                                    │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_Soporte │
├──────────────────┤
│ IdSoporte (PK)   │
│ IdUsuario (FK)   │
│ FechaSolicitud   │
│ Asunto           │
│ Descripcion      │
│ Categoria        │
│ Prioridad        │
│ Estatus          │
│ IdAsignado (FK)  │
│ FechaRespuesta   │
│ FechaCierre      │
│ Respuesta        │
│ SatisfaccionUser │◄─── NUEVO: Calificación 1-5
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Soporte-│ ◄─── NUEVA TABLA (seguimiento de tickets)
│   Seguimiento    │
├──────────────────┤
│ IdSeguimiento PK │
│ IdSoporte (FK)   │
│ IdUsuario (FK)   │
│ TipoAccion       │
│ Comentario       │
│ FechaAccion      │
│ AdjuntoUrl       │
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE REPORTES                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_Reporte-│
│    Guardado      │
├──────────────────┤
│ IdReporte (PK)   │
│ IdUsuarioCreador │
│ NombreReporte    │
│ FechaCreacion    │
│ TipoReporte      │
│ Descripcion      │
│ FiltrosJSON      │
│ Compartido       │
│ Favorito         │
│ UltimaEjecucion  │◄─── NUEVO
│ NumeroEjecuciones│◄─── NUEVO
└──────────────────┘
        │ 1:N
        ▼
┌──────────────────┐
│instituto_Reporte-│ ◄─── NUEVA TABLA (compartir reportes)
│   Compartido     │
├──────────────────┤
│ IdCompartido (PK)│
│ IdReporte (FK)   │
│ IdUsuario (FK)   │
│ PermisoEdicion   │
│ FechaCompartido  │
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE AUDITORÍA                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_        │
│ AuditoriaAcceso  │
├──────────────────┤
│ IdAuditoria (PK) │
│ IdUsuario (FK)   │
│ Accion           │
│ Modulo           │
│ Detalle          │
│ DireccionIP      │
│ UserAgent        │
│ Exito            │
│ FechaAccion      │
│ DuracionMs       │◄─── NUEVO: Tiempo que tomó la acción
└──────────────────┘


┌──────────────────┐
│instituto_        │ ◄─── NUEVA TABLA (auditoría de cambios en datos)
│AuditoriaCambios  │
├──────────────────┤
│ IdAuditCambio PK │
│ Tabla            │
│ IdRegistro       │
│ IdUsuario (FK)   │
│ TipoCambio       │◄─── INSERT, UPDATE, DELETE
│ ValoresAnteriores│◄─── JSON con valores antes del cambio
│ ValoresNuevos    │◄─── JSON con valores después del cambio
│ FechaCambio      │
│ DireccionIP      │
└──────────────────┘


┌──────────────────┐
│instituto_        │
│ HistorialProgreso│
├──────────────────┤
│ IdHistorial (PK) │
│ IdInscripcion FK │
│ EstatusAnterior  │
│ EstatusNuevo     │
│ PorcentajeAnt    │
│ PorcentajeNuevo  │
│ FechaCambio      │
│ Comentario       │
│ IdUsuarioModif FK│
│ TipoCambio       │◄─── NUEVO: Auto, Manual, Sistema
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE CONFIGURACIÓN                              │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│instituto_        │ ◄─── NUEVA TABLA (configuraciones del sistema)
│  Configuracion   │
├──────────────────┤
│ IdConfig (PK)    │
│ Clave            │
│ Valor            │
│ Tipo             │◄─── String, Int, Boolean, JSON
│ Descripcion      │
│ Categoria        │
│ Editable         │
│ IdUsuarioMod FK  │
│ FechaModificacion│
└──────────────────┘


┌──────────────────┐
│instituto_        │ ◄─── NUEVA TABLA (plantillas de emails/PDFs)
│   Plantilla      │
├──────────────────┤
│ IdPlantilla (PK) │
│ NombrePlantilla  │
│ TipoPlantilla    │◄─── Email, PDF, Certificado, etc.
│ Contenido        │◄─── HTML/Text con placeholders
│ VariablesJSON    │◄─── Variables disponibles
│ Activo           │
│ FechaCreacion    │
└──────────────────┘
```

---

## 🆕 NUEVAS TABLAS PROPUESTAS

| # | Tabla | Propósito | Prioridad |
|---|-------|-----------|-----------|
| 1 | `instituto_Permiso` | Gestión granular de permisos | 🔴 Alta |
| 2 | `instituto_RolPermiso` | Relación N:N entre roles y permisos | 🔴 Alta |
| 3 | `instituto_Nivel` | Niveles jerárquicos normalizados | 🟡 Media |
| 4 | `instituto_Posicion` | Posiciones laborales normalizadas | 🟡 Media |
| 5 | `instituto_Equipo` | Sub-departamentos o equipos de trabajo | 🟢 Baja |
| 6 | `instituto_Categoria` | Categorías de módulos | 🔴 Alta |
| 7 | `instituto_Leccion` | Lecciones dentro de módulos | 🔴 Alta |
| 8 | `instituto_RecursoLeccion` | Recursos por lección (reemplazo) | 🔴 Alta |
| 9 | `instituto_ProgresoLeccion` | Progreso por lección | 🔴 Alta |
| 10 | `instituto_Pregunta` | Preguntas de evaluaciones | 🔴 Alta |
| 11 | `instituto_Opcion` | Opciones de preguntas | 🔴 Alta |
| 12 | `instituto_Anuncio` | Anuncios generales del sistema | 🟡 Media |
| 13 | `instituto_SoporteSeguimiento` | Seguimiento de tickets | 🟡 Media |
| 14 | `instituto_ReporteCompartido` | Compartir reportes entre usuarios | 🟢 Baja |
| 15 | `instituto_AuditoriaCambios` | Auditoría de cambios en datos | 🟡 Media |
| 16 | `instituto_Configuracion` | Configuraciones del sistema | 🟡 Media |
| 17 | `instituto_Plantilla` | Plantillas de emails/PDFs | 🟡 Media |

---

## 🔑 RELACIONES PRINCIPALES

```
Usuario (1) ──────► (N) ProgresoModulo ◄────── (1) Modulo
                                                      │
                                                      │ (1:N)
                                                      ▼
                                                  Leccion
                                                      │
                                                      │ (1:N)
                                                      ▼
                                               ProgresoLeccion


Modulo (1) ───────► (N) Evaluacion
                           │
                           │ (1:N)
                           ▼
                       Pregunta
                           │
                           │ (1:N)
                           ▼
                        Opcion


ProgresoModulo ────► ResultadoEvaluacion ────► Certificado
     (1)                    (N)                    (1)


Rol (N) ◄──── RolPermiso ────► (N) Permiso
```

---

## ⚡ ÍNDICES RECOMENDADOS (ADICIONALES)

```sql
-- Búsquedas por email
CREATE INDEX idx_usuario_email_activo
ON instituto_Usuario(UserEmail, Activo);

-- Progreso por usuario y estatus
CREATE INDEX idx_progreso_usuario_estatus_modulo
ON instituto_ProgresoModulo(UserId, EstatusModulo, IdModulo);

-- Evaluaciones por módulo
CREATE INDEX idx_evaluacion_modulo_activo
ON instituto_Evaluacion(IdModulo, Activo);

-- Resultados recientes
CREATE INDEX idx_resultado_fecha_desc
ON instituto_ResultadoEvaluacion(FechaRealizacion DESC);

-- Notificaciones no leídas
CREATE INDEX idx_notif_usuario_leida_fecha
ON instituto_Notificacion(IdUsuario, Leida, FechaCreacion DESC);

-- Certificados válidos
CREATE INDEX idx_cert_codigo_valido
ON instituto_Certificado(CodigoCertificado, Valido);

-- Auditoría por fecha
CREATE INDEX idx_audit_fecha_usuario
ON instituto_AuditoriaAcceso(FechaAccion DESC, IdUsuario);
```

---

## 📊 VISTAS ADICIONALES RECOMENDADAS

```sql
-- Vista de usuarios con progreso completo
CREATE OR REPLACE VIEW vw_instituto_DashboardUsuario AS
SELECT
    u.IdUsuario,
    u.UserId,
    u.NombreCompleto,
    COUNT(DISTINCT pm.IdModulo) as ModulosAsignados,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as ModulosCompletados,
    ROUND(AVG(pm.PorcentajeAvance), 2) as ProgresoPromedio,
    COUNT(DISTINCT c.IdCertificado) as CertificadosObtenidos,
    MAX(pm.FechaFinalizacion) as UltimaFinalizacion
FROM instituto_Usuario u
LEFT JOIN instituto_ProgresoModulo pm ON u.UserId = pm.UserId
LEFT JOIN instituto_Certificado c ON pm.IdInscripcion = c.IdInscripcion
WHERE u.Activo = 1
GROUP BY u.IdUsuario;

-- Vista de módulos con estadísticas
CREATE OR REPLACE VIEW vw_instituto_EstadisticasModulo AS
SELECT
    m.IdModulo,
    m.NombreModulo,
    m.CategoriaModulo,
    COUNT(DISTINCT pm.UserId) as UsuariosInscritos,
    SUM(CASE WHEN pm.EstatusModulo = 'Completado' THEN 1 ELSE 0 END) as UsuariosCompletados,
    ROUND(AVG(CASE WHEN pm.EstatusModulo = 'Completado' THEN pm.TiempoInvertidoMinutos END), 0) as TiempoPromedioMin,
    ROUND(AVG(CASE WHEN re.Aprobado = 1 THEN re.PuntajeObtenido END), 2) as PromedioCalificacion
FROM instituto_Modulo m
LEFT JOIN instituto_ProgresoModulo pm ON m.IdModulo = pm.IdModulo
LEFT JOIN instituto_ResultadoEvaluacion re ON pm.IdInscripcion = re.IdInscripcion
WHERE m.Activo = 1
GROUP BY m.IdModulo;

-- Vista de alertas y vencimientos
CREATE OR REPLACE VIEW vw_instituto_AlertasVencimiento AS
SELECT
    u.IdUsuario,
    u.NombreCompleto,
    u.UserEmail,
    m.NombreModulo,
    pm.FechaVencimiento,
    DATEDIFF(pm.FechaVencimiento, NOW()) as DiasRestantes,
    pm.PorcentajeAvance,
    CASE
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) < 0 THEN 'Vencido'
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) <= 3 THEN 'Urgente'
        WHEN DATEDIFF(pm.FechaVencimiento, NOW()) <= 7 THEN 'Próximo'
        ELSE 'Normal'
    END as Prioridad
FROM instituto_ProgresoModulo pm
JOIN instituto_Usuario u ON pm.UserId = u.UserId
JOIN instituto_Modulo m ON pm.IdModulo = m.IdModulo
WHERE pm.EstatusModulo != 'Completado'
  AND pm.FechaVencimiento IS NOT NULL
  AND u.Activo = 1
ORDER BY pm.FechaVencimiento;
```

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

### **FASE 1 - CORRECCIONES URGENTES** 🔴
1. ✅ Actualizar **todas las queries** en `queries_hutchison.py` para usar prefijo `instituto_`
2. ✅ Crear tabla `instituto_Categoria` para normalizar categorías
3. ✅ Crear tabla `instituto_Permiso` y `instituto_RolPermiso` para permisos granulares
4. ✅ Agregar índices adicionales recomendados

### **FASE 2 - MEJORAS ESTRUCTURA** 🟡
5. ✅ Crear tablas `instituto_Leccion` y `instituto_ProgresoLeccion`
6. ✅ Crear tablas `instituto_Pregunta` y `instituto_Opcion`
7. ✅ Migrar `instituto_RecursoModulo` → `instituto_RecursoLeccion`
8. ✅ Crear vistas adicionales recomendadas

### **FASE 3 - FUNCIONALIDADES NUEVAS** 🟢
9. ⭕ Crear tabla `instituto_Anuncio`
10. ⭕ Crear tabla `instituto_SoporteSeguimiento`
11. ⭕ Crear tabla `instituto_AuditoriaCambios`
12. ⭕ Crear tabla `instituto_Configuracion` y `instituto_Plantilla`

---

## 📝 NOTAS FINALES

- **Total de tablas actuales:** 18
- **Total de tablas propuestas:** +17 nuevas = **35 tablas**
- **Vistas actuales:** 3
- **Vistas propuestas:** +3 nuevas = **6 vistas**
- **Procedimientos almacenados:** 3 (suficientes por ahora)
- **Triggers:** 3 (suficientes por ahora)

---

**Próximo documento:** `MIGRACIONES_BD.sql` con scripts de migración
