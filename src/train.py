import os
import sys
import numpy as np
import pandas as pd
import pickle
import getopt
import process
import matplotlib.pyplot as plt
from sklearn import model_selection
from xgboost import XGBClassifier


"""
训练
"""


def train(data_path, model_path, debug=False, sample=1.0):
	# 加载数据
	df = process.load_and_process(data_path, train=True, sample=sample)

	# 检查目录
	if not os.path.isdir(data_path):
		print("Error: training data '%s' does not exist." % data_path)
		sys.exit(1)

	# 模型描述文件
	desc_file_path = model_path + ".desc"
	desc_file = open(desc_file_path, 'w')

	# 训练测试集划分
	X = df.iloc[:, 1:]
	y = df.iloc[:, 0]
	X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=0)
	print("shape of X_train: %s" % str(X_train.shape))
	print("shape of y_train: %s" % str(y_train.shape))
	print("shape of X_test: %s" % str(X_test.shape))
	print("shape of y_test: %s" % str(y_test.shape))
	desc_file.write("shape of X_train: %s\n" % str(X_train.shape))
	desc_file.write("shape of y_train: %s\n" % str(y_train.shape))
	desc_file.write("shape of X_test: %s\n" % str(X_test.shape))
	desc_file.write("shape of y_test: %s\n" % str(y_test.shape))

	# 训练xgboost模型
	model = XGBClassifier(objective='binary:logistic', eval_metric='logloss')
	model.fit(X_train, y_train)
	print("model: %s" % str(model))
	desc_file.write("model: %s\n" % str(model))

	# 输出训练集效果
	y_pred = model.predict(X_train)
	eval_dict = process.eval(y_train, y_pred)
	print("evaluation on train: %s" % str(eval_dict))
	desc_file.write("evaluation on train: %s\n" % str(eval_dict))

	# 输出测试集效果
	y_pred = model.predict(X_test)
	eval_dict = process.eval(y_test, y_pred)
	print("evaluation on test: %s" % str(eval_dict))
	desc_file.write("evaluation on test: %s\n" % str(eval_dict))

	# 输出测试集调整阈值后的效果
	y_pred = model.predict_proba(X_test)[:, 1]
	eval_dict = process.eval(y_test, y_pred, 0.75)
	print("evaluation on test with threshold=0.75: %s" % str(eval_dict))
	desc_file.write("evaluation on test with threshold=0.75: %s\n" % str(eval_dict))

	# 保存模型文件
	pickle.dump(model, open(model_path, 'wb'))

	# 关闭模型描述文件
	desc_file.close()

	# debug输出
	if debug:
		debug_file_path = model_path + ".debug"
		df_test = pd.DataFrame(y_pred, index=y_test.index, columns=['pred'])
		df_test = df_test.reset_index()
		df = df.reset_index()
		df_test = pd.merge(df_test, df, on='key', how='inner')
		df_test = df_test.set_index('key')
		df_test.to_csv(debug_file_path)


def usage():
	print("Usage: python train.py input_path model_path [-d|--debug] [-s|--sample=1.0]")


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Error: invalid number of args.")
		usage()
		sys.exit(1)
	input_path = sys.argv[1]
	model_path = sys.argv[2]
	debug = False
	sample = 1.0
	if len(sys.argv) > 3:
		try:
			opts, args = getopt.getopt(sys.argv[3:], "ds:", ["debug", "sample="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		for o, a in opts:
			if o in ("-d", "--debug"):
				debug = True
			elif o in ("-s", "--sample"):
				sample = float(a)
			else:
				assert False, "Error: unknown option."
	train(input_path, model_path, debug, sample)

