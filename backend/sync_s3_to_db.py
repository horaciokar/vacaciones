import sys
import os

# Permite importar backend/config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import boto3
import mysql.connector
from backend.config import *

# Configuración S3
s3 = boto3.client(
    "s3",
    region_name="us-east-1"  # ⚠️ ajustar si tu bucket está en otra región
)

BUCKET = S3_BUCKET

# Conexión a MySQL
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = db.cursor()

print(f"Iniciando sync con bucket: {BUCKET}")

# Paginador (clave para subcarpetas)
paginator = s3.get_paginator("list_objects_v2")

total = 0
insertados = 0
omitidos = 0

for page in paginator.paginate(Bucket=BUCKET):
    for obj in page.get("Contents", []):

        key = obj["Key"]

        # Filtrar solo imágenes
        if not key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        total += 1

        print(f"Procesando: {key}")

        url = f"https://{BUCKET}.s3.amazonaws.com/{key}"

        # Evitar duplicados
        cursor.execute("SELECT id FROM fotos WHERE url=%s", (url,))
        if cursor.fetchone():
            print(f"Ya existe, skip: {key}")
            omitidos += 1
            continue

        # Detectar ubicación desde carpeta
        try:
            ubicacion = key.split("/")[0]
        except:
            ubicacion = "unknown"

        # Insertar en DB
        cursor.execute(
            "INSERT INTO fotos (nombre, url, fecha, ubicacion) VALUES (%s, %s, NOW(), %s)",
            (key, url, ubicacion)
        )

        db.commit()
        insertados += 1

        print(f"Insertado: {key}")

print("\n===== RESUMEN =====")
print(f"Total encontrados: {total}")
print(f"Insertados: {insertados}")
print(f"Omitidos: {omitidos}")
print("Sync terminado")