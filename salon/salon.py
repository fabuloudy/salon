from room import Room


class Salon:
    def __init__(self, amountFirstRoom, amountSecondRoom, amountThirdRoom):
        self.house = {'1': Room(amountFirstRoom), '2': Room(amountSecondRoom),
                      '3': Room(amountThirdRoom)}

    def receiveRequest(self, request):
        self.house[str(request.numberProcedure)].addToQueue(request)

    def giveRequestMasters(self, currentTime, period):
        for key, _ in self.house.items():
            self.house[key].giveRequestMasters(currentTime, period)

    def updateDataForNextDay(self):
        for key, _ in self.house.items():
            self.house[key].updateData()
