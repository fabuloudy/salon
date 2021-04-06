import PySimpleGUI as sg
import os
import pathlib
from random import randint as rand
from model import Model
import re

if __name__ == "__main__":

    time = str()
    requests = int()
    lengthQueue1 = int()
    lengthQueue2 = int()
    lengthQueue3 = int()
    PERIOD_OF_SIMULATION = 7
    mastersRoom1 = list()
    mastersRoom2 = list()
    mastersRoom3 = list()

    # Drawing window

    data = [['Пн', 0, 0, 0, 0, 0],
            ['Вт', 0, 0, 0, 0, 0],
            ['Ср', 0, 0, 0, 0, 0],
            ['Чт', 0, 0, 0, 0, 0],
            ['Пт', 0, 0, 0, 0, 0],
            ['Сб', 0, 0, 0, 0, 0],
            ['Вс', 0, 0, 0, 0, 0],
            ['Неделя', 0, 0, 0, 0, 0]]

    header_list = ['День недели', 'Обслужено', 'Ушли',
                   'Ср время(м)', 'Средняя з/п(р)', 'Простой(%)']

    sg.theme('NeutralBlue')

    layout = [

        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=True,
                  justification='center',
                  num_rows=min(len(data), 20),
                  alternating_row_color='lightblue',
                  row_colors=((0, 'red'), (2, 'yellow'),
                              (4, 'green'), (6, 'purple')),
                  # display_row_numbers=True,
                  key='table'),
         sg.Graph(
            canvas_size=(600, 260),
            graph_bottom_left=(5, 340),
            graph_top_right=(605, 600),
            key="salon"
        )],

        [sg.Text("Время от начала: ", font=5),
            sg.Text("                        ", key='time'), ],

        [sg.Text("Количество мастеров в зале 1:"),
            sg.InputCombo(['2', '3', '4', '5'], size=(
                3, 3), key="mas1", default_value='2'),
            sg.Button("   Начать   ", button_color=(
                "white", "green"), pad=(30, 5)), ],

        [sg.Text("Количество мастеров в зале 2:"),
         sg.InputCombo(['2', '3', '4', '5'], size=(3, 3),
                       key="mas2", default_value='3'),
         sg.Button("     Шаг      ", button_color=("white", "blue"), pad=(30, 5))],

        [sg.Text("Количество мастеров в зале 3:"),
         sg.InputCombo(['2', '3', '4', '5'], size=(3, 3),
                       key="mas3", default_value='4'),
         sg.Button("Завершить", button_color=("white", "red"), pad=(30, 5))],

        [sg.Text("Шаг моделирования:"),
         sg.InputCombo(['15 минут', '30 минут', '1 час'],
                       size=(8, 3), key="step", default_value='1 час')],
        [sg.Text("Диапазон появления клиентов:")],

        [sg.Text("пример: 10..20 (мин.)"),
         sg.InputText(key="seg_client", size=(15, 3), default_text='10..20')],

        [sg.Text("Диапазон выполнения заявки:"), ],

        [sg.Text("пример: 10..20 (мин.)"),
         sg.InputText(key="seg_request", size=(15, 3), default_text='60..120'), ]
    ]

    window = sg.Window("Парикмахерский салон", layout)
    window.Finalize()

    salon = window.Element("salon")
    queues = list()
    salon.DrawRectangle((5, 600), (200, 350),
                        line_color="black", fill_color='white')
    salon.DrawText("Зал 1", location=(100, 580), font=5)
    queue1 = salon.DrawText("Очередь: 0/5", location=(100, 550), font=5)
    salon.DrawRectangle((205, 600), (400, 350),
                        line_color="black", fill_color='white')
    salon.DrawText("Зал 2", location=(300, 580), font=5)
    queue2 = salon.DrawText("Очередь: 0/5", location=(300, 550), font=5)
    salon.DrawRectangle((405, 600), (600, 350),
                        line_color="black", fill_color='white')
    salon.DrawText("Зал 3", location=(500, 580), font=5)
    queue3 = salon.DrawText("Очередь: 0/5", location=(500, 550), font=5)
    queues.append(queue1)
    queues.append(queue2)
    queues.append(queue3)

    def print_curr_info(time, requests, lengthQueue1, lengthQueue2, lengthQueue3):
        'print queue information'

        salon.TKCanvas.delete(queues[0])
        text1 = "Очередь: " + str(lengthQueue1) + "/5"
        queue1 = salon.DrawText(text1, location=(100, 550), font=5)
        salon.TKCanvas.delete(queues[1])
        text2 = "Очередь: " + str(lengthQueue2) + "/5"
        queue2 = salon.DrawText(text2, location=(300, 550), font=5)
        salon.TKCanvas.delete(queues[2])
        text3 = "Очередь: " + str(lengthQueue3) + "/5"
        queue3 = salon.DrawText(text3, location=(500, 550), font=5)
        queues.clear()
        queues.append(queue1)
        queues.append(queue2)
        queues.append(queue3)

    def drawMasters(amount, param, masterRoom):
        'drawing masters at the begging of modeling'

        count = amount
        if count != 0:
            circle1 = salon.DrawCircle((35+200*param, 520),
                                       radius=15,
                                       fill_color="green",
                                       )
            count = count-1
            masterRoom.append(circle1)
        if count != 0:
            circle2 = salon.DrawCircle(
                (170+200*param, 520), radius=15, fill_color="green")
            count = count-1
            masterRoom.append(circle2)
        if count != 0:
            circle3 = salon.DrawCircle(
                (35+200*param, 450), radius=15, fill_color="green")
            count = count-1
            masterRoom.append(circle3)
        if count != 0:
            circle4 = salon.DrawCircle(
                (170+200*param, 450), radius=15, fill_color="green")
            count = count-1
            masterRoom.append(circle4)
        if count != 0:
            circle5 = salon.DrawCircle(
                (100+200*param, 380), radius=15, fill_color="green")
            count = count-1
            masterRoom.append(circle5)
        return masterRoom

    def name_day(day):
        if day == 1:
            return 'Пн'
        if day == 2:
            return 'Вт'
        if day == 3:
            return 'Ср'
        if day == 4:
            return 'Чт'
        if day == 5:
            return 'Пт'
        if day == 6:
            return 'Cб'
        if day == 7:
            return 'Вс'
        else:
            return 'Неделя'

    def addStatistic(day, completedRequests, lostRequests,
                     profit, averageSalary, averageSpentTime, freeTime):
        'display statistic'

        data[day-1] = [name_day(day), completedRequests, lostRequests,
                       averageSpentTime, averageSalary, freeTime]
        window.FindElement("table").Update(data, row_colors=(
            (0, 'red'), (2, 'yellow'), (4, 'green'), (6, 'purple')))

    def changeColorsOfCircles():
        'changing colors for busy and free masters'
        currentTime = model.timePerOneDay
        masters = model.salon.house['1'].masters
        for i in range(0, len(masters)):
            if (masters[i].readyTakeRequest <= currentTime):
                salon.TKCanvas.itemconfig(mastersRoom1[i], fill="green")
            else:
                salon.TKCanvas.itemconfig(mastersRoom1[i], fill="red")
        masters = model.salon.house['2'].masters
        for i in range(0, len(masters)):
            if (masters[i].readyTakeRequest <= currentTime):
                salon.TKCanvas.itemconfig(mastersRoom2[i], fill="green")
            else:
                salon.TKCanvas.itemconfig(mastersRoom2[i], fill="red")
        masters = model.salon.house['3'].masters
        for i in range(0, len(masters)):
            if (masters[i].readyTakeRequest <= currentTime):
                salon.TKCanvas.itemconfig(mastersRoom3[i], fill="green")
            else:
                salon.TKCanvas.itemconfig(mastersRoom3[i], fill="red")

    def print_time_request(time, request):
        'print current time'

        window.FindElement('time').Update(time)

    def nextStep():
        'doing step of modeling and checking actual statistic'
        ret = model.nextStep()
        stat = None
        if (ret is not None):
            stat = ret
        time = str(model.numberOfDay) + " д. " + \
            str(model.timePerOneDay // 60) + " ч. " + \
            str(model.timePerOneDay % 60) + " мин "
        requests = str(model.countRequestDay)
        lengthQueue1 = str(model.salon.house['1'].getQueueSize())
        lengthQueue2 = str(model.salon.house['2'].getQueueSize())
        lengthQueue3 = str(model.salon.house['3'].getQueueSize())
        changeColorsOfCircles()
        print_curr_info(time, requests, lengthQueue1,
                        lengthQueue2, lengthQueue3)

        if (stat is not None):
            day = stat.numberOfDay + 1
            completedRequests = stat.completedRequests
            lostRequests = str(stat.lostRequests)
            profit = str(stat.profit) + "руб. "
            averageSalary = str(stat.averageSalary) + "руб."
            averageSpentTime = str(stat.averageWorkingTime) + "мин"
            free = int(stat.freeTime)
            if free < 0:
                freeTime = "0%"
            else:
                freeTime = str(free) + "%"
            addStatistic(day, completedRequests, lostRequests, profit,
                         averageSalary, averageSpentTime, freeTime)

        if (model.numberOfDay == PERIOD_OF_SIMULATION):
            day = PERIOD_OF_SIMULATION + 1
            completedRequests = str(model.allCompletedRequests)
            lostRequests = str(model.allLostRequests)
            profit = str(model.allProfit) + "руб. "
            averageSalary = str(model.allAverageSalary) + "руб."
            averageSpentTime = str(model.allAverageWorkTime) + "мин"
            free = int(model.allFreeTime / 7)
            if free < 0:
                freeTime = "0%"
            else:
                freeTime = str(free) + "%"
            addStatistic(day, completedRequests, lostRequests, profit,
                         averageSalary, averageSpentTime, freeTime)
        print_time_request(time, requests)

    def check_str(period):
        return re.match(r'\d{1,3}..\d{1,3}', period)

    def create_queues(salon, queues, data):
        data[:] = [['Пн', 0, 0, 0, 0, 0],
                   ['Вт', 0, 0, 0, 0, 0],
                   ['Ср', 0, 0, 0, 0, 0],
                   ['Чт', 0, 0, 0, 0, 0],
                   ['Пт', 0, 0, 0, 0, 0],
                   ['Сб', 0, 0, 0, 0, 0],
                   ['Вс', 0, 0, 0, 0, 0],
                   ['Неделя', 0, 0, 0, 0, 0]]
        window.FindElement("table").Update(data, row_colors=(
            (0, 'red'), (2, 'yellow'), (4, 'green'), (6, 'purple')))
        queues[:] = list()
        salon.DrawRectangle((5, 600), (200, 350),
                            line_color="black", fill_color='white')
        salon.DrawText("Зал 1", location=(100, 580), font=5)
        queue1 = salon.DrawText("Очередь: 0/5", location=(100, 550), font=5)
        salon.DrawRectangle((205, 600), (400, 350),
                            line_color="black", fill_color='white')
        salon.DrawText("Зал 2", location=(300, 580), font=5)
        queue2 = salon.DrawText("Очередь: 0/5", location=(300, 550), font=5)
        salon.DrawRectangle((405, 600), (600, 350),
                            line_color="black", fill_color='white')
        salon.DrawText("Зал 3", location=(500, 580), font=5)
        queue3 = salon.DrawText("Очередь: 0/5", location=(500, 550), font=5)
        queues.append(queue1)
        queues.append(queue2)
        queues.append(queue3)

    while True:

        event, values = window.Read()

        if event == '   Начать   ':
            if (values['mas1'] == '' or values['mas2'] == '' or values['mas3'] == '' or
                    values['seg_client'] == '' or values['seg_request'] == ''):
                sg.popup("Заполните все поля!")
                continue
            reqPeriod = str(values['seg_client'])
            taskPeriod = str(values['seg_request'])
            if check_str(reqPeriod) is None:
                sg.popup(
                    "Некорректное заполнение поля 'Диапазон появления клиентов'!")
                continue
            if check_str(taskPeriod) is None:
                sg.popup(
                    "Некорректное заполнение поля 'Диапазон среднего выполнения заявки'!")
                continue
            create_queues(salon, queues, data)

            window.FindElement('     Шаг      ').Update(disabled=False)
            window.FindElement('   Начать   ').Update(disabled=True)
            amountroom1 = int(str(values['mas1']))
            amountroom2 = int(str(values['mas2']))
            amountroom3 = int(str(values['mas3']))

            timeSteps = str(values['step'])
            model = Model(amountroom1, amountroom2, amountroom3,
                          timeSteps, reqPeriod, taskPeriod)
            drawMasters(amountroom1, 0, mastersRoom1)
            drawMasters(amountroom2, 1, mastersRoom2)
            drawMasters(amountroom3, 2, mastersRoom3)

        if event == '     Шаг      ':
            if model.numberOfDay != PERIOD_OF_SIMULATION:
                nextStep()
            else:
                window.FindElement('     Шаг      ').Update(disabled=True)

        if event == 'Завершить':

            while (model.numberOfDay != PERIOD_OF_SIMULATION):
                nextStep()
            for mas in mastersRoom1:
                salon.TKCanvas.delete(mas)
            for mas in mastersRoom2:
                salon.TKCanvas.delete(mas)
            for mas in mastersRoom3:
                salon.TKCanvas.delete(mas)
            mastersRoom1.clear()
            mastersRoom2.clear()
            mastersRoom3.clear()
            window.FindElement('   Начать   ').Update(disabled=False)

        if event is None:
            break
