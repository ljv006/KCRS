#coding=utf8
import string
#import graphviz as pgv
import networkx as nx
import os
from numpy import *;
import math
import numpy
#from graphviz import Digraph
#import matplotlib.pyplot as plt
from flask import *

#plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
keywords = []
dict = {}
d = open("dict.txt",'rb')
count = 0
RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45]
for item in d:
    temp = item.replace("\r\n","")
    keywords.append(temp)
    dict[temp] = count
    count += 1

test = ['帕萨特','天籁','蒙迪欧','君威']
N = len(test)
translate = {1:[0,0],2:[1,3],3:[4,7],4:[8,12],5:[13,100]}
#dot = Digraph(comment='The Car Table',node_attr={"fontname":"FangSong","shape":"circle"})
MATRIX = []
for i in range(4):
    tmep = numpy.zeros((4,4))
    MATRIX.append(tmep)
    graph = numpy.zeros([count, count])
    num = numpy.zeros([count, count])
    dir = "comments" + str(i+1)
    walk = os.walk(os.path.realpath(dir))
    for root,dirs,files in walk:
        for file in files:
            f = open(os.path.join(root,file),'rb')
            file = file[:-4]
            n = dict[file]
            t = 0
            for line in f:
                if len(line) <= 2:
                    continue
                line = line.replace("\r\n", "")
                #print(line)
                if line in keywords:
                    t = dict[line]
                    continue
                data = line.split('###')
                label = data[0]
                if len(data) < 2:
                    continue
                sentence = data[1]
                graph[n][t] += int(label)
                num[n][t] += 1
    for j in range(N):
        a = dict[test[j]]
        for k in range(N):
            b = dict[test[k]]
            diff = int(graph[a][b] - graph[b][a])
            score = 0
            for l in translate:
                if abs(diff) >= translate[l][0] and abs(diff) <= translate[l][1]:
                    score = l
                    break
            if (diff > 0):
                MATRIX[i][j][k] = score
            elif (diff < 0):
                MATRIX[i][j][k] = 1.0 / (score)
            else:
                MATRIX[i][j][k] = score


matrix_tmp = MATRIX
control  = input("操控%:")
power = input("动力%:")
price = input("性价比%:")
oilconsumption = input("油耗%:")
control = int(control)
power = int(power)
price = int(price)
oilconsumption = int(oilconsumption)
criteria = []
criteria.append(control)
criteria.append(power)
criteria.append(price)
criteria.append(oilconsumption)
translate1 = {1:[1.0,1.0],2:[1.0,1.5],3:[1.5,1.8],4:[1.8,2.5],5:[2.5,99.0]}
compare_criteria = numpy.zeros((4,4))
for i in range(len(criteria)):
    a = criteria[i]
    for j in range(len(criteria)):
        b = criteria[j]
        div = max(a,b) / min(a,b)
        score = 0
        for k in translate:
            if div >= translate1[k][0] and div <= translate1[k][1]:
                score = k
                break
        if a >= b :
            compare_criteria[i][j] = score
        else:
            compare_criteria[i][j] = 1/score
#compare_criteria = [[1,3,1/4],[1/3,1,5],[4,1/5,1]]
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
        max_lambda += l[i]/(n*M[i])
    return max_lambda,M

def computeConsistence(max_lambda,n):
    CI = (max_lambda-n)/(n-1)
    CR = CI / RI[n-1]
    return CR
def getKey( x ):
    return x[1]

lambda_criteria,weight_criteria = computeLambda(compare_criteria)
consistence_criteria = computeConsistence(lambda_criteria,len(compare_criteria))

lambda_control,weight_control = computeLambda(MATRIX[0])
consistence_control = computeConsistence(lambda_control,len(MATRIX[0]))

lambda_power,weight_power = computeLambda(MATRIX[1])
consistence_power = computeConsistence(lambda_power,len(MATRIX[1]))

lambda_price,weight_price = computeLambda(MATRIX[2])
consistence_price = computeConsistence(lambda_price,len(MATRIX[2]))

lambda_oilconsumption,weight_oilconsumption = computeLambda(MATRIX[3])
consistence_oilconsumption = computeConsistence(lambda_oilconsumption,len(MATRIX[3]))

weight = []
weight.append(weight_control)
weight.append(weight_power)
weight.append(weight_price)
weight.append(weight_oilconsumption)
weight = mat(weight)
weight = weight.T
weight_criteria = mat(weight_criteria)
score = weight*weight_criteria.T
list = []
for i in range(N):
    info = []
    info.append(test[i])
    info.append(score.tolist()[i][0])
    list.append(info)
list.sort( key=lambda x:x[1],reverse=True )
for i in range(len(list)):
    print(i+1,list[i][0])
    #print(list[i][0])
    print(list[i][1])

app = Flask(__name__)
@app.route('/')
def index():

    p = []
    for i in range(len(MATRIX)):
        q = []
        for j in range(len(MATRIX[i])):
            r = []
            for k in range(len(MATRIX[i][j])):
                r.append(MATRIX[i][j][k])
            q.append(r)
        p.append(q)
    #p.append(test[0].decode('utf-8'))
    #p.append(test[1].decode('utf-8'))
    #p.append(test[2].decode('utf-8'))
    #p.append(test[3].decode('utf-8'))
    t = {'num':len(test),
        'cars':[u'帕萨特', u'天籁', u'蒙迪欧', u'君威'],
         'aspect':[u'操控',u'动力',u'性价比',u'油耗'],
         'weight':p,
         'result':[weight_control,weight_power,weight_price,weight_oilconsumption]}

    return render_template('index.html',**t)



if __name__ == '__main__':
    app.run()