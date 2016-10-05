import json
import os
import random
import uuid
from datetime import datetime

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


def random_id():
    return str(uuid.uuid4()).replace('-', '')


def main():
    print('Requesting json...', end="", flush=True)
    cache_url = 'https://arc.msn.com/v3/Delivery/Cache'
    # old 'lo': random.choice([5000, 80000]),
    # return error 'pid': 280810, 280811
    # 'npid':'SubscribedContent-280811'
    data = {'pubid': 'da63df93-3dbc-42ae-a505-b34988683ac7', 'pid': random.choice([209562, 209567, 279978]),
            'adm': 2, 'w': 1, 'h': 1, 'wpx': 1, 'fmt': 'json', 'cltp': 'app', 'dim': 'le', 'rafb': 0, 'ncp': 1, 'pm': 1,
            'cfmt': 'text,image,poly', 'sft': 'jpeg,png,gif', 'topt': 1, 'auid': random_id(), 'ctry': 'CN',
            'time': datetime.now().strftime('%Y%m%dT%H%M%SZ'), 'lc': 'zh-Hans-CN', 'pl': 'zh-Hans-CN,en-US,ja',
            'idtp': 'mid', 'uid': uuid.uuid4(), 'aid': '00000000-0000-0000-0000-000000000000',
            'ua': 'WindowsShellClient/9.0.40929.0 (Windows)', 'asid': random_id(),
            'ctmode': 'ImpressionTriggeredRotation', 'arch': 'x64', 'cdmver': '10.0.14936.1000',
            'devfam': 'Windows.Desktop', 'devform': 'Unknown', 'devosver': '10.0.14936.1000', 'disphorzres': 1920,
            'dispsize': 15.5, 'dispvertres': 1080, 'fosver': 14352, 'isu': 0, 'lo': 510893, 'metered': False,
            'nettype': 'wifi', 'npid': 'LockScreen', 'oemid': 'VMWARE', 'ossku': 'Professional', 'prevosver': 14257,
            'smBiosDm': 'VMware Virtual Platform', 'smBiosManufacturerName': 'VMware, Inc.', 'tl': 4, 'tsu': 6788
            }
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
    for d in ['spotlight\\landscape', 'spotlight\\portrait']:
        if os.path.exists(d) is False:
            os.makedirs(d)
    for i in range(20):
        main()
