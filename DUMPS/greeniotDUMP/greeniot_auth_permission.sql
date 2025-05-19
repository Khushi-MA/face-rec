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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add crop',6,'add_crop'),(22,'Can change crop',6,'change_crop'),(23,'Can delete crop',6,'delete_crop'),(24,'Can view crop',6,'view_crop'),(25,'Can add sensor data',7,'add_sensordata'),(26,'Can change sensor data',7,'change_sensordata'),(27,'Can delete sensor data',7,'delete_sensordata'),(28,'Can view sensor data',7,'view_sensordata'),(29,'Can add user',8,'add_newuser'),(30,'Can change user',8,'change_newuser'),(31,'Can delete user',8,'delete_newuser'),(32,'Can view user',8,'view_newuser'),(33,'Can add contact',9,'add_contact'),(34,'Can change contact',9,'change_contact'),(35,'Can delete contact',9,'delete_contact'),(36,'Can view contact',9,'view_contact'),(37,'Can add device',10,'add_device'),(38,'Can change device',10,'change_device'),(39,'Can delete device',10,'delete_device'),(40,'Can view device',10,'view_device'),(41,'Can add disease',11,'add_disease'),(42,'Can change disease',11,'change_disease'),(43,'Can delete disease',11,'delete_disease'),(44,'Can view disease',11,'view_disease'),(45,'Can add fertilizer requirement',12,'add_fertilizerrequirement'),(46,'Can change fertilizer requirement',12,'change_fertilizerrequirement'),(47,'Can delete fertilizer requirement',12,'delete_fertilizerrequirement'),(48,'Can view fertilizer requirement',12,'view_fertilizerrequirement'),(49,'Can add led control',13,'add_ledcontrol'),(50,'Can change led control',13,'change_ledcontrol'),(51,'Can delete led control',13,'delete_ledcontrol'),(52,'Can view led control',13,'view_ledcontrol'),(53,'Can add pest',14,'add_pest'),(54,'Can change pest',14,'change_pest'),(55,'Can delete pest',14,'delete_pest'),(56,'Can view pest',14,'view_pest'),(57,'Can add plot',15,'add_plot'),(58,'Can change plot',15,'change_plot'),(59,'Can delete plot',15,'delete_plot'),(60,'Can view plot',15,'view_plot'),(61,'Can add User Reply',16,'add_userreply'),(62,'Can change User Reply',16,'change_userreply'),(63,'Can delete User Reply',16,'delete_userreply'),(64,'Can view User Reply',16,'view_userreply'),(65,'Can add notification',17,'add_notification'),(66,'Can change notification',17,'change_notification'),(67,'Can delete notification',17,'delete_notification'),(68,'Can view notification',17,'view_notification'),(69,'Can add Password Reset OTP',18,'add_passwordresetotp'),(70,'Can change Password Reset OTP',18,'change_passwordresetotp'),(71,'Can delete Password Reset OTP',18,'delete_passwordresetotp'),(72,'Can view Password Reset OTP',18,'view_passwordresetotp');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15 21:31:33
