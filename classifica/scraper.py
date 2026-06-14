for i, row in enumerate(rows):
        # 1. Cerchiamo il nome squadra, se non c'è, saltiamo la riga (evita il crash)
        team_link = row.find('a', class_='ftbl__cta--inline')
        if not team_link:
            continue
            
        nome_squadra = team_link.text.strip().upper()
        
        # 2. Recuperiamo le celle
        cells = row.find_all('td')
        if len(cells) < 9:
            continue
            
        # 3. Creiamo l'item
        item = ET.SubElement(root, "item")
        
        # 4. Inseriamo i dati
        ET.SubElement(item, "row_number").text = str(1775 + i)
        ET.SubElement(item, "SERIE").text = "A"
        ET.SubElement(item, "ANNO").text = "2025-2026"
        ET.SubElement(item, "TEAM").text = nome_squadra
        ET.SubElement(item, "PT").text = cells[2].text.strip()
        ET.SubElement(item, "G").text = cells[3].text.strip()
        ET.SubElement(item, "V").text = cells[4].text.strip()
        ET.SubElement(item, "N").text = cells[5].text.strip()
        ET.SubElement(item, "P").text = cells[6].text.strip()
        ET.SubElement(item, "GF").text = cells[7].text.strip()
        ET.SubElement(item, "GS").text = cells[8].text.strip()
        
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
