#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import linecache
import re
import xlwt



excelTabel= xlwt.Workbook()#创建excel对象
sheet1=excelTabel.add_sheet('interface_error',cell_overwrite_ok=True)

sheet1.write(0,0,'接口名')
sheet1.write(0,1,'父类接口名')
sheet1.write(0,2,'文件名')
sheet1.write(0,3,'位置')
sheet1.write(0,4,'程序版本限制')
sheet1.write(0,5,'错误类型')
sheet1.write(0,6,'错误原因')
interface_data_file_path = "/Users/yuxingdong/TraversingOutput/APICheck/interface_check.txt"
interface_data_file = open(interface_data_file_path,'r')
line = interface_data_file.readline()
sheet1_line = 1
line_count = 1
while line:
    if(line.find("❌：该接口的使用不符合版本限制要求") >= 0):
        data_line_1st = linecache.getline(interface_data_file_path, line_count - 3)
        data_line_2nd = linecache.getline(interface_data_file_path, line_count - 2)
        data_line_3rd = linecache.getline(interface_data_file_path, line_count + 2)
        data_line_4th = linecache.getline(interface_data_file_path, line_count - 1)
        #print(data_line_1st)
        #print(data_line_2nd)
        #print(data_line_3rd)
        sheet1.write(sheet1_line, 0, data_line_2nd[data_line_2nd.find("接口名称:") + 5: data_line_2nd.find(";     父类接口名称:")])
        temp_str = data_line_2nd[data_line_2nd.find("父类接口名称:") + 7 : data_line_2nd.find("位置:")].strip()
        sheet1.write(sheet1_line, 1, temp_str[ : len(temp_str) - 1])
        sheet1.write(sheet1_line, 2, data_line_1st[data_line_1st.rfind("/") + 1 :])
        sheet1.write(sheet1_line, 3, data_line_2nd[data_line_2nd.find("位置:") + 3: data_line_2nd.find("行") + 1])
        sheet1.write(sheet1_line, 5, "该接口的使用不符合版本限制要求")
        sheet1.write(sheet1_line, 6, data_line_3rd)
        sheet1.write(sheet1_line, 4, data_line_4th[data_line_4th.find("版本限制为：") + 6 : ])
        sheet1_line = sheet1_line + 1
    if(line.find("❌：随版本的迭代，该接口的父类发生变更") >= 0):
        data_line_1st = linecache.getline(interface_data_file_path, line_count - 3)
        data_line_2nd = linecache.getline(interface_data_file_path, line_count - 2)
        data_line_3rd = linecache.getline(interface_data_file_path, line_count + 2)
        data_line_4th = linecache.getline(interface_data_file_path, line_count - 1)
        sheet1.write(sheet1_line, 0, data_line_2nd[data_line_2nd.find("接口名称:") + 5: data_line_2nd.find(";     父类接口名称:")])
        temp_str = data_line_2nd[data_line_2nd.find("父类接口名称:") + 7 : data_line_2nd.find("位置:")].strip()
        sheet1.write(sheet1_line, 1, temp_str[ : len(temp_str) - 1])
        sheet1.write(sheet1_line, 2, data_line_1st[data_line_1st.rfind("/") + 1 :])
        sheet1.write(sheet1_line, 3, data_line_2nd[data_line_2nd.find("位置:") + 3: data_line_2nd.find("行") + 1])
        sheet1.write(sheet1_line, 5, "随版本的迭代，该接口的父类发生变更")
        sheet1.write(sheet1_line, 6, data_line_3rd)
        sheet1.write(sheet1_line, 4, data_line_4th[data_line_4th.find("版本限制为：") + 6 : ])
        sheet1_line = sheet1_line + 1
    if(line.find("❌：该接口对应的父类信息出错") >= 0):
        data_line_1st = linecache.getline(interface_data_file_path, line_count - 2)
        data_line_2nd = linecache.getline(interface_data_file_path, line_count - 1)
        data_line_3rd = linecache.getline(interface_data_file_path, line_count + 2)
        #print(data_line_1st)
        #print(data_line_2nd)
        #print(data_line_3rd)
        sheet1.write(sheet1_line, 0, data_line_2nd[data_line_2nd.find("接口名称:") + 5: data_line_2nd.find(";     父类接口名称:")])
        temp_str = data_line_2nd[data_line_2nd.find("父类接口名称:") + 7 : data_line_2nd.find("位置:")].strip()
        sheet1.write(sheet1_line, 1, temp_str[ : len(temp_str) - 1])
        sheet1.write(sheet1_line, 2, data_line_1st[data_line_1st.rfind("/") + 1 :])
        sheet1.write(sheet1_line, 3, data_line_2nd[data_line_2nd.find("位置:") + 3: data_line_2nd.find("列") + 1])
        sheet1.write(sheet1_line, 5, "该接口对应的父类信息出错，请自行检查程序中的相关信息")
        sheet1.write(sheet1_line, 6, "系统接口信息表中提供的该接口的父类信息：" + data_line_3rd[data_line_3rd.find("--") + 2 : ])
        sheet1_line = sheet1_line + 1
    line = interface_data_file.readline()
    line_count = line_count + 1


