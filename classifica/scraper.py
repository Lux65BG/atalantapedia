import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os

def get_classifica():
    url = "https://sport.sky.it/calcio/serie-a/classifica"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    root = ET.Element("Root")
    
    # Cerchiamo le righe della tabella (ogni riga contiene una squadra)
    # Sky solitamente usa una struttura dove ogni squadra è in una riga 'tr'
    rows = soup.find_all('tr', class_='ftbl__competition-ranking__body-row')
    
    for row in rows:
        item = ET.SubElement(root, "item")
        
        # Nome squadra (dal link che hai trovato)
        team = row.find('a', class_='ftbl__cta--inline')
        if team:
            ET.SubElement(item, "TEAM").text = team.text.strip()
            
        # Punti
        pts = row.find('td', class_='ftbl__competition-ranking__body-cell--points')
        if pts:
            ET.SubElement(item, "PT").text = pts.find('span').text.strip()
            
        # Partite giocate
        played = row.find('td', class_='ftbl__competition-ranking__body-cell--mobile-show')
        if played:
            ET.SubElement(item, "G").text = played.find('span').text.strip()

    # Salva il file
    output_path = os.path.join(os.path.dirname(__file__), "classificaUPD.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()
