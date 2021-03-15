import PySimpleGUI as sg
import os
import pathlib
from PIL import Image
from random import randint as rand
from model import Model
from statistics import Statistic

time = str()
requests = int()
lengthQueue1 = int()
lengthQueue2 = int()
lengthQueue3 = int()

data = [['Пн',0,0,0,0,0],
        ['Вт',0,0,0,0,0],
        ['Ср',0,0,0,0,0],
        ['Чт',0,0,0,0,0],
        ['Пт',0,0,0,0,0],
        ['Сб',0,0,0,0,0],
        ['Вс',0,0,0,0,0],
        ['Неделя',0,0,0,0,0]]
header_list = ['День недели','Обслужено', 'Ушли', 'Ср время(м)', 'Средняя з/п(р)', 'Простой(%)']


sg.theme('NeutralBlue')


layout = [

    [
        sg.Table(values=data,
                        headings=header_list,
                        auto_size_columns=True,
                        justification='center',
                        num_rows=min(len(data), 20),
                        alternating_row_color='lightblue',
                        row_colors=((0, 'red'), (2, 'yellow'), (4,'green'),(6,'purple')),
                        #display_row_numbers=True,
                        key='table'),
        sg.Graph(
            canvas_size=(600, 260),
            graph_bottom_left=(5, 340),
            graph_top_right=(605, 600),
            key="salon"
        )
    ],
    [
        sg.Text("Параметры",font=5)
    ],
    [
        sg.Text("Количество мастеров в зале 1:"),
        sg.InputCombo(['2','3', '4','5'], size=(3, 3),key="mas1"),
        sg.Button("   Начать   ",button_color=("white","green"),pad=(30,5)),


 #       скопившиеся очереди, занятость
#мастеров, появление новых и уход обслуженных клиентов.


    ],
    [
        sg.Text("Количество мастеров в зале 2:"),
        sg.InputCombo(['2','3', '4','5'], size=(3, 3),key="mas2"),
        sg.Button("     Шаг      ",button_color=("white","blue"),pad=(30,5))
    ],
    [
        sg.Text("Количество мастеров в зале 3:"),
        sg.InputCombo(['2','3', '4','5'], size=(3, 3),key="mas3"),
        sg.Button("Завершить",button_color=("white","red"),pad=(30,5))
    ],
    [
        sg.Text("Шаг моделирования:"),
        sg.InputCombo(['15 минут', '30 минут'], size=(8, 3),key="step")
    ],
    [
        sg.Text("Диапазон появления клиентов:")
    ],
    [
        sg.Text("пример: 10..20"),
        sg.InputText(key="seg_client",size=(15,3))
    ],
    [
        sg.Text("Диапазон среднего выполнения заявки:"),
    ],
    [
        sg.Text("пример: 10..20"),
        sg.InputText(key="seg_request",size=(15,3)),
    ]


]

\

window = sg.Window("Парикмахерский салон", layout)
window.Finalize()

salon = window.Element("salon")


#parametrs = window.Element("parametrs")
#statistics = window.Element("statistics")
queues = list()
#draw salon
salon.DrawRectangle((5, 600), (200, 350), line_color="black")
salon.DrawText("Зал 1",location=(100,580),font=5)
queue1 = salon.DrawText("Очередь: 0",location=(100,550),font=5)
salon.DrawRectangle((205, 600), (400, 350), line_color="black")
salon.DrawText("Зал 2",location=(300,580),font=5)
queue2 = salon.DrawText("Очередь: 0",location=(300,550),font=5)
salon.DrawRectangle((405, 600), (600, 350), line_color="black")
salon.DrawText("Зал 3",location=(500,580),font=5)
queue3 = salon.DrawText("Очередь: 0",location=(500,550),font=5)
queues.append(queue1)
queues.append(queue2)
queues.append(queue3)

def print_curr_info(time,requests,lengthQueue1,lengthQueue2,lengthQueue3):
    salon.TKCanvas.delete(queues[0])
    text1 = "Очередь: " + str(lengthQueue1)
    queue1 = salon.DrawText(text1,location=(100,550),font=5)
    salon.TKCanvas.delete(queues[1])
    text2 = "Очередь: " + str(lengthQueue2)
    queue2 = salon.DrawText(text2,location=(300,550),font=5)
    salon.TKCanvas.delete(queues[2])
    text3 = "Очередь: " + str(lengthQueue3)
    queue3 = salon.DrawText(text3,location=(500,550),font=5)
    queues.clear()
    queues.append(queue1)
    queues.append(queue2)
    queues.append(queue3)
#parametrs.DrawRectangle((5, 295), (300, 10), line_color="black")
#parametrs.DrawText("Параметры",location=(80,270),font=5)
#statistics.DrawRectangle((315, 295), (605, 10), line_color="black")
#statistics.DrawText("Статистика",location=(380,270),font=5)



def drawMasters(amount,param,masterHall):

    count = amount
    if count !=0:
        #circle = graph.DrawCircle((75,75), 25, fill_color='black',line_color='white')
        circle1 = salon.DrawCircle((35+200*param,520),
                                        radius=15,
                                        fill_color="green",
                                        )
        count = count-1
        masterHall.append(circle1)
    if count !=0:
        circle2 =salon.DrawCircle((170+200*param,520),radius=15,fill_color="green")
        count = count-1
        masterHall.append(circle2)
    if count !=0:
        circle3 = salon.DrawCircle((35+200*param,450),radius=15,fill_color="green")
        count = count-1
        masterHall.append(circle3)
    if count !=0:
        circle4 = salon.DrawCircle((170+200*param,450),radius=15,fill_color="green")
        count = count-1
        masterHall.append(circle4)
    if count !=0:
        circle5 = salon.DrawCircle((100+200*param,380),radius=15,fill_color="green")
        count = count-1
        masterHall.append(circle5)
    return masterHall
