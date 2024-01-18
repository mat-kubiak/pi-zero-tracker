import sys

sys.path.insert(0, 'src')
from data import *
from parse import *
from rssi_pairmaker import *
from plot import *

config = read_json_file('config.json')
input_dir = config['data_directory']
output_dir = config['graph_directory']
trackers = sorted(list(config['trackers'].keys()))
beacons = sorted(config['beacons'])

distances = {}
for key in config['distances'].keys():
	rasps = key.split('-')
	first = trackers.index(rasps[0])
	second = trackers.index(rasps[1])

	value = config['distances'][key]
	distances[f'{first}-{second}'] = value
	distances[f'{second}-{first}'] = value

maximal_beacon_speed = float(config['maximal_beacon_speed(m/s)'])

def main():
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

		pairs = create_connections(records, distances, maximal_beacon_speed)
		if len(pairs) == 0:
			print(f'Warning: Could not find any connections for beacon {beacon}. skipping ...')
			continue

		total_pairs.extend(pairs)
		plot_routes(pairs, f'{output_dir}/{beacon}.png', trackers)
		graphs_completed += 1
	
	if graphs_completed < 2:
		print(f'Warning: no new data for overall graph, skipping ...')
	else:
		plot_routes(total_pairs, output_dir + '/breakfast.png')
		graphs_completed += 1

	print(f'Graphs created: {graphs_completed} out of {len(beacons) + 1}')

if __name__ == '__main__':
    main()