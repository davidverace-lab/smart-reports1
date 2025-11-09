"""
Script para importar usuarios desde Excel a CSV
Convierte datos de Excel a formato CSV para importación masiva a instituto_Usuario
"""

import pandas as pd
import hashlib
from datetime import datetime
from pathlib import Path


def leer_excel_usuarios(archivo_excel):
    """
    Lee archivo Excel con usuarios

    Args:
        archivo_excel: Ruta al archivo Excel

    Returns:
        DataFrame de pandas con los usuarios
    """
    print(f"📖 Leyendo archivo: {archivo_excel}")

    # Leer Excel
    df = pd.read_excel(archivo_excel)

    print(f"✅ Leídos {len(df)} registros")
    print(f"📋 Columnas encontradas: {list(df.columns)}")

    return df


def mapear_a_estructura_instituto(df):
    """
    Mapea columnas del Excel a estructura de instituto_Usuario

    Estructura esperada en instituto_Usuario:
    - UserId (VARCHAR 50) - REQUERIDO
    - IdUnidadDeNegocio (INT)
    - IdDepartamento (INT)
    - IdRol (INT)
    - NombreCompleto (VARCHAR 255)
    - UserEmail (VARCHAR 255)
    - PasswordHash (VARCHAR 255)
    - TipoDeCorreo (VARCHAR 50)
    - Nivel (VARCHAR 50)
    - Division (VARCHAR 100)
    - Position (VARCHAR 100)
    - UserStatus (VARCHAR 50)
    - Grupo (VARCHAR 100)
    - Ubicacion (VARCHAR 100)
    - Activo (TINYINT 1)
    """

    # Mapeo de columnas (ajustar según tu Excel)
    mapeo_columnas = {
        # Excel → Tabla instituto_Usuario
        'UserId': 'UserId',
        'User Id': 'UserId',
        'ID': 'UserId',
        'Email': 'UserEmail',
        'Mail': 'UserEmail',
        'Email address': 'UserEmail',
        'Nombre': 'NombreCompleto',
        'Full Name': 'NombreCompleto',
        'Display name': 'NombreCompleto',
        'Account enabled': 'UserStatus',
        'On-premises sync enabled': 'TipoDeCorreo',
        'User type': 'Nivel',
        'Department': 'Division',
        'Job title': 'Position',
        'Office location': 'Ubicacion',
        'City': 'Ubicacion',
        'Manager': 'Grupo',
        'Assigned licenses': 'Grupo',
    }

    # Renombrar columnas
    df_mapped = df.copy()
    for col_excel, col_db in mapeo_columnas.items():
        if col_excel in df_mapped.columns:
            df_mapped.rename(columns={col_excel: col_db}, inplace=True)

    # Asegurar columnas requeridas
    columnas_requeridas = [
        'UserId',
        'UserEmail',
        'NombreCompleto',
        'UserStatus',
        'TipoDeCorreo',
        'Nivel',
        'Division',
        'Position',
        'Grupo',
        'Ubicacion',
        'Activo',
        'PasswordHash',
        'IdUnidadDeNegocio',
        'IdDepartamento',
        'IdRol'
    ]

    for col in columnas_requeridas:
        if col not in df_mapped.columns:
            if col == 'UserId':
                # UserId es crítico
                raise ValueError(f"❌ Columna '{col}' es REQUERIDA y no se encontró")
            elif col == 'Activo':
                # Determinar según UserStatus
                if 'UserStatus' in df_mapped.columns:
                    df_mapped['Activo'] = df_mapped['UserStatus'].apply(
                        lambda x: 1 if str(x).lower() in ['true', 'yes', 'activo', '1', 'active'] else 0
                    )
                else:
                    df_mapped['Activo'] = 1  # Por defecto activo
            elif col == 'PasswordHash':
                # Generar hash temporal (deben cambiar en primer login)
                df_mapped['PasswordHash'] = df_mapped.apply(
                    lambda row: hashlib.sha256(f"{row.get('UserId', 'temp')}123".encode()).hexdigest(),
                    axis=1
                )
            elif col in ['IdUnidadDeNegocio', 'IdDepartamento', 'IdRol']:
                df_mapped[col] = None  # Se asignarán después
            else:
                df_mapped[col] = ''  # Valor vacío por defecto

    return df_mapped


