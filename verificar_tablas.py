"""
Script para verificar qué tablas existen en la base de datos
"""
from database.connection import DatabaseConnection

def verificar_tablas():
    """Verifica qué tablas existen en la BD"""
    db = DatabaseConnection()
    conn = db.connect()
    cursor = conn.cursor()

    # Tablas que buscamos
    tablas_base = [
        'Usuario', 'Modulo', 'ProgresoModulo', 'Departamento',
        'UnidadDeNegocio', 'ResultadoEvaluacion', 'Evaluacion', 'Rol'
    ]

    # Prefijos posibles
    prefijos = ['Instituto.', 'Instituto_', 'dbo.Instituto_', 'dbo.', '']

    print("\n" + "="*70)
    print("VERIFICACIÓN DE TABLAS EN LA BASE DE DATOS")
    print("="*70 + "\n")

    tablas_encontradas = {}

    for tabla in tablas_base:
        encontrada = False
        for prefijo in prefijos:
            nombre_completo = f"{prefijo}{tabla}"
            try:
                cursor.execute(f"SELECT TOP 1 1 FROM {nombre_completo}")
                print(f"✓ ENCONTRADA: {nombre_completo}")
                tablas_encontradas[tabla] = nombre_completo
                encontrada = True
                break
            except Exception as e:
                continue

        if not encontrada:
            print(f"✗ NO ENCONTRADA: {tabla}")
            tablas_encontradas[tabla] = None

    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70 + "\n")

    if any(v is None for v in tablas_encontradas.values()):
        print("⚠️  ADVERTENCIA: Algunas tablas NO existen en la base de datos")
        print("\nTablas faltantes:")
        for tabla, nombre in tablas_encontradas.items():
            if nombre is None:
                print(f"  - {tabla}")

        print("\n💡 SOLUCIÓN:")
        print("  1. Ejecuta el script de creación de tablas del esquema Instituto")
        print("  2. O verifica que la conexión a la BD sea correcta")
        print("  3. O contacta al administrador de BD")
    else:
        print("✓ Todas las tablas necesarias existen")

        print("\nMapeo de tablas:")
        for tabla, nombre in tablas_encontradas.items():
            print(f"  {tabla:20} -> {nombre}")

    conn.close()

    return tablas_encontradas

if __name__ == "__main__":
    try:
        verificar_tablas()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Verifica:")
        print("  1. Que el servidor de BD esté corriendo")
        print("  2. Que la configuración en config/settings.py sea correcta")
        print("  3. Que tengas permisos para acceder a la BD")
