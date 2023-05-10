import threading
import time
import mysql.connector
import csv
import gestioneDatiGov
from dotenv import dotenv_values

class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.skipped_ids = []

    def run(self):
        now = time.localtime()
        self.insert_data_from_csv()

    def insert_data_from_csv(self):

        env = dotenv_values(".env") # da rimettere :/

        host_name = "localhost" #env['DB_HOST']
        host_user = "root" #env['DB_USER']
        host_pass = "" #env['DB_PASSWORD']
        host_dbname = "carbu_bot" #env['DB_NAME']

        mydb = mysql.connector.connect(
            host = host_name,
            user = host_user,
            password = host_pass,
            database = host_dbname,
        )
        cursor = mydb.cursor()
        
        # TO-DO:
        # aggiungere controllo orario per riscaricare tutto solo alle 8
         
        # elimina tutti i record dalla tabella benzinai
        # elimina tutti i record dalla tabella prezzi 
        cursor.execute('DELETE from prezzi where 1')
        # elimina tutti i record dalla tabella benzinai
        cursor.execute('DELETE from benzinai where 1')

        mydb.commit()
        
        with open('anagrafica_impianti_attivi.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            # Salta le prime 2
            next(csv_reader)
            next(csv_reader)
            
            sql = """INSERT INTO benzinai (idImpianto, gestore, bandiera, tipoImpianto, nomeImpianto, indirizzo, comune, provincia, latitudine, longitudine)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = []

            for row in csv_reader:
                if "NULL" in row or "" in row:
                    self.skipped_ids.append(row[0])
                    continue # saltala
                
                idI=row[0]
                gest=row[1]
                band=row[2]
                tipoI=row[3]
                nomeI=row[4]
                ind=row[5]
                com=row[6]
                prov=row[7]
                lat=row[8]
                long=row[9]

                val.append((idI, gest, band, tipoI, nomeI, ind, com, prov, lat, long))
                if len(val) > 1000:
                    cursor.executemany(operation = sql,seq_params= val)
                    val = []
                    mydb.commit()

            cursor.executemany(operation = sql,seq_params= val)
            val = []
            mydb.commit()

        with open('prezzo_alle_8.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            # Salta le prime 2
            next(csv_reader)
            next(csv_reader)

            sql = '''INSERT INTO prezzi (idImpianto, descCarburante, prezzo, isSelf, dtComu) 
                    VALUES (%s, %s, %s, %s, %s)'''
            val = []
            
            for row in csv_reader:
                if row[0] in self.skipped_ids:
                    continue # saltala

                idI=row[0]
                descCarb=row[1]
                prezzo=row[2]
                isSelf=row[3]
                dtComu=row[4]

                val.append((idI, descCarb, prezzo, isSelf, dtComu))
                if len(val) > 1000:
                    cursor.executemany(operation = sql,seq_params= val)
                    val = []
                    mydb.commit()
            
            cursor.executemany(operation = sql,seq_params= val)
            val = []
            mydb.commit()

            cursor.close()
            