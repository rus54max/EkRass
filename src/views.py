import json

from src.utils import process_cards, get_greeting, process_transactions, process_currency_rates, process_stock_prices


def by_date(date_time): #YYYY-MM-DD HH:MM:SS
    dict_result = {}
    dict_result["greeting"] = get_greeting(date_time)
    dict_result["cards"] = process_cards(date_time)
    dict_result["top_transactions"] = process_transactions(date_time)
    dict_result["currency_rates"] = process_currency_rates()
    dict_result["stock_prices"] = process_stock_prices()
    return json.dumps(dict_result, ensure_ascii=False, indent=2)


dict_result = by_date("2021-10-24 14:30:00")
print(dict_result)


    # {
    #     "greeting": "Добрый день",
    #     "cards": [
    #         {
    #             "last_digits": "5814",
    #             "total_spent": 1262.00,
    #             "cashback": 12.62
    #         },
    #         {
    #             "last_digits": "7512",
    #             "total_spent": 7.94,
    #             "cashback": 0.08
    #         }
    #     ],
    #     "top_transactions": [
    #         {
    #             "date": "21.12.2021",
    #             "amount": 1198.23,
    #             "category": "Переводы",
    #             "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    #         },
    #         {
    #             "date": "20.12.2021",
    #             "amount": 829.00,
    #             "category": "Супермаркеты",
    #             "description": "Лента"
    #         },
    #         {
    #             "date": "20.12.2021",
    #             "amount": 421.00,
    #             "category": "Различные товары",
    #             "description": "Ozon.ru"
    #         },
    #         {
    #             "date": "16.12.2021",
    #             "amount": -14216.42,
    #             "category": "ЖКХ",
    #             "description": "ЖКУ Квартира"
    #         },
    #         {
    #             "date": "16.12.2021",
    #             "amount": 453.00,
    #             "category": "Бонусы",
    #             "description": "Кешбэк за обычные покупки"
    #         }
    #     ],
    #     "currency_rates": [
    #         {
    #             "currency": "USD",
    #             "rate": 73.21
    #         },
    #         {
    #             "currency": "EUR",
    #             "rate": 87.08
    #         }
    #     ],
    #     "stock_prices": [
    #         {
    #             "stock": "AAPL",
    #             "price": 150.12
    #         },
    #         {
    #             "stock": "AMZN",
    #             "price": 3173.18
    #         },
    #         {
    #             "stock": "GOOGL",
    #             "price": 2742.39
    #         },
    #         {
    #             "stock": "MSFT",
    #             "price": 296.71
    #         },
    #         {
    #             "stock": "TSLA",
    #             "price": 1007.08
    #         }
    #     ]
    # }