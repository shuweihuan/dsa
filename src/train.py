#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
#import talib as tl
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

# 规范化股票代码
def norm_code(code):
    code = str(code)
    l = 6 - len(code)
    return '0' * l + code

# 输出精度控制
def format_float(x, precision=2):
    f = "%." + str(precision) + "f"
    return f % x

# 计算是否上涨
def is_incr(x):
    if x > 0:
        return 1
    else:
        return 0

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
df = pd.read_csv("../data/stock_history/000066.csv")

# 计算索引
df['code'] = df['code'].apply(norm_code)
df['key'] = df['code'] + ':' + df['date']
df = df.set_index('key')

# 预测目标计算
df['incr_next_1d'] = df['close'].pct_change(periods=1).shift(-1)
df['incr_next_5d'] = df['close'].pct_change(periods=5).shift(-5)
df['label'] = df['incr_next_5d'].apply(is_incr)

# 计算特征
df['prev'] = df['close'].shift(-1)
df['diff_prev_open'] = df['open'] / df['prev'] - 1 # 当日开盘价相对于前一日收盘价变化
df['diff_prev_high'] = df['high'] / df['prev'] - 1 # 当日最高价相对于前一日收盘价变化
df['diff_prev_low'] = df['low'] / df['prev'] - 1 # 当日最低价相对于前一日收盘价变化
df['diff_open_close'] = df['close'] / df['open'] - 1 # 当日收盘价相对于开盘价变化
df['diff_open_high'] = df['high'] / df['open'] - 1 # 当日最高价相对于开盘价变化
df['diff_open_low'] = df['low'] / df['open'] - 1 # 当日最低价相对于开盘价变化
df['diff_close_high'] = df['high'] / df['close'] - 1 # 当日最高价相对于收盘价变化
df['diff_close_low'] = df['low'] / df['close'] - 1 # 当日最低价相对于收盘价变化
df['incr_prev_1d'] = df['close'].pct_change(periods=1) # 近1日涨幅
df['incr_prev_5d'] = df['close'].pct_change(periods=5) # 近5日涨幅
df['incr_prev_10d'] = df['close'].pct_change(periods=10) # 近10日涨幅
df['incr_prev_20d'] = df['close'].pct_change(periods=20) # 近20日涨幅
df['incr_prev_60d'] = df['close'].pct_change(periods=60) # 近60日涨幅
df['v_incr_prev_1d'] = df['volume'].pct_change(periods=1)
df['v_incr_prev_5d'] = df['volume'].pct_change(periods=5)
df['v_incr_prev_10d'] = df['volume'].pct_change(periods=10)
df['v_incr_prev_20d'] = df['volume'].pct_change(periods=20)
df['v_incr_prev_60d'] = df['volume'].pct_change(periods=60)

features = [
    'open', 'close', 'high', 'low', 'volume',
    'diff_prev_open', 'diff_prev_high', 'diff_prev_low',
    'diff_open_close', 'diff_open_high', 'diff_open_low', 'diff_close_high', 'diff_close_low',
    'incr_prev_1d', 'incr_prev_5d', 'incr_prev_10d', 'incr_prev_20d', 'incr_prev_60d',
    'v_incr_prev_1d', 'v_incr_prev_5d', 'v_incr_prev_10d', 'v_incr_prev_20d', 'v_incr_prev_60d'
    ]

# 行列筛选
df = df.dropna()
df = df[['label'] + features]
print(df.head())

# 训练测试集划分
X = df[features]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print("")
print("shape of X_train:", X_train.shape)
print("shape of y_train:", y_train.shape)
print("shape of X_test:", X_test.shape)
print("shape of y_test", y_test.shape)

#xgboost
model = XGBClassifier()
model.fit(X_train, y_train)
print(model)
y_pred = model.predict(X_train)
accuracy = accuracy_score(y_train, y_pred)
print("Accuracy on train: %.2f%%" % (accuracy * 100.0))
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy on test: %.2f%%" % (accuracy * 100.0))

# 测试结果输出
df_test = pd.DataFrame(y_pred, index=y_test.index, columns=['pred'])
df_test = df_test.reset_index()
df = df.reset_index()
df_test = pd.merge(df_test, df, on='key', how='inner')
df_test = df_test.set_index('key')
df_test.to_csv("test.csv")


