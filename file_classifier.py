import os
import shutil

from selenium import webdriver
import time
from selenium.webdriver.common.by import By


class FileClassifier(object):
    def __init__(self):
        self.path = '.\\lordicon\\'
        self.driver = webdriver.Edge(executable_path='msedgedriver.exe')
        self.urls = ['https://lordicon.com/icons/system/outline?categoryId=143&premium=0',
                     'https://lordicon.com/icons/wired/outline?categoryId=8&premium=0']
        self.all_format = ['gif', 'lottie', 'svg']
        self.file_list = [[], [], []]
        self.delete_list = [112, 12, 2030, 478, 61, 63, 2023, 2024, 2029, 1167, 1186, 350, 351, 352, 353, 354, 356, 357,
                            358, 359, 360, 362, 363, 364, 365, 366, 367, 368, 369, 1037, 1595, 1702, 1923, 1934, 1940,
                            1944, 1947, 1954, 1958, 1984, 482, 486, 290, 501, 798, 955, 1534, 1918, 1920, 1922, 1935,
                            497, 498, 243, 1305, 1309, 1312, 744, 1788, 1953, 2234, 1736, 1787, 1827, 1838, 1167, 1339,
                            11, 2235, 860, 1979, 1106, 120, 540, 428, 1614, 1650, 1730, 447, 1337, 438, 105, 331, 332,
                            334, 18, 188, 1097, 1931, 1807, 1948, 382, 1754, 58, 9, 32, 19, 44, 5, 68, 23, 1, 6]
        self.unwashed_files = []
        self.dic = {}
        self.get_unwashed_files()

    def create_dir(self, dir_name):
        if not os.path.exists(self.path + dir_name):
            os.makedirs(self.path + dir_name)

    def accept_cookie(self):
        print('关闭cookie')
        t = self.driver.find_elements(By.TAG_NAME, 'a')
        for i in t:
            if i.get_attribute('data-type') == 'agree':
                i.click()
                break

    def get_js(self, script, driver):
        result = driver.execute_script(script)
        return result

    def delete_files(self):
        print('删除不适用的文件')
        for form in self.all_format:
            root_dir = '.\\{}'.format(form)
            for parent, _, names in os.walk(root_dir):
                for name in names:
                    try:
                        if int(name.split('-')[0]) in self.delete_list or int(
                                name.split('-')[0]) not in self.unwashed_files:
                            os.remove(os.path.join(parent, name))
                    except:
                        if int(name.split('_')[0]) in self.delete_list or int(
                                name.split('_')[0]) not in self.unwashed_files:
                            os.remove(os.path.join(parent, name))

    def get_unwashed_files(self):
        print('获取未清洗文件列表')
        root_dir = ".\\svg"
        for parent, _, names in os.walk(root_dir):
            for name in names:
                self.unwashed_files.append(int(name.split('-')[0]))

    def get_downloaded_list_from_files(self):
        print('获取已下载的文件id')
        index = 0
        for form in self.all_format:
            root_dir = '.\\{}'.format(form)
            for parent, _, names in os.walk(root_dir):
                for name in names:
                    self.file_list[index].append(int(name.split('-')[0]))
            index += 1
        print(self.file_list)

    def get_categories(self):
        for url in self.urls:
            print('------------开始运行----------------')
            self.driver.get(url)
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
            for category in t.find_elements(By.TAG_NAME, 'div'):
                category.click()
                time.sleep(2)
                dir_name = category.text.split('\n')[0]
                self.dic[dir_name] = []
                self.create_dir(dir_name)
                js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
                     "'container').getElementsByClassName('icons')[0].children"
                icons = self.get_js(js, self.driver)
                for icon in icons:
                    idx = icons.index(icon)
                    js = "return document.querySelector('lord-icon-library-icons').shadowRoot.getElementById(" \
                         "'container').getElementsByClassName('icons')[0].children[{}].children[0].getAttribute(" \
                         "'icon')".format(idx)
                    icon_id = int(self.get_js(js, self.driver).split('-')[0])
                    self.dic[dir_name].append(icon_id)

                for form in self.all_format:
                    root_dir = '.\\{}'.format(form)
                    for parent, _, names in os.walk(root_dir):
                        for name in names:
                            if int(name.split('-')[0]) in self.dic[dir_name]:
                                shutil.copy(parent + '\\' + name, self.path + dir_name + '\\' + name)

                print('{}分类完成，共{}个。'.format(dir_name, len(self.dic[dir_name])))
                time.sleep(2)

            print('分类完成')


if __name__ == '__main__':
    files_classifier = FileClassifier()
    files_classifier.get_categories()
    # unwashed_files = []
    # root_dir = ".\\gif"
    # for parent, _, names in os.walk(root_dir):
    #     for name in names:
    #         unwashed_files.append(int(name.split('-')[0]))
    #
    # print(len(unwashed_files))
    #
    # root_dir = ".\\svg"
    # for parent, _, names in os.walk(root_dir):
    #     for name in names:
    #         if int(name.split('-')[0]) not in unwashed_files:
    #             print(int(name.split('-')[0]))
