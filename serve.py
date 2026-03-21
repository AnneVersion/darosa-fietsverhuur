"""
Darosa Fietsverhuur - Flask API Server
Darosa Beheer B.V. - Elektrische Bromfietsen Verhuur Arnhem
Port: 8092
"""

import os
import sys
import json
import random
import string
from datetime import datetime, date, timedelta
from decimal import Decimal
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS

import psycopg2
import psycopg2.extras

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database configuratie
DB_CONFIG = {
    'dbname': 'darosa_fietsverhuur',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}


def get_db():
    """Maak database connectie."""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def query_db(sql, params=None, fetchone=False):
    """Voer een query uit en retourneer resultaten als dict."""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params)
        if sql.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            if 'RETURNING' in sql.upper():
                result = cur.fetchone() if fetchone else cur.fetchall()
                return result
            return None
        if fetchone:
            return cur.fetchone()
        return cur.fetchall()
    finally:
        conn.close()


def genereer_reservering_nr():
    """Genereer uniek reserveringsnummer: DR-2026-XXXXX."""
    jaar = datetime.now().year
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"DR-{jaar}-{code}"


def bereken_prijs(ophaal_datum, inlever_datum):
    """Bereken prijs op basis van duur met kortingen."""
    if isinstance(ophaal_datum, str):
        ophaal_datum = datetime.strptime(ophaal_datum, '%Y-%m-%d').date()
    if isinstance(inlever_datum, str):
        inlever_datum = datetime.strptime(inlever_datum, '%Y-%m-%d').date()

    dagen = (inlever_datum - ophaal_datum).days
    if dagen <= 0:
        dagen = 1

    if dagen >= 30:
        # Maandtarief: €450 per 30 dagen
        maanden = dagen / 30
        totaal = maanden * 450
        dagprijs = totaal / dagen
    elif dagen >= 7:
        # Weektarief: €150 per 7 dagen
        weken = dagen / 7
        totaal = weken * 150
        dagprijs = totaal / dagen
    else:
        # Dagtarief: €25 per dag
        dagprijs = 25
        totaal = dagen * dagprijs

    return {
        'dagen': dagen,
        'dagprijs': round(dagprijs, 2),
        'totaal': round(totaal, 2),
        'borg': 250.00
    }


# ============================================================
# Statische bestanden
# ============================================================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/admin')
@app.route('/admin.html')
def admin():
    return send_from_directory('.', 'admin.html')


# ============================================================
# API: Fietsen
# ============================================================

@app.route('/api/fietsen', methods=['GET'])
def get_fietsen():
    """Lijst van alle fietsen met status, optioneel gefilterd op locatie."""
    locatie = request.args.get('locatie')
    sql = """
        SELECT f.*,
            (SELECT COUNT(*) FROM reserveringen r
             WHERE r.fiets_id = f.id
             AND r.status IN ('bevestigd', 'actief')
             AND r.ophaal_datum <= CURRENT_DATE
             AND r.inlever_datum >= CURRENT_DATE) as actief_verhuurd
        FROM fietsen f
    """
    params = []
    if locatie:
        sql += " WHERE f.locatie = %s"
        params.append(locatie)
    sql += " ORDER BY f.id"

    fietsen = query_db(sql, params if params else None)
    result = []
    for f in fietsen:
        fiets = dict(f)
        fiets['created_at'] = fiets['created_at'].isoformat() if fiets['created_at'] else None
        result.append(fiets)
    return jsonify(result)


@app.route('/api/fietsen/<int:fiets_id>', methods=['GET'])
def get_fiets(fiets_id):
    """Enkele fiets met details."""
    fiets = query_db("SELECT * FROM fietsen WHERE id = %s", (fiets_id,), fetchone=True)
    if not fiets:
        return jsonify({'error': 'Fiets niet gevonden'}), 404
    result = dict(fiets)
    result['created_at'] = result['created_at'].isoformat() if result['created_at'] else None
    return jsonify(result)


@app.route('/api/fietsen/<int:fiets_id>', methods=['PUT'])
def update_fiets(fiets_id):
    """Update fiets status/notities."""
    data = request.get_json()
    updates = []
    params = []
    for veld in ['status', 'kenteken', 'locatie', 'notities']:
        if veld in data:
            updates.append(f"{veld} = %s")
            params.append(data[veld])
    if not updates:
        return jsonify({'error': 'Geen velden om te updaten'}), 400
    params.append(fiets_id)
    query_db(f"UPDATE fietsen SET {', '.join(updates)} WHERE id = %s", params)
    return jsonify({'success': True})


