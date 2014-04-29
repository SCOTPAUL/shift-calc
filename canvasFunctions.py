from Tkinter import *

def drawWeekDays(can, posX, posY, boxWidth, boxHeight, days):
    for weekday in range(7):
        can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
        can.create_text(posX + 0.5*boxWidth, posY + 0.5*boxHeight, text = days[weekday])
        posX += boxWidth


def drawDay(can, posX, posY, boxWidth, boxHeight, day):
    can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
    can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))


def drawCurrentDay(can, posX, posY, boxWidth, boxHeight, day):
    can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "cyan3")
    can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))


def drawDayNotInMonth(can, posX, posY, boxWidth, boxHeight):
    can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "gray")
