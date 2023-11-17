import json

import requests
from environs import Env


def get_real_rep_data(shop_id: int, api_key: str, selected_month: str) -> dict:

    get_url = "https://api-seller.ozon.ru/v1/finance/realization"

    body = {"date": selected_month}
    body = json.dumps(body)

    # get client id and api key from ozon seller.
    headers = {"Client-Id": str(shop_id), "Api-Key": api_key}

    response = requests.post(get_url, headers=headers, data=body)

    rows = response.json()['result']['rows']
    item_dict = {}

    with open('json.json', 'w', encoding='utf-8') as file:
        json.dump(
            response.json()['result'],
            file,
            ensure_ascii=False,
            indent=4
        )

    for row in rows:
        item = row['offer_id']
        if item not in item_dict:
            item_dict[item] = {
                'sale_qty': row['sale_qty'],
                'sale_price_seller': row['sale_price_seller'],
                'return_qty': row['return_qty'],
                'return_price_seller': row['return_price_seller']
            }
        else:
            item_dict[item]['sale_qty'] += row['sale_qty']
            item_dict[item]['sale_price_seller'] += \
                row['sale_price_seller']
            item_dict[item]['return_qty'] += \
                row['return_qty']
            item_dict[item]['return_price_seller'] += \
                row['return_price_seller']

    return item_dict


if __name__ == '__main__':
    env = Env()
    env.read_env()
    select_month = input('ввод: ')  # format: %Y-%M, example 2023-11
    client_id = env('TEST_CLIENT_ID')
    api_key = env('TEST_API_KEY')
    print(get_real_rep_data(client_id, api_key, select_month))