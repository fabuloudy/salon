

class Master:

    def __init__(self,salary):
        self.numberOfClients = 0
        self.salary = salary
        self.spentTime = 0
        self.readyTakeRequest = 0

    def increaseNumberOfClients(self):
        self.numberOfClients = self.numberOfClients + 1

    def getNumberOfClients(self):
        return self.numberOfClients

    def getSalary(self):
        return self.salary

    def getSpentTime(self):
        return self.spentTime

    def setSpentTime(self,spentTime):
        self.spentTime = spentTime

    def getReadyTakeRequest(self):
        return self.readyTakeRequest

    def setReadyTakeRequest(self,readyTakeRequest):
        self.readyTakeRequest = readyTakeRequest

    def updateData(self):
        self.numberOfClients = 0
        self.spentTime = 0
        self.readyTakeRequest = 0