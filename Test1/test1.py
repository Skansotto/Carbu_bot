import requests
from myTelegram import myTelegram
token = "6151683029:AAGu4Hf_TMZ4Kv2EnJnXHELXVJZMpt5vHxg"
t = myTelegram(token)

t.getUpdates() #da fare nella classe

URL = f"https://api.telegram.org/bot{token}/"

servizioUpdate = "getUpdates"
servizioSend = "sendMessage"

result = requests.get(URL+servizioUpdate)

# if result.status_code==200:
#     dato=result.json()
#     print(dato)

if result.status_code==200:
    dato=result.json()
    if dato["ok"]:
        print("Num messaggi: " + str(len(dato["result"])))
        for messaggio in dato ["result"]:
            if(str(messaggio["message"]["text"]).lower().find("ciao") != -1):
                #rispondere
                text = "ciao anche a te!"
                chatID = messaggio["message"]["chat"]["id"]

                print(text)
                print(chatID)

                requests.get(URL+servizioSend, params={"chat_id":chatID, "text":text})

        requests.get(URL+servizioSend, params={"offset":dato["result"][-1]["update_id"]})