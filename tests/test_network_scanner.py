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
    nm = nmap.PortScanner()
    nm.scan(single_ip, '0-4096')
    return nm

@pytest.fixture(scope='session')
def nmap_scan_ip_network(ip, netmask):
    subnet = ip + "/" + netmask
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments="-p0-4096")
    return nm

def test_scan_single_ip(nmap_scan_single_ip, single_ip):
    network_scanner.scan_single_ip(single_ip)
    device_scanner.scan()
    device = devices_info.Device_info.GetDevice(single_ip)
    # Filter the list of open ports
    expected_ports = [int(port) for port, info in nmap_scan_single_ip[single_ip]['tcp'].items() if info['state'] == 'open']
    assert device.port == expected_ports

def test_scan(nmap_scan_ip_network, ip, netmask):
    network_scanner.scan(ip, netmask)
    device_scanner.scan()
    found_devices = [device.ip for device in devices_info.all_devices]
    expected_devices = list(nmap_scan_ip_network.all_hosts())
    # Check if each item of 'expected_devices' is present in the list 'found_devices'
    assert all(host in found_devices for host in expected_devices)
