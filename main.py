import os
import socket

from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev or isNewData:
            beacon_info = f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Name: {dev.getValueText(9)}, UUID: {dev.addr}, RSSI: {dev.rssi}"
            if dev.getValueText(9) == 'iNode_Bacon':
                print(beacon_info)
                with open("beacon_data.txt", "a") as file:
                    file.write(beacon_info + "\n")

scan_duration = 60  # 10 minutes
scanner = Scanner().withDelegate(ScanDelegate())
start_time = time.time()
while time.time() - start_time < scan_duration:
    devices = scanner.scan(1)
    time.sleep(1) #break between scans

class info:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile_path = os.path.join(script_dir, 'log')

    hostname = socket.gethostname()
    hostname = 'rasp12345' # uncomment to mimic pi (if not testing!!)
    host_number = int(hostname[4:])

def main():
    print('Hello from Raspberry Pi Zero no.{}!'.format(info.host_number))

if __name__ == '__main__':
    main()