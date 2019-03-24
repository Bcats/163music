import json
import threading

import numpy as np
import requests
from script import params
import re
from pyquery import PyQuery as pq

# 获取每个歌单的地址
def getPlayList(userid):
    url = "https://music.163.com/weapi/user/playlist?csrf_token="
    # user_home = "https://music.163.com/#/user/home?id="+userid

    session = requests.session()

    r = session.post(url, headers=params.HEADER, data=params.DATA, verify=False)

    html_json = r.json()
    playlist = html_json['playlist']
    urllist = []

    for play in playlist:
        if play['userId'] == userid:
            url = "https://music.163.com/playlist?id="+str(play['id'])
            urllist.append(url)

    return urllist if(len(urllist)!=0) else None

# 获取单个歌单HTML
def getHtmlByURL(url):

    return requests.get(url, headers=params.HEADER).text

# 解析单个歌单中歌曲的Url
def parserSongUrl(play_html):
    p = pq(play_html)
    doc = p('#song-list-pre-cache').items('li a')
    songlist = []
    for item in doc:
        url = pq(item).attr('href')
        url = re.findall(r"id=(.*)",url)[0]
        songlist.append(url)

    return songlist


def getComment(uid,songid,contents,songindex):

    # beforeTime = True


    offset = 0
    time = None
    doc = None

    while offset < 30: #time==None or time>1497918743160:


        doc = getHtmlByURL(params.COMMENT_URL_PRIFIX + str(songid) + "?limit=20&offset=" + str(offset))

        comments = json.loads(doc)['comments']
        for comment in comments:

            if(time != comment['time']):
                time = comment['time']
            else:
                break
            if comment['user']['userId'] == uid:
                contents.append(comment['content'])
                if len(contents) == len(set(contents)):
                    print("")
                    print(str(offset)+" 坛宝：" + comment['content'])
            #else:

                # print(str(comment['user']['userId'])+comment['content'])
                # print(".",end='')
        print(str(songindex+1)+"线程"+" 第"+str(offset)+"页")
        offset = offset + 1
        #t.sleep(5)
    print(offset)
    return contents



if __name__ == '__main__':
     # 获取歌单URL
    urllist = getPlayList(511843075)

    count = 0
    songlist = []

     # 获取所有歌曲URL
    for url in urllist:
        play_html = getHtmlByURL(url)
        lists = parserSongUrl(play_html)
        songlist = np.r_[songlist,lists]

     # 循环获取单首歌曲评论

    threads = []
    contents = []
    songindex = 0
    while songindex < len(songlist):
        if len(threading.enumerate()) < 10:
            try:
                i = len(threading.enumerate())
                thread = threading.Thread(target=getComment,args=(511843075,songlist[songindex],contents,songindex))
                thread.setDaemon(True)
                thread.start()
                songindex = songindex + 1
            except:
                print("error:thread")

        if songindex % 15 == 0:
            print(set(contents))

    print(set(contents))
