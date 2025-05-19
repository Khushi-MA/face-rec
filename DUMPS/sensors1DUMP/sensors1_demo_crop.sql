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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demo_crop`
--

LOCK TABLES `demo_crop` WRITE;
/*!40000 ALTER TABLE `demo_crop` DISABLE KEYS */;
INSERT INTO `demo_crop` VALUES (1,' MAIZE','Zea mays','Cereal','Maize (Zea mays L) is second rated grain used collectively in form of foodstuff or fodder. Globally, maize is known as queen of cereals because it has highest genetic yield potential among the cereals. Grains provides food items which are consumed in the form of starch, corn flakes also glucose. It is also used as animal feed in poultry. Maize can be cultivated in any soil as they require less fertile soil and various chemicals. Moreover, it fetch less ripening span, 3 months, in comparison to paddy, which takes 145 days.','3 Months','25°C - 30°C','50-100cm','25°C - 30°C','30-35°C','may -june ','Animal husbandry and fishery\r\nOrganic\r\nGovt. Schemes\r\nPartner With Us\r\nBlog\r\n Refine Search\r\nCrops\r\nCEREALS\r\n \r\nFIBRE CROPS\r\n \r\nFODDER\r\n \r\nGREEN MANURE\r\n \r\nOILSEEDS\r\n \r\nPULSES\r\n \r\nSUGAR AND STARCH CROPS\r\nhorticulture\r\nCITRUS\r\n \r\nFLOWERS\r\n \r\nFORESTRY\r\n \r\nFRUIT\r\n \r\nMEDICINAL PLANTS\r\n \r\nPLANTATION CROPS\r\n \r\nSPICE AND CONDIMENTS\r\n \r\nVEGETABLE CROPS\r\nAgriculture\r\nKharif Maize Crop Punjab\r\nMAIZE (KHARIF)\r\nSeason Kharif/ End-May - June\r\nSeason TYPES OF VARIETIES\r\nSeason CHEMICAL FERTILIZER\r\nSeason PEST CONTROL\r\nGeneral Information\r\nMaize (Zea mays L) is second rated grain used collectively in form of foodstuff or fodder. Globally, maize is known as queen of cereals because it has highest genetic yield potential among the cereals. Grains provides food items which are consumed in the form of starch, corn flakes also glucose. It is also used as animal feed in poultry. Maize can be cultivated in any soil as they require less fertile soil and various chemicals. Moreover, it fetch less ripening span, 3 months, in comparison to paddy, which takes 145 days.\r\n\r\nBy growing maize, farmers can easily shield the deteriorating grade of soil , preserve 90% of water and 70% of potency as compared with paddy and can make more profit than wheat and paddy,” reported by vice chancellor, Punjab Agricultural University, Ludhiana. It serves as basic raw material to thousands of industrial products like oil, starch, alcoholic beverages etc. Uttar Pradesh, Rajasthan, Madhya Pradesh, Bihar, Himachal Pradesh, J & K and Punjab are major maize growing states. AP and Karnataka is major producer of maize in south.\r\n\r\nShow Less\r\nClimate\r\nSeason\r\nTemperature\r\n25°C - 30°C\r\nSeason\r\nRainfall\r\n50-100cm\r\nSeason\r\nSowing Temperature\r\n25°C - 30°C\r\nSeason\r\nHarvesting Temperature\r\n30-35°C\r\nSoil\r\nFertile well-drained alluvial or simply red loams free of coarse elements and full off nitrogen are ideal soils for maize cultivation. Maize can be grown on wide range of soils including loamy sand to clay loam. Definitely depleted plains are effective suited to the cultivation, even though it grows up in various hilly zones equally. Soils with fine organic matter containing good water holding capacity with pH ranging from 5.5-7.5 are required to increase yield. Heavy clay soil is not suitable for cultivation.\r\n\r\nSoil test is necessary to know deficiency of any nutrient in the soil.','For cultivation selected land should be free from weeds and remains of previously grown crop. Plough the land to bring the soil to fine tilth. It may take 6 to 7 plough. Apply 4-6 tons/acre of well decomposed cow dung across the field, also apply 10 Azospirillum packets in field. Prepared furrow and ridges with 45 cm to 50 cm spacing.','Purpose, seed size, season, plant type, sowing method these factor affect seed rate. 1) For kharif maize : use seed rate of 8-10 kg/acre, 2) Sweet corn : use seed rate of 8 kg/acre 3) Baby corn: 16 kg/acre seed rate. 4) Pop corn: 7 kg/acre seed rate. 5) Fodder: 20 kg/acre seed rate. Intercropping: Pea can be taken as intercrop in maize plant. For that take one row of pea between maize crops. In autumn sugarcane and maize can also be intercropped. Sow one row of maize plant after two row of sugarcane.','To protect seeds from soil borne diseases and insect pest, seed treatment is necessary. To protect seeds from downy mildew, treat the seed with Carbendazim or Thiram@2gm/kg of seeds. After chemical treatment, treat seed with Azospirillum@600gm+ rice gruel. After treatment shade dry seeds for 15-20 minutes. Azosprillum helps in fixing of atmospheric nitrogen in the soil.','Dimethoate 30.00% EC,Carbofuran 03.00% CG	','5','In kharif season, crop is sown in month of May end to June corresponding with the onset of monsoon. Spring crops are sown during late February to end of march. Plantation of baby corn can be done all the year round, except December and January. Kharif and rabi season are best for sweet corn sowing.','To obtain higher yield along with resource-use efficiency, optimum plant spacing is the key factor.  \r\n1) For kharif maize : use spacing of 60x20 cm.\r\n2) Sweet corn : use spacing of 60x20 cm spacing.\r\n3) Baby corn: Use 60x20 cm or 60x15 cm spacing.\r\n4) Pop corn: Use 50x15 cm spacing.\r\n5) Fodder: use spacing of 30x10 cm spacing','Sowing can be done manually by dibbling seeds or by mechanically with help of tractor drawn ridger seed drill.','Seed should be sown at depth of 3-4 cm. For sweet corn cultivation keep depth of sowing to 2.5 cm.','Weeds are the serious problem in maize, particularly during kharif/monsoon season they competes with maize for nutrient and causes yield loss upto 35%. Therefore, timely weed management is needed for achieving higher yield. Take atleast one or two hand weeding in maize crop. First 20-25 days after sowing and second when on 40-45 days after sowing. If weed infestation is high, spray with Atrazine @500gm per 200 Ltr of water. After weeding, apply fertilizer as top dressing and carry out earthing up operation.','Apply irrigation immediately after sowing. Based upon soil type, on third or fourth day give lifesaving irrigation. In rainy season, if rain is satisfactory then it is not needed. Avoid water stagnation in early phase of crop and provide good drainage facility. Crop required less irrigation during early stage, 20 to 30 days after sowing afterwards it required irrigation once in a week. Seedling, knee height stage, flowering and grain feeling are the most sensitive stage for irrigation. Water stress at this stage cause huge loss in yield. In case of water scarcity, irrigate alternate furrow. It will save water also.\r\n\r\n','6','Harvesting should be done when cobs outer cover turns from green to white. The optimum time of harvesting maize is when the stalks have dried and moisture of grain as about 17-20%. Drying place or equipment should be dry, clean and disinfected.   Sweet corn harvesting: When crops come nears to maturity, examined a few ears daily to determine the time for the first picking. Corn is ready for harvest when the ear is full size for the variety, has a tight husk, and has somewhat dried silks. The kernels are fully developed and exude a milky liquid when punctured. Delay harvesting causes reduction in sugar content. Whether harvesting is done by hand or machine, sweet corn should be collected at night or early in the morning.  Baby corn: Ears are harvested 45-50 days after emergence, when silks are 1-2 cm long (within 1-2 days after silk emergence). Harvesting is carried out in morning when temperature is low and moisture is high. The picking of baby corn should be done once in three days and generally 7-8 pickings','100 kg','100','crop_images/corn-cob-isolated-maize-with-green-leaves-sketch-vector-28600391_rnRxXSB.jpg'),(2,'RICE','Oryza sativa','Cereal','Rice is the most important food crop of India covering about one-fourth of the total cropped area and providing food to about half of the Indian population. Punjab has made tremendous progress in rice productivity and production during the past 45 years. Due to use of high yielding varieties and new technology Punjab has given the title of \"Rice Bowl of India\".','6 Months','16-30° C','100-200cm','20-30°C','16-27° C','May-June','It can be grown on a variety of soils with low permeability and pH varying from 5.0 to 9.5. Sandy loam to loamy sand to silty loam to clay loams, silty to clayey loam soils with low permeability, free of water logging and sodicity are considered best for paddy cultivation.','After harvesting of wheat grow dhaincha (seed rate 20 kg/acre) or sunhemp @ 20 kg/acre or cowpea @ 12 kg/acre up to first week of May. When crop is of 6-8 week old, bury them into the soil one day before transplanting of paddy. It will save 25 kg of N per acre. Use laser land leveler for land levelling. After then puddle soil and to obtained fine well levelled puddle field to reduce water loss through percolation','8kg seeds are sufficient for planting in one acre land.','Before sowing, soak them in 10 Ltr water containing, Carbendazim@20gm+ Streptocycline@1gm for 8 to 10 hour before sowing. After then dry seeds in shade. And then use for sowing.\r\nAlso you can use below mention fungicides to protect crop from root rot disease. Use chemical fungicides first then treat seed with Trichoderma.','Dinotefuran','-','20 may to 5 june is the optimum time for sowing ','For normal sown crop a spacing of 20 - 22.5 cm between rows is recommended. When sowing is delayed a closer spacing of 15-18 cm should be adopted.','Broadcasting method','The seedlings should be transplanted at 2 to 3 cm depth. Shallow planting gives better yields. ','Weed Control\r\nUse Butachlor 50 EC @ 1200 ml/acre or Thiobencarb 50 EC @ 1200 ml or Pendimethalin 30 EC @ 1000 ml or Pretilachlor 50 EC @ 600 ml per acre as pre-emergence herbicides, 2 to 3 days after transplanting. Mix any one of these herbicides in 60 kg of sand per acre and broadcast uniformly in 4-5 cm deep standing water.\r\n\r\nFor broadleaf weed control, apply Metsulfuron 20 WP @ 30 gm/acre in 150 Ltr water as post emergence, 20-25 days after transplanting. Before spray, drained out the standing water from the field and apply irrigation one day after spray.','Keep field flooded up to two weeks after transplanting. When all water gets infiltrated two day after apply irrigation in field. Depth of standing water should not exceed 10 cm. While doing intercultural and weeding operation, drain out excess water from field and irrigate field after completion of this operations. Stop irrigation about a fortnight before maturity to facilitate easy harvesting.','6.0 to 6.8','Reap the yield once the panicles are developing fully as well as the crops get changed significantly yellow. The yield is generally harvested manually by sickles or by blend harvester. The harvested crops, tied up into compact bundles, strike it against really hard surface to split the grains from straw, accompanied by winnowing.','-','The post-harvest method includes some procedures which include the interval from harvest to utilization 1) harvesting 2) threshing 3) cleaning 4) drying 5) warehouse 6) milling then transport to the trade.\r\n\r\nBefore the storage of grains to protect harvested stuff from pest and disease attack, mix 500 gm Neem seed dust with 10 Kg of seed. To protect stored grains from pests attacked Mix Malathion 50 EC@30 ml/3 Ltr of water. Spray for 1002meter storage area at every 15 days.\r\n\r\n','crop_images/rice.jpg');
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

-- Dump completed on 2025-04-29 14:09:21
