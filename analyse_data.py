import sys

sys.path.insert(0, 'src')
from data import *
from parse import *
from rssi_pairmaker import *
from plot import *

# change for different outcome
input_dir = 'data'
output_dir = 'graphs'
overall_graph = 'graphs/breakfast.png'

def main():
	beacons = read_file('config/beacons.txt').split('\n')
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	total_pairs = []
	graphs_completed = 0

	for beacon in beacons:
		if not os.path.exists(f'{input_dir}/{beacon}.txt'):
			print(f'Warning: Beacon {beacon} data file not found, skipping ...')
			continue

		data = read_file(f'{input_dir}/{beacon}.txt')

		records = extract_array(data)
		if len(records) == 0:
			print(f'Warning: Data file for beacon {beacon} is empty. skipping ...')
			continue

		pairs = create_connections(records)
		if len(pairs) == 0:
			print(f'Warning: Could not find any connections for beacon {beacon}. skipping ...')
			continue

		total_pairs.extend(pairs)

		plot_routes(pairs, f'{output_dir}/{beacon}.png')
		graphs_completed += 1
	
	if graphs_completed < 2:
		print(f'Warning: no new data for overall graph, skipping ...')
	else:
		plot_routes(total_pairs, overall_graph)
		graphs_completed += 1

	print(f'Graphs created: {graphs_completed} out of {len(beacons) + 1}')

if __name__ == '__main__':
    main()