import json
import os
import random
import requests


def download(url, path, s):
    if os.path.exists(path) is False:
        d = s.get(url)
        if d.status_code == 200:
            with open(path, 'wb+') as f:
                for chunk in d:
                    f.write(chunk)
            print(url + '\tOK')


def main():
    print('Requesting json...', end="", flush=True)
    cache_url = 'https://arc.msn.com/v3/Delivery/Cache'
    data = {'pid': random.choice([209562, 209567, 279978]), 'fmt': 'json', 'rafb': 0, 'ua': 'WindowsShellClient/0',
            'lo': random.choice([5000, 80000])}
    landscapes, portraits = [], []
    r = requests.get(cache_url, params=data)
    if r.status_code == 200:
        for item in r.json()['batchrsp']['items']:
            d = json.loads(item['item'])
            landscapes.append(d['ad']['image_fullscreen_001_landscape']['u'])
            portraits.append(d['ad']['image_fullscreen_001_portrait']['u'])
        print('\tOK')

    with requests.Session() as s:
        for url in landscapes:
            download(url, 'spotlight\\landscape\\' + url.split('/')[3] + '.jpg', s)
        for url in portraits:
            download(url, 'spotlight\\portrait\\' + url.split('/')[3] + '.jpg', s)


if __name__ == '__main__':
    for dir in ['spotlight\\landscape', 'spotlight\\portrait']:
        if os.path.exists(dir) is False:
            os.makedirs(dir)
    count = 0
    while count < 20:
        main()
        count += 1
