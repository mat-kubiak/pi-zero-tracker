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
pip install python-nmap fabric numpy matplotlib
```
3. launch the tool:
```
python3 toolbox.py [additional arguments]
```

### How to use
```
usage: toolbox.py (-s SCRIPT | -c COMMAND | -g | -d) [-t TARGETS] [-n NETWORK] [-i INPUT] [-o OUTPUT] [-h] [-l] [-r]

Command-line utility for controlling bluetooth trackers in the local network.

Remote Operations:
  -s SCRIPT, --script SCRIPT
                        Execute a script by name, normally found in the 'scripts' directory.
  -c COMMAND, --command COMMAND
                        Executes a custom command.
  -g, --graph           Extract data from output file and create a graph.
  -d, --dummy           Do nothing.

Options:
  -t TARGETS, --targets TARGETS
                        Target hostnames separated by spaces. 'all' by default, targets all found trackers.
  -n NETWORK, --network NETWORK
                        Overwrites network ip range used for scaning for trackers.
  -i INPUT, --input INPUT
                        Specifies input text file with data used for --graph. 'archive/output/txt' by default.
  -o OUTPUT, --output OUTPUT
                        Specifies output file used for --graph. 'archive/graph.png' by default.
  -h, --help            Show this help message and exit.
  -l, --list_scripts    List all available scripts and exit.
  -r, --rebuild_cache   Forces to rebuild tracker ip cache, stored in the 'trackers.json' file.
```

## Example uses

``` bash
python3 toolbox.py -s execute # run the `execute` script on all found trackers (executes main.py)

python3 toolbox.py -ld # list all scripts

python3 toolbox.py -c 'ls -al' # run the `ls -al` command on all found trackers (working dir is `/home/admin/pi-zero-tracker`)

python3 toolbox.py -rd # rebuild tracker ip cache
```
