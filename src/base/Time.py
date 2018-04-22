import os
import time
import datetime

class Time:

	@staticmethod
	def today():
		return time.strftime('%Y-%m-%d')

	@ staticmethod
	def day(n):
		day = datetime.date.today()
		if n >= 0:
			day += datetime.timedelta(days=n)
		else:
			day -= datetime.timedelta(days=abs(n))
		return day.strftime('%Y-%m-%d')

	@staticmethod
	def time():
		return time.strftime('%H:%M:%S')

	@staticmethod
	def oneYearAgo():
		today = time.strftime('%Y-%m-%d')
		today_ = today.split('-')
		year = int(today_[0])
		year -= 1
		year = str(year)
		today_[0] = year
		return '-'.join(today_)

	@staticmethod
	def hasMarketOpened():
		return Time.time() < "09:00:00"

	@staticmethod
	def hasMarketClosed():
		return Time.time() > "15:00:00"

	@staticmethod
	def getPrevYear(year):
		return year-1

	@staticmethod
	def getPrevQuarter(year, quarter):
		if quarter == 1:
			return year-1, 4
		else:
			return year, quarter-1

	@staticmethod
	def getThisQuarter(today=""):
		if today == "":
			today = Time.today()
		ymd = today.split('-')
		year = int(ymd[0])
		month = int(ymd[1])
		return year, (month+2)/3

	@staticmethod
	def getLastQuarter(today=""):
		y, q = Time.getThisQuarter(today)
		return Time.getPrevQuarter(y, q)

	@staticmethod
	def getFirstDayOfQuarter(year, quarter):
		month = quarter * 3 - 2
		if month < 10:
			return str(year) + '-0' + str(month) + '-01'
		else:
			return str(year) + '-' + str(month) + '-01'

	@staticmethod
	def getLastDayOfQuarter(year, quarter):
		month = quarter * 3
		if quarter == 1 or quarter == 4:
			day = 31
		else:
			day = 30
		if month < 10:
			return str(year) + '-0' + str(month) + '-' + str(day)
		else:
			return str(year) + '-' + str(month) + '-' + str(day)

