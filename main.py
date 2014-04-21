#!usr/bin/python

from Tkinter import *
import datetime
import calendar

today = datetime.date.today()

currentYear = today.year
currentMonth = today.month

def daysInMonth(monthDates):
    days = 0
    for week in monthDates:
        for day in week:
            if day != 0:
                days += 1
    
    return days
                

def init(can, w, h, year, month):
    can.delete(ALL)
    
    cal = calendar.Calendar()
    monthDates = cal.monthdayscalendar(year, month)
    print daysInMonth(monthDates)
    
    rows = 7.0
    columns = 7.0
    
    
    boxWidth = w/columns
    boxHeight = h/rows

    posX = 10
    posY = 10
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    
    for weekday in range(7):
        can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
        can.create_text(posX + 0.5*boxWidth, posY + 0.5*boxHeight, text = days[weekday])
        posX += boxWidth
   
   
    for week in monthDates:
        posX = 10
        posY += boxHeight
        for day in week:
            if day != 0:
                can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
                can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))
            else:
                can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "gray")
            posX += boxWidth
    
    if len(monthDates) == 5:
        posY += boxHeight
        posX = 10
        for day in range(7):
            can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "gray")
            posX += boxWidth

    

def main():
    months = (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
               "Nov", "Dec"])
    numDays = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    
    root = Tk()

    root.title("Shift Calculator")
    root.resizable(0,0)               #Prevents window from being resized

    global monthInt
    global yearInt
    monthInt = currentMonth - 1
    yearInt = currentYear
    
    monthLabel = Label(root, text = months[monthInt]+ "\t" + str(yearInt))
    monthLabel.grid()

    def incMonth(*args):
        global monthInt
        global yearInt
        
        if monthInt <= 10:
            monthInt += 1
            monthLabel.configure(text = months[monthInt] + "\t" + str(yearInt))
            init(win, 400, 500, yearInt, monthInt + 1)
        else:
            yearInt += 1
            monthInt = 0
            monthLabel.configure(text = months[monthInt] + "\t" + str(yearInt))
            init(win, 400, 500, yearInt, monthInt + 1)
            
            
    def decMonth(*args):
        global monthInt
        global yearInt
        
        if monthInt > 0:
            monthInt -= 1
            monthLabel.configure(text = months[monthInt] + "\t" + str(yearInt))
            init(win, 400, 500, yearInt, monthInt + 1)
        else:
            yearInt -= 1
            monthInt = 11
            monthLabel.configure(text = months[monthInt] + "\t" + str(yearInt))
            init(win, 400, 500, yearInt, monthInt + 1)
            

    root.bind("<Right>", incMonth)
    root.bind("<Left>", decMonth)

    

    win = Canvas(root, width = 400, height = 500)
    win.grid(ipadx = 10, ipady = 10)  #Places canvas on screen

    
    init(win, 400, 500, currentYear, currentMonth)

    root.mainloop()


main()
