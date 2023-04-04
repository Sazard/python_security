from scapy.all import *
from time import sleep

# Define a packet handler function
def handle_packet(packet):
    # Analyze the packet and search for suspicious activity
    print(packet.show())
    sleep(0.5)

def sniffing_network(): 
    # Start sniffing packets on the network
    sniff(prn=handle_packet)