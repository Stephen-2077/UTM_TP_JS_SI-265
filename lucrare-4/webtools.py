# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

TIMEOUT = 10 # secunde

DEFAULT_HEADERS = {"User-Agent":"WebLab-Josan Stefan"}

import requests
import csv
import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

def fetch(url, timeout=10):
    """Returnează obiectul răspuns pentru adresa url."""
    response = requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)
    time.sleep(1)
    return response

def get_status(url):
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

def get_title(html):
    """Returnează titlul unei pagini HTML."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else None

def security_headers(url):
    """Verifică prezența antetelor de securitate."""
    response = fetch(url)

    headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    results = {}

    for header in headers:
        results[header] = header in response.headers

    return results

def page_exists(url):
    """Returnează True dacă cererea poate fi realizată fără eroare."""
    try:
        response = fetch(url)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def check_paths(base, paths):
    """Returnează codul HTTP pentru fiecare cale."""
    results = {}

    for path in paths:
        results[path] = get_status(base + path)

    return results

def get_header(url, name, default="lipsește"):
    """Returnează valoarea unui antet HTTP."""
    response = fetch(url)
    return response.headers.get(name, default)

def score_headers(results):
    """Returnează câte antete de securitate sunt prezente."""
    present = sum(results.values())
    total = len(results)

    return f"{present}/{total}"

def fetch_robots(base):
    """Returnează conținutul robots.txt sau None."""
    try:
        response = fetch(base + "/robots.txt")

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.text
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    """Returnează valorile Disallow din robots.txt."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            paths.append(path)

    return paths

def response_times(*urls):
    """Returnează timpul de răspuns pentru fiecare URL."""
    results = {}

    for url in urls:
        start = time.perf_counter()

        fetch(url)

        end = time.perf_counter()

        results[url] = end - start

    return results

def log(message, **details):
    """Afișează un mesaj urmat de detaliile primite."""
    output = message

    for name, value in details.items():
        output += f" | {name}={value}"

    print(output)

def extract_links(html):
    """Returnează legăturile href fără duplicate."""
    soup = BeautifulSoup(html, "html.parser")

    return list(dict.fromkeys(
        link.get("href")
        for link in soup.find_all("a")
        if link.get("href")
    ))

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

def page_fingerprint(url):
    """Returnează amprenta SHA-256 a paginii."""
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(response.content).hexdigest()

def resolve(hostname):
    """Returnează adresa IPv4 a unui hostname."""
    return socket.gethostbyname(hostname)

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

def save_csv_report(base, paths):
    results = check_paths(base, paths)

    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["path", "status", "checked_at"])

        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])

    print("Salvat în report.csv")

def site_report(url):
    """Colectează informații despre un site și creează report.json"""

    response = fetch(url)

    status = response.status_code
    final_url = response.url

    title = get_title(response.text)

    hostname = urlparse(final_url).hostname

    if hostname is not None:
        ip_address = resolve(hostname)
    else:
        ip_address = None

    redirect_response = fetch("http://" + hostname)

    redirects = []

    for redirect in redirect_response.history:
        redirects.append({"status": redirect.status_code, "url": redirect.url})

    redirects.append({"status": redirect_response.status_code, "url": redirect_response.url})
    
    header_results = security_headers(url)
    security_score = score_headers(header_results)

    if hostname is not None:
        certificate_days = cert_days_left(hostname)
    else:
        certificate_days = None

    links = extract_links(response.text)

    domain = urlparse(final_url).netloc

    internal_links, external_links = split_links(links, domain, final_url)

    robots_text = fetch_robots(url)
    disallowed = disallowed_paths(robots_text)

    report = {
        "url": url,
        "status_code": status,
        "final_url": final_url,
        "title": title,
        "ip_address": ip_address,
        "redirects": redirects,
        "security_headers": header_results,
        "security_score": security_score,
        "certificate_days_left": certificate_days,
        "internal_links": len(internal_links),
        "external_links": len(external_links),
        "disallowed_paths": disallowed
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:       {status}")
    print(f"URL final:          {final_url}")
    print(f"Titlu:              {title}")
    print(f"Adresă IP:          {ip_address}")

    print("Redirecționări:")

    if redirects:
        for redirect in redirects:
            print(
                f"  {redirect['status']} -> "
                f"{redirect['url']}"
            )
    else:
        print("  Nicio redirecționare")

    print(f"Scor securitate:    {security_score}")

    if certificate_days is not None:
        print(
            f"Certificat:         "
            f"{certificate_days} de zile rămase"
        )
    else:
        print("Certificat:         indisponibil")

    print(
        f"Legături:           "
        f"{len(internal_links)} interne, "
        f"{len(external_links)} externe"
    )

    print(
        "Căi interzise:      "
        + (
            ", ".join(disallowed)
            if disallowed
            else "niciuna"
        )
    )

    with open(
        "report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("Salvat în report.json")

    return report

# Valoarea variabilei __name__ este atribuită valoarea
# __main__ doar atunci când fișierul este rulat direct
# Când fișierul este importat, această variabila va avea
# valoarea webtools, și condiția nu se va îndeplini
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
