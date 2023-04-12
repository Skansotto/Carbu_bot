import requests
from myTelegram import myTelegram

#classe operazioni principali
t = myTelegram("6297186887:AAGsGTHHqERmCnFTx7KwVZhzHC3OJiuc1Uo")

#classe che riceve aggiornamenti sui messaggi
print(t.getUpdates()) #da fare nella classe