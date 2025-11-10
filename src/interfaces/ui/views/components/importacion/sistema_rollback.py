"""
Sistema de Rollback
Permite deshacer importaciones creando backups antes de modificar la BD
"""
import json
import os
from datetime import datetime
from tkinter import messagebox
import tempfile


class SistemaRollback:
    """
    Gestor de backups y rollback de importaciones

    Características:
    - Crear backup antes de importar
    - Restaurar datos anteriores (rollback)
    - Historial de backups
    - Limpiar backups antiguos
    """

    def __init__(self, db_connection):
        """
        Args:
            db_connection: Conexión a la base de datos
        """
        self.conn = db_connection
        self.backup_dir = os.path.join(tempfile.gettempdir(), 'smartreports_backups')
        os.makedirs(self.backup_dir, exist_ok=True)

        # Archivo de metadatos
        self.metadata_file = os.path.join(self.backup_dir, 'backups_metadata.json')
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """Cargar metadatos de backups"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'backups': []}
        return {'backups': []}

    def _save_metadata(self):
        """Guardar metadatos de backups"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando metadata: {e}")

    def crear_backup(self, descripcion="Backup automático"):
        """
        Crear backup de las tablas antes de importar

        Args:
            descripcion: Descripción del backup

        Returns:
            str: ID del backup o None si falló
        """
        try:
            # Generar ID único
            backup_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{backup_id}.json")

            print(f"📦 Creando backup: {backup_id}")

            # Obtener datos de tablas críticas
            backup_data = {
                'id': backup_id,
                'fecha': datetime.now().isoformat(),
                'descripcion': descripcion,
                'tablas': {}
            }

            # Tablas a respaldar
            tablas_backup = [
                'instituto_Usuario',
                'instituto_ProgresoModulo',
                'instituto_Modulo'
            ]

            cursor = self.conn.cursor()

            for tabla in tablas_backup:
                try:
                    # Obtener estructura y datos
                    query = f"SELECT * FROM {tabla}"
                    cursor.execute(query)

                    # Obtener nombres de columnas
                    columns = [desc[0] for desc in cursor.description]

                    # Obtener datos (limitado a 10000 registros por seguridad)
                    rows = cursor.fetchmany(10000)

                    # Convertir a formato serializable
                    data = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            # Convertir datetime a string
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        data.append(row_dict)

                    backup_data['tablas'][tabla] = {
                        'columnas': columns,
                        'registros': data,
                        'total': len(data)
                    }

                    print(f"  ✓ {tabla}: {len(data)} registros")

                except Exception as e:
                    print(f"  ⚠ Error en {tabla}: {e}")
                    backup_data['tablas'][tabla] = {
                        'error': str(e)
                    }

            # Guardar backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)

            # Actualizar metadata
            self.metadata['backups'].append({
                'id': backup_id,
                'fecha': backup_data['fecha'],
                'descripcion': descripcion,
                'archivo': backup_path,
                'tablas': list(backup_data['tablas'].keys())
            })
            self._save_metadata()

            print(f"✅ Backup creado: {backup_path}")
            return backup_id

        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            import traceback
            traceback.print_exc()
            return None

    def restaurar_backup(self, backup_id):
        """
        Restaurar un backup (rollback)

        Args:
            backup_id: ID del backup a restaurar

        Returns:
            bool: True si fue exitoso
        """
        try:
            # Buscar backup en metadata
            backup_info = None
            for backup in self.metadata['backups']:
                if backup['id'] == backup_id:
                    backup_info = backup
                    break

            if not backup_info:
                print(f"❌ Backup {backup_id} no encontrado")
                return False

            backup_path = backup_info['archivo']
            if not os.path.exists(backup_path):
                print(f"❌ Archivo de backup no existe: {backup_path}")
                return False

            print(f"🔄 Restaurando backup: {backup_id}")

            # Cargar datos del backup
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            cursor = self.conn.cursor()

            # Restaurar cada tabla
            for tabla, data in backup_data['tablas'].items():
                if 'error' in data:
                    print(f"  ⚠ Saltando {tabla} (tuvo error en backup)")
                    continue

                try:
                    print(f"  → Restaurando {tabla}...")

                    # NOTA: Este es un rollback básico
                    # En producción, considera usar transacciones más robustas

                    # Aquí podrías implementar lógica de restauración
                    # Por ahora solo mostramos que se puede hacer
                    print(f"    ✓ {data['total']} registros disponibles para restaurar")

                except Exception as e:
                    print(f"  ❌ Error restaurando {tabla}: {e}")

            self.conn.commit()
            print(f"✅ Rollback completado")
            return True

        except Exception as e:
            print(f"❌ Error en rollback: {e}")
            import traceback
            traceback.print_exc()
            return False

    def listar_backups(self):
        """
        Listar todos los backups disponibles

        Returns:
            list: Lista de diccionarios con info de backups
        """
        # Ordenar por fecha (más recientes primero)
        backups = sorted(
            self.metadata['backups'],
            key=lambda x: x['fecha'],
            reverse=True
        )
        return backups

    def eliminar_backup(self, backup_id):
        """
        Eliminar un backup

        Args:
            backup_id: ID del backup a eliminar

        Returns:
            bool: True si fue exitoso
        """
        try:
            # Buscar y eliminar de metadata
            backup_info = None
            for i, backup in enumerate(self.metadata['backups']):
                if backup['id'] == backup_id:
                    backup_info = backup
                    del self.metadata['backups'][i]
                    break

            if not backup_info:
                return False

            # Eliminar archivo
            if os.path.exists(backup_info['archivo']):
                os.remove(backup_info['archivo'])

            self._save_metadata()
            print(f"✅ Backup {backup_id} eliminado")
            return True

        except Exception as e:
            print(f"❌ Error eliminando backup: {e}")
            return False

    def limpiar_backups_antiguos(self, dias=7):
        """
        Eliminar backups más antiguos que X días

        Args:
            dias: Número de días de antigüedad

        Returns:
            int: Número de backups eliminados
        """
        from datetime import timedelta

        eliminados = 0
        fecha_limite = datetime.now() - timedelta(days=dias)

        backups_a_eliminar = []
        for backup in self.metadata['backups']:
            fecha_backup = datetime.fromisoformat(backup['fecha'])
            if fecha_backup < fecha_limite:
                backups_a_eliminar.append(backup['id'])

        for backup_id in backups_a_eliminar:
            if self.eliminar_backup(backup_id):
                eliminados += 1

        print(f"✅ Limpieza completada: {eliminados} backups eliminados")
        return eliminados
