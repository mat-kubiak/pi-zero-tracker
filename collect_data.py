import sys, os, threading
from fabric import *

sys.path.insert(0, 'src')
from data import *

def main():
    
    # INITIALIZE
    password = read_file('password.txt')
    trackers = read_json_file('trackers.json')
    targets = trackers.keys()
    command = 'cd pi-zero-tracker && cat beacon_data.txt'

    # RUN
    results = {}
    for target in targets:
        c = Connection(host=trackers[target], user='admin', connect_kwargs={'password': password})
        results[target] = c.run(command, hide=True).stdout.strip()
        c.close()
        print(f'{target} data collected')

    text = ''
    for target in targets:
        text += f'{target}:\n{results[target]}\n'

    with open('output1.txt', 'w') as file:
        file.write(text)

if __name__ == '__main__':
    main()