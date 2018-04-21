import os
import sys
import pickle
import process


def predict(model_path, input_data_path, output_data_path, date=""):
	model_file = os.path.join(model_path, 'model.txt')
	model = pickle.load(open(model_file, 'rb'))
	if date == "":
		output_file = os.path.join(output_data_path, "all.txt")
	else:
		output_file = os.path.join(output_data_path, date + "all.txt")

	X = process.load_and_process(input_data_path, label=False, date=date)
	y_pred = model.predict_proba(X)[:, 1]
	y_pred_df = pd.DataFrame(y_pred, index=X.index, columns=['pred'])
	y_pred_df.to_csv(output_file)

