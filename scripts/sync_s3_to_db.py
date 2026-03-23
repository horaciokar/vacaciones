import boto3
import mysql.connector
from backend.config import *

s3 = boto3.client("s3")

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = db.cursor()

BUCKET = S3_BUCKET

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=BUCKET):
    for obj in page.get("Contents", []):
        key = obj["Key"]

        if key.endswith((".jpg", ".jpeg", ".png")):
            print(f"Procesando {key}")

            url = f"https://{BUCKET}.s3.amazonaws.com/{key}"

            cursor.execute("SELECT id FROM fotos WHERE url=%s", (url,))
            if cursor.fetchone():
                print("Ya existe, skip")
                continue

            cursor.execute(
                "INSERT INTO fotos (nombre, url, fecha) VALUES (%s, %s, NOW())",
                (key, url)
            )

            db.commit()

for obj in response.get("Contents", []):
    key = obj["Key"]

    if key.endswith((".jpg", ".jpeg", ".png")):

        print(f"Procesando {key}")

        url = f"https://{BUCKET}.s3.amazonaws.com/{key}"

        # evitar duplicados
        cursor.execute("SELECT id FROM fotos WHERE url=%s", (url,))
        if cursor.fetchone():
            print("Ya existe, skip")
            continue

        cursor.execute(
            "INSERT INTO fotos (nombre, url, fecha) VALUES (%s, %s, NOW())",
            (key, url)
        )

        db.commit()

print("Sync terminado")