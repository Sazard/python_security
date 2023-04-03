import argparse
import sys

sys.path.insert(1, 'tools')

from tools import network_scanner
from tools import device_scanner

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Basic network scanner')
    parser.add_argument('--ip', metavar='ip', type=str, default='192.168.56.1', help='Host IP address')
    parser.add_argument('--netmask', metavar='netmask', type=str, default='24', help='Subnet mask')
    args = parser.parse_args()
    print("Ip :",args.ip, "| netmask :", args.netmask)

    devices = network_scanner.scan(args.ip, args.netmask)
    
    # For debug
    #devices = [('DESKTOP-IJ3JO0K', [], ['192.168.56.1'])]
    #print(devices)
    
    scan_result = device_scanner.scan(devices)
    
    # For debug
    #scan_result = {'192.168.56.1': ['DESKTOP-IJ3JO0K', 135, 139]}
    #print(scan_result)
    
    device_scanner.create_report(scan_result)
