CREATE TABLE `dodatkowe_info_osoby` (
  `id_osoby` int NOT NULL,
  `pierwszy_trening` date NOT NULL,
  `data_urodzenia` date DEFAULT NULL,
  PRIMARY KEY (`id_osoby`),
  UNIQUE KEY `id_dodatkowe_info_osoby_UNIQUE` (`id_osoby`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
