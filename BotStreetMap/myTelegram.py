import requests

class myTelegram:

    def __init__(self, token):
        self.token=token
        self.url = "https://api.telegram.org/bot"

    def getUpdates(self):
        urlUpdate = self.url+self.token+"/getUpdates"

        messageList=[]

        result = requests.post(urlUpdate)

        if result.status_code==200:
            dato=result.json()
            print(dato)

        if dato["ok"]:
            print(dato["result"])

            for messaggio in dato["result"]:
                #se il testo del messaggio è "ciao"
                if str(messaggio["message"]["text"]).lower().find("ciao")!=-1 :
                    #risposta
                    text = "Ciao anche a te"
                    chatId = messaggio["message"]["chat"]["id"]
                    mess = chatId
                    print(mess)
                    print(text)
                    print(chatId)
                    
                    requests.get(urlUpdate, params={"chat_id": chatId, "text":text})
                
        else:
            print("Errore!!!")
            messageList.append({})

        return messageList
    

# #nomi dei diversi tipi di servizio
# servizioUpdate = "getUpdates"
# servizioSend = "sendMessage"

# #risultato della richiesta al servizio update
# result = requests.get(URL+servizioUpdate)

# if result.status_code==200: #se la richiesta è andata a buon fine
#     dato=result.json()
#     if dato["ok"]:
#         print("Num messaggi: " + str(len(dato["result"])))
#         for messaggio in dato ["result"]:
#             if(str(messaggio["message"]["text"]).lower().find("ciao") != -1):
#                 #rispondere
#                 text = "ciao anche a te!"
#                 chatID = messaggio["message"]["chat"]["id"]

#                 print(text)
#                 print(chatID)

#                 requests.get(URL+servizioSend, params={"chat_id":chatID, "text":text})

#         requests.get(URL+servizioSend, params={"offset":dato["result"][-1]["update_id"]})