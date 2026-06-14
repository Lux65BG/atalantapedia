for row in rows:
        # Cerchiamo il nome squadra
        team_link = row.find('a', class_='ftbl__cta--inline')
        if not team_link: continue
        nome_squadra = team_link.text.strip().upper()
        
        # Cerchiamo i dati usando le classi specifiche (più sicuro!)
        # Sky usa queste classi per identificare le colonne
        pts = row.find('td', class_='ftbl__competition-ranking__body-cell--points')
        g = row.find('td', class_='ftbl__competition-ranking__body-cell--mobile-show') # Spesso è questa la classe per le giocate
        
        # Se non troviamo le classi, proviamo a prenderli dai 'span' dentro le celle
        # Questo è il metodo più robusto:
        spans = row.find_all('span', class_='ftbl__competition-ranking__body-cell-span')
        
        # Se abbiamo almeno 7 span, li mappiamo così:
        if len(spans) >= 7:
            item = ET.SubElement(root, "item")
            ET.SubElement(item, "row_number").text = str(1775 + i)
            ET.SubElement(item, "SERIE").text = "A"
            ET.SubElement(item, "ANNO").text = "2025-2026"
            ET.SubElement(item, "TEAM").text = nome_squadra
            ET.SubElement(item, "G").text = spans[0].text.strip()
            ET.SubElement(item, "V").text = spans[1].text.strip()
            ET.SubElement(item, "N").text = spans[2].text.strip()
            ET.SubElement(item, "P").text = spans[3].text.strip()
            ET.SubElement(item, "GF").text = spans[4].text.strip()
            ET.SubElement(item, "GS").text = spans[5].text.strip()
            ET.SubElement(item, "PT").text = spans[6].text.strip()
            
            # Logica POS
            pos = "2" if nome_squadra == "ATALANTA" else ("3" if i >= 17 else ("1" if i == 0 else "0"))
            ET.SubElement(item, "POS").text = pos
