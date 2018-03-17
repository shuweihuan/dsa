#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

# 计算涨幅分档
def calc_incr_level(incr):
    if incr<-0.20:
        return -4
    if -0.20<=incr and incr>-0.10:
        return -3
    if -0.10<=incr and incr>-0.05:
        return -2
    if -0.05<=incr and incr>-0.01:
        return -1
    if -0.01<=incr and incr<=0.01:
        return 0
    if 0.01<incr and incr<=0.05:
        return 1
    if 0.05<incr and incr<=0.10:
        return 2
    if 0.10<incr and incr<=0.20:
        return 3
    if 0.20<incr:
        return 4

# 加载数据
df = pd.read_csv("../data/cyb.csv")

# 预测目标计算
df['incr1'] = df['close'].pct_change(periods=1).shift(-1)
df['incr3'] = df['close'].pct_change(periods=3).shift(-3)
df['incr5'] = df['close'].pct_change(periods=5).shift(-5)
df['incr10'] = df['close'].pct_change(periods=10).shift(-10)
df['incr20'] = df['close'].pct_change(periods=20).shift(-20)
df['incr1_level'] = calc_incr_level(df['incr1'])
df['incr3_level'] = calc_incr_level(df['incr3'])
df['incr5_level'] = calc_incr_level(df['incr5'])
df['incr10_level'] = calc_incr_level(df['incr10'])
df['incr20_level'] = calc_incr_level(df['incr20'])

# 去除空值
df = df.dropna()

print(df.head())

X = df[['open', 'close', 'high', 'low', 'volume']]
y = df[['incr']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
reg = LinearRegression()
reg.fit(X_train, y_train)

print(reg.intercept_)
print(reg.coef_)

# 模型拟合训练集
y_pred = reg.predict(X_train)
# 计算MSE
print("MSE on train: ", metrics.mean_squared_error(y_train, y_pred))
# 计算RMSE
print("RMSE on train: ", np.sqrt(metrics.mean_squared_error(y_train, y_pred)))
# 模型拟合测试集
y_pred = reg.predict(X_test)
# 计算MSE
print("MSE on test: ", metrics.mean_squared_error(y_test, y_pred))
# 计算RMSE
print("RMSE on test: ", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print(X_test.shape)
print(y_test.shape)
print(y_pred.shape)

df1 = pd.DataFrame(X_test)
df2 = pd.DataFrame(y_test)
#df3 = pd.DataFrame(y_pred)
df3 = pd.DataFrame(y_pred, index=list(range(y_pred.shape[0])), columns=['pred'])
df1 = df1.head()
df2 = df2.head()
df3 = df3.head()
df1['index'] = list(range(len(df1.index)))
df2['index'] = list(range(len(df2.index)))
df3['index'] = list(range(len(df3.index)))
#df2 = df2.head()
#df3 = df3.head()
#df1 = df1.reset_index()
#df2 = df2.reset_index()
#df3 = df3.reset_index()
#df1 = df1.reset_index()
#df2 = df2.reset_index()
print(df1)
print(df2)
print(df3)

df = df1.merge(df2, on='index')
df = df.merge(df3, on='index')
print(df)

#print(df2)
#print(df3)

