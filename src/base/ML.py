#!/usr/bin/python
#coding: utf-8

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingRegressor

class ML:

	@staticmethod
	def loadModel(path):
		model = joblib.load(path)
		return model

	@staticmethod
	def saveModel(model, path):
		joblib.dump(model, path)

	@staticmethod
	def predict(model, x):
		return model.predict(x)

