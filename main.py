#!usr/bin/python

from Tkinter import *
import datetime
import calendar
import pickle

today = datetime.date.today()

currentYear = today.year
currentMonth = today.month
currentDay = today.day
HOLIDAYS = []

def resetHOLIDAYS():
    global HOLIDAYS
    HOLIDAYS = []
    fileHandler = open("./holidays.pck", "wb")
    pickle.dump(HOLIDAYS, fileHandler)
    fileHandler.close()
    

def readHOLIDAYS(filename):
    fileHandler = open(filename, "rb")
    HOLIDAYS = pickle.load(fileHandler)
    fileHandler.close()
    return HOLIDAYS
    
    
def daysInMonth(monthDates):
    days = 0
    for week in monthDates:
        for day in week:
            if day != 0:
                days += 1
    
    return days
                

def init(can, w, h, year, month):
    #Given a canvas, draws the calendar including dates
    
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
            
            
            for holiday in HOLIDAYS:
                try:
                    myDate = datetime.date(year, month, day)
                    if myDate >= holiday[0] and myDate <= holiday[1]:
                        can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "green")
                        can.create_text(posX + 0.2*boxWidth, posY + 0.2*boxHeight, text = str(day))
                except:
                    continue
                    
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
    
    
    
    
    
    
    #################Toolbar
    
    
    def newHol():
        global HOLIDAYS
        
        newHoltop = Toplevel()
        newHoltop.title("Add new holiday")
        
        start = Label(newHoltop, text = "Start Date:")
        start.grid(row = 0)
        
        sString = StringVar()
        sEntry = Entry(newHoltop, textvariable = sString)
        sEntry.insert(0, "dd/mm/yyyy")
        sEntry.grid(row = 0, column = 2)
        
        end = Label(newHoltop, text = "End Date:")
        end.grid(row = 1)
        
        eString = StringVar()
        eEntry = Entry(newHoltop, textvariable = eString)
        eEntry.insert(0, "dd/mm/yyyy")
        eEntry.grid(row = 1, column = 2)
        
        def getStartEnd():
            global HOLIDAYS
            
            s = sString.get()
            e = eString.get()
            
            try:
                s = [int(i) for i in s.split("/")]
                e = [int(i) for i in e.split("/")]
                HOLIDAYS += [[datetime.date(s[2], s[1], s[0]), datetime.date(e[2],e[1],e[0])]]
                newHoltop.destroy()
            except:
                pass
            
         
        submit = Button(newHoltop, text = "Submit", command = getStartEnd)
        submit.grid(column = 0, columnspan = 3)
        
        
    
    toolbar = Frame(root)
    addHoliday = Button(toolbar, text = "Add Holiday", command = newHol)
    addHoliday.grid()
    
    resetHolidays = Button(toolbar, text = "Reset Holidays", command = resetHOLIDAYS)
    resetHolidays.grid(row = 0, column = 1)
    
    toolbar.grid(row = 0, sticky = "W")
    
    

    global monthInt
    global yearInt
    monthInt = currentMonth - 1
    yearInt = currentYear
    
    #############Date Label
    
    monthLabel = Label(root, text = months[monthInt]+ " " + str(yearInt))
    monthLabel.grid()
    
    
    
    #############Canvas fns

    def changeMonth(e):
        #Changes the month/year variable when R or L keys are pressed
        #Then draws new calendar for that month
        
        global monthInt
        global yearInt
        
        if e.keysym == "Right":
            if monthInt <= 10:
                monthInt += 1
            else:
                yearInt += 1
                monthInt = 0
        elif e.keysym == "Left":
            if monthInt > 0:
                monthInt -= 1
            elif yearInt > 1970:
                yearInt -= 1
                monthInt = 11
        
        monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
        init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
            
            
    def changeYear(e):
        #Changes the year variable when U or D keys pressed
        #Then draws the calendar for that month
        global yearInt
        
        if e.keysym == "Up":
            yearInt += 1
            
        elif e.keysym == "Down":
            if yearInt > 1970:
                yearInt -=1
        
        monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
        init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1)
                
            
    def changeCurrentDate(*args):
        #When spacebar is pressed, draws the calendar at the current month
        
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

    CANWIDTH = 600
    CANHEIGHT = 500

    win = Canvas(root, width = CANWIDTH, height = CANHEIGHT)
    win.grid(ipadx = 10, ipady = 10)  #Places canvas on screen
    
    
    
    
    #########Instructions on bottom of screen
    
    instructions = Frame(root)
    
    instruct = Message(instructions, text = "Controls: Press Left and Right to change month, Up and Down to change year, and spacebar to return to the current date", width = 500)
                                   
    instruct.grid(columnspan = 3)
    
    instructions.grid(sticky = "WE", columnspan = 3)
    
    
    #############Draw first month
    
    init(win, CANWIDTH, CANHEIGHT, currentYear, currentMonth)
    
    def quitMain():
        fileHandler = open("./holidays.pck", "wb")
        pickle.dump(HOLIDAYS, fileHandler)
        fileHandler.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", quitMain)

    root.mainloop()

HOLIDAYS = readHOLIDAYS("holidays.pck")
main()
