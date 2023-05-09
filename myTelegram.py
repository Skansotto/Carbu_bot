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

    def getUpdates(self, update_id=-1):
        #if (update_id == -1):
        urlUpdate = self.url+self.token+"/getUpdates?offset=-1"
        response = requests.get(urlUpdate)
        print(len(response.json()['result']))
        # else:
        #     urlUpdate = self.url+self.token+"/getUpdates?offset={update_id}"
        #     print(urlUpdate)
        #     response = requests.get(urlUpdate)
        #     rep = response.json()
        return response.json()

    def get_chatId(self, response):
        chat_id = response["result"][0]["message"]["chat"]["id"]
        return chat_id
    
    def get_updateId(self, response):
        update_id = response["result"][0]["update_id"]
        return update_id
    
    def get_text(self, response):
        text = response["result"][0]["text"]
        return text
    
    def send_message(self, chat_id, message):
        urlMessage = self.url+self.token+"/sendMessage?chat_id={chat_id}&text={message}"
        response = requests.get(urlMessage.format(chat_id=chat_id, message=message))
        return response.json()
    
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

        if (datetime.now() == datetime.hour(8)):
            chk=True;

        return chk;
