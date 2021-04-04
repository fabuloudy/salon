
class Request:

    def __init__(self,firstProcedure,secondProcedure,thirdProcedure,arrivedTime):
        self.firstProcedure = firstProcedure
        self.secondProcedure = secondProcedure
        self.thirdProcedure = thirdProcedure
        self.arrivedTime = arrivedTime

    def getArrivedTime(self):
        return self.arrivedTime

    def getFirstProcedure(self):
        return self.firstProcedure

    def getSecondProcedure(self):
        return self.secondProcedure

    def getThirdProcedure(self):
        return self.thirdProcedure