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
-- Table structure for table `members_payment`
--

DROP TABLE IF EXISTS `members_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `transaction_id` varchar(100) NOT NULL,
  `payment_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `card_number` varchar(16) DEFAULT NULL,
  `upi_id` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  KEY `members_payment_created_by_id_de414e57_fk_members_user_id` (`created_by_id`),
  KEY `members_payment_order_id_5e390172_fk_members_order_id` (`order_id`),
  CONSTRAINT `members_payment_created_by_id_de414e57_fk_members_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `members_user` (`id`),
  CONSTRAINT `members_payment_order_id_5e390172_fk_members_order_id` FOREIGN KEY (`order_id`) REFERENCES `members_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_payment`
--

LOCK TABLES `members_payment` WRITE;
/*!40000 ALTER TABLE `members_payment` DISABLE KEYS */;
INSERT INTO `members_payment` VALUES (1,20.00,'upi','914ff749-38e0-48c4-a584-a34fceef5752','2025-04-22 08:31:16.813830','success',NULL,NULL,1,1),(2,80000.00,'card','5ecd0777-b0b6-4878-90b5-a52b628a318d','2025-04-24 06:32:51.385700','success',NULL,NULL,1,2),(3,19.99,'card','cd4f8cb6-cabc-4436-9f8a-1e870177ef9d','2025-04-24 08:57:18.969493','success',NULL,NULL,1,3);
/*!40000 ALTER TABLE `members_payment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 15:03:59
