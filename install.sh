#!/bin/bash
# ============================================
# SMART REPORTS - Script de Instalación Automática
# Instituto Hutchison Ports - PyQt6 Version
# ============================================

set -e  # Salir si hay error

echo "=========================================="
echo "🚀 SMART REPORTS - Instalación PyQt6"
echo "=========================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar Python
print_info "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python encontrado: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    print_success "Python encontrado: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python no encontrado. Por favor instala Python 3.11+"
    exit 1
fi

# Verificar versión de Python (debe ser 3.11+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    print_error "Se requiere Python 3.11 o superior. Versión actual: $PYTHON_VERSION"
    exit 1
fi

echo ""
print_info "Creando entorno virtual..."
if [ -d "venv" ]; then
    print_warning "El entorno virtual ya existe. Saltando creación..."
else
    $PYTHON_CMD -m venv venv
    print_success "Entorno virtual creado"
fi

echo ""
print_info "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

echo ""
print_info "Actualizando pip..."
pip install --upgrade pip
print_success "pip actualizado"

echo ""
print_info "Instalando dependencias desde requirements.txt..."
echo "Esto puede tomar varios minutos..."
pip install -r requirements.txt

echo ""
print_success "¡Todas las dependencias instaladas correctamente!"

echo ""
print_info "Verificando instalación de PyQt6..."
if $PYTHON_CMD -c "from PyQt6.QtWidgets import QApplication" 2>/dev/null; then
    print_success "PyQt6 instalado correctamente"
else
    print_error "Error al verificar PyQt6"
    exit 1
fi

echo ""
print_info "Verificando instalación de PyQt6-WebEngine..."
if $PYTHON_CMD -c "from PyQt6.QtWebEngineWidgets import QWebEngineView" 2>/dev/null; then
    print_success "PyQt6-WebEngine instalado correctamente"
else
    print_error "Error al verificar PyQt6-WebEngine"
    exit 1
fi

echo ""
print_info "Verificando otras dependencias..."
if $PYTHON_CMD -c "import pandas, numpy, openpyxl, reportlab, matplotlib, plotly" 2>/dev/null; then
    print_success "Todas las dependencias core verificadas"
else
    print_warning "Algunas dependencias podrían no estar instaladas correctamente"
fi

echo ""
print_success "=========================================="
print_success "✅ INSTALACIÓN COMPLETADA"
print_success "=========================================="
echo ""
print_info "Para ejecutar la aplicación:"
echo ""
echo "    source venv/bin/activate"
echo "    python main_pyqt6.py"
echo ""
print_warning "Nota: Recuerda activar el entorno virtual antes de ejecutar"
echo ""
print_info "Para más información, consulta: INSTALACION.md"
echo ""
