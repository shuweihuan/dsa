import os
import sys
import numpy as np
import pandas as pd
import talib

sys.path.append("..")
from conf.config import *
from base.Log import Log


# 规范化股票代码
def norm_code(code):
	code = str(code)
	l = 6 - len(code)
	return '0' * l + code


def process_data(df, label=False, date=""):
	if label == True:
		# 计算目标
		## 预测未来5日最高涨幅
		incr = df['high'].rolling(5).max().shift(-5) / df['close'] - 1  # 未来五日的最高涨幅
		df['label'] = incr.apply(is_gt_10pp)  # 上涨10%以上

	# 保留基础字段
	if label == True:
		df = df[['label', 'date', 'open', 'close', 'high', 'low', 'volume']]
	else:
		df = df[['date', 'open', 'close', 'high', 'low', 'volume']]

	# 计算特征

	## 本日各价格之间的变化
	df['OPEN_CLOSE_R'] = df['open'] / df['close']
	df['HIGH_CLOSE_R'] = df['high'] / df['close']
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

	if label == True:
		# 行列筛选
		df = df[incr.notna()]

	if date != "":
		# 筛选指定日期
		df = df[df['date'] == date]

	# 丢弃date字段
	df = df.drop('date', axis=1)

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


def load_and_process(data_path, label=False, date=""):
	merge_df = pd.DataFrame()
	if not os.path.isdir(data_path):
		return merge_df
	for file in os.listdir(data_path):
		# 加载数据
		f = os.path.join(data_path, file)
		Log.notice("loading %s ..." % f)
		df = load_data(f)
		# 处理数据
		Log.notice("processing ...")
		df = process_data(df, label, date)
		# 追加一支股票数据
		Log.notice("merging %d records ..." % len(df))
		merge_df = merge_df.append(df)
	return merge_df
