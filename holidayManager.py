from Tkinter import Toplevel, Label, StringVar, Entry, Button, Frame
import datetime
import ttk
from icalendar import Calendar, Event


class Holiday:
    """
    Representation of a time in the calendar where the shift patterns don't apply
    """

    def __init__(self, name, start, end, color):
        self.name = name
        self.start = start
        self.end = end
        self.color = color

    def get_ical_event(self, index):
        """
        :param index The unique id of the event
        :returns An iCalendar VEVENT representing the holiday
        """
        event = Event()
        event.add('summary', self.name)
        event.add('uid', index)
        event.add('dtstart', self.start)
        event.add('dtend', self.end)
        event.add('color', self.color)
        return event

    @classmethod
    def event_from_ical(cls, ical_event):
        """
        :param ical_event An iCalendar formatted event as a string
        :returns A Holiday instance representing the ical_event
        """

        name = ical_event.decoded('summary')
        start = ical_event.decoded('dtstart')
        end = ical_event.decoded('dtend')

        try:
            color = ical_event.decoded('color')
        except KeyError:
            # TODO: Set a default colour
            color = 'blue'

        return cls(name=name, color=color, start=start, end=end)


class HolidayManager:
    """
    Manages the holidays associated with the calendar
    """

    def __init__(self, filename, app):
        self.app = app
        self.holidays = []
        self.filename = filename
        self.read_ical()

    def add_holiday(self, start, end, title, colour):
        self.holidays.append(Holiday(start=start, end=end, name=title, color=colour))

    def get_holiday(self, day, month, year):
        """
        :return: Holiday if parameters occur during it, else returns None
        """
        current_date = datetime.date(year, month, day)
        for holiday in self.holidays:
            if holiday.start <= current_date <= holiday.end:
                return holiday

        return None

    def reset(self):
        """
        Resets and updates the holidays file
        """
        self.holidays = []
        self.write_ical()

        if self.app.calendar:
            self.app.update_calendar()

    def read_ical(self):
        """
        Reads in data for holidays in iCalendar format
        """
        completed = False

        while not completed:
            try:
                with open(self.filename, 'rb') as f:
                    ical_str = f.read()
                    cal = Calendar.from_ical(ical_str)
                    for component in cal.walk():
                        if component.name == "VEVENT":
                            holiday = Holiday.event_from_ical(component)
                            self.holidays.append(holiday)
                completed = True
            except IOError:
                self.reset()

    def write_ical(self):
        """
        Writes out the holidays to a file in the iCalendar format
        """
        cal = Calendar()

        cal.add('prodid', '-//shift-calc//mxm.dk//')
        cal.add('version', '0.1')

        for index, holiday in enumerate(self.holidays):
            event = holiday.get_ical_event(index)
            cal.add_component(event)

        with open(self.filename, 'wb') as f:
            f.write(cal.to_ical())

    def add_holiday_gui(self, date=None):
        """
        Opens window for adding new holidays to the holiday file
        :param date: If provided, the start/end date fields are prepopulated with this date, else with dd/mm/yyyy
        placeholders
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

        if date is not None:
            s_entry.insert(0, str(date.day) + "/" + str(date.month) + "/" + str(date.year))
        else:
            s_entry.insert(0, "dd/mm/yyyy")
        s_entry.grid(row=1, column=2)

        # End date label
        end = Label(new_hol_top, text="End Date:")
        end.grid(row=2, sticky="W")

        # End date entry box
        e_string = StringVar()
        e_entry = Entry(new_hol_top, textvariable=e_string)

        if date is not None:
            e_entry.insert(0, str(date.day) + "/" + str(date.month) + "/" + str(date.year))
        else:
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
