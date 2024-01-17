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


maximal_motion_speed = 3.5  # meters / second
minimal_distance_between_sensors = 10  # meters
minimal_travel_time = int((minimal_distance_between_sensors / maximal_motion_speed) * 10)  # in tens of a second


def create_connections(sensor_data, distances):

    pairs = []
    rssi_values = []
    last_recorded_signal_timestamp = 0

    # Do the procedure for the first time
    # First and last scan always has signal from the closest sensor
    for j in range(1, len(sensor_data)):
        rssi_values.append(sensor_data[j][0])

    active_raspberry = return_strongest_index(rssi_values)
    # active raspberry = closest to the beacon at the moment
    pairs.append((active_raspberry,))

    last_pair_index = 0
    for i in range(1, len(sensor_data[0])):
        rssi_values = []
        for j in range(1, len(sensor_data)):
            rssi_values.append(sensor_data[j][i])

        active_raspberry = return_strongest_index(rssi_values)
        if sensor_data[0][i] - last_recorded_signal_timestamp > minimal_travel_time:
            # if move happened too fast it is regarded as an error (caused by signal spike)
            if pairs[last_pair_index][0] != active_raspberry and active_raspberry:
                # last signal is not the same as new one -> beacon moves closer to different raspberry
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

# print(create_connections(dummy_sensor_data))
