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

def version_cmp(a, b):
	if(a[0] > b[0]):
		return 1
	else:
		return -1

def FindProperty(property_name, interface_name, version_low_limit, version_up_limit, version_id, version_range, super_interface_names):
	if(interface_name == "NSObject"):
		print("back to root")
	else:
		mysql_1 = "SELECT super_interface_name, version_id FROM interface_data_table where interface_name = '%s' ORDER BY super_interface_name, CONVERT(version_id,DECIMAL(12,1))" % interface_name
		try:
			cursor.execute(mysql_1)
			results = cursor.fetchall()
			if(len(results) > 0):
				super_interface_dic = []
				temp_name = results[0][0]
				temp_version = results[0][1]
				super_interface_dic.append([results[0][0],results[0][1]])
				count = 0
				for row in results:
					if(row[0] != temp_name):
						super_interface_dic[count].append(temp_version)
						super_interface_dic.append([row[0],row[1]])
						temp_name = row[0]
						count = count + 1
					temp_version = row[1]
				super_interface_dic[count].append(temp_version)
				#print(super_interface_dic)
				for dic_member in super_interface_dic:
					print(dic_member)
					if(float(dic_member[1]) <= float(version_up_limit) and float(version_low_limit) <= float(dic_member[2])):
						temp_inherit_range = [max(float(dic_member[1]),float(version_low_limit)),min(float(dic_member[2]),float(version_up_limit))]
						if(float(version_id) <= float(temp_inherit_range[1])):
							print(temp_inherit_range)
							check_again_sql = "SELECT * FROM property_data_table WHERE property_name = '%s' AND interface_name = '%s' ORDER BY CONVERT(version_id,DECIMAL(12,1))" % (property_name, dic_member[0])
							try:
								cursor.execute(check_again_sql)
								results = cursor.fetchall()
								if(len(results) > 0):
									print("find it in super super interface")
									if(float(results[0][4]) <= float(temp_inherit_range[1]) and float(temp_inherit_range[0]) <= float(results[len(results)-1][4])):
										temp_version_range = [max(float(results[0][4]),float(temp_inherit_range[0])),min(float(results[len(results)-1][4]), float(temp_inherit_range[1]))]
										version_range.append(temp_version_range)
										super_interface_names.append(dic_member[0])
								else:
									FindProperty(property_name, dic_member[0], temp_inherit_range[0], temp_inherit_range[1], version_id, version_range)
							except:
								print("find property error 2")
		except:
			print("find property error 1")

def PropertyCheck(line, data_file_path, save_file_path):
	information = line.split("\t")
	file_name = information[0]
	property_name = information[1]
	interface_name = information[2]
	super_interface_name = information[3]
	property_type = information[4]
	property_pos = information[5]
	version_id = information[6][ : information[6].rfind("\n")]
	print("---" + interface_name + "---" + property_name)
	#初步选择，判断当前属性是否属于当前接口：
	sql_1 = "SELECT * FROM property_data_table WHERE property_name = '%s' AND interface_name = '%s' ORDER BY CONVERT(version_id,DECIMAL(12,1))" % (property_name, interface_name)
	try:
		cursor.execute(sql_1)
		results = cursor.fetchall()
		if(len(results) > 0):
			save_file_path.write("文件名：" + file_name + "\t属性名：" + property_name + "\t位置：" + property_pos + "\t接口名：" + interface_name + "\t父类接口：" + super_interface_name + "\n版本限制：" + results[0][4])
			for row in results:
				save_file_path.write("\t" + row[4])
			save_file_path.write("\n程序中对使用该属性的版本限制为：" + version_id + "\n")
			if float(version_id) >= float(results[0][4]):
				save_file_path.write("✅：该属性的使用符合版本限制要求\n\n")
			else:
				save_file_path.write("❌：该属性的使用不符合版本限制要求\n\n")
		else:
			sql_2 = "SELECT super_interface_name, version_id FROM interface_data_table where interface_name = '%s' ORDER BY super_interface_name, CONVERT(version_id,DECIMAL(12,1))" % interface_name
			version_range = []
			super_interface_names = []
			try:
				cursor.execute(sql_2)
				results = cursor.fetchall()
				#对父类遍历
				if(len(results) > 0):
					super_interface_dic = []
					temp_name = results[0][0]
					temp_version = results[0][1]
					super_interface_dic.append([results[0][0],results[0][1]])
					count = 0
					for row in results:
						if(row[0] != temp_name):
							super_interface_dic[count].append(temp_version)
							super_interface_dic.append([row[0],row[1]])
							temp_name = row[0]
							count = count + 1
						temp_version = row[1]
					super_interface_dic[count].append(temp_version)
					for dic_member in super_interface_dic:
						if(float(version_id) <= float(dic_member[2])):
							print("father:" + dic_member[0])
							sql_3 = "SELECT * FROM property_data_table WHERE property_name = '%s' AND interface_name = '%s' ORDER BY CONVERT(version_id,DECIMAL(12,1))" % (property_name, dic_member[0])
							try:
								cursor.execute(sql_3)
								results = cursor.fetchall()
								if(len(results) > 0):
									print("find it in super interface")
									if(float(results[0][4]) <= float(dic_member[2]) and float(dic_member[1]) <= float(results[len(results)-1][4])):
										temp_version_range = [max(float(results[0][4]),float(dic_member[1])),min(float(results[len(results)-1][4]), float(dic_member[2]))]
										version_range.append(temp_version_range)
										super_interface_names.append(dic_member[0])
									print(temp_version_range)
								else:
									print("find father again")
									FindProperty(property_name, dic_member[0], dic_member[1], dic_member[2], version_id, version_range, super_interface_names)
							except:
								print("find error 3")
			except:
				print("find error 2")
			print(version_range)
			if(len(version_range) > 0):
				version_range = sorted(version_range, key=functools.cmp_to_key(version_cmp))
				save_file_path.write("文件名：" + file_name + "\t属性名：" + property_name + "\t位置：" + property_pos + "\t接口名：" + interface_name + "\t父类接口：" + super_interface_name + "\n属性继承自父类" + super_interface_names[0] + "，版本限制：[" + str(version_range[0][0]) + "," + str(version_range[0][1]) + "]")
				count = 1
				while(count < len(version_range)):
					save_file_path.write(",[" + str(version_range[count][0]) + "," + str(version_range[count][1]) + "]")
					count = count + 1
				save_file_path.write("\n程序中对使用该属性的版本限制为：" + version_id + "\n")
				if float(version_id) >= float(version_range[0][0]):
					save_file_path.write("✅：该属性的使用符合版本限制要求\n\n")
				else:
					save_file_path.write("❌：该属性的使用不符合版本限制要求\n\n")
			else:
				print("this property couldn't be find")
	except:
		print("find error 1")


def InformationGet(data_file_path, save_file_path):
	data_file = open(data_file_path,'r')
	line = data_file.readline()
	line_count = 1
	while line:
		if(line_count % 2 == 1):
			PropertyCheck(line, data_file_path, save_file_path)
		line = data_file.readline()
		line_count = line_count + 1

if __name__ == '__main__':
	data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_property.txt"
	save_file_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/property_check.txt"
	save_file_path = open(save_file_name,'w')
	print("property check")
	InformationGet(data_file_path, save_file_path)
	save_file_path.close()

#关闭数据库连接与游标对象
db.close()
cursor.close()
