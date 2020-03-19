import random
import requests
import time
from dataclasses import dataclass, field

PRIMARY_URL = 'https://www.supremenewyork.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded'
}


# Class for task formation
@dataclass
class Task:
    task_name: str
    keywords: list
    category: str
    color: str
    size: str
    delay: float


# Class for getting itemID
# Gets task for the item -> gives the full link to rhe item
class Parser:
    def __init__(self, task, proxy=None):
        self.task = task
        self.proxy = proxy

    # Continues to look for the necessary item
    def monitor(self):
        result = self.pars_stock()
        while result is None:
            time.sleep(1)
            result = self.pars_stock()

        return result

    # Gets keywords for the item -> gives the full link to the item
    def pars_stock(self):
        stock_url = PRIMARY_URL + 'mobile_stock.json?'
        stock_url += str(random.randint(1, 10000))
        headers = HEADERS
        item_id = None

        if self.proxy is None:
            r = requests.get(stock_url, headers=headers).json()
        else:
            proxies = {
                'http': f'http://{self.proxy}',
                'https': f'https://{self.proxy}'
            }

            try:
                r = requests.get(stock_url, headers=headers, proxies=proxies).json()
            except requests.RequestException:
                print(f'Proxy {self.proxy} failed while looking product')
                exit()

        all_prod_in_cat = r['products_and_categories'][self.task.category]

        for i in range(len(all_prod_in_cat)):
            prod_name = r['products_and_categories'][self.task.category][i]['name']
            count = 0
            for kw in self.task.keywords:
                if kw.upper() in prod_name.upper():
                    count += 1
                else:
                    break

            if count == len(self.task.keywords):
                item_id = r['products_and_categories'][self.task.category][i]['id']

        return item_id

# Class for getting styleID and sizeID
# Gets the full link to the item -> gives the full link to the styled item
    def find_style(self, item_id):
        item_url = PRIMARY_URL + f'shop/{self.task.category}/{item_id}.json'
        headers = HEADERS
        style_id = None
        size_id = None

        if self.proxy is None:
            r = requests.get(item_url, headers=headers).json()
        else:
            proxies = {
                'http': f'http://{self.proxy}',
                'https': f'https://{self.proxy}'
            }

            try:
                r = requests.get(item_url, headers=headers, proxies=proxies).json()
            except requests.RequestException:
                print(f'Proxy {self.proxy} failed while looking product')
                exit()

        all_styles = r['styles']

        for i in range(len(all_styles)):
            color_found = False
            size_found = False
            sold_out = True

            if all_styles[i]['name'].upper() == self.task.color.upper():
                style_id = r['styles'][i]['id']
                color_found = True

                all_sizes = r['styles'][i]['sizes']

                for _ in range(len(all_sizes)):
                    if r['styles'][i]['sizes'][_]['name'].upper() == self.task.size.upper():
                        size_id = r['styles'][i]['sizes'][_]['id']
                        size_found = True

                        stock_level = r['styles'][i]['sizes'][_]['stock_level']
                        if stock_level == 1:
                            sold_out = False

                        if color_found and size_found:
                            if not sold_out:
                                return style_id, size_id
                            else:
                                return style_id, size_id, 'SOLD OUT'
                        else:
                            return 'ITEM NOT FOUND'
