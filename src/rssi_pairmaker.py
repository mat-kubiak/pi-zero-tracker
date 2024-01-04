# dummy_sensor_data = [[1704282974, 1704282975, 1704282976, 1704282977, 1704282978, 1704282979, 1704282980],
#                      [-1000, -59, -1000, -61, -1000, -59, -1000],
#                      [-58, -1000, -1000, -67, -1000, -56, -1000],
#                      [-1000, -56, -1000, -65, -1000, -1000, -54]]

def check_rssi(args):
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

def create_connections(sensor_data):

    times_no_signal = 0
    pairs = []
    values = []

    # Do the procedure for the first time. Do not worry about lack of signal. First and last scan always has signal
    for j in range(1, len(sensor_data)):
        values.append(sensor_data[j][0])
    active_raspberry = check_rssi(values)
    pairs.append((active_raspberry,))

    last_pair = 0
    for i in range(1, len(sensor_data[0])):
        values = []
        for j in range(1, len(sensor_data)):
            values.append(sensor_data[j][i])

        active_raspberry = check_rssi(values)
        if pairs[last_pair][0] != active_raspberry and active_raspberry: #signals does not stay still. Beacon moves to different raspberry
            pairs[last_pair] += (active_raspberry,)
            last_pair += 1
            pairs.append((active_raspberry,))

    pairs.pop()
    return pairs
