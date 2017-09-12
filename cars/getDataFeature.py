#coding=utf-8
import os
import sys

keywords = []
dict = {}
d = open("dict.txt",'rb')
count = 0#车型数量

for item in d:
    temp = item.replace("\r\n","")
    keywords.append(temp)
    dict[temp] = count
    count += 1
dir_list = ["comments1","comments2", "comments3", "comments4"]
cnt_pos = 0
cnt_neg = 0
cnt_zero = 0
total = 0
out_pos = []
out_zero = []
out_neg = []
log_zero = open("zero_log.txt", "wb")
log_pos = open("pos_log.txt", "wb")
log_neg = open("neg_log.txt", "wb")
log_pVector_pos = open("pVector_log_pos.txt", "wb")
log_pVector_neg = open("pVector_log_neg.txt", "wb")
log_pVector_zero = open("pVector_log_zero.txt", "wb")
for dir in dir_list:
    walk = os.walk(os.path.realpath(dir))
    for root, dirs, files in walk:
        for file in files:
            f = open(os.path.join(root, file), 'rb')
            file = file[:-4]
            n = dict[file]  # 源车型标记
            entity1 = keywords[n]
            t = 0
            for line in f:
                if len(line) <= 2:
                    continue
                line = line.replace("\r\n", "")
                if line in keywords:
                    t = dict[line]  # 目标车型标记
                    continue
                entity2 = keywords[t]
                data = line.split('###')
                label = data[0]
                sentence = data[1]
                pVector1 = []
                pVector2 = []
                index1 = sentence.find(entity1)
                index2 = sentence.find(entity2)
                sentence_list = sentence.split()
                length = len(sentence_list)
                if index1 != -1:
                    for idx, word in enumerate(sentence_list):
                        pVector1.append(idx - index1)
                else:
                    pVector1 = [0 for x in range(length)]
                if index2 != -1:
                    for idx, word in enumerate(sentence_list):
                        pVector2.append(idx - index2)
                else:
                    pVector2 = [0 for x in range(length)]
                if int(label) == 0:
                    cnt_zero += 1
                    out_zero.append(sentence + "\n")
                if int(label) == 1:
                    cnt_pos += 1
                    out_pos.append(sentence + '\n')
                if int(label) == -1:
                    cnt_neg += 1
                    out_neg.append(sentence + '\n')
                total += 1
                pVector = pVector1 + pVector2
                print ','.join([str(num) for num in pVector]) + '\n'
                if int(label) == -1:
                    log_pVector_neg.writelines(','.join([str(num) for num in pVector]) + '\n')
                if int(label) == 1:
                    log_pVector_pos.writelines(','.join([str(num) for num in pVector]) + '\n')
                if int(label) == 0:
                    log_pVector_zero.writelines(','.join([str(num) for num in pVector]) + '\n')
                # print pVector1
                # print pVector2

print total, cnt_pos, cnt_zero, cnt_neg

# log_zero.writelines(out_zero)
# log_pos.writelines(out_pos)
# log_neg.writelines(out_neg)


