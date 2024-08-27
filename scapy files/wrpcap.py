from scapy.all import sniff, wrpcap

packets = []
def packet_sniffer(packet):
    packets.append(packet)
    print(packet.summary())

sniff(iface="\\Device\\NPF_Loopback", count=0, prn=packet_sniffer)
wrpcap('packets.pcap', packets)
