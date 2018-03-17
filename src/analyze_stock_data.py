#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
import talib
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.File import File
from base.Time import Time
from base.Data import Data
from base.Stock import Stock
from base.StockTech import StockTech

def get_index_daily_incr():

	""" 获得所有指数历史每天的未来价格增长数据（用于预测/对比） """

	Log.notice("started.")

	index_history_path = INDEX_HISTORY_PATH
	if not os.path.isdir(index_history_path):
		return False
	index_incr_path = INDEX_DAILY_INCR_PATH
	if not os.path.isdir(index_incr_path):
		os.mkdir(stock_incr_path)

	for code in ["sh", "sz", "hs300", "cyb", "zxb", "sz50"]:

		index_history_data_path = os.path.join(index_history_path, code + ".csv")
		if not os.path.isfile(index_history_data_path):
			continue
		index_incr_data_path = os.path.join(index_incr_path, code + ".csv")

		df = pd.read_csv(index_history_data_path).sort_index(by="date")
		df = df.set_index("date")
		df["open1"] = df["open"].shift(-1)
		df["open2"] = df["open"].shift(-2)
		df["open3"] = df["open"].shift(-3)
		df["open4"] = df["open"].shift(-4)
		df["close1"] = df["close"].shift(-1)
		df["close2"] = df["close"].shift(-2)
		df["close3"] = df["close"].shift(-3)
		df["incr1"] = df["close"].pct_change(periods=1).shift(-1).apply(Data.formatFloat, precision=4)
		df["incr3"] = df["close"].pct_change(periods=3).shift(-3).apply(Data.formatFloat, precision=4)
		df["incr5"] = df["close"].pct_change(periods=5).shift(-5).apply(Data.formatFloat, precision=4)
		df["incr10"] = df["close"].pct_change(periods=10).shift(-10).apply(Data.formatFloat, precision=4)
		df["incr20"] = df["close"].pct_change(periods=20).shift(-20).apply(Data.formatFloat, precision=4)
		df["incr60"] = df["close"].pct_change(periods=60).shift(-60).apply(Data.formatFloat, precision=4)
		df["incr1_oc"] = ( ( df["close1"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr2_oc"] = ( ( df["close2"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr3_oc"] = ( ( df["close3"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr1_oo"] = ( ( df["open2"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr2_oo"] = ( ( df["open3"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr3_oo"] = ( ( df["open4"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df = df[["incr1", "incr3", "incr5", "incr10", "incr20", "incr60", "incr1_oc", "incr2_oc", "incr3_oc", "incr1_oo", "incr2_oo", "incr3_oo"]]
		df.to_csv(index_incr_data_path)

	Log.notice("finished.")

	return True

def get_stock_daily_incr():

	""" 获得所有股票历史每天的未来价格增长数据（用于预测） """

	Log.notice("started.")

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False
	stock_incr_path = STOCK_DAILY_INCR_PATH
	if not os.path.isdir(stock_incr_path):
		os.mkdir(stock_incr_path)

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index

	for code in stock_list:

		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		stock_incr_data_path = os.path.join(stock_incr_path, code + ".csv")

		df = pd.read_csv(stock_history_data_path).sort_index(by="date")
		df = df.set_index("date")
		df["open1"] = df["open"].shift(-1)
		df["open2"] = df["open"].shift(-2)
		df["open3"] = df["open"].shift(-3)
		df["open4"] = df["open"].shift(-4)
		df["close1"] = df["close"].shift(-1)
		df["close2"] = df["close"].shift(-2)
		df["close3"] = df["close"].shift(-3)
		df["incr1"] = df["close"].pct_change(periods=1).shift(-1).apply(Data.formatFloat, precision=4)
		df["incr3"] = df["close"].pct_change(periods=3).shift(-3).apply(Data.formatFloat, precision=4)
		df["incr5"] = df["close"].pct_change(periods=5).shift(-5).apply(Data.formatFloat, precision=4)
		df["incr10"] = df["close"].pct_change(periods=10).shift(-10).apply(Data.formatFloat, precision=4)
		df["incr20"] = df["close"].pct_change(periods=20).shift(-20).apply(Data.formatFloat, precision=4)
		df["incr60"] = df["close"].pct_change(periods=60).shift(-60).apply(Data.formatFloat, precision=4)
		df["incr1_oc"] = ( ( df["close1"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr2_oc"] = ( ( df["close2"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr3_oc"] = ( ( df["close3"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr1_oo"] = ( ( df["open2"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr2_oo"] = ( ( df["open3"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df["incr3_oo"] = ( ( df["open4"] - df["open1"] ) / df["open1"] ).apply(Data.formatFloat, precision=4)
		df = df[["incr1", "incr3", "incr5", "incr10", "incr20", "incr60", "incr1_oc", "incr2_oc", "incr3_oc", "incr1_oo", "incr2_oo", "incr3_oo"]]
		df.to_csv(stock_incr_data_path)

	Log.notice("finished.")

	return True

def get_stock_tech():

	""" 获得股票的技术指标 """

	Log.notice("started.")

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False

	out_path = STOCK_TECHNICAL_ANALYSIS_PATH
	if not os.path.isdir(out_path):
		os.mkdir(out_path)

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()

	for code in stock_list:

		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		out_file = os.path.join(out_path, code + ".csv")
		df = pd.read_csv(stock_history_data_path).set_index("date").sort_index()

		# basics 
		df["change"] = df["close"].pct_change(periods=1)

		# MAX & MIN
		z = talib.MAX(np.asarray(df["close"]), 3)
		df["MAX3"] = z
		z = talib.MAX(np.asarray(df["close"]), 5)
		df["MAX5"] = z
		z = talib.MAX(np.asarray(df["close"]), 10)
		df["MAX10"] = z
		z = talib.MAX(np.asarray(df["close"]), 20)
		df["MAX20"] = z
		z = talib.MAX(np.asarray(df["close"]), 60)
		df["MAX60"] = z
		z = talib.MAX(np.asarray(df["close"]), 180)
		df["MAX180"] = z
		z = talib.MIN(np.asarray(df["close"]), 3)
		df["MIN3"] = z
		z = talib.MIN(np.asarray(df["close"]), 5)
		df["MIN5"] = z
		z = talib.MIN(np.asarray(df["close"]), 10)
		df["MIN10"] = z
		z = talib.MIN(np.asarray(df["close"]), 20)
		df["MIN20"] = z
		z = talib.MIN(np.asarray(df["close"]), 60)
		df["MIN60"] = z
		z = talib.MIN(np.asarray(df["close"]), 180)
		df["MIN180"] = z

		# VMAX & VMIN
		z = talib.MAX(np.asarray(df["amount"]), 3)
		df["VMAX3"] = z
		z = talib.MAX(np.asarray(df["amount"]), 5)
		df["VMAX5"] = z
		z = talib.MAX(np.asarray(df["amount"]), 10)
		df["VMAX10"] = z
		z = talib.MAX(np.asarray(df["amount"]), 20)
		df["VMAX20"] = z
		z = talib.MAX(np.asarray(df["amount"]), 60)
		df["VMAX60"] = z
		z = talib.MAX(np.asarray(df["amount"]), 180)
		df["VMAX180"] = z
		z = talib.MIN(np.asarray(df["amount"]), 3)
		df["VMIN3"] = z
		z = talib.MIN(np.asarray(df["amount"]), 5)
		df["VMIN5"] = z
		z = talib.MIN(np.asarray(df["amount"]), 10)
		df["VMIN10"] = z
		z = talib.MIN(np.asarray(df["amount"]), 20)
		df["VMIN20"] = z
		z = talib.MIN(np.asarray(df["amount"]), 60)
		df["VMIN60"] = z
		z = talib.MIN(np.asarray(df["amount"]), 180)
		df["VMIN180"] = z

		# MA & VMA
		z = talib.MA(np.asarray(df["close"]), 3)
		df["MA3"] = z
		z = talib.MA(np.asarray(df["close"]), 5)
		df["MA5"] = z
		z = talib.MA(np.asarray(df["close"]), 10)
		df["MA10"] = z
		z = talib.MA(np.asarray(df["close"]), 20)
		df["MA20"] = z
		z = talib.MA(np.asarray(df["close"]), 60)
		df["MA60"] = z
		z = talib.MA(np.asarray(df["close"]), 180)
		df["MA180"] = z
		z = talib.MA(np.asarray(df["amount"]), 3)
		df["VMA3"] = z
		z = talib.MA(np.asarray(df["amount"]), 5)
		df["VMA5"] = z
		z = talib.MA(np.asarray(df["amount"]), 10)
		df["VMA10"] = z
		z = talib.MA(np.asarray(df["amount"]), 20)
		df["VMA20"] = z
		z = talib.MA(np.asarray(df["amount"]), 60)
		df["VMA60"] = z
		z = talib.MA(np.asarray(df["amount"]), 180)
		df["VMA180"] = z
		

		# MACD
		z = talib.MACD(np.asarray(df["close"]))
		df["MACD"] = z[2] * 2 # MACD_HIST * 2 -> MACD
		df["MACD_DIFF"] = z[0] # MACD -> MACD_DIFF
		df["MACD_DEA"] = z[1] # MACD_SIGNAL -> MACD_DEA

		# RSI
		z = talib.RSI(np.asarray(df["close"]), 6)
		df["RSI6"] = z
		z = talib.RSI(np.asarray(df["close"]), 12)
		df["RSI12"] = z
		z = talib.RSI(np.asarray(df["close"]), 24)
		df["RSI24"] = z

		# CCI
		z = talib.CCI(np.asarray(df["high"]), np.asarray(df["low"]), np.asarray(df["close"]))
		df["CCI"] = z

		# DMI (ADX & ADXR)
		z = talib.ADX(np.asarray(df["high"]), np.asarray(df["low"]), np.asarray(df["close"]))
		df["ADX"] = z
		z = talib.ADXR(np.asarray(df["high"]), np.asarray(df["low"]), np.asarray(df["close"]))
		df["ADXR"] = z

		df.to_csv(out_file)

	Log.notice("finished.")

	return True

def get_stock_daily_features():

	""" 获得股票天级特征 """

	Log.notice("started.")

	stock_tech_path = STOCK_TECHNICAL_ANALYSIS_PATH
	if not os.path.isdir(stock_tech_path):
		return False

	out_path = STOCK_DAILY_FEATURE_PATH
	if not os.path.isdir(out_path):
		os.mkdir(out_path)

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()

	for code in stock_list:

		stock_tech_data_path = os.path.join(stock_tech_path, code + ".csv")
		if not os.path.isfile(stock_tech_data_path):
			continue
		out_file = os.path.join(out_path, code + ".csv")
		df = pd.read_csv(stock_tech_data_path).set_index("date").sort_index()

		# basic
		df["prev_close"] = df["close"].shift(1)

		# price
		df["change-1"] = df["close"].pct_change(periods=1).shift(1)
		df["change-2"] = df["close"].pct_change(periods=1).shift(2)
		df["change-3"] = df["close"].pct_change(periods=1).shift(3)
		df["change-4"] = df["close"].pct_change(periods=1).shift(4)
		df["change-open"] = ( df["open"] - df["prev_close"] ) / df["prev_close"]
		df["change-daily"] = ( df["close"] - df["open"] ) / df["prev_close"]
		df["amplitude"] = ( df["high"] - df["low"] ) / df["prev_close"]
		df["CHNG3"] = df["close"].pct_change(periods=3)
		df["CHNG5"] = df["close"].pct_change(periods=5)
		df["CHNG10"] = df["close"].pct_change(periods=10)
		df["CHNG20"] = df["close"].pct_change(periods=20)
		df["CHNG60"] = df["close"].pct_change(periods=60)
		df["CHNG180"] = df["close"].pct_change(periods=180)
		df["C/MAX3"] = df["close"] / df["MAX3"]
		df["C/MAX5"] = df["close"] / df["MAX5"]
		df["C/MAX10"] = df["close"] / df["MAX10"]
		df["C/MAX20"] = df["close"] / df["MAX20"]
		df["C/MAX60"] = df["close"] / df["MAX60"]
		df["C/MAX180"] = df["close"] / df["MAX180"]
		df["C/MIN3"] = df["close"] / df["MIN3"]
		df["C/MIN5"] = df["close"] / df["MIN5"]
		df["C/MIN10"] = df["close"] / df["MIN10"]
		df["C/MIN20"] = df["close"] / df["MIN20"]
		df["C/MIN60"] = df["close"] / df["MIN60"]
		df["C/MIN180"] = df["close"] / df["MIN180"]
		df["C/MA3"] = df["close"] / df["MA3"]
		df["C/MA5"] = df["close"] / df["MA5"]
		df["C/MA10"] = df["close"] / df["MA10"]
		df["C/MA20"] = df["close"] / df["MA20"]
		df["C/MA60"] = df["close"] / df["MA60"]
		df["C/MA180"] = df["close"] / df["MA180"]

		# volume
		df["V/VMAX3"] = df["amount"] / df["VMAX3"]
		df["V/VMAX5"] = df["amount"] / df["VMAX5"]
		df["V/VMAX10"] = df["amount"] / df["VMAX10"]
		df["V/VMAX20"] = df["amount"] / df["VMAX20"]
		df["V/VMAX60"] = df["amount"] / df["VMAX60"]
		df["V/VMAX180"] = df["amount"] / df["VMAX180"]
		df["V/VMIN3"] = df["amount"] / df["VMIN3"]
		df["V/VMIN5"] = df["amount"] / df["VMIN5"]
		df["V/VMIN10"] = df["amount"] / df["VMIN10"]
		df["V/VMIN20"] = df["amount"] / df["VMIN20"]
		df["V/VMIN60"] = df["amount"] / df["VMIN60"]
		df["V/VMIN180"] = df["amount"] / df["VMIN180"]
		df["V/VMA3"] = df["amount"] / df["VMA3"]
		df["V/VMA5"] = df["amount"] / df["VMA5"]
		df["V/VMA10"] = df["amount"] / df["VMA10"]
		df["V/VMA20"] = df["amount"] / df["VMA20"]
		df["V/VMA60"] = df["amount"] / df["VMA60"]
		df["V/VMA180"] = df["amount"] / df["VMA180"]

		df = df.drop(["prev_close", "open", "high", "low", "volume", 
				"MAX3", "MAX5", "MAX10", "MAX20", "MAX60", "MAX180", "MIN3", "MIN5", "MIN10", "MIN20", "MIN60", "MIN180",
				"VMAX3", "VMAX5", "VMAX10", "VMAX20", "VMAX60", "VMAX180", "VMIN3", "VMIN5", "VMIN10", "VMIN20", "VMIN60", "VMIN180",
				"MA3", "MA5", "MA10", "MA20", "MA60", "MA180", "VMA3", "VMA5", "VMA10", "VMA20", "VMA60", "VMA180"], axis=1)
		df.to_csv(out_file)

	Log.notice("finished.")

	return True

def get_stock_daily_features_of_one_day(date=""):

	""" 获得所有股票某天的天级特征 """

	Log.notice("started.")

	if date == "":
		date = Time.today()

	stock_feature_path = STOCK_DAILY_FEATURE_PATH
	if not os.path.isdir(stock_feature_path):
		return False

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()

	for code in stock_list:

		stock_feature_data = os.path.join(stock_feature_path, code + ".csv")
		if not os.path.isfile(stock_feature_data):
			continue
		feature_df = pd.read_csv(stock_feature_data).set_index("date")
		if date in feature_df.index:
			item = feature_df.loc[date]
			item ["code"] = code
			df = df.append(item, ignore_index=False)

	df = df.set_index("code")

	Log.notice("finished.")

	return df

def get_stock_trend(date=""):

	""" 获得股票的趋势信息 """

	Log.notice("started.")

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False

	out_file = STOCK_TREND_DATA_PATH

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()
	for code in stock_list:
		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		stock_history_df = pd.read_csv(stock_history_data_path)
		trend = StockTech.getTrend(stock_history_df, "close", "low", "high")
		trend["code"] = code
		df = df.append(trend, ignore_index=True)
	df = df.reindex(columns=["code", "price", "prev_high", "prev_low", "next_high", "next_low", "high_slope", "low_slope", "diff_high", "diff_low", "points"])
	df = df.set_index("code")
	df.to_csv(out_file)

	Log.notice("finished.")

	return True

def get_stock_pressure_support(date=""):

	""" 获得股票的压力和支撑信息 """

	Log.notice("started.")

	stock_history_path = STOCK_RESTORATION_HISTORY_PATH
	if not os.path.isdir(stock_history_path):
		return False

	out_file = STOCK_PRESSURE_SUPPORT_DATA_PATH

	stock_basics = Stock.get_stock_basics()
	stock_list = stock_basics.index
	df = pd.DataFrame()
	for code in stock_list:
		stock_history_data_path = os.path.join(stock_history_path, code + ".csv")
		if not os.path.isfile(stock_history_data_path):
			continue
		stock_history_df = pd.read_csv(stock_history_data_path)
		item = {}
		item["code"] = code
		trend = StockTech.getTrend(stock_history_df, "date", "high")
		item["pressure"] = trend["next_high"]
		item["pressure_slope"] = trend["high_slope"]
		item["pressure_diff"] = trend["diff_high"]
		trend = StockTech.getTrend(stock_history_df, "date", "low")
		item["support"] = trend["next_low"]
		item["support_slope"] = trend["low_slope"]
		item["support_diff"] = trend["diff_low"]
		item["price"] = trend["price"]
		df = df.append(item, ignore_index=True)
	df = df.reindex(columns=["code", "price", "pressure", "pressure_slope", "pressure_diff", "support", "support_slope", "support_diff"])
	df = df.set_index("code")
	df.to_csv(out_file)

	Log.notice("finished.")
	return True
		
if __name__ == "__main__":
	
	#get_index_daily_incr()
	#get_stock_daily_incr()
	get_stock_tech()
	get_stock_trend()
	#get_stock_pressure_support()
	get_stock_daily_features()
	#df = get_stock_daily_features_of_one_day("2015-12-18")
	#df.to_csv("x.csv")
	
