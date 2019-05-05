import json

try:
    from conf import Config
    import net
except ImportError:
    from heyyou.conf import Config
    import heyyou.net as net


def summarize():
    devices: dict = {}
    for mac in net.devices:
        device = net.devices[mac]
        brand = device.get_brand()
        aps: dict = {}
        for ap_key in device.aps:
            ap = device.aps[ap_key]
            ssid = ap.ssid
            wigle_data = ap.get_wigle_data()
            aps[ssid] = wigle_data

        devices[device.mac_address] = {
            "brand": brand,
            "aps": aps
        }
    with open(Config.summary, 'w') as file_:
        json.dump(devices, file_, indent=4, sort_keys=True)
