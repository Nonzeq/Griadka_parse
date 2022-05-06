import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep


def get_total_papes(url):
    soup = BeautifulSoup(url, 'lxml')
    try:
        pages_total = soup.find('p', id='toolbar-amount').find_all('span', class_='toolbar-number')[-1].text
        pages_mount = soup.find('p', id='toolbar-amount').find_all('span', class_='toolbar-number')[1].text
    except:
        count = 0
        return int(count)
    if int(pages_total) / int(pages_mount) != 0 and pages_total:
        count = int(pages_total) / int(pages_mount)
        return int(count+2)
    else:
        count = int(pages_total) / int(pages_mount)
        return int(count)



def get_all_parse_url(html):

    soup = BeautifulSoup(html, 'lxml')
    href = soup.find('ul', class_='togge-menu list-category-dropdown').find_all('a', class_='level-top')

    for i in href:
        url.append(i.get('href'))



def get_all_url_of_items(html):
    soup = BeautifulSoup(html, 'lxml')
    href = soup.find('div', id='layered-ajax-list-products').find_all('a', class_='product-item-link')

    for i in href:
        url_items.append(i.get('href'))


def get_start_html():
    url = 'https://gradka.com.ua'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    r = requests.get(url, headers=headers)
    return r.text


def get_site_html(url, p=0):
    p = '?p=' + str(p)
    url = url+p
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    r = requests.get(url,headers=headers)
    return r.text



def get_item_page_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    r = requests.get(url, headers=headers)
    return r.text


# def get_price(html):
#     soup = BeautifulSoup(html, 'lxml')
#     items = soup.find('div', id='layered-ajax-list-products').find_all('div', class_='item-product')
#
#     for pr in items:
#         title = pr.find('a', class_='product-item-link').text.replace('\t', '')
#         price = pr.find('span', class_='price').text.replace('\xa0', '')
#         data.append([title, price])
#     return data




def get_price(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='box-inner1')
    try:
        title = items.find('span', class_='base').text.replace('\t', '')
    except:
        title = '-'
    try:
        price = items.find('span', class_='price').text.replace('\xa0', '')
    except:
        price = '-'
    try:
        sku = items.find('div', itemprop='sku').text
    except:
        sku = '-'
    try:
        description = items.find('div', class_='product attribute overview').find('p').text
    except:
        description = '-'

    data.append([title, price, sku, description])
    return data

data = []
url = []
url_items = []
header = ['title', 'price', 'sku', 'description']


def main():
    get_all_parse_url(get_start_html())  #get all category url from site
    print('Йде збирання данних....')

    for u in url:
        count = get_total_papes(get_site_html(u))
        if count == 0:
            count = 2
        for p in range(1,count):
            get_all_url_of_items(get_site_html(u,p))
            # out = get_price(get_site_html(u,p))
            print('Збираю URL')
            sleep(1)


    for i in url_items:
        out = get_price(get_item_page_html(i))
        sleep(1)
        print('Збираю TITLE , PRICE, SKU, DESCRIPTION')

    df = pd.DataFrame(out, columns=header)
    df.to_excel('/home/bogdan/CirclePaprse/data.xlsx', index=False, encoding='utf8')
    print('ГОТОВО!')





if __name__ == '__main__':
    main()

