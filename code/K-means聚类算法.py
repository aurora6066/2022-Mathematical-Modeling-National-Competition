import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kmeans

plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False
name = ['高钾', '铅钡', '高钾与铅钡', '表单1']
# SiO2
Y = []
Y1 = pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[3], usecols="C:P")  # 原始数据
Y.append(Y1)
for i in range(1, 11):
    Y2 = Y1.copy()
    Y2["二氧化硅(SiO2)"][:] += i
    Y.append(Y2)
for i in range(1, 11):
    Y2 = Y1.copy()
    Y2["二氧化硅(SiO2)"][:] -= i
    Y.append(Y2)

# BaO
Z = []
Z1 = pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[3], usecols="C:P")  # 原始数据
Z.append(Z1)
for i in range(1, 11):
    Z2 = Z1.copy()
    Z2["氧化钡(BaO)"][:] += i
    Z.append(Z2)
for i in range(1, 11):
    Z2 = Z1.copy()
    Z2["氧化钡(BaO)"][:] -= i
    Z.append(Z2)

# PbO
V = []
V1 = pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[3], usecols="C:P")  # 原始数据
V.append(V1)
for i in range(1, 11):
    V2 = V1.copy()
    V2["氧化铅(PbO)"][:] += i
    V.append(V2)
for i in range(1, 11):
    V2 = V1.copy()
    V2["氧化铅(PbO)"][:] -= i
    V.append(V2)

# Fe2O3
B = []
B1 = pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[3], usecols="C:P")  # 原始数据
B.append(B1)
for i in range(1, 11):
    B2 = B1.copy()
    B2["氧化铁(Fe2O3)"][:] += i
    B.append(B2)
for i in range(1, 11):
    B2 = B1.copy()
    B2["氧化铁(Fe2O3)"][:] -= i
    B.append(B2)


def sure_location(centers, assignments, k):
    location = -1
    xx = []
    for i in range(len(centers)):
        xx.append([])
    for i in range(len(assignments)):
        xx[assignments[i]].append(i + 1)
    for i in range(len(xx)):
        if k in xx[i]:
            location = i
        print(xx[i])
    return location


# Decide which of the two broad categories is in
def judge_double(X):
    model = kmeans.KMeans(n_clusters=4, max_iter=15)
    centers, assignments = model.fit_transform(X)
    location = -1
    xx = []
    for i in range(len(centers)):
        xx.append([])
    for i in range(len(assignments)):
        xx[assignments[i]].append(i + 1)
    for i in range(len(xx)):
        if 68 in xx[i] and 1 in xx[i]:
            print("高钾类别")
            return i
        elif 68 in xx[i]:
            location = i
        print(xx[i])
    print("铅钡类别")
    return location


# Determine which subclass of high potassium is high
def judge_GK(X):
    model = kmeans.KMeans(n_clusters=2, max_iter=15)
    centers, assignments = model.fit_transform(X)
    return sure_location(centers, assignments, 19)


# Determine which subclass of lead barium is identified
def judge_QB(X):
    model = kmeans.KMeans(n_clusters=4, max_iter=15)
    centers, assignments = model.fit_transform(X)
    return sure_location(centers, assignments, 50)


# Loop judgment
# The order of judgment is (raw data, +1, +2, +3, +4, +5, +6, +7, +8, +9, +10, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10)
def circle_judge(W):
    for j in range(len(W)):
        for i in range(len(W[j])):
            X = np.concatenate((x3, np.array([W[j].iloc[i]], dtype=object)))
            temp = judge_double(X)
            print(temp)
            X = np.concatenate((x2, np.array([W[j].iloc[i]], dtype=object)))
            print("类别：", judge_QB(X) + 1)
            X = np.concatenate((x1, np.array([W[j].iloc[i]], dtype=object)))
            print("类别：", judge_GK(X) + 1)
            print()
        plt.legend()  # Pause the effect
        plt.show()


x1 = np.array(pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[0], usecols="E:R"), dtype=object)
x2 = np.array(pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[1], usecols="E:R"), dtype=object)
x3 = np.array(pd.read_excel('K-means聚类预测类别.xlsx', sheet_name=name[2], usecols="E:R"), dtype=object)

# SiO2
circle_judge(Y)
print("------------分割线------------")
# BaO
circle_judge(Z)
print("------------分割线------------")
# PbO
circle_judge(V)
print("------------分割线------------")
# Fe2O3
circle_judge(B)
print("------------分割线------------")
