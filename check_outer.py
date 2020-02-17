import requests
import time
import sys
from dataclasses import dataclass

HEADERS = None
PRIMARY_URL = 'https://www.supremenewyork.com/'


@dataclass
class Profile:
    pass


class CheckOuter:
    def __init__(self, profile, checkout_data):
        self.profile = profile
        self.checkout_data = checkout_data
