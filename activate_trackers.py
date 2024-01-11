import sys, os, threading, fabric

sys.path.insert(0, 'src')
from data import *
from scripts import *

run_duration = 30
whitelist = 'iNode_Bacon iNode_Eggs iNode_Bread'

def execute_remotely(results, target, target_ip, password, command):
    print(f'Target {target} started executing')
    try:
        c = fabric.Connection(host=target_ip, user='admin', connect_kwargs={'password': password})
        output = c.run(command, hide=True)
        c.close()
        results[target] = output.stdout
    except Exception as e:
        results[target] = f'Error: {e}'
    print(f'Target {target} finished executing')

def main():
    
    # INITIALIZE
    password = read_file('password.txt')
    trackers = read_json_file('trackers.json')
    targets = trackers.keys()

    command = f'''cd pi-zero-tracker
if [ -f "beacon_data.txt" ]; then
    echo "" >> "archive.txt"
    cat "beacon_data.txt" >> "archive.txt"
    rm -f "beacon_data.txt"
fi
sudo python3 tracker.py -d {run_duration} -w "{whitelist}"'''

    # RUN
    threads = []
    results = {}
    for target in targets:
        t = threading.Thread(target=execute_remotely, args=(results, target, trackers[target], password, command))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
    
    for target in targets:
        print(f'{target}:')
        print(f'{results[target]}\n')

if __name__ == '__main__':
    main()