import pandas as pd
from mypy.util import json_dumps

gen_list = []
cat_list = {}

df = pd.read_csv('../data/operations.csv')
for index, row in df.iterrows():
    cat = row['Категория']
    price = float(row['Сумма операции'].replace(',', '.'))
    # if cat == "" or cat == "nan":
    #     continue
    gen_list.append([cat, price])
    if cat not in cat_list:
        cat_list[cat] = 0

for key, value in cat_list.items():
    summ = sum(x[1] for x in gen_list if x[0] == key)
    cat_list[key] = summ

cat_list = { key: (value * -1) // 100 if value < 0 else value for key, value in cat_list.items()}
print(cat_list)