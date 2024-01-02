import sys, os, threading

class paths:
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(parent_dir, 'src')
    script_dir = os.path.join(parent_dir, 'scripts')
    archive_dir = os.path.join(parent_dir, 'archive')

    password_file = os.path.join(parent_dir, 'password.txt')
    trackers_file = os.path.join(parent_dir, 'trackers.json')

sys.path.insert(0, paths.src_dir)
from data import *
from network import *
from array import *
from plot import *

def find_trackers():
    if args.network == None:
        args.network = get_network_range()
    
    print(f'Scanning for devices in range {args.network}...')
    hosts = get_network_addresses(args.network)
    print(f'Discovered ip addresses: {hosts}')

    identified = {}
    for host in hosts:
        result = ''
        try:
            hostname = execute_ssh(host, 'admin', password, 'hostname').stdout.strip()
            print(f'Found remote hostname: {hostname} for {host}')
            identified[hostname] = host
        except Exception as e:
            print(f'Host {host} not responding')
    return identified

def execute_remotely(results, target, target_ip, username, password, command):
    print(f'Target {target} started executing')
    try:
        results[target] = execute_ssh(target_ip, username, password, command).stdout
    except Exception as e:
        results[target] = f'Error: {e}'
    print(f'Target {target} finished executing')

def main():
    # INITIALIZE

    global args, password

    args = parse_cli()
    
    if args.graph:
        data = read_file(args.input)
        print(extract_array(data))
        # plot_routes()
        exit(0)
    
    password = read_file(paths.password_file)
    scripts = get_dir_files(paths.script_dir)

    if args.list_scripts:
        print(f'Available scripts: {scripts}')
        exit(0)

    if args.script != None and args.script not in get_dir_files(paths.script_dir):
        print(f'Error: unable to find \'{args.script}\' script')
        print(f'Available scripts: {scripts}')
        exit(1)

    if not has_internet_access():
        print('Error: please connect to the internet!')
        exit(1)
    
    # DISCOVER TRACKERS

    trackers = {}
    if not args.rebuild_cache:
        try:
            trackers = read_json_file(paths.trackers_file)
        except Exception as e:
            print('Failed to load cache, attempting to rebuild')
            args.rebuild_cache = True
    if args.rebuild_cache:
        trackers = find_trackers()
    
    if not trackers:
        print('There are no known trackers, exiting.')
        exit(1)
    print(f'Found trackers: {trackers}')
    write_json_file(paths.trackers_file, trackers)

    # QUERY

    targets = trackers.keys() if args.targets == 'all' else args.targets.split()

    if args.dummy:
        print('I\'m doing nothing')
        exit(0)
    elif args.script:
        command = read_file(os.path.join(paths.script_dir, str(args.script) + '.sh'))
    elif args.command:
        command = f'cd pi-zero-tracker && {args.command}'
    
    threads = []
    results = {}
    for target in targets:
        t = threading.Thread(target=execute_remotely, args=(results, target, trackers[target], 'admin', password, command))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    for target in targets:
        print(f'{target}:')
        print(f'{results[target]}\n')

    if not os.path.exists(paths.archive_dir):
        os.makedirs(paths.archive_dir)

    with open(os.path.join(paths.archive_dir, 'output.txt'), 'w') as file:
        for target in targets:
            file.write(f'{target}:\n')
            file.write(results[target])

if __name__ == '__main__':
    main()
else:
    print('Do not run this as a module')
    exit(1)