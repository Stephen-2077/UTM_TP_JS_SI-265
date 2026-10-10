import re
import base64
from urllib.parse import unquote
import hashlib
import argparse, json

def a1():
    s = "Salut"
    b = s.encode()
    print(b, b[0])
    print(b.hex())
    print(bytes.fromhex(b.hex()))

print("A1:")
a1()

def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s) and s:
        return "base64"
    return "necunoscut"

print("\nA2:")
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))

def desfa(s):
    strat = ghici_strat(s)

    match strat:
        case "url":
            rezultat = unqoute(s).encode()
        case "hex":
            rezultat = bytes.fromhex(s)
        case "base64":
            rezultat = base64.b64decode(s, validate=True)
        case _:
            rezultat = s.encode()

    return strat, rezultat

def citibil(b):
    return all(32 <= c < 127 for c in b)

def decodeaza_straturi(val):
    for _ in range(8):
        strat, b = desfa(val)
        if not citibil(b):
            print(val)
            break

        val = b.decode(errors="replace")

print("\nA4:")
decodeaza_straturi("NTM1OTU3NTk=")

def sparge_xor(date):
    for k in range(256):
        clar = bytes(b ^ k for b in date)

        if citibil(clar):
            print("cheie: ", k, clar.decode())
            break

print("\nA5:")
date = open("probe/xor.bin", "rb").read()
sparge_xor(date)

def sparge_hash(tinta, wordlist):
    for cuv in wordlist:
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("gasit: ", cuv)
            break

print("\nA6:")
tinta = open("probe/hashuri.txt").readline().strip()
wordlist = open("probe/wordlist.txt", encoding="latin1")
sparge_hash(tinta, wordlist)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        date = open(a.intrare, "rb").read()
        intrare = date.decode(errors="replace")
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode(errors="replace")
    }

    with open("fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, ensure_ascii=False, indent=2)

    print(fisa)

if __name__ == "__main__":
    main()
