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

1. modify the default `config.json` file to fit your needs, include info about password, trackers and beacons.
2. install necessary libraries:
``` bash
pip install fabric numpy matplotlib
```
1. launch one of the scripts:
``` bash
python3 activate_trackers.py # run the program on trackers
python3 collect_data.py # collect data from trackers and save it in a folder
python3 analyse_data.py # read local data, analyse it and put it on graphs
```

> __Note__: inside each script, there is a section labeled `# change for different outcome`, under which you can change variables as you wish
