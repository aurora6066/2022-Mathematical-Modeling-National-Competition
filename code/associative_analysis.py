#关联分析
import csv

#1.从表单1的第二行第二列开始读取有效数据
def loadDataSet(filename):
    dataSet = []
    row = 0
    with open(filename,'r',encoding='utf-8-sig') as file:
        csvReader=csv.reader(file)
        for line in csvReader:
            if row > 0:
                dataSet.append(line[1:])
            row += 1
    return dataSet

#2.构建候选1项集C1
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return list(map(frozenset, C1))

#3.将候选集Ck转换为频繁项集Lk
#D：原始数据集
#Cn: 候选集项Ck
#minSupport:支持度的最小值
def scanD(D, Ck, minSupport):
    #候选集计数
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt.keys(): ssCnt[can] = 1
                else: ssCnt[can] += 1

    numItems = float(len(D))
    Lk= []     # 候选集项Cn生成的频繁项集Lk
    supportData = {}    #候选集项Cn的支持度字典
    #计算候选项集的支持度, supportData key:候选项， value:支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support > minSupport:
            Lk.append(key)
        supportData[key] = [support,ssCnt[key]]
    return Lk, supportData

#4.连接操作，将频繁Lk-1项集通过拼接转换为候选k项集
def aprioriGen(Lk_1, k):
    Ck = []
    lenLk = len(Lk_1)
    for i in range(lenLk):
        L1 = Lk_1[i]
        for j in range(i + 1, lenLk):
            L2 = Lk_1[j]
            if len(L1 & L2) == k - 2:
                L1_2 = L1 | L2
                if L1_2 not in Ck:
                    Ck.append(L1 | L2)
    return Ck

#5.
def apriori(dataSet, minSupport = 0):
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Lk_1 = L[k-2]
        Ck = aprioriGen(Lk_1, k)
        #print("ck:",Ck)
        Lk, supK = scanD(dataSet, Ck, minSupport)
        supportData.update(supK)
        #print("lk:", Lk)
        L.append(Lk)
        k += 1
    return L, supportData

#6. 计算规则的可信度，并过滤出满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    ''' 对候选规则集进行评估 '''
    prunedH = []
    for conseq in H:      
        conf = supportData[freqSet][0] / supportData[freqSet - conseq][0]
        if conf >= minConf:
            if conseq == frozenset({'风化'}) or conseq == frozenset({'无风化'}):
                print (freqSet - conseq, '-->', conseq, 'conf:', conf , 'support:', supportData[freqSet])
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

#7. 根据当前候选规则集H生成下一层候选规则集
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    while (len(freqSet) > m):  # 判断长度 > m，这时即可求H的可信度
        H = calcConf(freqSet, H, supportData, brl, minConf)     # 返回值prunedH保存规则列表的右部，这部分频繁项将进入下一轮搜索
        if (len(H) > 1):  # 判断求完可信度后是否还有可信度大于阈值的项用来生成下一层H
            H = aprioriGen(H, m + 1)
            #print ("H = aprioriGen(H, m + 1): ", H)
            m += 1
        else:  # 不能继续生成下一层候选关联规则，提前退出循环
            break

#8. 频繁项集列表L
# 包含那些频繁项集支持数据的字典supportData
# 最小可信度阈值minConf
def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    # 频繁项集是按照层次搜索得到的, 每一层都是把具有相同元素个数的频繁项集组织成列表，再将各个列表组成一个大列表，所以需要遍历Len(L)次, 即逐层搜索
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]    # 对每个频繁项集构建只包含单个元素集合的列表H1
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)     # 根据当前候选规则集H生成下一层候选规则集
    return bigRuleList

if __name__=='__main__':
    dataset = loadDataSet('D:\.nvscode\py\guosai\表单1.csv')
    L, supportData = apriori(dataset, minSupport=0.1)
    for key,values in supportData.items():
        if '风化' in key or '无风化' in key:
            print(key, values)
    # print(supportData)
    # 基于频繁项集生成满足置信度阈值的关联规则
    rules = generateRules(L, supportData, minConf=0.7)
