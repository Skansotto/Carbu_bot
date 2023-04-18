import requests
from myTelegram import myTelegram

#classe operazioni principali
t = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")

#classe che riceve aggiornamenti sui messaggi

messaggi = t.getUpdates()

for m in messaggi:
    print(m) #da fare nella classe
    