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
-- Table structure for table `demo_crop`
--

DROP TABLE IF EXISTS `demo_crop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo_crop` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `scientific_name` varchar(150) DEFAULT NULL,
  `crop_type` varchar(100) NOT NULL,
  `general_information` longtext NOT NULL,
  `growth_duration` varchar(50) NOT NULL,
  `temperature` varchar(100) NOT NULL,
  `rainfall` varchar(100) NOT NULL,
  `sowing_temperature` varchar(100) NOT NULL,
  `harvesting_temperature` varchar(100) NOT NULL,
  `season` varchar(50) NOT NULL,
  `soil` longtext NOT NULL,
  `land_preparation` longtext NOT NULL,
  `seed_rate` longtext NOT NULL,
  `seed_treatment` longtext NOT NULL,
  `insecticide_name` longtext NOT NULL,
  `quantity` longtext NOT NULL,
  `time_of_sowing` longtext NOT NULL,
  `spacing` longtext NOT NULL,
  `method_of_sowing` longtext NOT NULL,
  `sowing_depth` longtext NOT NULL,
  `weed_control` longtext NOT NULL,
  `irrigation` longtext NOT NULL,
  `ph_level` longtext NOT NULL,
  `harvesting_time` longtext NOT NULL,
  `yield_per_hectare` longtext NOT NULL,
  `post_harvest_handling` longtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_crop`
--

LOCK TABLES `demo_crop` WRITE;
/*!40000 ALTER TABLE `demo_crop` DISABLE KEYS */;
INSERT INTO `demo_crop` VALUES (1,'SUGARCANE','Saccharum officinarum','Cereal','Sugarcane, Saccharum officinarum L. is a perennial gras. It belongs to bamboo family and it is indigenous to India. It is the main source of sugar, jaggery and khandsari. About two-thirds of the total sugarcane produced in India is consumed for making jaggery and khandsari and only one third of it goes to sugar factories. It also provides raw material for manufacturing alcohol. Brazil is largest producer of sugarcane followed by India, China, Thailand, Pakistan and Mexico. In India, Maharashtra is largest producer of sugar and it contributes about 34% of sugar in country followed by Uttar Pradesh.\r\n\r\n','12 to 18 months','20-30°C','75-150cm','20-25°C','20-30°C','December to May','The most suitable soil types are loamy soils with good drainage and a pH range of 6.5 to 7.5. These soils have a good balance of nutrients, water-holding capacity, and aeration, which are crucial for healthy sugarcane growth. While sugarcane can also be grown in other soil types like sandy and clay loam, loamy soils are considered ide','Give two ploughings to land. First ploughing should be given at depth of 20-25 cm. Crush clods with suitable implements or machine.\r\n\r\n','Various research and experiment shows that, germination percentage of 3 bud sets is higher than the setts having more or less than three buds. Germination percentage of single bud sett is very low because of moisture loss from other cut end. Also if whole can stalk is planted without giving any cut, still germination percentage remain low as only top end will get germinate.  Seed rate vary from region to region. In North West India, seed rate is high because of low germination percentage and adverse weather i.e hot weather with desiccating winds. Use seed rate of 20,000 three budded setts per acre','Take seed material from crop of 6-7 months age. It should be free from pest and disease. Discard pest, disease affected and damaged buds and canes. Harvest seed crop one day before planting, it will give high and uniform germination. The setts should be soaked in Carbendazim@3gm in 1litre of water. After chemical treatment treat with  Azospirillum. For that dip setts in Azospirillum inoculum@800gm/acre +sufficient water solution for 15min before planting.   \r\n','','','In Punjab, planting season of sugarcane is from September to October and February to March. Sugarcane takes generally one year to mature therefore called as Eksali.','Row spacing is ranges from 60-120 cm for sub-tropical regions.\r\n','A) For sowing use improved method of planting like deep furrow, trench method, paired row method or ring pit method.  1) Dry planting in ridges and furrow: With the help of tractor drawn ridger, make ridges and furrows at distance of 90 cm. Plant sugarcane setts then cover it with soil. After then give light irrigation.   2) Paired row planting: Make Trenches at 150 cm distance using trenches opener. Plant sugarcane in paired row using 30:30-90-30:30cm spacing. It gives higher yield as compared to ridges and furrow.   3) Ring Pit method: Circular pits of 60 cm diameters are dug at depth of 30 cm with a tractor mounted digger. 60 cm gap is provided between adjacent pits. 2-3 ratoons can be taken. 25-50% higher yield can be obtained compared to ridge and furrow.   B) Single budded set planting: Select healthy setts for plantation. Make furrows at distance of 75-90 cm. Place single budded setts. If only small size setts from top portion of cane are selected then they are planted at distance of 6\"-9\". Place eye of sett on upward direction to ensure proper and quick germination. Cover setts with soil and apply light irrigation. Show Less','Sow the sugarcane at depth of 3-4 cm and cover it with soil.','In sugarcane due to weed infestation about 12 to 72% yield loss is observed depending upon severity. Initial 60-120 days are critical for weed management. Therefore weed management practices should be adopt within 3-4 months after planting. For control of weeds, chemical is not only solution. Adopting mechanical as well as cultural practices gives effective solution.\r\n\r\n1) Mechanical Measure: As sugarcane is widely space crop, weeding with hand or interculture operation can be easily carried out. Take 3-4 hoeing after every irrigation.\r\n\r\n2) Cultural Operations: It included change in cropping pattern, intercropping and trash mulching. Monocropping leads to heavy infestation of weed. Crop rotation with fodder or green manure crops suppress weeds. Also sugarcane is wider space crop so there is opportunity for weed to grow in large numbers. If sugarcane is intercrop with short duration crops then it will suppress the weed growth also give additional benefit. In trash mulching, mulch of 10-12cm thickness is provided in between cane row after emergence of cane. It will restrict the sunlight thus help to check weed growth. It also conserved soil moisture.\r\n\r\n3) Chemical: To control weeds, carry out pre-emergence weedicide application with Simazine or Atrazine@600-800 g/acre or Metribuzine@ 800 g/acre or Diuron@1- 1.2 kg/acre. Apply pre-emergence herbicides immediately after planting. Apply 2,4-D@250-300 g/acre as post-emergence herbicide for broad-spectrum weed control in sugarcane','The number of irrigations required will depending upon soil type, water availability etc. The hot weather associated with dry winds and drought increases the water requirement of the crop. \r\n\r\nApply first irrigation when 20-25% crops have germinated. In monsoon, apply irrigation depending upon rainfall intensity and frequency. In case of scanty rainfall apply irrigation with 10days interval. Afterwards increase irrigation intervals, i.e apply water with 20-25days interval. To conserved moisture in soil do mulching in between cane rows. Avoid water stress from April to June. Water stress during these days will reduce yield. Avoid water logging in standing field. Tillering stage and elongation or grand growth phase are critical for irrigation.\r\n\r\nEarthing: Soil between the furrows of canes, is taken with the help of spade and applied to the sides of the plants. It help to mix top dressed fertilizer well within the soil, also it help to support plant and prevent it from lodging.','6.5to 7.5','Harvesting of cane at right time is necessary for good yield and for high sugar recovery. Harvesting at over aged or under aged cane leads to loss in cane yield. Depending upon withering of leaves and cane juice, harvesting time can be decided. To know the right harvesting time some farmer used hand sugar refractometer is used. Sickles are used for harvesting. Stalks are cut at ground level so that the bottom sugar rich internodes are harvested which add to yield and sugar. De-topping at appropriate height. After harvesting quick disposal of the harvested cane to factory is necessary.','2','Sugarcane provides a juice, which is used for making white sugar, and jaggery (gur) and many by products like bagasse and molasses.','crop_images/6467idea99sugarcane.jpg');
/*!40000 ALTER TABLE `demo_crop` ENABLE KEYS */;
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
