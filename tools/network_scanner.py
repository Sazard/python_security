from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import argparse

def network_enum():
    devices = []
    for host in range(5):
        address = "192.168.56." + str(host)
        socket.setdefaulttimeout(0.5)

        try:
            hostname, alias, addresslist = socket.gethostbyaddr(address)
            devices.append((hostname, alias, addresslist))
        except socket.herror:
            hostname = None
            alias = None
            addresslist = address

        print(addresslist, '=>', hostname)
    return devices

def scan(ip, netmask):
    # Check if subnet mask is valid
    try:
        subnet_mask = int(netmask)
        if subnet_mask < 0 or subnet_mask > 32:
            raise argparse.ArgumentTypeError('Subnet mask must be between 0 and 32')
    except ValueError:
        raise argparse.ArgumentTypeError('Subnet mask must be an integer')

    # Calculate target IP address range
    host_network = ipaddress.IPv4Network(ip + '/' + netmask, strict=False)
    target_ip = str(host_network.network_address) + '/' + str(host_network.prefixlen)

    # Scanning network and creating list with results
    devices = network_enum()

    return devices
