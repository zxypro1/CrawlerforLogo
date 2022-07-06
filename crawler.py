import os

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
        self.all_format = ['gif', 'lottie', 'svg']
        self.test_url = 'https://lordicon.com/icons/system/outline?categoryId=143&premium=0'
        self.driver = webdriver.Edge(executable_path='msedgedriver.exe')
        self.downloaded_list = [[], [], []]
        self.delete_list = [112, 12, 2030, 478, 61, 63, 2023, 2024, 2029, 1167, 1186, 350, 351, 352, 353, 354, 356, 357,
                            358, 359, 360, 362, 363, 364, 365, 366, 367, 368, 369, 1037, 1595, 1702, 1923, 1934, 1940,
                            1944, 1947, 1954, 1958, 1984, 482, 486, 290, 501, 798, 955, 1534, 1918, 1920, 1922, 1935,
                            497, 498, 243, 1305, 1309, 1312, 744, 1788, 1953, 2234, 1736, 1787, 1827, 1838, 1167, 1339,
                            11, 2235, 860, 1979, 1106, 120, 540, 428, 1614, 1650, 1730, 447, 1337, 438, 105, 331, 332,
                            334, 18, 188, 1097, 1931, 1807, 1948, 382, 1754, 58, 9, 32, 19, 44, 5, 68, 23, 1, 6]

    def get_js(self, script, driver):
        result = driver.execute_script(script)
        return result

    def get_downloaded_list(self):
        return self.downloaded_list

    def create_dir(self, dir_name):
        if os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name

    def accept_cookie(self):
        print('关闭cookie')
        t = self.driver.find_elements(By.TAG_NAME, 'a')
        for i in t:
            if i.get_attribute('data-type') == 'agree':
                i.click()
                break

    def close_anti_crawler(self, driver):
        t = driver.find_elements(By.TAG_NAME, 'lord-icon')
        print('检查是否弹窗')
        # print(len(driver.find_elements(By.TAG_NAME, 'lord-icon')))
        for i in t:
            if i.get_attribute('icon') == 'main-close':
                i.click()
                break

    def restart(self):
        print('重启任务！！')
        self.driver = webdriver.Edge(executable_path='msedgedriver.exe')
        self.run_once()

    def get_downloaded_list_from_files(self):
        print('获取已下载的文件id')
        index = 0
        for form in self.all_format:
            root_dir = '.\\{}'.format(form)
            for parent, _, names in os.walk(root_dir):
                for name in names:
                    try:
                        self.downloaded_list[index].append(int(name.split('-')[0]))
                    except:
                        self.downloaded_list[index].append(int(name.split('_')[0]))
            index += 1
        print(self.downloaded_list)

    def run_once(self):
        print('------------开始运行----------------')
        self.get_downloaded_list_from_files()
        self.driver.get(self.test_url)
        time.sleep(8)
        t = self.driver.find_elements(By.TAG_NAME, 'lord-icon')
        print(len(self.driver.find_elements(By.TAG_NAME, 'lord-icon')))
        for i in t:
            if i.get_attribute('icon') == 'main-close':
                i.click()
                break

        time.sleep(2)
        self.accept_cookie()
        # t = driver.find_element(By.TAG_NAME, 'lord-icon-library-sidebar')
        js = "document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
             "'container').getElementsByClassName('category')[0].getElementsByTagName('div')[1].click()"
        self.driver.execute_script(js)

        js = "return document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
             "'container').getElementsByClassName('category')[1]"
        t = self.driver.execute_script(js)
        print(t)

        for i in range(3):
            print('当前任务：' + self.all_format[i])
            try:
                for category in t.find_elements(By.TAG_NAME, 'div'):
                    self.close_anti_crawler(self.driver)
                    category.click()
                    time.sleep(4)
                    # self.path = self.create_dir()
                    self.close_anti_crawler(self.driver)
                    js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
                         "'container').getElementsByClassName('icons')[0].children"
                    icons = self.get_js(js, self.driver)
                    for icon in icons:
                        idx = icons.index(icon)
                        js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
                             "'container').getElementsByClassName('icons')[0].children[{}].children[0].getAttribute(" \
                             "'icon')".format(idx)
                        icon_id = int(self.get_js(js, self.driver).split('-')[0])
                        if icon_id in self.downloaded_list[i] or icon_id in self.delete_list:
                            continue
                        time.sleep(8)
                        self.close_anti_crawler(self.driver)
                        icon.click()
                        time.sleep(1)
                        self.close_anti_crawler(self.driver)
                        js = "return document.querySelector('lord-icon-library-editor').shadowRoot.querySelectorAll(" \
                             "'lord-icon-button')[5] "
                        more = self.get_js(js, self.driver)
                        count = 0
                        while more.get_attribute('class') == 'inactive':
                            time.sleep(1)
                            count += 1
                            print('无响应，重启中：' + str(count))
                            time.sleep(2)
                            self.restart()
                            self.driver.close()
                            break

                        self.close_anti_crawler(self.driver)
                        more.click()
                        time.sleep(1)
                        js = "return document.getElementsByClassName('cols')[1].getElementsByClassName('btn-items-alt')"
                        types = self.get_js(js, self.driver)
                        for type in types:
                            quit = 0
                            for formt in type.find_elements(By.TAG_NAME, 'a'):
                                if formt.get_attribute('data-type') == self.all_format[i]:
                                    formt.click()
                                    time.sleep(1)
                                    if self.all_format[i] == 'gif':
                                        download = self.driver.find_element(By.TAG_NAME, 'lord-icon-button')
                                        download.click()
                                    time.sleep(2)
                                    self.close_anti_crawler(self.driver)
                                    quit = 1
                                    break
                            if quit == 1:
                                self.downloaded_list[i].append(icon_id)
                                break
            except Exception as result:
                print(result)
                self.restart()
            time.sleep(5)
        print('爬取完成！')
        self.driver.close()


