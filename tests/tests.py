import pytest
import sys

import network_scanner_test

sys.path.insert(1, 'src/tools')

from tools import network_scanner
from tools import device_scanner

if __name__ == '__main__':
    network_scanner_test.test_network_enum()
    network_scanner_test.test_scan()
