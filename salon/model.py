from salon import Salon
from statistics import Statistic
from request import Request
import random
import re
class Model:

    oneDay = 480
    def __init__(self,firstRoomAmount, secondRoomAmount, thirdRoomAmount,interval,
                    requestPeriod,taskPeriod):
        self.salon = Salon(firstRoomAmount, secondRoomAmount, thirdRoomAmount)
        self.timeInterval = self.takeTimeInterval(interval)
        self.timePerOneDay = 0
        self.numberOfDay = 0
        self.timeStep = 0
        self.countRequestDay = 0
        self.allLostRequests = 0
        self.allAverageSalary = 0
        self.allAverageWorkTime = 0
        self.allCompletedRequests = 0
        self.allProfit = 0
        self.allFreeTime = 0
        self.timeRequestPeriod = self.takePeriod(requestPeriod)
        self.timeTaskPeriod = self.takePeriod(taskPeriod)

    def takeTimeInterval(self,interval):
        switcher={
            "15 минут": 15,
            "30 минут": 30,
            "1 час": 60
        }
        return switcher.get(interval,15)
    def takePeriod(self,str_period):
        period = re.findall(r'\d{1,3}', str_period)
        print(period)
        return period

    def nextStep(self):
        while (self.timeStep < self.timeInterval):
            self.salon.giveRequestMasters(self.timeStep + self.timePerOneDay,self.timeTaskPeriod)
            self.timeStep = self.timeStep + self.generateRequest(self.timeStep + self.timePerOneDay)
            self.countRequestDay = self.countRequestDay + 1
        self.timePerOneDay = self.timePerOneDay + self.timeInterval
        self.salon.giveRequestMasters(self.timePerOneDay,self.timeTaskPeriod)
        if (self.timePerOneDay == self.oneDay):
            self.numberOfDay = self.numberOfDay + 1
            self.timePerOneDay = 0
            self.timeStep = 0
            return self.collectStatistics()
        else:
            self.timeStep = self.timeStep - self.timeInterval
        return None

    def collectStatistics(self):
        lostRequests = self.salon.getFirstRoom().getWentAway() + self.salon.getSecondRoom().getWentAway() + self.salon.getThirdRoom().getWentAway()
        self.allLostRequests = self.allLostRequests + lostRequests
        averageSalary = int((self.salon.getFirstRoom().getAverageSalary() + self.salon.getSecondRoom().getAverageSalary() + self.salon.getThirdRoom().getAverageSalary()) / 3)
        self.allAverageSalary += averageSalary
        averageSpentTime = int((self.salon.getFirstRoom().getAverageSpentTime() + self.salon.getSecondRoom().getAverageSpentTime() + self.salon.getThirdRoom().getAverageSpentTime()) / 3)
        self.allAverageWorkTime = self.allAverageWorkTime + averageSpentTime
        completedRequests = self.salon.getFirstRoom().getCompletedRequests() + self.salon.getSecondRoom().getCompletedRequests() + self.salon.getThirdRoom().getCompletedRequests()
        self.allCompletedRequests = self.allCompletedRequests + completedRequests
        profit = int(self.salon.getFirstRoom().getProfit() + self.salon.getSecondRoom().getProfit() + self.salon.getThirdRoom().getProfit())
        self.allProfit = self.allProfit + profit
        freeTime = (self.oneDay - averageSpentTime) * 100 / self.oneDay
        self.allFreeTime = self.allFreeTime + freeTime
        self.salon.updateDataForNextDay()
        return Statistic(self.numberOfDay - 1, completedRequests, lostRequests, profit, averageSalary, averageSpentTime, freeTime)


    def generateRequest(self,currentTime):
        numberTask = random.randint(1,3)
        firstService = False
        secondService = False
        thirdService = False
        if numberTask < 2:
            firstService = True
        elif numberTask < 3:
            secondService = True
        else:
            thirdService = True
        #метод takeRequest
        self.salon.receiveRequest(Request(firstService, secondService, thirdService, currentTime))

        timeUntilNextRequest = 0
        if (self.numberOfDay > 4 or self.timePerOneDay > 300):
            timeUntilNextRequest = random.randint(int(self.timeRequestPeriod[0]),int(self.timeRequestPeriod[1]))
        else:
            timeUntilNextRequest = random.randint(int(self.timeRequestPeriod[0])+10,int(self.timeRequestPeriod[1])+10)

        return timeUntilNextRequest


    def getCountRequestDay(self):
        return self.countRequestDay

    def getTimePerOneDay(self):
        return self.timePerOneDay

    def getNumberOfDay(self):
        return self.numberOfDay

    def getSalon(self):
        return self.salon

    def getAllLostRequests(self):
        return self.allLostRequests

    def getAllAverageSalary(self):
        return self.allAverageSalary

    def getAllAverageWorkTime(self):
        return self.allAverageWorkTime

    def getAllCompletedRequests(self):
        return self.allCompletedRequests

    def getAllProfit(self):
        return self.allProfit

    def getAllFreeTime(self):
        return self.allFreeTime


