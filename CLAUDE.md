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
- **Thema**: Natuur/Veluwe — forest green (#2D5F2D), leaf green (#4CAF50), warm earth (#8B6914), Verdana font

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
- Dag: EUR 45, Week: EUR 275, Maand: EUR 950
- Borg: EUR 250 (retour)
- Inclusief: helm, slot, oplader, verzekering

## Secties index.html
- Hero: full-screen groene gradient, "Ontdek Arnhem & de Veluwe"
- Natuur: 6 kaarten (Hoge Veluwe, Posbank, Sonsbeek, Meinerswijk, Veluwe, Rijn & IJssel)
- Flora & Fauna: 8 diersoorten (edelhert, wild zwijn, vos, zeearend, bever, konikpaard, ijsvogel, heideblauwtje)
- E-Bikes: Fuell Flluid specs card
- Tarieven: dag/week/maand + Serviced Apartments korting banner (20%)
- Routes: 3 suggestieroutes (Stadsroute 20km, Veluwe 45km, Rivier 35km)
- Praktische Info: ophaallocatie, openingstijden, inclusief items
- FAQ: 7 vragen
- Footer: met "Gebouwd met Claude" badge + link naar Serviced Apartments

## Features (maart 2026)
- Booking systeem met prijsberekening (EUR 45/275/950)
- Admin dashboard met fleet management
- RDW rechtszaak: kentekens nog niet afgegeven (15 maanden wachten)
- Rijbewijs AM of B vereist voor huur
- Alle tekst in het Nederlands
- NL vlag favicon

## Let op
- Port 8092
- Database moet draaien voor de server start
- Admin wachtwoord: `admin`
- Fietsen hebben nog geen kentekens (RDW procedure loopt)
