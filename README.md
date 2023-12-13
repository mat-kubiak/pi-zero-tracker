# Pi Zero Tracker Toolbox

A python utility to remotely control your pi tracker network via SSH.

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
pip install python-nmap
```
3. launch the tool:
```
python3 main.py [additional arguments]
```

### Usage

