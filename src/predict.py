import os
import sys
import pandas as pd
import pickle
import process


def predict(model_path, input_path, output_path, date=""):
	# 加载模型
	model = pickle.load(open(model_path, 'rb'))
	# 加载和处理数据
	X = process.load_and_process(input_path, label=False, date=date)
	# 预测
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	# 预测结果输出
	y_pred_df.to_csv(output_path)


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Error: invalid number of args.")
		print("Usage: %s model_path input_path output_path [date='']" % sys.argv[0])
		sys.exit(1)
	model_path = sys.argv[1]
	input_path = sys.argv[2]
	output_path = sys.argv[3]
	date = ""
	if len(sys.argv) > 4:
		date = sys.argv[4]
	predict(model_path, input_path, output_path, date)

