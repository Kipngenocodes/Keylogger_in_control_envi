from scapy.all import rdpcap

# Read the packets from the 'packets.pcap' file
packets = rdpcap('packets.pcap')

# Iterate over the packets and process them
for packet in packets:
    print(packet.summary())
    # You can also analyze or manipulate the packet data here
