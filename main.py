#!/usr/bin/python

from Tkinter import *
import holidayManager
import shiftCalendar
import datetime
import pickle
import ttk
import tooltip

today = datetime.date.today()

currentYear = today.year
currentMonth = today.month
currentDay = today.day
holiday_manager = holidayManager.HolidayManager("./holidays.pck")

# Init root window
root = Tk()
root.title("Shift Calculator")
root.resizable(0, 0)  # Prevents window from being resized

can_width = 600
can_height = 500
calendar = shiftCalendar.ShiftCalendar(root, can_width, can_height)

monthInt = currentMonth - 1
yearInt = currentYear


def reset_holidays_gui():
    confirm_top = Toplevel()
    confirm_top.title("Are you sure you wish to continue?")
    confirm_top.resizable(0, 0)

    # Warning to user
    warning_label = Label(confirm_top,
                          text="WARNING: This will remove all holidays from the application\nAre you sure you wish to continue?")
    warning_label.grid()

    buttons = Frame(confirm_top)

    ok_button = Button(buttons, text="OK", command=lambda: [holiday_manager.reset(), confirm_top.destroy()])
    ok_button.grid(row=0, column=1)

    cancel_button = Button(buttons, text="Cancel", command=confirm_top.destroy)
    cancel_button.grid(row=0, column=0)

    buttons.grid(row=1)


def about_info():
    # Opens window for information about application

    infoTop = Toplevel()
    infoTop.title("About")
    infoTop.resizable(0, 0)

    strtText = Label(infoTop, text="About the application")
    strtText.grid()

    devText = Label(infoTop, text="Developer: Paul Cowie")
    devText.grid()

    dateText = Label(infoTop, text=u"\u00a9 Paul Cowie 2014")
    dateText.grid()

    submit = Button(infoTop, text="Ok", command=infoTop.destroy)
    submit.grid(column=0, columnspan=3)


def goto_date():
    dateTop = Toplevel()
    dateTop.title("Enter date")
    dateTop.resizable(0, 0)

    # Inputs for month/year
    gotoMonth = Label(dateTop, text="Month:")
    gotoMonth.grid(row=0, column=0)

    mEntry = Entry(dateTop)
    mEntry.grid(row=0, column=1)

    gotoYear = Label(dateTop, text="Year:")
    gotoYear.grid(row=1, column=0)

    yEntry = Entry(dateTop)
    yEntry.grid(row=1, column=1)

    def monthJump():

        global yearInt
        global monthInt

        try:
            month = int(mEntry.get())
            year = int(yEntry.get())

            if 0 < month <= 12 and 1970 <= year < 5000:
                monthInt = month - 1
                yearInt = year
                calendar.draw_month(monthInt + 1, yearInt)
        except:
            pass

    submit = Button(dateTop, text="Submit", command=monthJump)
    submit.grid(column=0, columnspan=3)


# def newHol(shift_calendar):
# # Opens window for adding new holidays to HOLIDAYS variable
#
# global HOLIDAYS
#
#     # Create a new window
#     newHoltop = Toplevel()
#     newHoltop.title("Add new holiday")
#     newHoltop.resizable(0, 0)
#
#     # Title label
#     title = Label(newHoltop, text="Title:")
#     title.grid(row=0, sticky="W")
#
#     #Title entry box
#     tString = StringVar()
#     tEntry = Entry(newHoltop, textvariable=tString)
#     tEntry.grid(row=0, column=2)
#
#     #Start date label
#     start = Label(newHoltop, text="Start Date:")
#     start.grid(row=1, sticky="W")
#
#     #Start date entry box
#     sString = StringVar()
#     sEntry = Entry(newHoltop, textvariable=sString)
#     sEntry.insert(0, "dd/mm/yyyy")
#     sEntry.grid(row=1, column=2)
#
#     #End date label
#     end = Label(newHoltop, text="End Date:")
#     end.grid(row=2, sticky="W")
#
#     #End date entry box
#     eString = StringVar()
#     eEntry = Entry(newHoltop, textvariable=eString)
#     eEntry.insert(0, "dd/mm/yyyy")
#     eEntry.grid(row=2, column=2)
#
#     #Colour label
#     coloursLabel = Label(newHoltop, text="Colour:")
#     coloursLabel.grid(row=3, sticky="W")
#
#     #Colour ttk combobox
#     allowedColours = ["red", "green", "blue", "orange", "yellow", "purple"]
#     allowedColours.sort()
#     colourSelect = ttk.Combobox(newHoltop, values=allowedColours, width=19)
#     colourSelect.set("Choose a colour...")
#     colourSelect.grid(row=3, column=2, sticky="E")
#
#     def get_start_end():
#         # When holiday submitted, gets date, colour, title values and adds to
#         # HOLIDAYS variable
#
#         global HOLIDAYS
#
#         s = sString.get()
#         e = eString.get()
#         t = tString.get()
#         c = colourSelect.get()
#
#         if c in allowedColours:
#             try:
#                 s = [int(i) for i in s.split("/")]
#                 e = [int(i) for i in e.split("/")]
#                 HOLIDAYS += [[datetime.date(s[2], s[1], s[0]), datetime.date(e[2], e[1], e[0]), t, c]]
#
#                 #Refresh canvas
#                 canvasFunctions.init(can, w, h, year, month, today, HOLIDAYS)
#
#                 #Destroy popup window
#                 newHoltop.destroy()
#             except:
#                 pass
#
#
#     submit = Button(newHoltop, text="Submit", command=getStartEnd)
#     submit.grid(column=0, columnspan=3)


