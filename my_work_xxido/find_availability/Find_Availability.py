#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import linecache
import re


save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability.txt"
save_file_path = open(save_name, 'w')

#匹配数据存入txt
def DataInsertIntoTxt(file_path, line_count):
    count = 0
    while count <= 2:
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
        if(line.find("is only available on") >= 0):
            DataInsertIntoTxt(file_path, line_count)
        line = file.readline()
        line_count = line_count + 1

if __name__ == '__main__':
    data_file_path = "/Users/linjunhao/Desktop/complie_opt/备份/wework_test/Build_output.txt"
    GetTarget(data_file_path)

save_file_path.close()

