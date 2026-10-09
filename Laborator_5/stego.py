from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.get_flattened_data())

mesaj = b"FLAG{ascuns_in_pixeli}\0"
biti = "".join(f"{x:08b}" for x in mesaj)

if len(biti) > len(px) * 3:
    raise ValueError("Imaginea nu are suficienta capacitate.")

px_nou = []

for i, (r, g, b) in enumerate(px):
    canale = [r, g, b]

    for j in range(3):
        poz = i * 3 + j
        if poz < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[poz])

    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")
print("Imaginea stego.png a fost creată")

px = list(Image.open("stego.png").convert("RGB").get_flattened_data())
biti = ""

for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

mesaj = bytearray()

for i in range(0, len(biti) - 7, 8):
    octet = int(biti[i:i + 8], 2)

    if octet == 0:
        break

    mesaj.append(octet)

print(mesaj.decode())
