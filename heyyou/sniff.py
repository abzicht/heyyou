from scapy.all import Dot11, sniff

try:
    from conf import Config
except ImportError:
    from heyyou.conf import Config


class Sniff:

    def __init__(self):
        self.callback = None

    def start(self, *callback):
        self.callback = callback
        sniff(iface=Config.interface, prn=self.handle_packets)

    def handle_packets(self, packet):
        # Handle Probe Requests
        if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 4:
            ssid = packet.info.decode("ascii")
            mac = packet.addr2
            for callback_ in self.callback:
                callback_(mac, ssid)
