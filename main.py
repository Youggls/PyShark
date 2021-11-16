import sys
from tools import utils
from config import *
from ui import MainWindow
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow(window_name=ProjectName)
    sys.exit(app.exec_())
