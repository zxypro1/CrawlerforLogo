import requests

json_count = 0
url = 'https://lordicon.com/api/library/icon/3418/download'
directory = r'C:\icons'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
}

requests.get('https://lordicon.com/api/library/icon/3418/download', headers=header)
