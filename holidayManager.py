import pickle
import datetime


class HolidayManager:
    """
    Manages the holidays associated with the calendar
    """
    def __init__(self, filename):
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
