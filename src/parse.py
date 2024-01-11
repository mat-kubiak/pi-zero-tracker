from datetime import datetime
import numpy as np

no_signal_value = -1000  # value for the array when no signal is detected


def extract_array(file_content):
    reference_arr = []
    time_arr = []  # array of times from output.txt file
    raspberry_num = 0  # raspberry number

    for line in file_content.splitlines():
        if "rasp" in line:  # will break if we're scanning for other trackers
            raspberry_num += 1
            continue
        
        columns = line.split(',')
        date = datetime.strptime(columns[0], "%Y-%m-%d").date()
        time = datetime.strptime(str(columns[1] + ',' + columns[2]), "%H:%M:%S,%f").time()
        time_value = datetime.combine(date, time)
        rssi = columns[5].split('\n')[0]

        reference_arr.append([time_value, raspberry_num, rssi])
        time_arr.append(time_value)

    if len(reference_arr) == 0:
        return []

    # create new array with all timestamps
    time_arr.sort()  # sort time_arr and use first and last value to create a range of all time values
    full_time_arr = np.array(range(int(time_arr[0].timestamp() * 10), int(time_arr[len(time_arr) - 1].timestamp() * 10 + 1)))  # array of all times from rage

    # Next we create our final array, for now all rssi values will be no_signal_values (they will be changed later)
    # final_arr is a 2d array, where first row is time and subsequent rows are rssi values from given raspberry devices
    # for example: row 2 (id 1) will be rssi values from rasp1
    leng = len(full_time_arr)
    temp_arr = np.full(leng * raspberry_num, no_signal_value)
    full_time_arr = np.append(full_time_arr, temp_arr)
    final_arr = np.reshape(full_time_arr, (raspberry_num+1, -1))

    # Finally we replace no_signal_values from final_arr with proper values taken from reference_arr
    for i in range(len(reference_arr)):
        final_arr[reference_arr[i][1]][int(reference_arr[i][0].timestamp() * 10) - full_time_arr[0]] = int(reference_arr[i][2])
    return final_arr
    