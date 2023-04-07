#/bin/bash

pytest -v -s tests/test_network_scanner.py --single-ip 172.18.1.2 --ip 172.18.1.0 --netmask 24
