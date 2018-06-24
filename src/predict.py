import os
import sys
import pandas as pd
import pickle
import getopt
import process


def predict(model_path, input_path, output_path, test=False, debug=False, date=""):
	# 加载模型
	model = pickle.load(open(model_path, 'rb'))
	# 加载和处理数据
	df = process.load_and_process(input_path, train=False, date=date)
	X = df.iloc[:, 1:]
	y = df.iloc[:, 0]
	# 预测
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	if test==True:
		desc_file_path = output_path + ".desc"
		desc_file = open(desc_file_path, 'w')
		print("shape of X: %s" % str(X.shape))
		print("shape of y: %s" % str(y.shape))
		desc_file.write("shape of X: %s\n" % str(X.shape))
		desc_file.write("shape of y: %s\n" % str(y.shape))
		eval_dict = process.eval(y, y_pred, 0.75)
		print("evaluation on test with threshold=0.75: %s" % str(eval_dict))
		desc_file.write("evaluation on test with threshold=0.75: %s\n" % str(eval_dict))
	# 预测结果输出
	y_pred_df.to_csv(output_path)
	# debug输出
	if debug:
		debug_file_path = output_path + ".debug"
		df_test = pd.DataFrame(y_pred, index=y.index, columns=['pred'])
		df_test = df_test.reset_index()
		df = df.reset_index()
		df_test = pd.merge(df_test, df, on='key', how='inner')
		df_test = df_test.set_index('key')
		df_test.to_csv(debug_file_path)


def usage():
	print("Usage: python predict.py model_path input_path output_path [--test] [--debug] [--date='']")


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Error: invalid number of args.")
		usage()
		sys.exit(1)
	model_path = sys.argv[1]
	input_path = sys.argv[2]
	output_path = sys.argv[3]
	test = False
	debug = False
	date = ""
	if len(sys.argv) > 4:
		try:
			opts, args = getopt.getopt(sys.argv[4:], "", ["test", "debug", "date="])
		except getopt.GetoptError as err:
			print(err)
			usage()
			sys.exit(1)
		for o, a in opts:
			if o in ("--test"):
				test = True
			elif o in ("--debug"):
				debug = True
				test = True
			elif o in ("--date"):
				date = a
			else:
				assert False, "Error: unknown option."
	predict(model_path, input_path, output_path, test, debug, date)


