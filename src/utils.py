import json
import pandas as pd
from datetime import datetime
import requests


def get_data_by_file_oper():
    #df = pd.read_csv("../data/operations.csv", parse_dates=['Дата операции'], date_format= "%d-%m-%Y %H:%M:%S")
    df = pd.read_csv("../data/operations.csv", parse_dates=['Дата операции'], date_format="%d-%m-%Y %H:%M:%S")
    return df

def get_dada_by_file_user_settings():
    with open('../user_settings.json') as f:
        return json.load(f)


def get_greeting(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def str_date_to_date(date_str) -> datetime:
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    str_dt = dt.strftime("%Y-%m-%d")
    return datetime.strptime(str_dt, "%Y-%m-%d")


def process_cards(date_str):
    date = str_date_to_date(date_str)
    date_start = date.replace(day=1)
    date_start = date_start.strftime("%Y-%m-%d")
    df = get_data_by_file_oper()
    df = df.dropna(subset=['Номер карты', 'Сумма операции'])
    df = df[df['Дата операции'] <= date_str]
    df = df[df['Дата операции'] >= date_start]
    """Обработка данных по картам: последние 4 цифры, сумма расходов, кешбэк"""
    cards_info = []
    # Группируем по карте
    grouped = df.dropna(subset=['Номер карты']).groupby('Номер карты')
    for card, group in grouped:
        last_digits = str(card)[-4:]
        #total_spent = list(map(float, group['Сумма операции'])).sum()
        total_spent = sum([float(x.replace(',', '.')) for x in group['Сумма операции']])
        cashback = total_spent / 100  # 1 рубль на 100 рублей
        cards_info.append({
            'last_digits': last_digits,
            'total_spent': round(total_spent, 2),
            'cashback': round(cashback, 2)
        })
    return cards_info



def process_transactions(date_str):
    """Получение топ-5 транзакций за дату"""
    df = get_data_by_file_oper()
    filtered = df[df['Дата операции'] == date_str]
    top = filtered.sort_values(by='Сумма операции', ascending=False).head(5)
    result = []
    for _, row in top.iterrows():
        date_obj = datetime.strptime(row['Дата операции'], "%Y-%m-%d")
        date_str_formatted = date_obj.strftime("%d.%m.%Y")
        result.append({
            'date': date_str_formatted,
            'amount': round(row['Сумма операции'], 2),
            'category': row.get('Категория', ''),
            'description': row.get('Описание', '')
        })
    return result


def get_full_currency_dict():
    dict_user_settings = get_dada_by_file_user_settings()
    if "user_currencies" not in dict_user_settings:
        return
    list_need_currency = dict_user_settings["user_currencies"]
    url = "https://api.apilayer.com/exchangerates_data/symbols"     #?symbols=EUR,GBP

    payload = {}
    headers = {
        "apikey": "24z0Oh9LjLrDGi9p8XyNuCwZ3k6HvEz4"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.text

def process_currency_rates():
    """Статичные курсы валют"""
    return [
        {'currency': 'USD', 'rate': 73.21},
        {'currency': 'EUR', 'rate': 87.08}
    ]


def process_stock_prices():
    """Статичные цены акций"""
    return [
        {'stock': 'AAPL', 'price': 150.12},
        {'stock': 'AMZN', 'price': 3173.18},
        {'stock': 'GOOGL', 'price': 2742.39},
        {'stock': 'MSFT', 'price': 296.71},
        {'stock': 'TSLA', 'price': 1007.08}
    ]


def main(input_datetime_str):
    get_full_currency_dict()
    # Определяем приветствие
    greeting = get_greeting(input_datetime_str)

    # Чтение данных
    df = pd.read_csv('../data/operations.csv')

    # Получаем дату из строки
    dt = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    date_str = dt.strftime("%Y-%m-%d")

    # Обработка
    cards_info = process_cards("2023-10-24 14:30:00")
    top_transactions = process_transactions(df, date_str)
    currency_rates = process_currency_rates()
    stock_prices = process_stock_prices()

    # Итоговый JSON
    result = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return json.dumps(result, ensure_ascii=False, indent=2)

# Пример вызова:
#print(main("2023-10-24 14:30:00"))


# • https://www.alphavantage.co/
#
# • https://finnhub.io/
#
# • https://twelvedata.com/








# import pandas as pd
# from datetime import datetime
#
#
# def get_data_by_file():
#     df = pd.read_csv("../data/operations.csv")
#     return df
#
# def display_current_time():
#     now = datetime.now()
#     current_time_str = now.strftime("%H:%M:%S")
#     if current_time_str >= "4:00:00" and current_time_str <= "11:59:59":
#         return "Доброе утро"
#     elif current_time_str >= "12:00:00" and current_time_str <= "17:59:59":
#         return "Добрый день"
#     elif current_time_str >= "18:00:00" and current_time_str <= "23:59:59":
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"






# def get_top_transactions():
#     df = pd.read_csv('../data/operations.csv')
#     transactions =





# def process_transactions():
#     transactions = pd.read_csv('../data/operations.csv').to_dict(orient='records')
#     card_summary = {}
#     for transaction in transactions:
#         card_number = transaction['Номер карты']
#         amount = transaction['Сумма операции']
#
#         if card_number not in card_summary:
#             card_summary[card_number] = {'total_spent': 0, 'last_digits': card_number[-4:], 'cashback': 0}
#
#         card_summary[card_number]['total_spent'] += amount
#         card_summary[card_number]['cashback'] += amount // 100  # 1 рубль на каждые 100 рублей
#
#     return list(card_summary.values())
#
# process_transactions()

# gen_list = []
# cat_list = {}
#
# df = pd.read_csv('operations.csv')
# for index, row in df.iterrows():
#     cat = row['Номер карты']
#     price = float(row['Сумма операции'].replace(',', '.'))
#     if cat == "" or cat == "nan":
#         continue
#     gen_list.append([cat, price])
#     if cat not in cat_list:
#         cat_list[cat] = 0
#
# for key, value in cat_list.items():
#     summ = sum(x[1] for x in gen_list if x[0] == key)
#     cat_list[key] = summ
#
# cat_list = { key: (value * -1) // 100 if value < 0 else value for key, value in cat_list.items()}
# print(cat_list)

# # 1. Чтение данных из файла
# df = pd.read_csv('../data/operations.csv')
#
# # 2. Группировка по столбцу 'Категория' и суммирование 'Значения'
# grouped_data = df.groupby('Номер карты')['Сумма операции'].sum()
#
# print(grouped_data)



# def is_float(string):
#     try:
#         return float(string)  #and '.' in string  # True if string is a number contains a dot
#     except ValueError:  # String is not a number
#         return False
#
#
# def get_list_card_group():
#     p = get_data_by_file()
#     result ={}
#     for i, value in p.iterrows():
#         namber_card = value['Номер карты']
#         if namber_card == "nan":
#             continue
#         price_tran = value['Сумма операции']
#         if not is_float(price_tran):
#             continue
#         price_tran = int(price_tran)
#         if namber_card in result:
#             result[namber_card] += price_tran
#         else:
#             result[namber_card] = price_tran
#
#
#
#
#     print(result)
#
# get_list_card_group()




    # "last_digits": "Номер карты"
    # "total_spent": "Сумма операции"
    # "cashback": "Кэшбэк"




    # # Чтение CSV в DataFrame
    # df = pd.read_csv('input.csv')
    #
    # # Преобразование DataFrame в список словарей
    # data_list_pd = df.to_dict('records')
    #
    # print(data_list_pd)
    # # Пример вывода:
    # # [{'Имя': 'Алиса', 'Возраст': 30, 'Город': 'Москва'}, ...]
    #
    # print(wine_reviews.head(5))