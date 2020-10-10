import argparse
import ipaddress
import pyshark
import asyncio
import time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('pcap_file', help='the path to the pcap file to dissect')
    # TODO: add filter by packet-type here
    return parser.parse_args()


def get_among_us_server_ip(capture):
    local_src_port = 0
    for packet in capture:
        if ipaddress.ip_address(packet.ip.src).is_private:
            local_src_port = packet.udp.srcport
        elif local_src_port != 0 and packet.udp.dstport == local_src_port:
            capture.reset()
            return packet.ip.addr

def main():
    args = get_args()
    capture = pyshark.FileCapture(args.pcap_file, display_filter='udp.port == 22023')
    among_us_server_ip = get_among_us_server_ip(capture)
    print(among_us_server_ip)
    capture.close()


if __name__ == "__main__":
    main()