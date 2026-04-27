-- =====================================================
-- Setup for API-features
-- Denne filen oppretter databaseobjektene som oppgaven krever:
-- Stored Procedure for kunder og tabell for unike fakturanummer.
-- =====================================================

-- 1. Stored Procedure for å liste kunder
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_list_kunder$$

CREATE PROCEDURE sp_list_kunder()
BEGIN
    -- Denne prosedyren brukes av API-et når kundelisten skal hentes uten at
    -- SQL-spørringen ligger direkte i Python-ruten.
    SELECT k.KNr,
           CONCAT(k.Fornavn, ' ', k.Etternavn) AS Navn,
           k.Adresse,
           k.PostNr AS Postnummer,
            p.Poststed AS `By`
    FROM kunde k
    LEFT JOIN poststed p ON k.PostNr = p.PostNr
    ORDER BY Navn ASC;
END$$

DELIMITER ;

-- 2. Faktura-tabell for PDF-generering med unikt fakturanummer
CREATE TABLE IF NOT EXISTS faktura (
    -- Tabellen lagrer ett fakturanummer per ordre, slik at samme ordre ikke får
    -- flere ulike fakturanummer ved gjentatt generering.
    FakturaID INT AUTO_INCREMENT PRIMARY KEY,
    FakturaNr VARCHAR(40) NOT NULL UNIQUE,
    OrdreNr INT NOT NULL,
    Opprettet DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalForMoms DECIMAL(12, 2) NOT NULL,
    MomsBelop DECIMAL(12, 2) NOT NULL,
    TotalMedMoms DECIMAL(12, 2) NOT NULL,
    UNIQUE KEY uk_faktura_ordre (OrdreNr)
);

-- =====================================================
-- Verify tables exist
-- =====================================================

-- Check ordre_linje table structure (if it exists)
-- Should have: OrdreNr, VNr, Antall, PrisPrEnhet
DESCRIBE ordrelinje;

-- Check kunde table structure
-- Should have: KNr, Fornavn, Etternavn, Adresse, PostNr
DESCRIBE kunde;

-- Check ordre table
-- Should have: OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr
DESCRIBE ordre;

-- Check vare table
-- Should have: VNr, Betegnelse, Antall, Pris
DESCRIBE vare;
