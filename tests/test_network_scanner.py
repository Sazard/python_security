import nmap
import pytest
import sys

sys.path.append('src')

from tools import device_scanner
from tools import network_scanner

@pytest.fixture
def nm():
    nm = nmap.PortScanner()
    nm.scan('192.168.1.254', '0-4096')
    return nm

def test_scan_single_ip(nm):
    result = network_scanner.scan_single_ip('192.168.1.254')
    assert result == list(nm['192.168.1.254']['tcp'].keys())

def test_network_enum():
    expected = [('host1.localdomain', None, ['192.168.0.1']), (None, None, '192.168.0.2')]
    assert network_scanner.network_enum('192.168.1.254', '24') == expected

def test_scan():
    expected = [('host1.localdomain', None, ['192.168.0.1']), (None, None, '192.168.0.2')]
    assert network_scanner.scan('192.168.1.254', '24') == expected
