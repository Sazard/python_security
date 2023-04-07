import argparse
import sys

sys.path.insert(1, 'tools')

from tools import network_scanner
from tools import device_scanner
from tools import network_interceptor
from tools import devices_info

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Basic network scanner')
    parser.add_argument('-i', '--ip', metavar='ip', type=str, default='192.168.56.1', help='Host IP address')
    parser.add_argument('-n', '--netmask', metavar='netmask', type=str, default='24', help='Subnet mask')
    parser.add_argument('-1', '--single-ip', metavar='single_ip', type=str, help='Single IP address to scan')
    parser.add_argument('-f', '--output-format', metavar='output_format', type=str, choices=['json', 'csv', 'html'], default='html', help='Output format')
    parser.add_argument('-a', '--analyse', metavar='analyse', type=str, help='Analyse network traffic')
    args = parser.parse_args()

    if args.analyse:
        results = network_interceptor.sniffing_network(str(args.ip) + '/' + str(args.netmask))
    elif args.single_ip:

        print("IP:",args.single_ip, "| netmask: 32")

        # Scan single IP address
        network_scanner.scan_single_ip(args.single_ip)
        device_scanner.scan()
        device_scanner.create_report(args.output_format)

    else:

        print("IP:",args.ip, "| netmask:", args.netmask)

        # For debug
        #devices = [('DESKTOP-IJ3JO0K', [], ['192.168.56.1'])]
        #print(devices)

        network_scanner.scan(args.ip, args.netmask)

        # For debug
        #scan_result = {'192.168.56.1': ['DESKTOP-IJ3JO0K', 135, 139]}
        #print(scan_result)

        device_scanner.scan()
        device_scanner.create_report(args.output_format)
