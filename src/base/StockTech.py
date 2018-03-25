#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import types
import numpy as np
import pandas as pd
import tushare as ts
sys.path.append("../..")
from conf.config import *

def is_highest(l, k, m=3):
	try:
		if np.isnan(l[k]):
			return False
		for i in range(k-m, k+m+1):
			if i == k:
				continue
			if l[k] < l[i]:
				return False
		return True
	except IndexError:
		return False
	
def is_lowest(l, k, m=3):
	try:
		if np.isnan(l[k]):
			return False
		for i in range(k-m, k+m+1):
			if i == k:
				continue
			if l[k] > l[i]:
				return False
		return True
	except IndexError:
		return False

class StockTech:

	@staticmethod
	def analyzeMACD(df, macd_index):
		""" 分析MACD """
		"""
			返回值示例：
			{
				"n" : 100,
				"n_parts" : 3,
				"p_sign" : ['-', '+', '-'],
				"p_len" : [25, 50, 25],
				"p_peaks" : [2, 3, 1],
				"peaks":[('-',4,'2015-08-23',-0.34),('-',20,'2015-07-18',-0.29),...]
			}
		"""

		macd_ = {}
		df = df.sort_index(ascending=False)
		n = len(df)
		key_array = list(df.index)
		macd_array = list(df[macd_index])
		n_parts = 0
		p_sign = []
		p_len = []
		count = 0
		for i in range(n):
			if macd_array[i] >= 0:
				sign = "+"
			else:
				sign = "-"
			if i == 0: 
				count += 1
				last_sign = sign
			elif sign == last_sign:
				count += 1
			else:
				p_sign.append(last_sign)
				p_len.append(count)
				n_parts += 1
				count = 1
				last_sign = sign
		p_sign.append(sign)
		p_len.append(count)
		n_parts += 1

		j = 0
		peaks = []
		p_peaks = []
		for i in range(n_parts):
			sign = p_sign[i]
			p_so = j
			p_eo = j + p_len[i]

			count = 0
			for k in range(p_so, p_eo):
				if sign == "+":
					if is_highest(macd_array, k):
						peaks.append(('+', k, key_array[k], macd_array[k]))
						count += 1
				if sign == "-":
					if is_lowest(macd_array, k):
						peaks.append(('-', k, key_array[k], macd_array[k]))
						count += 1
			p_peaks.append(count)
			j = p_eo

		macd_["n"] = n
		macd_["n_parts"] = n_parts
		macd_["p_sign"] = p_sign
		macd_["p_len"] = p_len
		macd_["p_peaks"] = p_peaks
		macd_["peaks"] = peaks

		return macd_


	@staticmethod
	def getTrend(df, close_index, low_index, high_index):

		"""	获得股票趋势信息 """
		""" 
			返回值示例：
			{
				"high_slope":0.021,
				"low_slope":0.019,
				"prev_high":39.42,
				"prev_low":34.03,
				"next_high":42.23,
				"next_low":38.39,
				"diff_high":-0.124,
				"diff_low":0.026,
				"price":40.02,
				"points":[('+',4,'2015-08-23',39.28),('-',9,'2015-08-18',36.25),...]
			}
		"""

		trend = {}
		df = df.sort_index(ascending=False)
		n = len(df)
		key_array = list(df.index)
		close_array = list(df[close_index])
		low_array = list(df[low_index])
		high_array = list(df[high_index])

		# 获得当前价格
		price = close_array[0]
		trend["price"] = price

		# 获得近期的高点和低点
		cnt = 0
		h_cnt = 0
		l_cnt = 0
		points = []
		for i in range(2,n):
			if is_highest(high_array, i):
				cnt += 1
				h_cnt += 1
				key = key_array[i]
				value = high_array[i]
				points.append( ('+', i, key, value) )
			if is_lowest(low_array, i):
				cnt += 1
				l_cnt += 1
				key = key_array[i]
				value = low_array[i]
				points.append( ('-', i, key, value) )
			if cnt == 7:
				break
		trend["points"] = points

		# 计算斜率、之前的高低点、未来的高低点
		trend["prev_high"] = np.nan
		trend["prev_low"] = np.nan
		trend["next_high"] = np.nan
		trend["next_low"] = np.nan
		trend["high_slope"] = np.nan
		trend["low_slope"] = np.nan
		trend["diff_prev_high"] = np.nan
		trend["diff_prev_low"] = np.nan
		trend["diff_high"] = np.nan
		trend["diff_low"] = np.nan
		if h_cnt >= 2:
			hp = []
			for i in range(0, cnt):
				if points[i][0] == '+':
					hp.append(points[i])
			high_slope = ( hp[0][3] - hp[1][3] ) / ( hp[1][1] - hp[0][1] ) # 价格变化 / 时间间隔
			prev_high = hp[0][3]
			next_high = hp[0][3] + high_slope * hp[0][1] # 预测下一高点
			diff_prev_high = ( prev_high - price ) / price # 当前价格到下一高点的涨幅
			diff_high = ( next_high - price ) / price # 当前价格到下一高点的涨幅
			high_slope = high_slope / hp[1][3] # 斜率归一化到百分数
			trend["high_slope"] = high_slope
			trend["prev_high"] = prev_high 
			trend["next_high"] = next_high 
			trend["diff_prev_high"] = diff_prev_high 
			trend["diff_high"] = diff_high 
		if l_cnt >= 2:
			lp = []
			for i in range(0, cnt):
				if points[i][0] == '-':
					lp.append(points[i])
			low_slope = ( lp[0][3] - lp[1][3] ) / ( lp[1][1] - lp[0][1] ) # 价格变化 / 时间间隔
			prev_low = lp[0][3]
			next_low = lp[0][3] + low_slope * lp[0][1] # 预测下一低点
			diff_prev_low = ( price - prev_low ) / price # 当前价格到下一低点的跌幅
			diff_low = ( price - next_low ) / price # 当前价格到下一低点的跌幅
			low_slope = low_slope / lp[1][3] # 斜率归一化到百分数
			trend["low_slope"] = low_slope
			trend["prev_low"] = prev_low
			trend["next_low"] = next_low
			trend["diff_prev_low"] = diff_prev_low
			trend["diff_low"] = diff_low

		return trend
			
if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print "Error: invalid parameters."
		sys.exit(1)
	code = str(sys.argv[1])
	df = pd.read_csv("/root/workspace/StockAnalyzer/analysis/stock_technical_analysis/" + code + ".csv").set_index("date")
	t = StockTech.getTrend(df, "close", "low", "high")
	print t

