from Tkconstants import DISABLED
from Tkinter import Canvas, Label
import datetime
import calendar


class ShiftBox:
    """
    Represents a single box on a calendar
    """

    def __init__(self, shift_calendar, box_num):
        self.shift_calendar = shift_calendar
        self.canvas = self.shift_calendar.canvas
        self.box_num = box_num

        self.dims = self.__calculate_box_dims()
        self.text_dims = (
            self.dims[0] + 0.2 * self.shift_calendar.box_width, self.dims[1] + 0.2 * self.shift_calendar.box_height)
        self.title_dims = (
            self.dims[0] + 0.5 * self.shift_calendar.box_width, self.dims[1] + 0.5 * self.shift_calendar.box_height)

        self.rect = self.canvas.create_rectangle(self.dims)
        self.text = self.canvas.create_text(self.text_dims, text="", state=DISABLED)
        self.title = self.canvas.create_text(self.title_dims, text="", state=DISABLED)

        self.canvas.tag_bind(self.rect, "<Button-1>", func=self.click_handler)

    def draw_active(self, day, month, year):
        """
        Draws a day of the month in the box. If the day is today, it draws in a different colour
        :param day: Day of the month
        :param month: Month of the year
        :param year: Year
        """
        today = datetime.date.today()
        holiday = self.shift_calendar.holiday_manager.get_holiday(day, month, year)
        if holiday is not None:
            self.draw_holiday(day, holiday[2], holiday[3])
        elif day == today.day and month == today.month and year == today.year:
            self.draw_today(day)
        else:
            self.__draw("white", str(day))

    def draw_inactive(self):
        """
        Draws a day which is not in the month, acting as padding
        """
        self.__draw("gray")

    def draw_today(self, day):
        """
        Applies a special colour to indicate the current date
        :param day: The current day of the month
        """
        self.__draw("cyan3", str(day))

    def draw_holiday(self, day, title, color):
        self.__draw(color, day, title)

    def __draw(self, color, text="", title=""):
        self.canvas.itemconfig(self.rect, fill=color)
        self.canvas.itemconfig(self.text, text=text)
        self.canvas.itemconfig(self.title, text=title)

    def __calculate_box_dims(self):
        x1 = 10 + (self.box_num % self.shift_calendar.columns) * self.shift_calendar.box_width
        y1 = 20 + (self.box_num / self.shift_calendar.columns) * self.shift_calendar.box_height
        x2 = x1 + self.shift_calendar.box_width
        y2 = y1 + self.shift_calendar.box_height
        return x1, y1, x2, y2

    def click_handler(self, event):
        if self.canvas.find_withtag(self.rect):
            self.canvas.itemconfig(self.rect, fill="blue")
            self.canvas.update_idletasks()
            self.canvas.after(200)
            self.canvas.itemconfig(self.rect, fill="red")


class ShiftCalendar:
    """
    Graphical representation of a calendar
    """
    months = (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
               "Nov", "Dec"])

    week_days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

    def __init__(self, root, width, height, holiday_manager):
        self.holiday_manager = holiday_manager
        self.root = root
        today = datetime.date.today()

        self.month_label = Label(root, text=self.months[today.month] + " " + str(today.year))
        self.month_label.grid(row=1)

        win = Canvas(root, width=width, height=height)
        win.grid(ipadx=10, ipady=10)  # Places canvas on screen

        self.canvas = win

        self.calendar = calendar.Calendar()

        self.rows = 6
        self.columns = 7

        self.box_width = width / self.columns
        self.box_height = height / self.rows

        self.boxes = self.__generate_boxes(self.rows * self.columns)

        self.__draw_weekday_names()
        self.draw_month(today.month, today.year)

    def __generate_boxes(self, num):
        boxes = []
        for i in range(num):
            boxes.append(ShiftBox(self, i))

        return boxes

    def __update_month_label(self, month, year):
        self.month_label.config(text=self.months[month - 1] + " " + str(year))

    def __draw_weekday_names(self):
        pos_x = 10
        pos_y = 10

        for day in self.week_days:
            self.canvas.create_text(pos_x + 0.5 * self.box_width, pos_y, text=day)
            pos_x += self.box_width

    def draw_month(self, month, year):
        month_dates = self.calendar.monthdayscalendar(year, month)
        self.__update_month_label(month, year)

        box_counter = 0
        for week in month_dates:
            for day in week:
                box = self.boxes[box_counter]
                if day != 0:
                    box.draw_active(day, month, year)
                else:
                    box.draw_inactive()

                box_counter += 1

        while box_counter < self.rows * self.columns:
            box = self.boxes[box_counter]
            box.draw_inactive()
            box_counter += 1
