import sys
from config import *
from ui import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow(window_name=ProjectName)
    sys.exit(app.exec_())
