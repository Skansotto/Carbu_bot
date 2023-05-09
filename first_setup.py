import requests
from datetime import datetime
import mysql.connector
# custom
import prezzi
import benzinaio

utente = {  # TODO: RINOMINARLE COME NEL DB
    "username": None,
    "chat_id": None
}

veicolo = {
    "vehicleType": None,
    "fuelType": None,
    "tankCapacity": None,
    "maxKm": None
}

class first_setup:

    def __init__(self):
        pass

    def inserisciPersona(text):
        for key in utente.keys():
            if (utente[key] == None):
                utente[key] = text  # valore del bot
                break

    def inserisciVeicolo(text):
        for key in veicolo.keys():
            if (veicolo[key] == None):
                veicolo[key] = text  # valore del bot
                break
