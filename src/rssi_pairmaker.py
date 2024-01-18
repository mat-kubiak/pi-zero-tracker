from src.data import read_json_file


# dummy_sensor_data = [[17042829740, 17042829750, 17042829760, 17042829770, 17042829780, 17042829790, 17042829800],
#                      [-1000, -59, -1000, -61, -1000, -59, -1000],
#                      [-58, -1000, -1000, -67, -1000, -56, -1000],
#                      [-1000, -56, -1000, -65, -1000, -1000, -54]
#                      ]
#
#   dummy data structure:   [[time values, ...],
#                             [first sensor data, ...],
#                             [second sensor data, ...], ...
#                           ]
#
#                           sensor_data[raspberry_no][measurement_no]
#                           raspberry_no == 0 -> time_value
#

def return_strongest_index(args):
    if all(arg == -1000 for arg in args):
        return 0
    else:
        max_arg_index = None
        max_value = -1001
        for i, arg in enumerate(args):
            if arg > max_value and arg > -90 and arg != -1000:
                max_value = arg
                max_arg_index = i
        return 0 if max_arg_index is None else max_arg_index + 1


def create_connections(sensor_data, distances, max_bc_speed = 3.5):

    pairs = []
    rssi_values = []
    last_recorded_signal_timestamp = sensor_data[0][0]

    # Do the procedure for the first time
    # First and last scan always has signal from the closest sensor
    for j in range(1, len(sensor_data)):
        rssi_values.append(sensor_data[j][0])

    last_active_raspberry = return_strongest_index(rssi_values)
    # active raspberry = closest to the beacon at the moment
    pairs.append((last_active_raspberry,))

    last_pair_index = 0
    for i in range(1, len(sensor_data[0])):
        rssi_values = []
        for j in range(1, len(sensor_data)):
            rssi_values.append(sensor_data[j][i])

        active_raspberry = return_strongest_index(rssi_values)

        if pairs[last_pair_index][0] != active_raspberry and active_raspberry:
            # last signal is not the same as new one -> beacon moves closer to different raspberry
            current_distance = int(distances[f'{last_active_raspberry-1}-{active_raspberry-1}'])
            if current_distance:
                if sensor_data[0][i] - last_recorded_signal_timestamp > int(current_distance * 10 / max_bc_speed):
                    print(sensor_data[0][i] - last_recorded_signal_timestamp)
                    print(int(current_distance * 10 / max_bc_speed))
                    # if move happened too fast it is regarded as an error (caused by signal spike)

                    last_active_raspberry = active_raspberry
                    pairs[last_pair_index] += (active_raspberry,)
                    last_pair_index += 1
                    pairs.append((active_raspberry,))
                    last_recorded_signal_timestamp = sensor_data[0][i]

    pairs.pop()
    return pairs


dummy_sensor_data = [[17042829740, 17042829750, 17042829760, 17042829770, 17042829780, 17042829790, 17042829800],
                     [-1000, -59, -1000, -61, -1000, -59, -1000],
                     [-58, -1000, -1000, -67, -1000, -56, -1000],
                     [-1000, -56, -1000, -65, -1000, -1000, -54]
                     ]

config = read_json_file('../config.json')

trackers = sorted(list(config['trackers'].keys()))
distances = {}
for key in config['distances'].keys():
	first, second = [trackers.index(part) for part in key.split('-')]
	value = config['distances'][key]

	distances[f'{first}-{second}'] = value
	distances[f'{second}-{first}'] = value

for i in range(len(trackers)):
	distances[f'{i}-{i}'] = 0.

maximal_beacon_speed = float(config['maximal_beacon_speed(m/s)'])

print(create_connections(dummy_sensor_data, distances, maximal_beacon_speed))
# print(create_connections(dummy_sensor_data))