# ============================================================
# API: Beschikbaarheid
# ============================================================

@app.route('/api/beschikbaarheid', methods=['GET'])
def check_beschikbaarheid():
    """Check beschikbare fietsen voor een datumbereik, optioneel gefilterd op locatie."""
    van = request.args.get('van')
    tot = request.args.get('tot')
    locatie = request.args.get('locatie')
    if not van or not tot:
        return jsonify({'error': 'Parameters van en tot zijn verplicht'}), 400

    sql = """
        SELECT f.* FROM fietsen f
        WHERE f.status != 'onderhoud'
        AND f.id NOT IN (
            SELECT r.fiets_id FROM reserveringen r
            WHERE r.status IN ('bevestigd', 'actief')
            AND r.ophaal_datum < %s
            AND r.inlever_datum > %s
        )
    """
    params = [tot, van]
    if locatie:
        sql += " AND f.locatie = %s"
        params.append(locatie)
    sql += " ORDER BY f.id"

    beschikbaar = query_db(sql, params)

    result = []
    for f in beschikbaar:
        fiets = dict(f)
        fiets['created_at'] = fiets['created_at'].isoformat() if fiets['created_at'] else None
        result.append(fiets)

    prijs = bereken_prijs(van, tot)
    return jsonify({
        'beschikbaar': result,
        'aantal_beschikbaar': len(result),
        'prijs': prijs
    })


# ============================================================
# API: Reserveringen
# ============================================================