# def get_js(script, driver):
#     result = driver.execute_script(script)
#     return result
#
#
# def close_anti_crawler(driver):
#     t = driver.find_elements(By.TAG_NAME, 'lord-icon')
#     print(len(driver.find_elements(By.TAG_NAME, 'lord-icon')))
#     for i in t:
#         if i.get_attribute('icon') == 'main-close':
#             i.click()
#             break


if __name__ == '__main__':
    crawler = Crawler()
    crawler.run_once()
    # all_format = ['gif', 'lottie', 'svg']
    # # crawler = Crawler()
    # test_url = 'https://lordicon.com/icons/wired/outline?categoryId=3&premium=0'
    # # test_url = 'https://baidu.com'
    # driver = webdriver.Edge(executable_path='msedgedriver.exe')
    #
    # driver.get(test_url)
    # time.sleep(8)
    # t = driver.find_elements(By.TAG_NAME, 'lord-icon')
    # print(len(driver.find_elements(By.TAG_NAME, 'lord-icon')))
    # for i in t:
    #     if i.get_attribute('icon') == 'main-close':
    #         i.click()
    #         break
    #
    # time.sleep(2)
    # # t = driver.find_element(By.TAG_NAME, 'lord-icon-library-sidebar')
    # js = "document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
    #      "'container').getElementsByClassName('category')[0].getElementsByTagName('div')[1].click()"
    # driver.execute_script(js)
    #
    # js = "return document.querySelector('lord-icon-library-sidebar').shadowRoot.getElementById(" \
    #      "'container').getElementsByClassName('category')[1]"
    # t = driver.execute_script(js)
    # print(t)
    #
    # for i in range(3):
    #     for category in t.find_elements(By.TAG_NAME, 'div'):
    #         category.click()
    #         js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
    #              "'container').getElementsByClassName('icons')[0].children"
    #         icons = get_js(js, driver)
    #         for icon in icons:
    #             idx = icons.index(icon)
    #             js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
    #                  "'container').getElementsByClassName('icons')[0].children[{}].children[0].getAttribute(" \
    #                  "'icon')".format(idx)
    #             icon_id = int(get_js(js, driver).split('-')[0])
    #             if ((icon_id <= 500 and i == 0) or (icon_id in self.downloaded_list)):
    #                 break
    #             time.sleep(8)
    #             close_anti_crawler(driver)
    #             icon.click()
    #             time.sleep(1)
    #             close_anti_crawler(driver)
    #             js = "return document.querySelector('lord-icon-library-editor').shadowRoot.querySelectorAll(" \
    #                  "'lord-icon-button')[5] "
    #             more = get_js(js, driver)
    #             count = 0
    #             while more.get_attribute('class') == 'inactive':
    #                 time.sleep(1)
    #                 count += 1
    #                 if count % 20 == 0:
    #                     driver.refresh()
    #                     time.sleep(8)
    #
    #             close_anti_crawler(driver)
    #             more.click()
    #             time.sleep(1)
    #             js = "return document.getElementsByClassName('cols')[1].getElementsByClassName('btn-items-alt')"
    #             types = get_js(js, driver)
    #             for type in types:
    #                 quit = 0
    #                 for formt in type.find_elements(By.TAG_NAME, 'a'):
    #                     if formt.get_attribute('data-type') == all_format[i]:
    #                         formt.click()
    #                         time.sleep(1)
    #                         download = driver.find_element(By.TAG_NAME, 'lord-icon-button')
    #                         download.click()
    #                         time.sleep(2)
    #                         quit = 1
    #                         break
    #                 if quit == 1:
    #                     break
    #
    # time.sleep(5)
    # driver.close()
