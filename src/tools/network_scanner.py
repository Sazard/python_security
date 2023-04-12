from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import argparse
import subprocess
from tools import devices_info

def is_alive(ip):
    """
    Checks if the given IP address is alive by sending a ping request.

    Args:
        ip (str): The IP address to check.

    Returns:
        bool: True if the IP address is alive, False otherwise.
    """
    # Use ping to check if IP is alive
    command = ['ping', '-c', '1', '-W', '0.5', ip]
    # print("testing alive: ", ip)
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def network_enum(ip, netmask):
    """
    Enumerates all devices on the given IP address range and adds information about them to a list.

    Args:
        ip (str): The IP address to scan.
        netmask (int): The subnet mask for the IP address range, as an integer between 0 and 32.

    Returns:
        None
    """
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
            devices_info.DeviceInfo.addDevice(addresslist[0],alias,hostname[0])
        except socket.herror:
            if is_alive(address):
                print("Is alive: ", host)
                hostname = None
                alias = None
                addresslist = address
                devices_info.DeviceInfo.addDevice(addresslist,alias,hostname)



def scan(ip, netmask):
    """
    Scans the IP address range specified by `ip` and `netmask`, and adds information about each device to the `DeviceInfo` list in the `devices_info` module.

    This function first checks if the subnet mask is valid. It then calculates the target IP address range and iterates through all the IP addresses in that range. For each IP address, it calls the `network_enum` function to add information about the device to the `DeviceInfo` list.

    Args:
        ip (str): The IP address to scan.
        netmask (int): The subnet mask for the IP address range, as an integer between 0 and 32.

    Returns:
        None
    """
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
    """
    Scans a single IP address and adds information about the device to the `DeviceInfo` list in the `devices_info` module.

    This function calls the `network_enum` function to add information about the device to the `DeviceInfo` list.

    Args:
        ip (str): The IP address to scan.

    Returns:
        None
    """
    # Scanning network and creating list with results
    network_enum(ip, '32')
