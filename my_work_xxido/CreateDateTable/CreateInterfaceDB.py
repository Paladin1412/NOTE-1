#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
import os
import linecache
import re

#打开数据库连接
db = pymysql.connect("localhost","root","ljh@123456","sdkdatabase",unix_socket="/tmp/mysql.sock")
#创建游标对象
cursor = db.cursor()

#数据入库
def DataInsertIntoTable(line_list):
    if(len(line_list) == 3):
        #sql插入语句
        sql = "INSERT INTO interface_data_table(interface_name, super_interface_name, version_id) \
            VALUES ('%s', '%s', '%s') " %(line_list[0], line_list[1], line_list[2])
        try:
            #执行sql语句
            cursor.execute(sql)
            #提交到数据库执行
            db.commit()
        except:
            #如果发生错误则回滚
            db.rollback()

#读取文件，分割字符
def GetTarget(file_path):
    file = open(file_path,'r')
    line = file.readline()
    while line:
        if(line.find("\t") >= 0):
            line = line.replace("\n","")
            line_list = line.split("\t")
            DataInsertIntoTable(line_list)
        line = file.readline()

#遍历文件夹
def FileTraversing(dir_path):
    sub_paths = os.listdir(dir_path)
    for sub_path in sub_paths:
        file_path = os.path.join(dir_path, sub_path)
        if not os.path.isdir(file_path):
            if(file_path.endswith(".txt") == 1):
                print(file_path)
                GetTarget(file_path)
        else:
            FileTraversing(file_path)

if __name__ == '__main__':
    data_dir_path = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/interface"
    sql = "TRUNCATE TABLE interface_data_table"
    try:
        cursor.execute(sql)
        db.commit()
        print("interface data \n")
        FileTraversing(data_dir_path)
    except:
        db.rollback()
        print("clear error")

#关闭数据库连接与游标对象
db.close()
cursor.close()


