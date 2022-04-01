import os
import requests
from lxml import etree
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'referer': 'https://www.mangabz.com/m22238/'}


def main():
    url = input('输入漫画地址:')
    mid = url.strip('htps:/w.mangbzco')
    # print(mid)

    href, titeo, page = getCatalog(url)
    for _href, _page, _titeo in zip(href[::-1], page, titeo[::-1]):
        cid = _href[2:-1]
        pageNum = getPageNum(_href, mid, _page, cid)
        getPhotos(mid, cid, pageNum, _titeo, _page)


def getCatalog(url):
    # url = 'https://www.mangabz.com/279bz'
    htmlCode = etree.HTML(requests.get(url, headers=headers).text)
    href = htmlCode.xpath('//*[@id="chapterlistload"]/a/@href')
    # for each in href:
    #     print(each)
    titeo_old = htmlCode.xpath('//*[@id="chapterlistload"]/a/text()')
    # print(titeo_old)
    titeo_new = []
    for each in titeo_old:
        titeo_new.append(each.strip(' '))
    titeo = [i for i in titeo_new if i != '']
    # for each in titeo:
    #     print(each)
    # print(type(titeo))
    page_old = htmlCode.xpath('//*[@id="chapterlistload"]/a/span/text()')
    page = []
    for each in page_old[::-1]:
        page.append(each.strip('（P）'))

    return href, titeo, page


def getPageNum(href: str, mid, page, cid):
    pageNum = []
    # print(page)
    for each in range(1, int(page) + 1):
        url = f'https://www.mangabz.com{href}chapterimage.ashx?cid={cid}&page={each}'  # Format:url+目录网页去字母+href+加密页数
        # https://www.mangabz.com/m22238/chapterimage.ashx?cid=22238&page=1&key=&_cid=22238&_mid=279&_dt=2020-07-27+01%3A12%3A47&_sign=4f52ff0973c5593d2e6ef090d828a87a
        # print(url)
        text = requests.get(url, headers=headers).text
        # print(text)
        # print(text.split('|')[4:])
        for _text in text.split('|')[4:]:
            # print(_text)
            if '_' in _text:
                pageNum.append(_text)
                # print(pageNum)
    pageNum = list(set(pageNum))

    return pageNum


def getPhotos(mid: str, cid: str, pageNum, titeo, page):
    # https://image.mangabz.com/1/279/22238/16_5310.jpg
    for _pageNum, _page in zip(pageNum, range(1, int(page) + 1)):
        url = f'https://image.mangabz.com/1/{mid}/{cid}/{_pageNum}.jpg'
        # print(url)
        photo = requests.get(url, headers=headers)
        try:
            with open(f'./Downloads/{titeo}/{_pageNum[0]}.jpg', 'wb') as f:
                f.write(photo.content)
        except FileNotFoundError:
            os.makedirs(f'./Downloads/{titeo}')
            with open(f'./Downloads/{titeo}/{_pageNum[0]}.jpg', 'wb') as f:
                f.write(photo.content)

    print('#')


if __name__ == "__main__":
    main()
    time.sleep(1)
