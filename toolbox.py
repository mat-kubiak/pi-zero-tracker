import sys, os
from fabric import Connection

class paths:
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(parent_dir, 'src')
    password_file = os.path.join(parent_dir, 'password.txt')
    script_dir = os.path.join(parent_dir, 'scripts')

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

if __name__ == '__main__':
    main()
else:
    print('Do not run this as a module')
    exit(1)