#!/usr/bin/python
#coding: utf-8

import sys

class Data:

	@staticmethod
	def formatFloat(x, precision=2):
		f = "%." + str(precision) + "f"
		return f % x

	@staticmethod
	def formatPercentage(x, precision=2, keep=False):
		f = "%." + str(precision) + "f"
		if keep:
			return f % ( x ) + "%"
		else:
			return f % ( x * 100 ) + "%"

