-- Base de datos reestructurada para producción (MySQL 5.7+)
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- ================================================
-- CREAR BASE DE DATOS Y USAR
-- ================================================
CREATE DATABASE IF NOT EXISTS `ecommerce` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ecommerce`;

-- ================================================
-- TABLA: USUARIOS
-- ================================================
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `email` VARCHAR(150) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `verify` BOOLEAN DEFAULT FALSE,
  `admin` BOOLEAN DEFAULT FALSE,
  `token` VARCHAR(64) UNIQUE,
  `token_expiry` DATETIME,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_email` (`email`),
  KEY `idx_username` (`username`),
  KEY `idx_admin` (`admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: CATEGORIAS
-- ================================================
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL UNIQUE,
  `descripcion` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: PRODUCTOS
-- ================================================
CREATE TABLE IF NOT EXISTS `productos` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT,
  `precio` DECIMAL(10, 2) NOT NULL,
  `stock` INT UNSIGNED NOT NULL DEFAULT 0,
  `imagen_url` VARCHAR(255),
  `categoria_id` INT UNSIGNED,
  `activo` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_categoria_id` (`categoria_id`),
  KEY `idx_nombre` (`nombre`),
  KEY `idx_activo` (`activo`),
  CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: CARRITO
-- ================================================
CREATE TABLE IF NOT EXISTS `carrito` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `usuario_id` INT UNSIGNED NOT NULL,
  `producto_id` INT UNSIGNED NOT NULL,
  `cantidad` INT UNSIGNED NOT NULL DEFAULT 1,
  `imagen_url` VARCHAR(255),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uk_usuario_producto` (`usuario_id`, `producto_id`),
  KEY `idx_usuario_id` (`usuario_id`),
  KEY `idx_producto_id` (`producto_id`),
  CONSTRAINT `fk_carrito_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_carrito_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: DIRECCION_ENVIO
-- ================================================
CREATE TABLE IF NOT EXISTS `direccion_envio` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `usuario_id` INT UNSIGNED NOT NULL,
  `direccion` VARCHAR(255) NOT NULL,
  `colonia` VARCHAR(150) NOT NULL,
  `ciudad` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(100) NOT NULL,
  `codigo_postal` VARCHAR(10) NOT NULL,
  `pais` VARCHAR(100) DEFAULT 'México',
  `telefono` VARCHAR(20) NOT NULL,
  `referencias` TEXT,
  `es_principal` BOOLEAN DEFAULT FALSE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_usuario_id` (`usuario_id`),
  CONSTRAINT `fk_direccion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: COMPRAS (Pedidos)
-- ================================================
CREATE TABLE IF NOT EXISTS `compras` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `usuario_id` INT UNSIGNED NOT NULL,
  `direccion_envio_id` INT UNSIGNED NOT NULL,
  `total` DECIMAL(10, 2) NOT NULL,
  `estado` ENUM('pendiente', 'pagado', 'procesando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
  `metodo_pago` VARCHAR(50) NOT NULL DEFAULT 'tarjeta',
  `stripe_session_id` VARCHAR(255),
  `paypal_transaction_id` VARCHAR(255),
  `notas` TEXT,
  `fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_usuario_id` (`usuario_id`),
  KEY `idx_estado` (`estado`),
  KEY `idx_fecha` (`fecha`),
  KEY `idx_metodo_pago` (`metodo_pago`),
  CONSTRAINT `fk_compra_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_compra_direccion` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direccion_envio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: DETALLE_COMPRA
-- ================================================
CREATE TABLE IF NOT EXISTS `detalle_compra` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `compra_id` INT UNSIGNED NOT NULL,
  `producto_id` INT UNSIGNED NOT NULL,
  `cantidad` INT UNSIGNED NOT NULL,
  `precio_unitario` DECIMAL(10, 2) NOT NULL,
  `subtotal` DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY `idx_compra_id` (`compra_id`),
  KEY `idx_producto_id` (`producto_id`),
  CONSTRAINT `fk_detalle_compra` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_detalle_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: ENVIOS
-- ================================================
CREATE TABLE IF NOT EXISTS `envios` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `compra_id` INT UNSIGNED NOT NULL,
  `usuario_id` INT UNSIGNED NOT NULL,
  `direccion_envio_id` INT UNSIGNED NOT NULL,
  `numero_rastreo` VARCHAR(150),
  `estado` ENUM('pendiente', 'procesado', 'aceptado', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
  `observaciones` TEXT,
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_compra_id` (`compra_id`),
  KEY `idx_usuario_id` (`usuario_id`),
  KEY `idx_estado` (`estado`),
  KEY `idx_numero_rastreo` (`numero_rastreo`),
  CONSTRAINT `fk_envio_compra` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_envio_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_envio_direccion` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direccion_envio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- TABLA: ACTIVITY_LOGS
-- ================================================
CREATE TABLE IF NOT EXISTS `activity_logs` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT UNSIGNED,
  `action` VARCHAR(255) NOT NULL,
  `ip_address` VARCHAR(45),
  `extra_info` JSON,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY `idx_user_id` (`user_id`),
  KEY `idx_timestamp` (`timestamp`),
  CONSTRAINT `fk_activity_user` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================
-- DATOS DE EJEMPLO
-- ================================================

-- Categorías
INSERT IGNORE INTO `categorias` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Ropa Deportiva', 'Prendas para deportes y ejercicio'),
(2, 'Accesorios', 'Accesorios y complementos deportivos'),
(3, 'Calzado', 'Zapatos y calzado deportivo');

-- Productos
INSERT IGNORE INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `imagen_url`, `categoria_id`, `activo`) VALUES
(1, 'Camiseta Deportiva', 'Camiseta ligera y transpirable para deportes', 29.99, 50, '', 1, TRUE),
(2, 'Pantalones Cortos Deportivos', 'Pantalones cortos cómodos para correr o entrenar', 24.99, 40, '', 1, TRUE),
(3, 'Sudadera con Capucha', 'Sudadera con capucha para calentamiento y frío', 49.99, 30, '', 1, TRUE),
(4, 'Calcetas Deportivas', 'Calcetas que absorben el sudor para mayor comodidad', 9.99, 100, '', 1, TRUE),
(5, 'Chaqueta Cortaviento', 'Chaqueta ligera resistente al viento para exteriores', 59.99, 20, '', 1, TRUE),
(6, 'Malla Deportiva', 'Malla ajustada para mayor rendimiento en el entrenamiento', 20.99, 25, '', 1, TRUE);

-- Usuario administrador de ejemplo (password: Admin123!)
INSERT IGNORE INTO `usuarios` (`id`, `username`, `nombre`, `apellido`, `email`, `password_hash`, `verify`, `admin`, `created_at`) VALUES
(1, 'admin', 'Administrador', 'Sistema', 'admin@ecommerce.local', 'scrypt:32768:8:1$VIulv51biFXAK67A$bb1a154014b4ca31e9cde5d1dfca54c73d87a5f06eae1db5bb0f9ffbea23b9ac59be07e91c12f9a8d28284044eb701098718b39d9da589812f93a2da6b4b04bc', TRUE, TRUE, NOW());

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
COMMIT;
