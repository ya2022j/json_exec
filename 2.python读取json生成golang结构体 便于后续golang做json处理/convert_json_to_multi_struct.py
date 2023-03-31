#!/usr/bin/python3
"""
Convert json string to golang struct.
"""

import os, json

space = "    "
fmt = '{0}{1:25s}{2:15s}`json:"{3}"`\n'
list_fmt = '{0}{1:25s}[]{2:13s}`json:"{3}"`\n'
structs = {}
def writeinto_file(filename, data):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        f.write(data)
        f.write("\n")
    f.close()

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

    return content
def json_to_struct(jsonfile,topKey,gofile):
    j = read_file(jsonfile)
    while isinstance(j, list):
        j = j[0]
    conv(j,topKey)

    for k, v in structs.items():
        writeinto_file(gofile,"{}\n".format(v))

if __name__ == "__main__":
    global status
    json_to_struct("dt.json","DDD","dt.go")


