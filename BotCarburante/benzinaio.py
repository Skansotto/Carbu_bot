class benzinaio:
    
    idImpianto = 0 
    gestore = ""
    bandiera = ""
    tipoImpianto = ""
    nomeImpianto = ""
    indirizzo = ""
    comune = ""
    provincia = ""
    latitudine = 0.0
    longitudine = 0.0

    def __init__(self, idImpianto, gestore, bandiera, tipoImpianto, nomeImpianto, indirizzo, comune, provincia, latitudine, longitudine):
        self.idImpianto = idImpianto
        self.gestore = gestore
        self.bandiera = bandiera
        self.tipoImpianto = tipoImpianto
        self.nomeImpianto = nomeImpianto
        self.indirizzo = indirizzo
        self.comune = comune
        self.provincia = provincia
        self.latitudine = latitudine
        self.longitudine = longitudine            

    def __str__(self):
        return "idImpianto: " + str(self.idImpianto) + "\ngestore: " + str(self.gestore) + "\nbandiera: " + str(self.bandiera) + "\ntipoImpianto: " + str(self.tipoImpianto) + "\nnomeImpianto: " + str(self.nomeImpianto) + "\nindirizzo: " + str(self.indirizzo) + "\ncomune: " + str(self.comune) + "\nprovincia: " + str(self.provincia) + "\nlatitudine: " + str(self.latitudine) + "\nlongitudine: " + str(self.longitudine)
    
    def getNome():
        return getattr(benzinaio, 'nome')
    
    def setNome(nomeBenzinaio):
        return setattr(benzinaio, nomeBenzinaio)
    
    def getIdImpianto():
        return getattr(benzinaio, 'idImpianto')
    
    def setIdImpianto(idImpianto):
        return setattr(benzinaio, 'idImpianto', idImpianto)
    
    def getGestore():
        return getattr(benzinaio, 'gestore')
    
    def setGestore(gestore):
        return setattr(benzinaio, 'gestore', gestore)
    
    def getBandiera():
        return getattr(benzinaio, 'bandiera')
    
    def setBandiera(bandiera):
        return setattr(benzinaio, 'bandiera', bandiera)
    
    def getTipoImpianto():
        return getattr(benzinaio, 'tipoImpianto')
    
    def setTipoImpianto(tipoImpianto):
        return setattr(benzinaio, 'tipoImpianto', tipoImpianto)
    
    def getNomeImpianto():
        return getattr(benzinaio, 'nomeImpianto')
    
    def setNomeImpianto(nomeImpianto):
        return setattr(benzinaio, 'nomeImpianto', nomeImpianto)
    
    def getIndirizzo():
        return getattr(benzinaio, 'indirizzo')
    
    def setIndirizzo(indirizzo):
        return setattr(benzinaio, 'indirizzo', indirizzo)
    
    def getComune():
        return getattr(benzinaio, 'comune')
    
    def setComune(comune):
        return setattr(benzinaio, 'comune', comune)
    
    def getProvincia():
        return getattr(benzinaio, 'provincia')
    
    def setProvincia(provincia):
        return setattr(benzinaio, 'provincia', provincia)
    
    def getLatitudine():
        return getattr(benzinaio, 'latitudine')
    
    def setLatitudine(latitudine):
        return setattr(benzinaio, 'latitudine', latitudine)
    
    def getLongitudine():
        return getattr(benzinaio, 'longitudine')
    
    def setLongitudine(longitudine):
        return setattr(benzinaio, 'longitudine', longitudine)