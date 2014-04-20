#!usr/bin/python

from Tkinter import *


def init(can, w, h, numDays):
    rows = 6.0
    columns = 7.0
    
    
    boxWidth = w/columns
    boxHeight = h/rows

    posX = 10
    posY = 10
    monthDay = 1
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

    for week in range(int(rows)):
        posX = 10
        
        for day in range(int(columns)):
            
            can.create_rectangle(posX, posY, posX + boxWidth, posY + boxHeight, fill = "white")
            
            if week == 0:
                can.create_text(posX+(0.5*boxWidth), posY+(0.5*boxHeight), text = days[day])
                
            elif monthDay < numDays + 1:
                can.create_text(posX+(0.2*boxWidth), posY+(0.2*boxHeight), text = str(monthDay))
                monthDay += 1
                
            posX += boxWidth
            
        posY += boxHeight


def main():
    months = (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
               "Nov", "Dec"])
    numDays = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    
    root = Tk()

    root.title("Shift Calculator")
    root.resizable(0,0)               #Prevents window from being resized

    global monthInt
    monthInt = 0
    monthLabel = Label(root, text = months[monthInt])
    monthLabel.grid()

    def incMonth(*args):
        global monthInt
        if monthInt <= 10:
            monthInt += 1
            monthLabel.configure(text = months[monthInt])
            init(win, 400, 500, numDays[monthInt])
    def decMonth(*args):
        global monthInt
        if monthInt > 0:
            monthInt -= 1
            monthLabel.configure(text = months[monthInt])
            init(win, 400, 500, numDays[monthInt])

    root.bind("<Right>", incMonth)
    root.bind("<Left>", decMonth)

    

    win = Canvas(root, width = 400, height = 500)
    win.grid(ipadx = 10, ipady = 10)  #Places canvas on screen

    
    init(win, 400, 500, numDays[monthInt])

    root.mainloop()


main()
