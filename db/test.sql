-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: test_db
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `salary` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (4,'Backend Developer', 300.0),(3,'Communications Dispatch', 500.0),(6,'Design', 100.0),(5,'Frontend Developer',123.2),(2,'Human resources',3333.2),(7,'Management',33.1);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `department_id` int NOT NULL,
  `role_id` int NOT NULL,
  `birth_date` date NOT NULL,
  `salary` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `department_id` (`department_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`),
  CONSTRAINT `employee_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (5,'James','Smith','james@gmail.com','$2b$12$vfDxDGX0fhchIeRMxVeXhuNnZFNhleBNUzzxFEIBLJq0A6Ymc1EeS',6,3,'1980-11-11',600),(6,'James','Murray','j@gmail.com','$2b$12$CZKYM97iSZrhJy9j4F8Lb.ENMhiRxWqvD4egxzacEPnNM26IMMSm.',7,3,'1996-04-17',720),(7,'Ben','Dover','ben@gmail.com','$2b$12$jxJa3aEJzy80CoXmeDP9NeYVzUUSXOVEK4TTt62KSVP2E6ee9B6Ua',3,4,'1980-11-05',1890),(8,'Dave','Hubert','dave@gmail.com','$2b$12$xP00QuY/cE7bVaVJbYtZ1O6gMgObaOKQ3fHOLlUyXFOTUsiXQs636',6,3,'1995-11-09',700),(9,'Rinat','Minnakhmetov','rinnik228@gmail.com','sha256$ZmOeNXDgMLYswQTB$f312adad3c15512023642bada27e1e6577fc54b8220ba13d9afa40b6db610d9e',4,3,'2002-11-27',627.26),(10,'Kyle','Stevens','kyle@gmail.com','$2b$12$Ix2/OCZzXezc/BLAxasxqe2jmAFcUnY/YCsntJs1h8xnRZrEXpQ0q',7,3,'1989-06-13',800),(11,'Lima','Martinez','lima@gmail.com','$2b$12$K9kLkVvPzUOsoQbNW.Z.OOv4WwMW7YEWHLyV.YuY2qZCEGcqKjmKu',6,3,'1992-10-15',600),(12,'Waldo','Bruno','intermemes@gmail.com','$2b$12$p4H8eg.gmWhDy6Hrny29COhYrROEvFDtPEr2yunFG/NRVcs0UmydW',4,3,'1995-02-28',500),(15,'Miguel','Menger','miguel@gmail.com','$2b$12$D6uXsUEa5HS24c8TMCyd1eAhAID/5GrPKKZbcBi/TCOwduULbGbb2',4,3,'1999-12-02',0);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender` int NOT NULL,
  `change_department_id` int DEFAULT NULL,
  `increase_salary` int DEFAULT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `change_department_id` (`change_department_id`),
  KEY `sender` (`sender`),
  CONSTRAINT `request_ibfk_3` FOREIGN KEY (`sender`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (15,9,3,0,2),(16,5,6,0,2),(17,5,6,5,2),(18,11,2,1,2),(19,6,7,20,1),(20,6,6,0,2),(21,9,0,20,2),(22,9,3,0,1),(23,9,0,10,1),(24,9,4,20,2),(25,9,4,20,2),(26,9,4,20,2),(27,9,4,20,1),(28,5,6,0,1),(30,5,4,5,0);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (4,'admin'),(3,'regular');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-29 20:03:05
