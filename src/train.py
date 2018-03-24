#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
import talib
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

# 特征定义
features = [
    'open', 'close', 'high', 'low', 'volume',
    'diff_prev_open', 'diff_prev_high', 'diff_prev_low',
    'diff_open_close', 'diff_open_high', 'diff_open_low', 'diff_close_high', 'diff_close_low',
    'incr_prev_1d', 'incr_prev_5d', 'incr_prev_10d', 'incr_prev_20d', 'incr_prev_60d',
    'v_incr_prev_1d', 'v_incr_prev_5d', 'v_incr_prev_10d', 'v_incr_prev_20d', 'v_incr_prev_60d',
    'MAX_5D_R', 'MAX_10D_R', 'MAX_20D_R', 'MAX_60D_R',
    'V_MAX_5D_R', 'V_MAX_10D_R', 'V_MAX_20D_R', 'V_MAX_60D_R',
    'MIN_5D_R', 'MIN_10D_R', 'MIN_20D_R', 'MIN_60D_R',
    'V_MIN_5D_R', 'V_MIN_10D_R', 'V_MIN_20D_R', 'V_MIN_60D_R',
    'MA_5D_R', 'MA_10D_R', 'MA_20D_R', 'MA_60D_R',
    'V_MA_5D_R', 'V_MA_10D_R', 'V_MA_20D_R', 'V_MA_60D_R',
]

# 计算目标和特征
def calc_features(df):

    # 计算目标
    df['incr_next_1d'] = df['close'].pct_change(periods=1).shift(-1)
    df['incr_next_5d'] = df['close'].pct_change(periods=5).shift(-5)
    df['label'] = df['incr_next_5d'].apply(is_incr)
    #df.to_csv("debug.csv")

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
    ## MAX & V_MAX
    df['MAX_5D'] = talib.MAX(np.asarray(df['close']), 5)
    df['MAX_10D'] = talib.MAX(np.asarray(df['close']), 10)
    df['MAX_20D'] = talib.MAX(np.asarray(df['close']), 20)
    df['MAX_60D'] = talib.MAX(np.asarray(df['close']), 60)
    df['V_MAX_5D'] = talib.MAX(np.asarray(df['volume']), 5)
    df['V_MAX_10D'] = talib.MAX(np.asarray(df['volume']), 10)
    df['V_MAX_20D'] = talib.MAX(np.asarray(df['volume']), 20)
    df['V_MAX_60D'] = talib.MAX(np.asarray(df['volume']), 60)
    ## MIN & V_MIN
    df['MIN_5D'] = talib.MIN(np.asarray(df['close']), 5)
    df['MIN_10D'] = talib.MIN(np.asarray(df['close']), 10)
    df['MIN_20D'] = talib.MIN(np.asarray(df['close']), 20)
    df['MIN_60D'] = talib.MIN(np.asarray(df['close']), 60)
    df['V_MIN_5D'] = talib.MIN(np.asarray(df['volume']), 5)
    df['V_MIN_10D'] = talib.MIN(np.asarray(df['volume']), 10)
    df['V_MIN_20D'] = talib.MIN(np.asarray(df['volume']), 20)
    df['V_MIN_60D'] = talib.MIN(np.asarray(df['volume']), 60)
    ## MA & V_MA
    df['MA_5D'] = talib.MA(np.asarray(df["close"]), 5)
    df['MA_10D'] = talib.MA(np.asarray(df["close"]), 10)
    df['MA_20D'] = talib.MA(np.asarray(df["close"]), 20)
    df['MA_60D'] = talib.MA(np.asarray(df["close"]), 60)
    df['V_MA_5D'] = talib.MA(np.asarray(df["volume"]), 5)
    df['V_MA_10D'] = talib.MA(np.asarray(df["volume"]), 10)
    df['V_MA_20D'] = talib.MA(np.asarray(df["volume"]), 20)
    df['V_MA_60D'] = talib.MA(np.asarray(df["volume"]), 60)
    ## MAX & V_MAX与当日收盘价的相对值
    df['MAX_5D_R'] = df['MAX_5D'] / df['close']
    df['MAX_10D_R'] = df['MAX_10D'] / df['close']
    df['MAX_20D_R'] = df['MAX_20D'] / df['close']
    df['MAX_60D_R'] = df['MAX_60D'] / df['close']
    df['V_MAX_5D_R'] = df['V_MAX_5D'] / df['volume']
    df['V_MAX_10D_R'] = df['V_MAX_10D'] / df['volume']
    df['V_MAX_20D_R'] = df['V_MAX_20D'] / df['volume']
    df['V_MAX_60D_R'] = df['V_MAX_60D'] / df['volume']
    ## MIN & V_MIN与当日收盘价的相对值
    df['MIN_5D_R'] = df['MIN_5D'] / df['close']
    df['MIN_10D_R'] = df['MIN_10D'] / df['close']
    df['MIN_20D_R'] = df['MIN_20D'] / df['close']
    df['MIN_60D_R'] = df['MIN_60D'] / df['close']
    df['V_MIN_5D_R'] = df['V_MIN_5D'] / df['volume']
    df['V_MIN_10D_R'] = df['V_MIN_10D'] / df['volume']
    df['V_MIN_20D_R'] = df['V_MIN_20D'] / df['volume']
    df['V_MIN_60D_R'] = df['V_MIN_60D'] / df['volume']
    ## MA & V_MA与当日收盘价的相对值
    df['MA_5D_R'] = df['MA_5D'] / df['close']
    df['MA_10D_R'] = df['MA_10D'] / df['close']
    df['MA_20D_R'] = df['MA_20D'] / df['close']
    df['MA_60D_R'] = df['MA_60D'] / df['close']
    df['V_MA_5D_R'] = df['V_MA_5D'] / df['volume']
    df['V_MA_10D_R'] = df['V_MA_10D'] / df['volume']
    df['V_MA_20D_R'] = df['V_MA_20D'] / df['volume']
    df['V_MA_60D_R'] = df['V_MA_60D'] / df['volume']

    # 行列筛选
    df = df[df['incr_next_5d'].notna()]
    df = df[['label'] + features]

    return df

# 加载数据
def load_data(path):
    merge_df = pd.DataFrame()
    if not os.path.isdir(path):
        return merge_df
    for file in os.listdir(path):
        f = os.path.join(path, file)
        print("-> Loading ", f, " ...")
        df = pd.read_csv(f)
        old_len = len(df)
        # 计算索引
        df['code'] = df['code'].apply(norm_code)
        df['key'] = df['code'] + ':' + df['date']
        df = df.set_index('key')
        # 计算目标和特征
        df = calc_features(df)
        new_len = len(df)
        print("-> Total ", old_len, " lines, trimmed to ", new_len, " lines.")
        # 追加一支股票数据
        merge_df = merge_df.append(df)
    return merge_df

df = load_data("../data/stock_history")
#df.to_csv("data.csv")
#df = pd.read_csv("../data/stock_history/000066.csv")

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
# TODO target should be accuracy on 1
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


