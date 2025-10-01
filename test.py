#%%
# Подключаем модули для работы с данными
import pandas as pd
import sqlalchemy as sa

# Читаем Каталог с валидацией данных и правильным неймингом
catalog = (
    pd
    .read_excel(
        io ="primary_task_1-4/test_data.xlsx",
        sheet_name='Каталог',
        dtype = {
            "Артикул 1C": pd.Int64Dtype(),
            "SKU": pd.Int64Dtype(),
            "Название": pd.StringDtype(),
            "Статус":  pd.StringDtype(),
            "МП":  pd.StringDtype(),
        }
    )
    .rename(columns = {
        "Артикул 1C": "sku_1c",
        "SKU": "sku",
        "Название": "name",
        "Статус": "status",
        "МП": "placement"
    })
)

# Читаем Продажи с валидацией данных и правильным неймингом
sales = (
    pd
    .read_excel(
        io ="primary_task_1-4/test_data.xlsx",
        sheet_name='Продажи',
        dtype = {
            "Артикул 1C": pd.Int64Dtype(),
            "SKU": pd.Int64Dtype(),
            "Цена продажи,р": pd.Float64Dtype(),
            "Кол-во": pd.Float64Dtype(),
            "Комиссия(% от выручки)": pd.Float64Dtype(),
            "Логистика,р": pd.Float64Dtype()
        }
    )
    .rename(columns = {
        "Артикул 1C": "sku_1c",
        "SKU": "sku",
        "Цена продажи,р": "item_price",
        "Кол-во": "quantity",
        "Комиссия(% от выручки)": "commission_pnt",
        "Логистика,р": "logistic_price",
        "Дата": "report_date"
    })
)
# Исправляем комиссию
sales['commission_pnt'] = sales['commission_pnt'] / 100

cost_price = (
    pd
    .read_excel(
        io ="primary_task_1-4/test_data.xlsx",
        sheet_name='Себестоимость',
        dtype = {
            "Артикул 1C": pd.Int64Dtype(),
            "Себестоимость": pd.Float64Dtype(),
        }
    )
    .rename(
        columns = {
            "Артикул 1C": "sku_1c",
            "Себестоимость": "cost",
        }
    )
)

#%%
# Сохраняем в базу данных
psql_eng = sa.create_engine('postgresql://test:test@localhost:5432/postgres')
catalog.to_sql(
    name = "catalog",
    con = psql_eng,
    if_exists = "replace",
    index = False,
)
sales.to_sql(
    name = "sales",
    con = psql_eng,
    if_exists = "replace",
    index = False,
)
cost_price.to_sql(
    name = "cost_price",
    con = psql_eng,
    if_exists = "replace",
    index = False,
)