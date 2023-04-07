#/bin/bash

pytest -v -s tests/test_network_scanner.py --single-ip 65.21.239.190 --ip 192.168.1.0 --netmask 24
