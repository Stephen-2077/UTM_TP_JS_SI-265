import re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def tip_real(cale):
    cap = open(cale, "rb").read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()

print("B1:")
print(tip_real("probe/foto.jpg"))

print("\nB2:")
date = open("probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

print("\nB3:")
exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get(34853, {})
gps = {GPSTAGS.get(k, k): v for k, v in gps.items()}

def grade(val):
    return float(val[0]) + float(val[1]) / 60 + float(val[2]) / 3600

if "GPSLatitude" in gps and "GPSLongitude" in gps:
    lat = grade(gps["GPSLatitude"])
    lon = grade(gps["GPSLongitude"])

    if gps.get("GPSLatitudeRef") == "S":
        lat = -lat
    if gps.get("GPSLongitudeRef") == "W":
        lon = -lon

    print("Latitudine:", lat)
    print("Longitudine:", lon)
