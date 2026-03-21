-- Darosa Fietsverhuur - Seed Data
-- 5 Fuell Flluid elektrische bromfietsen
-- Nog geen kentekens (RDW procedure loopt)
-- Locaties: 3x Arnhem Centrum, 1x Arnhem Apartments, 1x Zandvoort

INSERT INTO fietsen (naam, model, type, bereik_km, max_snelheid, status, kenteken, locatie, notities) VALUES
('Fuell Flluid #1', 'Fuell Flluid', 'elektrische bromfiets', 150, 45, 'beschikbaar', NULL, 'arnhem_centrum', 'Kleur: Midnight Black'),
('Fuell Flluid #2', 'Fuell Flluid', 'elektrische bromfiets', 150, 45, 'beschikbaar', NULL, 'arnhem_centrum', 'Kleur: Midnight Black'),
('Fuell Flluid #3', 'Fuell Flluid', 'elektrische bromfiets', 150, 45, 'beschikbaar', NULL, 'arnhem_centrum', 'Kleur: Arctic White'),
('Fuell Flluid #4', 'Fuell Flluid', 'elektrische bromfiets', 150, 45, 'beschikbaar', NULL, 'arnhem_apartments', 'Kleur: Arctic White'),
('Fuell Flluid #5', 'Fuell Flluid', 'elektrische bromfiets', 150, 45, 'beschikbaar', NULL, 'zandvoort', 'Kleur: Midnight Black');
