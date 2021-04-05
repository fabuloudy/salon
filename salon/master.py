
class Master:

    def __init__(self, salary):
        self.numberOfClients = 0
        self.salary = salary
        self.spentTime = 0
        self.readyTakeRequest = 0

    def increaseNumberOfClients(self):
        self.numberOfClients = self.numberOfClients + 1

    def updateData(self):
        self.numberOfClients = 0
        self.spentTime = 0
        self.readyTakeRequest = 0