def main():
    # Main body of program, creates canvas and graphical elements

    # Keybind fns

    def change_month(e):
        # Changes the month/year variable when R or L keys are pressed
        # Then draws new calendar for that month

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

        calendar.draw_month(monthInt + 1, yearInt)

    def change_year(e):
        # Changes the year variable when U or D keys pressed
        # Then draws the calendar for that month
        global yearInt

        if e.keysym == "Up":
            yearInt += 1

        elif e.keysym == "Down":
            if yearInt > 1970:
                yearInt -= 1

        calendar.draw_month(monthInt + 1, yearInt)

    def change_current_date(*args):
        # When spacebar is pressed, draws the calendar at the current month

        global yearInt
        global monthInt

        yearInt = currentYear
        monthInt = currentMonth - 1

        calendar.draw_month(monthInt + 1, yearInt)

    root.bind("<Right>", change_month)
    root.bind("<Left>", change_month)
    root.bind("<Up>", change_year)
    root.bind("<Down>", change_year)
    root.bind("<space>", change_current_date)

    # Instructions on bottom of screen
    instructions = Frame(root)
    instruct = Message(instructions, text=("Controls: Press Left and Right to change month, Up and Down to "
                                           "change year, and spacebar to return to the current date"), width=500)
    instruct.grid(columnspan=3)
    instructions.grid(sticky="WE", columnspan=3)

    def quit_main():
        # When program closed, writes holidays
        holiday_manager.write()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", quit_main)  # Calls quit_main when closing root window

    root.mainloop()

############

# Menu
menubar = Menu(root, relief=FLAT)


# Contains standard calendar functions
fileMenu = Menu(menubar, tearoff=0)
# fileMenu.add_command(label="Add holiday",
#                     command=lambda: newHol(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today))
fileMenu.add_command(label="Reset holidays", command=reset_holidays_gui)
fileMenu.add_command(label="Goto month",
                     command=goto_date)
menubar.add_cascade(label="File", menu=fileMenu)

# Contains about option, giving application information
helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label="About", command=about_info)
menubar.add_cascade(label="Help", menu=helpMenu)

# Display on screen
root.config(menu=menubar)


# Toolbar
toolbar = Frame(root)

# Add holiday button calls newHol with args to refresh window
# addHoliday = Button(toolbar, text="Add Holiday",
#                    command=lambda: newHol(win, CANWIDTH, CANHEIGHT, yearInt, monthInt + 1, today))
# addHoliday.grid()
# tooltip.createToolTip(addHoliday, "Adds a new holiday to the calendar")

# Reset button clears holidays, resets to current date
resetHolidays = Button(toolbar, text="Reset Holidays", command=reset_holidays_gui)
resetHolidays.grid(row=0, column=1)
tooltip.createToolTip(resetHolidays, "Resets all of the user set holidays")

# Goto month button opens window to jump to a date
goto_month_button = Button(toolbar, text="Goto month", command=goto_date)
goto_month_button.grid(row=0, column=2)
tooltip.createToolTip(goto_month_button, "Jump to a specific month")

toolbar.grid(row=0, sticky="W")

main()
