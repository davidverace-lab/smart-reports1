# 🔧 Solución Error: "sqlsever" vs "sqlserver"

## ❌ Error Detectado

```
ValueError: Tipo de BD no soportado: sqlsever
```

## 🎯 Causa

Hay un **typo** en tu archivo de configuración. Dice `sqlsever` pero debe ser `sqlserver`.

---

## ✅ Solución Rápida

### Opción 1: Archivo .env (RECOMENDADO)

Si tienes un archivo `.env` en la raíz del proyecto:

1. **Abre el archivo** `.env` (está en la raíz del proyecto junto a `main.py`)
2. **Busca la línea:**
   ```bash
   DB_TYPE=sqlsever  # ❌ INCORRECTO
   ```

3. **Cámbiala a:**
   ```bash
   DB_TYPE=sqlserver  # ✅ CORRECTO
   ```

4. **Guarda** el archivo
5. **Reinicia** la aplicación

---

### Opción 2: Archivo database.py

Si no tienes archivo `.env`, edita directamente:

**Archivo:** `src/main/res/config/database.py`

1. **Abre el archivo** `src/main/res/config/database.py`
2. **Busca la línea 11:**
   ```python
   DB_TYPE = os.getenv('DB_TYPE', 'mysql')
   ```

3. **Cámbiala a:**
   ```python
   DB_TYPE = 'sqlserver'  # o 'mysql' según tu caso
   ```

4. **Guarda** el archivo
5. **Reinicia** la aplicación

---

## 📝 Valores Válidos

Solo hay 2 opciones válidas para `DB_TYPE`:

- **`sqlserver`** - Para SQL Server (trabajo/producción)
- **`mysql`** - Para MySQL (casa/desarrollo)

---

## 🔍 Verificar Configuración

Después de corregir, verifica tu configuración:

```bash
# Si usas SQL Server
DB_TYPE=sqlserver

# Si usas MySQL
DB_TYPE=mysql
```

---

## 💡 Prevenir el Error

Para evitar este problema en el futuro:

1. **Usa el archivo de ejemplo** como plantilla:
   ```bash
   cp .env.example .env
   ```

2. **Edita** el nuevo archivo `.env` con tus valores
3. El archivo `.env.example` siempre tiene los valores correctos

---

## 🆘 Ayuda Adicional

Si el error persiste después de corregir el typo:

1. **Verifica** que guardaste el archivo
2. **Cierra completamente** la aplicación
3. **Reinicia** la aplicación
4. **Revisa** la consola para ver qué valor de `DB_TYPE` está leyendo

---

## 📦 Dependencias Actualizadas

Asegúrate de tener todas las dependencias instaladas:

```bash
pip install -r requirements.txt
```

**Nuevas dependencias añadidas:**
- `plotly>=5.18.0` - Gráficas interactivas
- `kaleido>=0.2.1` - Exportación de gráficas Plotly

---

## ✨ Mejoras Implementadas

Con esta actualización también se añadió:

- Detección automática de typos comunes
- Mensajes de error más útiles con soluciones
- Validación mejorada de configuración
- Dashboard moderno con animaciones fluidas

---

**Última actualización:** 2025-11-13
