import os
import sys
import getopt
from config import *
import train
import predict


def usage():
	print("	spider: python %s spider [--history --new]" % sys.argv[0])
	print("	train: python %s train [--tiny --sample]" % sys.argv[0])
	print("	predict: python %s predict [--tiny --date]" % sys.argv[0])
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
	elif cmd == "spider":
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
