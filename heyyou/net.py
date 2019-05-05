"""
Device and AP can be modeled as a net where
devices and aps are vertices. Each vertex of one type can
only be adjacent to a vertex that is not of the same type.

Devices are to be connected to APs when they searched for
that AP
"""

try:
    from conf import Config
    from wigle import Wigle
except ImportError:
    from heyyou.conf import Config
    from heyyou.wigle import Wigle


def add(mac: str, ssid: str) -> bool:
    new = False
    if mac not in devices:
        new = True
    if ssid not in aps:
        new = True
    device = Device.get_device(mac)
    ap = AP.get_ap(ssid)
    device.add_ap(ap)
    return new


devices: dict = {}
aps: dict = {}


class Device:

    def __init__(self, mac_address: str):
        self.mac_address = mac_address
        self.aps = {}

    def add_ap(self, ap):
        if ap.ssid not in self.aps:
            self.aps[ap.ssid] = ap
            ap.add_device(self)

    def get_mac(self) -> str:
        return self.mac_address

    def get_brand(self) -> str:
        if Config.mac:
            return Config.mac.find_vendor(mac_address=self.mac_address)
        else:
            return None

    @staticmethod
    def get_device(mac_address: str):
        if mac_address in devices:
            return devices[mac_address]
        else:
            dev = Device(mac_address)
            devices[mac_address] = dev
            return dev

    def __str__(self):
        str_ = self.mac_address
        str_ += '\n'
        for ap in self.aps:
            str_ += '\t' + str(ap) + '\n'
        return str_


class AP:

    def __init__(self, ssid: str):
        self.ssid = ssid
        self.devices = {}
        self.wigle = Wigle(ssid=ssid)

    def add_device(self, device: Device):
        if device.mac_address not in self.devices:
            self.devices[device.mac_address] = device
            device.add_ap(self)

    def get_wigle_data(self):
        return self.wigle.get_data()

    @staticmethod
    def get_ap(ssid: str):
        if ssid in aps:
            return aps[ssid]
        else:
            ap = AP(ssid)
            aps[ssid] = ap
            return ap

    def __str__(self):
        str_ = self.ssid
        str_ += '\n'
        str_ += str(self.get_wigle_data())
        return str_
