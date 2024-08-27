from scapy.all import get_if_list

for x in get_if_list():
    print(x)
