# 网易云两个加密参数解析
# 调用模块需要提供两个参数
# @param offset : 偏移量
# @param limit : 数量 （请求评论的数量，最大值为100）
# return Dict类型的参数，用于网易云接口访问时提供

from Crypto.Cipher import AES
import base64
import requests

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# 获取params
def __get_params(offset=None,limit=None,userId=None):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'

    if offset!=None and limit!=None:
        comment_param = "{rid:\"\", offset:\""+str(offset)+"\", total:\"true\", limit:\""+str(limit)+"\", csrf_token:\"\"}"
        h_encText = __AES_encrypt(comment_param, first_key, iv)
        return __AES_encrypt(h_encText, second_key, iv)

    if userId != None:
        user_param = "{\"uid\":\"" + str(userId) + "\",\"wordwrap\":\"7\",\"offset\":\"0\",\"total\":\"true\",\"limit\":\"36\",\"csrf_token\":\"\"}"
        h_encText = __AES_encrypt(user_param, first_key, iv)
        return __AES_encrypt(h_encText, second_key, iv)

# encSecKey是一个定值，通用
def __get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

# 网易云加密规则
def __AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text,encoding="utf-8")
    return encrypt_text

# 返回访问需要的Post参数
def getPostParams(offset=None,limit=None,userId=None):

    if offset!=None and limit!=None:
        return {"params": __get_params(offset=offset, limit=limit), "encSecKey": __get_encSecKey()}

    if userId!=None:
        return {"params": __get_params(userId=userId), "encSecKey": __get_encSecKey()}

