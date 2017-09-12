#coding=utf-8
#限制输出的个数
from sort import *
def keyToIndex(aspect_name):
    keyWord = {"综合": 0, "操控": 1, "动力": 2, "性价比": 3, "油耗": 4, "空间": 5, "舒适性": 6, "外观": 7, "内饰": 8}
    return keyWord[aspect_name]
def getTextResult(aspect_percentage):
        result = ""
        comprehensive_result = []
        aspect = ["综合"]
        template_aspect = ["综合而言，&&1最值得推荐，&&2仅次于&&1之后，而&&3比&&4更值得购买",
                           "就操控方面而言，&&1的指向最为精准，&&2在精准度上逊于&&1，优于&&3和&&4",
                           "就动力方面而言，&&1的马力最强，&&2也有不错的动力体验，&&3和&&4的发动机表现与这两款车型还有一定的差距",
                           "就性价比方面而言，&&1的性价比最高，&&2次之，而&&3和&&4也有不错的性价比",
                           "就油耗方面而言，&&1最省油，&&2也有较低的油耗，&&3和&&4在油耗方面的表现有待提高",
                           "就空间方面而言，&&1的车厢空间最大，&&2也为乘客提供了足够的空间，&&3以及&&4的车内空间虽然没有前两款车的大，但也可以接受",
                           "就舒适性方面而言，&&1这款车的舒适性最高，为乘客提供很好的乘车体验，&&2，&&3和&&4在舒适性这个方面都排在它之后",
                           "就外观方面而言，&&1的外观最为漂亮，&&2也有不错的口碑，&&3和&&4两款车型排在它们之后",
                           "就内饰方面而言，&&1的内饰最精致，&&2的内饰与&&1差距不大，比&&3和&&4更为一众车主所接受"]
        comprehensive_result.append(sortByAspect(aspect_percentage, "综合"))
        for key in aspect_percentage:
            comprehensive_result.append(sortByAspect(aspect_percentage, key))
            aspect.append(key)
        cnt_aspect = 0
        num_aspect = len(aspect)
        for tmp1 in comprehensive_result:
            cnt = 1
            template = template_aspect[keyToIndex(aspect[cnt_aspect])]
            for tmp2 in tmp1:
                if cnt > 4:
                    break
                template = template.replace("&&" + str(cnt), tmp2)
                cnt += 1
            cnt_aspect += 1
            if num_aspect == cnt_aspect:
                result += template + "."
            else:
                result += template + ";" + "\n"
        return result
if __name__ == "__main__":
        # aspect = ["综合", "内饰","动力"]
        # result = [["凯美瑞", "君威", "帕萨特", "迈腾", "雅阁"],["君威","凯美瑞", "迈腾", "帕萨特","雅阁"],["迈腾","君威", "帕萨特", "雅阁","凯美瑞"]]
        # print getTextResult(result, aspect)
        #aspect_percentage = {"内饰":0.3, "动力":0.6, "性价比":0.1}
        aspect_percentage = getPercentage("我要买一台有很强操控性，油耗低，性价比不错,有强动力的汽车")
        print getTextResult(aspect_percentage)