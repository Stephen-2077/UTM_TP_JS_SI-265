# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 # secunde

import time
import requests
from urllib.parse import urljoin, urlparse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime, timezone

def ex_35():
    url = BASE_URL + "/path?x=1#top"

    parsed_url = urlparse(url)

    print(parsed_url.scheme)
    print(parsed_url.netloc)
    print(parsed_url.path)
    print(parsed_url.query)
    print(parsed_url.fragment)

def ex_36():
    print(urljoin(BASE_URL, "/about"))
    print(urljoin(BASE_URL, "contact.html"))
    print(urljoin(BASE_URL, "../index.html"))

def extract_links(html):
    """Returnează legăturile href fără duplicate."""
    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))

def ex_37():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    links = extract_links(response.text)

    for link in links:
        print(link)

def split_links(links, domain, base):
    """Separă legăturile interne de cele externe."""
    internal = []
    external = []

    for link in links:
        full_url = urljoin(base, link)
        netloc = urlparse(full_url).netloc

        if netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external

def ex_38():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    links = extract_links(response.text)

    domain = urlparse(BASE_URL).netloc

    internal, external = split_links(links, domain, BASE_URL)

    print("Legături interne:")
    
    for link in internal:
        print(link)

    print("Legături externe:")

    for link in external:
        print(link)

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    # Metoda este apelată automat de HTMLParser
    # când întâlnește un tag de început
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return

        src = dict(attrs).get("src")

        if src is not None:
            self.images.append(src)

def local_test():
    test_html = """
    <html><body>
        <img src="/logo.png" alt="Logo">
        <IMG SRC="poza.jpg">
        <img alt="imagine fără src">
        <img src="https://cdn.example.com/banner.webp" />
        <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
 
    finder = ImageFinder()
    finder.feed(test_html)
    print(finder.images)
 
    assert finder.images == [
        "/logo.png",                            # imagine obișnuită
        "poza.jpg",                             # tag scris cu majuscule
        "https://cdn.example.com/banner.webp",  # tag care se închide singur
    ], "Parserul nu a găsit exact imaginile așteptate"
    print("Testul a trecut!")

def real_test():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    finder = ImageFinder()
    finder.feed(response.text)
    print(len(finder.images), "imagini găsite")
    for src in finder.images:
        print(src)

    print("Nr. de \"<img\" in cod: ", response.text.lower().count("<img"))

def ex_39():
    local_test()
    real_test()

def page_fingerprint(url):
    """Returnează amprenta SHA-256 a paginii."""
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(response.content).hexdigest()

def ex_40():
    print(page_fingerprint(BASE_URL))

    time.sleep(1)

    print(page_fingerprint(BASE_URL))

    # Amprentele ar fi diferite chiar și dacă s-ar schimba
    # un singur bit din response.content

def ex_41():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    headers = dict(response.headers)

    with open("headers.json", "w", encoding="utf-8") as file:
        json.dump(headers, file, indent=2)

    with open("headers.json", "r", encoding="utf-8") as file:
        loaded_headers = json.load(file)

    print(loaded_headers.get("Content-Type", "lipsește"))

def resolve(hostname):
    """Returnează adresa IPv4 a unui hostname."""
    return socket.gethostbyname(hostname)

def ex_42():
    print(resolve("cybercor.org"))

def cert_days_left(hostname):
    """Returnează numărul de zile până la expirarea certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            certificate = secure_sock.getpeercert()

    expiration = certificate["notAfter"]

    expiration_timestamp = ssl.cert_time_to_seconds(expiration)

    expiration_date = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)

    now = datetime.now(timezone.utc)

    return (expiration_date - now).days

def ex_43():
    print(cert_days_left("cybercor.org"))

print("Exercițiul 35")
ex_35()
time.sleep(1)

print("\nExercițiul 36")
ex_36()
time.sleep(1)

print("\nExercițiul 37")
ex_37()
time.sleep(1)

print("\nExercițiul 38")
ex_38()
time.sleep(1)

print("\nExercițiul 39")
ex_39()
time.sleep(1)

print("\nExercițiul 40")
ex_40()
time.sleep(1)

print("\nExercițiul 41")
ex_41()
time.sleep(1)

print("\nExercițiul 42")
ex_42()
time.sleep(1)

print("\nExercițiul 43")
ex_43()
time.sleep(1)
