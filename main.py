from myTelegram import myTelegram
import time
from threading import Thread
from gestioneDB import MyThread
from gestioneDatiDB import gestioneDatiDB
import mysql.connector
import requests
import urllib.parse

def main():

    # finire il controllo/aggiornamento delle 8 di mattina
    dati = MyThread()
    dati.start()

    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")
    token = "6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo"

    # TO-DO:
    # Trovare un modo attendere invio messaggio

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

    #risultato = cursor.fetchall()

    # attendi che qualcuno invii il comando /nuovoVeicolo
    _isListening = True

    attesa=0

    # ciclo attesa messaggi
    while _isListening:

        #RICONTROLLARE IL METODO
        #chatId = bot.get_chatId()

        updates = bot.getUpdates()

        # https://it.martech.zone/calculate-great-circle-distance/ sito con query qui sotto

        # queri in km
        query = '"SELECT *, (((acos(sin((".$latitude."*pi()/180)) * sin((`latitude`*pi()/180)) + cos((".$latitude."*pi()/180)) * cos((`latitude`*pi()/180)) * cos(((".$longitude."- `longitude`) * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) as distance FROM `table` WHERE distance <= ".$distance."'

        for messaggio in updates:
            if "location" not in messaggio["message"].keys():
                if(str(messaggio["message"]["text"]).lower().find("/start") != -1): #risposta in caso di /start
                    #azzero il counter dei secondi di attesa di un messaggio dell'utente
                    attesa = 0
                    chat_id = messaggio["message"]["chat"]["id"]

                    cursor.execute("SELECT * FROM users WHERE chatId="+ str(chat_id))
                    risultato = cursor.fetchall()

                    if (len(risultato)==1):
                        requests.get('https://api.telegram.org/bot6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo/sendMessage?chat_id='+str(chat_id)+'&text=Scegli una operazione:&reply_markup=%7B%22keyboard%22%3A+%5B%5B%22nuovoVeicolo%22%5D%5D%7D')
                    else:
                        #salvare nuovo utente
                        nomeUtente = ""
                        chk = False
                        text="Ciao, come ti chiami?"
                        bot.send_message(chat_id, text)

                        while (chk == False):
                            agg = bot.getUpdates()
                            for mex in agg:
                                if (str(mex["message"]["text"])!= "" or str(mex(["message"]["text"])) != None):
                                    nomeUtente = str(mex["message"]["text"])
                                    chk = True
                                else:
                                    chk = False


                        sql = 'INSERT INTO users (chatId , username, stato) VALUES ('+str(chat_id)+', "'+nomeUtente+'", "data")'
                        cursor.execute(sql)
                        mydb.commit()

                #Inserimento nuovo veicolo con sovrascrizione del precedente (se esistente)
                if (str(messaggio["message"]["text"]) == "nuovoVeicolo"):

                    chat_id = messaggio["message"]["chat"]["id"]

                    tipoVeicolo = ""
                    tipoCarburante = ""
                    capacitaSerbatoio = ""
                    maxKm = ""

                    chk = False

                    #fare bottonitipo veicolo
                    #requests.get('https://api.telegram.org/bot6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo/sendMessage?chat_id='+str(chat_id)+'&text=Che veicolo vuoi inserire?&reply_markup=%7B%22keyboard%22%3A+%5B%5B%22Auto%22%82%22Moto%22%5D%5D%7D')
                    bot.send_message(chat_id, "Che veicolo vuoi inserire? (auto - moto)")

                    while (chk == False):
                            agg = bot.getUpdates()
                            for mex in agg:
                                if (str(mex["message"]["text"]) == "moto" or str(mex["message"]["text"]) == "auto"):
                                    tipoVeicolo = str(mex["message"]["text"])
                                    chk = True
                                else:
                                    chk = False

                    #fare bottoni tipo carburante
                    bot.send_message(chat_id, "Che tipo di carburante utilizza? (benzina - diesel - gasolio - gpl - metano)")

                    chk = False
                    while (chk == False):
                            agg = bot.getUpdates()
                            for mex in agg:
                                if (str(mex["message"]["text"]) == "benzina" or str(mex["message"]["text"]) == "diesel" or str(mex["message"]["text"]) == "gasolio" or str(mex["message"]["text"]) == "gpl" or str(mex["message"]["text"]) == "metano"):
                                    tipoCarburante = str(mex["message"]["text"])
                                    chk = True
                                else:
                                    chk = False

                    bot.send_message(chat_id, "Inserisci la capacità del serbatoio? (in litri, es: 12)")

                    chk = False
                    while (chk == False):
                            agg = bot.getUpdates()
                            for mex in agg:
                                if (int(mex["message"]["text"]) > 0):  #Capire se è un intero -> int(mex["message"]["text"]) == mex["message"]["text"]
                                    capacitaSerbatoio = int(mex["message"]["text"])
                                    chk = True
                                else:
                                    chk = False

                    bot.send_message(chat_id, "Quanti chilometri sei disposto a fare? (es: 10)")
                    chk = False
                    while (chk == False):
                            agg = bot.getUpdates()
                            for mex in agg:
                                if (int(mex["message"]["text"]) > 0): #aggiungere controllo se è intero
                                    maxKm = int(mex["message"]["text"])
                                    chk = True
                                    #essendo l'ultimo if della sezione inserimento dati, aggiorna lo stato dell'utente
                                    cursor.execute("UPDATE users SET stato='location' WHERE chatId="+ str(chat_id))
                                    mydb.commit()
                                else:
                                    chk = False

                    sql = 'INSERT INTO veicoli (vehicleType, fuelType, tankCapacity, maxKm, idChatUtente) VALUES ("'+tipoVeicolo+'", "'+tipoCarburante+'", '+str(capacitaSerbatoio)+', '+str(maxKm)+', '+str(chat_id)+')'
                    cursor.execute(sql)
                    mydb.commit()

                    #cursor.execute("UPDATE users SET stato='singing' WHERE "+ chat_id)

                if (str(messaggio["message"]["text"]) == "/help"):
                    #azzero il counter dei secondi di attesa di un messaggio dell'utente
                    attesa = 0

                    chat_id = messaggio["message"]["chat"]["id"]

                    text = "Ciao, sono Carbu_bot il tuo amico benzinaio di fiducia.\nDopo il primo accesso e l'inserimento dei tuoi dati, puoi inviare la posizione per ricevere il benzinaio più conveniente in base ai tuoi dati.\nSe vuoi inserire un nuovo veicolo e sostituire il precedente scrivi 'nuovoVeicolo'."
                    #scrivere istruzioni per il bot

                    bot.send_message(chat_id, text)
            
            if "location" in messaggio["message"].keys():

                chat_id = messaggio["message"]["chat"]["id"]

                cursor.execute("SELECT * FROM users WHERE chatId="+ str(chat_id))
                risultato = cursor.fetchall()

                if (len(risultato)==1 and risultato["stato"]=="location"):
                    cursor.execute("SELECT * FROM veicoli WHERE chatId="+ str(chat_id))
                    veicolo = cursor.fetchall()

                    tipoVeicolo = veicolo["vehicleType"]
                    tipoCarburante = veicolo["fuelType"]
                    capacitaSerbatoio = veicolo["tankCapacity"]
                    maxKm = veicolo["maxKm"]

                    latitudine = str(messaggio["message"]["location"]["latitude"])
                    longitudine = str(messaggio["message"]["location"]["logitude"])
                    
                    queryRicercaBenzinai = 'SELECT *, (((acos(sin(('+latitudine+'*pi()/180)) * sin((`latitude`*pi()/180)) + cos(('+latitudine+'*pi()/180)) * cos((`latitude`*pi()/180)) * cos((('+longitudine+'- `longitude`) * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) as distance FROM `benzinai` WHERE distance <= '+maxKm +''
                    
                    #questa è la query di concil che le dicevo --> a lei va a me no :/
                    """SELECT * FROM impianti join prezzi on impianti.idImpianto = prezzi.idImpianto WHERE descCarburante = "Benzina" AND (acos(sin(45.815132)*sin( Latitudine )+cos(45.815132)*cos( Latitudine )*cos( Longitudine - 9.227647))*6371) BETWEEN 0 AND 400 ORDER By prezzo,(acos(sin(45.815132)*sin( Latitudine )+cos(45.815132)*cos( Latitudine )*cos( Longitudine - 9.227647))*6371) ASC;"""
                else:
                    bot.send_message(chat_id, "Inserisci prima i tuoi dati con /start")
                 



            #non entra qui: WHY??
            '''if (len(messaggio["result"]) == 0):
                attesa+2
                if(attesa > 25):
                    text = "Sembra tu non sappia da dove iniziare ..."
                    #scrivere istruzioni per il bot
                    bot.send_message(chat_id, text)
                    attesa = 0'''

        time.sleep(2)
        


if __name__ == '__main__':
    main()
