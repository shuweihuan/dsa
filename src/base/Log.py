#!/usr/bin/python
#coding: utf-8

import sys
import time

class Log:

	@staticmethod
	def notice(msg):
		f = Log._trace()
		s = "notice: "
		s += Log._datetime()
		s += ", file "
		s += f.f_code.co_filename
		s += ", func "
		s += f.f_code.co_name
		s += "(), "
		s += msg
		sys.stdout.write(s + "\n")

	@staticmethod
	def warning(msg):
		f = Log._trace()
		s = "warning: "
		s += Log._datetime()
		s += ", file "
		s += f.f_code.co_filename
		s += ", func "
		s += f.f_code.co_name
		s += "(), line " 
		s += str(f.f_lineno)
		s += ", "
		s += msg
		sys.stderr.write(s + "\n")

	@staticmethod
	def error(msg):
		f = Log._trace()
		s = "error: "
		s += Log._datetime()
		s += ", file "
		s += f.f_code.co_filename
		s += ", func "
		s += f.f_code.co_name
		s += "(), line " 
		s += str(f.f_lineno)
		s += ", "
		s += msg
		sys.stderr.write(s + "\n")

	@staticmethod
	def _date():
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))
	
	@staticmethod
	def _time():
		return time.strftime('H:%M:%S',time.localtime(time.time()))

	@staticmethod
	def _datetime():
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	@staticmethod
	def _trace():
		try:
			raise Exception
		except:
			return sys.exc_info()[2].tb_frame.f_back.f_back

if __name__ == "__main__":
		
	Log.notice("test notice.")
	Log.warning("test warning.")
	Log.error("test error.")

