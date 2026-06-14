import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os

def get_classifica():
    # URL di esempio (da verificare quando inizierai lo scraping vero e proprio)
    url = "https://sport.sky.it/calcio/serie-a/classifica"
    # È buona norma aggiungere un header per simulare un browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Esempio di creazione XML
    root = ET.Element("classifica")
    # Qui aggiungerai la logica per leggere i dati da 'soup'
    
    # Salvataggio nella cartella specifica
    output_path = os.path.join(os.path.dirname(__file__), "classifica.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()