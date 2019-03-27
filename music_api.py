# encoding: utf-8
from flask import Flask,request
from utils import decrypt
import requests

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/',
    'User-Agent':'Mozilla/5.0 '
}

app = Flask(__name__)

@app.route("/")
def index():
    return "<a href=\"http://08c08a36.ngrok.io/api/userhome/511843075/\">测试1用户主页</a><br><br>" \
           "<a href=\"http://08c08a36.ngrok.io/comments/35448141/?offset=0&limit=100\">测试2评论接口</a>"

# 接口地址格式，eg：http://127.0.0.1:5000/api/userhome/511843075/
@app.route("/api/userhome/<userId>/")
def api_userhome(userId):
    url = "https://music.163.com/weapi/user/playlist?csrf_token="
    return requests.post(url,headers=headers,data=decrypt.getPostParams(userId=userId)).text


# 接口地址格式，eg：http://127.0.0.1:5000/api/comments/35448141/?offset=0&limit=100
@app.route("/api/comments/<songId>/")
def api_comments(songId):

    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + songId + "/?csrf_token="
    # 获取前台GET请求URL中的参数
    offset = request.args.get('offset')
    limit = request.args.get('limit')

    # 调用网易云参数解析模块，得到Dict类型参数
    params = decrypt.getPostParams(offset=offset,limit=limit)

    # 返回网易云音乐请求评论数据
    return requests.post(url=url,headers=headers,data=params).text



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000,debug=True)

