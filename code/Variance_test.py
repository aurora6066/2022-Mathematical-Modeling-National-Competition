#独立样本t检验
import csv
from  scipy.stats import ttest_ind, levene
import pandas as pd

def loadData(filename):
    dataSet = []
    with open(filename,'r',encoding='utf-8-sig') as file:
        csvReader=csv.reader(file)
        for line in csvReader:
            print(line[0])
            x = line[1:7]           #高钾玻璃组，6组风化，12组无风化
            y = line[7:]
            x = list(map(float, x))
            y = list(map(float, y))
            print(levene(x,y))           #方差齐次性检查
            if levene(x,y).pvalue>0.05:
                print(ttest_ind(x, y))     # 独立样本T检验,默认方差齐性
            else:
                print(ttest_ind(x,y,equal_var=False)) #如果方差不齐性，则equal_var=False
            print("\n")

if __name__ == '__main__':
    loadData('D:\.nvscode\py\guosai\高钾玻璃t检验.csv')
    
