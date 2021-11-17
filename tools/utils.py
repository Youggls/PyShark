import time
import pcap
import dpkt
import threading
from winpcapy import WinPcapUtils, WinPcapDevices


def get_devices():
    devices = WinPcapDevices.list_devices()
    return devices


def iter2string(ip):
    return f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}'


def parse_raw_package(ts, data):
    eth = dpkt.ethernet.Ethernet(data)
    if not isinstance(eth.data, dpkt.ip.IP):
        return 0, '', '', ''
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', (time.localtime(ts)))
    ip = eth.data
    src = iter2string(ip.src)
    dst = iter2string(ip.dst)
    if ip.p == 17:
        udp = ip.data
        protocol = 'UDP'
        if udp.sport == 443 or udp.dport == 443:
            protocol += '-HTTPS'
        elif udp.sport == 80 or udp.dport == 80:
            protocol += '-HTTP'
        elif udp.sport == 53 or udp.dport == 53:
            protocol += '-DNS'
    elif ip.p == 6:
        tcp = ip.data
        protocol = 'TCP'
        if tcp.sport == 443 or tcp.dport == 443:
            protocol += '-HTTPS'
        elif tcp.sport == 80 or tcp.dport == 80:
            protocol += '-HTTP'
    else:
        protocol = str(ip.p)
    return timestamp, protocol, src, dst


def capture_package(device, ip_address, event, task_list):
    while True:
        p = pcap.pcap(device, promisc=True)
        filter_str = 'ip and host ' + ip_address
        p.setfilter(filter_str)
        for ts, data in p:
            if event.is_set():
                task = ThreadWorker(ts, data)
                task_list.append(task)
                task.setDaemon(True)
                task.start()
            else:
                return


class ThreadWorker(threading.Thread):
    def __init__(self, ts, data):
        super(ThreadWorker, self).__init__()
        self.result = None
        self.ts = ts
        self.data = data

    def run(self):
        self.result = parse_raw_package(self.ts, self.data)

    def get_result(self):
        return self.result


class MainCaptureWorker(threading.Thread):
    def __init__(self, device, ip_address, event):
        super(MainCaptureWorker, self).__init__()
        self.device = device
        self.ip_address = ip_address
        self.event = event
        self.sub_task_list = []

    def run(self):
        capture_package(self.device, self.ip_address, self.event, self.sub_task_list)

    def get_result(self):
        return [worker.get_result() for worker in self.sub_task_list]
