from bs4 import BeautifulSoup as bs
import re
import time


def get_params(myProfile, checkout_page, cookSub):
    regex = re.compile('[^a-zA-Z]')
    soup = bs(checkout_page, "html.parser")
    all_scripts = soup.find_all("script")
    data = find_params_script(myProfile, all_scripts, cookSub, regex)
    return data


def find_params_script(myProfile, all_scripts, cookSub, regex):
    coData = {}
    for script in all_scripts:
        try:
            script = script.text
            soup = bs(script, "html.parser")
            select_fields = soup.find_all("select")
            input_fields = soup.find_all("input")

            has_value = []
            no_value = []

            for input_box in input_fields:
                try:
                    value_check = input_box["value"]
                    has_value.append(input_box)
                except:
                    try:
                        cause_error = input_box["name"]
                        no_value.append(input_box)
                    except:
                        pass

            for hv in has_value:
                coData[hv["name"]] = hv["value"]
                if hv["value"] == "":
                    try:
                        placeholder = regex.sub("", hv["placeholder"]).lower().strip()

                        if "cvv" in placeholder or "cvv" == placeholder:
                            coData[hv["name"]] = myProfile.cvv
                        elif "card" in placeholder or "credit" in placeholder:
                            coData[hv["name"]] = myProfile.card_number

                    except:
                        coData[hv["name"]] = hv["value"]

            for nv in no_value:
                try:
                    placeholder = regex.sub("", nv["placeholder"]).lower().strip()
                    name = regex.sub("", nv["name"]).lower().strip()

                    if placeholder == "name" or "name" in nv["name"]:
                        if nv["name"] not in coData:
                            coData[nv["name"]] = myProfile.name

                    elif placeholder == "email" or "email" in name or "e-mail" in name or "e-mail" == placeholder:
                        coData[nv["name"]] = myProfile.email

                    elif placeholder == "telephone" or placeholder == "tel" or "tel" in placeholder or "tel" in name:
                        coData[nv["name"]] = myProfile.tel

                    elif placeholder == "address" or placeholder == "billing address" or placeholder == "addr":
                        coData[nv["name"]] = myProfile.address

                    elif placeholder == "apt, unit, etc" or "apt" in placeholder or "unit" in placeholder:
                        coData[nv["name"]] = myProfile.apt

                    elif "zip" in name or "billing zip" in name or placeholder == "postcode":
                        coData[nv["name"]] = myProfile.zip

                    elif placeholder == "city" or "city" in name:
                        coData[nv["name"]] = myProfile.city

                except:
                    if "cookie" in nv["name"] or "sub" in nv["name"]:
                        coData[nv["name"]] = cookSub

            for sf in select_fields:
                id_ = regex.sub("", sf["id"]).lower().strip()
                name = regex.sub("", sf["name"]).lower().strip()

                if "state" in name or "state" in id_:
                    coData[sf["name"]] = myProfile.state

                elif "country" in name or "country" in id_:
                    coData[sf["name"]] = myProfile.country

                elif "month" in name or "month" in id_:
                    coData[sf["name"]] = myProfile.exp_month

                elif "year" in name or "year" in id_:
                    coData[sf["name"]] = myProfile.exp_year

                elif "type" in name or "type" in id_:
                    coData[sf["name"]] = myProfile.brand

        except:
            pass

    return coData
