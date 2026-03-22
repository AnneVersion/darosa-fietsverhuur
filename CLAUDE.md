# Darosa Fietsverhuur - Claude Code Instructies

## Project
Elektrische bromfietsen verhuur voor Darosa Beheer B.V. in Arnhem.
5 Fuell Flluid bromfietsen, bereik 150km, max 45km/u.

- **Locatie**: `E:\scripts\webscraper\CBSbuurt\darosa-fietsverhuur\`
- **URL**: `http://localhost:8092`
- **GitHub**: AnneVersion/darosa-fietsverhuur
- **GitHub Pages**: anneversion.github.io/darosa-fietsverhuur

## Startup Checklist
1. PostgreSQL moet draaien met database `darosa_fietsverhuur` (user `postgres`, pw `postgres`)
2. Database initialiseren (alleen eerste keer):
   ```bash
   psql -U postgres -d darosa_fietsverhuur -f sql/01_schema.sql
   psql -U postgres -d darosa_fietsverhuur -f sql/02_seed.sql
   psql -U postgres -d darosa_fietsverhuur -f sql/03_locaties.sql
   ```
3. Start de server:
   ```bash
   python serve.py  # http://localhost:8092
   ```
4. Controleer:
   - [ ] Server start zonder errors op port 8092
   - [ ] `http://localhost:8092/` laadt index.html (publieke website)
   - [ ] `http://localhost:8092/admin.html` laadt admin dashboard
   - [ ] Admin login werkt met wachtwoord `admin`
   - [ ] Reserveringsformulier opent en berekent prijzen
   - [ ] Fleet overzicht toont 5 bromfietsen in admin

## Branch-strategie
- **main** = stabiel/productie
- **develop** = dagelijkse ontwikkeling (standaard werkbranch)
- **feature/*** = nieuwe features, maak aan vanuit develop

Werk op `develop`. Alleen mergen naar `main` als het stabiel is.

## Technisch
- **Server**: Flask op port 8092 (`serve.py`)
- **Database**: PostgreSQL `darosa_fietsverhuur`, user `postgres`, pw `postgres`
- **Frontend**: Pure HTML/CSS/JS, geen frameworks
- **Thema**: Natuur/Veluwe -- forest green (#2D5F2D), leaf green (#4CAF50), warm earth (#8B6914), Verdana font

## Bestanden
| Bestand | Functie |
|---------|---------|
| `index.html` | Publieke website met reserveringssysteem |
| `admin.html` | Admin dashboard met fleet management (wachtwoord: `admin`) |
| `serve.py` | Flask API server |
| `optimize_images.py` | Afbeeldingen optimalisatie script |
| `sql/01_schema.sql` | Database schema (fietsen, klanten, reserveringen) |
| `sql/02_seed.sql` | Seed data (5 Fuell Flluid bromfietsen) |
| `sql/03_locaties.sql` | Locatie data |
| `img/` | Afbeeldingen (jpg/jpeg in .gitignore, alleen webp/png in git) |

## Database tabellen
- `fietsen` - 5 bromfietsen met status (beschikbaar/verhuurd/onderhoud)
- `klanten` - Klantgegevens (naam, email, telefoon, rijbewijs)
- `reserveringen` - Boekingen met reservering_nr (DR-YYYY-XXXXX)

## Prijsmodel
| Periode | Prijs |
|---------|-------|
| Dag | EUR 45 |
| Week | EUR 275 |
| Maand | EUR 950 |
| Borg | EUR 250 (retour) |

Inclusief: helm, slot, oplader, verzekering.

## Secties index.html
- Hero: full-screen groene gradient, "Ontdek Arnhem & de Veluwe"
- Natuur: 6 kaarten (Hoge Veluwe, Posbank, Sonsbeek, Meinerswijk, Veluwe, Rijn & IJssel)
- Flora & Fauna: 8 diersoorten
- E-Bikes: Fuell Flluid specs card
- Tarieven: dag/week/maand + Serviced Apartments korting banner (20%)
- Routes: 3 suggestieroutes (Stadsroute 20km, Veluwe 45km, Rivier 35km)
- Praktische Info: ophaallocatie, openingstijden, inclusief items
- FAQ: 7 vragen
- Footer: met "Gebouwd met Claude" badge + link naar Serviced Apartments

## RDW Rechtszaak
- Kentekens nog niet afgegeven (15 maanden wachten)
- Beroep ingediend bij Rechtbank Gelderland
- Fietsen hebben nog geen kentekens (procedure loopt)
- Rijbewijs AM of B vereist voor huur

## Let op
- Port 8092 (geen conflict met andere projecten)
- Database moet draaien voor de server start
- Admin wachtwoord: `admin`
- Alle tekst in het Nederlands
- NL vlag favicon
- `.gitignore`: `__pycache__/`, `.env`, `*.log`, `img/*.jpg`, `img/*.jpeg`, `optimize_images.py`
