import os, socket, time, argparse
from datetime import datetime

from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self, inc_date, white_ls, sepr):
        DefaultDelegate.__init__(self)
        self.time_format = '%Y-%m-%d %H:%M:%S' if inc_date else '%H:%M:%S'
        self.whitelist = white_ls
        self.separator = sepr
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not isNewDev and not isNewData:
            return

        if self.whitelist != None and not dev.getValueText(9) in self.whitelist:
            return

        timestamp = datetime.now().strftime(self.time_format)
        milliseconds = datetime.now().microsecond // 1000
        name = dev.getValueText(9)
        uuid = dev.addr
        rssi = dev.rssi

        report = f'{timestamp}:{milliseconds:03}{self.separator}{name}{self.separator}{uuid}{self.separator}{rssi}'

        print(report)
        with open("beacon_data.txt", "a") as file:
            file.write(report)

class info:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile_path = os.path.join(script_dir, 'log')

    hostname = socket.gethostname()
    hostname = 'rasp12345' # uncomment to mimic pi (if not testing!!)
    host_number = int(hostname[4:])

def parse_cli():
    parser = argparse.ArgumentParser(
        prog='pi-tracker',
        description='Bluetooth tracker software for raspberry pi devices.')

    parser.add_argument('-d', '--duration', default='120', help='Duration of scanning, expressed in float seconds. 120 by default.')
    parser.add_argument('-p', '--pause', default='1', help='Duration of the pause between scans, expressed in float seconds. 1 by default.')
    parser.add_argument('-w', '--whitelist', help='Whitelist of devices. If empty (default), will catch all.')
    parser.add_argument('-dt', '--date', action='store_true', help='Includes date in output records.')
    parser.add_argument('-s', '--separator', default=':', help='Separator between values in a single entry. \':\' by default.')

    args = parser.parse_args()
    return args

def main():
    global args
    args = parse_cli()
    
    with open("beacon_data.txt", "a") as file:
            file.write(f'\nReport for {info.hostname} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
 
    scanner = Scanner().withDelegate(ScanDelegate(args.date, args.whitelist, args.separator))
    start_time = time.time()
    
    while time.time() - start_time < float(args.duration):
        devices = scanner.scan(1)
        time.sleep(float(args.pause))


if __name__ == '__main__':
    main()