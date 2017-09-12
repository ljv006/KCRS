#-*-coding=utf-8-*-
import jieba
import sys

reload(sys)

sys.setdefaultencoding('utf8')
#同向
pos_point3 = ["好", "强", "高"]
pos_point2 = ["正常", "不错", "适中"]
pos_point1 = ["一般", "还好"]
#反向
neg_point3 = ["低"]
neg_point2 = ["一般", "适中"]
neg_point1 = ["高"]
#评价词
markWord = ["好", "强", "高","正常", "不错", "适中","一般", "还好","低"]

def cut_sentence_new(words):
    words = (words).decode('utf8')
    start = 0
    i = 0
    sents = []

    punt_list = ',.!?:;~，。！？：；～'.decode('utf8')
    for word in words:
        if word in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sents.append(words[start:i+1])
            start = i+1
            i += 1
        else:
            i += 1
            token = list(words[start:i+2]).pop() # 取下一个字符
    if start < len(words):
        sents.append(words[start:])
    return sents

def calculate(aspect,mark):
    aspect = aspect.encode("utf-8").strip();
    if aspect == "操控" or aspect == "性价比" or aspect == "动力":
        if mark in pos_point3:
            return 3
        elif mark in pos_point2:
            return 2
        elif mark in pos_point1:
            return 1
    elif aspect == "油耗":
        if mark in neg_point3:
            return 3
        elif mark in neg_point2:
            return 2
        elif mark in neg_point1:
            return 1

def getPercentage(input_sentence):
    #seg_list = jieba.cut(input_sentence, cut_all=False)
    # 强度词在方面词前
    # 例：有着较强操控性
    seg_list = cut_sentence_new(input_sentence)
    value = {}
    res = {}
    keyWord = ["操控", "动力", "性价比", "油耗", "空间", "舒适性", "外观", "内饰"]
    for seg_sent in seg_list:
        for key in keyWord:
            if key in seg_sent:
                for mark in markWord:
                    if mark in seg_sent:
                        value.__setitem__(key, mark)  # 这里可以改进
    for val in value:
        res.__setitem__(val, calculate(val, value[val]))
    cnt = 0
    for key in res:
        if res[key] == None:
            res[key] = 0
            cnt += 0
        else:
            cnt += res[key]
    for key in res:
        res[key] = round(res[key] / (cnt + 0.0), 3)
    return res

# sen1 = "我要买一辆操控强，油耗低，性价比高的汽车"#bug
# sen2 = "我要买一台有很强操控性，油耗低，性价比不错,有强动力的汽车"
# sen3 = "我要买一台操控性一般，油耗低，性价比高,动力一般的汽车"
#我要买一台操控性一般，油耗低，动力一般的汽车
