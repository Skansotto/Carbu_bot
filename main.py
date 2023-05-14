from myTelegram import myTelegram
import time
from threading import Thread
from gestioneDB import MyThread
from gestioneDatiDB import gestioneDatiDB
import mysql.connector
import requests

def main():

    dati = MyThread()
    dati.start()

    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")

    # TO-DO:
    # Trovare un modo attendere invio messaggio

    temp = 0
    tempId = 0

    # attendi che qualcuno invii il comando /nuovoVeicolo
    _isListening = True

    while _isListening:
        chatId = bot.get_chatId()
        updates = bot.getUpdates()
        id = bot.get_messageId()
        #bot.send_message(739998937, updates['result'])

        # https://it.martech.zone/calculate-great-circle-distance/ sito con query qui sotto

        # queri in km
        query = '"SELECT *, (((acos(sin((".$latitude."*pi()/180)) * sin((`latitude`*pi()/180)) + cos((".$latitude."*pi()/180)) * cos((`latitude`*pi()/180)) * cos(((".$longitude."- `longitude`) * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) as distance FROM `table` WHERE distance <= ".$distance."'

        if updates.status_code==200:
            element = updates.json()
            for messaggio in element["result"]:
                if(str(messaggio["message"]["text"]).lower().find("/start") != -1): #risposta in caso di /start
                    text="Ciao, dove ti trovi?"

                    bot.send_message(chatId,text)

        # -- TEST 1 --
        # if (temp > 0 ):
        #     if (id != tempId):
        #         if (text == "ciao"):
        #         #inserimento(text)
        #             bot.send_message(bot.get_chatId(), "Benvenuto!")
        #             tempId = id

        # temp+1


        time.sleep(3)
        


if __name__ == '__main__':
    main()
