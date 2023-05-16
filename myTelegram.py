import requests
from datetime import datetime
import mysql.connector
# custom
import prezzi
import benzinaio

class myTelegram:

    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot"
        self.getUpdates()

    def getUpdates(self):
        urlUpdate = self.url+self.token+"/getUpdates" # prima avevo messo -1
        self.response = requests.get(urlUpdate)
        
        lst = []
        if self.response.status_code==200:
            lst = self.response.json()
            if len(lst["result"]) > 0:
                requests.get(urlUpdate,params={"offset":lst['result'][-1]['update_id']+1})
         
        return lst['result']

    def get_chatId(self, messaggio):
        return messaggio["message"]["chat"]["id"]
    
    def get_messageId(self, messaggio):
        return messaggio["message"]["message_id"]

    def get_updateId(self, messaggio):
        return messaggio["update_id"]
    
    def get_text(self, messaggio):
        if (messaggio['message']["text"]!=None):
            return messaggio['message']["text"]
        else:
            return ""
    
    def send_message(self, chat_id, message):
        urlMessage = self.url+self.token+"/sendMessage?chat_id={chat_id}&text={message}"
        response = requests.get(urlMessage.format(chat_id=chat_id, message=message))
        return response.json()
    
    # da finire
    def controllo_orario():
        chk=False;

        #controlla se l'orario attuale è uguale alle 8 di mattina
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="carbu_bot"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT lastUpdate * FROM update_dati")

        result = mycursor.fetchall()

        if (datetime.now().hour >= 8):
            chk=True;

        return chk;
