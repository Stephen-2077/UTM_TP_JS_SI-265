# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 # secunde

import time
import requests

def fetch(url, timeout=10):
    """Returnează obiectul răspuns pentru adresa url."""
    response = requests.get(url, timeout=timeout)
    time.sleep(1)    
    return response

def ex_21():
    response = fetch(BASE_URL)
    print(response.status_code)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

def ex_22():
    print(get_status(BASE_URL + "/"))
    print(get_status(BASE_URL + "/robots.txt"))
    print(get_status(BASE_URL + "/sitemap.xml"))

def ex_23():
    print(fetch(BASE_URL).status_code)
    print(fetch(BASE_URL, timeout=3).status_code)

def get_title(html):
    """Returnează titlul unei pagini HTML."""
    start = html.find("<title>") + len("<title>")

    if start == -1:
        return None

    end = html.find("</title>", start)

    if end == -1:
        return None

    return html[start:end].strip()

def ex_24():
    response = fetch(BASE_URL)
    title = get_title(response.text)

    print(title)

def ex_25():
    print(help(get_title))

def ex_26():
    try:
        print(get_status(123))
    except (requests.RequestException, TypeError) as error:
        print(error)

def page_exists(url):
    """Returnează True dacă cererea poate fi realizată fără eroare."""
    try:
        response = fetch(url)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def ex_27():
    print(page_exists("https://this-domain-does-not-exist.invalid"))

def check_paths(base, paths):
    """Returnează codul HTTP pentru fiecare cale."""
    results = {}

    for path in paths:
        results[path] = get_status(base + path)
        
    return results

def ex_28():
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

def get_header(url, name, default="lipsește"):
    """Returnează valoarea unui antet HTTP."""
    response = fetch(url)
    return response.headers.get(name, default)

def ex_29():
    print(get_header(BASE_URL, name="Server"))

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

def ex_30():
    results = security_headers(BASE_URL)

    for header, present in results.items():
        print(header, ": ", present)

def score_headers(results):
    """Returnează câte antete de securitate sunt prezente."""
    present = sum(results.values())
    total = len(results)

    return f"{present}/{total}"

def ex_31():
    print(score_headers(security_headers(BASE_URL)))

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

def ex_32():
    robots = fetch_robots(BASE_URL)

    if robots is None:
        print("robots.txt nu a putut fi descărcat")
    else:
        paths = disallowed_paths(robots)

        print("Căi interzise:")

        for path in paths:
            print(path)

def response_times(*urls):
    """Returnează timpul de răspuns pentru fiecare URL."""
    results = {}

    for url in urls:
        start = time.perf_counter()

        fetch(url)

        end = time.perf_counter()

        results[url] = end - start
       
    return results

def ex_33():
    results = response_times(BASE_URL, BASE_URL + "/robots.txt")

    for url, seconds in results.items():
        print(f"{url}: {seconds:.4f} secunde")

def log(message, **details):
    """Afișează un mesaj urmat de detaliile primite."""
    output = message

    for name, value in details.items():
        output += f" | {name}={value}"

    print(output)

def ex_34():
    response = fetch(BASE_URL)

    log("verificat", url=BASE_URL, status=response.status_code)

# print() afișează o valoare la consolă
# return întoarce o valoare la locul apelării, pentru a fi folosită mai departe


print("Exercițiul 21:")
ex_21()

print("\nExercițiul 22:")
ex_22()

print("\nExercițiul 23:")
ex_23()

print("\nExercițiul 24:")
ex_24()

print("\nExercițiul 25:")
ex_25()

print("\nExercițiul 26:")
ex_26()

print("\nExercițiul 27:")
ex_27()

print("\nExercițiul 28:")
ex_28()

print("\nExercițiul 29:")
ex_29()

print("\nExercițiul 30:")
ex_30()

print("\nExercițiul 31:")
ex_31()

print("\nExercițiul 32:")
ex_32()

print("\nExercițiul 33:")
ex_33()

print("\nExercițiul 34:")
ex_34()

