import nmap
import pytest
import sys

sys.path.append('src')

from tools import device_scanner
from tools import network_scanner
from tools import devices_info
from tools import device_scanner

@pytest.fixture(scope='session')
def nmap_scan_single_ip(single_ip):
    """
    Perform a single IP Nmap scan on the provided IP address.

    :param single_ip: The IP address to be scanned.
    :type single_ip: str
    :return: nmap.PortScanner
    """
    nm = nmap.PortScanner()
    nm.scan(single_ip, '0-4096')
    return nm

@pytest.fixture(scope='session')
def nmap_scan_ip_network(ip, netmask):
    """
    Perform an IP network Nmap scan on the provided IP address and netmask.

    :param ip: The IP address to be scanned.
    :type ip: str
    :param netmask: The netmask for the IP address.
    :type netmask: str
    :return: nmap.PortScanner
    """
    subnet = ip + "/" + netmask
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments="-p0-4096")
    return nm

def test_scan_single_ip(nmap_scan_single_ip, single_ip):
    """
    Test the scan_single_ip() function from the network_scanner module.

    :param nmap_scan_single_ip: The nmap_scan_single_ip fixture.
    :param single_ip: The IP address to be scanned.
    :type single_ip: str
    :return: None
    """
    network_scanner.scan_single_ip(single_ip)
    device_scanner.scan()
    device = devices_info.DeviceInfo.getDevice(single_ip)
    # Filter the list of open ports
    expected_ports = [int(port) for port, info in nmap_scan_single_ip[single_ip]['tcp'].items() if info['state'] == 'open']
    assert device.ports == expected_ports

def test_network_enum(nmap_scan_ip_network, ip, netmask):
    """
    Test the network_enum() with the scan() function from the network_scanner module.

    :param nmap_scan_ip_network: The nmap_scan_ip_network fixture.
    :param ip: The IP address to be scanned.
    :type ip: str
    :param netmask: The netmask for the IP address.
    :type netmask: str
    :return: None
    """
    network_scanner.scan(ip, netmask)
    device_scanner.scan()
    found_devices = [device.ip for device in devices_info.all_devices]
    expected_devices = list(nmap_scan_ip_network.all_hosts())
    # Check if each item of 'expected_devices' is present in the list 'found_devices'
    assert all(host in found_devices for host in expected_devices)

def test_scan_multiple_ip(nmap_scan_single_ip, ip, netmask):
    """
    Test the scan_multiple_ip() function from the network_scanner module.

    :param nmap_scan_single_ip: The nmap_scan_single_ip fixture.
    :param ip: The IP address to be scanned.
    :type ip: str
    :param netmask: The netmask for the IP address.
    :type netmask: str
    :return: None
    """
    network_scanner.scan(ip, netmask)
    device_scanner.scan()
    found_devices = [device.ip for device in devices_info.all_devices]
    for d_ip in found_devices:
        test_scan_single_ip(nmap_scan_single_ip, d_ip)