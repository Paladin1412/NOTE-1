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

def version_cmp(x, y):  #检查版本，如果x< y 返回 -1
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
	if not line_3rd.find("------") >= 0:
		line_3rd = linecache.getline(data_file_path,line_count + 4)
	#line_4th包含所属方法
	line_4th = linecache.getline(data_file_path, line_count + 2)
	#去除冗余信息，获得接口所在位置
	if(line_1st.find(" <") >= 0):
		interface_postion = line_1st[line_1st.find(":") + 1 : line_1st.find(" <")]
		line_1st = line_1st[ : line_1st.find(":")]
		interface_postion = "位置:" + interface_postion[ : interface_postion.find(":")] + "行"
	else:
		interface_postion = line_2nd[line_2nd.find("位置") : line_2nd.rfind("行") + 1]
	interface_name = line_2nd[line_2nd.find("接口名称:") + 5 : line_2nd.find("父类接口名称:")].strip()
	print(interface_name)
	super_interface_name = line_2nd[line_2nd.find("父类接口名称:") + 7 : line_2nd.find("位置:")].strip()
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
	interface_name = interface_name[ : len(interface_name) - 1]
	super_interface_name = super_interface_name[ : len(super_interface_name) - 1]
	#sql查询语句
	#先查询获取到的接口是否在数据表中
	sql_1st = "SELECT * FROM interface_data_table WHERE interface_name = '%s' " % (interface_name)
	try:
		cursor.execute(sql_1st)
		results = cursor.fetchall()
		if(len(results) == 0):
			save_file_path.write(line_1st)
			save_file_path.write(line_2nd[line_2nd.find("接口名称:"): line_2nd.find("位置")] + "\t" + interface_postion + "\n")
			save_file_path.write("⚠️：未在系统接口信息表中找到该接口的相关信息，其可能为开发人员自定义的接口类型或其他\n\n")
		else:
			sql_2nd = "SELECT * FROM interface_data_table WHERE interface_name = '%s' AND super_interface_name = '%s' ORDER BY version_id" % (interface_name, super_interface_name)
			try:
				cursor.execute(sql_2nd)
				results = cursor.fetchall()
				if(len(results) == 0):
					save_file_path.write(line_1st)
					save_file_path.write(line_2nd[line_2nd.find("接口名称:"): line_2nd.find("位置")] + "\t" + interface_postion + "\n")
					save_file_path.write("❌：该接口对应的父类信息出错，请自行检查程序中的相关信息\n")
					save_file_path.write("参考信息：系统接口信息表中提供的该接口的父类信息：\n")
					sql_3rd = "SELECT * FROM interface_data_table WHERE interface_name = '%s' ORDER BY version_id" % (interface_name)
					try:
						cursor.execute(sql_3rd)
						results = cursor.fetchall()
						for row in results:
							save_file_path.write(row[3] + "--" + row[2] + "\n")
						save_file_path.write("\n")
					except:
						print("find error 3\n")
				else:
					save_file_path.write(line_1st)
					save_file_path.write(line_2nd[line_2nd.find("接口名称:"): line_2nd.find("位置")] + "\t" + interface_postion + "\n")
					save_file_path.write("支持该接口的iOS版本为：")
					version_ids = []
					for row in results:
						version_ids.append(row[3])
					version_ids = sorted(version_ids, key=functools.cmp_to_key(version_cmp))
					save_file_path.write("程序中对使用该接口的版本限制为：" + version_id + "\n")
					if float(version_id) >= float(version_ids[0]):
					#if version_ids.count(version_id) > 0 or version_ids.count(version_id + ".0") > 0:
						save_file_path.write("✅：该接口的使用符合版本限制要求\n\n")
					else:
						sql_4th = "SELECT * FROM interface_data_table WHERE interface_name = '%s' ORDER BY version_id" % (interface_name) 
						try:
							cursor.execute(sql_4th)
							results = cursor.fetchall()
							version_ids = []
							for row in results:
								version_ids.append(row[3])
							version_ids = sorted(version_ids, key=functools.cmp_to_key(version_cmp))
							if float(version_id) >= float(version_ids[0]):
								save_file_path.write("❌：随版本的迭代，该接口的父类发生变更\n")
							else:
								save_file_path.write("❌：该接口的使用不符合版本限制要求\n")
							save_file_path.write("请参照以下信息检查\n")
							for row in results:
								save_file_path.write(row[3] + "--" + row[2] + "\t")
							save_file_path.write("\n\n")
						except:
							print("find error 4\n")
			except:
				print("find error 2\n")
	except:
		print("find error 1\n")



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
    data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_interface.txt"
    save_file_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/interface_check.txt"
    save_file_path = open(save_file_name,'w')
    print("interface check")
    InformationGet(data_file_path, save_file_path)
    save_file_path.close()

#关闭数据库连接与游标对象
db.close()
cursor.close()
