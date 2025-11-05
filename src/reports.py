import pandas as pd
from typing import Optional
from datetime import datetime


def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    if date:
        reference_date = pd.to_datetime(date, dayfirst=True)
    else:
        reference_date = pd.to_datetime('today')
    start_date = (reference_date - pd.DateOffset(months=3)).replace(day=1)
    end_date = reference_date
    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)
    mask = (transactions['Дата платежа'] >= start_date) & (transactions['Дата платежа'] <= end_date)
    recent_transactions = transactions.loc[mask]
    recent_transactions['weekday'] = recent_transactions['Дата платежа'].dt.weekday
    recent_transactions['day_type'] = recent_transactions['weekday'].apply(
        lambda x: 'Рабочий день' if x < 5 else 'Выходной день'
    )
    result = recent_transactions.groupby('day_type')['Сумма платежа'].mean().reset_index()
    return result


df = pd.read_csv('../data/operations.csv')
result = spending_by_workday(df, '20.05.2024')

print(result)


















# def spending_by_workday(transactions: pd.DataFrame,
#                         date: Optional[str] = None) -> pd.DataFrame:
#     # Если дата не передана, берем текущую
#     if date:
#         reference_date = pd.to_datetime(date, dayfirst=True)
#     else:
#         reference_date = pd.to_datetime('today')
#
#     # Расчет диапазона: последние 3 месяца с 1-го числа начала месяца
#     start_date = (reference_date - pd.DateOffset(months=3)).replace(day=1)
#     end_date = reference_date
#
#     # Преобразуем колонку 'date' в datetime, если нужно
#     transactions['date'] = pd.to_datetime(transactions['date'])
#
#     # Фильтруем по диапазону
#     mask = (transactions['date'] >= start_date) & (transactions['date'] <= end_date)
#     recent_transactions = transactions.loc[mask]
#
#     # Определим день недели: 0 - понедельник, 6 - воскресенье
#     recent_transactions['weekday'] = recent_transactions['date'].dt.weekday
#
#     # Определим рабочие и выходные дни
#     # 0-4 - рабочие, 5-6 — выходные
#     recent_transactions['day_type'] = recent_transactions['weekday'].apply(
#         lambda x: 'Рабочий день' if x < 5 else 'Выходной день'
#     )
#
#     # Группируем по типу дня и считаем средний расход
#     result = recent_transactions.groupby('day_type')['amount'].mean().reset_index()
#
#     # Для удобства: отображение
#     return result