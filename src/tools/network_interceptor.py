import scapy.all as scapy
from time import sleep

# code to get MAC Address
def mac(ipadd):
  # requesting arp packets from the IP address
  # if it's wrong then will throw error
    arp_request = scapy.ARP(pdst=ipadd)
    br = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_br = br / arp_request
    list_1 = scapy.srp(arp_req_br, timeout=5,
                       verbose=False)[0]
    return list_1[0][1].hwsrc

# defining function to process sniffed packet
def process_sniffed_packet(packet):
  # if it is an ARP packet and if it is an ARP Response
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
 
       # originalmac will get old MAC whereas
        originalmac = mac(packet[scapy.ARP].psrc)
        # responsemac will get response of the MAC
        responsemac = packet[scapy.ARP].hwsrc

# Analyze the packet and search for suspicious activity
def handle_packet(interface):
    if interface == "":
        # Sniff all interfaces
        # Set store to False for long time running less memory eating
        scapy.sniff(store=False,
                    prn=process_sniffed_packet)
    else :
        scapy.sniff(iface=interface, store=False,
                    prn=process_sniffed_packet)


def sniffing_network(interface):
    print("Sniffing ...")
    # Start sniffing packets on the network
    handle_packet(interface)