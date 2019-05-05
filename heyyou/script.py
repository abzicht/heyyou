import argparse
import sys

try:
    from conf import Config
    from sniff import Sniff
    from censor import Censor
    import wifi
    import net
    import summary
    import verbose
except ImportError:
    from heyyou.conf import Config
    from heyyou.sniff import Sniff
    from heyyou.censor import Censor
    from heyyou import wifi
    import heyyou.net as net
    import heyyou.summary as summary
    import heyyou.verbose as verbose


def callback(mac, ssid):
    is_new = net.add(mac, ssid)
    if is_new:
        verbose.print_(mac, ssid)


def main():
    parser = argparse.ArgumentParser(description="""Sniff for SSIDs and determine their potential physical location.
    To stop sniffing, send SIGINT to the process.""", epilog="""When using wigle, data is printed out in the following
format: {latitude},{longitude}: {country} - {region} - {city} - {postalcode} - {street} - {house number} ({last update})
""")
    parser.add_argument('interface', metavar='INTERFACE', type=str,
                        help="the wifi interface to use (must be capable of monitor mode")
    parser.add_argument('-c', '--censor', dest='censor', action='store_true',
                        help="censor SSIDs, MAC addresses, and any other sensitive information")
    parser.add_argument('-w', '--wigle-auth', dest='auth_token', type=str, help="the auth code used for the wigle api")
    parser.add_argument('-m', '--mac-vendors', dest='mac_vendors', action='store_true',
                        help="use a MAC to brand mapping to print the devices' brands")
    parser.add_argument('-s', '--summary', dest='summary', help="store all results to this json file")
    args = parser.parse_args()
    Config(args)
    try:
        wifi.monitor()
    except AssertionError:
        print("Switching wifi interface {} to monitor mode not possible, exiting".format(Config.interface),
              file=sys.stderr)
        __cleanup__()

    sniff = Sniff()
    try:
        sniff.start(callback)
    except KeyboardInterrupt:
        pass
    if Config.summary:
        summary.summarize()
    __cleanup__()


def __cleanup__():
    try:
        wifi.managed()
    except AssertionError:
        print("""Switching wifi interface {} to managed mode not possible.
Perform this task manually to be able to use the interface again""".format(Config.interface), file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
