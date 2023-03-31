#! -*- coding:utf-8 -*-
import json
import os

from flask_cors import cross_origin,CORS

from flask import render_template, redirect, flash,url_for, request,Flask,send_from_directory,jsonify




app = Flask(__name__)

app.config["JSON_AS_ASCII"]= False

def read_file(file):
    with open(file,"r",encoding="utf-8") as f:
        content = json.load(f)

    return content






@app.route("/",methods=["GET"])
@cross_origin()
def all_app_info():
    ret = read_file("dt.json")
    response = jsonify(ret)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json; charset=utf-8"  #  要确保返回的内容是json
    return ret



if __name__ == '__main__':
    app.run(debug=True,host="192.168.84.184",port=8003)
