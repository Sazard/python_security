from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import argparse
import subprocess
from tools import devices_info

def is_alive(ip):
    # Use ping to check if IP is alive
    command = ['ping', '-c', '1', '-W', '0.5', ip]
    # print("testing alive: ", ip)
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def network_enum(ip, netmask):
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
            # print("testing: ", host)
            hostname, alias, addresslist = socket.gethostbyaddr(address)
            print("Is alive: ", host)
            devices_info.Device_info.AddDevice(addresslist[0],alias,hostname[0])
        except socket.herror:
            if is_alive(address):
                print("Is alive: ", host)
                hostname = None
                alias = None
                addresslist = address
                devices_info.Device_info.AddDevice(addresslist,alias,hostname)



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
    network_enum(ip, netmask)

def scan_single_ip(ip):
    # Scanning network and creating list with results
   network_enum(ip, '32')
