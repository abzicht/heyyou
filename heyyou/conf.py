try:
    from mac import Mac
    from censor import Censor
except ImportError:
    from heyyou.mac import Mac
    from heyyou.censor import Censor


class Config:
    interface: str = None
    mac: Mac = None
    auth_token: str = None
    summary: bool = False
    censor: Censor = None

    def __init__(self, args):
        Config.interface = args.interface
        Config.auth_token = args.auth_token
        Config.summary = args.summary
        Config.censor = Censor(args.censor)
        if args.mac_vendors:
            Config.mac = Mac(args.mac_vendors)
