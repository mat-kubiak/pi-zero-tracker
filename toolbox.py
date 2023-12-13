import sys, os

class paths:
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(parent_dir, 'src')
    script_dir = os.path.join(parent_dir, 'scripts')

    password_file = os.path.join(parent_dir, 'password.txt')
    trackers_file = os.path.join(parent_dir, 'trackers.json')

sys.path.insert(0, paths.src_dir)
from data import *
from network import *

def main():
    args = parse_cli()
    password = read_password(paths.password_file)
    script_names = get_script_names(paths.script_dir)

    if not has_internet_access():
        print('Error: please connect to the internet!')
        exit(1)
    
    if args.execute != '' and args.execute not in get_script_names():
        print(f'Error: unable to find \'{args.execute}\' script')
        print(f'Available scripts: {script_names}')
        exit(1)

    tracker_ips = {}
    if not args.rebuild_cache:
        try:
            tracker_ips = read_json(paths.trackers_file)
        except Exception as e:
            print('Failed to load cache, attempting to rebuild')
            args.rebuild_cache = True

    if args.rebuild_cache:
        if args.network == '':
            args.network = get_local_range()
        print(f'Using network range: {args.network}')

        print('Scanning for devices...')
        hosts = scan_local_network(args.network)
        print(f'Discovered ip addresses: {hosts}')

        open_hosts = {}
        for host in hosts:
            result = ''
            try:
                hostname = execute_ssh(host, 'admin', password, 'hostname').stdout.strip()
                print("Found remote hostname:", hostname)
                open_hosts[hostname] = host
            except Exception as e:
                print(e)
        
        tracker_ips = open_hosts
        write_json(paths.trackers_file, open_hosts)

    if not tracker_ips:
        print('Fatal Error: could not load or discover tracker ips')
        exit(1)

    print('Tracker ips loaded successfully:')
    print(tracker_ips)

if __name__ == '__main__':
    main()
else:
    print('Do not run this as a module')
    exit(1)