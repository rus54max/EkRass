import pandas as pd
from src.utils import get_data_by_file_oper

def find_by_phone(phone):
    df = get_data_by_file_oper()

    df = df[df['Описание'].str.contains('|'.join(phone))]
    return df.to_dict()

def find_by_desc(find_string):
    df = get_data_by_file_oper()

    df = df[df['Описание'].str.contains('|'.join(find_string))]
    return df.to_dict()

#res = find_by_phone(r"\bЯ МТС \+7 921 11-22-33")
res = find_by_phone(r"\bМТС")
print(res)








# from mypy.util import json_dumps
#
# gen_list = []
# cat_list = {}
#
# df = pd.read_csv('../data/operations.csv')
# for index, row in df.iterrows():
#     cat = row['Категория']
#     price = float(row['Сумма операции'].replace(',', '.'))
#     # if cat == "" or cat == "nan":
#     #     continue
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