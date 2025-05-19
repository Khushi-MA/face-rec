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
INSERT INTO `django_session` VALUES ('aiyxquwfo6umo3fn5b3s598lcalovwby','.eJxVjEEOwiAQRe_C2hCgFEaX7j0DGWZAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnER2ojT7xiRnqnuhB9Y701Sq8s8Rbkr8qBd3hqn1_Vw_w4K9rLVJpE6D9GS1YoRwLMCHd0AQKNxkbVnjTljVsokcClCRuU3w1Ies7fi8wUIODhc:1uF9uU:_NL-U9DclZZI7px1rvAAfH8PIrGW2IcVxFJJ2hP-piw','2025-05-28 11:04:26.625559'),('e1cnkau0n2zkeyvye5l4a2q2i3309fdv','.eJyNjEEKwjAURO_yt9Yyv79NNSsP0X0IEjTQmJBkoUjvbkRxLczmMTPvSdkVV40L1q-kqdhgc70mW_0Khpwu76I_x0AdmeJK8fFm3D35_CAtQPcVxJraHTPPB9WmH1RgkanhX_r2-ZlpwDDt0TIuOGpmLapnYBTsAA3Q9gKCCjj8:1uBVLw:60EdU6G0ixQNGTlNrlKK-nCSMF9ybhisWV4zhBSNBTA','2025-05-04 09:14:40.499130'),('e8jn3un9y4s1sf3eub09kz2zus3tvu4i','.eJyrVipKLU4tic8vKVCyUjK1NDSzMFPSgQqm5iZm5gCFixNzE4tKMgoSSzJzDAwNjB3SQRJ6yfm5QKXxxanFxZn5efGpFQWZRZVKVsYGBrUA_KEdcA:1uBUea:VchBofO5b4L6Q8dtW5NFvEmWYGL1L9zpuLzyTP_4Jic','2025-05-04 08:29:52.564388'),('qjdvll2vnvodim7690fkfyi9j25u2la3','.eJxVjDEOwjAMRe-SGUWNHaU1IztniBzbpQXUSk07Ie4OlTrA-t97_-Uyb-uQt2pLHtWdXetOv1thedi0A73zdJu9zNO6jMXvij9o9ddZ7Xk53L-DgevwrbkxVNSutSgAQjEpEUchC5okQYMSUmyICYygDwX7AhhLbxE4YOfeH-oON9E:1uF9vh:mp9P3BlnV3RG1DDHBUF-Oqp1ZdgLHVdCiMzeqzfLg2w','2025-05-28 11:05:41.683471'),('w2capmpnij2e9utehxrrghxbrzwrlj35','.eJxVjMsOgjAQRf9l1ob0FaSsjHu_oZm2g1SBkrYYjfHfBcPG7T3nnjcsmZKhEcMALWQcMZV-xhIGxpk8XTdQuTjCAUymnEOcDD3nkF7QSsYOEMtsHpRCF8hDW9JCq4lL6c2vHNYRjvC3WXR3mjbgbzhd49qfSgq22pRqp7m6RE_DeXf_Aj3mfn0jI-mlb46knBBOq9prjcpp4r52tWDS8VoxjVqQFh23srNCKtuREshlA58vs0JVdA:1uDi6q:TgNkGK_-NW4cygaGR1-ykeI4o9hW7D3aKzobt6pTTrw','2025-05-10 11:16:12.513611');
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

-- Dump completed on 2025-05-15 21:31:33
