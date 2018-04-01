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

reload(sys)  
sys.setdefaultencoding('utf8')

def download_k_data(folder_path, code, start, end, ktype, autype):
	try:
		Log.notice("ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) started." % (code, start, end, ktype, autype))
		df = ts.get_k_data(code, start, end, ktype, autype)
	except:
		Log.warning("ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) failed." % (code, start, end, ktype, autype))
		return False
	if df.empty:
		return False
	f_name = os.path.join(folder_path, code+".csv")
	df.to_csv(f_name)
	return True

def batch_download_k_data(folder_path, code_list, start, end, ktype, autype):
	for code in code_list:
		download_k_data(folder_path, code, start, end, ktype, autype)
	return True

def download_all_index_k_data(folder_path, start, end, ktype, autype):
	if not os.path.isdir(folder_path):
		os.mkdir(folder_path)
#	try:
#		index_df = ts.get_index()
#	except:
#		Log.warning("ts.get_index() failed.")
#		return False
	code_list = ['sh', 'sz', 'cyb', 'zxb', 'hs300', 'sz50']
	batch_download_k_data(folder_path, code_list, start, end, ktype, autype)
	return True

def download_all_stock_k_data(folder_path, start, end, ktype, autype):
	if not os.path.isdir(folder_path):
		os.mkdir(folder_path)
	try:
		stock_df = ts.get_stock_basics()
	except:
		Log.warning("ts.get_stock_basics() failed.")
		return False
	code_list = stock_df.index
	batch_download_k_data(folder_path, code_list, start, end, ktype, autype)
	return True

if __name__ == '__main__':

	download_all_stock_k_data(STOCK_DATA_PATH, start=Time.day(-180), end=Time.today(), ktype='D', autype='qfq')

