from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QListWidget, QListWidgetItem, QPushButton
from tools import utils


class DeviceChooser(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle('Choose Device')
        self.device_list = utils.get_devices()
        self.__init_ui()
        self.main_window = main_window

    def __init_ui(self):
        list_widget = QListWidget(self)
        for device in self.device_list:
            btn = QPushButton(device)
            btn.clicked.connect(self.list_item_listener)
            item = QListWidgetItem(device)
            list_widget.addItem(item)
            list_widget.setItemWidget(item, btn)
        self.show()

    def list_item_listener(self):
        self.main_window.set_device(self.sender().text())
        self.close()
