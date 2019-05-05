from threading import Thread

try:
    from conf import Config
    from censor import Censor
    import net
except ImportError:
    from heyyou.conf import Config
    from heyyou.censor import Censor
    import heyyou.net as net


def print_(mac, ssid):
    device = net.devices[mac]
    ap = net.aps[ssid]
    if not device or not ap:
        return
    thread = None
    if Censor.censor:
        thread = Thread(target=censored_wigle_thread, args=(device, ap))
    else:
        thread = Thread(target=wigle_thread, args=(device, ap))
    thread.start()


def wigle_thread(device, ap):
    brand = device.get_brand()
    str_ = ''
    if brand:
        str_ = '{} ({}) -> {}'.format(device.mac_address, brand, ap.ssid)
    else:
        str_ = '{} -> {}'.format(device.mac_address, ap.ssid)
    wigle_data = ap.get_wigle_data()  # this could take a while

    if not wigle_data:
        print(str_)
        return
    str_ += ' ({} results)'.format(wigle_data['resultCount'])
    print(str_)
    results = wigle_data['results']
    for result in results:
        str_ = '\t{},{}: '.format(result['trilat'], result['trilong'])
        country = result["country"]
        region = result["region"]
        city = result["city"]
        postalcode = result["postalcode"]
        street = result["road"]
        house_number = result["housenumber"]
        last_update = result["lastupdt"]
        str_ += '{} - {} - {} - {} - {} - {} ({})'.format(country, region, city, postalcode, street, house_number,
                                                          last_update)
        print(str_)


def censored_wigle_thread(device, ap):
    brand = Censor.brand(device.get_brand())
    str_ = ''
    if brand:
        str_ = '{} ({}) -> {}'.format(Censor.mac(device.mac_address), brand, Censor.ssid(ap.ssid))
    else:
        str_ = '{} -> {}'.format(device.mac_address, ap.ssid)
    wigle_data = ap.get_wigle_data()  # this could take a while

    if not wigle_data:
        print(str_)
        return
    str_ += ' ({} results)'.format(wigle_data['resultCount'])
    print(str_)
    results = wigle_data['results']
    for result in results:
        str_ = '\t{},{}: '.format(Censor.gps(result['trilat']), Censor.gps(result['trilong']))
        country = Censor.country(result["country"])
        region = Censor.region(result["region"])
        city = Censor.city(result["city"])
        postalcode = Censor.postalcode(result["postalcode"])
        street = Censor.road(result["road"])
        house_number = Censor.housenumber(result["housenumber"])
        last_update = result["lastupdt"]
        str_ += '{} - {} - {} - {} - {} - {} ({})'.format(country, region, city, postalcode, street, house_number,
                                                          last_update)
        print(str_)
