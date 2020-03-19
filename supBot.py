import json
import parser
import check_outer
import time


class Bot:
    def __init__(self, tk, prf, proxy=None):
        self.task = tk
        self.profile = prf
        self.proxy = proxy

    def go(self):
        start = time.time()
        pars = parser.Parser(self.task, self.proxy)
        item_id = pars.monitor()
        returned_ids = pars.find_style(item_id)

        if returned_ids is None:
            print(f"Error finding style or size for task '{self.task.task_name}'\n")
        elif len(returned_ids) == 2:
            co_data = [item_id, returned_ids[0], returned_ids[1]]

            check = check_outer.CheckOuter(self.profile, co_data, start)
            result = check.atc_checkout()

            if "slug" in result[0]:
                slug = result[0]
                slug = slug["slug"]
                print("\n")
                for _ in range(2):
                    stat = check.get_status(slug)
                    time.sleep(3.5)
                    print(f"Status for '{self.task.task_name}': {stat}")
            else:
                print(f"Checkout failed for task '{self.task.task_name}', restarting\n")
                time.sleep(1.25)
                self.go()
        else:
            print(f"Item sold out for '{self.task.task_name}', restarting")
            time.sleep(2)
            self.go()


if __name__ == '__main__':
    print('Запускаем test')
    task_name = 'test'
    kw = ['stars', 'crewneck']
    category = 'Sweatshirts'
    size = 'Medium'
    color = 'Red'
    delay = 5.8

    task = parser.Task(task_name, kw, category, color, size, delay)

    name = 'EGOR SHEVELEV'
    email = 'technik.rek@gmail.com'
    tel = '+79087541340'
    address = 'Sem val'
    apt = ''
    zip_code = '105094'
    city = 'Moscow'
    state = ''
    country = 'RU'
    card_number = '5321 3046 3260 2741'
    exp_mon = '04'
    exp_year = '2024'
    cvv = '717'
    brand = 'master'

    profile = check_outer.Profile(name, email, tel, address, apt, zip_code, city, state, country, card_number, exp_mon,
                                  exp_year, cvv, brand)

    bot = Bot(task, profile)

    bot.go()
