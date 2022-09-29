CREATE TABLE `statystyki_osobowe` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_osoby` int NOT NULL,
  `id_rekordu` int NOT NULL,
  `ilosc_wejsc` int NOT NULL,
  `miesiac` varchar(45) NOT NULL,
  `rok` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
