# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 # secunde

import time

import requests
import urllib.request
def ex_1():
    print(requests.__version__)
     
    # Requests este un pachet extern, care trebuie să fie instalat cu pip install.
    # Pe când urllib face parte din biblioteca standard Python.

def ex_2():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

    time.sleep(1)

    from requests import get
    response = get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

    # Stilul "import requests" ajută la evitarea conflictelor de nume între module,
    # încât fiecare apelare își are specificată originea.
    # Stilul ”from requests import get” evită repetarea numelui bibliotecii importate.

def ex_3():
    import requests as rq

    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

    # Putem folosi un alias când folosim funcțiile unei biblioteci foarte des.
    # Pe de altă parte, un alias ce nu face clară originea unei funcții poate îngreuna
    # citirea codului.

def ex_4():
    try:
        response = urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
        print(response.status)

        body = response.read().decode("utf-8")
        print(body[:200])
    
    except urllib.error.HTTPError as error:
        print(error.code)

def ex_5():
    print(dir(requests))

    # Response - clasă
    # post - funcție
    # utils - modul

def ex_6():
    help(requests.get)

    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

def ex_7():
    start = time.perf_counter()

    response = requests.get(BASE_URL, timeout=TIMEOUT)

    end = time.perf_counter()
    print("Timp măsurat cu time.perf_counter(): ", end - start)
    print("Time măsurat cu response.elapsed: ", response.elapsed)

def ex_8():
    try:
        import bs4
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4")

# Un modul este un singur fișier de cu extensia .py
# Un pachet grupează mai multe module
# O bibliotecă se referă la cod reutilizabil

print("Exercițiul 1:")
ex_1()
time.sleep(1)

print("\nExercițiul 2:")
ex_2()
time.sleep(1)

print("\nExercițiul 3:")
ex_3()
time.sleep(1)

print("\nExercițiul 4:")
ex_4()
time.sleep(1)

print("\nExercițiul 5:")
ex_5()
time.sleep(1)

print("\nExercițiul 6:")
ex_6()
time.sleep(1)

print("\nExercițiul 7:")
ex_7()
time.sleep(1)

print("\nExercițiul 8:")
ex_8()
