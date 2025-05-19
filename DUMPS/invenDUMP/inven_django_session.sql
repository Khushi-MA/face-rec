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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4mdep8pvz7ivmyn04lill6la6maraa5o','e30:1u78yA:E_9e7viLXgg8cXja9m-t5ReHoqcx0dMQA-IsgO66pPw','2025-04-23 08:27:06.914403'),('jqt57p93ca5tbc1vxib39drbgldi07fv','.eJyl0sFu3CAQBuBXqXxOEGAbQ25NlESq1FN7i6rVGGbXbh2IMK5URfvuMascMtiHSjkywPjj97xWB1jScFhmjIfRVTdVU119rPVg_6DPG-43-FNgNvgUx57lI-x9d2bfg8Pp9v0saTDAPKy3UTb9UWhQXW2bRiN3qle1O6KzzlnFwTXHDgHQtR2iM9x0vdY9GKOdbGu1Nn2J6EabxuDn6ubptXKQcO0suWyveXMts9yutVOI_9b6Qwjuciu4xaa1cAfeo_vyuNbndeMYIlqYE-bHCdOuJbBpgSkvtbos7RLB5mamZbn9X4gjeJs_27B85BJZhh14db7ammpq-motznOII86EdgunjUgZKhKFSDJDRR0TRCR2RZKK7ie0KQY_Wir68QwxvQzBYwkzHXFxTV1as466hGA1gcldmPg_2E_oJ0wlqhUfUXWRleJMU1NtmCSmetfEqeluCmkY_YmAvuWp34CEqGlMXfH7mjKmtkip2RMJ85mUFDFpWaRkNinxIqV216Q_O1Ja06zaYqT4ZqRMEZaqzr_Ob_uocq0:1u7ssd:hxp5txanBGhAT_ArSvJ3fcimP00mWne_2jxdbW0hItA','2025-04-25 09:28:27.107995'),('l4hwq8hb0ovm7fqx877zg9zutqu9b8t6','.eJxVjEEOwiAQRe_C2pChlE5x6d4zkIEZpGpoUtqV8e7apAvd_vfef6lA21rC1mQJE6uzMur0u0VKD6k74DvV26zTXNdlinpX9EGbvs4sz8vh_h0UauVbj-AGIOm8s5YBx0wQUSxFQJ-NTwadZen7gcSOHWb0kTH3Qt7AAAbV-wPMnDdJ:1u78nZ:OFVfy5FAvA2g_Uqr-4u9GwENw18oY95CzrO2_qOAiXs','2025-04-23 08:16:09.945401');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
