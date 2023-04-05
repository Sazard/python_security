import nmap
import pytest
import sys

sys.path.append('src')

from tools import device_scanner
from tools import network_scanner
from tools import devices_info

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
    device = devices_info.Device_info.GetDevice(single_ip)
    tested_ports = device.port
    expected_ports = list(nmap_scan_single_ip[single_ip]['tcp'].keys())
    assert tested_ports == expected_ports

# def test_scan(nmap_scan_ip_network, ip, netmask):
#     network_scanner.scan(ip, netmask)
#     tested_devices = devices_info.Device_info.all_devices()
#     expected_devices = list(nmap_scan_single_ip.all_hosts())
#     assert tested_devices == expected_devices # et on va devoir itérer pour vérifier si les devices sont bien dedans...

# def test_network_enum(ip, netmask):
#     expected = [('host1.localdomain', None, ['192.168.0.1']), (None, None, '192.168.0.2')]
#     network_scanner.network_enum(ip, netmask)
#     devices_list = devices_info.Device_info.all_devices
#     assert devices_list == expected
