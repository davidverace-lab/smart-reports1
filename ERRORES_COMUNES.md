# 🐛 Errores Comunes y Soluciones

Soluciones rapidas a problemas frecuentes.

---

## ❌ Error: ModuleNotFoundError: No module named 'customtkinter'

**Causa:** Faltan dependencias instaladas

**Solucion:**
```powershell
pip install -r requirements.txt
```

**Si falla por permisos:**
```powershell
pip install --user -r requirements.txt
```

---

## ❌ Error: ModuleNotFoundError: No module named 'src.interfaces...'

**Causa:** Imports incorrectos (YA RESUELTO en ultima version)

**Solucion:** Asegurate de tener la version mas reciente:
```powershell
git pull
```

O descarga el proyecto de nuevo.

---

## ❌ Error: UnicodeDecodeError en requirements.txt

**Causa:** Encoding de archivo (YA RESUELTO)

**Solucion:** Asegurate de tener la version mas reciente del requirements.txt

---

## ❌ Error: python no se reconoce como comando

**Causa:** Python no esta en PATH

**Solucion:**

1. Busca "Variables de entorno" en Windows
2. Edita "Path" en Variables del sistema
3. Agrega: `C:\Users\tu_usuario\AppData\Local\Programs\Python\Python311`
4. Reinicia PowerShell

**Alternativa temporal:**
```powershell
py main.py
```

---

## ❌ Error: pip no se reconoce como comando

**Solucion:**
```powershell
python -m pip install -r requirements.txt
```

---

## ❌ Error instalando pyodbc (SQL Server)

**Causa:** Falta ODBC Driver

**Solucion:** Instala ODBC Driver 17 for SQL Server:
- Descarga: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Instala
- Luego: `pip install pyodbc`

---

## ❌ Error: No se puede conectar a la base de datos

**Verificar:**

1. **La BD esta corriendo?**
   - MySQL: `net start MySQL80` (Windows)
   - SQL Server: Abre SQL Server Management Studio

2. **Las credenciales son correctas?**
   - Abre `config\database.py`
   - Verifica lineas 16-26 (SQL Server) o 31-39 (MySQL)

3. **El tipo de BD es correcto?**
   - Abre `config\database.py` linea 11
   - Debe ser `'mysql'` o `'sqlserver'`

**Si no tienes BD:** La app sigue funcionando con datos de ejemplo (mock)

---

## ❌ Error: Puerto 8050 ya esta en uso

**Solucion:** Cambia el puerto en `config\settings.py`:
```python
D3_CONFIG = {
    "http_server_port": 8051,  # Cambiar a 8051 u otro puerto libre
}
```

---

## ❌ Graficos D3.js no se muestran

**Verificar:**

1. **tkinterweb instalado?**
   ```powershell
   pip install tkinterweb
   ```

2. **Revisa la consola** cuando ejecutas `python main.py`
   - Debe decir: "Cargando dashboards gerenciales..."
   - Si hay errores 404, reportalos

3. **Alternativa:** Usa tkhtmlview
   ```powershell
   pip install tkhtmlview matplotlib
   ```

---

## ❌ Error: Access denied / Permission denied

**Solucion:**

1. **Ejecuta PowerShell como Administrador**
2. O instala con `--user`:
   ```powershell
   pip install --user -r requirements.txt
   ```

---

## ❌ La ventana se abre y se cierra inmediatamente

**Causa:** Error en la conexion a BD o credenciales incorrectas

**Solucion:**

1. Ejecuta desde PowerShell (NO hacer doble clic en main.py)
2. Lee el error en la consola
3. Si es de BD, revisa `config\database.py`

---

## ❌ Error: No module named 'config.settings'

**Causa:** Ejecutando desde carpeta incorrecta

**Solucion:** Asegurate de estar en la carpeta raiz:
```powershell
cd C:\Users\tu_usuario\OneDrive\Documentos\smart-reports1-main\smart-reports1-main
python main.py
```

---

## ✅ Verificacion Completa

Ejecuta este script para diagnosticar TODO:

```powershell
python verificar_dependencias.py
```

Te dira exactamente que falta.

---

## 📚 Mas Ayuda

- `INSTALACION_WINDOWS.md` - Guia completa para Windows
- `INSTALACION_RAPIDA.md` - Guia general
- `GUIA_CONFIGURACION.md` - Configuracion detallada BD
- `README.md` - Documentacion completa

---

## 💬 Reporte de Bugs

Si ninguna solucion funciona, crea un issue con:

1. Version de Python: `python --version`
2. Sistema operativo: Windows 10/11
3. Error completo (copia todo el texto rojo)
4. Que intentaste hacer
5. Comandos que ejecutaste

---

**v2.0.1** - Errores Comunes Actualizados
