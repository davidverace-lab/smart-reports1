@echo off
echo ========================================
echo LIMPIEZA DE CACHE DE PYTHON
echo ========================================
echo.
echo Eliminando archivos __pycache__ y .pyc...
echo.

for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo.
echo ✅ Cache limpiado correctamente
echo.
pause
