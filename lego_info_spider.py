from tb_utils import *

i = '乐高官方旗舰店'
# update search content
file_name = 'lego_info'
# update file name
max_page = 20
# update max search page

save(['Product Name', 'Price', 'Sales', 'Shop', 'Search Content'], file_name)
url = 'https://s.taobao.com/search?q=iPad'
driver.get(url)
driver.implicitly_wait(30)
# delay for manual login

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
