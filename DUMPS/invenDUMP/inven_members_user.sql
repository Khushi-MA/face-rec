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
-- Table structure for table `members_user`
--

DROP TABLE IF EXISTS `members_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_user`
--

LOCK TABLES `members_user` WRITE;
/*!40000 ALTER TABLE `members_user` DISABLE KEYS */;
INSERT INTO `members_user` VALUES (1,'pbkdf2_sha256$870000$cB0aboDbCiYIif3d02PWqu$JNy6ic5XITVESuxrvF2kHw2MiQMEmsGjdsKLef2xGYQ=','2025-04-24 08:56:16.254660',0,'sharada yaligar','','','shanu@gmail.com',0,1,'2025-04-22 08:16:09.906216','manager','2025-04-22 08:16:09.906799'),(3,'pbkdf2_sha256$870000$R1GhQHJ0wjivhMPMiS4O7u$uIhN7MdPoHiVvmWbnCBIopRA6XqEa/NDPRT7tYZp5RM=','2025-04-22 08:17:38.511223',0,'sharada ','','','sharada@gmail.com',0,1,'2025-04-22 08:17:38.496787','manager','2025-04-22 08:17:38.497470'),(4,'pbkdf2_sha256$870000$UATlTPn4jL4OXkKOhuRfC1$/z/HVVWvNYlyIrCoxhVHEFN25cFXPRKRmUiPcmOWJpI=','2025-04-24 08:57:49.561305',0,'Prathik patil','','','pratikpatil@gmail.com',0,1,'2025-04-22 08:19:49.229059','analyst','2025-04-22 08:19:49.229526'),(5,'pbkdf2_sha256$870000$uYUocSZ2vFVst0m76PQcXu$L5ZOyRAWcoe1TQrmL5O7pExDiNeyC0wtU5VFJoiTZ/A=','2025-04-24 06:56:38.774927',0,'Gayathri','','','gayathrialigar@gmail.com',0,1,'2025-04-22 08:22:19.224927','admin','2025-04-22 08:22:19.225358'),(6,'pbkdf2_sha256$870000$WpTUZraMieohxrK8PH0rJO$ahyQaEI2pNivywgsDbeByOeSrbFZLc093R/dfpTel7w=','2025-04-24 06:51:40.961695',1,'sachin','','','sachin@gmail.com',1,1,'2025-04-24 06:44:26.139909','manager','2025-04-24 06:44:26.727611');
/*!40000 ALTER TABLE `members_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-24 15:04:01
