import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats


lego_sales = pd.read_csv("lego_sales.csv").drop_duplicates()

sales_info = lego_sales['Sales'].str.split(r'(\d+)')
lego_sales['Sales'] = sales_info.apply(lambda x: x[1])
lego_sales['Sales'] = lego_sales['Sales'].apply(int)
# extract set sales
lego_sales['Search Content'] = lego_sales['Search Content'].str.replace('乐高', '')

lego_info = pd.read_csv("set.csv")
# import data from Lego TMall
lego_info['Set_No'] = lego_info['Set_No'].apply(str)
# print(list(lego_sales.columns))
lego_info = lego_info[[
    'Price',
    'Sales',
    'Set_No'
]]

lego_info.rename(columns={'Price':'Official Price',
                          'Sales':'Official Sales'},
                 inplace=True)

lego_sales = pd.merge(lego_sales, lego_info,
                      left_on='Search Content',
                      right_on='Set_No')
# map set info to sales
print(lego_sales.shape)

lego_sales = lego_sales[lego_sales.apply(lambda x: x['Set_No'] in x['Product Name'], axis=1)]
print(lego_sales.shape)
# filter out not related products

lego_sales = lego_sales[lego_sales['Price'].between(lego_sales['Official Price']*0.45, lego_sales['Official Price']*1.2, inclusive=True)]
# assume price from 3rd party range from 55% off or 20% plus vs. official price)
print(lego_sales.shape)

sets = pd.read_csv('sets.csv')
themes = pd.read_csv('themes.csv')
# import data from rebrickable.com
# print(list(sets.columns))
# print(list(themes.columns))
sets.rename(columns={'name':'Official Product Name'},
                 inplace=True)
sets['set_num'] = sets['set_num'].str.replace('-1', '')
themes.rename(columns={'name':'Theme'},
                 inplace=True)

sets = pd.merge(sets, themes,
                      left_on='theme_id',
                      right_on='id')
print(list(sets.columns))
lego_sales = pd.merge(lego_sales, sets,
                      left_on='Set_No',
                      right_on='set_num')
# print(list(lego_sales.columns))
print(list(lego_sales.shape))

lego_sales['yr_launch'] = 2023 - lego_sales['year']

lego_sales['sum_sales'] = lego_sales.groupby('Set_No')['Sales'].transform('sum')


lego_sales = lego_sales[['Product Name',
                         'Price',
                         'Sales',
                         'sum_sales',
                         'Shop',
                         'Official Price',
                         'Official Sales',
                         'Set_No',
                         'Official Product Name',
                         'year',
                         'yr_launch',
                         'num_parts',
                         'Theme']]


lego_sales.info()
lego_sales.describe()

lego_sales_int = lego_sales[['Price',
                             'Official Price',
                             'Official Sales',
                             'num_parts',
                             'Sales',
                             'sum_sales',
                             'yr_launch']]

sns.pairplot(lego_sales_int)

corr = lego_sales_int.corr()
print(corr)
sns.heatmap(lego_sales_int.corr())

def my_pvalue_pearson(x):
    col = x.shape[1]
    col_name = x.columns.values
    p_val = []
    for i in range(col):
        for j in range(col):
            p_val.append(stats.pearsonr(x[col_name[i]], x[col_name[j]])[1])
    p_val = pd.DataFrame(np.array(p_val).reshape(col, col), columns=col_name, index=col_name)
    print(p_val)
# calculate p-value

my_pvalue_pearson(lego_sales_int)

