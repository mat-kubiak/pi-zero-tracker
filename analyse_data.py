import sys

sys.path.insert(0, 'src')
from data import *
from parse import *
from rssi_pairmaker import *
from plot import *

# change for different outcome
input_file = 'archive/output.txt'
output_file = 'graph.png'

def main():
    data = read_file(input_file)

    records = extract_array(data)
    print(f'Records: {records}\n')

    pairs = create_connections(records)
    print(f'Pairs: {pairs}')

    plot_routes(pairs, output_file)

if __name__ == '__main__':
    main()