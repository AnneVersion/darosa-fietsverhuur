-- Darosa Fietsverhuur - Database Schema
-- Darosa Beheer B.V. - Elektrische Bromfietsen Verhuur Arnhem

CREATE TABLE IF NOT EXISTS fietsen (
    id SERIAL PRIMARY KEY,
    naam VARCHAR(100) NOT NULL,
    model VARCHAR(100) DEFAULT 'Fuell Flluid',
    type VARCHAR(50) DEFAULT 'elektrische bromfiets',
    bereik_km INTEGER DEFAULT 150,
    max_snelheid INTEGER DEFAULT 45,
    status VARCHAR(20) DEFAULT 'beschikbaar', -- beschikbaar, verhuurd, onderhoud
    kenteken VARCHAR(20),
    notities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS klanten (
    id SERIAL PRIMARY KEY,
    naam VARCHAR(200) NOT NULL,
    email VARCHAR(320),
    telefoon VARCHAR(20),
    rijbewijs_nr VARCHAR(50),
    adres TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reserveringen (
    id SERIAL PRIMARY KEY,
    reservering_nr VARCHAR(20) UNIQUE NOT NULL,
    fiets_id INTEGER REFERENCES fietsen(id),
    klant_id INTEGER REFERENCES klanten(id),
    ophaal_datum DATE NOT NULL,
    inlever_datum DATE NOT NULL,
    dagprijs DECIMAL(8,2) DEFAULT 25.00,
    totaal DECIMAL(8,2),
    borg DECIMAL(8,2) DEFAULT 250.00,
    status VARCHAR(20) DEFAULT 'bevestigd', -- bevestigd, actief, afgerond, geannuleerd
    notities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index voor snelle beschikbaarheid checks
CREATE INDEX IF NOT EXISTS idx_reserveringen_dates ON reserveringen(ophaal_datum, inlever_datum);
CREATE INDEX IF NOT EXISTS idx_reserveringen_fiets ON reserveringen(fiets_id);
CREATE INDEX IF NOT EXISTS idx_reserveringen_status ON reserveringen(status);
CREATE INDEX IF NOT EXISTS idx_fietsen_status ON fietsen(status);
