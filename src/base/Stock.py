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

class Stock:

	@staticmethod
	def norm_code(code):
		code = str(code)
		l = 6 - len(code)
		return '0' * l + code

	@staticmethod
	def norm_value(x):
		if isinstance(x, str):
			if x == "--":
				return np.nan
		return x

	@staticmethod
	def is_code(code):
		code = Stock.norm_code(code)
		if len(code) != 6:
			return False
		if code[:2] == "60" or code[:2] == "00" or code[:2] == "30":
			return True
		return False

	@staticmethod
	def get_market(code):
		code = Stock.norm_code(code)
		if len(code) == 6:
			if code[:2] == "60":
				return "sh"
			if code[:2] == "00" or code[:2] == "30":
				return "sz"
		return "unknown"
	
	@staticmethod
	def getUrl(code):
		code = Stock.norm_code(code)
		market = Stock.get_market(code)
		url = "http://quote.eastmoney.com/" + market + code + ".html"
		return url

	@staticmethod
	def get_stock_basics():
		stock_basics_csv_path = STOCK_BASICS_DATA_PATH
		if os.path.isfile(stock_basics_csv_path):
			stock_basics_df = pd.read_csv(stock_basics_csv_path, dtype={"code":"object"})
			stock_basics_df = stock_basics_df.set_index("code")
		else:
			stock_basics_df = ts.get_stock_basics()
		return stock_basics_df

	@staticmethod
	def get_stock_prices():
		stock_prices_csv_path = STOCK_PRICES_DATA_PATH
		if os.path.isfile(stock_prices_csv_path):
			stock_prices_df = pd.read_csv(stock_prices_csv_path, dtype={"code":"object"})
			stock_prices_df = stock_prices_df.set_index("code")
		else:
			stock_prices_df = ts.get_today_all()
			stock_prices_df = stock_prices_df.set_index("code")
		return stock_prices_df

	@staticmethod
	def get_stock_concept():
		stock_concept_csv_path = STOCK_CONCEPT_DATA_PATH
		load_flag = False
		if os.path.isfile(stock_concept_csv_path):
			stock_concept_df = pd.read_csv(stock_concept_csv_path, dtype={"code":"object"})
			stock_concept_df = stock_concept_df.set_index("code")
			load_flag = True
		else:
			stock_concept_df = ts.get_concept_classified()
			stock_concept_df = stock_concept_df.set_index("code")
		stock_concept_dict = {}
		for r in stock_concept_df.itertuples():
			code = r[0]
			c = r[2]
			if code in stock_concept_dict:
				stock_concept_dict[code] += ( "|" + c )
			else:
				stock_concept_dict[code] = c
		stock_concept_df = stock_concept_df["name"].drop_duplicates()
		stock_concept_list = []
		for i in stock_concept_df.index:
			if load_flag:
				code = i
				name = stock_concept_df[i]
				concept = stock_concept_dict[i]
			else:
				code = i.encode('utf-8')
				name = stock_concept_df[i].encode('utf-8')
				concept = stock_concept_dict[i].encode('utf-8')
			stock_concept_list.append( {"code":code, "name":name, "concept":concept} )
		stock_concept_df = pd.DataFrame(stock_concept_list)
		stock_concept_df = stock_concept_df.set_index("code")[["name", "concept"]]
		return stock_concept_df

	@staticmethod
	def get_10jqka_stock_concept():
		csv_path = STOCK_10JQKA_CONCEPT_DATA_PATH
		if not os.path.isfile(csv_path):
			return pd.DataFrame()
		df = pd.read_csv(csv_path, dtype={"code":"object"})
		df = df.set_index("code")
		return df

	@staticmethod
	def get_stock_info():
		stock_basics_df = Stock.get_stock_basics().reset_index()
		stock_prices_df = Stock.get_stock_prices().reset_index().drop("name", axis=1)
		#stock_concept_df = Stock.get_stock_concept().reset_index().drop("name", axis=1)
		stock_concept_df = Stock.get_10jqka_stock_concept().reset_index()
		df = stock_basics_df
		df = pd.merge(df, stock_prices_df, on="code", how="outer")
		df = pd.merge(df, stock_concept_df, on="code", how="outer")
		df["circulated_value"] = df["trade"] * df["outstanding"] / 10000
		return df.set_index("code")
	
if __name__ == "__main__":
	#df = Stock.get_10jqka_stock_concept()
	#df.to_csv("concept.csv")
	df = Stock.get_stock_info()
	df.to_csv("stock_info.csv")

