from flask import Flask, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__, template_folder='frontend/templates')
CORS(app)

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

@app.route('/')
def index():
    cursor.execute("SELECT * FROM mytable")
    result = cursor.fetchall()
    return render_template('index.html', data=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
