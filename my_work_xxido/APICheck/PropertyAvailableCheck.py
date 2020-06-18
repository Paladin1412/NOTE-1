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
            if(int(x_lists[count]) < int(y_lists[count])):
                return -1
            else:
                return 1
    if x_len < y_len:
        return -1
    else: 
        return 1

excelTabel= xlwt.Workbook()#创建excel对象
sheet1=excelTabel.add_sheet('interface_error',cell_overwrite_ok=True)
sheet1.write(0,0,'属性名')
sheet1.write(0,1,'接口名')
sheet1.write(0,2,'属性是否继承自父类')
sheet1.write(0,3,'文件名')
sheet1.write(0,4,'位置')
sheet1.write(0,5,'错误类型')
sheet1.write(0,6,'最低版本限制')
#sheet1.write(0,7,'额外信息')
property_data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/property_check.txt"
property_data_file = open(property_data_file_path,'r')
line = property_data_file.readline()
sheet1_line = 1
line_count = 1
while line:
    if(line.find("❌：该属性的使用不符合版本限制要求") >= 0):

        data_line_1st = linecache.getline(property_data_file_path, line_count - 3)
        data_line_2nd = linecache.getline(property_data_file_path, line_count - 2)
        if data_line_2nd.find("属性继承自父类") >= 0:
            inherit_flag = "是：" + data_line_2nd[data_line_2nd.find("属性继承自父类") + 7 : data_line_2nd.find("，版本限制")]
        else:
            inherit_flag = "否"
        sheet1.write(sheet1_line, 0, data_line_1st[data_line_1st.find("属性名：") + 4 : data_line_1st.find("\t位置")])
        sheet1.write(sheet1_line, 1, data_line_1st[data_line_1st.find("接口名：") + 4 : data_line_1st.find("\t父类接口")])
        sheet1.write(sheet1_line, 2, inherit_flag)
        sheet1.write(sheet1_line, 3, data_line_1st[data_line_1st.find("文件名：") + 4 : data_line_1st.find("\t属性名")])
        sheet1.write(sheet1_line, 4, data_line_1st[data_line_1st.find("位置：") + 3 : data_line_1st.find("\t接口名")])
        sheet1.write(sheet1_line, 5, "该属性的使用不符合版本限制要求")
        if(inherit_flag.find("是") >= 0):
            sheet1.write(sheet1_line, 6, data_line_2nd[data_line_2nd.find("版本限制：[") + 6 : data_line_2nd.find(",")])
        else:
            sheet1.write(sheet1_line, 6, data_line_2nd[data_line_2nd.find("版本限制：") + 5 : data_line_2nd.find("\t")])
        #sheet1.write(sheet1_line, 7, data_line_2nd)
        sheet1_line = sheet1_line + 1
    line = property_data_file.readline()
    line_count = line_count + 1

excelTabel.save('/Users/linjunhao/Desktop/complie_opt/TraversingOutput/APICheck/PropertyAPICheck.xls')