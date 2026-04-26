-- =====================================================
-- Setup for API-features
-- =====================================================

-- 1. Stored Procedure for å liste kunder
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_list_kunder$$

CREATE PROCEDURE sp_list_kunder()
BEGIN
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