def generar_csv_importacion(df, archivo_salida='usuarios_importacion.csv'):
    """
    Genera CSV listo para importación a MySQL

    Args:
        df: DataFrame con usuarios mapeados
        archivo_salida: Nombre del archivo CSV de salida
    """

    # Orden de columnas según tabla instituto_Usuario
    columnas_finales = [
        'UserId',
        'IdUnidadDeNegocio',
        'IdDepartamento',
        'IdRol',
        'NombreCompleto',
        'UserEmail',
        'PasswordHash',
        'TipoDeCorreo',
        'Nivel',
        'Division',
        'Position',
        'UserStatus',
        'Grupo',
        'Ubicacion',
        'Activo'
    ]

    # Filtrar solo usuarios activos (opcional)
    df_activos = df[df['Activo'] == 1].copy()

    print(f"\n📊 Estadísticas:")
    print(f"   Total registros: {len(df)}")
    print(f"   Usuarios activos: {len(df_activos)}")
    print(f"   Usuarios inactivos: {len(df) - len(df_activos)}")

    # Seleccionar columnas finales
    df_final = df_activos[columnas_finales].copy()

    # Limpiar valores
    df_final = df_final.fillna('')  # Reemplazar NaN por string vacío
    df_final = df_final.replace({'None': '', 'nan': ''})  # Limpiar strings

    # Guardar CSV
    df_final.to_csv(archivo_salida, index=False, encoding='utf-8-sig')

    print(f"\n✅ CSV generado: {archivo_salida}")
    print(f"   Registros: {len(df_final)}")
    print(f"   Columnas: {len(columnas_finales)}")

    return archivo_salida


