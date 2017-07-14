import json
import os
import sys
import random
import re
import requests


def download(url, path, s):
    print(url, end="", flush=True)
    if os.path.exists(path) is False:
        d = s.get(url)
        if d.status_code == 200:
            with open(path, 'wb+') as f:
                for chunk in d:
                    f.write(chunk)
            print('\tOK')
        else:
            print('\tFailed')
    else:
        print('\tExisted')


def main():
    landscapes, portraits = [], []
    cache_url = 'https://arc.msn.com/v3/Delivery/Cache'
    req = {'pid': random.choice([209562, 209567, 279978]), 'ctry': 'en', 'lc': 'en', 'lo': 510893, 'fmt': 'json'}
    headers = {'User-Agent': ''}
    print('Requesting json...' + str(req['pid']), end="", flush=True)
    r = requests.get(cache_url, params=req, headers=headers)
    if r.status_code == 200:
        data = r.json()['batchrsp']
        if 'items' in data:
            for item in data['items']:
                p = re.compile(r'adData = (.+?);')
                rp = p.findall(item['item'].replace('\n', ''))
                d = json.loads(rp[0])
                landscapes.append(d['ad']['image_fullscreen_001_landscape']['u'])
                portraits.append(d['ad']['image_fullscreen_001_portrait']['u'])
            print('\tOK')

    with requests.Session() as s:
        for url in landscapes:
            name = url.split('/')[7].split('?')[0]
            download(url, sys.path[0] + '\\spotlight\\landscape\\' + name + '.jpg', s)
        for url in portraits:
            name = url.split('/')[7].split('?')[0]
            download(url, sys.path[0] + '\\spotlight\\portrait\\' + name + '.jpg', s)


if __name__ == '__main__':
    for di in [sys.path[0] + '\\spotlight\\landscape', sys.path[0] + '\\spotlight\\portrait']:
        if os.path.exists(di) is False:
            os.makedirs(di)
    for i in range(20):
        main()