def addStatistic(day, completedRequests, lostRequests, profit, averageSalary, averageSpentTime, freeTime):


    data[day-1] = [day,completedRequests,lostRequests,averageSpentTime,averageSalary,freeTime]
    window.FindElement("table").Update(data)
    print(day,completedRequests,lostRequests,averageSpentTime,averageSalary,freeTime)


    #sg.Table

def changeColorsOfCircles():
        currentTime = model.getTimePerOneDay()
        masters = model.getSaloon().getFirstHall().getMasters()
        for i in range(0,len(masters)):
            if (masters[i].getReadyTakeRequest() <= currentTime):
                salon.TKCanvas.itemconfig(mastersHall1[i], fill = "green")
            else:
                salon.TKCanvas.itemconfig(mastersHall1[i], fill = "red")
        masters = model.getSaloon().getSecondHall().getMasters()
        for i in range(0,len(masters)):
            if (masters[i].getReadyTakeRequest() <= currentTime):
                salon.TKCanvas.itemconfig(mastersHall2[i], fill = "green")
            else:
                salon.TKCanvas.itemconfig(mastersHall2[i], fill = "red")
        masters = model.getSaloon().getThirdHall().getMasters()
        for i in range(0,len(masters)):
            if (masters[i].getReadyTakeRequest() <= currentTime):
                salon.TKCanvas.itemconfig(mastersHall3[i], fill = "green")
            else:
                salon.TKCanvas.itemconfig(mastersHall3[i], fill = "red")


def nextStep():
        ret = model.nextStep()
        stat = None
        if (ret != None):
            stat = ret
        time = str(model.getNumberOfDay()) + " д. " + str(model.getTimePerOneDay() / 60) + " ч. " + str(model.getTimePerOneDay() % 60) + " мин "
        requests = str(model.getCurrentAmountOfRequestPerDay())
        lengthQueue1 = str(model.getSaloon().getFirstHall().getQueueSize())
        lengthQueue2 = str(model.getSaloon().getSecondHall().getQueueSize())
        lengthQueue3 = str(model.getSaloon().getThirdHall().getQueueSize())
        changeColorsOfCircles()
        print_curr_info(time,requests,lengthQueue1,lengthQueue2,lengthQueue3)


        if (stat != None):
            day = stat.getNumberOfDay() + 1
            completedRequests = stat.getCompletedRequests()
            lostRequests = str(stat.getLostRequests())
            profit = str(stat.getProfit()) + "руб. "
            averageSalary = str(stat.getAverageSalary()) + "руб."
            averageSpentTime = str(stat.getAverageWorkingTime()) + "мин"
            freeTime = str(stat.getFreeTime()) + "%"
            addStatistic(day, completedRequests, lostRequests, profit, averageSalary, averageSpentTime, freeTime)

        if (model.getNumberOfDay() == PERIOD_OF_SIMULATION):
            #buttonNextStep.setDisable(true)
            #buttonFinish.setDisable(true);
            day = PERIOD_OF_SIMULATION + 1
            completedRequests = str(model.getTotalCompletedRequests())
            lostRequests = str(model.getTotalLostRequests())
            profit = str(model.getTotalProfit()) + "руб. "
            averageSalary = str(model.getTotalAverageSalary()) + "руб."
            averageSpentTime = str(model.getTotalAverageSpentTime()) + "мин"
            freeTime = str(model.getTotalFreeTime() / 7) + "%"
            addStatistic(day, completedRequests, lostRequests, profit, averageSalary, averageSpentTime, freeTime)

PERIOD_OF_SIMULATION = 7
mastersHall1 = list()
mastersHall2 = list()
mastersHall3 = list()

while True:

    event, values = window.Read()
    print(event,values)
    #window.FindElement('Шаг').Update(disabled=True)
    #window.FindElement('Завершить').Update(disabled=True)

    if event == '   Начать   ':
        if (values['mas1'] == '' or values['mas2'] == '' or values['mas3'] == '' or
            values['seg_client'] == '' or values['seg_request'] == ''):
            sg.popup("Заполните все поля!")
            continue
        #window.FindElement('Начать').Update(disabled=True)
        #window.FindElement('Завершить').Update(disabled=False)
        amountroom1 = int(str(values['mas1']))
        amountroom2 = int(str(values['mas2']))
        amountroom3 = int(str(values['mas3']))
        timeSteps = str(values['step'])
        model = Model(amountroom1,amountroom2,amountroom3,timeSteps)
        drawMasters(amountroom1,0,mastersHall1)
        drawMasters(amountroom2,1,mastersHall2)
        drawMasters(amountroom3,2,mastersHall3)


        #buttonNextStep.setStyle("-fx-background-color: rgba(96,51,211,0.72); -fx-textfill: #000000;");
        #currentInformation.add(buttonNextStep, 0, 7);
        #buttonFinish = new Button("Завершить");
        #buttonFinish.setOnAction(event -> {
        #    while (model.getNumberOfDay() != PERIOD_OF_SIMULATION) {
        #        nextStep();
        #    }
        #});
    if event == '     Шаг      ':
        nextStep()
        print("Шаг")

    if event == 'Завершить':
        #стереть круги
        while (model.getNumberOfDay() != PERIOD_OF_SIMULATION):
                nextStep()

        print('Завершить')
        #window.FindElement('Начать').Update(disabled=False)
        #window.FindElement('Завершить').Update(disabled=True)
    if event is None:
        break

