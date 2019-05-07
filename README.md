# DISCLAIMER
ONLY USE THIS TOOL ON YOURSELF OR PEOPLE THAT EXPLICITLY ALLOWED
YOU TO. THIS TOOL IS CAPABLE OF TRACKING PEOPLES' HOMES AND PLACES
THEY VISIT OR HAVE VISITED IN THE PAST.
DO NOT USE THIS TOOL WHEN NEAR SOMEONE ELSE'S WIRELESS DEVICE UNLESS
YOU ARE ALLOWED TO BY THAT PERSON.
DO NOT USE THIS TOOL IN A CROWDED AREA WHERE YOU ARE UNCERTAIN WHETHER
YOU COULD UNINTENTIONALLY SCAN FOREIGN DEVICES.
THIS TOOL MERELY IS A DEMONSTRATION OF THE POSSIBILITIES THAT COME WITH
THE KNOWLEDGE OF SSIDS.
YOU ARE COMPLETELY LIABLE FOR ANY (LEGAL) CONSEQUENCES WHEN USING THIS TOOL.
THE AUTHOR CAN NEITHER BE HELD RESPONSIBLE NOR CHARGED IN ANY WAY FOR YOUR ACTIONS AND
YOUR USE OF THIS TOOL. 

THIS TOOL IS OPEN SOURCE - THIS MEANS THAT YOU KNOW WHAT YOU ARE DOING WHEN RUNNING
THIS TOOL.

FOR MORE INFORMATION, READ THE [LICENSE](./LICENSE).

# hey, you!
__heyyou__ is a tool for sniffing WiFi probe requests, filtering out
the requested SSIDs and determining the physical locations of the access points
those SSIDs map to.

This tool is intended for demonstration purposes only, showing unaware audiences the risks
that come with

* easily identifiable SSIDs,
* leaving a phone's / laptop's WiFi powered on when in public.


## Installation

```bash
git clone https://github.com/abzicht/heyyou
cd heyyou
python3 setup.py install
```

## Requirements
* Your pc must have a wireless interface that supports [monitor mode](https://en.wikipedia.org/wiki/Monitor_mode).
* `ip`, `iw`, need to be installed
* You need an auth code for the [Wigle](https://wigle.net) api

## Running heyyou

### Pure sniff
Only sniff for SSIDs, do not search for physical locations:

```
heyyou wlp2s0
```

If you do not know your WiFi interface's name (something like `wlp2s0`), here is how you can obtain it:
```bash
# this prints out all WiFi interfaces connected to your pc
iw dev

# this command uses some unix magic to determine the first WiFi interface
# in the list and automatically use it for heyyou:
iw dev | grep -m 1 Interface | cut -d ' ' -f 2 | xargs heyyou
```

### Sniff and evaluation
Sniff for SSIDs and search for the physical locations of access points using the Wigle api with the help
of the authtoken.

```bash
heyyou -w <authtoken> wlp2s0
```

If you do not want to see your authtoken in the shell history, use some UNIX magic:

```bash
cat authtoken.txt | xargs heyyou wlp2s0 -w
```
This assumes, of course, that your exact authtoken is stored in `authtoken.txt`.

You find your authtoken [here](https://wigle.net/account).

### Sniff and brand evaluation
Wireless devices send their MAC address in most WiFi frames. You can utilize Cisco's MAC vendor list to
determine the brands of the sniffed devices. This helps in identifying which device searched for which SSID.

```bash
heyyou -m mac_vendors.xml wlp2s0
```

This assumes that the file `./mac_vendors.xml` contains Cisco's MAC vendor list.

If that is not the case, here is how you can obtain it:

```bash
curl https://macaddress.io/database/macaddress.io-db-cisco-vendor.xml > ./mac_vendors.xml
```

### Demonstration
When demonstrating this tool to an audience (that previously agreed on this _attack_), it would
be nice to NOT print out the audience's postal addresses and more. For that purpose, use the `-c` flag
to censor the most sensitive information:

```bash
heyyou -m mac_vendors.xml -c -w <authtoken> wlp2s0
```

### Summary
The tool prints out most (not all) retrieved information _on the fly_. Add the `-s` flag to store __all__ information
in a neat json file.
```bash
heyyou -s heyyou.json wlp2s0
```

### The all in one command

The following command automatically determines the WiFi interface to use, the authtoken to use for Wigle,
and translates MAC addresses to brand names. All information is printed to stdout, sensitive information
is censored, a summary is stored as `heyyou.json`.
```bash
heyyou -w $(cat authtoken.txt) \
       -m mac_vendors.xml -c \
       -s heyyou.json \
       $(iw dev | grep -m 1 Interface | cut -d ' ' -f 2)
```

# Output
As soon as a device searching for WiFi is found, its MAC address and SSID it searches for are output to stdout.  
Assuming the MAC address is `00:00:00:00:00:00` and the AP's SSID is `MyWiFi`, the output looks like this:

```text
00:00:00:00:00:00 -> MyWiFi
```

When a MAC-Vendor list was specified and the MAC address resolves to a valid vendor, the output also contains
the vendor's name:

```text
00:00:00:00:00:00 ({vendor}) -> MyWiFi
```

When using the Wigle API functionality, Wigle's response to the SSID is added.  
Assuming that Wigle found `30` matches for the SSID `MyWiFi`, the number of entries would
be appended to the SSID and all 30 entries would be appended line by line.

```text
00:00:00:00:00:00 -> MyWiFi (30 results)
    {latitude},{longitude}: {country} - {region} - {city} - {postalcode} - {street} - {house number} ({last update})
```

Wigle limits the number of results being sent for one request. Only the top 100 entries are returned and therefore
there are never more than 100 rows being printed out for one SSID.
