-- =====================================================
-- Setup for API-features
-- =====================================================

-- 1. Stored Procedure for å liste kunder
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_list_kunder$$

CREATE PROCEDURE sp_list_kunder()
BEGIN
    SELECT KNr, Navn, Adresse, Postnummer, By
    FROM kunde
    ORDER BY Navn ASC;
END$$

DELIMITER ;

-- =====================================================
-- Verify tables exist
-- =====================================================

-- Check ordre_linje table structure (if it exists)
-- Should have: OrdreNr, VNr, Antall, Pris
DESCRIBE ordre_linje;

-- Check kunde table structure
-- Should have: KNr, Navn, Adresse, Postnummer, By
DESCRIBE kunde;

-- Check ordre table
-- Should have: OrdreNr, OrdreDato, SendtDato, BetaltDato, KNr
DESCRIBE ordre;

-- Check vare table
-- Should have: VNr, Betegnelse, Antall, Pris
DESCRIBE vare;
