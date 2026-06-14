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
    
    # Seleziona le righe della tabella
    rows = soup.find_all('tr', class_='ftbl__competition-ranking__body-row')
    
    # Usiamo enumerate per avere 'i' (il contatore della riga)
    for i, row in enumerate(rows):
        # Cerchiamo il nome squadra
        team_link = row.find('a', class_='ftbl__cta--inline')
        if not team_link:
            continue
        nome_squadra = team_link.text.strip().upper()
        
        # Estraiamo tutti gli span che contengono i dati numerici
        spans = row.find_all('span', class_='ftbl__competition-ranking__body-cell-span')
        
        # Verifichiamo di avere abbastanza dati (almeno 7 per coprire G, V, N, P, GF, GS, PT)
        if len(spans) >= 7:
            item = ET.SubElement(root, "item")
            
            # Dati fissi
            ET.SubElement(item, "row_number").text = str(1775 + i)
            ET.SubElement(item, "SERIE").text = "A"
            ET.SubElement(item, "ANNO").text = "2025-2026"
            ET.SubElement(item, "TEAM").text = nome_squadra
            
            # Mappatura dei dati estratti dagli span
            ET.SubElement(item, "G").text = spans[0].text.strip()
            ET.SubElement(item, "V").text = spans[1].text.strip()
            ET.SubElement(item, "N").text = spans[2].text.strip()
            ET.SubElement(item, "P").text = spans[3].text.strip()
            ET.SubElement(item, "GF").text = spans[4].text.strip()
            ET.SubElement(item, "GS").text = spans[5].text.strip()
            ET.SubElement(item, "PT").text = spans[6].text.strip()
            
            # Logica POS
            if nome_squadra == "ATALANTA":
                pos = "2"
            elif i >= 17:
                pos = "3"
            elif i == 0:
                pos = "1"
            else:
                pos = "0"
            ET.SubElement(item, "POS").text = pos

    # Salvataggio
    output_path = os.path.join(os.path.dirname(__file__), "classificaUPD.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()
