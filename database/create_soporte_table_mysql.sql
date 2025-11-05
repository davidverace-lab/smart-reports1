-- Script para crear la tabla Instituto_Soporte en MySQL
-- Almacena los registros de soporte brindado a usuarios

-- Eliminar tabla si existe (solo para desarrollo)
-- DROP TABLE IF EXISTS Instituto_Soporte;

-- Crear tabla
CREATE TABLE IF NOT EXISTS Instituto_Soporte (
    SoporteId INT AUTO_INCREMENT PRIMARY KEY,
    UserId VARCHAR(50) NOT NULL,
    Asunto VARCHAR(200) NOT NULL,
    Descripcion TEXT NOT NULL,
    Categoria VARCHAR(50) NOT NULL,
    FechaRegistro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    RegistradoPor VARCHAR(50) NULL,
    CONSTRAINT FK_Instituto_Soporte_Usuario
        FOREIGN KEY (UserId) REFERENCES Instituto_Usuario(UserId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Crear índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS IX_Instituto_Soporte_UserId
    ON Instituto_Soporte(UserId);

CREATE INDEX IF NOT EXISTS IX_Instituto_Soporte_FechaRegistro
    ON Instituto_Soporte(FechaRegistro DESC);

-- Verificar creación
SELECT 'Tabla Instituto_Soporte creada exitosamente' AS Resultado;

-- Mostrar estructura de la tabla
DESCRIBE Instituto_Soporte;
