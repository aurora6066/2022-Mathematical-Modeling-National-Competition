import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import kmeans

plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False
name = ['高钾', '铅钡']
Name = ['原始数据', '噪音干扰数据']
color = ['salmon', 'mediumorchid']


def calculate_distance(point, center):
    dist = 0
    for l in range(len(point)):
        dist += (point[l]-center[l])**2
    return math.sqrt(dist)


def select_k_value(x, w):
    SSE = []
    for i in range(1, 10):
        model = kmeans.KMeans(n_clusters=i, max_iter=15)
        centers, assignments = model.fit_transform(x)
        inertias = 0
        for j in range(len(assignments)):
            inertias += calculate_distance(x[j], centers[assignments[j]])
        SSE.append(inertias)
    fig = plt.subplot()
    fig.plot(list(range(1, 10)), SSE, 'o-', color='salmon', label='inertias-k的关系')
    fig.set_title(name[w]+'玻璃-inertias指标')
    fig.set_xlabel('聚类簇数K')
    fig.set_ylabel('误差平方和SSE')
    fig.figure.savefig(name[w]+'玻璃-inertias指标.jpg')
    plt.show()


# 轮廓系数计算
def sc(x, assignments, k, ww):
    xx = []
    for j in range(k):
        xx.append([])
    for j in range(len(assignments)):
        xx[assignments[j]].append(x[j])
    ai = []
    bi = []
    si = []
    for j in range(len(xx)):
        for l in range(len(xx[j])):
            # 计算ai
            a = 0
            for w in range(len(xx[j])):
                if l == w:
                    continue
                else:
                    a += calculate_distance(xx[j][l], xx[j][w])
            ai.append(a / (len(xx[j]) - 1))
            # 计算blw
            bl = 0
            blw = []
            for w in range(len(xx)):
                if j == w:
                    continue
                else:
                    for r in range(len(xx[w])):
                        bl += calculate_distance(xx[j][l], xx[w][r])
                    blw.append(bl/len(xx[w]))
            bi.append(min(blw))
    for j in range(len(ai)):
        si.append((bi[j]-ai[j])/max(ai[j], bi[j]))
    print(sum(si)/len(si))
    return si


def Print(x, k, w):
    model = kmeans.KMeans(n_clusters=k, max_iter=15)
    centers, assignments = model.fit_transform(x)
    xx = []
    for j in range(k):
        xx.append([])
    for j in range(len(assignments)):
        xx[assignments[j]].append(j+1)
    for j in range(k):
        print(xx[j])
    si = sc(x, assignments, k, w)
    print()
    plt.plot(list(range(len(si))), si, 'o-', color=color[0], label=name[w]+'玻璃样本轮廓系数')
    plt.xlabel('样本标签')
    plt.ylabel('样本的轮廓系数')
    plt.title(name[w]+'玻璃样本轮廓系数')
    plt.legend()
    plt.savefig(name[w]+'玻璃样本轮廓系数.jpg')
    plt.show()


def contrast(x, j):
    model = kmeans.KMeans(n_clusters=K[j], max_iter=15)
    centers, assignments = model.fit_transform(x)
    return sc(x, assignments, K[j], 0)


def Rand(x, j, num):
    Y = pd.read_excel('随机数.xlsx', sheet_name='Sheet1', usecols="A:N")
    for i in range(num):
        r = random.randint(1, 99)
        x = np.concatenate((x, np.array(Y.iloc[r:r+1], dtype=object)), axis=0)
    model = kmeans.KMeans(n_clusters=K[j], max_iter=15)
    centers, assignments = model.fit_transform(x)
    return sc(x, assignments, K[j], 1)


k1, k2 = 2, 4
K = [k1, k2]
for i in range(2):
    print(name[i] + ":(与标签号对应)")
    X = np.array(pd.read_excel('K-means聚类的分类结果.xlsx', sheet_name=name[i], usecols="E:R"), dtype=object)
    select_k_value(X, i)
    Print(X, K[i], i)

n = 5  # 加入n组与2n组干扰数据
for i in range(2):
    X = np.array(pd.read_excel('K-means聚类的分类结果.xlsx', sheet_name=name[i], usecols="E:R"), dtype=object)
    model = kmeans.KMeans(n_clusters=K[0], max_iter=15)
    centers, assignments = model.fit_transform(X)
    si = contrast(X, i)
    plt.plot(list(range(len(si))), si, 'o-', color=color[0], label=Name[0]+' s(i)='+str(int(sum(si)/len(si)*10000)/10000))
    si = Rand(X, i, n*(i+1))
    plt.plot(list(range(len(si))), si, 'o-', color=color[1], label=Name[1]+' s(i)='+str(int(sum(si)/len(si)*10000)/10000))
    plt.title(name[i]+'玻璃样本轮廓系数（加入'+str(n*(i+1))+'组干扰数据)')
    plt.xlabel('样本标签')
    plt.ylabel('样本的轮廓系数')
    plt.legend()
    plt.savefig(name[i] + '玻璃样本轮廓系数对比('+str(n*(i+1))+').jpg')
    plt.show()
    print()

