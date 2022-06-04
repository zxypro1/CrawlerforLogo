from bs4 import BeautifulSoup
from selenium import webdriver
import time
from lxml import etree
import requests
import re
import time


class Crawler(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.75 Safari/537.36',
        }
        self.url = 'http://www.bbsnet.com/doutu'

    def run(self):
        pass

    def get_target_urls(self):
        pass

    def get_target_images(self, target_urls):
        pass


if __name__ == '__main__':
    crawler = Crawler()
    test_url = 'https://lordicon.com/icons/wired/outline?categoryId=3&premium=0'
    # test_url = 'https://baidu.com'
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.get(test_url)
    print(driver.find_element('content').text)
    driver.close()
    # r = requests.get(test_url)
    # html_response = r.text
    #
    # soup = BeautifulSoup(html_response, 'html.parser')
    # print(soup)
    #
    # category = soup.find('div')
    # print(category)

