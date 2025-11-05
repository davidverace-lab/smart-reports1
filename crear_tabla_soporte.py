"""
Script para crear la tabla Instituto_Soporte en la base de datos
Ejecuta automáticamente el script SQL create_soporte_table.sql
"""
import pyodbc
from config.db_config import get_db_connection

def crear_tabla_soporte():
    """Crear tabla Instituto_Soporte si no existe"""
    print("="*60)
    print("CREACIÓN DE TABLA INSTITUTO_SOPORTE")
    print("="*60)

    try:
        # Conectar a la base de datos
        print("\n[1/3] Conectando a la base de datos...")
        conn = get_db_connection()
        cursor = conn.cursor()
        print("✓ Conexión exitosa")

        # Verificar si la tabla ya existe
        print("\n[2/3] Verificando si la tabla existe...")
        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = 'Instituto_Soporte'
        """)

        tabla_existe = cursor.fetchone()[0] > 0

        if tabla_existe:
            print("⚠ La tabla 'Instituto_Soporte' ya existe")
            respuesta = input("\n¿Desea recrearla? (se perderán todos los datos) [s/N]: ")
            if respuesta.lower() != 's':
                print("\nOperación cancelada")
                return

            print("\nEliminando tabla existente...")
            cursor.execute("DROP TABLE Instituto_Soporte")
            conn.commit()
            print("✓ Tabla eliminada")

        # Crear la tabla
        print("\n[3/3] Creando tabla Instituto_Soporte...")
        cursor.execute("""
            CREATE TABLE [dbo].[Instituto_Soporte] (
                [SoporteId] INT IDENTITY(1,1) PRIMARY KEY,
                [UserId] VARCHAR(50) NOT NULL,
                [Asunto] NVARCHAR(200) NOT NULL,
                [Descripcion] NVARCHAR(MAX) NOT NULL,
                [Categoria] NVARCHAR(50) NOT NULL,
                [FechaRegistro] DATETIME NOT NULL DEFAULT GETDATE(),
                [RegistradoPor] VARCHAR(50) NULL,
                CONSTRAINT FK_Instituto_Soporte_Usuario FOREIGN KEY (UserId)
                    REFERENCES Instituto_Usuario(UserId)
            )
        """)

        # Crear índices
        print("  - Creando índice por UserId...")
        cursor.execute("""
            CREATE INDEX IX_Instituto_Soporte_UserId
            ON Instituto_Soporte(UserId)
        """)

        print("  - Creando índice por FechaRegistro...")
        cursor.execute("""
            CREATE INDEX IX_Instituto_Soporte_FechaRegistro
            ON Instituto_Soporte(FechaRegistro DESC)
        """)

        conn.commit()
        print("✓ Tabla creada exitosamente")

        # Verificar creación
        cursor.execute("""
            SELECT
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS c
            WHERE c.TABLE_NAME = 'Instituto_Soporte'
            ORDER BY c.ORDINAL_POSITION
        """)

        print("\n" + "="*60)
        print("ESTRUCTURA DE LA TABLA")
        print("="*60)
        print(f"{'Columna':<25} {'Tipo':<15} {'Longitud':<10}")
        print("-"*60)

        for row in cursor.fetchall():
            columna = row[0]
            tipo = row[1]
            longitud = row[2] if row[2] else '-'
            print(f"{columna:<25} {tipo:<15} {str(longitud):<10}")

        print("\n✓ Tabla 'Instituto_Soporte' creada exitosamente")
        print("\nAhora puedes usar la función de Registro de Soporte en la aplicación.")

        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print(f"\n✗ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    crear_tabla_soporte()
    input("\nPresiona Enter para salir...")
