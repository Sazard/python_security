import scapy.all as scapy
from scapy.all import ARP
from scapy.layers.http import HTTPRequest
import re

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
    # if this packet is an ARP Response
    if pkt.haslayer(ARP) and pkt[scapy.ARP].op == 2:
        if pkt[scapy.ARP].hwsrc != mac_ip_dict.get(pkt[scapy.ARP].psrc):
            print("WARNING :\nARP poisoning detected! Source MAC: " + str(pkt[scapy.ARP].hwsrc) +
                  "\nIP: " + str(pkt[scapy.ARP].psrc) +
                  "\nActual MAC: " + str(mac_ip_dict.get(pkt[scapy.ARP].psrc)))
    # if this packet is an HTTP Request
    elif pkt.haslayer(HTTPRequest):
        http_uri(pkt)
    
def sniffing_network(ip_adress):
    # Start sniffing network traffic
    scapy.sniff(prn=analisis, filter="arp or port 80", store=0)

    # Add MAC-IP bindings to the dictionary as they are discovered
    scapy.arping(ip_adress, verbose=0, timeout=1, retry=0, store=0, prn=add_mac_ip)



