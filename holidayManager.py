import pickle


class HolidayManager:
    def __init__(self, filename):
        self.holidays = []
        self.filename = filename
        self.read()

    def reset(self):
        # Resets the HOLIDAYS variable to [] and updates file
        self.holidays = []
        file_handler = open(self.filename, "wb")
        pickle.dump(self.holidays, file_handler)
        file_handler.close()

    def read(self):
        # Reads in data for holidays using pickle
        try:
            file_handler = open(self.filename, "rb")
        except:
            self.reset()
            file_handler = open(self.filename, "rb")

        holidays = pickle.load(file_handler)
        file_handler.close()

        self.holidays = holidays

    def write(self):
        file_handler = open(self.filename, "wb")
        pickle.dump(self.holidays, file_handler)
        file_handler.close()
