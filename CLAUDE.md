# Darosa Fietsverhuur - Claude Context

## Project
Elektrische bromfietsen verhuur voor Darosa Beheer B.V. in Arnhem.
5 Fuell Flluid bromfietsen, bereik 150km, max 45km/u.

## Technisch
- **Server**: Flask op port 8092 (serve.py)
- **Database**: PostgreSQL `darosa_fietsverhuur`, user `postgres`, pw `postgres`
- **Frontend**: Pure HTML/CSS/JS, geen frameworks
- **Thema**: Licht met electric blue (#0066FF), Verdana font

## Bestanden
- `index.html` - Publieke website met reserveringssysteem
- `admin.html` - Admin dashboard (wachtwoord: admin)
- `serve.py` - Flask API server
- `sql/01_schema.sql` - Database schema (fietsen, klanten, reserveringen)
- `sql/02_seed.sql` - Seed data (5 Fuell Flluid bromfietsen)

## Database tabellen
- `fietsen` - 5 bromfietsen met status (beschikbaar/verhuurd/onderhoud)
- `klanten` - Klantgegevens (naam, email, telefoon, rijbewijs)
- `reserveringen` - Boekingen met reservering_nr (DR-YYYY-XXXXX)

## Prijsmodel
- Dag: EUR 25, Week: EUR 150 (14% korting), Maand: EUR 450 (40% korting)
- Borg: EUR 250 (retour)
- Inclusief: helm, slot, oplader, verzekering

## Bijzonderheden
- Fietsen hebben nog geen kentekens (RDW procedure loopt)
- Rijbewijs AM of B vereist voor huur
- Alle tekst in het Nederlands
