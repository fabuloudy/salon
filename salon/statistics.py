class Statistic:
    def __init__(self,numberOfDay,completedRequests,lostRequests,profit,averageSalary,averageWorkingTime,freeTime):
        self.numberOfDay = numberOfDay
        self.completedRequests = completedRequests
        self.lostRequests = lostRequests
        self.profit = profit
        self.averageSalary = averageSalary
        self.averageWorkingTime = averageWorkingTime
        self.freeTime = freeTime
    

    def getNumberOfDay(self):
        return self.numberOfDay

    def getCompletedRequests(self):
        return self.completedRequests

    def getLostRequests(self):
        return self.lostRequests

    def getProfit(self):
        return self.profit

    def getAverageSalary(self):
        return self.averageSalary

    def getAverageWorkingTime(self):
        return self.averageWorkingTime

    def getFreeTime(self):
        return self.freeTime
    