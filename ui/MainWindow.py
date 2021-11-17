import threading
import time

from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QApplication, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QMessageBox, QTableWidgetItem
from .DeviceChooser import DeviceChooser
from tools import utils


class MainWindow(QWidget):
    """
    The main window of current application
    """
    def __init__(self, window_name, is_debug=True):
        super().__init__()
        # Timer
        self.event = threading.Event()

        # Basic value of device, ip address and duration time
        self.device_name = 'Device Name: NULL'
        self.device_id = 'Device ID: NULL'
        self.ip_address = '-1.-1.-1.-1'
        self.duration_time = -1

        # Basic component
        self.device_id_label = QLabel(self.device_id, self)
        self.device_name_label = QLabel(self.device_name, self)
        self.time_input = QLineEdit(self)
        self.ip_input = QLineEdit(self)
        self.table = QTableWidget()

        # Get resolution of current monitor
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
        bottom_container = QHBoxLayout()

        choose_device_btn = QPushButton('Choose device', self)
        choose_device_btn.clicked.connect(self.choose_device_button_listener)
        top_container.addWidget(choose_device_btn)
        top_container.addWidget(self.device_id_label)
        top_container.addWidget(self.device_name_label)

        time_hint = QLabel('Capture duration (s)', self)
        ip_address_hint = QLabel('IP address', self)
        middle_container.addWidget(time_hint)
        middle_container.addWidget(self.time_input)
        middle_container.addWidget(ip_address_hint)
        middle_container.addWidget(self.ip_input)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Time', 'Protocol', 'Origin Address', 'Target Address'])
        bottom_container.addWidget(self.table)

        total_container.addLayout(top_container)
        total_container.addLayout(middle_container)
        total_container.addLayout(bottom_container)

        self.setLayout(total_container)
        self.show()

    def choose_device_button_listener(self):
        chooser = DeviceChooser(self)
        chooser.show()
        chooser.exec_()

    def __get_input(self):
        self.duration_time = self.time_input.text()
        self.ip_address = self.ip_input.text()

    def __check_and_transform_input_value(self):
        self.__get_input()
        try:
            self.duration_time = int(self.duration_time)
        except ValueError:
            QMessageBox.warning(self, 'Value Error', 'Please input correct time!')
            return False
        if self.duration_time <= 0:
            QMessageBox.warning(self, 'Value Error', 'Please input positive time!')
            return False
        if self.ip_address == '' or self.ip_address == '-1.-1.-1.-1' or self.ip_address is None:
            QMessageBox.warning(self, 'Value Error', 'Please input right ip address')
            return False
        return True

    def __show_result(self):
        res = self.capture_task.get_result()
        self.table.setRowCount(len(res))
        for i, line in enumerate(res):
            for j, item in enumerate(line):
                self.table.setItem(i, j, QTableWidgetItem(item))
        self.show()

    def __time_control(self):
        time.sleep(self.duration_time)
        self.event.clear()
        self.__show_result()

    def __handle_capture(self):
        if self.__check_and_transform_input_value():
            self.event.set()
            self.capture_task = utils.MainCaptureWorker(self.device_id, self.ip_address, self.event)
            controller = threading.Thread(
                target=self.__time_control
            )
            self.capture_task.start()
            controller.start()
        else:
            return

    def set_device(self, device_id, device_name):
        self.device_id = device_id
        self.device_id_label.setText('Device ID: ' + device_id)
        self.device_name = device_name
        self.device_name_label.setText('Device Name: ' + device_name)
        self.device_id_label.adjustSize()
        self.device_name_label.adjustSize()
        self.show()
        self.__handle_capture()
