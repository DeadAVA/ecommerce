-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-06-2025 a las 02:34:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ecommerce`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `ip_address` varchar(45) DEFAULT NULL,
  `extra_info` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `timestamp`, `ip_address`, `extra_info`) VALUES
(1, 5, 'Accedió al panel de control', '2025-06-01 00:32:25', '127.0.0.1', NULL),
(2, 5, 'Accedió al panel de control', '2025-06-01 00:33:16', '127.0.0.1', NULL),
(3, 5, 'Accedió al panel de control', '2025-06-01 00:33:26', '127.0.0.1', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT 1,
  `fecha_agregado` datetime DEFAULT current_timestamp(),
  `imagen_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`) VALUES
(1, 'Ropa Deportiva');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `estado` varchar(50) DEFAULT 'pendiente',
  `direccion_envio_id` int(11) DEFAULT NULL,
  `metodo_pago` varchar(50) NOT NULL DEFAULT 'transferencia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`id`, `usuario_id`, `total`, `fecha`, `estado`, `direccion_envio_id`, `metodo_pago`) VALUES
(13, 5, 49.99, '2025-05-01 22:48:58', 'pendiente', 3, 'transferencia'),
(14, 5, 24.99, '2025-05-01 22:49:06', 'pendiente', 3, 'paypal'),
(15, 5, 24.99, '2025-05-01 22:49:10', 'pendiente', 3, 'paypal'),
(16, 5, 24.99, '2025-05-01 22:49:16', 'pagado', 3, 'paypal'),
(17, 5, 24.99, '2025-05-01 22:49:18', 'pagado', 3, 'paypal'),
(18, 5, 124.95, '2025-05-01 22:49:20', 'pendiente', 3, 'paypal'),
(19, 5, 24.99, '2025-05-01 22:49:23', 'pendiente', 3, 'transferencia'),
(21, 5, 24.99, '2025-05-02 22:49:25', 'pendiente', 3, 'transferencia');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobantes`
--

CREATE TABLE `comprobantes` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) NOT NULL,
  `archivo` varchar(200) NOT NULL,
  `fecha_subida` datetime DEFAULT current_timestamp(),
  `verificado` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comprobantes`
--

INSERT INTO `comprobantes` (`id`, `pedido_id`, `archivo`, `fecha_subida`, `verificado`) VALUES
(5, 13, '73a927ce26ce43bda3a3b66959e344b3_img001.jpg', '2025-05-19 23:19:21', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_compra`
--

CREATE TABLE `detalle_compra` (
  `id` int(11) NOT NULL,
  `compra_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_compra`
--

INSERT INTO `detalle_compra` (`id`, `compra_id`, `producto_id`, `cantidad`, `precio_unitario`) VALUES
(8, 13, 4, 1, 49.99),
(9, 14, 3, 1, 24.99),
(10, 15, 3, 1, 24.99),
(11, 16, 3, 1, 24.99),
(12, 17, 3, 1, 24.99),
(13, 18, 3, 5, 24.99),
(14, 19, 3, 1, 24.99),
(15, 21, 3, 1, 24.99);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direccion_envio`
--

CREATE TABLE `direccion_envio` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `direccion` text NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `pais` varchar(100) DEFAULT 'México',
  `telefono` varchar(20) DEFAULT NULL,
  `referencias` text DEFAULT NULL,
  `colonia` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `direccion_envio`
--

INSERT INTO `direccion_envio` (`id`, `usuario_id`, `direccion`, `ciudad`, `estado`, `codigo_postal`, `pais`, `telefono`, `referencias`, `colonia`) VALUES
(3, 5, 'Bahía Concepcion 126', 'Ensenada', 'Baja California', '22785', 'México', '6461844845', 'Casa color beige rejas color negro y dos perritos, uno colo blanco y otro color vainilla', 'Vista Hermosa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envios`
--

CREATE TABLE `envios` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `estado` enum('pendiente','procesado','aceptado','enviado','entregado','cancelado') NOT NULL DEFAULT 'pendiente',
  `numero_rastreo` varchar(150) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `direccion_envio_id` int(11) NOT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `imagen_url` varchar(255) DEFAULT NULL,
  `categoria_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `imagen_url`, `categoria_id`) VALUES
(2, 'Camiseta Deportiva', 'Camiseta ligera y transpirable para deportes', 29.99, 50, '', 1),
(3, 'Pantalones Cortos Deportivos', 'Pantalones cortos cómodos para correr o entrenar', 24.99, 40, '', 1),
(4, 'Sudadera con Capucha', 'Sudadera con capucha para calentamiento y frío', 49.99, 30, '', 1),
(5, 'Calcetas Deportivas', 'Calcetas que absorben el sudor para mayor comodidad', 9.99, 100, '', 1),
(6, 'Chaqueta Cortaviento', 'Chaqueta ligera resistente al viento para exteriores', 59.99, 20, '', 1),
(7, 'Malla Deportiva', 'Malla ajustada para mayor rendimiento en el entrenamiento', 20.99, 25, '', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `verify` tinyint(1) NOT NULL DEFAULT 0,
  `token` varchar(64) DEFAULT NULL,
  `token_expiry` datetime DEFAULT NULL,
  `admin` tinyint(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `nombre`, `apellido`, `email`, `password_hash`, `verify`, `token`, `token_expiry`, `admin`) VALUES
(5, 'Alan', 'Alan', 'Aranda', 'alan.villalobos0603@gmail.com', 'scrypt:32768:8:1$VIulv51biFXAK67A$bb1a154014b4ca31e9cde5d1dfca54c73d87a5f06eae1db5bb0f9ffbea23b9ac59be07e91c12f9a8d28284044eb701098718b39d9da589812f93a2da6b4b04bc', 1, NULL, NULL, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `direccion_envio_id` (`direccion_envio_id`);

--
-- Indices de la tabla `comprobantes`
--
ALTER TABLE `comprobantes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_comprobante_pedido` (`pedido_id`);

--
-- Indices de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD PRIMARY KEY (`id`),
  ADD KEY `compra_id` (`compra_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `direccion_envio`
--
ALTER TABLE `direccion_envio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `envios`
--
ALTER TABLE `envios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pedido` (`pedido_id`),
  ADD KEY `fk_usuario` (`usuario_id`),
  ADD KEY `fk_direccion` (`direccion_envio_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `categoria_id` (`categoria_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `token` (`token`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `comprobantes`
--
ALTER TABLE `comprobantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `direccion_envio`
--
ALTER TABLE `direccion_envio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `envios`
--
ALTER TABLE `envios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direccion_envio` (`id`);

--
-- Filtros para la tabla `comprobantes`
--
ALTER TABLE `comprobantes`
  ADD CONSTRAINT `fk_comprobante_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `compras` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalle_compra`
--
ALTER TABLE `detalle_compra`
  ADD CONSTRAINT `detalle_compra_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`),
  ADD CONSTRAINT `detalle_compra_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `direccion_envio`
--
ALTER TABLE `direccion_envio`
  ADD CONSTRAINT `direccion_envio_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `envios`
--
ALTER TABLE `envios`
  ADD CONSTRAINT `fk_direccion` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direccion_envio` (`id`),
  ADD CONSTRAINT `fk_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `compras` (`id`),
  ADD CONSTRAINT `fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
