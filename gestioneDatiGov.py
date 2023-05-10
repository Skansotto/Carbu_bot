import requests
import csv
import mysql.connector

import prezzi
from benzinaio import benzinaio

class gestioneDatiGov:
    
    def __init__(self):
        pass
    
    def downloadPrezzi(self,url="https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv"):

        response = requests.get(url)

        with open('prezzo_alle_8.csv', 'wb') as f:
            f.write(response.content)

        recordPrezzi = []

        with open("prezzo_alle_8.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # Skip the header row
            next(reader)
            next(reader)
            for row in reader:
                record = prezzi.prezzo(row[0], row[1], float(row[2].replace(',', '.')), row[3], row[4])
                recordPrezzi.append(record)
        
        print("prezzi")
        return recordPrezzi

    def downloadBenziani(self,url="https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"):

        response = requests.get(url)
        print(response)
        open('anagrafica_impianti_attivi.csv', 'w').write(response.content.decode('utf-8'))
        
        # Mette il file in un array
        recordImpianti = []
        with open("anagrafica_impianti_attivi.csv", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            # Salta le prime righe
            next(reader)
            next(reader)
            for row in reader:
                record = benzinaio(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                recordImpianti.append(record)

        print("benzinai")
        return recordImpianti