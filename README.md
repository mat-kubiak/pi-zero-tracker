# Pi Zero Tracker Toolbox

A python utility to remotely control your pi tracker network over SSH.

### Hardware Setup

Please create your setup with following restrictions in mind:

* All pi zeroes and the controller have to be connected to the same network.
* All pi zeroes hostnames have to follow `rasp[1-9][0-9]*` pattern, i.e. `rasp1`, `rasp2` `rasp4`, `rasp10001` etc.
* Two different pi zeroes cannot have the same name.
* All pi zeroes have to have an `admin` user with sudo privileges.
* All pi zeroes' `admin` users have to have the same password.

### Software Setup

1. create a folder `config` with files inside:
   * `password.txt` containing the password to the `admin` users on trackers.
   * `trackers.json` containing a list of tracker ips using the format:
    ```json
    {
      "rasp1":"192.168.0.1",
      "rasp2":"192.168.0.2",
      "rasp3":"192.168.0.3"
    }
    ```
   * `beacons.txt` containing the list of beacon names in separate lines, i.e.:
    ```
    iNode_Bacon
    iNode_Eggs
    iNode_Bread
    ```
2. install necessary libraries:
``` bash
pip install fabric numpy matplotlib
```
3. launch one of the scripts:
``` bash
python3 activate_trackers.py # run the program on trackers
python3 collect_data.py # collect data from trackers and save it in a folder
python3 analyse_data.py # read local data, analyse it and put it on graphs
```

> __Note__: inside each script, there is a section labeled `# change for different outcome`, under which you can change variables as you wish
