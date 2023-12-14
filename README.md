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
usage: toolbox [-h] [-e EXECUTE] [-c COMMAND] [-t TARGET] [-n NETWORK] [-r]

Command utility to control pi trackers in the local network.

options:
  -h, --help            show this help message and exit
  -e EXECUTE, --execute EXECUTE
                        execute a script by name, normally found in the 'scripts' directory. If empty, will open the console.
  -c COMMAND, --command COMMAND
                        the command to execute on targets. Will overwrite the --execute argument.
  -t TARGET, --target TARGET
                        target hostnames separated by spaces. 'all' by default, targets all found trackers.
  -n NETWORK, --network NETWORK
                        network ip range to scan for trackers.
  -r, --rebuild_cache   attempts to rebuild tracker ip cache, stored in the 'trackers.json' file.
```

### Main Flow

During its execution, the app undergoes four steps:

1. __Initialization__ - parses cli input and initializes ssh connection manager
2. __Tracker Discovery__ - attempts to load trackers from trackers.json, if failed or forced, rebuilds it by discovering trackers from network
3. __Execution__ - either executes the specified script, or opens a console
4. __Finalization__ - closes all ssh connections and exits the app
