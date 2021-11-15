from winpcapy import WinPcapUtils, WinPcapDevices


def get_devices():
    devices = WinPcapDevices.list_devices()
    return devices
