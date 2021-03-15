
class Request: 

    def __init__(self,firstService,secondService,thirdService,arrivedTime):
        self.firstService = firstService
        self.secondService = secondService
        self.thirdService = thirdService
        self.arrivedTime = arrivedTime

    def getArrivedTime(self):
        return self.arrivedTime

    def getFirstService(self):
        return self.firstService

    def getSecondService(self):
        return self.secondService

    def getThirdService(self):
        return self.thirdService