from Tkinter import Canvas, Label
import datetime
import calendar


class ShiftBox:
    def __init__(self, shift_calendar, box_num):
        self.shift_calendar = shift_calendar
        self.canvas = self.shift_calendar.canvas
        self.box_num = box_num

        self.dims = self._calculate_box_dims()
        self.text_dims = (
            self.dims[0] + 0.2 * self.shift_calendar.box_width, self.dims[1] + 0.2 * self.shift_calendar.box_height)

        self.rect = self.canvas.create_rectangle(self.dims)
        self.text = self.canvas.create_text(self.text_dims, text="")

    def draw_active(self, day):
        today = datetime.date.today().day
        if day == today:
            self.draw_today(day)
        else:
            self._draw("white", str(day))

    def draw_inactive(self):
        self._draw("gray")

    def draw_today(self, day):
        self._draw("cyan3", str(day))

    def _draw(self, color, text=None):
        self.canvas.itemconfig(self.rect, fill=color)

        if text is not None:
            self.canvas.itemconfig(self.text, text=text)
        else:
            self.canvas.itemconfig(self.text, text="")

    def _calculate_box_dims(self):
        x1 = 10 + (self.box_num % self.shift_calendar.columns) * self.shift_calendar.box_width
        y1 = 10 + (self.box_num / self.shift_calendar.columns) * self.shift_calendar.box_height
        x2 = x1 + self.shift_calendar.box_width
        y2 = y1 + self.shift_calendar.box_height
        return x1, y1, x2, y2


class ShiftCalendar:
    months = (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
               "Nov", "Dec"])

    def __init__(self, root, width, height):
        self.root = root
        today = datetime.date.today()

        self.month_label = Label(root, text=self.months[today.month] + " " + str(today.year))
        self.month_label.grid()

        win = Canvas(root, width=width, height=height)
        win.grid(ipadx=10, ipady=10)  # Places canvas on screen

        self.canvas = win

        self.calendar = calendar.Calendar()

        self.rows = 6
        self.columns = 7

        self.box_width = width / self.columns
        self.box_height = height / self.rows

        self.week_days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

        self.boxes = self._generate_boxes(self.rows * self.columns)

        self.draw_month(today.month, today.year)

    def _generate_boxes(self, num):
        boxes = []
        for i in range(num):
            boxes.append(ShiftBox(self, i))

        return boxes

    def _update_month_label(self, month, year):
        self.month_label.config(text=self.months[month - 1] + " " + str(year))

    def draw_month(self, month, year):
        month_dates = self.calendar.monthdayscalendar(year, month)
        self._update_month_label(month, year)

        box_counter = 0
        for week in month_dates:
            for day in week:
                box = self.boxes[box_counter]
                if day != 0:
                    box.draw_active(day)
                else:
                    box.draw_inactive()

                box_counter += 1

        while box_counter < self.rows * self.columns:
            box = self.boxes[box_counter]
            box.draw_inactive()
            box_counter += 1
