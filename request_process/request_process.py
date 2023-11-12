import json
import requests


def get_real_rep_data(shop_id: int, api_key: str, client_id: int = None) -> dict:

    get_url = "https://api-seller.ozon.ru/v1/finance/realization"

    body = {"date": "2023-09"}
    body = json.dumps(body)

    # get your client id and api key from ozon seller.
    headers = {"Client-Id": str(shop_id), "Api-Key": api_key}

    response = requests.post(get_url, headers=headers, data=body)

    rows = response.json()['result']['rows']
    item_dict = {}


    with open('json.json', 'w', encoding='utf-8') as file:
        json.dump(response.json()['result'], file, ensure_ascii=False, indent=4)


    # book = openpyxl.Workbook()
    #
    # main_sht = book.active
    # main_sht['A1'] = 'ITEM'
    # main_sht['B1'] = 'SALE_QTY'
    # main_sht['C1'] = 'SOLD_AMMOUNT'
    # main_sht['D1'] = 'RETURN_QTY'
    # main_sht['E1'] = 'RETURN_AMMOUNT'
    #
    for row in rows:
        item = row['offer_id']
        if item not in item_dict:
            selling_volume = {}
            selling_volume['sale_qty'] = row['sale_qty']
            selling_volume['sale_price_seller'] = row['sale_price_seller']
            selling_volume['return_qty'] = row['return_qty']
            selling_volume['return_price_seller'] = row['return_price_seller']
            item_dict[item] = selling_volume
        else:
            item_dict[item]['sale_qty'] += row['sale_qty']
            item_dict[item]['sale_price_seller'] += row['sale_price_seller']
            item_dict[item]['return_qty'] += row['return_qty']
            item_dict[item]['return_price_seller'] += row['return_price_seller']

    return item_dict
    #
    # row_index = 2
    # for item, value in item_dict.items():
    #     print(item, value)
    #     main_sht.cell(row=row_index, column=1).value = item
    #     main_sht.cell(row=row_index, column=2).value = value['sale_qty']
    #     main_sht.cell(row=row_index, column=3).value = value['sale_price_seller']
    #     main_sht.cell(row=row_index, column=4).value = value['return_qty']
    #     main_sht.cell(row=row_index, column=5).value = value['return_price_seller']
    #     row_index += 1
    #
    # book.save('ozon.xlsx')
    # book.close()
    #
    # with open('json.json', 'w') as file:
    #     json.dump(response.json()['result'], file, indent=4)

if __name__ == '__main__':
    get_real_rep_data(CLIENT_ID, API_KEY)