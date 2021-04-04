from collections import deque
import random
from master import Master
class Room:

    MAX_SALARY = 3000
    MIN_SALARY = 200
    #queue = deque() #для запросов


    def __init__(self,amount):
        self.masters = list()
        for _ in range(0,amount):
            mas = Master(int(random.random() * (self.MAX_SALARY - self.MIN_SALARY + 1) + self.MIN_SALARY))
            self.masters.append(mas)
        #залезла
        self.queue = deque()
        self.wentAway = 0
        self.completedRequests = 0

    def addToQueue(self,request):
        if len(self.queue) == 5:
            self.wentAway = self.wentAway + 1
        else:
            self.completedRequests = self.completedRequests + 1
            self.queue.append(request)

    def getWentAway(self):
        return self.wentAway

    def getMasters(self):
        return self.masters

    def getQueueSize(self):
        return len(self.queue)

    def giveRequestMasters(self,currentTime,period):
        time = random.randint(int(period[0]),int(period[1]))
        busyMasters = set()
        while (len(self.queue) != 0 and len(busyMasters) != len(self.masters)):
            number = int(random.random() * len(self.masters))
            if (number in busyMasters and self.masters[number].getReadyTakeRequest() <= currentTime):
                master = self.masters[number]
                arrivedTime = self.queue.popleft().getArrivedTime()
                master.setReadyTakeRequest(max(master.getReadyTakeRequest(), arrivedTime) + time)
                master.increaseNumberOfClients()
                master.setSpentTime(master.getSpentTime() + time)
            busyMasters.add(number)

    def getAverageSalary(self):
        return self.getProfit() / len(self.masters)

    def getProfit(self):
        summ = 0
        for master in self.masters:
            summ = summ + 0.5 * master.getSalary() * master.getNumberOfClients()
        return summ

    def getAverageSpentTime(self):
        summ = 0
        for master in self.masters:
            summ = summ + master.getSpentTime()
        return summ / len(self.masters)

    def getCompletedRequests(self):
        return self.completedRequests - len(self.queue)

    def updateData(self):
        self.completedRequests = 0
        self.wentAway = 0
        self.queue = deque()
        for master in self.masters:
            master.updateData()


