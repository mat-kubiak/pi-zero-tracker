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

1. create the text file `password.txt` containing the password to the `admin` users on trackers.
2. install necessary libraries:
```
pip install python-nmap fabric
```
3. launch the tool:
```
python3 toolbox.py [additional arguments]
```

### How to use
```
usage: toolbox [-h] [-e EXECUTE] [-t TARGET] [-n NETWORK]

Command utility to control pi trackers in the local network.

options:
  -h, --help            show this help message and exit
  -e EXECUTE, --execute EXECUTE
                        execute a script by name. If empty, will open the console.
  -t TARGET, --target TARGET
                        target hostnames separated by spaces. 'all' by default, targets all found trackers.
  -n NETWORK, --network NETWORK
                        network ip range to scan for trackers.
```
