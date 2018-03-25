#!/usr/bin/python
#coding: utf-8

import sys
from Stock import Stock
sys.path.append("../..")
from conf.config import *

class XML:

	@staticmethod
	def genHtmlHead(title=""):
		html = ""
		html += "<html>\n"
		html += "<head>\n"
		html += ( "<title>" + title + "</title>" )
		f = open(DEFAULT_CSS_PATH, 'r')
		for line in f:
			html += line
		f.close()
		html += "</head>\n"
		html += "<body>\n"
		return html

	@staticmethod
	def genHtmlTail():
		return "</body>\n</html>\n"

	@staticmethod
	def dataFrame2Table(df, index_name="", code_link=False):
		html = ""
		html += '<table id="main_table">\n'
		html += "<thead>\n"
		html += "<tr>"
		html += ( "<th>" + index_name + "</th>" )
		for col in df.keys():
			html += ( "<th>" + col + "</th>" )
		html += "</tr>\n"
		html += "</thead>\n"
		html += "<tbody>\n"
		i = 0
		for row in df.itertuples():
			if i % 2 == 0:
				html += "<tr>"
			else:
				html += '<tr class="alt">'
			j = 0
			for col in row:
				if code_link and j==0:
					html += ( "<td><a href=" + Stock.getUrl(col) + ">" + str(col) + "</a></td>" )
				else:
					html += ( "<td>" + str(col) + "</td>" )
				j += 1
			html += "</tr>\n"
			i += 1
		html += "</tbody>\n"
		html += "</table>\n"
		return html

