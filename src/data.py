import argparse, os, json

def parse_cli():
    parser = argparse.ArgumentParser(
        prog='toolbox.py',
        description='Command-line utility for controlling bluetooth trackers in the local network.',
        add_help=False)
    
    ops = parser.add_argument_group('Remote Operations').add_mutually_exclusive_group()
    ops.required = True
    ops.add_argument('-s', '--script', help='Execute a script by name, normally found in the \'scripts\' directory.')
    ops.add_argument('-c', '--command', help='Executes a custom command.')
    ops.add_argument('-d', '--dummy', action='store_true', help='Do nothing.')

    opts = parser.add_argument_group('Options')
    opts.add_argument('-t', '--targets', action='append', default='all', help='Target hostnames separated by spaces. \'all\' by default, targets all found trackers.')
    opts.add_argument('-n', '--network', help='Overwrites network ip range used for scaning for trackers.')

    opts.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    opts.add_argument('-l', '--list_scripts', action='store_true', help='List all available scripts and exit.')
    opts.add_argument('-r', '--rebuild_cache', action='store_true', help='Forces to rebuild tracker ip cache, stored in the \'trackers.json\' file.')

    args = parser.parse_args()
    return args

def get_dir_files(path):
    script_files = []
    for file_name in os.listdir(path):
        # Check if the path is a file (not a directory)
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and not file_path in script_files:
            root, extension = os.path.splitext(file_name)
            script_files.append(root)
    return script_files

def read_file(path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

    text = ''
    for line in lines:
        text += line
    return text

def read_json_file(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
    return data

def write_json_file(path, data):
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)