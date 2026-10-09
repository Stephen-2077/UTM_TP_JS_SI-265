# Laborator: funcții, metode și importuri pe web
# Student: Josan Ștefan

import time
import argparse
import csv

import webtools

def ex_44(url):
    print(webtools.get_title(webtools.fetch(url).text))

# Dacă fișierul main.py ar avea și el o funcție
# cu numele get_title, aceasta ar ascunde funcția
# importată și ar fi folosită la fiecare apel
from webtools import get_title, security_headers

def ex_45(url):
    print(get_title(webtools.fetch(url).text))

from webtools import DEFAULT_HEADERS

def ex_47():
    print(DEFAULT_HEADERS)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analizează un site web."
    )

    parser.add_argument(
        "url",
        help="URL-ul site-ului"
    )

    return parser.parse_args()

def ex_49(url):
    paths = ["/", "/robots.txt","/sitemap.xml"]

    webtools.save_csv_report(url, paths)

def ex_50(url):
    webtools.site_report(url)

def main():
    args = parse_arguments()

    url = args.url

    print("Exercițiul 44:")
    ex_44(url)
    
    print("\nExercițiul 45:")
    ex_45(url)
 
    print("\nExercițiul 47:")
    ex_47()
 
    print("\nExercițiul 49:")
    ex_49(url)

    print("\nExercițiul 50:")
    ex_50(url)

if __name__ == "__main__":
    main()
