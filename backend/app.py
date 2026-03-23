from flask import Flask, jsonify
import mysql.connector
from config import *

app = Flask(__name__)

@app.route("/api/fotos")
def fotos():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fotos ORDER BY fecha ASC")

    return jsonify(cursor.fetchall())

app.run(host="0.0.0.0", port=5000)