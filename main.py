from myTelegram import myTelegram
from time import sleep, perf_counter, time
from threading import Thread
from gestioneDB import MyThread

def main():
    bot = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")
    chatId = bot.get_chatId(bot.getUpdates())

    # bot.getUpdates()['result'][0]['message']['text'] == "/start"
    
    # print(time.now())
    dati = MyThread()
    dati.start()

    # TO-DO:
    # Trovare un modo attendere invio messaggio

    # attendi che qualcuno invii il comando /nuovoVeicolo
    while True:
        updates = bot.getUpdates()
        
        if updates['result'][0]['message']['text'] == "/nuovoVeicolo":
            bot.send_message(chatId, "Inserisci il nome del veicolo")


if __name__ == '__main__':
    main()







# def task():
#     print('')
#     sleep(1)
#     print('done')


# start_time = perf_counter()

# # create two new threads
# t1 = Thread(target=task)
# t2 = Thread(target=task)

# # start the threads
# t1.start()
# t2.start()

# # wait for the threads to complete
# t1.join()
# t2.join()

# end_time = perf_counter()

# print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')