def generar_script_importacion_sql(csv_file):
    """
    Genera script SQL para importar el CSV

    Args:
        csv_file: Ruta al archivo CSV
    """
    script_sql = f"""-- ============================================
-- SCRIPT DE IMPORTACIÓN MASIVA DE USUARIOS
-- Archivo CSV: {csv_file}
-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================

USE tngcore;

-- ============================================
-- OPCIÓN 1: LOAD DATA INFILE (MÁS RÁPIDO)
-- ============================================

-- Habilitar cargas locales (si es necesario)
SET GLOBAL local_infile = 1;

-- Cargar CSV
LOAD DATA LOCAL INFILE '{Path(csv_file).absolute()}'
INTO TABLE instituto_Usuario
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS
(UserId, @IdUnidadDeNegocio, @IdDepartamento, @IdRol,
 NombreCompleto, UserEmail, PasswordHash, TipoDeCorreo,
 Nivel, Division, Position, UserStatus, Grupo, Ubicacion, Activo)
SET
    IdUnidadDeNegocio = NULLIF(@IdUnidadDeNegocio, ''),
    IdDepartamento = NULLIF(@IdDepartamento, ''),
    IdRol = NULLIF(@IdRol, ''),
    FechaCreacion = NOW();

-- ============================================
-- OPCIÓN 2: MYSQL WORKBENCH (GUI)
-- ============================================

-- 1. Clic derecho en tabla instituto_Usuario
-- 2. "Table Data Import Wizard"
-- 3. Seleccionar archivo: {csv_file}
-- 4. Mapear columnas automáticamente
-- 5. Importar

-- ============================================
-- OPCIÓN 3: SCRIPT PYTHON
-- ============================================

-- Ejecutar: python database_manager_instituto.py

-- ============================================
-- VERIFICACIÓN POST-IMPORTACIÓN
-- ============================================

-- Contar usuarios importados
SELECT COUNT(*) AS TotalUsuarios FROM instituto_Usuario;

-- Ver primeros registros
SELECT * FROM instituto_Usuario LIMIT 10;

-- Ver usuarios por estado
SELECT
    UserStatus,
    COUNT(*) AS Total
FROM instituto_Usuario
GROUP BY UserStatus;

-- Ver usuarios sin unidad de negocio (pendientes de asignar)
SELECT
    UserId,
    NombreCompleto,
    UserEmail
FROM instituto_Usuario
WHERE IdUnidadDeNegocio IS NULL
LIMIT 10;

-- ============================================
-- POST-PROCESAMIENTO RECOMENDADO
-- ============================================

-- Asignar unidad de negocio por dominio de email
UPDATE instituto_Usuario
SET IdUnidadDeNegocio = CASE
    WHEN UserEmail LIKE '%@icave.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'ICAVE')
    WHEN UserEmail LIKE '%@eit.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'EIT')
    WHEN UserEmail LIKE '%@lct.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'LCT')
    WHEN UserEmail LIKE '%@timsa.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'TIMSA')
    WHEN UserEmail LIKE '%@hpmx.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'HPMX')
    WHEN UserEmail LIKE '%@tng.%' THEN (SELECT IdUnidadDeNegocio FROM instituto_UnidadDeNegocio WHERE Codigo = 'TNG')
    ELSE IdUnidadDeNegocio
END
WHERE IdUnidadDeNegocio IS NULL;

-- Asignar rol por defecto (Usuario)
UPDATE instituto_Usuario
SET IdRol = (SELECT IdRol FROM instituto_Rol WHERE NombreRol = 'Usuario')
WHERE IdRol IS NULL;

-- ============================================
-- RESULTADO FINAL
-- ============================================

SELECT '✅ Importación completada!' AS Resultado;

SELECT
    'Usuarios totales:' AS Metrica,
    COUNT(*) AS Valor
FROM instituto_Usuario

UNION ALL

SELECT
    'Usuarios activos:',
    COUNT(*)
FROM instituto_Usuario
WHERE Activo = 1

UNION ALL

SELECT
    'Con unidad asignada:',
    COUNT(*)
FROM instituto_Usuario
WHERE IdUnidadDeNegocio IS NOT NULL

UNION ALL

SELECT
    'Con departamento asignado:',
    COUNT(*)
FROM instituto_Usuario
WHERE IdDepartamento IS NOT NULL;
"""

    archivo_sql = csv_file.replace('.csv', '_importacion.sql')
    with open(archivo_sql, 'w', encoding='utf-8') as f:
        f.write(script_sql)

    print(f"✅ Script SQL generado: {archivo_sql}")

    return archivo_sql


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def procesar_excel_a_csv(archivo_excel=None):
    """
    Función principal que procesa Excel y genera CSV

    Args:
        archivo_excel: Ruta al archivo Excel. Si no se proporciona, busca en el directorio actual
    """
    print("=" * 60)
    print("IMPORTACIÓN MASIVA DE USUARIOS")
    print("Excel → CSV → instituto_Usuario")
    print("=" * 60)

    # Buscar archivo Excel si no se proporciona
    if archivo_excel is None:
        # Buscar archivos Excel en el directorio actual
        archivos_excel = list(Path('.').glob('*.xlsx')) + list(Path('.').glob('*.xls'))

        if not archivos_excel:
            print("\n❌ No se encontraron archivos Excel (.xlsx, .xls)")
            print("\n💡 Uso:")
            print("   1. Coloca tu archivo Excel en esta carpeta")
            print("   2. Ejecuta: python importar_usuarios_excel.py")
            print("\n   O especifica la ruta:")
            print("   python importar_usuarios_excel.py /ruta/al/archivo.xlsx")
            return

        archivo_excel = archivos_excel[0]
        print(f"\n📁 Archivo encontrado: {archivo_excel}")

    try:
        # 1. Leer Excel
        df = leer_excel_usuarios(archivo_excel)

        # Mostrar muestra de datos
        print("\n📋 Muestra de datos originales:")
        print(df.head(3).to_string())

        # 2. Mapear a estructura
        print("\n🔄 Mapeando a estructura instituto_Usuario...")
        df_mapped = mapear_a_estructura_instituto(df)

        # Mostrar muestra mapeada
        print("\n📋 Muestra de datos mapeados:")
        cols_importantes = ['UserId', 'NombreCompleto', 'UserEmail', 'UserStatus', 'Activo']
        cols_disponibles = [c for c in cols_importantes if c in df_mapped.columns]
        print(df_mapped[cols_disponibles].head(3).to_string())

        # 3. Generar CSV
        print("\n💾 Generando CSV...")
        csv_file = generar_csv_importacion(df_mapped)

        # 4. Generar script SQL
        print("\n📝 Generando script SQL...")
        sql_file = generar_script_importacion_sql(csv_file)

        # Resumen final
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print(f"\n📄 Archivos generados:")
        print(f"   1. CSV: {csv_file}")
        print(f"   2. SQL: {sql_file}")

        print(f"\n📊 Próximos pasos:")
        print(f"   1. Revisar el CSV generado")
        print(f"   2. Importar con MySQL Workbench o ejecutar SQL")
        print(f"   3. Asignar unidades de negocio y departamentos")

        print(f"\n🔧 Opciones de importación:")
        print(f"   A) MySQL Workbench: Table Data Import Wizard")
        print(f"   B) Línea de comandos:")
        print(f"      mysql -u root -p tngcore < {sql_file}")
        print(f"   C) Python:")
        print(f"      from database_manager_instituto import InstitutoSmartReportsDB")

        print("\n" + "=" * 60)

        return csv_file, sql_file

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# EJECUTAR
# =============================================================================

if __name__ == "__main__":
    import sys

    # Permitir pasar archivo Excel como argumento
    archivo_excel = sys.argv[1] if len(sys.argv) > 1 else None

    procesar_excel_a_csv(archivo_excel)
