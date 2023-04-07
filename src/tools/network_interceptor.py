import scapy.all as scapy
from scapy.all import ARP
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP
import re
from collections import deque
import time

# Initialize variables
# For brute force attack
ip_addresses = {}
queue = deque()
# Packet received detection
threshold = 50


# Create a dictionary to store the MAC-IP bindings
mac_ip_dict = {}

# Define a function to add MAC-IP bindings to the dictionary
def add_mac_ip(mac, ip):
    mac_ip_dict[mac] = ip

# Sniffing for http request with ip in uri
def http_uri(pkt):
    # Regex to analise URL
    ip_regex = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    
    # get the requested URL
    url = pkt[HTTPRequest].Host.decode() + pkt[HTTPRequest].Path.decode()
    if (ip_regex.search(url)):
        print("WARNING :\nHTTP access with ip in URL : http://",url)

# Analising packets 
def analisis(pkt):
    global ip_addresses
    # if this packet is an ARP Response
    if pkt.haslayer(ARP) and pkt[scapy.ARP].op == 2:
        src_mac = pkt[scapy.ARP].hwsrc
        src_ip = pkt[scapy.ARP].psrc
        actual_mac = mac_ip_dict.get(src_ip)
        # Checking if source mac is different from actual one
        if (src_mac != actual_mac):
            print("WARNING:\nARP poisoning detected!\nSource MAC: {}\nSource IP: {}\nActual MAC: {}"
                  .format(src_mac, src_ip, actual_mac))
    # if this packet is an HTTP Request
    elif pkt.haslayer(HTTPRequest):
        http_uri(pkt)
    # if packet has IP and TCP layer
    elif pkt.haslayer(IP) and pkt.haslayer(TCP):
        ip = pkt[IP]
        tcp = pkt[TCP]
        flags = tcp.flags
        if flags == 'FPA' or flags == 'PAU':
            # Alert on single-packet attack
            print(f"WARNING :\nSingle-packet attack detected from {ip.src} to {ip.dst}. Flags: {flags}.")
        else :
            src_ip = pkt[IP].src
            # Add source IP to dictionary and increment request count
            ip_addresses[src_ip] = ip_addresses.get(src_ip, 0) + 1
            # Add current time to queue
            queue.append(time.time())

            # Check if queue has more than 60 elements (1 minute)
            while len(queue) > 0 and queue[0] < time.time() - 60:
                # Remove elements from queue that are more than 1 minute old
                old_time = queue.popleft()
                # Decrement request count for corresponding IP
                ip_addresses[src_ip] -= 1

            # Check if request count for IP exceeds threshold
            if ip_addresses[src_ip] > threshold:
                print("WARNING :\nPossible brute force attack from", src_ip)
                # Reset counter
                ip_addresses = {}
    
def sniffing_network(ip_adress):
    # Start sniffing network traffic
    scapy.sniff(prn=analisis, filter="arp or port 80 or tcp", store=0)

    # Add MAC-IP bindings to the dictionary as they are discovered
    scapy.arping(ip_adress, verbose=0, timeout=1, retry=0, store=0, prn=add_mac_ip)



