import json

import requests
import os


class IconSpider(object):
    def __init__(self):
        self.json_count = 0
        self.url = 'https://lordicon.com/icons/wired/outline'
        self.directory = r'C:\icons'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
        }

    def create_directory(self, name):
        self.directory = self.directory.format(name)

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += r'\{}'

    def get_image_link(self, url):
        list_image_link = []
        str_html = requests.get(url, headers=self.header)
        json_info = json.loads(str_html.text)

    def save_image(self, img_link, filename):
        res = requests.get(img_link, headers=self.header)
        if res.status_code == 404:
            print(f'图片{img_link}下载出错-----------')
        with open(filename, "wb") as f:
            f.write(res.content)
            print('存储路径：' + filename)

    def run(self):
        pic_number = 0
        for index in range(self.json_count):
            


