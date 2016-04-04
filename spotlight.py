import requests
import json
import os


def main():
    print('Requesting json...', end="" ,flush=True)
    json_url = 'https://arc.msn.com/v3/Delivery/Cache?pid=209567&fmt=json&rafb=0&ua=WindowsShellClient%2F0&lo=5000'
    images = []
    r = requests.get(json_url)
    if r.status_code == 200:
        for item in r.json()['batchrsp']['items']:
            d = json.loads(item['item'])
            images.append(d['ad']['image_fullscreen_001_landscape']['u'])
            images.append(d['ad']['image_fullscreen_001_portrait']['u'])
        print('\tOK')

    with requests.Session() as s:
        for url in images:
            file_path = 'spotlight\\' + url.split('/')[3] + '.jpg'
            if os.path.exists(file_path) is False:
                d = s.get(url)
                if d.status_code == 200:
                    with open(file_path, 'wb+') as f:
                        for chunk in d:
                            f.write(chunk)
                    print(url + '\tOK')


if __name__ == '__main__':
    if os.path.exists('spotlight') is False:
            os.makedirs('spotlight')
    count = 0
    while count < 20:
        main()
        count += 1
