import argparse
import sys

sys.path.insert(1, 'tools')

import network_scanner

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Basic network scanner')
    parser.add_argument('--ip', metavar='ip', type=str, default='192.168.56.1', help='Host IP address')
    parser.add_argument('--netmask', metavar='netmask', type=str, default='24', help='Subnet mask')
    args = parser.parse_args()
    print("Ip :",args.ip, "| netmask :", args.netmask)

    network_scanner.scan(args.ip, args.netmask)

main()

