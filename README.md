# Darosa Fietsverhuur

Elektrische bromfietsen verhuur applicatie voor **Darosa Beheer B.V.** in Arnhem.

## Over

Darosa Beheer B.V. verhuurt 5 Fuell Flluid elektrische bromfietsen in Arnhem.
Deze applicatie biedt een publieke website voor klanten en een admin dashboard voor beheer.

## Stack

- **Frontend**: HTML, CSS, JavaScript (geen frameworks)
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Port**: 8092

## Installatie

```bash
# Database aanmaken
PGPASSWORD=postgres psql -U postgres -h localhost -c "CREATE DATABASE darosa_fietsverhuur;"

# Schema laden
PGPASSWORD=postgres psql -U postgres -h localhost -d darosa_fietsverhuur -f sql/01_schema.sql

# Seed data laden (5 fietsen)
PGPASSWORD=postgres psql -U postgres -h localhost -d darosa_fietsverhuur -f sql/02_seed.sql

# Server starten
python serve.py
```

## URL's

- Website: http://localhost:8092
- Admin: http://localhost:8092/admin (wachtwoord: admin)

## API Endpoints

| Methode | Endpoint | Beschrijving |
|---------|----------|-------------|
| GET | /api/fietsen | Lijst alle fietsen |
| GET | /api/fietsen/:id | Enkele fiets |
| PUT | /api/fietsen/:id | Update fiets status |
| GET | /api/beschikbaarheid?van=&tot= | Check beschikbaarheid |
| POST | /api/reservering | Nieuwe reservering |
| GET | /api/reserveringen | Lijst reserveringen |
| PUT | /api/reserveringen/:id | Update reservering |
| GET | /api/klanten | Lijst klanten |
| GET | /api/stats | Dashboard statistieken |
| GET | /api/prijs?van=&tot= | Prijsberekening |

## Tarieven

| Periode | Prijs | Korting |
|---------|-------|--------|
| Per dag | EUR 25 | - |
| Per week | EUR 150 | 14% |
| Per maand | EUR 450 | 40% |
| Borg | EUR 250 | Retour bij inlevering |

## Contact

Darosa Beheer B.V.
Rosendaalsestraat 129, 6824 CD Arnhem
