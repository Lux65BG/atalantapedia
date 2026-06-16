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
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    rows = soup.find_all('tr', class_='ftbl__competition-ranking__body-row')
    
    # Questo ciclo deve essere indentato di 4 spazi rispetto alla def get_classifica():
    for i, row in enumerate(rows):
        team_link = row.find('a', class_='ftbl__cta--inline')
        if not team_link: continue
        nome_squadra = team_link.text.strip().upper()
        
        cells = row.find_all('td')
        
        if len(cells) >= 9:
            data = []
            for cell in cells:
                valore = cell.text.strip()
                if valore:
                    data.append(valore)
            
            # Qui controlliamo che 'data' abbia abbastanza elementi per evitare crash
            if len(data) >= 9:
                item = ET.SubElement(root, "item")
                ET.SubElement(item, "row_number").text = str(1795 + i)
                ET.SubElement(item, "SERIE").text = "A"
                ET.SubElement(item, "ANNO").text = "2025-2026 - A"
                ET.SubElement(item, "TEAM").text = nome_squadra
                
                # Mappatura corretta dalla lista 'data'
                ET.SubElement(item, "PT").text = data[2] 
                ET.SubElement(item, "G").text = data[3]
                ET.SubElement(item, "V").text = data[4]
                ET.SubElement(item, "N").text = data[5]
                ET.SubElement(item, "P").text = data[6]
                ET.SubElement(item, "GF").text = data[7]
                ET.SubElement(item, "GS").text = data[8]
                
                pos = "2" if nome_squadra == "ATALANTA" else ("3" if i >= 17 else ("1" if i == 0 else "0"))
                ET.SubElement(item, "POS").text = pos

    output_path = os.path.join(os.path.dirname(__file__), "classificaUPD.xml")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    get_classifica()
