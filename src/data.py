import argparse, os, json

def read_password(path):
    password = ''
    if not os.path.exists(path):
        print('Error: \'{path}\' file missing!')
        exit(1)
    with open(path, 'r') as file:
        password = file.read().strip()
    if password == '':
        print('Error: password cannot be empty!')
        exit(1)
    return password

def parse_cli():
    parser = argparse.ArgumentParser(
        prog='toolbox',
        description='Command utility to control pi trackers in the local network.')
    parser.add_argument('-e', '--execute', default='', help='execute a script by name, normally found in the \'scripts\' directory. If empty, will open the console.')
    parser.add_argument('-c', '--command', default='', help='the command to execute on targets. Will overwrite the --execute argument.')
    parser.add_argument('-t', '--target', default='all', help='target hostnames separated by spaces. \'all\' by default, targets all found trackers.')
    parser.add_argument('-n', '--network', default='', help='network ip range to scan for trackers.')
    parser.add_argument('-r', '--rebuild_cache', action='store_true', help='attempts to rebuild tracker ip cache, stored in the \'trackers.json\' file.')
    args = parser.parse_args()

    if args.command != '':
        args.execute = ''

    return args

def get_script_names(path):
    script_files = []
    for file_name in os.listdir(path):
        # Check if the path is a file (not a directory)
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and not file_path in script_files:
            root, extension = os.path.splitext(file_name)
            script_files.append(root)
    return script_files

def loadFile(path):
    text = ''
    with open(path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        text += line
    return text

def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def write_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)