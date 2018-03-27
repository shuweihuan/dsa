#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt

from sklearn import model_selection
from sklearn import metrics

from xgboost import XGBClassifier

# 规范化股票代码
def norm_code(code):
    code = str(code)
    l = 6 - len(code)
    return '0' * l + code

# 规范化浮点数
def norm_float(x, precision=4):
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

def eval(y, y_pred, threshold=0.5):
    y_pred = (y_pred >= threshold) * 1
    print("-> Accuracy: %.4f" % metrics.accuracy_score(y, y_pred))
    print("-> AUC: %.4f" % metrics.roc_auc_score(y, y_pred))
    print("-> Precision: %.4f" % metrics.precision_score(y, y_pred))
    print("-> Recall: %.4f" % metrics.recall_score(y, y_pred))
    print("-> F1-score: %.4f" % metrics.f1_score(y, y_pred))
    print("-> Confusion Matrix:")
    print(metrics.confusion_matrix(y, y_pred))

"""
处理数据，生成预测目标和特征
"""
def process(df):

    # 计算目标
    incr = df['close'].pct_change(periods=5).shift(-5)  # 未来五日涨幅
    df['label'] = incr.apply(is_incr)
    df = df[['label', 'open', 'close', 'high', 'low', 'volume']]

    # 计算特征

    ## 本日各价格之间的变化
    df['OPEN_CLOSE_R'] = df['open'] / df['close']
    df['HIGH__CLOSE_R'] = df['high'] / df['close']
    df['LOW_CLOSE_R'] = df['low'] / df['close']
    df['HIGH_OPEN_R'] = df['high'] / df['open']
    df['LOW_OPEN_R'] = df['low'] / df['open']
    df['HIGH_LOW_R'] = df['high'] / df['low']

    ## 前日与本日的量价变化
    prev_close = df['close'].shift(-1)
    prev_volume = df['volume'].shift(-1)
    df['PREV_OPEN_R'] = prev_close / df['open']
    df['PREV_CLOSE_R'] = prev_close / df['close']
    df['PREV_HIGH_R'] = prev_close / df['high']
    df['PREV_LOW_R'] = prev_close / df['low']
    df['PREV_VOL_R'] = prev_volume / df['volume']

    ## 近日量价变化
    df['PREV_5D_R'] = df['close'].pct_change(periods=5) # 近5日价格涨幅
    df['PREV_10D_R'] = df['close'].pct_change(periods=10) # 近10日价格涨幅
    df['PREV_20D_R'] = df['close'].pct_change(periods=20) # 近20日价格涨幅
    df['PREV_60D_R'] = df['close'].pct_change(periods=60) # 近60日价格涨幅
    df['V_PREV_5D_R'] = df['volume'].pct_change(periods=5) # 近5日交易量涨幅
    df['V_PREV_10D_R'] = df['volume'].pct_change(periods=10) # 近10日交易量涨幅
    df['V_PREV_20D_R'] = df['volume'].pct_change(periods=20) # 近20日交易量涨幅
    df['V_PREV_60D_R'] = df['volume'].pct_change(periods=60) # 近60日交易量涨幅

    ## MAX & V_MAX与当日收盘价的相对值
    max_5d = talib.MAX(np.asarray(df['close']), 5)
    max_10d = talib.MAX(np.asarray(df['close']), 10)
    max_20d = talib.MAX(np.asarray(df['close']), 20)
    max_60d = talib.MAX(np.asarray(df['close']), 60)
    v_max_5d = talib.MAX(np.asarray(df['volume']), 5)
    v_max_10d = talib.MAX(np.asarray(df['volume']), 10)
    v_max_20d = talib.MAX(np.asarray(df['volume']), 20)
    v_max_60d = talib.MAX(np.asarray(df['volume']), 60)
    df['MAX_5D_R'] = max_5d / df['close']
    df['MAX_10D_R'] = max_10d / df['close']
    df['MAX_20D_R'] = max_20d / df['close']
    df['MAX_60D_R'] = max_60d / df['close']
    df['V_MAX_5D_R'] = v_max_5d / df['volume']
    df['V_MAX_10D_R'] = v_max_20d / df['volume']
    df['V_MAX_20D_R'] = v_max_20d / df['volume']
    df['V_MAX_60D_R'] = v_max_60d / df['volume']

    ## MIN & V_MIN与当日收盘价的相对值
    min_5d = talib.MIN(np.asarray(df['close']), 5)
    min_10d = talib.MIN(np.asarray(df['close']), 10)
    min_20d = talib.MIN(np.asarray(df['close']), 20)
    min_60d = talib.MIN(np.asarray(df['close']), 60)
    v_min_5d = talib.MIN(np.asarray(df['volume']), 5)
    v_min_10d = talib.MIN(np.asarray(df['volume']), 10)
    v_min_20d = talib.MIN(np.asarray(df['volume']), 20)
    v_min_60d = talib.MIN(np.asarray(df['volume']), 60)
    df['MIN_5D_R'] = min_5d / df['close']
    df['MIN_10D_R'] = min_10d / df['close']
    df['MIN_20D_R'] = min_20d / df['close']
    df['MIN_60D_R'] = min_60d / df['close']
    df['V_MIN_5D_R'] = v_min_5d / df['volume']
    df['V_MIN_10D_R'] = v_min_10d / df['volume']
    df['V_MIN_20D_R'] = v_min_20d / df['volume']
    df['V_MIN_60D_R'] = v_min_60d / df['volume']

    ## MA & V_MA与当日收盘价的相对值
    ma_5d = talib.MA(np.asarray(df["close"]), 5)
    ma_10d = talib.MA(np.asarray(df["close"]), 10)
    ma_20d = talib.MA(np.asarray(df["close"]), 20)
    ma_60d = talib.MA(np.asarray(df["close"]), 60)
    v_ma_5d = talib.MA(np.asarray(df["volume"]), 5)
    v_ma_10d = talib.MA(np.asarray(df["volume"]), 10)
    v_ma_20d = talib.MA(np.asarray(df["volume"]), 20)
    v_ma_60d = talib.MA(np.asarray(df["volume"]), 60)
    df['MA_5D_R'] = ma_5d / df['close']
    df['MA_10D_R'] = ma_10d / df['close']
    df['MA_20D_R'] = ma_20d / df['close']
    df['MA_60D_R'] = ma_60d / df['close']
    df['V_MA_5D_R'] = v_ma_5d / df['volume']
    df['V_MA_10D_R'] = v_ma_10d / df['volume']
    df['V_MA_20D_R'] = v_ma_20d / df['volume']
    df['V_MA_60D_R'] = v_ma_60d / df['volume']

    # 行列筛选
    df = df[incr.notna()]

    return df

