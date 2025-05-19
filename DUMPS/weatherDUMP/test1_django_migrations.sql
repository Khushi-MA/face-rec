-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: test1
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-02 05:40:40.670954'),(2,'contenttypes','0002_remove_content_type_name','2025-05-02 05:40:40.805835'),(3,'auth','0001_initial','2025-05-02 05:40:41.026630'),(4,'auth','0002_alter_permission_name_max_length','2025-05-02 05:40:41.113067'),(5,'auth','0003_alter_user_email_max_length','2025-05-02 05:40:41.120108'),(6,'auth','0004_alter_user_username_opts','2025-05-02 05:40:41.130820'),(7,'auth','0005_alter_user_last_login_null','2025-05-02 05:40:41.146934'),(8,'auth','0006_require_contenttypes_0002','2025-05-02 05:40:41.151745'),(9,'auth','0007_alter_validators_add_error_messages','2025-05-02 05:40:41.164339'),(10,'auth','0008_alter_user_username_max_length','2025-05-02 05:40:41.176827'),(11,'auth','0009_alter_user_last_name_max_length','2025-05-02 05:40:41.189564'),(12,'auth','0010_alter_group_name_max_length','2025-05-02 05:40:41.215281'),(13,'auth','0011_update_proxy_permissions','2025-05-02 05:40:41.222424'),(14,'auth','0012_alter_user_first_name_max_length','2025-05-02 05:40:41.230959'),(15,'accounts','0001_initial','2025-05-02 05:40:41.524810'),(16,'account','0001_initial','2025-05-02 05:40:41.672820'),(17,'account','0002_email_max_length','2025-05-02 05:40:41.698316'),(18,'account','0003_alter_emailaddress_create_unique_verified_email','2025-05-02 05:40:41.742439'),(19,'account','0004_alter_emailaddress_drop_unique_email','2025-05-02 05:40:41.801895'),(20,'account','0005_emailaddress_idx_upper_email','2025-05-02 05:40:41.866710'),(21,'account','0006_emailaddress_lower','2025-05-02 05:40:41.893323'),(22,'account','0007_emailaddress_idx_email','2025-05-02 05:40:41.995859'),(23,'account','0008_emailaddress_unique_primary_email_fixup','2025-05-02 05:40:42.021299'),(24,'account','0009_emailaddress_unique_primary_email','2025-05-02 05:40:42.042435'),(25,'admin','0001_initial','2025-05-02 05:40:42.160834'),(26,'admin','0002_logentry_remove_auto_add','2025-05-02 05:40:42.178873'),(27,'admin','0003_logentry_add_action_flag_choices','2025-05-02 05:40:42.218315'),(28,'sessions','0001_initial','2025-05-02 05:40:42.290212'),(29,'sites','0001_initial','2025-05-02 05:40:42.313547'),(30,'sites','0002_alter_domain_unique','2025-05-02 05:40:42.338722'),(31,'socialaccount','0001_initial','2025-05-02 05:40:42.616064'),(32,'socialaccount','0002_token_max_lengths','2025-05-02 05:40:42.716266'),(33,'socialaccount','0003_extra_data_default_dict','2025-05-02 05:40:42.726740'),(34,'socialaccount','0004_app_provider_id_settings','2025-05-02 05:40:42.955541'),(35,'socialaccount','0005_socialtoken_nullable_app','2025-05-02 05:40:43.115800'),(36,'socialaccount','0006_alter_socialaccount_extra_data','2025-05-02 05:40:43.245652');
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

-- Dump completed on 2025-05-02 12:24:23
