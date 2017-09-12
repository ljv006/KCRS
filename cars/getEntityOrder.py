#coding=utf-8
import re
import os
import sys
import jieba
import jieba.posseg as pseg
reload(sys)
sys.setdefaultencoding('utf-8')

posWord = ["省心","好看", "大", "舒适","好","多","轻盈", "稳定", "下降","精准", "满意", "省","省油","高兴", "低", "高", "值得", "无敌", "给力", "靓丽"]
neuWord = ["差不多","没有区别","没区别","接近","没差别","不相上下"]
negWord = ["差","坏","不适应","模糊", "耗油"]

keywords = []
dict = {}
d = open("dict.txt",'rb')
count = 0#车型数量

#建立关键词表
#有比的关系
#没有比的关系
#其他（取0）
def judgeSentiment(sent):
    words = pseg.cut(sent)
    filteredWords = []
    for w in words:
        flag = w.flag
        tmp = w.word
        if len(tmp) > 1 and len(flag) > 0 and flag[0] not in filter_list and tmp[0] >= u'/u4e00' and tmp[0] <= u'\u9fa5':
            filteredWords.append(w.word)
    for word in filteredWords:
        if word in posWord:
            return 1
        if word in neuWord:
            return 0
        if word in negWord:
            return -1

for item in d:
    temp = item.replace("\r\n","")
    keywords.append(temp)
    dict[temp] = count
    count += 1
dir_list = ["comments1","comments2", "comments3", "comments4"]
cnt = 0
total = 0
for dir in dir_list:
    walk = os.walk(os.path.realpath(dir))
    log = open("order_log.txt", "ab")
    out = []
    filter_list = ['t','q','p','u','e','y','o','w','m']
    for root, dirs, files in walk:
        for file in files:
            f = open(os.path.join(root, file), 'rb')
            file = file[:-4]
            n = dict[file]  # 源车型标记
            entity1 = keywords[n]
            #print "entity1: " + entity1
            t = 0
            for line in f:
                if len(line) <= 2:
                    continue
                line = line.replace("\r\n", "")
                if line in keywords:
                    t = dict[line]  # 目标车型标记
                    continue
                entity2 = keywords[t]
                #print "entity2: " + entity2
                data = line.split('###')
                label = data[0]
                sentence = data[1]
                #flag=1:en1,en2
                #flag=-1:en2,en1
                #flag=0:en1和en2的关系顺序不重要
                flag = 1
                regex1 = ur"([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)(%s)([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)" % (entity1.decode("utf-8"))
                rr = re.compile(regex1)
                m1 = rr.search(sentence.decode("utf-8"))
                if m1:
                    relationStr = m1.group(0)
                    if relationStr.__contains__('比不了') or relationStr.__contains__('比不上'):
                        flag = 1
                    elif relationStr.__contains__('比'):
                        regex1 = ur"(比)([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)"
                        rr = re.compile(regex1)
                        m1 = rr.search(relationStr)
                        sentence = m1.group(0)
                        res = judgeSentiment(sentence)
                        if res == 1:
                            flag = -1
                        if res == -1:
                            flag = 1
                        if res == 0:
                            flag = 0
                    else:
                        sentence = m1.group(0)
                        res = judgeSentiment(sentence)
                        if res == -1:
                            flag = -1
                        if res == 1:
                            flag = 1
                        if res == 0:
                            flag = 0

                else:
                    regex2 = ur"([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)(%s)([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)" % (entity2.decode("utf-8"))
                    rr = re.compile(regex2)
                    m2 = rr.search(sentence.decode("utf-8"))
                    if m2:
                        relationStr =  m2.group(0)
                        if relationStr.__contains__('比不了') or relationStr.__contains__('比不上'):
                            flag = 1
                        elif relationStr.__contains__('比'):
                            regex2 = ur"(比)([\u4e00-\u9fa5、，/（）#(\d.\d)a-zA-Z]*)"
                            rr = re.compile(regex2)
                            m2 = rr.search(relationStr)
                            sentence = m2.group(0)
                            res = judgeSentiment(sentence)
                            if res == -1:
                                flag = -1
                            if res == 1:
                                flag = 1
                            if res == 0:
                                flag = 0
                        else:
                            sentence = m2.group(0)
                            res = judgeSentiment(sentence)
                            if res == 1:
                                flag = -1
                            if res == -1:
                                flag = 1
                            if res == 0:
                                flag = 0
                total += 1
                if int(label) == flag:
                    cnt += 1
print cnt,total
print cnt / (total + 0.0)