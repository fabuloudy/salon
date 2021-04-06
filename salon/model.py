from salon import Salon
import random
import re
from collections import namedtuple

Statistic = namedtuple('Statistic', ['numberOfDay', 'completedRequests',
                               'lostRequests', 'profit', 'averageSalary',
                               'averageWorkingTime', 'freeTime'])

Request = namedtuple('Request', ['numberProcedure', 'arrivedTime'])

class Model:
    'class for generation requests, running salon and returning statistics'

    DURATION_OF_DAY = 480 # длительность одного дня в минутах

    def __init__(self, firstRoomAmount, secondRoomAmount, thirdRoomAmount,
                 interval, requestPeriod, taskPeriod):

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

    def takeTimeInterval(self, interval):
        switcher = {
            "15 минут": 15,
            "30 минут": 30,
            "1 час": 60
        }
        return switcher.get(interval, 15)

    def takePeriod(self, str_period):
        period = re.findall(r'\d{1,3}', str_period)
        return period

    def nextStep(self):
        while (self.timeStep < self.timeInterval):
            self.salon.giveRequestMasters(self.timeStep + self.timePerOneDay,
                                          self.timeTaskPeriod)
            self.timeStep = self.timeStep + \
                self.generateRequest(self.timeStep +
                                     self.timePerOneDay)
            self.countRequestDay = self.countRequestDay + 1
        self.timePerOneDay = self.timePerOneDay + self.timeInterval
        self.salon.giveRequestMasters(self.timePerOneDay, self.timeTaskPeriod)
        if (self.timePerOneDay == self.DURATION_OF_DAY):
            self.numberOfDay = self.numberOfDay + 1
            self.timePerOneDay = 0
            self.timeStep = 0
            return self.collectStatistics()
        else:
            self.timeStep = self.timeStep - self.timeInterval
        return None

    def collectStatistics(self):
        lostRequests = 0
        averageSalary = 0
        averageSpentTime = 0
        completedRequests = 0
        profit = 0
        for key,_ in self.salon.house.items():
            lostRequests = lostRequests + self.salon.house[key].wentAway
            averageSalary = averageSalary + int(self.salon.house[key].getAverageSalary())
            averageSpentTime = averageSpentTime + int(self.salon.house[key].getAverageSpentTime())
            completedRequests = completedRequests + int(self.salon.house[key].completedRequests)
            profit =  profit + int(self.salon.house[key].getProfit())
        self.allLostRequests = self.allLostRequests + lostRequests
        averageSalary = int(averageSalary / 3)
        averageSpentTime =  int(averageSpentTime / 3)
        self.allAverageSalary += averageSalary
        self.allAverageWorkTime = self.allAverageWorkTime + averageSpentTime
        self.allCompletedRequests = self.allCompletedRequests + completedRequests
        self.allProfit = self.allProfit + profit

        freeTime = (self.DURATION_OF_DAY - averageSpentTime) * 100 / self.DURATION_OF_DAY

        self.allFreeTime = self.allFreeTime + freeTime
        self.salon.updateDataForNextDay()
        return Statistic(self.numberOfDay - 1, completedRequests,
                         lostRequests, profit, averageSalary,
                         averageSpentTime, freeTime)

    def generateRequest(self, currentTime):
        numberTask = random.randint(1, 3)
        # метод takeRequest
        self.salon.receiveRequest(
            Request(numberTask, currentTime))

        timeUntilNextRequest = 0
        if (self.numberOfDay > 4 or self.timePerOneDay > 300):
            timeUntilNextRequest = random.randint(
                int(self.timeRequestPeriod[0]), int(self.timeRequestPeriod[1]))
        else:
            timeUntilNextRequest = random.randint(
                int(self.timeRequestPeriod[0])+10,
                int(self.timeRequestPeriod[1])+10)

        return timeUntilNextRequest
