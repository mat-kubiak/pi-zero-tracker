import argparse, os

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
    parser.add_argument('-e', '--execute', default='', help='execute a script by name. If empty, will open the console.')
    parser.add_argument('-t', '--target', default='all', help='target hostnames separated by spaces. \'all\' by default, targets all found trackers.')
    parser.add_argument('-n', '--network', default='', help='network ip range to scan for trackers.')
    args = parser.parse_args()
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
