import socket, nmap, fabric

def has_internet_access():
    try:
        # Create a socket connection to Google's DNS server on port 53 (DNS)
        socket.setdefaulttimeout(3)  # Set a timeout for the connection attempt
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True  # Connection successful, internet is accessible
    except socket.error:
        return False  # Connection failed, no internet access

def get_network_range():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    network_range = '.'.join(ip_address.split('.')[:-1]) + '.0/24'
    return network_range

def get_network_addresses(range):
    nm = nmap.PortScanner()
    nm.scan(hosts=range, arguments='-sn -R')
    return nm.all_hosts()

def execute_ssh(host_ip, username, password, command):
    c = fabric.Connection(host=host_ip, user=username, connect_kwargs={'password': password})
    result = c.run(command, hide=True)
    c.close()
    
    return result