@app.route('/api/reservering', methods=['POST'])
def maak_reservering():
    """Maak een nieuwe reservering aan."""
    data = request.get_json()

    # Validatie
    required = ['fiets_id', 'ophaal_datum', 'inlever_datum', 'naam']
    for veld in required:
        if veld not in data or not data[veld]:
            return jsonify({'error': f'Veld {veld} is verplicht'}), 400

    # Check beschikbaarheid
    conflict = query_db("""
        SELECT id FROM reserveringen
        WHERE fiets_id = %s
        AND status IN ('bevestigd', 'actief')
        AND ophaal_datum < %s
        AND inlever_datum > %s
    """, (data['fiets_id'], data['inlever_datum'], data['ophaal_datum']))

    if conflict:
        return jsonify({'error': 'Deze fiets is niet beschikbaar voor de gekozen periode'}), 409

    # Check fiets status
    fiets = query_db("SELECT status FROM fietsen WHERE id = %s", (data['fiets_id'],), fetchone=True)
    if not fiets:
        return jsonify({'error': 'Fiets niet gevonden'}), 404
    if fiets['status'] == 'onderhoud':
        return jsonify({'error': 'Deze fiets is momenteel in onderhoud'}), 409

    # Klant aanmaken of ophalen
    klant = None
    if data.get('email'):
        klant = query_db("SELECT id FROM klanten WHERE email = %s", (data['email'],), fetchone=True)

    if not klant:
        klant = query_db("""
            INSERT INTO klanten (naam, email, telefoon, rijbewijs_nr, adres)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data['naam'],
            data.get('email'),
            data.get('telefoon'),
            data.get('rijbewijs_nr'),
            data.get('adres')
        ), fetchone=True)

    # Prijs berekenen
    prijs = bereken_prijs(data['ophaal_datum'], data['inlever_datum'])
    reservering_nr = genereer_reservering_nr()

    # Reservering aanmaken
    reservering = query_db("""
        INSERT INTO reserveringen (reservering_nr, fiets_id, klant_id, ophaal_datum, inlever_datum, dagprijs, totaal, borg, ophaal_locatie, status, notities)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'bevestigd', %s)
        RETURNING id, reservering_nr, totaal, borg
    """, (
        reservering_nr,
        data['fiets_id'],
        klant['id'],
        data['ophaal_datum'],
        data['inlever_datum'],
        prijs['dagprijs'],
        prijs['totaal'],
        250.00,
        data.get('ophaal_locatie', 'arnhem_centrum'),
        data.get('notities')
    ), fetchone=True)

    return jsonify({
        'success': True,
        'reservering': dict(reservering),
        'prijs': prijs
    }), 201


@app.route('/api/reserveringen', methods=['GET'])
def get_reserveringen():
    """Lijst van alle reserveringen."""
    status_filter = request.args.get('status')
    sql = """
        SELECT r.*, f.naam as fiets_naam, k.naam as klant_naam, k.email as klant_email, k.telefoon as klant_telefoon
        FROM reserveringen r
        JOIN fietsen f ON r.fiets_id = f.id
        JOIN klanten k ON r.klant_id = k.id
    """
    params = []
    if status_filter:
        sql += " WHERE r.status = %s"
        params.append(status_filter)
    sql += " ORDER BY r.created_at DESC"

    reserveringen = query_db(sql, params if params else None)
    result = []
    for r in reserveringen:
        res = dict(r)
        for key in ['ophaal_datum', 'inlever_datum', 'created_at']:
            if res.get(key):
                res[key] = res[key].isoformat()
        for key in ['dagprijs', 'totaal', 'borg']:
            if res.get(key):
                res[key] = float(res[key])
        result.append(res)
    return jsonify(result)


@app.route('/api/reserveringen/<int:res_id>', methods=['PUT'])
def update_reservering(res_id):
    """Update reservering status."""
    data = request.get_json()
    updates = []
    params = []
    for veld in ['status', 'notities']:
        if veld in data:
            updates.append(f"{veld} = %s")
            params.append(data[veld])
    if not updates:
        return jsonify({'error': 'Geen velden om te updaten'}), 400
    params.append(res_id)
    query_db(f"UPDATE reserveringen SET {', '.join(updates)} WHERE id = %s", params)

    # Als reservering actief wordt, update fiets status
    if data.get('status') == 'actief':
        fiets = query_db("SELECT fiets_id FROM reserveringen WHERE id = %s", (res_id,), fetchone=True)
        if fiets:
            query_db("UPDATE fietsen SET status = 'verhuurd' WHERE id = %s", (fiets['fiets_id'],))
    elif data.get('status') in ('afgerond', 'geannuleerd'):
        fiets = query_db("SELECT fiets_id FROM reserveringen WHERE id = %s", (res_id,), fetchone=True)
        if fiets:
            query_db("UPDATE fietsen SET status = 'beschikbaar' WHERE id = %s", (fiets['fiets_id'],))

    return jsonify({'success': True})


# ============================================================
# API: Klanten
# ============================================================

@app.route('/api/klanten', methods=['GET'])
def get_klanten():
    """Lijst van alle klanten."""
    klanten = query_db("""
        SELECT k.*,
            (SELECT COUNT(*) FROM reserveringen r WHERE r.klant_id = k.id) as aantal_reserveringen
        FROM klanten k
        ORDER BY k.created_at DESC
    """)
    result = []
    for k in klanten:
        klant = dict(k)
        klant['created_at'] = klant['created_at'].isoformat() if klant['created_at'] else None
        result.append(klant)
    return jsonify(result)


# ============================================================
# API: Locaties
# ============================================================

LOCATIES = {
    'arnhem_centrum': {
        'id': 'arnhem_centrum',
        'naam': 'Arnhem Centrum',
        'type': 'Los huren',
        'adres': 'Rosendaalsestraat 129, 6824 CD Arnhem',
        'lat': 51.9851,
        'lng': 5.9115,
        'beschrijving': 'Voor iedereen — toeristen, forensen, locals',
        'highlights': 'Nabij: Veluwe, Sonsbeek, centrum',
        'korting': None
    },
    'arnhem_apartments': {
        'id': 'arnhem_apartments',
        'naam': 'Arnhem Apartments',
        'type': 'Bij short-stay',
        'adres': 'Bij de Serviced Apartments',
        'lat': 51.9794,
        'lng': 5.9096,
        'beschrijving': '20% korting voor appartement huurders',
        'highlights': 'Bij de Serviced Apartments studio\'s',
        'korting': 20
    },
    'zandvoort': {
        'id': 'zandvoort',
        'naam': 'Zandvoort aan Zee',
        'type': 'Bij short-stay',
        'adres': 'Bij het strandappartement, Zandvoort',
        'lat': 52.3727,
        'lng': 4.5330,
        'beschrijving': 'Fietsen langs de kust, duinen, strand',
        'highlights': '20% korting voor appartement huurders',
        'korting': 20
    }
}


@app.route('/api/locaties', methods=['GET'])
def get_locaties():
    """Lijst van alle verhuurlocaties met beschikbare fietsen."""
    result = []
    for loc_id, loc in LOCATIES.items():
        beschikbaar = query_db(
            "SELECT COUNT(*) as count FROM fietsen WHERE locatie = %s AND status = 'beschikbaar'",
            (loc_id,), fetchone=True
        )
        loc_data = dict(loc)
        loc_data['beschikbaar'] = beschikbaar['count'] if beschikbaar else 0
        result.append(loc_data)
    return jsonify(result)


# ============================================================
# API: Statistieken
# ============================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Dashboard statistieken."""
    totaal_fietsen = query_db("SELECT COUNT(*) as count FROM fietsen", fetchone=True)['count']
    beschikbaar = query_db("SELECT COUNT(*) as count FROM fietsen WHERE status = 'beschikbaar'", fetchone=True)['count']
    verhuurd = query_db("SELECT COUNT(*) as count FROM fietsen WHERE status = 'verhuurd'", fetchone=True)['count']
    onderhoud = query_db("SELECT COUNT(*) as count FROM fietsen WHERE status = 'onderhoud'", fetchone=True)['count']

    actieve_reserveringen = query_db(
        "SELECT COUNT(*) as count FROM reserveringen WHERE status IN ('bevestigd', 'actief')",
        fetchone=True
    )['count']

    totaal_reserveringen = query_db("SELECT COUNT(*) as count FROM reserveringen", fetchone=True)['count']
    totaal_klanten = query_db("SELECT COUNT(*) as count FROM klanten", fetchone=True)['count']

    # Omzet deze maand
    omzet_maand = query_db("""
        SELECT COALESCE(SUM(totaal), 0) as omzet
        FROM reserveringen
        WHERE status IN ('actief', 'afgerond')
        AND DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)
    """, fetchone=True)

    # Omzet totaal
    omzet_totaal = query_db("""
        SELECT COALESCE(SUM(totaal), 0) as omzet
        FROM reserveringen
        WHERE status IN ('actief', 'afgerond')
    """, fetchone=True)

    # Omzet per week (laatste 8 weken)
    omzet_per_week = query_db("""
        SELECT DATE_TRUNC('week', created_at)::date as week,
               COALESCE(SUM(totaal), 0) as omzet,
               COUNT(*) as aantal
        FROM reserveringen
        WHERE status IN ('actief', 'afgerond')
        AND created_at >= CURRENT_DATE - INTERVAL '8 weeks'
        GROUP BY DATE_TRUNC('week', created_at)
        ORDER BY week DESC
    """)

    omzet_weken = []
    for w in (omzet_per_week or []):
        omzet_weken.append({
            'week': w['week'].isoformat(),
            'omzet': float(w['omzet']),
            'aantal': w['aantal']
        })

    return jsonify({
        'fietsen': {
            'totaal': totaal_fietsen,
            'beschikbaar': beschikbaar,
            'verhuurd': verhuurd,
            'onderhoud': onderhoud
        },
        'reserveringen': {
            'actief': actieve_reserveringen,
            'totaal': totaal_reserveringen
        },
        'klanten': totaal_klanten,
        'omzet': {
            'deze_maand': float(omzet_maand['omzet']),
            'totaal': float(omzet_totaal['omzet']),
            'per_week': omzet_weken
        }
    })


# ============================================================
# API: Prijsberekening
# ============================================================

@app.route('/api/prijs', methods=['GET'])
def bereken_prijs_api():
    """Bereken prijs voor een datumbereik."""
    van = request.args.get('van')
    tot = request.args.get('tot')
    if not van or not tot:
        return jsonify({'error': 'Parameters van en tot zijn verplicht'}), 400
    prijs = bereken_prijs(van, tot)
    return jsonify(prijs)


# ============================================================
# Start server
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  Darosa Fietsverhuur - Elektrische Bromfietsen Arnhem")
    print("  Darosa Beheer B.V.")
    print("  http://localhost:8092")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8092, debug=True)
