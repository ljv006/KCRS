#coding=utf-8
from flask import Flask, render_template, request, redirect, jsonify, url_for
from getOutputSentence import *
import json
app = Flask(__name__)
app._static_folder = "/Users/longjiawei/PycharmProjects/cars/cars/static"

@app.route('/')
def index():
    return render_template('/kcrs_start.html')

@app.route('/hello', methods=['GET', 'POST']) # 按钮指向的路由
def hello(): # 这个函数可以放你要运行的代码，然后返回相应的值
    if request.method == 'GET':
        sentence = request.args.get("sentence")
        sentence_json = json.dumps({"sentence" : sentence})
        aspect_percentage = getPercentage(sentence)
        percentage_json = json.dumps(aspect_percentage)
        result_map = sort(aspect_percentage)
        ordered_json = json.dumps(result_map)
        text_result = getTextResult(aspect_percentage)
        text_result_json = json.dumps({"text_result" : text_result})
        return render_template('/kcrs_result.html',
            query_sent = sentence_json, query_percent = percentage_json,
            ordered_result = ordered_json, text_result = text_result_json)
    #return "hello"
if __name__ == '__main__':
    app.run()