-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: inven
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `members_item`
--

DROP TABLE IF EXISTS `members_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) NOT NULL,
  `category` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `quantity` int unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `reorder_level` int unsigned NOT NULL,
  `supplier` varchar(200) NOT NULL,
  `sku` varchar(50) DEFAULT NULL,
  `product_image` varchar(100) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `members_item_created_by_id_1310264b_fk_members_user_id` (`created_by_id`),
  CONSTRAINT `members_item_created_by_id_1310264b_fk_members_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `members_user` (`id`),
  CONSTRAINT `members_item_chk_1` CHECK ((`quantity` >= 0)),
  CONSTRAINT `members_item_chk_2` CHECK ((`reorder_level` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_item`
--

LOCK TABLES `members_item` WRITE;
/*!40000 ALTER TABLE `members_item` DISABLE KEYS */;
INSERT INTO `members_item` VALUES (1,'Chips','Food','food item',4,20.00,3,'chips center','chips01','products/image001.png',1,'2025-04-22 08:29:35.465918','2025-04-22 08:31:05.703058',1),(2,'Mobile','Electronics','mobile',1,80000.00,1,'sangeetha mobils','mob01','products/ChatGPT_Image_Apr_1_2025_07_23_48_PM.png',1,'2025-04-22 08:30:44.882938','2025-04-24 06:32:24.320730',1),(3,'T-Shirt','Clothing','Cotton T-Shirt',9,19.99,5,'',NULL,'',1,'2025-04-24 08:42:28.755432','2025-04-24 08:57:06.691321',NULL);
/*!40000 ALTER TABLE `members_item` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 15:04:00
