import sys

import requests

try:
    from conf import Config
except ImportError:
    from heyyou.conf import Config


class Wigle:
    query = 'https://api.wigle.net/api/v2/network/search'

    def __init__(self, ssid: str):
        self.data = None
        self.ssid = ssid

    def get_data(self):
        if not self.data:
            self.data = self.__retrieve_data__()
        return self.data

    def __retrieve_data__(self):
        if not Config.auth_token:
            return None
        payload = {}
        if self.ssid:
            payload["ssid"] = self.ssid
        else:
            return None
        r = None
        try:
            r = requests.get(Wigle.query, params=payload,
                             headers={'Authorization': 'Basic {}'.format(Config.auth_token)})
            return r.json()
        except:
            print("Error occured while requesting WIGLE information", file=sys.stderr)
            return None
