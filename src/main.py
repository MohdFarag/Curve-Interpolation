# !/usr/bin/python

import sys
import warnings
from app import QApplication, Window
from stylesheets import StyleSheet

warnings.filterwarnings("ignore")

def main():
    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(StyleSheet)

    window = Window()
    window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
