import sys
import math
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import QTime, QTimer, Qt
import time

class BasicTamilTimeFormat:
    @staticmethod
    def format(year, month, month_day, week_day, hour, minute, second):
        time_str = f"{DateUtils.get_hour_prefix(hour)} {hour}:{minute:02d}:{second:02d}"
        date_str = f"{DateUtils.tamil_month(month)} {month_day}, {year} - {DateUtils.tamil_weekday(week_day)}"
        return f"{time_str}\n{date_str}"

class DateUtils:
    YEAR = u"ஆண்டு"
    WEEK = u"வாரம்"
    MONTH = u"மாதம்"
    DAY = u"நாள்"
    DAY_SUFFIX = u"கிழமை"
    MINUTE = u"நிமிடம்"
    HOUR = u"மணி"
    TIME = u"நேரம்"
    WEEKDAYS_INDEX = [u"monday", u"tuesday", u"wednesday", u"thursday", u"friday", u"saturday", u"sunday"]
    WEEKDAYS = {
        u"monday": u"திங்கள்",
        u"tuesday": u"செவ்வாய்",
        u"wednesday": u'புதன்',
        u"thursday": u'வியாழன்',
        u'friday': u'வெள்ளி',
        u'saturday': u'சனிக்கிழமை',
        u'sunday': u'ஞாயிறு',
    }
    MONTHS_INDEX = [None, u"January", u"February", u"March", u"April", u"May", u"June", u"July", u"August", u"September", u"October", u"November", u"December"]

    MONTHS = {
        u'January': u"தை", 
        u'February': u"மாசி",
        u'March': u"பங்குனி",
        u'April': u"சித்திரை",
        u'May': u"வைகாசி",
        u'June': u"ஆனி",
        u'July': u"ஆடி",
        u'August': u"ஆவணி",
        u'September': u"புரட்டாசி",
        u'October': u"ஐப்பசி",
        u'November': u"கார்த்திகை",
        u'December': u"மார்கழி"
    }

    @staticmethod
    def tamil_weekday(week_day):
        key = DateUtils.WEEKDAYS_INDEX[week_day]
        return DateUtils.WEEKDAYS[key]

    @staticmethod
    def tamil_month(month):
        key = DateUtils.MONTHS_INDEX[month]
        return DateUtils.MONTHS[key]
    
    @staticmethod
    def get_time(local_time=None):
        if not local_time:
            local_time = time.localtime()
        year = local_time.tm_year
        month_day = local_time.tm_mday
        month = local_time.tm_mon
        week_day = local_time.tm_wday
        hour, minute, second = local_time.tm_hour, local_time.tm_min, local_time.tm_sec
        
        return BasicTamilTimeFormat.format(year, month, month_day, week_day, hour, minute, second)

    @staticmethod
    def get_hour_prefix(hour):
        assert (hour >= 0 and hour <= 24)
        if (hour <= 3) or (hour >= 12 + 11):
            prefix = u"நள்ளிரவு"
        elif hour <= 6:
            prefix = u"அதிகாலை"
        elif hour < 12:
            prefix = u"காலை"
        elif hour < (12 + 3):
            prefix = u"மத்தியானம்"
        elif hour < (12 + 7):
            prefix = u"மாலை"
        elif hour < (12 + 11):
            prefix = u"இரவு"
        else:
            assert False
        return prefix    

class DigitalTamilClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Tamil Clock")
        self.setGeometry(100, 100, 400, 200)   
        
        # Set minimum and maximum size
        self.setMinimumSize(400, 200)  # Minimum width and height
        self.setMaximumSize(800, 400)  # Maximum width and height
             
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignCenter)
  
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;") 
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.label)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Update every second

        self.update_time()

    def update_time(self):
        current_time = DateUtils.get_time()
        self.label.setText(current_time)


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analogue & Digital Tamil Clock")
        self.setMinimumSize(350, 500)  # Minimum width and height
        self.setMaximumSize(600, 800)  # Maximum width and height

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

        self.hourHandColor = QColor(50, 50, 50)
        self.minuteHandColor = QColor(80, 80, 80)
        self.secondHandColor = QColor(200, 50, 50)

        self.secondHandPath = []
        self.trailLength = 30

        # Embed DigitalTamilClock
        self.digital_clock = DigitalTamilClock()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.digital_clock)  # Digital Clock on top
        self.setLayout(layout)



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()
        radius = min(center.x(), center.y()) * 0.8

        # Draw the full face with numbers
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(center, radius, radius)

        # Draw the numbers
        painter.setFont(QFont('Arial', int(radius * 0.15)))  # Adjust font size
        for i in range(1, 13):
            angle = i * 30 - 90
            x = center.x() + radius * 0.75 * math.cos(math.radians(angle))  # Slightly inside the tick marks
            y = center.y() + radius * 0.75 * math.sin(math.radians(angle))
            painter.drawText(int(x - radius * 0.07), int(y + radius * 0.05), str(i)) # Centering adjustment

        # Draw hour and minute ticks (slightly different from before)
        for i in range(60):  # 60 ticks for minutes and seconds
            angle = i * 6 - 90
            inner_radius = 0.8 if i % 5 == 0 else 0.85  # Longer ticks for hour markers
            x1 = center.x() + radius * inner_radius * math.cos(math.radians(angle))
            y1 = center.y() + radius * inner_radius * math.sin(math.radians(angle))
            x2 = center.x() + radius * 0.95 * math.cos(math.radians(angle)) # Ticks slightly shorter
            y2 = center.y() + radius * 0.95 * math.sin(math.radians(angle))

            pen = QPen(QColor(0, 0, 0), 1) if i % 5 != 0 else QPen(QColor(0, 0, 0), 2)  # Thicker pen for hour ticks
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))


        # Get current time
        time = QTime.currentTime()

        # Draw hands (same as before)
        self.drawHand(painter, time.hour() % 12, 30, radius * 0.5, self.hourHandColor)
        self.drawHand(painter, time.minute(), 6, radius * 0.7, self.minuteHandColor)

        # Second hand and trail (same as before)
        angle = time.second() * 6 - 90
        end_x = center.x() + radius * 0.85 * math.cos(math.radians(angle))
        end_y = center.y() + radius * 0.85 * math.sin(math.radians(angle))

        self.secondHandPath.append((int(end_x), int(end_y)))
        if len(self.secondHandPath) > self.trailLength:
            self.secondHandPath.pop(0)

        pen = QPen(self.secondHandColor, 2)
        painter.setPen(pen)
        for x, y in self.secondHandPath:
            painter.drawPoint(x, y)

        self.drawHand(painter, time.second(), 6, radius * 0.85, self.secondHandColor)

    def drawHand(self, painter, value, scale, length, color):
        angle = value * scale - 90
        end_x = self.rect().center().x() + length * math.cos(math.radians(angle))
        end_y = self.rect().center().y() + length * math.sin(math.radians(angle))

        painter.setPen(QPen(color, 2))
        painter.drawLine(self.rect().center().x(), self.rect().center().y(), int(end_x), int(end_y))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec_())



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
