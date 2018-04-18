#!/usr/bin/python

import os
import sys
import pickle
import process

sys.path.append("..")
from conf.config import *
from base.Log import Log


def predict(model_path, input_data_path, output_file_path, date=""):
	model_file = os.path.join(model_path, 'model.txt')
	model = pickle.load(open(model_file, 'rb'))

	X = process.load_and_process(input_data_path, label=False, date=date)
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	y_pred_df.to_csv(output_file_path)

if __name__ == "__main__":
	predict(XGBOOST_TINY_MODEL_PATH, NEW_STOCK_TINY_DATA_PATH, "x.csv", date="2018-03-30")

#	if len(sys.argv) < 2:
#		print("Error: Invalid args.")
#		exit(1)
#	if sys.argv[1] == "tiny":
#		predict(XGBOOST_TINY_MODEL_PATH, NEW_STOCK_TINY_DATA_PATH)
#	else:
#		print("Error: Invalid args.")
#		exit(1)
