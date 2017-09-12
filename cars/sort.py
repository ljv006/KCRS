#-*-coding=utf-8-*-
import string
import graphviz as pgv
import networkx as nx
import os
from numpy import *
from getInputSentence import *
import math
import numpy
from myEvaluator import *

RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45]

def computeLambda(compare_matrix):
    n = len(compare_matrix)
    M = []
    for i in range(n):
        m = 1
        for j in range(n):
            m = m * compare_matrix[i][j]
        M.append(math.pow(m,1.0/n))
    W = sum(M)
    for i in range(n):
        M[i] = M[i] / W
    A = mat(compare_matrix)
    x = mat(M)
    l = A*x.T
    max_lambda = 0
    for i in range(n):
        max_lambda += l[i]/(n*M[i])#分母可能为0
    return max_lambda,M

def computeConsistence(max_lambda,n):
    CI = (max_lambda-n)/(n-1)
    CR = CI / RI[n-1]
    return CR

def getKey( x ):
    return x[1]

def sort(aspect_percentage):
    keywords = []
    dict = {}
    d = open("dict.txt",'rb')
    # log = open("log.txt", "ab")
    # log1 = open("log1.txt", "ab")
    count = 0#车型数量

    for item in d:
        temp = item.replace("\r\n","")
        keywords.append(temp)
        dict[temp] = count
        count += 1
    criteria_map = {}
    aspect2Id_map = {"操控":1, "动力":2, "性价比":3, "油耗":4, "空间":5, "舒适性":6, "外观":7, "内饰":8}
    criteria = []
    aspect = []
    if aspect_percentage is None:
        os._exit(0)
    for key, value in aspect_percentage.items():
        value = float(value)
        criteria.append(value)
        criteria_map.__setitem__(key, value)
        # log.write(key + ":%.2f%% " % (value * 100))

    carType = ['帕萨特', '天籁', '蒙迪欧', '君威', '凯美瑞', '宝马', '雅阁', '凯迪拉克', "迈腾", "奥迪", "君越", "博瑞", "速派"]
    criteria_num = len(criteria_map)
    car_num = len(carType)#车型数量
    translate = {1:[0,0],2:[1,1.5],3:[1.5,2.2],4:[2.2,3.5],5:[3.5,100]}
    MATRIX = []
    cnt = 0
    for key in criteria_map:
        temp = numpy.zeros((car_num,car_num))
        MATRIX.append(temp)
        graph = numpy.zeros([count, count])
        num = numpy.zeros([count, count])

        dir = "comments" + str(aspect2Id_map[key])
        walk = os.walk(os.path.realpath(dir))
        for root,dirs,files in walk:
            for file in files:
                f = open(os.path.join(root,file),'rb')
                file = file[:-4]
                n = dict[file]#源车型标记
                t = 0
                for line in f:
                    if len(line) <= 2:
                        continue
                    line = line.replace("\r\n", "")
                    #print(line)
                    if line in keywords:
                        t = dict[line]#目标车型标记
                        continue
                    data = line.split('###')
                    label = data[0]
                    sentence = data[1]
                    graph[n][t] += int(label)
                    num[n][t] += 1
        for j in range(car_num):
            a = dict[carType[j]]
            for k in range(car_num):
                b = dict[carType[k]]
                diff = int(graph[a][b] - graph[b][a])
                score = 0
                for l in translate:
                    if abs(diff) >= translate[l][0] and abs(diff) <= translate[l][1]:
                        score = l
                        break
                if (diff >= 0):
                    MATRIX[cnt][j][k] = score
                elif (diff < 0):
                    MATRIX[cnt][j][k] = 1.0 / (score)
        cnt += 1

    translate1 = {1:[1.0,1.0],2:[1.0,1.5],3:[1.5,1.8],4:[1.8,2.5],5:[2.5,99.0]}
    compare_criteria = numpy.zeros((criteria_num, criteria_num))
    for i in range(criteria_num):
        a = criteria[i]
        for j in range(criteria_num):
            b = criteria[j]
            if min(a, b) == 0:
                div = 0
            else:
                div = max(a,b) / min(a,b)
            score = 0
            for k in translate1:
                #落在不同的区间中
                if div >= translate1[k][0] and div <= translate1[k][1]:
                    score = k
                    break
            if a >= b :
                compare_criteria[i][j] = score
            else:
                if score == 0:
                    print "score为空"
                    os._exit(0)
                else:
                    compare_criteria[i][j] = 1/score


    lambda_aspect = [0 for n in range(criteria_num)]
    weight_aspect = [0 for n in range(criteria_num)]
    consistence_aspect = [0 for n in range(criteria_num)]
    lambda_criteria,weight_criteria = computeLambda(compare_criteria)
    consistence_criteria = computeConsistence(lambda_criteria,len(compare_criteria))

    pos = 0
    for value in MATRIX:
        lambda_aspect[pos], weight_aspect[pos] = computeLambda(value)
        consistence_aspect[pos] = computeConsistence(lambda_aspect[pos],len(lambda_aspect[pos]))
        pos += 1

    weight_aspect = mat(weight_aspect)
    weight_aspect = weight_aspect.T
    weight_criteria = mat(weight_criteria)
    score = weight_aspect*weight_criteria.T

    list = []
    standard_seq = []
    system_seq = []
    for i in range(car_num):
        info = []
        info.append(carType[i])
        #按照默认的输入顺序，做测试对照
        #system_seq.append(carType[i])
        info.append(score.tolist()[i][0])
        list.append(info)
    list.sort( key=lambda x:x[1],reverse=True )
    out = []
    result_map = {}
    for i in range(len(list)):
        res = list[i][0] + " " + str(list[i][1]) + " "
        system_seq.append(list[i][0])
        result_map.__setitem__(list[i][0], round(list[i][1], 3))
        out.append(res)
    result_pair = getStandardList(aspect_percentage, carType)
    out1 = []
    for key, value in aspect_percentage.items():
        out1.append(key + ":" + str(value) + ",")
    for key in result_pair:
        tmp = json.dumps(key).decode("unicode-escape")
        standard_seq.append(key[0])
        out1.append(key[0] + " " +  str(key[1]) + " ")
    system_seq_tmp = json.dumps(system_seq).decode("unicode-escape")
    #print system_seq_tmp
    standard_seq_tmp = json.dumps(standard_seq).decode("unicode-escape")
    #print standard_seq_tmp
    input_list = getScoreList(system_seq, standard_seq)
    # log1.writelines(out1)
    # log1.write('\n')
    # log.writelines(out)
    # log.write('\n')
    dcg = round(getDCG(input_list), 3)
    ndcg = round(getNDCG(input_list), 3)
    result_map["DCG"] = dcg
    result_map["NDCG"] = ndcg
    return result_map
def sortByAspect(aspect_percentage, flag):
    if flag == "综合":
        return sort(aspect_percentage)
    else:
        aspect_percentage_flag = {flag:1}
        return sort(aspect_percentage_flag)