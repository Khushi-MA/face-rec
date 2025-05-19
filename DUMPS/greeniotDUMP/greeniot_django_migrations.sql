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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-03 20:54:07.024315'),(2,'contenttypes','0002_remove_content_type_name','2025-05-03 20:54:07.094653'),(3,'auth','0001_initial','2025-05-03 20:54:07.271399'),(4,'auth','0002_alter_permission_name_max_length','2025-05-03 20:54:07.355536'),(5,'auth','0003_alter_user_email_max_length','2025-05-03 20:54:07.362548'),(6,'auth','0004_alter_user_username_opts','2025-05-03 20:54:07.374042'),(7,'auth','0005_alter_user_last_login_null','2025-05-03 20:54:07.385032'),(8,'auth','0006_require_contenttypes_0002','2025-05-03 20:54:07.391313'),(9,'auth','0007_alter_validators_add_error_messages','2025-05-03 20:54:07.402608'),(10,'auth','0008_alter_user_username_max_length','2025-05-03 20:54:07.416814'),(11,'auth','0009_alter_user_last_name_max_length','2025-05-03 20:54:07.426327'),(12,'auth','0010_alter_group_name_max_length','2025-05-03 20:54:07.454827'),(13,'auth','0011_update_proxy_permissions','2025-05-03 20:54:07.465953'),(14,'auth','0012_alter_user_first_name_max_length','2025-05-03 20:54:07.472952'),(15,'demo','0001_initial','2025-05-03 20:54:08.284975'),(16,'admin','0001_initial','2025-05-03 20:54:08.356552'),(17,'admin','0002_logentry_remove_auto_add','2025-05-03 20:54:08.369565'),(18,'admin','0003_logentry_add_action_flag_choices','2025-05-03 20:54:08.380817'),(19,'sessions','0001_initial','2025-05-03 20:54:08.437656'),(20,'demo','0002_newuser_reset_token_alter_newuser_full_name_and_more','2025-05-04 06:07:47.499900'),(21,'demo','0003_newuser_security_answer_newuser_security_question','2025-05-04 06:41:30.716621'),(22,'demo','0004_newuser_otp_newuser_otp_created_at','2025-05-04 09:23:39.971072'),(23,'demo','0005_remove_newuser_otp_remove_newuser_otp_created_at_and_more','2025-05-04 09:23:40.618690'),(24,'demo','0006_notification_delete_userreply','2025-05-04 13:47:58.900067'),(25,'demo','0002_alter_newuser_contact_no','2025-05-04 18:17:21.539572'),(26,'demo','0002_newuser_profile_photo','2025-05-10 11:00:03.380046'),(27,'demo','0003_passwordresetotp','2025-05-10 11:00:03.509163'),(28,'demo','0004_delete_passwordresetotp','2025-05-10 11:00:03.606332'),(29,'demo','0005_passwordresetotp','2025-05-10 11:00:03.772734');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15 21:31:31
