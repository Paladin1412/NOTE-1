#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import linecache
import re
import functools

blew_save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability_blew9.txt"
blew_save_file_path = open(blew_save_name, 'w')
over_save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability_over9.txt"
over_save_file_path = open(over_save_name, 'w')

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
    if x_len <= y_len:
        return -1
    else: 
        return 1

#匹配数据存入txt
def DataInsertIntoTxt(line, file_path, line_count):
    version = line[line.find("iOS ") + 4 : line.find("or newer")]
    version = version.strip()
    if (version_cmp(version,"10.0")) == -1:
        count = 0
        while count <= 2:
            line = linecache.getline(file_path, line_count + count)
            blew_save_file_path.write(line)
            count = count + 1
        blew_save_file_path.write("\n") 
    else:
        count = 0
        while count <= 2:
            line = linecache.getline(file_path, line_count + count)
            over_save_file_path.write(line)
            count = count + 1
        over_save_file_path.write("\n") 

#读取文件
def GetTarget(file_path):
    file = open(file_path,'r')
    line_count = 1
    line = file.readline()
    while line:
        if(line.find("is only available on") >= 0):
            DataInsertIntoTxt(line, file_path, line_count)
        line = file.readline()
        line_count = line_count + 1

if __name__ == '__main__':
    data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability.txt"
    GetTarget(data_file_path)

blew_save_file_path.close()
over_save_file_path.close()