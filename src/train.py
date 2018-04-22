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
from config import *


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
	# 转换为绝对路径
	data_path = os.path.join(MAIN_PATH, data_path)
	model_path = os.path.join(MAIN_PATH, model_path)

	# 加载数据
	df = process.load_and_process(data_path, label=True, sample=sample)

	# 检查目录
	if not os.path.isdir(data_path):
		print("Error: training data '%s' does not exist." % data_path)
		sys.exit(1)
	if not os.path.isdir(model_path):
		os.mkdir(model_path)

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
	model_file = model_path + ".txt"
	pickle.dump(model, open(model_file, 'wb'))

	# 测试结果输出
#    df_test = pd.DataFrame(y_pred, index=y_test.index, columns=['pred'])
#    df_test = df_test.reset_index()
#    df = df.reset_index()
#    df_test = pd.merge(df_test, df, on='key', how='inner')
#    df_test = df_test.set_index('key')
#    df_test.to_csv("test.csv")

if __name__ == "__main__":
	# 在tiny数据集上测试
	train("data/history_stock_tiny", "model/xgboost/tiny", sample=0.1)
