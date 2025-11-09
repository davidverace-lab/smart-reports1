#!/usr/bin/env python3
"""
Test simple del motor matplotlib
"""
from nucleo.servicios.motor_graficos_matplotlib import MotorGraficosMatplotlib
import tkinter as tk

print("=" * 60)
print("TEST MOTOR MATPLOTLIB")
print("=" * 60)

# Datos de prueba
datos_barras = {
    'labels': ['A', 'B', 'C', 'D'],
    'values': [10, 20, 15, 25]
}

try:
    # Crear ventana temporal
    root = tk.Tk()
    root.title("Test Matplotlib")

    motor = MotorGraficosMatplotlib()

    print("\n1. Probando gráfico de barras...")
    canvas = motor.crear_grafico_barras(root, datos_barras, 'dark', 'Test')

    if canvas:
        print("   ✅ Canvas creado exitosamente")
        canvas.get_tk_widget().pack(fill='both', expand=True)
        print("   ✅ Widget empaquetado correctamente")
        print("\n✅ MOTOR MATPLOTLIB FUNCIONA CORRECTAMENTE")
        print("\nCerrando ventana de prueba en 3 segundos...")
        root.after(3000, root.destroy)
        root.mainloop()
    else:
        print("   ❌ No se pudo crear canvas")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
