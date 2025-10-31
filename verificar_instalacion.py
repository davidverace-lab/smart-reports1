"""
Script de verificación de instalación
Smart Reports v2.1 - Hutchison Ports
"""

import sys

def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    dependencias = {
        'customtkinter': 'CustomTkinter (UI)',
        'plotly': 'Plotly (Gráficos interactivos)',
        'matplotlib': 'Matplotlib (Gráficos estáticos)',
        'pandas': 'Pandas (Procesamiento de datos)',
        'numpy': 'NumPy (Cálculos numéricos)',
        'PIL': 'Pillow (Imágenes)',
        'reportlab': 'ReportLab (PDFs)',
    }

    print("="*60)
    print("VERIFICACION DE INSTALACION - SMART REPORTS v2.1")
    print("="*60)
    print()

    todas_ok = True
    faltantes = []

    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"[OK] {nombre}")
        except ImportError:
            print(f"[FALTA] {nombre}")
            todas_ok = False
            faltantes.append(modulo)

    print()
    print("="*60)

    if todas_ok:
        print("EXITO: Todas las dependencias estan instaladas correctamente!")
        print()
        print("Puedes ejecutar la aplicacion con:")
        print("  python main.py")
    else:
        print("ADVERTENCIA: Faltan algunas dependencias")
        print()
        print("Ejecuta para instalarlas:")
        print("  pip install -r requirements.txt")
        print()
        print("Dependencias faltantes:")
        for dep in faltantes:
            print(f"  - {dep}")

    print("="*60)
    print()

    # Verificar archivos nuevos
    print("Verificando archivos nuevos...")
    print()

    import os
    archivos_nuevos = [
        'smart_reports/ui/components/top_bar.py',
        'smart_reports/ui/components/custom_tab_button.py',
        'smart_reports/ui/components/unit_selector.py',
        'smart_reports/ui/components/plotly_interactive_chart.py',
        'smart_reports/ui/panels/interactive_charts_panel.py',
    ]

    archivos_ok = True
    for archivo in archivos_nuevos:
        if os.path.exists(archivo):
            print(f"[OK] {archivo}")
        else:
            print(f"[FALTA] {archivo}")
            archivos_ok = False

    print()
    if archivos_ok:
        print("EXITO: Todos los archivos nuevos estan presentes!")
    else:
        print("ADVERTENCIA: Faltan algunos archivos")

    print("="*60)

    return todas_ok and archivos_ok


if __name__ == "__main__":
    exito = verificar_dependencias()
    sys.exit(0 if exito else 1)
