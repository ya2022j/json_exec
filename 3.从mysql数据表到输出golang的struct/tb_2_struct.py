#!/usr/bin/python3
"""
Convert json string to golang struct.
"""

import os, json

space = "    "
fmt = '{0}{1:25s}{2:15s}`json:"{3}"`\n'
list_fmt = '{0}{1:25s}[]{2:13s}`json:"{3}"`\n'
structs = {}


def normallize(name):
    return name.capitalize()


def conv_list(jlist, struct_name, key_name, old_key):
    """
    Convert list, we simply think that the element types in the list are the same.
    Don't handle two-dimensional or multidimensional list.
    If jlist is none, we consider it's a string list.
    """
    global space, structs
    item = jlist[0] if jlist else "string"
    if isinstance(item, str):
        structs[struct_name] += list_fmt.format(space, key_name, "string", old_key)
    elif isinstance(item, bool):
        structs[struct_name] += list_fmt.format(space, key_name, "bool", old_key)
    elif isinstance(item, int):
        structs[struct_name] += list_fmt.format(space, key_name, "int64", old_key)
    elif isinstance(item, float):
        structs[struct_name] += list_fmt.format(space, key_name, "float64", old_key)
    elif isinstance(item, list):
        pass
    elif isinstance(item, dict):
        structs[struct_name] += list_fmt.format(space, key_name, key_name, old_key)
        conv(item, key_name)
    else:
        pass

def writeinto_file(filename, data):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        f.write(data)
        f.write("\n")
    f.close()
def conv(jsonstr, struct_name):

    global structs, fmt, space
    if struct_name in structs.keys():
        return
    structs[struct_name] = "type %s struct {\n" % struct_name

    for k, v in jsonstr.items():
        new_k = "".join(list(map(normallize, k.split("_"))))
        if isinstance(v, str):
            structs[struct_name] += fmt.format(space, new_k, "string", k)
        elif isinstance(v, bool):
            structs[struct_name] += fmt.format(space, new_k, "bool", k)
        elif isinstance(v, int):
            structs[struct_name] += fmt.format(space, new_k, "int64", k)
        elif isinstance(v, float):
            structs[struct_name] += fmt.format(space, new_k, "float64", k)
        elif isinstance(v, list):
            conv_list(v, struct_name, new_k, k)
        elif isinstance(v, dict):
            structs[struct_name] += fmt.format(space, new_k, new_k, k)
            conv(v, new_k)
        else:
            pass

    structs[struct_name] += "}"


def read_file(file):
    with open(file, "r", encoding="utf-8") as f:
        content = json.load(f)

    return content[1][0]

def json_to_struct(jsonfile,topKey,gofile):
    j = read_file(jsonfile)
    while isinstance(j, list):
        j = j[0]
    conv(j,topKey)

    for k, v in structs.items():
        writeinto_file(gofile,"{}\n".format(v))

import pymysql
import json
from datetime import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

class DBToJson():
    def __init__(self,dbname):
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db=dbname,
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        self.cursor = cursor

    def exec(self):
        table_list = self.fetchAllTB()
        for single_tb in table_list:
            dt = self.get_single_dt(single_tb)
            jsonfile = single_tb+".json"
            gofile = single_tb+".go"
            self.output_jsonfile(jsonfile,dt)
            self.jsonfile_to_Struct(jsonfile,single_tb.upper(),gofile)
            self.remove_jsonfile(jsonfile)



    def fetchAllTB(self):
        # 获取mysql中所有数据库

        self.cursor.execute('SHOW TABLES')

        tablenames =  [list(x.items())[0][1] for x in self.cursor.fetchall()]

        return tablenames

# ['add_itjob', 'add_job', 'admin', 'aparttime_employee_resume', 'employee_basic_info', 'employee_login_vefify', 'firm_info', 'firm_login_vefify', 'regular_employee_resume']

    def get_single_dt(self,tablename):
        sql = 'select * from {0} limit 1'.format(tablename)
        self.cursor.execute(sql)
        dt =  self.cursor.fetchall()

        print(dt)

        return tablename,dt


    def output_jsonfile(self,filename, list_data):
        with open(filename, 'w', encoding='utf-8') as fw:
            json.dump(list_data, fw, default=str,indent=2, ensure_ascii=False)
            fw.close()


    def jsonfile_to_Struct(self,jsonfile,structname,gofile):
        if os.path.exists(jsonfile):
            json_to_struct(jsonfile,structname,gofile)

    def remove_jsonfile(self,jsonfile):

        for file in os.listdir("."):
            file_list = file.split(".")
            if len(file_list) != 1 and os.path.exists(jsonfile):
                os.remove(jsonfile)




if __name__ == "__main__":
    dbname = "mojoru_recruit"
    c = DBToJson(dbname)
    c.exec()

