from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from data.all_config import Andrew_PATH_driver
import pandas as pd

def chrome_open():
    """
    
    Запускаем Хром
    """
    chrome = webdriver.Chrome(Andrew_PATH_driver)
    return chrome
    
def pages_count(minprice, maxprice):

    page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

    chrome = webdriver.Chrome(Andrew_PATH_driver)
    chrome.minimize_window()
    chrome.get(page_link)

    soup = BeautifulSoup(chrome.page_source, features="html.parser")

    return soup

def links_flat(maxprice, minprice, answer_count_page):
    df_flat_links = pd.DataFrame()
    chrome = webdriver.Chrome(Andrew_PATH_driver)
    chrome.minimize_window()
    for i in range(1, int(answer_count_page)):
        page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'
        chrome.get(page_link)
        soup = BeautifulSoup(chrome.page_source, features="html.parser")
        flat_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--39cNw'])
        flat_list = [link.attrs['href'] for link in flat_links]
        for i in range(len(flat_list)):
            df_flat_links = df_flat_links.append({'links': flat_list[i]}, ignore_index = True)
    return df_flat_links