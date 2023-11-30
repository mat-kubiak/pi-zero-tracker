import os
import socket

class info:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile_path = os.path.join(script_dir, 'log')

    hostname = socket.gethostname()
    hostname = 'rasp12345' # uncomment to mimic pi (if not testing!!)
    host_number = int(hostname[4:])

def main():
    print('Hello from Raspberry Pi Zero no.{}!'.format(info.host_number))

if __name__ == '__main__':
    main()