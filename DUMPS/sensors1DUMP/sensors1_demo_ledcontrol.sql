-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sensors1
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
-- Table structure for table `demo_ledcontrol`
--

DROP TABLE IF EXISTS `demo_ledcontrol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_ledcontrol` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `relay_status` varchar(10) NOT NULL,
  `timer_duration` int NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `device_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `demo_ledcontrol_device_id_5e5e5bd8_fk_demo_device_id` (`device_id`),
  KEY `demo_ledcontrol_user_id_04cd9682_fk_demo_newuser_id` (`user_id`),
  CONSTRAINT `demo_ledcontrol_device_id_5e5e5bd8_fk_demo_device_id` FOREIGN KEY (`device_id`) REFERENCES `demo_device` (`id`),
  CONSTRAINT `demo_ledcontrol_user_id_04cd9682_fk_demo_newuser_id` FOREIGN KEY (`user_id`) REFERENCES `demo_newuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_ledcontrol`
--

LOCK TABLES `demo_ledcontrol` WRITE;
/*!40000 ALTER TABLE `demo_ledcontrol` DISABLE KEYS */;
INSERT INTO `demo_ledcontrol` VALUES (23,'ON',0,'2025-04-28 07:14:36.343260',NULL,2,3),(24,'OFF',30,'2025-04-28 07:14:44.818809',NULL,2,3),(25,'OFF',30,'2025-04-28 07:15:22.850103',NULL,2,3),(26,'OFF',0,'2025-04-28 07:15:58.732138',NULL,2,3),(27,'ON',0,'2025-04-28 07:16:38.208714',NULL,2,3),(28,'OFF',0,'2025-04-28 07:17:03.642748',NULL,2,3),(29,'OFF',30,'2025-04-28 07:45:23.210482',NULL,2,3),(30,'OFF',0,'2025-04-28 07:46:00.716230',NULL,2,3),(31,'ON',0,'2025-04-28 09:07:24.446610',NULL,2,3),(32,'ON',0,'2025-04-28 09:07:29.759353',NULL,2,3),(33,'ON',0,'2025-04-28 09:07:38.624848',NULL,2,3),(34,'ON',0,'2025-04-28 09:07:47.871262',NULL,2,3),(35,'OFF',0,'2025-04-28 09:07:51.683925',NULL,2,3),(36,'ON',0,'2025-04-28 12:23:03.389728',NULL,2,3),(37,'OFF',0,'2025-04-28 12:35:40.886715',NULL,2,3),(38,'OFF',0,'2025-04-28 15:53:31.366013',NULL,2,3);
/*!40000 ALTER TABLE `demo_ledcontrol` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-29 14:09:22
