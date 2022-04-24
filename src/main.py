# !/usr/bin/python

import sys
import os
from app import *
from setColorWindow import *

StyleSheet = '''
#RedProgressBar {
    text-align: center;
}
#RedProgressBar::chunk {
    background-color: #F44336;
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
#BlueProgressBar {
    border: 2px solid #2196F3;
    border-radius: 5px;
    background-color: #E0E0E0;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
    width: 10px;
    margin: 0.5px;
}
'''

if __name__ == "__main__":

    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(StyleSheet)

    popWin = popWindow("Dark or Light or Orange ?", ["Light", "Orange", "Dark"])
    popWin.show()

    # Run the application
    sys.exit(app.exec_())