#!/usr/bin/python
#coding: utf-8

import os
import sys
import smtplib
from email.mime.text import MIMEText
sys.path.append("../..")
from conf.config import *

class Email:

	@staticmethod
	def send(fr, to, subject, content):
		msg = MIMEText(content,_subtype='html',_charset='utf-8')
		msg['From'] = fr
		msg['To'] = ";".join(to)  
		msg['Subject'] = subject
		try: 
			server = smtplib.SMTP()
			server.connect(MAIL_HOST)
			server.login(MAIL_USER, MAIL_PSWD)
			server.sendmail(fr, to, msg.as_string())
			server.close()  
			return True
		except Exception, e:
			print str(e)
			return False

