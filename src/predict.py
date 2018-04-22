import os
import sys
import pandas as pd
import pickle
import process
from config import *


def predict(model_path, input_data_path, output_data_path, date=""):
	# 转换为绝对路径
	model_file = os.path.join(MAIN_PATH, model_path + ".txt")
	input_data_path = os.path.join(MAIN_PATH, input_data_path)
	output_data_path = os.path.join(MAIN_PATH, output_data_path)

	# 加载模型
	model = pickle.load(open(model_file, 'rb'))
	if date == "":
		output_file = os.path.join(output_data_path, "all.txt")
	else:
		output_file = os.path.join(output_data_path, date + ".txt")

	X = process.load_and_process(input_data_path, label=False, date=date)
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	y_pred_df.to_csv(output_file)


if __name__ == "__main__":
	# 在tiny数据集上测试
	predict("model/xgboost/tiny", "data/new_stock_tiny", "predict/stock_tiny", date="2018-03-30")

