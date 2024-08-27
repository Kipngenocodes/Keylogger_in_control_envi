#  This program will use scapy to create packet sniffer

# importing the scapy module
from scapy.all import sniff

# Using a function to process the packets 
def packet_sniffer(packet):
    
    print(packet.summary())
    
    print(packet.show())
# start sniffing 
sniff(iface ="\\Device\\NPF_Loopback", count =0, prn = packet_sniffer)