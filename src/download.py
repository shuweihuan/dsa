import os
import sys
import time
import numpy as np
import pandas as pd
import tushare as ts
from config import *
from base.Log import Log
from base.Time import Time


def download_k_data(folder_path, code, start, end, ktype, autype):
	try:
		Log.notice("ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) started." % (
		code, start, end, ktype, autype))
		df = ts.get_k_data(code, start, end, ktype, autype)
	except:
		Log.warning(
			"ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) failed." % (code, start, end, ktype, autype))
		return False
	if df.empty:
		Log.warning("ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) - got 0 item.")
		return False
	f_name = os.path.join(folder_path, code + ".csv")
	df.to_csv(f_name)
	Log.notice("ts.get_k_data(code=%s, start=%s, end=%s, ktype=%s, autype=%s) - got %d items." % (code, start, end, ktype, autype, len(df)))
	return True


def batch_download_k_data(folder_path, code_list, start, end, ktype, autype):
	for code in code_list:
		download_k_data(folder_path, code, start, end, ktype, autype)
	return True


def download_all_index_k_data(folder_path, start, end, ktype, autype):
	if not os.path.isdir(folder_path):
		os.mkdir(folder_path)
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
	if len(sys.argv) < 4:
		print("Error: invalid number of args.")
		print("Usage: %s data_path start_day end_day [ktype='D'] [autype='qfq']" % sys.argv[0])
		sys.exit(1)
	data_path = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
	ktype = 'D'
	autype = 'qfq'
	if len(sys.argv) > 4:
		ktype = sys.argv[4]
	if len(sys.argv) > 5:
		autype = sys.argv[5]
	download_all_stock_k_data(data_path, start, end, ktype, autype)

