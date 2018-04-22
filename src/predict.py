import os
import sys
import pandas as pd
import pickle
import process


def predict(model_path, input_data_path, output_data_path, date=""):
	# 加载模型
	model = pickle.load(open(model_path, 'rb'))
	if date == "":
		output_file = os.path.join(output_data_path, "all.txt")
	else:
		output_file = os.path.join(output_data_path, date + ".txt")
	# 加载和处理数据
	X = process.load_and_process(input_data_path, label=False, date=date)
	# 预测
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	# 预测结果输出
	y_pred_df.to_csv(output_file)


if __name__ == "__main__":
	# 在tiny数据集上测试
	predict("../model/xgboost/tiny.model", "../data/new_stock_tiny", "../predict/stock_tiny", date="2018-03-30")

