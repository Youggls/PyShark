from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
from tools import utils


class DeviceChooser(QDialog):
    def __init__(self, main_window):
        """
        Initialization function
        :param main_window: main windows object
        """
        super().__init__()
        self.setWindowTitle('Choose Device')
        self.device_dic = utils.get_devices()
        self.device_id_list = [key for key in self.device_dic]
        self.table = QTableWidget()
        self.main_window = main_window
        self.__init_ui()

    def __init_ui(self):
        self.setGeometry(self.main_window.main_window_rect)
        self.resize(self.main_window.main_window_size)
        self.setFixedSize(self.main_window.main_window_size)

        total_container = QVBoxLayout()
        confirm_button = QPushButton('Choose and Start Capture', self)
        confirm_button.clicked.connect(self.start_button_listener)
        total_container.addWidget(confirm_button)

        self.table.setRowCount(len(self.device_dic))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['device name', 'device id'])
        self.table.setVerticalHeaderLabels([str(i) for i in range(len(self.device_dic))])
        for idx, device in enumerate(self.device_dic):
            device_name_item = QTableWidgetItem(self.device_dic[device])
            device_id_item = QTableWidgetItem(device)
            self.table.setItem(idx, 0, device_name_item)
            self.table.setItem(idx, 1, device_id_item)

        total_container.addWidget(self.table)
        self.setLayout(total_container)
        self.adjustSize()
        self.show()

    def start_button_listener(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Error!', 'Please choose legal row!')
        self.main_window.set_device(self.device_id_list[row], self.device_dic[self.device_id_list[row]])
        self.close()
