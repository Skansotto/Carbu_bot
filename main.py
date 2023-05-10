from myTelegram import myTelegram
import time
from threading import Thread
from gestioneDB import MyThread
from gestioneDatiDB import gestioneDatiDB

def main():

    dati = MyThread()
    dati.start()

    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")

    # TO-DO:
    # Trovare un modo attendere invio messaggio

    temp = 0
    tempId = 0

    # attendi che qualcuno invii il comando /nuovoVeicolo
    isListening = True

    while isListening:
        chatId = bot.get_chatId()
        updates = bot.getUpdates()
        text = bot.get_text()
        id = bot.get_messageId()
        #bot.send_message(739998937, updates['result'])
        
        if (temp > 0 ):
            if (id != tempId):
                if (text == "ciao"):
                #inserimento(text)
                    bot.send_message(bot.get_chatId(), "Benvenuto!")
                    tempId = id

        temp+1
        time.sleep(3)


if __name__ == '__main__':
    main()