# 加载数据
def load_data(path):
    merge_df = pd.DataFrame()
    if not os.path.isdir(path):
        return merge_df
    for file in os.listdir(path):
        f = os.path.join(path, file)
        print("-> Loading", f, "...")
        df = pd.read_csv(f)
        old_len = len(df)
        # 计算索引
        df['code'] = df['code'].apply(norm_code)
        df['key'] = df['code'] + ':' + df['date']
        df = df.set_index('key')
        # 处理数据
        df = process(df)
        new_len = len(df)
        print("-> Total", old_len, "lines, trimmed to", new_len, "lines.")
        # 追加一支股票数据
        merge_df = merge_df.append(df)
    return merge_df

df = load_data("../data/stock_history")

# 训练测试集划分
X = df.iloc[:, 1:]
y = df.iloc[:, 0]
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=0)
print("")
print("-> Shape of X_train:", X_train.shape)
print("-> Shape of y_train:", y_train.shape)
print("-> Shape of X_test:", X_test.shape)
print("-> Shape of y_test", y_test.shape)

#xgboost
#model = XGBClassifier()
model = XGBClassifier(objective='binary:logistic', eval_metric='logloss')
model.fit(X_train, y_train)
print(model)
y_pred = model.predict(X_train)
print("Evaluation on train")
eval(y_train, y_pred)
y_pred = model.predict(X_test)
print("Evaluation on test")
eval(y_test, y_pred)
y_pred = model.predict_proba(X_test)[:, 1]
print("Evaluation on test with threshold=0.75")
eval(y_test, y_pred, 0.75)

# 测试结果输出
df_test = pd.DataFrame(y_pred, index=y_test.index, columns=['pred'])
df_test = df_test.reset_index()
df = df.reset_index()
df_test = pd.merge(df_test, df, on='key', how='inner')
df_test = df_test.set_index('key')
df_test.to_csv("test.csv")

