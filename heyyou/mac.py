import xml.etree.ElementTree


class Mac:

    def __init__(self, file_path):
        self.mac_map = {}
        self.__init_mac_file__(file_path)

    def __init_mac_file__(self, file_path):
        root = xml.etree.ElementTree.parse(file_path).getroot()
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
