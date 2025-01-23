"""
Author: Jesman Anthonypillai
Email: jesman23@gmail.com
Date: July 23, 2024
Description: தற்போதைய நேரம் மற்றும் தேதி தூய தமிழில். 

             This is a Digital Tamil Clock application developed in Python using PyQt5. 
             It displays the current time and date in Pure Tamil Only.
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
	
from tamiltime import TamilTime  # Ensure this module is correctly implemented



class DigitalTamilClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("உங்கள் நேரமும் தேதியும் உங்கள் கையில்")
        self.setGeometry(100, 100, 450, 200)

        # Disable maximize button and fix the window size
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(450, 200)

        # Label to display the time
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: green;")

        # Layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Timer for updating the time
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Update every second

        self.update_time()

    def update_time(self):
        # Fetch current time in Tamil
        current_time = TamilTime.get_tamil_time()
        self.label.setText(current_time)

def main():
    app = QApplication([])
    clock = DigitalTamilClock()
    clock.show()
    app.exec_()

if __name__ == '__main__':
    main()

