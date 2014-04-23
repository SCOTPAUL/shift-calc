#!usr/bin/python

from Tkinter import *
import datetime
import calendar

today = datetime.date.today()

currentYear = today.year
currentMonth = today.month
currentDay = today.day

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
            if day != currentDay or month != currentMonth or year != currentYear:
                if day != 0:
                    can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
                    can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))
                else:
                    can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "gray")
            else:
                can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "cyan3")
                can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))
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
    
    monthLabel = Label(root, text = months[monthInt]+ " " + str(yearInt))
    monthLabel.grid(row = 0)

    def changeMonth(e):
        global monthInt
        global yearInt
        
        if e.keysym == "Right":
            if monthInt <= 10:
                monthInt += 1
                monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
                init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
            else:
                yearInt += 1
                monthInt = 0
                monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
                init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
                
        elif e.keysym == "Left":
            if monthInt > 0:
                monthInt -= 1
                monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
                init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
            elif yearInt > 1970:
                yearInt -= 1
                monthInt = 11
                monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
                init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
            
            
    def changeYear(e):
        global yearInt
        
        if e.keysym == "Up":
            yearInt += 1
            monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
            init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
        elif e.keysym == "Down":
            if yearInt > 1970:
                yearInt -=1
                monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
                init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
                
            
    def changeCurrentDate(*args):
        global yearInt
        global monthInt
        
        yearInt = currentYear
        monthInt = currentMonth - 1
    
        monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
        init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
            

    root.bind("<Right>", changeMonth)
    root.bind("<Left>", changeMonth)
    root.bind("<Up>", changeYear)
    root.bind("<Down>", changeYear)
    root.bind("<space>", changeCurrentDate)

    CANWIDTH = 500
    CANHEIGHT = 500

    win = Canvas(root, width = CANWIDTH, height = CANHEIGHT)
    win.grid(row = 1, ipadx = 10, ipady = 10)  #Places canvas on screen
    
    instruct = [Label(root, text = "Press the Left and Right arrow keys to change month, or Up and Down to change year"),
                Label(root, text = "Spacebar will return you to the current date")]
                                   
    instruct[0].grid(row = 2)
    instruct[1].grid(row = 3)

    
    init(win, CANWIDTH, CANHEIGHT, currentYear, currentMonth)

    root.mainloop()


main()
