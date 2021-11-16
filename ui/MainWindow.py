from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QApplication
from .DeviceChooser import DeviceChooser


class MainWindow(QWidget):
    """
    The main window of current application
    """
    def __init__(self, window_name, is_debug=True):
        super().__init__()
        # Get resolution of current monitor
        self.device_id = QLabel('NULL', self)
        self.desktop = QApplication.desktop()
        self.screen_rect = self.desktop.screenGeometry()
        self.height = self.screen_rect.height()
        self.width = self.screen_rect.width()

        # calculate the window size by monitor size.
        self.window_height = int(self.height / 2)
        self.window_width = int(self.width / 3)
        # The start position of main window.
        self.window_pos_x = int(self.width / 2 - self.window_width / 2)
        self.window_pos_y = int(self.height / 2 - self.window_height / 2)

        self.setWindowTitle(window_name)
        self.init_ui()
        if is_debug:
            self.__print_info()

    def __print_info(self):
        print(f'The resolution of current monitor is {self.width} * {self.height}')
        print(f'The main window size is {self.window_width} * {self.window_height}')
        print(f'The position of window is {self.window_pos_x} * {self.window_pos_y}')

    def init_ui(self):
        """
        Init ui
        :return: None
        """
        self.setGeometry(self.window_pos_x, self.window_pos_y, self.window_width, self.window_height)
        self.resize(self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        # self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)

        choose_device_btn = QPushButton('选择网卡', self)
        choose_device_btn.move(20, 20)
        choose_device_btn.clicked.connect(self.button_listener)
        self.device_id.move(150, 20)

        # Middle h-box, input capture duration time.
        time_hint = QLabel('捕获时间 (s)', self)
        time_hint.move(20, 60)
        time_input = QLineEdit(self)
        time_input.move(150, 60)

        self.show()

    def button_listener(self):
        sender = self.sender()
        print('button')
        chooser = DeviceChooser(self)
        chooser.show()
        chooser.exec_()

    def set_device(self, text):
        self.device_id.setText(text)
