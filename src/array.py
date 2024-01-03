from datetime import datetime
import numpy as np

no_signal_value = -1000  # value for the array when no signal is detected

def extract_array(file_content):
    reference_arr = []
    time_arr = []  # array of times from output.txt file
    raspberry_num = 0  # raspberry number

    for line in file_content.splitlines():
        if "rasp" in line: # will break if we're scanning for other trackers
            raspberry_num += 1
            continue
        
        columns = line.split(',')
        time = columns[0]
        rssi = columns[3].split('\n')[0]

        reference_arr.append([time, raspberry_num, rssi])
        time_arr.append(time)

    # create new array with all timestamps
    time_arr.sort()
    today = datetime.today() # since the output file doesn't have DD:MM:YYYY value, we will use current days value
    dtb = datetime.combine(today, datetime.strptime(time_arr[0], '%H:%M:%S').time())  # dtb - datetime begin
    dte = datetime.combine(today, datetime.strptime(time_arr[len(time_arr) - 1], '%H:%M:%S').time())  # datetime end
    full_time_arr = np.array(range(int(dtb.timestamp()), int(dte.timestamp() + 1)))  # array of all times from rage

    # Next we create our final array, for now all rssi values will be no_signal_values (they will be changed later)
    # final_arr is a 2d array, where first row is time and subsequent rows are rssi values from given raspberry devices
    # for example: row 2 (id 1) will be rssi values from rasp1
    leng = len(full_time_arr)
    for raspb in range(raspberry_num):
        temp_arr = np.full(leng, no_signal_value)
        full_time_arr = np.append(full_time_arr, temp_arr)
    final_arr = np.reshape(full_time_arr, (raspberry_num+1, -1))

    # Finally we replace no_signal_values from final_arr with proper values taken from reference_arr
    for i in range(len(reference_arr)):
        final_arr[reference_arr[i][1]][int(datetime.combine(today, datetime.strptime(reference_arr[i][0], '%H:%M:%S').time()).timestamp())-full_time_arr[0]] = reference_arr[i][2]
    return final_arr
    