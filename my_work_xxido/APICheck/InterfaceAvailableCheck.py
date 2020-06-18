#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import linecache
import re
import xlwt
import functools

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
            if(int(x_lists[count]) < int(y_lists[count])):  #x的版本号小于y，返回-1
                return -1
            else:
                return 1
    if x_len < y_len:
        return -1
    else: 
        return 1

excelTabel= xlwt.Workbook()#创建excel对象
sheet1=excelTabel.add_sheet('interface_error',cell_overwrite_ok=True)
sheet1.write(0,0,'接口名')
sheet1.write(0,1,'父类接口名')
sheet1.write(0,2,'文件名')
sheet1.write(0,3,'位置')
sheet1.write(0,4,'错误类型')
sheet1.write(0,5,'最低版本限制')
interface_data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/interface_check.txt"
interface_data_file = open(interface_data_file_path,'r')
line = interface_data_file.readline()
sheet1_line = 1
line_count = 1
while line:
    if(line.find("❌：该接口的使用不符合版本限制要求") >= 0):
        data_line_1st = linecache.getline(interface_data_file_path, line_count - 3)
        data_line_2nd = linecache.getline(interface_data_file_path, line_count - 2)
        data_line_3rd = linecache.getline(interface_data_file_path, line_count + 2)
        versions = data_line_3rd.split("\t")
        count = 0
        version = []
        while(count < len(versions)):
            if(versions[count].find("--") >= 0):
                version.append(versions[count][ : versions[count].find("--")])
            count = count + 1
        version = sorted(version, key=functools.cmp_to_key(version_cmp))
        print(version)
        sheet1.write(sheet1_line, 0, data_line_2nd[data_line_2nd.find("接口名称:") + 5: data_line_2nd.find(";     父类接口名称:")])
        temp_str = data_line_2nd[data_line_2nd.find("父类接口名称:") + 7 : data_line_2nd.find("位置:")].strip()
        sheet1.write(sheet1_line, 1, temp_str[ : len(temp_str) - 1])
        sheet1.write(sheet1_line, 2, data_line_1st[data_line_1st.rfind("/") + 1 :])
        sheet1.write(sheet1_line, 3, data_line_2nd[data_line_2nd.find("位置:") + 3: data_line_2nd.find("行") + 1])
        sheet1.write(sheet1_line, 4, "该接口的使用不符合版本限制要求")
        sheet1.write(sheet1_line, 5, version[0])
        sheet1_line = sheet1_line + 1
    line = interface_data_file.readline()
    line_count = line_count + 1

excelTabel.save('/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/InterfaceAPICheck.xls')

