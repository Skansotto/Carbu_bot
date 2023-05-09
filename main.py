from myTelegram import myTelegram
import time
from threading import Thread
from gestioneDB import MyThread

veicolo = {  # TODO: RINOMINARLE COME NEL DB
    "tipoVeicolo": None,
    "tipoCarburante": None,
    "capacitaSerbatoio": None,
    "maxKm": None
}

def inserimento(text):
    for key in veicolo.keys():
        if (veicolo[key] == None):
            veicolo[key] = text  # valore del bot
            break

def main():
    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")
    chatId = bot.get_chatId(bot.getUpdates())

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
        text = updates['result'][0]['message']['text']
        id = updates['result'][0]['message']['message_id']
        #bot.send_message(739998937, updates['result'])
        
        if (id != tempId):
            inserimento(text)
            bot.send_message(739998937, veicolo)
            tempId = id

        # if len(updates['result']) != initialLen:
        #     inserimento(updates['result'][-1]["message"]['text'])
        #     bot.send_message(739998937, veicolo)
        #     initialLen = len(updates['result'])
        
        # if updates['result'][0]['message']['text'] == "/nuovoVeicolo":
        #    bot.send_message(chatId, "Inserisci il nome del veicolo")

        time.sleep(2)


if __name__ == '__main__':
    main()
