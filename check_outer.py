import requests
import time
import sys
from dataclasses import dataclass

CO_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/11.0 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.supremenewyork.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.supremenewyork.com/mobile/',
    'TE': 'Trailers'
    }
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded'
}
PRIMARY_URL = 'https://www.supremenewyork.com/'


@dataclass
class Profile:
    pass


class CheckOuter:
    def __init__(self, profile, checkout_data):
        self.profile = profile
        self.checkout_data = checkout_data
