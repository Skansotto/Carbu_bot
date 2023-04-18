import requests
import csv
import logging
import mysql.connector
# custom
import prezzi
import benzinaio

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"{TG_VER} versione non compatibile."
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TIPO, CARBURANTE, CAPACITA, MAXKM = range(4)

tastieraTipo = [["Auto", "Moto"]]
tastieraCaburante = [["Benzina", "Diesel", "Metano"]]
tastieraCapacita = [["10", "20", "30", "40", "50"]]
tastieraMaxkm = [["5", "10", "20", "40", "50"]]

class myTelegram:

    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot"


    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # avvia il bot
        user = update.message.from_user

        await update.message.reply_text(
            f"Ciao " + user.username + " sono CarbuBot, il tuo assistente personale per la scelta della migliore stazione di rifornimento per il tuo veicolo.\n\n"
            "Invia /cancel per smettere di parlare con me.\n\n"
            "Che veicolo vuoi registrare?",

            reply_markup=ReplyKeyboardMarkup(
                tastieraTipo, one_time_keyboard=True, input_field_placeholder="Seleziona il tipo di veicolo:"
            ),
        )
        # user = update.message.from_user
        # await update.message.reply_text(f"Ciao{user}")
        return CARBURANTE
    
    async def carburante(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        
        user = update.message.from_user

        await update.message.reply_text(
            "Che tipo di carburante utilizza?",

            reply_markup=ReplyKeyboardMarkup(
                tastieraCaburante, one_time_keyboard=True, input_field_placeholder="Seleziona il tipo di carburante:"
            ),
        )

        return CAPACITA


    async def capacita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user = update.message.from_user

        await update.message.reply_text(
            "Qual'è la capacità del serbatoio approssimata in litri?",

            reply_markup=ReplyKeyboardMarkup(
                tastieraCapacita, one_time_keyboard=True, input_field_placeholder="Seleziona la capacità del tuo serbatoio:"
            ),
        )

        return MAXKM


    async def maxkm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user = update.message.from_user

        await update.message.reply_text(
            "Quanti chilometri sei disposto a fare per fare rifornimento?",

            reply_markup=ReplyKeyboardMarkup(
                tastieraMaxkm, one_time_keyboard=True, input_field_placeholder="Seleziona i km che sei disposto a fare:"
            ),
        )

        return ConversationHandler.END


    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user = update.message.from_user

        logger.info("L'utente %s ha chiuso la conversazione.", user.first_name)
        await update.message.reply_text(
            "Arrivederci!", reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def getUpdates(self, update_id=-1):
        if (update_id == -1):
            urlUpdate = self.url+self.token+"/getUpdates"
            response = requests.get(urlUpdate)
            print(response)
        else:
            urlUpdate = self.url+self.token+"/getUpdates?offset={update_id}"
            response = requests.get(urlUpdate)
            rep = response.json()
        return response.json()

    def get_chat_and_update_ids(self, response):
        chat_id = response["result"][0]["message"]["chat"]["id"]
        update_id = response["result"][0]["update_id"]
        return chat_id, update_id

    def downloadPrezzi(self, url="https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv"):
        response = requests.get(url)

        with open('prezzo_alle_8.csv', 'wb') as f:
            f.write(response.content)
        
        recordPrezzi = []

        with open("prezzo_alle_8.csv", newline='', encoding='utf-8') as csv:
            new_var = csv
            reader = csv.reader(new_var, delimiter=';')
            # Skip the header row
            next(reader)
            next(reader)
            for row in reader:
                # Create a new Record object for each row and append it to the list
                record = prezzi.prezzo(row[0], row[1], float(
                    row[2].replace(',', '.')), row[3], row[4])
                recordPrezzi.append(record)
        return recordPrezzi

    def downloadBenziani(self, url="https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"):
        """Download the CSV data from the URL and save it to a file."""
        response = requests.get(url)
        with open('anagrafica_impianti_attivi.csv', 'wb') as f:
            f.write(response.content)
        """Read and process the CSV data from the file into an array."""
        recordImpianti = []
        with open("anagrafica_impianti_attivi.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # Skip the header row
            next(reader)
            next(reader)
            for row in reader:
                # Create a new Record object for each row and append it to the list
                record = benzinaio.Impianto(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                recordImpianti.append(record)
        return recordImpianti
    
    def insert_data_from_csv():

        myTelegram.downloadBenziani()
        myTelegram.downloadPrezzi()
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="carbu_bot"
        )
        
        cursor = mydb.cursor()
        #...

        with open('anagrafica_impianti_attivi.csv',encoding='utf-8') as csv:
            csv_reader = csv.reader(csv, delimiter=';')
           
            #Salta le prime 2 righe
            next(csv_reader)
            next(csv_reader)
            
            for row in csv_reader:
                idI=int(row[0])
                gest=row[1]
                band=row[2]
                tipoI=row[3]
                nomeI=row[4]
                ind=row[5]
                com=row[6]
                prov=row[7]
                lat=row[8]
                long=row[9]
                #insert in db
                cursor.execute('INSERT INTO impianto (idImpianto, gestore, bandiera, tipoImpianto, nomeImpianto, indirizzo, comune, provincia, latitudine, longitudine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idI, gest, band, tipoI, nomeI, ind, com, prov, lat, long))
            mydb.commit()
            cursor.close()
        
