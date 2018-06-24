import os
import sys
import pandas as pd
import pickle
import getopt
import process


def predict(model_path, input_path, output_path, test=False, date=""):
	# 加载模型
	model = pickle.load(open(model_path, 'rb'))
	# 加载和处理数据
	df = process.load_and_process(input_path, train=False, date=date)
	X = df.iloc[:, 1:]
	y = df.iloc[:, 0]
	# 预测
	y_pred = model.predict_proba(X)[:, 1]
	if test==True:
		eval_dict = process.eval(y, y_pred, 0.75)
		print("evaluation on test with threshold=0.75: %s" % str(eval_dict))
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	# 预测结果输出
	y_pred_df.to_csv(output_path)


def usage():
	print("Usage: python predict.py model_path input_path output_path [-t|--test] [-d|--date='']")


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Error: invalid number of args.")
		usage()
		sys.exit(1)
	model_path = sys.argv[1]
	input_path = sys.argv[2]
	output_path = sys.argv[3]
	test = False
	date = ""
	if len(sys.argv) > 4:
		try:
			opts, args = getopt.getopt(sys.argv[4:], "td:", ["test", "date="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		for o, a in opts:
			if o in ("-t", "--test"):
				test = True
			elif o in ("-d", "--date"):
				date = a
			else:
				assert False, "Error: unknown option."
	predict(model_path, input_path, output_path, test, date)


