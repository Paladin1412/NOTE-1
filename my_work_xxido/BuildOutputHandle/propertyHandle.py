#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
import os
import linecache
import re
import functools

#打开数据库连接
db = pymysql.connect("localhost","root","ljh@123456","sdkdatabase",unix_socket="/tmp/mysql.sock")
#创建游标对象
cursor = db.cursor()

property_save_name = "/Users/linjunhao/Desktop/conplie_opt/TraversingOutput/wework_buildout/build_output_property.txt"
property_save_file_path = open(property_save_name, 'w')

def version_cmp(x, y):
	x_lists = x.split('.')
	y_lists = y.split('.')
	x_len = len(x_lists)
	y_len = len(y_lists)
	cmp_len = min(x_len,y_len)
	count = 0
	while count < cmp_len:
		if(x_lists[count] == y_lists[count]):
			count = count + 1
		else:
			if(int(x_lists[count]) < int(y_lists[count])):
				return -1
			else:
				return 1
	if x_len < y_len:
		return -1
	else: 
		return 1

#初步处理数据，去除自定义接口
def DataInsertIntoTxt(file_path, line_count, interface_names, property_names):
	#1st包含文件位置
	line_1st = linecache.getline(file_path, line_count)
	#2nd包含属性的相关信息
	line_2nd = linecache.getline(file_path, line_count + 1)
	#3rd包含版本限制信息
	line_3rd = linecache.getline(file_path, line_count + 3)
	#获取版本信息，如果未明确指明版本要求则默认为9.0
	if line_3rd.find("对应版本为：") >= 0:
		version_id = line_3rd[line_3rd.find("对应版本为：") + 6: ].strip()
	elif line_3rd.find("对应版本为:") >= 0:
		version_id = line_3rd[line_3rd.find("对应版本为:") + 6: ].strip()
	elif line_3rd.find("对应版本高于") >= 0:
		version_id = line_3rd[line_3rd.rfind("包含）") + 3 : ].strip()
	else:
		version_id = "10.0"
	if (version_id.rfind(".") == (len(version_id)-1)):
		version_id = version_id[ : len(version_id) - 1]
	if (version_cmp(version_id,"10") == -1):
		version_id = "10.0"
	#去除不完全的匹配结果
	if(line_2nd.find("_nothing_") < 0):
		interface_name = line_2nd[line_2nd.find("所属接口名称:") + 7 : line_2nd.find(";     父类接口名称:")].lower()
		#去除用户自己定义的接口类型
		if not(interface_name.find("ww") == 0 or interface_name.find("y") == 0):
			file_name = line_1st[line_1st.rfind("/") + 1 : ].strip()
			property_name = line_2nd[line_2nd.find("属性名:") + 4 : line_2nd.find(";     类型:")].strip()
			interface_name = line_2nd[line_2nd.find("所属接口名称:") + 7 : line_2nd.find(";     父类接口名称:")].strip()
			super_interface_name = line_2nd[line_2nd.find("父类接口名称:") + 7 : line_2nd.find(";     位置:")].strip()
			property_pos = line_2nd[line_2nd.find("位置:") + 3 : line_2nd.find("行")].strip() + "行"
			property_type = line_2nd[line_2nd.find("类型:") + 3 : line_2nd.find(";     所属接口名称:")].strip()
			print(property_name)
			if property_type.find("_Nonnull") >= 0:
				property_type = property_type[ : property_type.find("_Nonnull")]
			if property_type.find("_Null") >= 0:
				property_type = property_type[ : property_type.find("_Null")]
			property_type = "".join(property_type.split())
			if(interface_names.count((interface_name,)) > 0):
				if(property_names.count((property_name,)) > 0):
					property_save_file_path.write(file_name + "\t" + property_name + "\t" + interface_name + "\t" + super_interface_name + "\t" + property_type + "\t" +property_pos + "\t" + version_id)
					property_save_file_path.write("\n\n")

#读取文件
def GetTarget(file_path, interface_names, property_names):
    file = open(file_path,'r')
    line_count = 1
    line = file.readline()
    while line:
        if(line.find("所在文件：") >= 0):
            DataInsertIntoTxt(file_path, line_count, interface_names, property_names)
        line = file.readline()
        line_count = line_count + 1

if __name__ == '__main__':
	sql_find_interface = "SELECT interface_name FROM interface_data_table GROUP BY interface_name"
	try:
		cursor.execute(sql_find_interface)
		names = cursor.fetchall()
		interface_names = list(names)
	except:
		print("find interface_name error")
	sql_find_property = "SELECT property_name FROM property_data_table GROUP BY property_name"
	try:
		cursor.execute(sql_find_property)
		names = cursor.fetchall()
		property_names = list(names)
	except:
		print("find property_name error")
	data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_property_all.txt"
	GetTarget(data_file_path, interface_names, property_names)



property_save_file_path.close()
