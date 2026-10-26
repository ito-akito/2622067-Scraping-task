import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urljoin, urlparse, urldefrag

url_list = ['https://www.musashino-u.ac.jp/']
domain = urlparse(url_list[0]).netloc
page_dict = {}

for url in url_list:
    time.sleep(1)

    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        print(f'取得できませんでした：{url}')
        continue

    if urlparse(res.url).netloc != domain:
        continue

    if 'text/html' not in res.headers.get('Content-Type', '').lower():
        continue

    html_soup = BeautifulSoup(res.content, 'html.parser')

    title = html_soup.find('title')

    if title is not None:
        page_dict[url] = title.get_text(strip=True)
    else:
        page_dict[url] = ''

    print(url, page_dict[url])

    a_list = html_soup.find_all('a')

    for a in a_list:
        href = a.get('href')

        if href is not None:
            next_url = urljoin(res.url, href)
            next_url = urldefrag(next_url)[0]
            parsed_url = urlparse(next_url)

            if parsed_url.scheme in ['http', 'https']:
                if parsed_url.netloc == domain:
                    if next_url not in url_list:
                        url_list.append(next_url)

with open('sitemap.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'title'])

    for url, title in page_dict.items():
        writer.writerow([url, title])

print(f'{len(page_dict)}件をsitemap.csvに保存しました。')