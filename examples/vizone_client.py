from articulate import define
from vizone.client import init
from vizone.resource.asset import create_asset, asset_Item as Item

@define('a Viz One client for <hostname>')
class VizOneSession:
    def __init__(self, hostname):
        self.hostname = hostname

    def __expose__(self):
        return {
            'hostname': self.hostname,
        }

    @define('authenticate with <username> and <password>')
    def authenticate(self, username, password):
        self.client = init(self.hostname, username, password)

    @define('create asset <title>')
    def create_asset(self, title):
        return create_asset(Item(title=title))
