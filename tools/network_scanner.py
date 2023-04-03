from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import argparse
import subprocess

def is_alive(ip):
    # Use ping to check if IP is alive
    command = ['ping', '-c', '1', '-W', '0.400', ip]
    print("testing: ", ip)
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def network_enum(ip, netmask):
    devices = []
    # Check if subnet mask is valid
    try:
        subnet_mask = int(netmask)
        if subnet_mask < 0 or subnet_mask > 32:
            raise argparse.ArgumentTypeError(
                'Subnet mask must be between 0 and 32')
    except ValueError:
        raise argparse.ArgumentTypeError('Subnet mask must be an integer')

    # Calculate target IP address range
    host_network = ipaddress.IPv4Network(ip + '/' + netmask, strict=False)

    for host in host_network.hosts():
        address = str(host)
        socket.setdefaulttimeout(0.5)

        
        try:
            hostname, alias, addresslist = socket.gethostbyaddr(address)
            devices.append((hostname, alias, addresslist))
        except socket.herror:
            if is_alive(address):
                hostname = 'Host-' + address
                alias = 'Alias-' + address
                addresslist = address
                devices.append((hostname, alias, addresslist))

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
    devices = network_enum(ip, netmask)

    return devices

def scan_single_ip(ip):
    # Scanning network and creating list with results
    devices = network_enum(ip, '32')
    return devices
