import os
import sys
import numpy as np
import pandas as pd
import talib
from sklearn import metrics
from config import *


"""
规范化股票代码
"""


def norm_code(code):
	code = str(code)
	l = 6 - len(code)
	return '0' * l + code


"""
根据年月日获得月份
"""


def get_month(date):
	month = date.split('-')[1]
	return int(month)


"""
根据年月日获得日期
"""


def get_day(date):
	day = date.split('-')[2]
	return int(day)


"""
规范化浮点数
"""


def norm_float(x, precision=4):
	f = "%." + str(precision) + "f"
	return f % x


"""
将timedelta转化为相隔天数
"""


def norm_delta_days(delta):
	return delta.days


"""
计算评估结果
"""


def eval(y, y_pred, threshold=0.5):
	y_pred = (y_pred >= threshold) * 1
	eval_dict = {}
	eval_dict["accuracy"] = metrics.accuracy_score(y, y_pred)
	eval_dict["auc"] = metrics.roc_auc_score(y, y_pred)
	eval_dict["precision"] = metrics.precision_score(y, y_pred)
	eval_dict["recall"] = metrics.recall_score(y, y_pred)
	eval_dict["f1-score"] = metrics.f1_score(y, y_pred)
	eval_dict["confusion_matrix"] = metrics.confusion_matrix(y, y_pred)
	return eval_dict


"""
处理数据
"""


def process_data(df):

	# 计算目标
	#incr = df['high'].rolling(5).max().shift(-5) / df['close'] - 1  # 未来5日的最高涨幅
	incr = df['high'].rolling(10).max().shift(10) / df['close'] - 1  # 未来10日的最高涨幅
	#incr = df['high'].rolling(20).max().shift(20) / df['close'] - 1  # 未来20日的最高涨幅
	df['label'] = incr.apply(lambda x: 1 if x > 0.1 else 0)  # 目标价格上涨10%以上

	# 保留基础字段
	df = df[['label', 'date', 'open', 'close', 'high', 'low', 'volume']]

	# 计算特征

	## 时间特征
#	df['MONTH'] = df['date'].apply(get_month)
#	df['DAY'] = df['date'].apply(get_day)
	delta = pd.to_datetime(df['date']) - pd.to_datetime(df['date'].shift(1))
	df["DELTA_DAYS"] = delta.apply(norm_delta_days)  # 与上一交易日间隔天数

	## 本日各价格之间的变化
	df['OPEN_CLOSE_R'] = df['open'] / df['close']  # 当日开盘价/当日收盘价
	df['HIGH_CLOSE_R'] = df['high'] / df['close']  # 当日最高价/当日收盘价
	df['LOW_CLOSE_R'] = df['low'] / df['close']  # 当日最低价/当日收盘价
	df['HIGH_OPEN_R'] = df['high'] / df['open']  # 当日最高价/当日开盘价
	df['LOW_OPEN_R'] = df['low'] / df['open']  # 当日最低价/当日开盘价
	df['HIGH_LOW_R'] = df['high'] / df['low']  # 当日最高价/当日最低价

	## 前日与本日的量价变化
	prev_close = df['close'].shift(1)
	prev_volume = df['volume'].shift(1)
	df['PREV_OPEN_R'] = prev_close / df['open']  # 前日收盘价/当日开盘价
	df['PREV_CLOSE_R'] = prev_close / df['close']  # 前日收盘价/当日收盘价
	df['PREV_HIGH_R'] = prev_close / df['high']  # 前日收盘价/当日最高价
	df['PREV_LOW_R'] = prev_close / df['low']  # 前日收盘价/当日最低价
	df['PREV_VOL_R'] = prev_volume / df['volume']  # 前日交易量/当日交易量

	## 近日量价变化
	df['PREV_5D_R'] = df['close'].pct_change(periods=5)  # 近5日价格涨幅
	df['PREV_10D_R'] = df['close'].pct_change(periods=10)  # 近10日价格涨幅
	df['PREV_20D_R'] = df['close'].pct_change(periods=20)  # 近20日价格涨幅
	df['PREV_60D_R'] = df['close'].pct_change(periods=60)  # 近60日价格涨幅
	df['V_PREV_5D_R'] = df['volume'].pct_change(periods=5)  # 近5日交易量涨幅
	df['V_PREV_10D_R'] = df['volume'].pct_change(periods=10)  # 近10日交易量涨幅
	df['V_PREV_20D_R'] = df['volume'].pct_change(periods=20)  # 近20日交易量涨幅
	df['V_PREV_60D_R'] = df['volume'].pct_change(periods=60)  # 近60日交易量涨幅

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

	return df


"""
读取数据
"""


def load_data(data_file):
	# 读取文件
	df = pd.read_csv(data_file)
	# 计算索引
	df['code'] = df['code'].apply(norm_code)
	df['key'] = df['code'] + ':' + df['date']
	df = df.set_index('key')
	return df


"""
加载并处理数据
"""


def load_and_process(data_path, train=True, sample=1.0, date=""):
	merge_df = pd.DataFrame()
	if not os.path.isdir(data_path):
		print("Error: data path '%s' does not exist." % data_path)
		return merge_df
	for file in os.listdir(data_path):
		# 加载数据
		f = os.path.join(data_path, file)
		print("loading %s ..." % f)
		df = load_data(f)
		# 处理数据
		print("processing ...")
		df = process_data(df)
		# 随机抽样
		if sample < 1.0:
			n = int(sample * len(df))
			if n == 0:
				continue
			df = df.sample(n=n)
		# 处理label
		if train== True:
			df = df[df['label'].notna()]
		# 处理date
		if date != "":
			df = df[df['date'] == date]
		df = df.drop('date', axis=1)
		# 汇总股票数据
		print("merging %d records ..." % len(df))
		merge_df = merge_df.append(df)
	return merge_df

