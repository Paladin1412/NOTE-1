#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
import os
import linecache
import re
import functools

#打开数据库连接
db = pymysql.connect("localhost","root","Yxd@123","sdkdatabase")
#创建游标对象
cursor = db.cursor()


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

def InterfaceCheck(line_count, data_file_path, save_file_path):
	#line_1st包含文件位置
	line_1st = linecache.getline(data_file_path, line_count)
	#line_2nd包含接口名称与父类接口名称
	line_2nd = linecache.getline(data_file_path, line_count + 1)
	#line_3rd包含版本限制信息
	line_3rd = linecache.getline(data_file_path, line_count + 3)
	#line_4th包含所属方法
	line_4th = linecache.getline(data_file_path, line_count + 2)
	if(line_1st.find(" <") >= 0):
		property_postion = line_1st[line_1st.find(":") + 1 : line_1st.find(" <")]
		line_1st = line_1st[ : line_1st.find(":")]
		property_postion = "位置:" + property_postion[ : property_postion.find(":")] + "行" + property_postion[property_postion.find(":")+1 : ] + "列"
	else:
		property_postion = line_2nd[line_2nd.find("位置") : line_2nd.rfind(";")]

	print(line_1st)

	property_name = line_2nd[line_2nd.find("属性名:") + 4 : line_2nd.find("类型:")].strip()
	property_type = line_2nd[line_2nd.find("类型:") + 3 : line_2nd.find("所属接口名称:")].strip()
	interface_name = line_2nd[line_2nd.find("所属接口名称:") + 7 : line_2nd.find("父类接口名称:")].strip()
	super_interface_name = line_2nd[line_2nd.find("父类接口名称:") + 7 : line_2nd.find("位置:")].strip()
	if line_3rd.find("对应版本为：") >= 0:
		version_id = line_3rd[line_3rd.find("对应版本为：") + 6 : ].strip()
	else:
		version_id = "9.0"
	property_name = property_name[ : len(property_name) - 1]
	property_type = property_type[ : len(property_type) - 1]
	interface_name = interface_name[ : len(interface_name) - 1]
	super_interface_name = super_interface_name[ : len(super_interface_name) - 1]
	if property_type.find("_Nonnull") >= 0:
		property_type = property_type[ : property_type.find("_Nonnull")]
	if property_type.find("_Null") >= 0:
		property_type = property_type[ : property_type.find("_Null")]
	property_type = "".join(property_type.split())
	#print(property_name)
	#print(property_type)
	#print(interface_name)
	#print(super_interface_name)
	#print(version_id)
	#sql查询语句
	#先查询获取到的接口是否在数据表中
	sql_1st = "SELECT * FROM property_data_table WHERE property_name = '%s' " % (property_name)
	try:
		cursor.execute(sql_1st)
		results = cursor.fetchall()
		if(len(results) == 0):
			#print("could not find target")
			save_file_path.write(line_1st)
			save_file_path.write(line_2nd[line_2nd.find("属性名:") : line_2nd.find("位置:") ] + "\t" + property_postion + "\n")
			save_file_path.write("⚠️：未在系统属性信息表中找到该属性的相关信息，其可能为开发人员自定义的属性类型或其他\n\n")
		else:
			sql_2nd = "SELECT * FROM property_data_table WHERE property_name = '%s' AND interface_name = '%s' ORDER BY version_id " % (property_name, interface_name)
			try:
				cursor.execute(sql_2nd)
				results = cursor.fetchall()
				save_file_path.write(line_1st)
				save_file_path.write(line_2nd[line_2nd.find("属性名:") : line_2nd.find("位置:") ] + "\t" + property_postion + "\n")
				if(len(results) == 0):
					save_file_path.write("该属性可能继承自当前接口的父类接口，需对其进行进一步检测\n")
					sql_3rd = "SELECT * FROM property_data_table WHERE property_name = '%s' AND interface_name = '%s' ORDER BY version_id " % (property_name, super_interface_name)
					try:
						cursor.execute(sql_3rd)
						results = cursor.fetchall()
						if(len(results) == 0):
							save_file_path.write("⚠️：在对当前接口和其对应的父类接口进行检测之后，均未发现该属性的相关信息，其可能继承自更上层的接口或为开发人员自定义的属性类型，请自行检查程序中的相关信息\n")
							sql_4th = "SELECT * FROM property_data_table WHERE property_name = '%s' AND property_type = '%s' ORDER BY interface_name, version_id " % (property_name, property_type)
							try:
								cursor.execute(sql_4th)
								results = cursor.fetchall()
								save_file_path.write("参考信息：提供该种类型(" + property_type +")属性的接口有：\n")
								for row in results:
									save_file_path.write(row[1] + "————" + row[2] + "————" + row[3] + "————" + row[4] + "\n")
								save_file_path.write("\n")
							except:
								print("find error 4")
						else:
							version_ids = []
							property_types = []
							for row in results:
								version_ids.append(row[4])
								property_types.append(row[2])
							version_ids = sorted(version_ids, key=functools.cmp_to_key(version_cmp))
							save_file_path.write("在对当前接口的父类接口进行检测之后，获知该属性继承自父类接口\n")
							save_file_path.write("支持该接口的iOS版本以及对应的类型为：" + version_ids[0] + "(" + property_types[0] + ")")
							count = 1
							while(count < len(version_ids)):
								save_file_path.write("，" + version_ids[count] + "(" + property_types[count] + ")")
								count = count + 1
							save_file_path.write("\n程序中对使用该属性的版本限制为：" + version_id + "\n")
							#if float(version_id) >= float(version_ids[0]):
							if version_ids.count(version_id) >= 0 or version_ids.count(version_id + ".0") >= 0:
								save_file_path.write("✅：该属性的使用符合版本限制要求\n\n")
							else:
								save_file_path.write("❌：该属性的使用不符合版本限制要求\n\n")
					except:
						print("find error 3")
				else:
					version_ids = []
					property_types = []
					for row in results:
						version_ids.append(row[4])
						property_types.append(row[2])
					version_ids = sorted(version_ids, key=functools.cmp_to_key(version_cmp))
					save_file_path.write("支持该接口的iOS版本以及对应的类型为：" + version_ids[0] + "(" + property_types[0] + ")")
					count = 1
					while(count < len(version_ids)):
						save_file_path.write("，" + version_ids[count] + "(" + property_types[count] + ")")
						count = count + 1
					save_file_path.write("\n程序中对使用该属性的版本限制为：" + version_id + "\n")
					#if float(version_id) >= float(version_ids[0]):
					if version_ids.count(version_id) > 0 or version_ids.count(version_id + ".0") > 0:
						save_file_path.write("✅：该属性的使用符合版本限制要求\n\n")
					else:
						save_file_path.write("❌：该属性的使用不符合版本限制要求\n\n")
			except:
				print("find error 2")
	except:
		print("find error 1")

def InformationGet(data_file_path, save_file_path):
	data_file = open(data_file_path,'r')
	line = data_file.readline()
	line_count = 1
	while line:
		if(line.find("所在文件") >= 0):
			#忽略信息不全的匹配结果
			if not(linecache.getline(data_file_path, line_count + 1).find("NULL") >= 0):
				InterfaceCheck(line_count, data_file_path, save_file_path)
		line = data_file.readline()
		line_count = line_count + 1


if __name__ == '__main__':
    data_file_path = "/Users/yuxingdong/TraversingOutput/wework_buildout/build_output_property.txt"
    save_file_name = "/Users/yuxingdong/TraversingOutput/APICheck/property_check.txt"
    save_file_path = open(save_file_name,'w')
    print("property check")
    InformationGet(data_file_path, save_file_path)
    save_file_path.close()

#关闭数据库连接与游标对象
db.close()
cursor.close()