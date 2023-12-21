import json
import logging

import aiofiles
import aiohttp
from environs import Env


async def get_real_rep_data(shop_id: int, api_key: str, selected_month: str) -> dict:
    get_url = "https://api-seller.ozon.ru/v1/finance/realization"

    body = {"date": selected_month}
    body = json.dumps(body)

    # получение идентификатора клиента и ключа API от продавца на Ozon
    headers = {"Client-Id": str(shop_id), "Api-Key": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.post(get_url, headers=headers, data=body) as response:
            data = await response.json()
            logging.info(json.dumps(data))
            print(f'___________{data}____________')
            rows = data['result']['rows']
            item_dict = {}

            async with aiofiles.open('json.json', 'w', encoding='utf-8') as file:
                await file.write(json.dumps(
                    data['result'],
                    ensure_ascii=False,
                    indent=4
                ))

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
            print('такой вывод: ', item_dict)
            return item_dict


if __name__ == '__main__':
    env = Env()
    env.read_env()
    select_month = input('ввод: ')  # format: %Y-%M, example 2023-11
    client_id = env('TEST_CLIENT_ID')
    api_key = env('TEST_API_KEY')
    print(get_real_rep_data(client_id, api_key, select_month))
