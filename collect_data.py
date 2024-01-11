import sys, os, threading
from fabric import *

sys.path.insert(0, 'src')
from utils import *

# change for different outcome
output_dir = 'data'

def main():
    
    # INITIALIZE
    password = read_file('config/password.txt')
    trackers = read_json_file('config/trackers.json')
    targets = trackers.keys()
    beacons = read_file('config/beacons.txt').split()
    command = 'cd pi-zero-tracker && cat beacon_data.txt'

    # RUN
    results = {}
    for target in targets:
        c = Connection(host=trackers[target], user='admin', connect_kwargs={'password': password})
        results[target] = c.run(command, hide=True).stdout.strip()
        c.close()
        print(f'{target} data collected')
        print(results[target])

    # SPLIT BY BEACONS
    output_files = {}
    for beacon in beacons:
        output_files[beacon] = ''

        for target in targets:
            output_files[beacon] += f'{target}:\n'
            lines = results[target].split('\n')
            
            for line in lines:
                if beacon in line:
                    output_files[beacon] += f'{line}\n'
    
    # SAVE
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for beacon in beacons:
        write_file(f'{output_dir}/{beacon}.txt', output_files[beacon])

if __name__ == '__main__':
    main()