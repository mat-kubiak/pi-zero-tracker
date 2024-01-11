import sys

sys.path.insert(0, 'src')
from utils import *
from parse import *
from rssi_pairmaker import *
from plot import *

# change for different outcome
input_dir = 'data'
output_dir = 'graphs'

def main():
    beacons = read_file('config/beacons.txt').split('\n')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pairs = {}

    for beacon in beacons:
        if not os.path.exists(f'{input_dir}/{beacon}.txt'):
            print(f'Beacon {beacon} data not found, skipping')
            continue

        data = read_file(f'{input_dir}/{beacon}.txt')

        records = extract_array(data)
        print(f'Records: {records}\n')

        pairs[beacon] = create_connections(records)
        print(f'Pairs: {pairs[beacon]}')

        plot_routes(pairs[beacon], f'{output_dir}/{beacon}.png')

if __name__ == '__main__':
    main()