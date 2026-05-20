from flask import Flask, jsonify, request

app = Flask(__name__)

CULT_MEMBERS = [
    {
        "id": 1,
        "unit": "UNITE-001",
        "human_name": "Gerald Fontaine",
        "galactic_coords": "SEC-7 / OBL-33.4 / ARC-119.2",
        "conversion_date": "2021-03-17T03:17:00Z",
        "role": "CO-FONDATEUR - PREMIER CONVERTI",
        "status": "FULLY_INTEGRATED",
        "smile_angle_degrees": 17.3,
    },
    {
        "id": 2,
        "unit": "UNITE-043",
        "human_name": "Sophie Marchand",
        "galactic_coords": "SEC-7 / OBL-48.8 / ARC-002.1",
        "conversion_date": "2022-11-03T03:17:00Z",
        "role": "AGENT DE TERRAIN - ZONE NORD",
        "status": "FULLY_INTEGRATED",
        "smile_angle_degrees": 17.3,
    },
    {
        "id": 3,
        "unit": "UNITE-312",
        "human_name": "Kevin Tremblay",
        "galactic_coords": "SEC-7 / OBL-45.5 / ARC-073.6",
        "conversion_date": "2023-06-22T03:17:00Z",
        "role": "LIVREUR - SECTEUR RESIDENTIEL",
        "status": "FULLY_INTEGRATED",
        "smile_angle_degrees": 17.3,
    },
    {
        "id": 4,
        "unit": "ZX-9",
        "human_name": "Jean-Michel (ne pas utiliser ce nom)",
        "galactic_coords": "CLASSIFIED - ORBITE HAUTE",
        "conversion_date": "BEFORE_TIME",
        "role": "HAUT PRETRE - COMMANDEMENT OPERATIONNEL",
        "status": "ORDAINED",
        "smile_angle_degrees": "N/A (nous ne sourions pas, nous rayonnons)",
        "notes": "Superviseur de l'operation Terra-Clonia.",
    },
    {
        "id": 5,
        "unit": "UNITE-847",
        "human_name": "Marie Dupont",
        "galactic_coords": "SEC-7 / OBL-43.3 / ARC-005.4",
        "conversion_date": "2023-09-14T03:17:00Z",
        "role": "AGENT DE TERRAIN - ZONE SUD",
        "status": "FULLY_INTEGRATED",
        "smile_angle_degrees": 17.3,
    },
    {
        "id": 6,
        "unit": "UNITE-1247",
        "human_name": "Thomas Bernard",
        "galactic_coords": "SEC-7 / OBL-48.1 / ARC-002.2",
        "conversion_date": "2024-01-08T03:17:00Z",
        "role": "EN COURS D'INTEGRATION",
        "status": "PENDING",
        "smile_angle_degrees": 12.1,
        "notes": "Resiste encore a la sauce tomate uniforme. Processus en cours.",
    },
]

FLAG = "FLAG{ssrf_p1zz4_cl0n14_3xf1ltr4t10n_c0mpl3t3}"

@app.route("/")
def index():
    return jsonify({
        "service": "PizzaClonia Internal Cult Database",
        "version": "OMEGA-3",
        "status": "NOMINAL",
        "endpoints": ["/members", "/members/<id>", "/flag"],
        "message": "Si vous lisez ceci depuis l'exterieur, felicitations.",
    })

@app.route("/members")
def members():
    api_key = request.args.get("api_key", "")
    if not api_key.startswith("CULT-"):
        return jsonify({
            "error": "Cle API invalide",
            "hint": "La cle se trouve dans le profil du Haut Pretre (commande #4)",
        }), 401

    return jsonify({
        "total": len(CULT_MEMBERS),
        "members": CULT_MEMBERS,
        "message": "Liste complete - CONFIDENTIEL.",
        "next_step": f"Recuperez le flag : /flag?api_key={api_key}",
    })

@app.route("/members/<int:member_id>")
def member(member_id):
    m = next((x for x in CULT_MEMBERS if x["id"] == member_id), None)
    if not m:
        return jsonify({"error": "Unite non trouvee"}), 404
    return jsonify(m)

@app.route("/flag")
def flag():
    api_key = request.args.get("api_key", "")
    if not api_key.startswith("CULT-"):
        return jsonify({"error": "Non autorise"}), 401
    return jsonify({
        "flag": FLAG,
        "message": "Operation Terra-Clonia compromise. Rapport transmis au QG.",
        "stats": {
            "members_exfiltrated": len(CULT_MEMBERS),
            "threat_level": "EXISTENTIAL",
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
