from room import Room
class Salon:
    def __init__(self,amountFirstHall,amountSecondHall,amountThirdHall):
        self.firstHall = Room(amountFirstHall)
        self.secondHall = Room(amountSecondHall)
        self.thirdHall = Room(amountThirdHall)

    def receiveRequest(self,request):
        if (request.getFirstService()):
            self.firstHall.addToQueue(request)
        elif (request.getSecondService()):
            self.secondHall.addToQueue(request)
        else:
            self.thirdHall.addToQueue(request)

    def giveRequestMasters(self,currentTime):
        self.firstHall.giveRequestMasters(currentTime)
        self.secondHall.giveRequestMasters(currentTime)
        self.thirdHall.giveRequestMasters(currentTime)

    def getFirstHall(self):
        return self.firstHall

    def getSecondHall(self):
        return self.secondHall

    def getThirdHall(self):
        return self.thirdHall

    def updateDataForNextDay(self):
        self.firstHall.updateData()
        self.secondHall.updateData()
        self.thirdHall.updateData()