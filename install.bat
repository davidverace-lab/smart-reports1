@echo off
REM ============================================
REM SMART REPORTS - Script de Instalación Automática
REM Instituto Hutchison Ports - PyQt6 Version
REM ============================================

echo ==========================================
echo 🚀 SMART REPORTS - Instalación PyQt6
echo ==========================================
echo.

REM Verificar Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Por favor instala Python 3.11+
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python encontrado
echo.

REM Crear entorno virtual
echo [INFO] Creando entorno virtual...
if exist venv (
    echo [WARNING] El entorno virtual ya existe. Saltando creación...
) else (
    python -m venv venv
    echo [SUCCESS] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [SUCCESS] Entorno virtual activado
echo.

REM Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip
echo [SUCCESS] pip actualizado
echo.

REM Instalar dependencias
echo [INFO] Instalando dependencias desde requirements.txt...
echo Esto puede tomar varios minutos...
pip install -r requirements.txt
echo.
echo [SUCCESS] Todas las dependencias instaladas correctamente
echo.

REM Verificar instalación
echo [INFO] Verificando instalación de PyQt6...
python -c "from PyQt6.QtWidgets import QApplication" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Error al verificar PyQt6
    pause
    exit /b 1
)
echo [SUCCESS] PyQt6 instalado correctamente
echo.

echo [INFO] Verificando instalación de PyQt6-WebEngine...
python -c "from PyQt6.QtWebEngineWidgets import QWebEngineView" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Error al verificar PyQt6-WebEngine
    pause
    exit /b 1
)
echo [SUCCESS] PyQt6-WebEngine instalado correctamente
echo.

echo [INFO] Verificando otras dependencias...
python -c "import pandas, numpy, openpyxl, reportlab, matplotlib, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Algunas dependencias podrían no estar instaladas correctamente
) else (
    echo [SUCCESS] Todas las dependencias core verificadas
)
echo.

echo ==========================================
echo ✅ INSTALACIÓN COMPLETADA
echo ==========================================
echo.
echo Para ejecutar la aplicación:
echo.
echo     venv\Scripts\activate.bat
echo     python main_pyqt6.py
echo.
echo [WARNING] Nota: Recuerda activar el entorno virtual antes de ejecutar
echo.
echo Para más información, consulta: INSTALACION.md
echo.
pause
