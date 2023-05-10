import threading
import time
import mysql.connector
import csv
import gestioneDatiGov
from dotenv import dotenv_values

host_name = "localhost"
host_user = "root"
host_pass = ""
host_dbname = "carbu_bot"


class gestioneDatiDB():

    def __init__(self):
        pass

    # def run(self):
    #     now = time.localtime()
    #     self.insert_data_from_csv()

    def insert_persona(self, username, chatId):

        mydb = mysql.connector.connect(
            host=host_name,
            user=host_user,
            password=host_pass,
            database=host_dbname
        )

        cursor = mydb.cursor()

        cursor.execute('INSERT INTO users (chatId, username) VALUES (%s, %s)', (username, chatId))
        print("Utente inserito con successo")
        res = mydb.commit()

        cursor.close()

        return res

    def insert_veicolo(self, vehicleType, fuelType, tankCapacity, maxKm, idChatUtente):

        eseguito = False

        mydb = mysql.connector.connect(
            host=host_name,
            user=host_user,
            password=host_pass,
            database=host_dbname
        )

        cursor = mydb.cursor()

        cursor.execute('INSERT INTO veicoli (vehicleType, fuelType, tankCapacity, maxKm, idChatUtente) VALUES (%s, %s, %i, %i, %i)', (vehicleType, fuelType, tankCapacity, maxKm,idChatUtente))
        
        res = mydb.commit()

        if (res == True):
            print("Veicolo inserito con successo")

        cursor.close()

        return res
