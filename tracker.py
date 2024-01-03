import os, socket, time, argparse
from datetime import datetime

from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self, inc_date, white_ls, sepr):
        DefaultDelegate.__init__(self)
        self.time_format = '%Y:%m:%d:%H:%M:%S' if inc_date else '%H:%M:%S'
        self.whitelist = white_ls
        self.separator = sepr
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not isNewDev and not isNewData:
            return

        if self.whitelist != None and not dev.getValueText(9) in self.whitelist.split():
            return

        timestamp = datetime.now().strftime(self.time_format)
        millis_str = f':{datetime.now().microsecond // 1000:03}' if args.milis else ''
        name = dev.getValueText(9)
        uuid = dev.addr
        rssi = dev.rssi

        report = f'{timestamp}{milis_str}{self.separator}{name}{self.separator}{uuid}{self.separator}{rssi}'

        if not args.disable_output:
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
        prog='tracker.py',
        description='Bluetooth tracker software for raspberry pi devices.',
        add_help=False
    )

    general = parser.add_argument_group('general options')
    general.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    general.add_argument('-d', '--duration', default='120', help='Duration of scanning, expressed in float seconds. 120 by default. If set to 0, it will run forever.')
    general.add_argument('-p', '--pause', default='1', help='Duration of the pause between scans, expressed in float seconds. 1 by default.')
    general.add_argument('-w', '--whitelist', help='Whitelist of devices. If empty (default), will catch all.')
    general.add_argument('-do', '--disable_output', action='store_true', help='Will disable output to console.')

    # format
    format = parser.add_argument_group('format')
    format.add_argument('-dt', '--date', action='store_true', help='Includes date in output records.')
    format.add_argument('-m', '--milis', action='store_true', help='Includes miliseconds in output records.')
    format.add_argument('-s', '--separator', default=' ', help='Separator between values in a single entry. Space by default.')

    args = parser.parse_args()
    return args

def main():
    global args
    args = parse_cli()

    with open("beacon_data.txt", "a") as file:
        file.write(f'\nReport for {info.hostname} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    scanner = Scanner().withDelegate(ScanDelegate(args.date, args.whitelist, args.separator))
    start_time = time.time()
    
    while args.duration == 0:
        devices = scanner.scan(1)
        time.sleep(float(args.pause))

    while time.time() - start_time < float(args.duration):
        devices = scanner.scan(1)
        time.sleep(float(args.pause))

if __name__ == '__main__':
    main()