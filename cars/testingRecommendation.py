#coding=utf-8
from myEvaluator import *
from sort import *
def getAspectAndPercent():
    aspect_name = ["操控", "动力", "性价比", "油耗", "空间", "舒适性", "外观", "内饰"]
    #控制方面数
    aspect_num = random.randint(1, 8)
    aspect_percentage = {}
    mark = []
    counter = 0
    #生成不同方面的百分比
    while counter < aspect_num:
        j = random.randint(1, 8)
        while aspect_name[j] not in mark:
            aspect_percent_before_normalize = random.randint(25, 60)
            aspect_percentage.__setitem__(aspect_name[j], aspect_percent_before_normalize)
            mark.append(aspect_name[j])
            counter += 1
    cnt = 0
    #归一化
    for key in aspect_percentage:
        cnt += aspect_percentage[key]
    for key in aspect_percentage:
        aspect_percentage[key] = aspect_percentage[key] / (cnt + 0.0)
    return aspect_percentage
if __name__ == "__main__":
    cnt = 0
    total = 10000
    for i in range(0, total):
        print i
        aspectPercentage = getAspectAndPercent()
        #print aspectPercentage
        result_map = sort(aspectPercentage)
        cnt += result_map["NDCG"]
    print cnt/(total + 0.0)
