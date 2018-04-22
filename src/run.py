import os
import sys
import getopt
from config import *
import download
import train
import predict
from base.Time import Time

def usage():
	print("	download: python %s download [--index --type=new|history]" % sys.argv[0])
	print("	train: python %s train [--tiny --sample=]" % sys.argv[0])
	print("	predict: python %s predict [--tiny --date=]" % sys.argv[0])
	print("	help: python %s help" % sys.argv[0])


def main():
	# 参数个数检查
	if len(sys.argv) < 2:
		print("Error: invalid number of args.")
		usage()
		sys.exit(1)
	# 获取命令
	cmd = sys.argv[1]
	# 帮助
	if cmd == "help":
		usage()
		sys.exit()
	# 抓取
	elif cmd == "download":
		try:
			opts, args = getopt.getopt(sys.argv[2:], "it:", ["index", "type="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		data = "stock"
		type = "new"
		for o, a in opts:
			if o in ("-i", "--index"):
				data = "index"
			elif o in ("-t", "--type"):
				type = a
			else:
				assert False, "Error: unknown option."
		if data == "stock" and type == "new":
			download.download_all_stock_k_data("data/new_stock", start=Time.day(-180), end=Time.today(), ktype='D', autype='qfq')
		elif data == "stock" and type == "history":
			download.download_all_stock_k_data("data/history_stock", start="2000-01-01", end="2017-12-31", ktype='D', autype='qfq')
		elif data == "index" and type == "new":
			download.download_all_index_k_data("data/new_index", start=Time.day(-180), end=Time.today(), ktype='D', autype='qfq')
		elif data == "index" and type == "history":
			download.download_all_index_k_data("data/history_index", start="2000-01-01", end="2017-12-31", ktype='D', autype='qfq')
		else:
			assert False, "Error: unknown args."
		sys.exit()
	# 训练
	elif cmd == "train":
		try:
			opts, args = getopt.getopt(sys.argv[2:], "ts:", ["tiny", "sample="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		data = "full"
		sample = 1.0
		for o, a in opts:
			if o in ("-t", "--tiny"):
				data = "tiny"
			elif o in ("-s", "--sample"):
				sample = float(a)
			else:
				assert False, "Error: unknown option."
		if data == "tiny":
			train.train("data/history_stock_tiny", "model/xgboost/tiny", sample=sample)
		else:
			train.train("data/history_stock", "model/xgboost/full", sample=sample)
		sys.exit()
	# 预测
	elif cmd == "predict":
		try:
			opts, args = getopt.getopt(sys.argv[2:], "td:", ["tiny", "date="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		data = "full"
		date = ""
		for o, a in opts:
			if o in ("-t", "--tiny"):
				data = "tiny"
			elif o in ("-d", "--date"):
				date = a
			else:
				assert False, "Error: unknown option."
		if data == "tiny":
			predict.predict("model/xgboost/tiny", "data/new_stock_tiny", "predict/stock_tiny", date=date)
		else:
			predict.predict("model/xgboost/full", "data/new_stock", "predict/stock", date=date)
		sys.exit()
	# 其他
	else:
		print("Error: invalid command.")
		usage()
		sys.exit(1)


if __name__ == "__main__":
	# 目录初始化
	model_path = os.path.join(MAIN_PATH, "model")
	xgboost_model_path = os.path.join(model_path, "xgboost")
	predict_path = os.path.join(MAIN_PATH, "predict")
	tiny_predict_path = os.path.join(predict_path, "stock_tiny")
	full_predict_path = os.path.join(predict_path, "stock")
	if not os.path.isdir(model_path):
		os.mkdir(model_path)
	if not os.path.isdir(xgboost_model_path):
		os.mkdir(xgboost_model_path)
	if not os.path.isdir(predict_path):
		os.mkdir(predict_path)
	if not os.path.isdir(tiny_predict_path):
		os.mkdir(tiny_predict_path)
	if not os.path.isdir(full_predict_path):
		os.mkdir(full_predict_path)
	# 主函数
	main()
