#coding=utf-8
import re
import os
# #同向
# pos_point3 = ["好", "强", "高"]
# pos_point2 = ["正常", "不错", "适中"]
# pos_point1 = ["一般", "还好"]
# #反向
# neg_point3 = ["低"]
# neg_point2 = ["一般", "适中"]
# neg_point1 = ["高"]
# entity1 = "阿特兹"
# entity2 = "金牛座"

# sent1 = "转向精准，指向性清楚，地盘感觉非常整，刚性十足，过减速带车身没有多余的乱响，只有蹦蹦的两声清脆声音，上路雨雪泥泞等路面还有待检验 底盘及悬架：底盘非常整齐，我在安装胎压监测系统的时候，升起整车，下面都是平整的护板，听说一方面是保护车底的管线油线，还有就是因为平整更有利于降低风阻，节省燃油消耗，对发动机，排气管的保护很是到位！ 横向对比：底盘保护完整度，我见过的比阿特兹好的，福特金牛座，也是我比较平民吧，没见过其他土豪级别的车底盘，就是很好！"
#sent1 = "我比你帅很多"
#比字之后十个单词
keywords = []
dict = {}
d = open("dict.txt",'rb')
count = 0#车型数量

for item in d:
    temp = item.replace("\r\n","")
    keywords.append(temp)
    dict[temp] = count
    count += 1
dir = "comments1"
walk = os.walk(os.path.realpath(dir))
for root, dirs, files in walk:
    for file in files:
        f = open(os.path.join(root, file), 'rb')
        file = file[:-4]
        n = dict[file]  # 源车型标记
        t = 0
        for line in f:
            if len(line) <= 2:
                continue
            line = line.replace("\r\n", "")
            # print(line)
            if line in keywords:
                t = dict[line]  # 目标车型标记
                continue
            data = line.split('###')
            label = data[0]
            sentence = data[1]
            #print keywords[t]
            #str = ur"(%s)[\u4e00-\u9fa5、，！。？]{2,10}" %  (keywords[t].decode("utf-8"))
            str = ur"[\u4e00-\u9fa5](比)[\u4e00-\u9fa5]"
            regex = str
            rr = re.compile(regex)
            m = rr.search(sentence.decode("utf-8"))
            print m.group()
# regex = \
# ur"((比)[\u4e00-\u9fa5]{2,10})"
# rr = re.compile(regex)
# m = rr.search(sent1.decode("utf-8"))
# print m.group()
# for str in rr.findall(sent1.decode("utf-8")):
#     print str

