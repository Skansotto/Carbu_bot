from myTelegram import myTelegram
from first_setup import first_setup
import time
from threading import Thread
from gestioneDB import MyThread





def main():
    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")
    fs = first_setup()
    chatId = bot.get_chatId()

    # bot.getUpdates()['result'][0]['message']['text'] == "/start"

    # dati = MyThread()
    # dati.start()

    # TO-DO:
    # Trovare un modo attendere invio messaggio

    initialLen = 0
    tempId = 0
    # attendi che qualcuno invii il comando /nuovoVeicolo
    while True:
        updates = bot.getUpdates()
        text = bot.get_text()
        id = bot.get_messageId()
        #bot.send_message(739998937, updates['result'])
        
        if (id != tempId):
            inserimento(text)
            bot.send_message(bot.get_chatId(), veicolo)
            tempId = id

        time.sleep(3)


if __name__ == '__main__':
    main()
