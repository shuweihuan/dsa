import os
import sys
from config import *
import download
import predict
from base.Time import Time
from base.Log import Log

# 文件路径定义
model_path = os.path.join(MAIN_PATH, "model/xgboost/stock_all_sample_10p_high_10p.model")
input_path = os.path.join(MAIN_PATH, "data/new_stock")
predict_path = os.path.join(MAIN_PATH, "predict")
stock_predict_path = os.path.join(predict_path, "stock")

# 文件检查
if not os.path.isfile(model_path):
	Log.error("model path '%s' does not exist." % model_path)
	sys.exit(1)
if not os.path.isdir(input_path):
	Log.error("input path '%s' does not exist." % input_path)
	sys.exit(1)
if not os.path.isdir(predict_path):
	os.mkdir(predict_path)
	Log.notice("predict path '%s' created." % predict_path)
if not os.path.isdir(stock_predict_path):
	os.mkdir(stock_predict_path)
	Log.notice("stock predict path '%s' created." % stock_predict_path)

# 下载最近180天的股票数据
download.download_all_stock_k_data(input_path, start=Time.day(-180), end=Time.today(), ktype='D', autype='qfq')

# 使用模型预测未来5日最高价涨幅大于10%的股票
predict.predict(model_path, input_path, stock_predict_path, date=Time.today())
