-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: lili
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cardapio`
--

DROP TABLE IF EXISTS `Cardapio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cardapio` (
  `id_cardapio` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(20) NOT NULL COMMENT 'Nome do Produto',
  `gramatura` int NOT NULL COMMENT 'Os produtos são divididos em categorias por peso 250g, 500g, 1000g',
  `tempo_forno` varchar(45) NOT NULL,
  `validade` varchar(45) NOT NULL,
  PRIMARY KEY (`id_cardapio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Destina-se aos Itens de Produção e Vendas';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cardapio`
--

LOCK TABLES `Cardapio` WRITE;
/*!40000 ALTER TABLE `Cardapio` DISABLE KEYS */;
/*!40000 ALTER TABLE `Cardapio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Compras`
--

DROP TABLE IF EXISTS `Compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Compras` (
  `idCompras` int NOT NULL AUTO_INCREMENT,
  `idInsumos` int NOT NULL,
  `quantidade` float NOT NULL,
  `unidade` varchar(5) NOT NULL COMMENT 'Referencia a unidade de medida *Analizando se é melhor fazer uma conversão via software.\nunidade = [ kg, L, g, ml , unid]',
  `valor` decimal(10,2) NOT NULL,
  `validade` date NOT NULL,
  `fornecedor` varchar(45) NOT NULL,
  `menor_parte` float NOT NULL COMMENT 'transformar as unidades a menor parte para uso.',
  `valor_medio` decimal(10,5) NOT NULL COMMENT 'valor médio =  quantidade/valor',
  `idMov` int DEFAULT NULL,
  PRIMARY KEY (`idCompras`),
  KEY `fk_Compras_1_idx` (`idInsumos`),
  KEY `fk_Compras_2_idx` (`idMov`),
  CONSTRAINT `fk_Compras_1` FOREIGN KEY (`idInsumos`) REFERENCES `Insumos` (`idInsumos`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_Compras_2` FOREIGN KEY (`idMov`) REFERENCES `Movimentacoes` (`idMov`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Compras`
--

LOCK TABLES `Compras` WRITE;
/*!40000 ALTER TABLE `Compras` DISABLE KEYS */;
/*!40000 ALTER TABLE `Compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Endereco`
--

DROP TABLE IF EXISTS `Endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Endereco` (
  `id_endereco` int NOT NULL AUTO_INCREMENT,
  `rua_av` varchar(100) NOT NULL,
  `numero` varchar(10) DEFAULT NULL,
  `complemento` varchar(20) DEFAULT NULL,
  `tipo` enum('RESINDENCIAL','COMERCIAL') NOT NULL,
  `id_pessoa` int NOT NULL,
  PRIMARY KEY (`id_endereco`),
  KEY `fk_Endereco_1_idx` (`id_pessoa`),
  CONSTRAINT `fk_Endereco_1` FOREIGN KEY (`id_pessoa`) REFERENCES `Pessoa` (`id_pessoa`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Endereco`
--

LOCK TABLES `Endereco` WRITE;
/*!40000 ALTER TABLE `Endereco` DISABLE KEYS */;
/*!40000 ALTER TABLE `Endereco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ficha_Tecnica`
--

DROP TABLE IF EXISTS `Ficha_Tecnica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ficha_Tecnica` (
  `id_Ficha_Tecnica` int NOT NULL AUTO_INCREMENT,
  `cardapio` int NOT NULL,
  `ingredientes` int NOT NULL,
  `tempo_preparo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_Ficha_Tecnica`),
  KEY `fk_cardapio_1_idx` (`cardapio`),
  KEY `fk_ingredientes_1_idx` (`ingredientes`),
  CONSTRAINT `fk_cardapio_1` FOREIGN KEY (`cardapio`) REFERENCES `Cardapio` (`id_cardapio`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ingredientes_1` FOREIGN KEY (`ingredientes`) REFERENCES `Ingredientes` (`id_ingredientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Ficha Técnica é feita na área de produção dos Produtos pelo surpervisor e/ou gerente, \ndetalha todo material usado e quantidades necessárias para cada item do cárdapio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ficha_Tecnica`
--

LOCK TABLES `Ficha_Tecnica` WRITE;
/*!40000 ALTER TABLE `Ficha_Tecnica` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ficha_Tecnica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fone`
--

DROP TABLE IF EXISTS `Fone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fone` (
  `id_fone` int NOT NULL AUTO_INCREMENT,
  `fone` varchar(45) NOT NULL,
  `pessoa_id` int NOT NULL,
  PRIMARY KEY (`id_fone`),
  KEY `fk_Fone_1_idx` (`pessoa_id`),
  CONSTRAINT `fk_Fone_1` FOREIGN KEY (`pessoa_id`) REFERENCES `Pessoa` (`id_pessoa`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fone`
--

LOCK TABLES `Fone` WRITE;
/*!40000 ALTER TABLE `Fone` DISABLE KEYS */;
/*!40000 ALTER TABLE `Fone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ingredientes`
--

DROP TABLE IF EXISTS `Ingredientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ingredientes` (
  `id_ingredientes` int NOT NULL AUTO_INCREMENT,
  `quantidade` float NOT NULL,
  `unidade` varchar(5) NOT NULL,
  `categoria` varchar(12) NOT NULL,
  `Insumos_idInsumos` int NOT NULL,
  PRIMARY KEY (`id_ingredientes`),
  KEY `fk_Ingredientes_Insumos1_idx` (`Insumos_idInsumos`),
  CONSTRAINT `fk_Ingredientes_Insumos1` FOREIGN KEY (`Insumos_idInsumos`) REFERENCES `Insumos` (`idInsumos`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Somente os igredientes de acordo com cada tabela "ficha técnica" do cardapio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ingredientes`
--

LOCK TABLES `Ingredientes` WRITE;
/*!40000 ALTER TABLE `Ingredientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ingredientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Insumos`
--

DROP TABLE IF EXISTS `Insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Insumos` (
  `idInsumos` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `categoria` varchar(15) NOT NULL COMMENT 'define um da lista ["Cereal","Descartável", "Embutidos", "Embalagen", "Enlatados", "Fruta","Tempêro",\n                    "Laticínio","Legume","Limpeza", "Óleo", "Proteína","Verdura", "Outro"]',
  PRIMARY KEY (`idInsumos`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COMMENT='Entrada dos insumos';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Insumos`
--

LOCK TABLES `Insumos` WRITE;
/*!40000 ALTER TABLE `Insumos` DISABLE KEYS */;
INSERT INTO `Insumos` VALUES (1,'farinha de trigo','cereal'),(2,'ovos','proteina'),(3,'açucar','cereal');
/*!40000 ALTER TABLE `Insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Movimentacoes`
--

DROP TABLE IF EXISTS `Movimentacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Movimentacoes` (
  `idMov` int NOT NULL AUTO_INCREMENT,
  `idInsumos` int NOT NULL COMMENT 'Qual o insumo está sendo referenciado',
  `tipo` enum('ENTRADA','SAIDA') NOT NULL COMMENT 'Define o tipo de operação no estoque [Entrada ou Saída]',
  `quantidade` float NOT NULL,
  `data_mov` datetime NOT NULL,
  PRIMARY KEY (`idMov`),
  KEY `fk_Movimentacoes_1_idx` (`idInsumos`),
  CONSTRAINT `fk_Movimentacoes_1` FOREIGN KEY (`idInsumos`) REFERENCES `Insumos` (`idInsumos`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9005 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Controla a Movimentação de entrada e saida de cada insumo do estoque.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Movimentacoes`
--

LOCK TABLES `Movimentacoes` WRITE;
/*!40000 ALTER TABLE `Movimentacoes` DISABLE KEYS */;
INSERT INTO `Movimentacoes` VALUES (9000,1,'ENTRADA',10,'2025-08-23 00:00:00'),(9001,1,'SAIDA',5,'2025-08-23 00:00:00'),(9002,2,'ENTRADA',12,'2025-08-23 00:00:00'),(9003,2,'SAIDA',4,'2025-08-23 00:00:00'),(9004,3,'ENTRADA',7,'2025-08-23 00:00:00');
/*!40000 ALTER TABLE `Movimentacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pessoa`
--

DROP TABLE IF EXISTS `Pessoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pessoa` (
  `id_pessoa` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL COMMENT 'Somente primeiro nome',
  `sobrenome` varchar(150) NOT NULL COMMENT 'sobrenome completo',
  `cpf` varchar(11) NOT NULL COMMENT 'cpf , numero com restrição UNIQUE , não é possível números iguais de CPF',
  `data_nasc` date NOT NULL,
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pessoa`),
  UNIQUE KEY `cpf_UNIQUE` (`cpf`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pessoa`
--

LOCK TABLES `Pessoa` WRITE;
/*!40000 ALTER TABLE `Pessoa` DISABLE KEYS */;
/*!40000 ALTER TABLE `Pessoa` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-24 16:56:23
