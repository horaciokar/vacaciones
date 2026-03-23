import os
import boto3
from PIL import Image
from PIL.ExifTags import TAGS
import mysql.connector
from backend.config import *

s3 = boto3.client("s3")

def get_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        data = {}

        if exif:
            for tag, val in exif.items():
                data[TAGS.get(tag, tag)] = val

        return data.get("DateTime", "2000:01:01 00:00:00")
    except:
        return "2000:01:01 00:00:00"

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = db.cursor()

BASE_PATH = "./fotos"

for root, _, files in os.walk(BASE_PATH):
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(root, f)
            key = f

            s3.upload_file(path, S3_BUCKET, key)

            url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
            fecha = get_exif(path)

            cursor.execute(
                "INSERT INTO fotos (nombre, url, fecha) VALUES (%s, %s, %s)",
                (f, url, fecha)
            )

db.commit()