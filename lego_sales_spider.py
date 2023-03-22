from tb_utils import *
import pandas as pd


set = pd.read_csv('lego_info.csv')
# print(set.shape)
# (1583, 5)

set = set[set['Shop'] == '乐高官方旗舰店'].drop_duplicates()
# filter official shop only
# print(set.shape)
# (554, 5)

prod_info = set['Product Name'].str.split(r'(\d+)')
set['Set_No'] = prod_info.apply(lambda x: x[1])
# extract set no.
sales_info = set['Sales'].str.split(r'(\d+)')
set['Sales'] = sales_info.apply(lambda x: x[1])
# extract set sales
print(set.head())

# set.to_csv('set.csv', index=False, encoding='utf_8_sig')

search = ('乐高' + set['Set_No']).to_list()

file_name = 'lego_sales'
# update file name
max_page = 2
# update max search page

save(['Product Name', 'Price', 'Sales', 'Shop', 'Search Content'], file_name)
url = 'https://s.taobao.com/search?q=iPad'
driver.get(url)
driver.implicitly_wait(30)
# delay for manual login

for i in search:
    driver.find_element(By.ID, "q").clear()
    # clear search box
    driver.find_element(By.ID, "q").send_keys(i)
    # input search content
    driver.find_element(By.XPATH,
                        '//*[(@id = "J_SearchForm")]//*[contains(concat( " ", @class, " " ), concat( " ", "icon-btn-search", " " ))]').click()
    # click search button
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//*[contains(concat( " ", @class, " " ), concat( " ", "sort", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "link", " " ))]').click()
    # sort sales from high to low
    time.sleep(5)
    get_info(i, driver.current_url, 1, max_page, file_name)
    time.sleep(20)


