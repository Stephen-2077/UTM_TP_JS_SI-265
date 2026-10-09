# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 # secunde

import time
import requests

def ex_9():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    print(response.status_code) # atribut
    print(response.ok) # atribut
    print(response.url) #atribut
    print(response.encoding) # atribut

def ex_10():
    response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    print(response.status_code)

    try:
        response.raise_for_status() # metodă
    except requests.HTTPError:
        print("Eroare la accesarea paginii.")

def ex_11():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    for name, value in response.headers.items():
        print(f"{name}: {value}")

def ex_12():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    print(response.headers.get("Server", "lipsește"))
    print(response.headers.get("Content-Type", "lipsește"))  

    print(response.headers.get("content-type", "lipsește"))

    # response.headers este case-insensitive
    # așa că "Content-Type" și "content-type" returnează aceeași valoare

def ex_13():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    print(response.text.lower().count("cyber"))

    # Metoda .lower() returnează un șir de caractere.
    # Deoarece rezultatul este tot un șir, putem apela metoda .count() al lui

def ex_14():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    html = response.text

    start = html.find("<title>") + len("<title>")
    end = html.find("</title>", start)

    title = html[start:end].strip()

    print(title)

def ex_15():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    lines = response.text.splitlines()
    
    print("Nr. de linii: ", len(lines))
    print("Lungimea celei mai lungi linii: ", len(max(lines, key=len)))
    
def ex_16():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    if response.url.startswith("https://"):
        print("Conexiune securizată")
    else:
        print("Conexiune nesecurizată")

def ex_17():
    response = requests.get("http://cybercor.org", timeout=TIMEOUT)

    for redirect in response.history:
        print(redirect.status_code, redirect.url)

    print("URL final: ", response.url)

def ex_18():
    head_response = requests.head(BASE_URL, timeout=TIMEOUT)
    print("Bytes în requests.head(): ", len(head_response.content))

    time.sleep(1)

    get_response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Bytes in requests.get(): ", len(get_response.content))

    # cererea HEAD solicită doar antetele răspunsului
    # cererea GET solicită antetele și corpul paginii
    # de aceea răspunsul cererii GET este mai lung

def ex_19():
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    if response.cookies:
        for cookie in response.cookies:
            print(cookie.name, cookie.secure)
    else:
        print("Niciun cookie setat.")

def ex_20():
    with requests.Session() as session:
        session.headers.update({"User-Agent": "WebLab-Josan Stefan"})

        response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)

        print(response.text)

        data = response.json()

        user_agent = data["headers"].get("User-Agent")
        print("User-Agent: ", user_agent)
    
    # response.text este un atribut, de aceea nu are paranteze
    # response.json() este o metodă, de aceea este apelată cu paranteze

print("Exercițiul 9")
ex_9()
time.sleep(1)

print("\nExercițiul 10")
ex_10()
time.sleep(1)

print("\nExercițiul 11")
ex_11()
time.sleep(1)

print("\nExercițiul 12")
ex_12()
time.sleep(1)

print("\nExercițiul 13")
ex_13()
time.sleep(1)

print("\nExercițiul 14")
ex_14()
time.sleep(1)

print("\nExercițiul 15")
ex_15()
time.sleep(1)

print("\nExercițiul 16")
ex_16()
time.sleep(1)

print("\nExercițiul 17")
ex_17()
time.sleep(1)

print("\nExercițiul 18")
ex_18()
time.sleep(1)

print("\nExercițiul 19")
ex_19()
time.sleep(1)

print("\nExercițiul 20")
ex_20()
