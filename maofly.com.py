from os import path, mkdir
import requests
import lzstring
import json
import re


def GetPhotosUrl(comicUrl):
    domain = 'https://www.maofly.com/uploads/'
    response = requests.get(comicUrl)
    response.encoding = "utf-8"
    chapterNum = re.findall(r"data-chapter_num=\"(.*?)\"", response.text)[0]
    chapterType = re.findall(r"data-chapter-type=\"(.*?)\"", response.text)[0]
    imgData = re.findall(r"img_data = \"(.*?)\"", response.text)[0]
    x = lzstring.LZString()
    imgDataArr = x.decompressFromBase64(imgData).split(',')
    imgUrlArr = [domain + path for path in imgDataArr]
    return imgUrlArr, chapterNum, chapterType


def DownPhotos(ImgUrl, chapterNum):
    img = requests.get(ImgUrl).content
    pageName = ImgUrl.split('/', )[-1]
    if not path.exists(f'./Downloads/maofly/{chapterNum}/'):
        mkdir(f'./Downloads/maofly/{chapterNum}/')
    with open(f'./Downloads/maofly/{chapterNum}/{pageName}', 'wb') as f:
        f.write(img)


def GetNextPageUrl(chapterNum, chapterType):
    url = f"https://www.maofly.com/chapter_num?chapter_id={chapterNum}&ctype=1&type={chapterType}"
    response = requests.get(url)
    pageUrl = json.loads(response.content)["url"]
    return pageUrl


def main():
    url = 'https://www.maofly.com/manga/34453/416030.html'
    if not path.exists(f'./Downloads/maofly'):
        mkdir(f'./Downloads/maofly')
    while url != "":
        imgUrlArr, chapterNum, chapterType = GetPhotosUrl(url)
        for imgUrl in imgUrlArr:
            DownPhotos(imgUrl, chapterNum)
        url = GetNextPageUrl(chapterNum, chapterType)
        print("#")


if __name__ == "__main__":
    main()
