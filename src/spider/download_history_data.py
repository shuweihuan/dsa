#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import types
import string
import numpy as np
import pandas as pd
import tushare as ts
sys.path.append("../..")
from conf.config import *
sys.path.append("..")
from base.Log import Log
from base.Time import Time
from base.Stock import Stock
#from base.Spider import Spider

#reload(sys)  
#sys.setdefaultencoding('utf8')

###################
# Stock List Data #
###################

def get_list_data(get_func):
	f = open('/dev/null', 'w')
	fbak = sys.stdout
	sys.stdout = f
	try:
		df = get_func()
	except:
		Log.warning(get_func.__name__ + "() failed.")
		return pd.DataFrame()
	f.close()
	sys.stdout = fbak
	if type(df) == types.NoneType:
		return pd.DataFrame()
	return df

def download_list_data(get_func, file_path, index=True):
	df = get_list_data(get_func)
	if df.empty:
		return False
	df.to_csv(file_path, index=index)
	return True

#####################
# Single Stock Data #
#####################

def get_single_data(code, get_func):
	f = open('/dev/null', 'w')
	fbak = sys.stdout
	sys.stdout = f
	try:
		df = get_func(code)
	except:
		Log.warning(get_func.__name__ + "('" + str(code) +"') failed.")
		return pd.DataFrame()
	f.close()
	sys.stdout = fbak
	if type(df) == types.NoneType:
		return pd.DataFrame()
	return df

def download_single_data(code, get_func, folder_path):
	df = get_single_data(code, get_func)
	if df.empty:
		return False
	f_name = os.path.join(folder_path, code+".csv")
	df.to_csv(f_name)
	return True

def download_all_single_data(get_func, folder_path):
	stock_list_df = get_list_data(ts.get_stock_basics)
	if stock_list_df.empty:
		return False
	if not os.path.isdir(folder_path):
		os.mkdir(folder_path)
	for code in stock_list_df.index:
		download_single_data(code, get_func, folder_path)
	return True

def download_all_stock_history():
	download_all_single_data(ts.get_k_data, STOCK_HISTORY_PATH)

def download_all_index_history():
	if not os.path.isdir(INDEX_HISTORY_PATH):
		os.mkdir(INDEX_HISTORY_PATH)
	for i in ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']:
		download_single_data(i, ts.get_k_data, INDEX_HISTORY_PATH)
	return True

if __name__ == '__main__':

	download_list_data(ts.get_index, INDEX_PRICE_DATA_PATH, index=False)
	download_list_data(ts.get_today_all, STOCK_PRICE_DATA_PATH, index=False)
	download_list_data(ts.get_stock_basics, STOCK_BASICS_DATA_PATH)

	download_all_index_history()
	#download_all_stock_history()

