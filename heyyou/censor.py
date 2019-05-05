class Censor():
    censor: bool = False

    def __init__(self, censor: bool = False):
        Censor.censor = censor

    @staticmethod
    def mac(mac):
        if Censor.censor:
            if len(mac) < 17:
                return "**:**:**:**:**:**"
            return mac[0:5] + ":**:**:**:**"
        return mac

    @staticmethod
    def ssid(ssid):
        if Censor.censor:
            if len(ssid) < 8:
                return "*" * 8
            return ssid[0:2] + "*" * 6
        return ssid

    @staticmethod
    def gps(coord):
        if Censor.censor:
            coord_ = str(coord)
            if len(coord_) < 8:
                return "**.*****"
            return coord_[0:4] + "*" * 6
        return coord

    @staticmethod
    def housenumber(num):
        if Censor.censor:
            return "**"
        return num

    @staticmethod
    def road(str_):
        if Censor.censor:
            return Censor.text(str_, 4)
        return str_

    @staticmethod
    def city(str_):
        if Censor.censor:
            return Censor.text(str_, 1)
        return str_

    @staticmethod
    def postalcode(str_):
        if Censor.censor:
            return Censor.text(str_, 1)
        return str_

    @staticmethod
    def country(str_):
        if Censor.censor:
            return Censor.text(str_, 0)
        return str_

    @staticmethod
    def region(str_):
        if Censor.censor:
            return Censor.text(str_, 0)
        return str_

    @staticmethod
    def brand(str_):
        if Censor.censor:
            return Censor.text(str_, 2)
        return str_

    @staticmethod
    def text(text_, min_len):
        if Censor.censor:
            text_ = str(text_)
            if len(text_) <= min_len:
                return "*" * min_len
            else:
                return text_[0:min_len] + "*" * 4
        return text_
