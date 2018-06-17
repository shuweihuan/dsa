import os
import sys
import numpy as np
import pandas as pd
import pickle
import process
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn import metrics
from xgboost import XGBClassifier


"""
计算评估结果
"""


def eval(y, y_pred, threshold=0.5):
	y_pred = (y_pred >= threshold) * 1
	eval_dict = {}
	eval_dict["accuracy"] = metrics.accuracy_score(y, y_pred)
	eval_dict["auc"] = metrics.roc_auc_score(y, y_pred)
	eval_dict["precision"] = metrics.precision_score(y, y_pred)
	eval_dict["recall"] = metrics.recall_score(y, y_pred)
	eval_dict["f1-score"] = metrics.f1_score(y, y_pred)
	eval_dict["confusion_matrix"] = metrics.confusion_matrix(y, y_pred)
	return eval_dict


"""
训练
"""


def train(data_path, model_path, sample=1.0):
	# 加载数据
	df = process.load_and_process(data_path, label=True, sample=sample)

	# 检查目录
	if not os.path.isdir(data_path):
		print("Error: training data '%s' does not exist." % data_path)
		sys.exit(1)

	# 训练测试集划分
	X = df.iloc[:, 1:]
	y = df.iloc[:, 0]
	X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=0)
	print("shape of X_train: %s" % str(X_train.shape))
	print("shape of y_train: %s" % str(y_train.shape))
	print("shape of X_test: %s" % str(X_test.shape))
	print("shape of y_test: %s" % str(y_test.shape))

	# 训练xgboost模型
	model = XGBClassifier(objective='binary:logistic', eval_metric='logloss')
	model.fit(X_train, y_train)
	print("model: %s" % str(model))

	# 输出训练集效果
	y_pred = model.predict(X_train)
	eval_dict = eval(y_train, y_pred)
	print("evaluation on train: %s" % str(eval_dict))

	# 输出测试集效果
	y_pred = model.predict(X_test)
	eval_dict = eval(y_test, y_pred)
	print("evaluation on test: %s" % str(eval_dict))

	# 输出测试集调整阈值后的效果
	y_pred = model.predict_proba(X_test)[:, 1]
	eval_dict = eval(y_test, y_pred, 0.75)
	print("evaluation on test with threshold=0.75: %s" % str(eval_dict))

	# 保存模型文件
	pickle.dump(model, open(model_path, 'wb'))

	# 测试结果输出
#    df_test = pd.DataFrame(y_pred, index=y_test.index, columns=['pred'])
#    df_test = df_test.reset_index()
#    df = df.reset_index()
#    df_test = pd.merge(df_test, df, on='key', how='inner')
#    df_test = df_test.set_index('key')
#    df_test.to_csv("test.csv")

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Error: invalid number of args.")
		print("Usage: %s input_path model_path [sample=1.0]" % sys.argv[0])
		sys.exit(1)
	input_path = sys.argv[1]
	model_path = sys.argv[2]
	sample = 1.0
	if len(sys.argv) > 3:
		sample = sys.argv[3]
	train(input_path, model_path, sample)

