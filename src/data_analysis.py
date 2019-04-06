import jieba
import csv
import pandas
import os
import glob
import numpy
import json
# from pyhanlp import *
import jieba.posseg as pseg
number_class_dict = {
    "26": "中国儿童文学",
    "27": "外国儿童文学",
    "70": "绘本图画书",
    "05": "科普百科",
    "44": "婴儿读物",
    "45": "幼儿启蒙",
    "46": "益智游戏",
    "48": "玩具书",
    "50": "卡通动漫",
    "51": "少儿英语",
    "55": "励志成长",
    "57": "进口儿童书",
    "69": "少儿期刊",
    "59": "阅读工具书"}

class_number_dict = {v:k for k,v in number_class_dict.items()}
# file_list = glob.glob('./data/*.txt')
file_name_list = [os.path.basename(x) for x in glob.glob('./data/*.txt')]

def main():
    for file in file_name_list:
        print(file)
        for line in open('./data/'+file):
            # json.load(line).get('author'
            print(json.loads(line).get('author'))
            author = json.loads(line).get('author')
            if not author:
                continue
            # author = "美国培生教育出版集团"
            words = pseg.cut(author)
            for word, flag in words:
                if flag not in ["nr", "nrt", "ns"]:
                    continue
                print('%s %s' % (word, flag))
    # print(pseg.cut("我爱北京天安门"))
    # for term in HanLP.segment('下雨天地面积水'):
    #     if
    #     print('{}\t{}'.format(term.word, term.nature)) # 获取单词与词性

        # name = file.split('-')
        # file_name_list.get(str(name[0])) = {

        # }


    # replace('.txt', '')
    # print(file_list)
if __name__ == '__main__':
    main()