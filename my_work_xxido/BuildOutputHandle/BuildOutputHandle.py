#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import linecache
import re


interface_save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_interface.txt"
property_save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_property_all.txt"
instance_save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/build_output_instance.txt"
interface_save_file_path = open(interface_save_name, 'w')
property_save_file_path = open(property_save_name, 'w')
instance_save_file_path = open(instance_save_name, 'w')


#匹配数据存入txt
def DataInsertIntoTxt(file_path, line_count):
    if linecache.getline(file_path, line_count).find("属性匹配") >= 0:
        save_file_path = property_save_file_path
    elif linecache.getline(file_path, line_count).find("变量匹配") >= 0:
        save_file_path = interface_save_file_path
    elif linecache.getline(file_path, line_count).find("实例匹配") >= 0:
        save_file_path = instance_save_file_path
    count = 1
    while count <= 5:
        line = linecache.getline(file_path, line_count + count)
        save_file_path.write(line)
        count = count + 1
    save_file_path.write("\n") 

#读取文件
def GetTarget(file_path):
    file = open(file_path,'r')
    line_count = 1
    line = file.readline()
    while line:
        if(line.find("——————*") >= 0):
            DataInsertIntoTxt(file_path, line_count)
        line = file.readline()
        line_count = line_count + 1

if __name__ == '__main__':
    data_file_path = "/Users/linjunhao/Desktop/complie_opt/备份/wework_test/Build_output.txt"
    GetTarget(data_file_path)

interface_save_file_path.close()
property_save_file_path.close()
instance_save_file_path.close()

