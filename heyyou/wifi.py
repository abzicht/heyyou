from subprocess import call

try:
    from conf import Config
except ImportError:
    from heyyou.conf import Config


def managed():
    __switch_mode__('managed')


def monitor():
    __switch_mode__('monitor')


def __switch_mode__(operation_mode: str):
    assert 0 == call(["ip", "link", "set", Config.interface, "down"])
    assert 0 == call(["iw", "dev", Config.interface, "set", "type", operation_mode])
    assert 0 == call(["ip", "link", "set", Config.interface, "up"])
