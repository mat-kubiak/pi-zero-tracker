import os, socket, time, argparse
from datetime import datetime

from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self, white_ls):
        DefaultDelegate.__init__(self)
        self.whitelist = white_ls
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not isNewDev and not isNewData:
            return

        # an empty whitelist will catch all devices
        if self.whitelist != None and not dev.getValueText(9) in self.whitelist.split():
            return

        timestamp = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        milis = f'{datetime.now().microsecond // 1000:03}'
        name = dev.getValueText(9)
        uuid = dev.addr
        rssi = dev.rssi

        report = f'{timestamp},{milis},{name},{uuid},{rssi}'

        if not args.disable_output:
            print(report)

        # record is appended to file after every discovery, so the data won't be lost when the program fails
        with open("beacon_data.txt", "a") as file:
            file.write(report + '\n')

class info:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile_path = os.path.join(script_dir, 'log')
    hostname = socket.gethostname()
    host_number = int(hostname[4:])

def parse_cli():
    parser = argparse.ArgumentParser(
        prog='tracker.py',
        description='Bluetooth tracker software for raspberry pi devices.',
        add_help=False
    )

    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    parser.add_argument('-d', '--duration', default='120', help='Duration of scanning, expressed in float seconds. 120 by default. If set to 0, it will run forever.')
    parser.add_argument('-p', '--pause', default='1', help='Duration of the pause between scans, expressed in float seconds. 1 by default.')
    parser.add_argument('-w', '--whitelist', help='Whitelist of devices. If empty (default), will catch all.')
    parser.add_argument('-do', '--disable_output', action='store_true', help='Will disable output to console.')

    args = parser.parse_args()
    return args

def main():
    global args
    args = parse_cli()

    scanner = Scanner().withDelegate(ScanDelegate(args.whitelist))
    start_time = time.time()

    while float(args.duration) == 0:
        devices = scanner.scan(1)
        time.sleep(float(args.pause))

    while time.time() - start_time < float(args.duration):
        devices = scanner.scan(1)
        time.sleep(float(args.pause))

if __name__ == '__main__':
    main()