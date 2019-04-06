import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
import random

class_dict = {
    "26": "中国儿童文学",
    "27": "外国儿童文学",
    "70": "绘本-图画书",
    "05": "科普百科",
    "44": "婴儿读物",
    "45": "幼儿启蒙",
    "46": "益智游戏",
    "48": "玩具书",
    "50": "卡通-动漫",
    "51": "少儿英语",
    "55": "励志-成长",
    "57": "进口儿童书",
    "69": "少儿期刊",
    "59": "阅读工具书"}


def get_page(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    time.sleep(random.randint(0, 30))
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    return str(soup.find("ul", class_="bang_list clearfix bang_list_mode"))


def parse_one_page(html):
    pattern = re.compile(
        '<a\shref="http://search.dangdang.com/\?key=%.*?target="_blank">(.*?)</a></div>.*?', re.S)
    items = re.findall(pattern, html)
    author_list = []
    soup = BeautifulSoup(html)
    index_list = list(
        map(lambda x: x.string, soup.find_all("div", class_="list_num")))
    link_list = list(map(lambda x: x.find("a").get("href"),
                         soup.find_all("div", class_="name")))
    book_name_list = list(map(lambda x: x.find("a").get(
        "title"), soup.find_all("div", class_="name")))
    try:
        author_list = list(filter(None, list(map(lambda x: x.find("a").get(
            "title"), soup.find_all("div", class_="publisher_info")))))
    except:
        for s in soup.find_all("div", class_="publisher_info"):
            try:
                if s.find("a").get("title"):
                    author_list.append(s.find("a").get("title"))
            except:
                author_list.append(None)
    publish_soup = list(filter(None, list(map(lambda x: x.find(
        "span"), soup.find_all("div", class_="publisher_info")))))
    publish_date_list = list(map(lambda x: str(x).replace(
        '<span>', '').replace('</span>', ''), publish_soup))
    if len(publish_date_list) != len(index_list):  # TODO Change to True judgment
        x = len(index_list)
        publish_date_list.append(None)
    publishment_list = []

    try:
        publishment_list = list(map(lambda x: x.find(
            "a").string, soup.find_all("div", class_="publisher_info")))[1::2]
    except:
        for s in soup.find_all("div", class_="publisher_info"):
            try:
                if s.find("a").string:
                    publishment_list.append(s.find("a").string)
            except:
                publishment_list.append(None)
        publishment_list = publishment_list[1::2]

    number_of_people_list = list(map(lambda x: x.find(
        "a").string, soup.find_all("div", class_="star")))
    print(publishment_list)
    print("index num is ", len(index_list))
    print("publishment num is ", len(publishment_list))
    print("items num is ", len(items))
    for y in range(len(index_list)):
        try:
            if len(publishment_list) < len(items):
                yield {
                    'index': index_list[y],
                    'link': link_list[y],
                    'title': book_name_list[y],
                    'author': author_list[y],
                    'date': publish_date_list[y],
                    'publishment': items[y],
                    'number_of_people': number_of_people_list[y]
                }
            elif len(publishment_list) >= len(items):
                yield {
                    'index': index_list[y],
                    'link': link_list[y],
                    'title': book_name_list[y],
                    'author': author_list[y],
                    'date': publish_date_list[y],
                    'publishment': publishment_list[y],
                    'number_of_people': number_of_people_list[y]
                }
        except:
            yield {}


def write_to_file(content, file_name):
    with open('./data/'+file_name+'.txt', 'a', encoding='utf-8') as f:
        # print(content)
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    year_list = ["2016", "2017", "2018"]

    for year in year_list:
        for class_ in class_dict.keys():
            for i in range(25):
                # TODO add interrupt continuation in here
                # if year == "2016" and class_ in ["26", "27", "70", "05", "44", "45", "46", "48"]:
                #     continue
                url = 'http://bang.dangdang.com/books/childrensbooks/01.41.' + \
                    str(class_)+'.00.00.00-year-'+year + \
                    '-0-1-' + str(i + 1) + '-bestsell'
                print(url)
                html = get_page(url)
                for item in parse_one_page(html):
                    file_name = str(class_dict.get(class_)) + '-' + str(year)
                    write_to_file(item, file_name)


if __name__ == '__main__':
    main()
