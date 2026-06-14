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
    
    # Seleziona le righe della tabella. 
    # NOTA: Assicurati che il tag e la classe siano corretti basandoti sull'ispezione della pagina.
    rows = soup.find_all('tr', class_='ftbl__competition-ranking__body-row')
    
    for i, row in enumerate(rows):
        item = ET.SubElement(root, "item")
        
        # Estrazione dati dalle celle (td)
        # Supponiamo l'ordine standard di Sky: Squadra, G, V, N, P, GF, GS, PT
        cells = row.find_all('td')
        if len(cells) < 8: continue # Salta se la riga non è completa
        
        nome_squadra = row.find('a', class_='ftbl__cta--inline').text.strip().upper()
        
        # Creazione dei tag richiesti
        ET.SubElement(item, "row_number").text = str(1775 + i)
        ET.SubElement(item, "SERIE").text = "A"
        ET.SubElement(item, "ANNO").text = "2025-2026"
        ET.SubElement(item, "TEAM").text = nome_squadra
        ET.SubElement(item, "PT").text = cells[7].text.strip() # PT
        ET.SubElement(item, "G").text = cells[1].text.strip()  # G
        ET.SubElement(item, "V").text = cells[2].text.strip()  # V
        ET.SubElement(item, "N").text = cells[3].text.strip()  # N
        ET.SubElement(item, "P").text = cells[4].text.strip()  # P
        ET.SubElement(item, "GF").text = cells[5].text.strip() # GF
        ET.SubElement(item, "GS").text = cells[6].text.strip() # GS
        
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
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()
