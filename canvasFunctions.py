from Tkinter import *
import datetime
import calendar


def init(can, w, h, year, month, today, HOLIDAYS):
    #Given a canvas, draws the calendar including dates
    currentYear = today.year
    currentMonth = today.month
    currentDay = today.day
    
    can.delete(ALL)
    
    cal = calendar.Calendar()
    monthDates = cal.monthdayscalendar(year, month)
    
    rows = 7.0
    columns = 7.0
    
    
    boxWidth = w/columns
    boxHeight = h/rows

    posX = 10
    posY = 10
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    
    drawWeekDays(can, posX, posY, boxWidth, boxHeight, days)
   
   
    for week in monthDates:
        posX = 10
        posY += boxHeight
        for day in week:
            isCurrentDay = False

            if day != 0:
                drawDay(can, posX, posY, boxWidth, boxHeight, day)
            else:
                drawDayNotInMonth(can, posX, posY, boxWidth, boxHeight)
            
            if day == currentDay and month == currentMonth and year == currentYear:
                isCurrentDay = True

            anyHoliday = False
            for holiday in HOLIDAYS:
                isHoliday = False

                try:
                    myDate = datetime.date(year, month, day)

                    if myDate >= holiday[0] and myDate <= holiday[1]:
                        isHoliday = True
                        anyHoliday = True

                        if isCurrentDay:
                            drawCurrentDay(can, posX, posY, boxWidth, boxHeight, day)
                        else:
                            can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = holiday[3])
                            can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))

                        can.create_text(posX + 0.5*boxWidth, posY + 0.5*boxHeight, text = holiday[2])

                except:
                    continue

            if not anyHoliday and isCurrentDay:
                drawCurrentDay(can, posX, posY, boxWidth, boxHeight, day)


            
                    
            posX += boxWidth
    
    if len(monthDates) == 5:
        posY += boxHeight
        posX = 10
        for day in range(7):
            drawDayNotInMonth(can, posX, posY, boxWidth, boxHeight)
            posX += boxWidth


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
