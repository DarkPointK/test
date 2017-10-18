# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:34:33 2017
http://blog.csdn.net/marksinoberg/article/details/70809830 参考链接
http://blog.csdn.net/u013473520/article/details/51764334 生成词云
https://www.zhihu.com/question/36081767 抓取多行
@author: chuc
python3.5
"""
import requests
import json
from Crypto.Cipher import AES
import base64

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"
url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_30953009/?csrf_token="  # 要抓取不同的音乐，在这里更换30953009


def get_params(first_param):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)

    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16

    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8")
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


for i in range(1000):  # 抓取1000页
    f = i * 20
    first_param = '{rid:\"\", offset: \"' + str(f) + '\", total:\"true\", limit:\"20\", csrf_token:\"\"} '
    params = get_params(first_param);
    encSecKey = get_encSecKey();
    json_text = get_json(url, params, encSecKey)
    json_text = str(json_text, encoding="utf-8")
    json_dict = json.loads(json_text)
    for item in json_dict['comments']:
        with open('wordcomment.txt', 'a', encoding='utf-8') as fi:
            fi.writelines(item['content'] + '\n')
import jieba  # 分词

f = open('wordcomment.txt', 'r', encoding="utf-8").read()
s = {}
f = jieba.cut(f)
for w in f:
    if len(w) > 1:
        previous_count = s.get(w, 0)
        s[w] = previous_count + 1
from wordcloud import WordCloud

wordcloud = WordCloud(font_path='C:/Users/Windows/fonts/simkai.ttf').fit_words(s)

import matplotlib.pyplot as plt  # 画图

plt.imshow(wordcloud)
plt.axis("off")
plt.show()
