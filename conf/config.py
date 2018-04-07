#!/usr/bin/python
#coding: utf-8

import os
import pandas as pd

# path setting

MAIN_PATH = ".."

SRC_PATH = os.path.join(MAIN_PATH, "src")
CONF_PATH = os.path.join(MAIN_PATH, "conf")
DATA_PATH = os.path.join(MAIN_PATH, "data")
MODEL_PATH = os.path.join(MAIN_PATH, "model")

HISTORY_INDEX_DATA_PATH = os.path.join(DATA_PATH, "history_index")
HISTORY_STOCK_DATA_PATH = os.path.join(DATA_PATH, "history_stock")
HISTORY_STOCK_SAMPLE_PATH = os.path.join(DATA_PATH, "history_stock_sample")
NEW_INDEX_DATA_PATH = os.path.join(DATA_PATH, "new_index")
NEW_STOCK_DATA_PATH = os.path.join(DATA_PATH, "new_stock")
NEW_STOCK_SAMPLE_PATH = os.path.join(DATA_PATH, "new_stock_sample")
XGBOOST_MODEL_FILE = os.path.join(MODEL_PATH, "xgboost.model")

