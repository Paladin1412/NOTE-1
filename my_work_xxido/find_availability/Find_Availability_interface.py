import os
import linecache
import re
import functools

save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability_interface.txt"
save_file_path = open(save_name, 'w')

#匹配数据存入txt
def DataInsertIntoTxt(file_path, line_count):
    count = 0
    while count <= 3:
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
        if(line.find("interface：") >= 0):
            print(line)
            DataInsertIntoTxt(file_path, line_count)
        line = file.readline()
        line_count = line_count + 1

if __name__ == '__main__':
    data_file_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/wework_buildout/Wunguarded_availability_over9.txt"
    GetTarget(data_file_path)

save_file_path.close()