sheet2=excelTabel.add_sheet('property_error',cell_overwrite_ok=True)
sheet2.write(0,0,'属性名')
sheet2.write(0,1,'类型')
sheet2.write(0,2,'接口名')
sheet2.write(0,3,'父类接口名')
sheet2.write(0,4,'文件名')
sheet2.write(0,5,'位置')
sheet2.write(0,7,'错误类型')
sheet2.write(0,8,'错误原因')
property_data_file_path = "/Users/yuxingdong/TraversingOutput/APICheck/property_check.txt"
property_data_file = open(property_data_file_path,'r')
line = property_data_file.readline()
sheet2_line = 1
line_count_2 = 1
while line:
    if line.find("❌：该属性的使用不符合版本限制要求") >= 0:
        data_line_1st = linecache.getline(property_data_file_path, line_count_2 - 4)
        data_line_2nd = linecache.getline(property_data_file_path, line_count_2 - 3)
        data_line_3rd = linecache.getline(property_data_file_path, line_count_2 - 2)
        data_line_4th = linecache.getline(property_data_file_path, line_count_2 - 1)
        if data_line_2nd.find("在对当前接口的父类接口进行检测之后") >= 0:
            data_line_1st = linecache.getline(property_data_file_path, line_count_2 - 6)
            data_line_2nd = linecache.getline(property_data_file_path, line_count_2 - 5)
        #print(data_line_1st)
        #print(data_line_2nd)
        #print(data_line_3rd)
        sheet2.write(sheet2_line, 0, data_line_2nd[data_line_2nd.find("属性名:") + 4: data_line_2nd.find(";     类型:")])
        sheet2.write(sheet2_line, 1, data_line_2nd[data_line_2nd.find("类型:") + 3: data_line_2nd.find(";     所属接口名称:")])
        sheet2.write(sheet2_line, 2, data_line_2nd[data_line_2nd.find("所属接口名称:") + 7: data_line_2nd.find(";     父类接口名称:")])
        temp_str = data_line_2nd[data_line_2nd.find("父类接口名称:") + 7: data_line_2nd.find("位置:")].strip()
        sheet2.write(sheet2_line, 3, temp_str[ : len(temp_str) - 1])
        sheet2.write(sheet2_line, 4, data_line_1st[data_line_1st.rfind("/") + 1: ])
        sheet2.write(sheet2_line, 5, data_line_2nd[data_line_2nd.find("位置:") + 3: data_line_2nd.find("列") + 1])
        sheet2.write(sheet2_line, 6, data_line_4th + "或通过if(@available())之外的方式限制版本")
        sheet2.write(sheet2_line, 7, "该接口的使用不符合版本限制要求")
        sheet2.write(sheet2_line, 8, data_line_3rd)

        sheet2_line = sheet2_line + 1
    line = property_data_file.readline()
    line_count_2 = line_count_2 + 1 

excelTabel.save('/Users/yuxingdong/TraversingOutput/APICheck/APICheck.xls')

