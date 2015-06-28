from Tkinter import Toplevel, Label, StringVar, Entry, Button, Frame
import pickle
import datetime
import ttk


class HolidayManager:
    """
    Manages the holidays associated with the calendar
    """
    def __init__(self, filename, app):
        self.app = app
        self.holidays = []
        self.filename = filename
        self.read()

    def add_holiday(self, start, end, title, colour):
        self.holidays.append([start, end, title, colour])

    def get_holiday(self, day, month, year):
        """
        :returns Holiday if parameters occur during it, else returns None
        """
        current_date = datetime.date(year, month, day)
        for holiday in self.holidays:
            if holiday[0] <= current_date <= holiday[1]:
                return holiday

        return None

    def reset(self):
        """
        Resets and updates the holidays file
        """
        self.holidays = []
        self.write()

    def read(self):
        """
        Reads in data for holidays using pickle
        """
        try:
            file_handler = open(self.filename, "rb")
        except IOError:
            self.reset()
            file_handler = open(self.filename, "rb")

        holidays = pickle.load(file_handler)
        file_handler.close()

        self.holidays = holidays

    def write(self):
        """
        Writes out the holidays to a file
        """
        file_handler = open(self.filename, "wb")
        pickle.dump(self.holidays, file_handler)
        file_handler.close()

    def add_holiday_gui(self):
        """
        Opens window for adding new holidays to the holiday file
        :param app: The main application class
        """

        # Create a new window
        new_hol_top = Toplevel()
        new_hol_top.title("Add new holiday")
        new_hol_top.resizable(0, 0)

        # Title label
        title = Label(new_hol_top, text="Title:")
        title.grid(row=0, sticky="W")

        # Title entry box
        t_string = StringVar()
        t_entry = Entry(new_hol_top, textvariable=t_string)
        t_entry.grid(row=0, column=2)

        # Start date label
        start = Label(new_hol_top, text="Start Date:")
        start.grid(row=1, sticky="W")

        # Start date entry box
        s_string = StringVar()
        s_entry = Entry(new_hol_top, textvariable=s_string)
        s_entry.insert(0, "dd/mm/yyyy")
        s_entry.grid(row=1, column=2)

        # End date label
        end = Label(new_hol_top, text="End Date:")
        end.grid(row=2, sticky="W")

        # End date entry box
        e_string = StringVar()
        e_entry = Entry(new_hol_top, textvariable=e_string)
        e_entry.insert(0, "dd/mm/yyyy")
        e_entry.grid(row=2, column=2)

        # Colour label
        colours_label = Label(new_hol_top, text="Colour:")
        colours_label.grid(row=3, sticky="W")

        # Colour ttk combobox
        allowed_colours = ["red", "green", "blue", "orange", "yellow", "purple"]
        allowed_colours.sort()
        colour_select = ttk.Combobox(new_hol_top, values=allowed_colours, width=19)
        colour_select.set("Choose a colour...")
        colour_select.grid(row=3, column=2, sticky="E")

        def get_start_end():
            # When holiday submitted, gets date, colour, title values and adds to
            # holidays variable

            s = s_string.get()
            e = e_string.get()
            t = t_string.get()
            c = colour_select.get()

            if c in allowed_colours:
                try:
                    s = [int(i) for i in s.split("/")]
                    e = [int(i) for i in e.split("/")]
                    self.add_holiday(datetime.date(s[2], s[1], s[0]), datetime.date(e[2], e[1], e[0]), t, c)

                    # Refresh canvas
                    self.app.update_calendar()

                    # Destroy popup window
                    new_hol_top.destroy()
                except:
                    pass

        submit = Button(new_hol_top, text="Submit", command=get_start_end)
        submit.grid(column=0, columnspan=3)

    def reset_holidays_gui(self):
        confirm_top = Toplevel()
        confirm_top.title("Are you sure you wish to continue?")
        confirm_top.resizable(0, 0)

        # Warning to user
        warning_label = Label(confirm_top,
                              text="WARNING: This will remove all holidays from the application\nAre you sure you wish to continue?")
        warning_label.grid()

        buttons = Frame(confirm_top)

        ok_button = Button(buttons, text="OK", command=lambda: [self.reset(), confirm_top.destroy()])
        ok_button.grid(row=0, column=1)

        cancel_button = Button(buttons, text="Cancel", command=confirm_top.destroy)
        cancel_button.grid(row=0, column=0)

        buttons.grid(row=1)
