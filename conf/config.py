import os

MAIN_PATH = ".."

SRC_PATH = os.path.join(MAIN_PATH, "src")
DATA_PATH = os.path.join(MAIN_PATH, "data")
MODEL_PATH = os.path.join(MAIN_PATH, "model")

HISTORY_INDEX_DATA_PATH = os.path.join(DATA_PATH, "history_index")
HISTORY_STOCK_DATA_PATH = os.path.join(DATA_PATH, "history_stock")
HISTORY_STOCK_TINY_DATA_PATH = os.path.join(DATA_PATH, "history_stock_tiny")
NEW_INDEX_DATA_PATH = os.path.join(DATA_PATH, "new_index")
NEW_STOCK_DATA_PATH = os.path.join(DATA_PATH, "new_stock")
NEW_STOCK_TINY_DATA_PATH = os.path.join(DATA_PATH, "new_stock_tiny")
PREDICT_STOCK_DATA_PATH = os.path.join(DATA_PATH, "predict_stock")
PREDICT_STOCK_TINY_DATA_PATH = os.path.join(DATA_PATH, "predict_stock_tiny")
XGBOOST_MODEL_PATH = os.path.join(MODEL_PATH, "xgboost_model")
XGBOOST_TINY_MODEL_PATH = os.path.join(MODEL_PATH, "xgboost_model_tiny")

