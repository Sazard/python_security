import pytest
import sys

sys.path.insert(1, 'src/tools')

from tools import network_scanner
from tools import device_scanner

def test_network_enum():
    expected = [('host1.localdomain', None, ['192.168.0.1']), (None, None, '192.168.0.2')]
    assert network_scanner.network_enum('192.168.1.254', '24') == expected

def test_scan():
    expected = [('host1.localdomain', None, ['192.168.0.1']), (None, None, '192.168.0.2')]
    assert network_scanner.scan('192.168.1.254', '24') == expected
