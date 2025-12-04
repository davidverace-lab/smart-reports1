"""
Sistema de Caché Simple para Optimización de Rendimiento

OPTIMIZACIÓN: Evita queries repetidas innecesarias

Casos de uso:
- Datos de configuración (cambian raramente)
- Listas de unidades de negocio
- Estadísticas que se recalculan cada 5 minutos
"""
from functools import wraps
from typing import Any, Callable, Optional
from datetime import datetime, timedelta
import threading


class CacheManager:
    """
    Gestor de caché en memoria con TTL (Time To Live)

    Características:
    - Caché en memoria (dict)
    - TTL configurable por entrada
    - Thread-safe
    - Decorador @cached para funciones

    Uso:
        cache = CacheManager()

        @cache.cached(ttl_seconds=300)  # 5 minutos
        def get_business_units():
            # Query pesada
            return cursor.fetchall()
    """

    def __init__(self):
        """Inicializar gestor de caché"""
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        Obtener valor del caché

        Args:
            key: Clave única

        Returns:
            Valor cacheado o None si expiró/no existe
        """
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]

            # Verificar si expiró
            if entry['expires_at'] and datetime.now() > entry['expires_at']:
                del self._cache[key]
                return None

            return entry['value']

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """
        Guardar valor en caché

        Args:
            key: Clave única
            value: Valor a cachear
            ttl_seconds: Tiempo de vida en segundos (None = infinito)
        """
        with self._lock:
            expires_at = None
            if ttl_seconds:
                expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': datetime.now()
            }

    def delete(self, key: str):
        """Eliminar entrada del caché"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self):
        """Limpiar todo el caché"""
        with self._lock:
            self._cache.clear()

    def cached(self, ttl_seconds: int = 300, key_prefix: str = ''):
        """
        Decorador para cachear resultados de funciones

        Args:
            ttl_seconds: Tiempo de vida del caché (default: 5 minutos)
            key_prefix: Prefijo para la clave de caché

        Uso:
            @cache_manager.cached(ttl_seconds=600)
            def get_statistics():
                # Query pesada
                return results

        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generar clave única basada en función y argumentos
                cache_key = self._generate_cache_key(func, args, kwargs, key_prefix)

                # Intentar obtener del caché
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Ejecutar función y cachear resultado
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl_seconds)

                return result

            # Agregar método para invalidar caché
            wrapper.invalidate_cache = lambda: self.delete(
                self._generate_cache_key(func, (), {}, key_prefix)
            )

            return wrapper

        return decorator

    @staticmethod
    def _generate_cache_key(func: Callable, args: tuple, kwargs: dict, prefix: str = '') -> str:
        """Generar clave única para caché"""
        func_name = f"{func.__module__}.{func.__name__}"
        args_str = str(args) + str(sorted(kwargs.items()))

        key = f"{prefix}:{func_name}:{hash(args_str)}"
        return key

    def get_stats(self) -> dict:
        """Obtener estadísticas del caché"""
        with self._lock:
            total_entries = len(self._cache)
            expired = 0
            active = 0

            now = datetime.now()
            for entry in self._cache.values():
                if entry['expires_at'] and now > entry['expires_at']:
                    expired += 1
                else:
                    active += 1

            return {
                'total_entries': total_entries,
                'active': active,
                'expired': expired,
                'memory_keys': list(self._cache.keys())
            }


# Instancia global del gestor de caché
_global_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Obtener instancia global del gestor de caché (Singleton)"""
    global _global_cache_manager
    if _global_cache_manager is None:
        _global_cache_manager = CacheManager()
    return _global_cache_manager


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Ejemplo de uso
    cache = get_cache_manager()

    # Decorador
    @cache.cached(ttl_seconds=10)
    def expensive_query():
        print("Ejecutando query pesada...")
        import time
        time.sleep(2)  # Simular query lenta
        return [1, 2, 3, 4, 5]

    # Primera llamada - ejecuta query
    print("Primera llamada:")
    result1 = expensive_query()
    print(f"Resultado: {result1}")

    # Segunda llamada - usa caché
    print("\nSegunda llamada (debería ser instantánea):")
    result2 = expensive_query()
    print(f"Resultado: {result2}")

    # Estadísticas
    print(f"\nEstadísticas del caché: {cache.get_stats()}")

    # Invalidar caché manualmente
    expensive_query.invalidate_cache()
    print("\nCaché invalidado")

    # Tercera llamada - ejecuta query nuevamente
    print("\nTercera llamada (después de invalidar):")
    result3 = expensive_query()
    print(f"Resultado: {result3}")
