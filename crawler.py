from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def get_js(script, driver):
    result = driver.execute_script(script)
    return result


def close_anti_crawler(driver):
    t = driver.find_elements(By.TAG_NAME, 'lord-icon')
    print(len(driver.find_elements(By.TAG_NAME, 'lord-icon')))
    for i in t:
        if i.get_attribute('icon') == 'main-close':
            i.click()
            break


if __name__ == '__main__':
    all_format = ['gif', 'lottie', 'svg']
    # crawler = Crawler()
    test_url = 'https://lordicon.com/icons/wired/outline?categoryId=3&premium=0'
    # test_url = 'https://baidu.com'
    driver = webdriver.Edge(executable_path='msedgedriver.exe')

    driver.get(test_url)
    time.sleep(8)
    t = driver.find_elements(By.TAG_NAME, 'lord-icon')
    print(len(driver.find_elements(By.TAG_NAME, 'lord-icon')))
    for i in t:
        if i.get_attribute('icon') == 'main-close':
            i.click()
            break

    time.sleep(2)
    # t = driver.find_element(By.TAG_NAME, 'lord-icon-library-sidebar')
    js = "document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
         "'container').getElementsByClassName('category')[0].getElementsByTagName('div')[1].click()"
    driver.execute_script(js)

    js = "return document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
         "'container').getElementsByClassName('category')[1]"
    t = driver.execute_script(js)
    print(t)

    for i in range(3):
        for category in t.find_elements(By.TAG_NAME, 'div'):
            category.click()
            js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
                 "'container').getElementsByClassName('icons')[0].children"
            icons = get_js(js, driver)
            for icon in icons:
                time.sleep(8)
                close_anti_crawler(driver)
                icon.click()
                time.sleep(1)
                close_anti_crawler(driver)
                js = "return document.querySelector('lord-icon-library-editor').shadowRoot.querySelectorAll(" \
                     "'lord-icon-button')[5] "
                more = get_js(js, driver)
                count = 0
                while more.get_attribute('class') == 'inactive':
                    time.sleep(1)
                    count += 1
                    if count % 20 == 0:
                        driver.refresh()
                        time.sleep(8)

                close_anti_crawler(driver)
                more.click()
                time.sleep(1)
                js = "return document.getElementsByClassName('cols')[1].getElementsByClassName('btn-items-alt')"
                types = get_js(js, driver)
                for type in types:
                    quit = 0
                    for formt in type.find_elements(By.TAG_NAME, 'a'):
                        if formt.get_attribute('data-type') == all_format[i]:
                            formt.click()
                            time.sleep(1)
                            download = driver.find_element(By.TAG_NAME, 'lord-icon-button')
                            download.click()
                            time.sleep(2)
                            quit = 1
                            break
                    if quit == 1:
                        break

    time.sleep(5)
    driver.close()
    # r = requests.get(test_url)
    # html_response = r.text
    #
    # soup = BeautifulSoup(html_response, 'html.parser')
    # print(soup)
    #
    # category = soup.find('div')
    # print(category)
