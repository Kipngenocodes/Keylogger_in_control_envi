from scapy.all import ARP, Ether, srp
# import ipaddress

def network_scanner(ip_range):
    """
    Scans the given IP range to identify active hosts.

    :param ip_range: The IP range to scan, e.g., '192.168.1.0/24'
    """
    # Create an ARP(address resolution protocol) request
    arp_request = ARP(pdst=ip_range)
    # Create an Ethernet frame to broadcast the ARP request
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the Ethernet frame with the ARP request
    arp_request_broadcast = broadcast / arp_request

    # Send the ARP request and capture responses
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Extract and display the IP and MAC addresses of active hosts
    print("Active Hosts:")
    print("IP Address\t\tMAC Address")
    print("-" * 40)
    for sent, received in answered_list:
        print(f"{received.psrc}\t\t{received.hwsrc}")


if __name__ == "__main__":
    # Specify the IP range to scan
    ip_range = "192.168.1.0/24"
    network_scanner(ip_range)
