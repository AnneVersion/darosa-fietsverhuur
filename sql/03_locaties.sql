-- Darosa Fietsverhuur - Locaties migratie
-- 3 verhuurlocaties: Arnhem Centrum, Arnhem Apartments, Zandvoort aan Zee

-- Locatie kolom toevoegen aan fietsen
ALTER TABLE fietsen ADD COLUMN IF NOT EXISTS locatie VARCHAR(50) DEFAULT 'arnhem_centrum';

-- Ophaallocatie kolom toevoegen aan reserveringen
ALTER TABLE reserveringen ADD COLUMN IF NOT EXISTS ophaal_locatie VARCHAR(50) DEFAULT 'arnhem_centrum';

-- Fietsen toewijzen aan locaties (3 Arnhem, 1 Arnhem Apartments, 1 Zandvoort)
UPDATE fietsen SET locatie = 'arnhem_centrum' WHERE id IN (1, 2, 3);
UPDATE fietsen SET locatie = 'arnhem_apartments' WHERE id = 4;
UPDATE fietsen SET locatie = 'zandvoort' WHERE id = 5;
