-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: greeniot
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
-- Table structure for table `demo_newuser`
--

DROP TABLE IF EXISTS `demo_newuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_newuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `contact_no` varchar(15) DEFAULT NULL,
  `place` varchar(100) NOT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact_no` (`contact_no`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_newuser`
--

LOCK TABLES `demo_newuser` WRITE;
/*!40000 ALTER TABLE `demo_newuser` DISABLE KEYS */;
INSERT INTO `demo_newuser` VALUES (1,'pbkdf2_sha256$1000000$AhBoUpgtli8HX6bGwo5Roi$17lIQc3DWtUrXyzxq34OGyLxJcmiBEiff9WLS16wDDo=','2025-05-04 05:14:47.000585',0,'sam1@gmail.com','','',0,1,'2025-05-03 20:54:51.459772','Samarth Patil','sam1@gmail.com','6360236750','hubli',NULL),(7,'pbkdf2_sha256$1000000$BUV0hlCOr2VPBsqB2avmHD$CO369h37y8BCLaylpQYZ2qwJBn/8W6wfw16OrzBPgWM=','2025-05-14 11:05:41.675327',0,'samarthpatil0103@gmail.com','','',0,1,'2025-05-04 09:14:58.554627','Samarth Patil','samarthpatil0103@gmail.com','6360236756','hubli','profile_photos/samarth-photo.png'),(12,'pbkdf2_sha256$1000000$iZKYGGh1ilumSlbXXx13sg$+X+5nqHcOpMIZvLeDnqHEkV+XPzWaRdhNCe/nolXnpU=','2025-05-14 11:04:26.617541',1,'admim','','',1,1,'2025-05-12 04:17:53.120637','admin','admin@gmail.com','9632587456','hubli','');
/*!40000 ALTER TABLE `demo_newuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15 21:31:32
