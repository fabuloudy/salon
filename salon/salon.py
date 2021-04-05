from room import Room


class Salon:
    def __init__(self, amountFirstRoom, amountSecondRoom, amountThirdRoom):
        self.firstRoom = Room(amountFirstRoom)
        self.secondRoom = Room(amountSecondRoom)
        self.thirdRoom = Room(amountThirdRoom)

    def receiveRequest(self, request):
        if (request.firstProcedure):
            self.firstRoom.addToQueue(request)
        elif (request.secondProcedure):
            self.secondRoom.addToQueue(request)
        else:
            self.thirdRoom.addToQueue(request)

    def giveRequestMasters(self, currentTime, period):
        self.firstRoom.giveRequestMasters(currentTime, period)
        self.secondRoom.giveRequestMasters(currentTime, period)
        self.thirdRoom.giveRequestMasters(currentTime, period)

    def updateDataForNextDay(self):
        self.firstRoom.updateData()
        self.secondRoom.updateData()
        self.thirdRoom.updateData()
