# Darosa Fietsverhuur - Claude Code Instructies

## Project
Elektrische bromfietsen verhuur voor Darosa Beheer B.V. in Arnhem.
5 Fuell Flluid bromfietsen, bereik 150km, max 45km/u.
Locatie: `E:\scripts\webscraper\CBSbuurt\darosa-fietsverhuur\`
GitHub: AnneVersion/darosa-fietsverhuur
GitHub Pages: anneversion.github.io/darosa-fietsverhuur

## Starten
```bash
python serve.py  # http://localhost:8092
```

## Branch-strategie
- **main** = stabiel/productie
- **develop** = dagelijkse ontwikkeling (standaard werkbranch)
- **feature/*** = nieuwe features, maak aan vanuit develop

## Technisch
- **Server**: Flask op port 8092 (serve.py)
- **Database**: PostgreSQL `darosa_fietsverhuur`, user `postgres`, pw `postgres`
- **Frontend**: Pure HTML/CSS/JS, geen frameworks
- **Thema**: Licht met electric blue (#0066FF), Verdana font

## Bestanden
- `index.html` - Publieke website met reserveringssysteem
- `admin.html` - Admin dashboard met fleet management (wachtwoord: admin)
- `serve.py` - Flask API server
- `sql/01_schema.sql` - Database schema (fietsen, klanten, reserveringen)
- `sql/02_seed.sql` - Seed data (5 Fuell Flluid bromfietsen)

## Database tabellen
- `fietsen` - 5 bromfietsen met status (beschikbaar/verhuurd/onderhoud)
- `klanten` - Klantgegevens (naam, email, telefoon, rijbewijs)
- `reserveringen` - Boekingen met reservering_nr (DR-YYYY-XXXXX)

## Prijsmodel
- Dag: EUR 45 (TODO: update in code), Week: EUR 275, Maand: EUR 950
- Borg: EUR 250 (retour)
- Inclusief: helm, slot, oplader, verzekering

## Features (maart 2026)
- Booking systeem met prijsberekening
- Admin dashboard met fleet management
- RDW rechtszaak: kentekens nog niet afgegeven (15 maanden wachten)
- Rijbewijs AM of B vereist voor huur
- Alle tekst in het Nederlands

## Let op
- Port 8092
- Database moet draaien voor de server start
- Admin wachtwoord: `admin`
- Fietsen hebben nog geen kentekens (RDW procedure loopt)
