from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import mysql.connector
import os
import time
import requests

app = Flask(__name__, template_folder='frontend/templates')
CORS(app, resources={r"/*": {"origins": "*"}})

def is_mysql_available():
    try:
        # Try connecting to MySQL
        db = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "mysql"),
            user=os.environ.get("DB_USER", "myuser"),
            password=os.environ.get("DB_PASSWORD", "mypassword"),
            database=os.environ.get("DB_DATABASE", "mydatabase"),
            port=int(os.environ.get("DB_PORT", 3306))
        )
        db.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# Wait for MySQL to become available
while not is_mysql_available():
    print("Waiting for MySQL to become available...")
    time.sleep(1)

# Configuration de la base de données
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "mysql"),
    user=os.environ.get("DB_USER", "myuser"),
    password=os.environ.get("DB_PASSWORD", "mypassword"),
    database=os.environ.get("DB_DATABASE", "mydatabase"),
    port=int(os.environ.get("DB_PORT", 3306))
)

cursor = db.cursor()

@app.route('/add_colis', methods=['POST'])
def add_colis():
    data = request.get_json()
    id = data['id']
    adresse_x = data['adresse_x']
    adresse_y = data['adresse_y']
    cursor = db.cursor()

    # Chercher le numéro de livraison le plus élevé
    cursor.execute("SELECT MAX(livraison_id) FROM livraisons")
    livraison_id = cursor.fetchone()[0]

    # Si la table livraisons est vide, initialiser une nouvelle livraison
    if livraison_id is None:
        cursor.execute("SELECT camion_id FROM camions ORDER BY camion_id ASC LIMIT 1")
        camion_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO livraisons (camion_id, etat_livraison) VALUES (%s, %s)", (camion_id, 0))
        db.commit()
        livraison_id = cursor.lastrowid
    else:
        # Vérifier qu'au maximum 30 colis sont attachés à cette livraison
        cursor.execute("SELECT COUNT(*) FROM colis WHERE livraison_id = %s", (livraison_id,))
        count = cursor.fetchone()[0]
        if count >= 30:
            # Chercher le camion qui a le moins de livraisons en cours
            cursor.execute("""
                SELECT c.camion_id 
                FROM camions c 
                LEFT JOIN livraisons l ON c.camion_id = l.camion_id AND l.etat_livraison = 0
                GROUP BY c.camion_id 
                ORDER BY COUNT(l.livraison_id) ASC 
                LIMIT 1
            """)
            camion_id = cursor.fetchone()[0]

            # Ajouter une ligne dans la table livraisons avec un id incrémenté
            cursor.execute("INSERT INTO livraisons (camion_id, etat_livraison) VALUES (%s, %s)", (camion_id, 0))
            db.commit()
            livraison_id = cursor.lastrowid

    # Ajouter les informations dans la table colis
    cursor.execute("INSERT INTO colis (colis_id, livraison_id, adresse_x, adresse_y, etat_colis) VALUES (%s, %s, %s, %s, %s)", (id, livraison_id, adresse_x, adresse_y, 0))
    db.commit()

    return jsonify({"message": "Colis ajouté avec succès"}), 201




@app.route('/postPosColisFromDevice', methods=['POST'])
def post_route2():
    data = request.get_json()
    colis_id = data.get('colis_id')
    new_etat_colis = data.get('etat_colis')

    if colis_id and new_etat_colis is not None:
        cursor = db.cursor()
        update_query = "UPDATE colis SET etat_colis = %s WHERE colis_id = %s"
        cursor.execute(update_query, (new_etat_colis, colis_id))
        db.commit()

    return jsonify({'message': 'Mise à jour réussie'}), 200

@app.route('/postPosCamionFromDevice', methods=['POST'])
def post_route3():
    data = request.get_json()
    camion_id = data.get('camion_id')
    new_camion_pos_x = data.get('camion_pos_x')
    new_camion_pos_y = data.get('camion_pos_y')

    if camion_id and new_camion_pos_x is not None and new_camion_pos_y is not None:
        cursor = db.cursor()
        update_query = "UPDATE camions SET camion_pos_x = %s, camion_pos_y = %s WHERE camion_id = %s"
        cursor.execute(update_query, (new_camion_pos_x, new_camion_pos_y, camion_id))
        db.commit()

    return jsonify(data), 201

@app.route('/getLivraison', methods=['GET'])
def get_route():
    query = """
    SELECT livraisons.livraison_id, colis.colis_id, colis.adresse_x, colis.adresse_y, colis.etat_colis
    FROM livraisons
    JOIN colis ON livraisons.livraison_id = colis.livraison_id
    WHERE livraisons.etat_livraison = 0
    """
    try:
        cursor = db.cursor(dictionary=True)  # Add dictionary=True
        cursor.execute(query)
        result = cursor.fetchall()
        db.commit()
        return jsonify(result), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Error executing query"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
