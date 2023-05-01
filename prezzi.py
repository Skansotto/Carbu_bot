class prezzo:
        
    idImpianto = 0 
    descCarburante = ""
    prezzo = 0.0
    isSelf = False
    dtComu = ""

    def __init__(self, idImpianto, descCarburante, prezzo, isSelf, dtComu):
        self.idImpianto = idImpianto
        self.descCarburante = descCarburante
        self.prezzo = prezzo
        self.isSelf = isSelf
        self.dtComu = dtComu

    def __str__(self):
        return "idImpianto: " + str(self.idImpianto) + "\ndescCarburante: " + self.descCarburante + "\nprezzo: " + str(self.prezzo) + "\nisSelf: " + str(self.isSelf) + "\ndtComu: " + self.dtComu

    def getIdImpianto(self):
        return self.idImpianto
    
    def getDescCarburante(self):
        return self.descCarburante
    
    def getPrezzo(self):
        return self.prezzo
    
    def isSelf(self):
        return self.isSelf
    
    def getDtComu(self):
        return self.dtComu
    
    def setDtComu(self, dtComu):
        self.dtComu = dtComu

    def setDescCarburante(self, descCarburante):
        self.descCarburante = descCarburante
    
    def setPrezzo(self, prezzo):
        self.prezzo = prezzo
    
    def setIdImpianto(self, idImpianto):
        self.idImpianto = idImpianto
    
    def setSelf(self, isSelf):
        self.isSelf = isSelf
