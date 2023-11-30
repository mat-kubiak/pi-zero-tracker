# pi-zero-tracker

Bluetooth beacon tracker for Pi Zero.

## How this works

1. Raspberry pi is configured to automatically connect to a wifi network at startup.
2. Immediately after that, the Network Manager will execute `/etc/network/if-up.d/02-github-automate-script`,
which will pull the newest code from `test` branch and execute `start.sh` script.
3. `start.sh` will launch the virtual test environment and then execute the main project through `main.py`
4. All errors and output from `start.sh` and `main.py` are redirected into the `log` file

## Using testenv

```
# enter the environment
source ./testenv/bin/activate

# install libs
pip install <some-software>

# start the script
python3 main.py
```