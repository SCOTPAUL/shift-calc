#!/usr/bin/python

from Tkinter import *
import canvasFunctions
import datetime
import pickle
import ttk
import tooltip

today = datetime.date.today()

currentYear = today.year
currentMonth = today.month
currentDay = today.day
HOLIDAYS = []


def resetHOLIDAYS():
    #Resets the HOLIDAYS variable to [] and updates file

    global HOLIDAYS
    HOLIDAYS = []
    fileHandler = open("./holidays.pck", "wb")
    pickle.dump(HOLIDAYS, fileHandler)
    fileHandler.close()
   
 
def readHOLIDAYS(filename):
    #Reads in data for HOLIDAYS using pickle

    try:
        fileHandler = open(filename, "rb")
    except:
        resetHOLIDAYS()
        fileHandler = open(filename, "rb")
        
    HOLIDAYS = pickle.load(fileHandler)
    fileHandler.close()
    return HOLIDAYS


def newHol(can, w, h, year, month, today):
    #Opens window for adding new holidays to HOLIDAYS variable

    global HOLIDAYS
    
    #Create a new window
    newHoltop = Toplevel()
    newHoltop.title("Add new holiday")

    #Title label
    title = Label(newHoltop, text = "Title:")
    title.grid(row = 0, sticky = "W")
    
    #Title entry box
    tString = StringVar()
    tEntry = Entry(newHoltop, textvariable = tString)
    tEntry.grid(row = 0, column = 2)
    
    #Start date label
    start = Label(newHoltop, text = "Start Date:")
    start.grid(row = 1, sticky = "W")
    
    #Start date entry box
    sString = StringVar()
    sEntry = Entry(newHoltop, textvariable = sString)
    sEntry.insert(0, "dd/mm/yyyy")
    sEntry.grid(row = 1, column = 2)
    
    #End date label
    end = Label(newHoltop, text = "End Date:")
    end.grid(row = 2, sticky = "W")
    
    #End date entry box
    eString = StringVar()
    eEntry = Entry(newHoltop, textvariable = eString)
    eEntry.insert(0, "dd/mm/yyyy")
    eEntry.grid(row = 2, column = 2)

    #Colour label
    coloursLabel = Label(newHoltop, text = "Colour:")
    coloursLabel.grid(row = 3, sticky = "W")
    
    #Colour ttk combobox
    allowedColours = ["red", "green", "blue", "orange", "yellow", "purple"]
    allowedColours.sort()
    colourSelect = ttk.Combobox(newHoltop, values = allowedColours, width = 19)
    colourSelect.set("Choose a colour...")
    colourSelect.grid(row = 3, column = 2, sticky = "E")


    def getStartEnd():
        #When holiday submitted, gets date, colour, title values and adds to
        #HOLLIDAYS variable

        global HOLIDAYS
        
        s = sString.get()
        e = eString.get()
        t = tString.get()
        c = colourSelect.get()

        if c in allowedColours:
            try:
                s = [int(i) for i in s.split("/")]
                e = [int(i) for i in e.split("/")]
                HOLIDAYS += [[datetime.date(s[2], s[1], s[0]), datetime.date(e[2],e[1],e[0]), t, c]]

                #Refresh canvas
                canvasFunctions.init(can, w, h, year, month, today, HOLIDAYS)

                #Destroy popup window
                newHoltop.destroy()
            except:
                pass


    submit = Button(newHoltop, text = "Submit", command = getStartEnd)
    submit.grid(column = 0, columnspan = 3)


def main():
    #Main body of program, creates canvas and graphical elements

    global monthInt
    global yearInt
    monthInt = currentMonth - 1
    yearInt = currentYear

    months = (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
               "Nov", "Dec"])
    numDays = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


    #Init root window
    root = Tk()
    root.title("Shift Calculator")
    root.resizable(0,0)               #Prevents window from being resized 
    

    #Toolbar   
    
    toolbar = Frame(root)

    #Add holiday button calls newHol with args to refresh window
    addHoliday = Button(toolbar, text = "Add Holiday", command = lambda: newHol(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today))
    addHoliday.grid()
    tooltip.createToolTip(addHoliday, "Adds a new holiday to the calendar")
    
    #Reset button clears HOLIDAYS, resets to current date
    resetHolidays = Button(toolbar, text = "Reset Holidays", command = lambda: [resetHOLIDAYS(), changeCurrentDate()] )
    resetHolidays.grid(row = 0, column = 1)
    tooltip.createToolTip(resetHolidays, "Resets all of the user set holidays")
    
    toolbar.grid(row = 0, sticky = "W")
    
    
    #Date Label
    monthLabel = Label(root, text = months[monthInt]+ " " + str(yearInt))
    monthLabel.grid()
    
    
    #Keybind fns

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
        canvasFunctions.init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today, HOLIDAYS)
            
            
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
        canvasFunctions.init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today, HOLIDAYS)
                
            
    def changeCurrentDate(*args):
        #When spacebar is pressed, draws the calendar at the current month
        
        global yearInt
        global monthInt
        
        yearInt = currentYear
        monthInt = currentMonth - 1
    
        monthLabel.configure(text = months[monthInt] + " " + str(yearInt))
        canvasFunctions.init(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today, HOLIDAYS)
            

    root.bind("<Right>", changeMonth)
    root.bind("<Left>", changeMonth)
    root.bind("<Up>", changeYear)
    root.bind("<Down>", changeYear)
    root.bind("<space>", changeCurrentDate)

    #Canvas

    CANWIDTH = 600
    CANHEIGHT = 500

    win = Canvas(root, width = CANWIDTH, height = CANHEIGHT)
    win.grid(ipadx = 10, ipady = 10)  #Places canvas on screen
    
    
    #Instructions on bottom of screen
    
    instructions = Frame(root)
    instruct = Message(instructions, text = ("Controls: Press Left and Right to change month, Up and Down to"
                                             "change year, and spacebar to return to the current date"), width = 500)                                 
    instruct.grid(columnspan = 3)
    instructions.grid(sticky = "WE", columnspan = 3)

    
    #Draw first month
    canvasFunctions.init(win, CANWIDTH, CANHEIGHT, currentYear, currentMonth, today, HOLIDAYS)
    
    def quitMain():
        #When program closed, writes HOLIDAYS to holidays.pck
        fileHandler = open("holidays.pck", "wb")
        pickle.dump(HOLIDAYS, fileHandler)
        fileHandler.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", quitMain)  #Calls quitMain when closing root window

    root.mainloop()

############

HOLIDAYS = readHOLIDAYS("holidays.pck")
main()
