from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QApplication, QVBoxLayout, QHBoxLayout
from .DeviceChooser import DeviceChooser


class MainWindow(QWidget):
    """
    The main window of current application
    """
    def __init__(self, window_name, is_debug=True):
        super().__init__()
        # Get resolution of current monitor
        self.device_name = 'Name: NULL'
        self.device_id = 'ID: NULL'
        self.device_id_label = QLabel(self.device_id, self)
        self.device_name_label = QLabel(self.device_name, self)
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
        # Main windows rect
        self.main_window_rect = QRect(self.window_pos_x, self.window_pos_y, self.window_width, self.window_height)
        self.main_window_size = QSize(self.window_width, self.window_height)
        # Set main window title
        self.setWindowTitle(window_name)
        # Call init_ui to init window.
        self.init_ui()
        # If is_debug is True, print basic information of main window.
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
        # Set window size and position
        self.setGeometry(self.main_window_rect)
        self.resize(self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)

        total_container = QVBoxLayout()
        top_container = QHBoxLayout()
        middle_container = QHBoxLayout()

        choose_device_btn = QPushButton('Choose device', self)
        # choose_device_btn.move(20, 20)
        choose_device_btn.clicked.connect(self.choose_device_button_listener)
        top_container.addWidget(choose_device_btn)
        top_container.addWidget(self.device_id_label)
        top_container.addWidget(self.device_name_label)
        # self.device_id_label.move(220, 27)

        # Middle h-box, input capture duration time.
        time_hint = QLabel('Capture duration (s)', self)
        # time_hint.move(20, 60)
        time_input = QLineEdit(self)
        # time_input.move(220, 57)

        middle_container.addWidget(time_hint)
        middle_container.addWidget(time_input)

        total_container.addLayout(top_container)
        total_container.addLayout(middle_container)

        self.setLayout(total_container)

        self.show()

    def choose_device_button_listener(self):
        chooser = DeviceChooser(self)
        chooser.show()
        chooser.exec_()

    def set_device(self, device_id, device_name):
        self.device_id = device_id
        self.device_id_label.setText('ID: ' + device_id)
        self.device_name = device_name
        self.device_name_label.setText('Name: ' + device_name)
        self.device_id_label.adjustSize()
        self.device_name_label.adjustSize()
        self.show()
