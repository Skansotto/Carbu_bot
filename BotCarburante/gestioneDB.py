import threading
import time
import mysql.connector
import csv
import gestioneData

class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.skipped_ids = []

    def run(self):
        #while True:
        now = time.localtime()
            #if now.tm_hour == 8 and now.tm_min == 10:
        self.insert_data_from_csv()
            #time.sleep(24 * 60 * 60)
            #else:
            # Wait for 10 seconds before checking again
            #time.sleep(10)

    def insert_data_from_csv(self):
        #gestioneData.gestioneData.downloadBenziani(self)
        #gestioneData.gestioneData.downloadPrezzi(self)
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="carbu_bot"
        )
        cursor = mydb.cursor()
        
        cursor.execute('DELETE from prezzi where 1')
        # drop foreign key constraint on prezzo table
        #cursor.execute('ALTER TABLE prezzi DROP FOREIGN KEY benzinai')
        # truncate table
        cursor.execute('DELETE from benzinai where 1')
        # recreate foreign key constraint on prezzi table
        #cursor.execute('ALTER TABLE prezzi ADD CONSTRAINT benzinai FOREIGN KEY (idImpianto) REFERENCES benzinai (idImpianto)')
        

        with open('anagrafica_impianti_attivi.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            # Skip the first 2 row
            next(csv_reader)
            next(csv_reader)
            
            for row in csv_reader:
                # check if any of the fields in the row are "NULL" or ""
                if "NULL" in row or "" in row:
                    self.skipped_ids.append(row[0])  # add ID to list of skipped IDs
                    continue  # skip this row
                #get data from row
                idI=int(row[0])
                gest=row[1]
                band=row[2]
                tipoI=row[3]
                nomeI=row[4]
                ind=row[5]
                com=row[6]
                prov=row[7]
                lat=row[8]
                long=row[9]
                #insert in db
                cursor.execute('INSERT INTO benzinai (idImpianto, gestore, bandiera, tipoImpianto, nomeImpianto, indirizzo, comune, provincia, latitudine, longitudine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idI, gest, band, tipoI, nomeI, ind, com, prov, lat, long))
                print("impianti attivi")
            mydb.commit()

        with open('prezzo_alle_8.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            # Skip the first 2 row
            next(csv_reader)
            next(csv_reader)
            
            for row in csv_reader:
                # check if any of the fields in the row are "NULL" or ""
                if row[0] in self.skipped_ids:
                    continue  # skip this row
                #get data from row
                idI=int(row[0])
                descCarb=row[1]
                prezzo=row[2]
                isSelf=row[3]
                dtComu=row[4]
                #insert in db
                cursor.execute('INSERT INTO prezzi (idImpianto, descCarburante, prezzo, isSelf, dtComu) VALUES (%s, %s, %s, %s, %s)', (idI, descCarb, prezzo, isSelf, dtComu))
                mydb.commit()
                print("prezzi mattutini")

            cursor.close()
            