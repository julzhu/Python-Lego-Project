from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
import csv


driver = webdriver.Chrome()

def get_info(i, url, page, max_page, file_name):
    page = page + 1
    driver.get(url)
    driver.implicitly_wait(10)
    selector = etree.HTML(driver.page_source)
    infos = selector.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "J_MouserOnverReq", " " ))]')
    print(len(infos))
    # select product element

    for info in infos:
        product_name = info.xpath('div/div/div/a/img/@alt')[0]
        print(product_name)
        price = info.xpath('div[2]/div/div/strong/text()')[0]
        print(price)
        sales = info.xpath('div[2]/div/div[@class="deal-cnt"]/text()')[0]
        print(sales)
        shop = info.xpath('div[2]/div[3]/div/a/span[2]/text()')[0]
        print(shop)
        file = [product_name, price, sales, shop, i]
        save(file, file_name)

    if page <= max_page:
        NextPage(i, url, page, max_page, file_name)
    else:
        pass

    '''
    for info in infos:
        product_name = info.xpath('//*[(@id = "mainsrp-itemlist")]//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')[0]
        print(product_name)
        price = info.xpath('//strong')[0]
        print(price)
        sales = info.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "deal-cnt", " " ))]')[0]
        print(sales)
        shop = info.xpath('//*+[contains(concat( " ", @class, " " ), concat( " ", "dsrs", " " ))]//span')[0]
        print(shop)
        file = [product_name, price, sales, shop, i]
        save(file, file_name)
    '''

def save(item, file_name):
    with open(f'{file_name}.csv', 'a+', encoding='utf_8_sig', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(item)

def roll_window_to_bottom(browser, stop_length=None, step_length=500):
    original_top = 0
    while True:
        if stop_length:
            if stop_length - step_length < 0:
                browser.execute_script("window.scrollBy(0,{})".format(stop_length))
                break
            stop_length -= step_length
        browser.execute_script("window.scrollBy(0,{})".format(step_length))
        time.sleep(1)
        check_height = browser.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        if check_height == original_top:
            break
        original_top = check_height

def NextPage(i, url, page, max_page, file_name):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'//a[@trace="srp_bottom_pagedown"]').click()
    time.sleep(4)
    get_info(i, driver.current_url, page, max_page, file_name)


