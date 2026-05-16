-- Opprett DB-bruker for Ram (MySQL 8+)
-- Kjor dette som en admin-bruker som har CREATE USER/GRANT-rettigheter.

-- Bytt ut passordet med et sterkt passord.
CREATE USER IF NOT EXISTS 'ram'@'%' IDENTIFIED BY 'ByttTilSterktPassord!2026';
ALTER USER 'ram'@'%' IDENTIFIED BY 'ByttTilSterktPassord!2026';

-- Minste rettigheter for prosjektet (lesing + CRUD + execute stored procedures)
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON `varehusdb`.* TO 'ram'@'%';
FLUSH PRIVILEGES;

-- Verifiser rettigheter
SHOW GRANTS FOR 'ram'@'%';
