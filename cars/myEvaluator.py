#coding=utf-8

import csv
import json
from basicEvaluator import *

def keyToIndex(aspect_name):
    keyWord = {"综合": 0, "操控": 1, "动力": 2, "性价比": 3, "油耗": 4, "空间": 5, "舒适性": 6, "外观": 7, "内饰": 8}
    return keyWord[aspect_name]
def getDCG(rels):
    return dcg_at_k(rels, 13)

def getIDCG(rels):
    rels.sort()
    rels.reverse()
    return dcg_at_k(rels, 13)

def getNDCG(rels):
    return ndcg_at_k(rels, 13)
def getScoreList(result_list, standard_list):
    numOfEachGroup = 4
    group_nums = len(standard_list) / numOfEachGroup
    result_groups = []
    cnt = 0
    tmp_list = []
    for car in standard_list:
        tmp_list.append(car)
        cnt += 1
        if cnt == numOfEachGroup:
            cnt = 0
            result_groups.append(tmp_list)
            tmp_list = []
    result_groups.append(tmp_list)
    tmp = json.dumps(result_groups).decode("unicode-escape")
    # print tmp
    res = []
    #衡量推荐结果与最优结果之间的差别
    for index1, car in enumerate(result_list):
        for index2, group in enumerate(result_groups):
            if car in group:
                res.append(group_nums - index2 + 1)
    return res


def getStandardList(percentage, carType):
    csv_reader = csv.reader(open('standard.csv', 'rb'))
    point = []
    cnt = 0
    for row in csv_reader:
        if cnt == 0:
            cnt += 1
            continue
        else:
            point.append(row)
        cnt += 1
        #print json.dumps(row).decode("unicode-escape")
    pair = {}
    for car in carType:
        mark = 0
        for row in point:
            if car == row[9]:
                for aspect_name, aspect_per in percentage.items():
                    mark += aspect_per * float(row[keyToIndex(aspect_name)])
        pair.__setitem__(car, mark)
    return sorted(pair.items(), key = lambda pair: pair[1], reverse=True)
def calPrecision(standardSeq, systemSeq):
    match_cnt = 0
    num = len(standardSeq)
    for i in range(num):
        if standardSeq[i] == systemSeq[i]:
            match_cnt += 1
    return match_cnt / (num + 0.0)
if __name__ == "__main__":
    #percentage = {"油耗":0.3, "动力":0.15, "性价比":0.5,"操控":0.05}
    #percentage = {"油耗": 0.1, "动力": 0.1, "性价比": 0.1, "操控": 0.7}
    #percentage = {"油耗": 0.1, "动力": 0.7, "性价比": 0.1, "操控": 0.1}
    #percentage = {"油耗": 0.7, "动力": 0.1, "性价比": 0.1, "操控": 0.1}
    #percentage = {"油耗": 0.1, "动力": 0.1, "性价比": 0.7, "操控": 0.1}
    # test = ['帕萨特', '天籁', '蒙迪欧', '君威', '凯美瑞', '宝马', '雅阁', '凯迪拉克']
    # result_pair = getStandardList(percentage, test)
    # log = open("log1.txt", "ab")
    # out = []
    # for key, value in percentage.items():
    #     out.append(key + ":" + str(value) + ",")
    # for key in result_pair:
    #     tmp = json.dumps(key).decode("unicode-escape")
    #     print tmp
    #     out.append(key[0] + " " +  str(key[1]) + " ")
    # log.writelines(out)
    # log.write('\n')
    #如何衡量两个序列的相似程度
    seq1 = ["宝马", "君威", "凯迪拉克", "帕萨特", "蒙迪欧", "雅阁", "天籁", "凯美瑞"]
    seq2 = ["凯迪拉克", "宝马", "帕萨特", "蒙迪欧", "君威", "雅阁", "天籁", "凯美瑞"]
    seq3 = ["凯迪拉克", "宝马", "帕萨特", "君威", "天籁", "蒙迪欧", "雅阁", "凯美瑞"]
    seq4 = ["凯迪拉克", "蒙迪欧", "宝马", "帕萨特", "雅阁", "天籁", "君威", "凯美瑞"]
    seq5 = ["雅阁", "凯美瑞", "帕萨特", "凯迪拉克", "天籁", "宝马", "君威", "蒙迪欧"]
    seq6 = ["帕萨特", "宝马", "天籁", "雅阁", "凯美瑞", "凯迪拉克", "蒙迪欧", "君威"]
    seq7 = ["天籁", "凯迪拉克", "君威", "凯美瑞", "蒙迪欧", "宝马", "雅阁", "帕萨特"]
    seq8 = ["凯迪拉克", "天籁", "帕萨特", "蒙迪欧", "宝马", "君威", "凯美瑞", "雅阁"]
    # print calPrecision(seq1, seq2)
    # print calPrecision(seq3, seq4)
    # print calPrecision(seq5, seq6)
    # print calPrecision(seq7, seq8)
    input_list = getScoreList(seq2, seq3)
    print input_list
    #1:0.911881216528
    #2:0.944313625086
    #3:0.923782427567
    #4:0.932865867054
    print getDCG(input_list) / getIDCG(input_list)