# Pi Zero Tracker

Bluetooth beacon tracker for Pi Zero.

Software from branch `main` should run on a raspberry pi tracker device. To remotely control it, use software from the [toolbox branch](https://github.com/mat-kubiak/pi-zero-tracker/tree/toolbox) on a separate computer connected to the same local network as the tracker. The report is generated in the file `beacon_data.txt`

> IMPORTANT! When using the script, always use `sudo`. The Bluepy library requires root privileges to work with bluetooth. 

## Get Started

1. Install [pi imager software](https://www.raspberrypi.com/software/).
2. during the os installation on a choosen micro sd card, click the 'edit settings' option:
   1. set up hostname as `rasp` preceding an intiger number (i.e. `rasp0`, `rasp1002` etc.). It's recommended that all trackers have different hostnames.
   2. set up username `admin` and a choosen password. (the password has to be the same for all trackers).
   3. (optional) set up automatic wireless lan connection to a wifi network (recommended for testing since direct connection requires a lan adapter)
   4. ensure that in 'services' tab ssh via password authentication is enabled.
3. click 'save' and 'yes' for 'would you like to apply OS customization settings?'. This will install the software
4. After installation, clone this repository into the `/home/admin/pi-zero-tracker` directory of the `rootfs` partition on the card.
5. put the microsd card into raspberry pi, connect power and turn on wifi or connect via lan. 
6. the tracker can now be controlled manually via an ssh connection or by the `toolbox` script from another pc connected to the same network.

## Help Page

```
usage: tracker.py [-h] [-d DURATION] [-p PAUSE] [-w WHITELIST] [-do]

Bluetooth tracker software for raspberry pi devices.

options:
  -h, --help            Show this help message and exit.
  -d DURATION, --duration DURATION
                        Duration of scanning, expressed in float seconds. 120 by default. If set to 0, it will run forever.
  -p PAUSE, --pause PAUSE
                        Duration of the pause between scans, expressed in float seconds. 1 by default.
  -w WHITELIST, --whitelist WHITELIST
                        Whitelist of devices. If empty (default), will catch all.
  -do, --disable_output
                        Will disable output to console.
```

## Example Uses

``` bash
sudo python3 tracker.py # default options, executes for 120s with 1s pause.

sudo python3 tracker.py -d 60 -p 0.5 # scan for 60 seconds with 0.5 s pause between scans.

sudo python3 tracker.py -d 0 -do # run indefinitely without printing output.
```
