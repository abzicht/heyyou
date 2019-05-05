import xml.etree.ElementTree
from os import path
from pathlib import Path


class Mac:
    file_path = path.join(str(Path.home()), '.heyyou/mac_vendors.xml')

    def __init__(self):
        self.mac_map = {}
        self.__init_mac_file__()

    def __init_mac_file__(self):
        root = xml.etree.ElementTree.parse(Mac.file_path).getroot()
        for child in root.getchildren():
            mac = str.upper(child.get("mac_prefix"))
            self.mac_map[mac] = child.get("vendor_name")

    def find_vendor(self, mac_address) -> str:
        u_mac_address = str.upper(mac_address)
        if u_mac_address in self.mac_map.keys():
            return self.mac_map[u_mac_address]

        for i in range(len(u_mac_address)):
            if i % 3 == 0:
                # The list does not have prefixes ending with ':' so we can skip those
                continue
            cut_u_mac_address = u_mac_address[:-1 * (i + 1)]
            if cut_u_mac_address in self.mac_map.keys():
                return self.mac_map[cut_u_mac_address]

        return None
