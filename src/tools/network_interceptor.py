import scapy.all as scapy

# Create a dictionary to store the MAC-IP bindings
mac_ip_dict = {}

# Define a function to add MAC-IP bindings to the dictionary
def add_mac_ip(mac, ip):
    mac_ip_dict[mac] = ip

# Define a function to check for ARP poisoning
def check_poisoning(pkt):
    if pkt[scapy.ARP].op == 2:  # ARP response
        if pkt[scapy.ARP].hwsrc != mac_ip_dict.get(pkt[scapy.ARP].psrc):
            print("ARP poisoning detected! Source MAC: " + str(pkt[scapy.ARP].hwsrc) +
                  " IP: " + str(pkt[scapy.ARP].psrc) +
                  " Actual MAC: " + str(mac_ip_dict.get(pkt[scapy.ARP].psrc)))

def sniffing_network(ip_adress):
    # Start sniffing network traffic
    scapy.sniff(prn=check_poisoning, filter="arp", store=0)

    # Add MAC-IP bindings to the dictionary as they are discovered
    scapy.arping(ip_adress, verbose=0, timeout=1, retry=0, store=0, prn=add_mac_ip)


