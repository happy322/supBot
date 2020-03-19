import requests
import time
import sys
from dataclasses import dataclass
from gparams import get_params as gp

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
    name: str
    email: str
    tel: str
    address: str
    apt: str
    zip: str
    city: str
    state: str
    country: str
    card_number: str
    exp_month: str
    exp_year: str
    cvv: str
    brand: str


class CheckOuter:
    def __init__(self, profile, checkout_data, start, delay=0.8, proxy=None):
        self.profile = profile
        self.checkout_data = checkout_data
        self.proxy = proxy
        self.start_time = start
        self.delay = delay

    def atc_checkout(self):
        s = requests.Session()
        url = f"https://www.supremenewyork.com/shop/{self.checkout_data[0]}/add.json"

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Mobile/15E148',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            "style": self.checkout_data[1],
            "size": self.checkout_data[2],
            "quantity": "1"
        }

        q = s.post(url, headers=headers, data=data)

        cooks = s.cookies.get_dict()
        cookSub = cooks["pure_cart"]
        coHeaders = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
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

        checkout_page = s.get("https://www.supremenewyork.com/mobile/#checkout")
        co_data = gp(self.profile, checkout_page.content, cookSub)

        if co_data is None:
            print("\nError with parsing checkout parameters")
            sys.exit(0)
        else:

            s.cookies["hasShownCookieNotice"] = "1"
            s.cookies["lastVisitedFragment"] = "checkout"
            co_url = "https://www.supremenewyork.com/checkout.json"

            time.sleep(self.delay)

            if self.proxy is None:
                z = s.post(co_url, headers=coHeaders, data=co_data)
            else:
                proxies = {
                    "http": f"http://{self.proxy}",
                    "https": f"https://{self.proxy}"
                }
                try:
                    z = s.post(co_url, headers=coHeaders, data=co_data, proxies=proxies)
                except requests.RequestException:
                    print(f"Proxy {self.proxy} failed at checkout")
                    exit()

            end = time.time()
            all_time = end - self.start_time
            all_time = round(all_time, 3)
            all_time = f"\nCheckout details sent in {all_time} seconds"

            return z.json(), all_time

    def get_status(self, slug):
        statUrl = f"https://www.supremenewyork.com/checkout/{slug}/status.json"

        if self.proxy is None:
            r = requests.get(statUrl).json()

        else:
            proxies = {
                "http": f"http://{self.proxy}",
                "https": f"https://{self.proxy}"
            }
            try:
                time.sleep(4.75)
                r = requests.get(statUrl, proxies=proxies).json()
            except requests.RequestException:
                print(f"Proxy {self.proxy} failed at status check")
                sys.exit(0)
        return r["status"]
