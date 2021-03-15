from salon import Salon
from statistics import Statistic
from request import Request
import random
class Model:
    ONE_WORK_DAY = 480
    #interval = values['step]
    def __init__(self,firstRoomAmount, secondRoomAmount, thirdRoomAmount,interval):
        self.salon = Salon(firstRoomAmount, secondRoomAmount, thirdRoomAmount)
        self.timeInterval = self.takeTimeInterval(interval) #шаг моделирования
        self.timePerOneDay = 0 #время работы салона в день
        self.numberOfDay = 0 #номер дня
        self.currentTimePerStep = 0 #время в шаге
        self.currentAmountOfRequestPerDay = 0 #количество заявок в день
        self.totalLostRequests = 0 #количество ушедних клиентов за все дни
        self.totalAverageSalary = 0 #средняя зарплата за все дни
        self.totalAverageSpentTime = 0 #среднее время работы за все дни
        self.totalCompletedRequests = 0 #количество обслуженных клиентов за все дни
        self.totalProfit = 0 #доход салона за все дни
        self.totalFreeTime = 0 #свободное время мастеров за все дни

    def takeTimeInterval(self,interval):
        switcher={
            "15мин": 15,
            "30мин": 30
        }
        return switcher.get(interval,15)
#метод возращает статистику
    def nextStep(self):
        while (self.currentTimePerStep < self.timeInterval):
            self.salon.giveRequestMasters(self.currentTimePerStep + self.timePerOneDay)
            self.currentTimePerStep = self.currentTimePerStep + self.generateRequest(self.currentTimePerStep + self.timePerOneDay)
            self.currentAmountOfRequestPerDay = self.currentAmountOfRequestPerDay + 1
        self.timePerOneDay = self.timePerOneDay + self.timeInterval
        self.salon.giveRequestMasters(self.timePerOneDay)
        if (self.timePerOneDay == self.ONE_WORK_DAY):
            self.numberOfDay = self.numberOfDay + 1
            self.timePerOneDay = 0
            self.currentTimePerStep = 0
            return self.collectStatistics()
        else:
            self.currentTimePerStep = self.currentTimePerStep - self.timeInterval
        return None
#метод возвращает статистику
    def collectStatistics(self):
        lostRequests = self.salon.getFirstHall().getWentAway() + self.salon.getSecondHall().getWentAway() + self.salon.getThirdHall().getWentAway()
        self.totalLostRequests = self.totalLostRequests + lostRequests
        averageSalary = int((self.salon.getFirstHall().getAverageSalary() + self.salon.getSecondHall().getAverageSalary() + self.salon.getThirdHall().getAverageSalary()) / 3)
        self.totalAverageSalary += averageSalary
        averageSpentTime = int((self.salon.getFirstHall().getAverageSpentTime() + self.salon.getSecondHall().getAverageSpentTime() + self.salon.getThirdHall().getAverageSpentTime()) / 3)
        self.totalAverageSpentTime = self.totalAverageSpentTime + averageSpentTime
        completedRequests = self.salon.getFirstHall().getCompletedRequests() + self.salon.getSecondHall().getCompletedRequests() + self.salon.getThirdHall().getCompletedRequests()
        self.totalCompletedRequests = self.totalCompletedRequests + completedRequests
        profit = int(self.salon.getFirstHall().getProfit() + self.salon.getSecondHall().getProfit() + self.salon.getThirdHall().getProfit())
        self.totalProfit = self.totalProfit + profit
        freeTime = (self.ONE_WORK_DAY - averageSpentTime) * 100 / self.ONE_WORK_DAY
        self.totalFreeTime = self.totalFreeTime + freeTime
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
        minNext = random.random()
        #диапазон получения заявки
        if (self.numberOfDay > 4 or self.timePerOneDay > 300):
            timeUntilNextRequest = int(minNext * 10)
        else:
            timeUntilNextRequest = int(minNext * 20)
        
        return timeUntilNextRequest
    

    def getCurrentAmountOfRequestPerDay(self):
        return self.currentAmountOfRequestPerDay

    def getTimePerOneDay(self):
        return self.timePerOneDay

    def getNumberOfDay(self):
        return self.numberOfDay

    def getSaloon(self):
        return self.salon

    def getTotalLostRequests(self):
        return self.totalLostRequests

    def getTotalAverageSalary(self):
        return self.totalAverageSalary

    def getTotalAverageSpentTime(self):
        return self.totalAverageSpentTime

    def getTotalCompletedRequests(self):
        return self.totalCompletedRequests

    def getTotalProfit(self):
        return self.totalProfit

    def getTotalFreeTime(self):
        return self.totalFreeTime
    

