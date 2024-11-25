"""
Author: Jesman Anthonypillai
Email: jesman23@gmail.com
Date: July 23, 2024
Description: தற்போதைய நேரம் மற்றும் தேதி தூய தமிழில். 

             This is a Digital Tamil Clock application developed in Python using PyQt5. 
             It displays the current time and date in Pure Tamil Only.
"""


from __future__ import print_function
import time
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

PYTHON3 = sys.version > '3'

if PYTHON3:
    class long(int):
        pass

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
        self.setWindowTitle("உங்கள் நேரமும் தேதியும் உங்கள் கையில்")
        self.setGeometry(100, 100, 450, 200)   
        
        # Set minimum and maximum size
        self.setMinimumSize(400, 200)  # Minimum width and height
        self.setMaximumSize(800, 400)  # Maximum width and height
        
        # Set the window icon
        app_icon = QIcon("./icon.png")
        self.setWindowIcon(app_icon)

             
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: green;")
        
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

def main():
    app = QApplication(sys.argv)
    clock = DigitalTamilClock()
    clock.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

