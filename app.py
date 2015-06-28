from Tkconstants import FLAT
from Tkinter import Tk, Frame, Message, Menu, Button, Toplevel, Label, Entry
import datetime
import holidayManager
import shiftCalendar
import tooltip


class App:
    def __init__(self):
        today = datetime.date.today()
        self.holiday_manager = holidayManager.HolidayManager("./holidays.pck", self)

        self.month = today.month
        self.year = today.year

        self.__setup_calendar()
        self.__setup_instructions()
        self.__setup_menus()
        self.__setup_bindings()

    def __setup_menus(self):
        self.menu = Menu(self.root, relief=FLAT)
        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Add holiday",
                              command=self.holiday_manager.add_holiday_gui)

        file_menu.add_command(label="Reset holidays", command=self.holiday_manager.reset_holidays_gui)
        file_menu.add_command(label="Goto month", command=self.goto_date_gui)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Contains about option, giving application information
        help_menu = Menu(self.menu, tearoff=0)
        help_menu.add_command(label="About", command=self.about_info_gui)
        self.menu.add_cascade(label="Help", menu=help_menu)

        # Display on screen
        self.root.config(menu=self.menu)

        # Toolbar
        toolbar = Frame(self.root)

        # Add holiday button calls add_new_holiday with args to refresh window
        add_holiday = Button(toolbar, text="Add Holiday",
                             command=self.holiday_manager.add_holiday_gui)
        add_holiday.grid(row=0, column=0)
        tooltip.createToolTip(add_holiday, "Adds a new holiday to the calendar")

        # Reset button clears holidays, resets to current date
        reset_holidays = Button(toolbar, text="Reset Holidays", command=self.holiday_manager.reset_holidays_gui)
        reset_holidays.grid(row=0, column=1)
        tooltip.createToolTip(reset_holidays, "Resets all of the user set holidays")

        toolbar.grid(row=0, sticky="W")

    def __setup_instructions(self):
        # Instructions on bottom of screen
        self.instructions = Frame(self.root)
        instruct = Message(self.instructions, text=("Controls: Press Left and Right to change month, Up and Down to "
                                                    "change year, and spacebar to return to the current date"),
                           width=500)
        instruct.grid(columnspan=3)
        self.instructions.grid(sticky="WE", columnspan=3)

    def __setup_calendar(self):
        # Init root window
        self.root = Tk()
        self.root.title("Shift Calculator")
        self.root.resizable(0, 0)  # Prevents window from being resized

        can_width = 600
        can_height = 528
        self.calendar = shiftCalendar.ShiftCalendar(self.root, can_width, can_height, self.holiday_manager)

    def __setup_bindings(self):
        self.root.bind("<Right>", self.change_month)
        self.root.bind("<Left>", self.change_month)
        self.root.bind("<Up>", self.change_year)
        self.root.bind("<Down>", self.change_year)
        self.root.bind("<space>", self.change_to_current_date)

    def about_info_gui(self):
        """
        Opens window for information about application
        """
        info_top = Toplevel()
        info_top.title("About")
        info_top.resizable(0, 0)

        about = Label(info_top, text="About the application")
        about.grid()

        dev_text = Label(info_top, text="Developer: Paul Cowie")
        dev_text.grid()

        date_text = Label(info_top, text=u"\u00a9 Paul Cowie 2014")
        date_text.grid()

        submit = Button(info_top, text="Ok", command=info_top.destroy)
        submit.grid(column=0, columnspan=3)

    def goto_date_gui(self):
        date_top = Toplevel()
        date_top.title("Enter date")
        date_top.resizable(0, 0)

        # Inputs for month/year
        goto_month = Label(date_top, text="Month:")
        goto_month.grid(row=0, column=0)

        m_entry = Entry(date_top)
        m_entry.grid(row=0, column=1)

        goto_year = Label(date_top, text="Year:")
        goto_year.grid(row=1, column=0)

        y_entry = Entry(date_top)
        y_entry.grid(row=1, column=1)

        def month_jump():
            try:
                month = int(m_entry.get())
                year = int(y_entry.get())

                if 0 < month <= 12 and 1970 <= year < 5000:
                    self.month = month - 1
                    self.year = year
                    self.update_calendar()
            except:
                pass

        submit = Button(date_top, text="Submit", command=month_jump)
        submit.grid(column=0, columnspan=3)

    def change_month(self, event):
        """
        Changes the month/year variable when Right or Left keys are pressed, then draws new calendar for that month
        """
        if event.keysym == "Right":
            if self.month < 12:
                self.month += 1
            else:
                self.year += 1
                self.month = 1
        elif event.keysym == "Left":
            if self.month > 1:
                self.month -= 1
            elif self.year > 1970:
                self.year -= 1
                self.month = 12

        self.update_calendar()

    def change_year(self, event):
        """
        Changes the year variable when Up or Down keys pressed, then draws the calendar for that month
        """
        if event.keysym == "Up":
            self.year += 1

        elif event.keysym == "Down":
            if self.year > 1970:
                self.year -= 1

        self.update_calendar()

    def change_to_current_date(self, event):
        """
        Draws the calendar at the current month
        """
        today = datetime.date.today()

        self.year = today.year
        self.month = today.month

        self.update_calendar()

    def update_calendar(self):
        """
        Draws the calendar at self.month and self.year
        """
        self.calendar.draw_month(self.month, self.year)

    def start(self):
        """
        Starts the GUI
        """
        self.root.protocol("WM_DELETE_WINDOW", self.stop)  # Calls quit_main when closing root window
        self.root.mainloop()

    def stop(self):
        """
        Gracefully closes the graphical interface, writing holidays to file first
        """
        self.holiday_manager.write()
        self.root.destroy()
