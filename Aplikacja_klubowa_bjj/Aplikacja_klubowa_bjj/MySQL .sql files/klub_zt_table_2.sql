CREATE TABLE `karnety` (
  `id` int NOT NULL,
  `aktywny_karnet` tinyint NOT NULL,
  `miesiac` varchar(45) NOT NULL,
  `typ_karnetu` varchar(45) NOT NULL,
  `dostepne_treningi_ogolnie` int NOT NULL,
  `pozostale_treningi_w_miesiacu` int NOT NULL,
  `plec` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
