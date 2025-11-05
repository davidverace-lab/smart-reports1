-- Script para crear la tabla Instituto_Soporte
-- Almacena los registros de soporte brindado a usuarios

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Instituto_Soporte]') AND type in (N'U'))
BEGIN
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

    -- Índice para búsquedas rápidas por UserId
    CREATE INDEX IX_Instituto_Soporte_UserId ON Instituto_Soporte(UserId)

    -- Índice para ordenar por fecha
    CREATE INDEX IX_Instituto_Soporte_FechaRegistro ON Instituto_Soporte(FechaRegistro DESC)

    PRINT 'Tabla Instituto_Soporte creada exitosamente'
END
ELSE
BEGIN
    PRINT 'La tabla Instituto_Soporte ya existe'
END
