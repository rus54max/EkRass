import json
import os
from traceback import format_exception
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import requests

load_dotenv()

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
    date_start = date_start.strftime("%d-%m-%Y %H:%M:%S") #%Y-%m-%d %H:%M:%S
    df = get_data_by_file_oper()
    df = df.dropna(subset=['Номер карты', 'Сумма операции'])
    df = df[df['Дата операции'] >= date_start]
    df = df[df['Дата операции'] <= date_str]
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
    date = str_date_to_date(date_str)
    date_start = date.replace(hour=0, minute=0, second=0)
    date_start = date_start.strftime("%d.%m.%Y") # %H:%M:%S
    date_finish = date.replace(day=date.day+1, hour=0, minute=0, second=0)
    date_finish = date_finish.strftime("%d.%m.%Y %H:%M:%S")  # %Y-%m-%d %H:%M:%S
    #df = df.loc[date_start : date_finish]
    #filtered = df[(df['Дата операции'] >= date_start)]
    df = df[df['Дата операции'] >= date_start]
    df = df[df['Дата операции'] < date_finish]
    #df = df[df['Дата операции'] == date_start]
    #df = df[df['Дата операции'] == date]
    top = df.sort_values(by='Сумма операции', ascending=False).head(5)
    #print(df.head(5))
    #print(df.tail(5))
    result = []
    for _, row in top.iterrows():
        # date_obj = datetime.strptime(row['Дата операции'], "%Y-%m-%d")
        # date_str_formatted = date_obj.strftime("%d.%m.%Y")
        date_str_formatted = row['Дата операции']
        result.append({
            'date': date_str_formatted,
            'amount': round(float(row['Сумма операции'].replace(",", ".")), 2),
            'category': row.get('Категория', ''),
            'description': row.get('Описание', '')
        })
    return result


def process_currency_rates():
    result_list = []

    dict_user_settings = get_dada_by_file_user_settings()
    if "user_currencies" not in dict_user_settings:
        return

    list_need_currency = dict_user_settings["user_currencies"]
    for cur in list_need_currency:
        url = f"https://api.apilayer.com/currency_data/live?source={cur}&currencies=RUB" #{",".join(dict_user_settings['user_currencies'])}   #?symbols=EUR,GBP
        payload = {}
        headers = {
            "apikey": os.getenv('API_LAYER')
            #"apikey": "24z0Oh9LjLrDGi9p8XyNuCwZ3k6HvEz4"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code == 200:
            result = json.loads(response.text)
            result_list.append({"currentcy": result["source"], "rate": list(result["quotes"].items())[0][1]})
    return  result_list

def process_stock_prices():
    result_list = []

    dict_user_settings = get_dada_by_file_user_settings()
    if "user_stocks" not in dict_user_settings:
        return

    list_need_stocks = dict_user_settings["user_stocks"]

    for stock in list_need_stocks:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={stock}"
        payload = {}
        headers = {
            "X-Api-Key": os.getenv('API_NINJAS')
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code == 200:
            result = json.loads(response.text)
            result_list.append({"stock": result["ticker"], "price": result["price"]})
    return  result_list






