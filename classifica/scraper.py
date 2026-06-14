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
    rows = soup.find_all('tr', class_='ftbl__competition-ranking__body-row')
    
for i, row in enumerate(rows):
        # 1. Recupero Nome Squadra (questo lo sappiamo fare bene)
        team_link = row.find('a', class_='ftbl__cta--inline')
        if not team_link: continue
        nome_squadra = team_link.text.strip().upper()
        
        # 2. Cerchiamo SOLO le celle che contengono i dati numerici
        # Le celle di Sky hanno spesso classi diverse. 
        # Prendiamo tutti i 'td' e ne estraiamo il contenuto pulito
        cells = row.find_all('td')
        
        # Questa è una lista di dati puri (saltando i primi 2 che sono Pos e Nome)
        # Se la riga ha almeno 9 celle, i dati numerici sono dalla 2 in poi
        if len(cells) >= 9:
            data = []
            for cell in cells:
                # Estraiamo il testo e puliamo spazi extra
                valore = cell.text.strip()
                if valore: # Aggiungiamo solo se non è vuoto
                    data.append(valore)
            
            # Ora 'data' dovrebbe essere una lista tipo: 
            # ['1', 'Inter', '87', '38', '27', '6', '5', '89', '35', '54', 'N', 'V'...]
            # La posizione è data[0], il Nome è data[1], i Punti dovrebbero essere data[2]
            
            item = ET.SubElement(root, "item")
            ET.SubElement(item, "row_number").text = str(1775 + i)
            ET.SubElement(item, "SERIE").text = "A"
            ET.SubElement(item, "ANNO").text = "2025-2026"
            ET.SubElement(item, "TEAM").text = nome_squadra
            
            # Mappatura sicura dalla lista 'data'
            # Se vedi ancora dati sballati, basta cambiare il numero tra parentesi
            ET.SubElement(item, "PT").text = data[2] 
            ET.SubElement(item, "G").text = data[3]
            ET.SubElement(item, "V").text = data[4]
            ET.SubElement(item, "N").text = data[5]
            ET.SubElement(item, "P").text = data[6]
            ET.SubElement(item, "GF").text = data[7]
            ET.SubElement(item, "GS").text = data[8]
            
            # Logica POS
            pos = "2" if nome_squadra == "ATALANTA" else ("3" if i >= 17 else ("1" if i == 0 else "0"))
            ET.SubElement(item, "POS").text = pos
            


    output_path = os.path.join(os.path.dirname(__file__), "classificaUPD.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()
