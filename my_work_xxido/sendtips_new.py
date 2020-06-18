# -*- coding:utf-8 -*-
import subprocess
import setting
import getpass
import logging
import logging.config
import json
import urllib
import urllib2
import traceback
import json
import setting
import os
import sys
#from util import *
from urllib2 import Request, urlopen  # Python 2
#Logger=BackLogger("sendtips.py")
logging.config.dictConfig(setting.LOG_SETTINGS)
Logger = logging.getLogger()
CURPATH=os.getcwd()
sendrtx='%s/Notify.sh'%CURPATH
ROBOT_URL='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ef08cf10-0b10-46c8-a7d8-99262912730f'
COMPILE_LIST='linjunhao'
def SendRTXRobot(msg_title,msg,rtxname=COMPILE_LIST):
	try:
		Logger.error(msg)
	except:
		Logger.error(msg.decode('gbk'))
	SendRTX(rtxname,msg_title,msg)
	SendRobot(msg)
def SendRobot(content,roboturl=ROBOT_URL,requesturl='http://10.123.11.26/robot/scripts/httpdo.py'):
	content=content
	print content
	data={"text": {"content":content,"mentioned_list":["@all"]},"msgtype":"text"}
	#print urllib.urlencode(data)
	try:
		req = Request(ROBOT_URL)
		response = urlopen(req,json.dumps(data)).read()
		resjson= (json.loads(response))
		errcode=resjson['errcode']
		Logger.info('url:%s,data:%s,errcode:%s'%(ROBOT_URL,data,errcode))
	except Exception,e:
		Logger.error(traceback.format_exc())
	return resjson
def SendRTX(rtxname, msg_title, msg ):
	ip='10.123.11.26'
	msg=getpass.getuser()+'@'+ip+' '+msg
	if len(rtxname) <= 0 or len(msg_title) <= 0 or len(msg) <= 0:
		Logger.error('rtxnanme or msg_tile or msg is none:%s rtxname:%s,msg_title:%s,msg:%s'%(rtxname,msg_title.decode('gbk'),msg.decode('gbk')))
		return
	cmd = '%s rtx \'%s\' \'%s\' \'%s\'' % ( sendrtx, rtxname, msg_title, msg )
	p = subprocess.Popen( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )
	(stdout_output, stderr_output) = p.communicate()
	if p.returncode != 0:
		try:
			Logger.error("cmd %s, %d, %s"%(cmd.decode('gbk'), p.returncode, stderr_output))
		except:
			Logger.error("cmd %s, %d, %s"%(cmd, p.returncode, stderr_output))
	else:
		try:
			Logger.info("cmd %s, %d"%(cmd.decode('gbk'), p.returncode))
		except:
			Logger.info("cmd %s, %d"%(cmd.decode('gbk'), p.returncode))
if __name__=='__main__':
	#SendRTX('likunhuang','zhong¹þ¹þ','testÖÐÎÄ')
	#SendRTXRobot( '±àÒëÍê³É,send rtx exception','±àÒëÍê³É,send rtx exception')
	#SendRobot('test')
	#count=os.popen('cat /Users/melissalu/Desktop/TraversingOutput/APICheck/interface_check.txt|grep 不符合').read()
	#count1=os.popen('cat /Users/melissalu/Desktop/TraversingOutput/APICheck/property_check.txt|grep 不符合').read()
	#print count
	#if count=='' and count1=='':
	SendRobot("clang 编译失败")
