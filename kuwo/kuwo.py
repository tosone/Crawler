#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import logging
import os
import sqlite3
import time

import requests

import oss2

LIMIT_PER_SONG = 15

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
]

URL = "http://album.kuwo.cn/album/servlet/commkdtpage?flag=2&listid=2"

DB_FILE = "kuwo-moxuanriji.db"
DB_TABLE = "kuwo"


def insert(arg):
    con = sqlite3.connect(DB_FILE)
    sql = "INSERT OR REPLACE INTO '" + DB_TABLE + "' VALUES (?,?,?,?,?,?,?)"
    with con:
        cur = con.cursor()
        cur.execute(sql, arg)


def checkDatabaseTable():
    con = sqlite3.connect(DB_FILE)
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS '" + DB_TABLE + "' ('musicrid' TEXT PRIMARY KEY NOT NULL, 'name' TEXT NOT NULL, 'yr' TEXT NOT NULL, 'artist' TEXT NOT NULL, 'album' TEXT NOT NULL, 'formats' TEXT NOT NULL, 'audio_id' TEXT NOT NULL)")


def getUrl(musicrid):
    res = requests.get("http://antiserver.kuwo.cn/anti.s?rid=MUSIC_" + musicrid + "&response=url&format=mp3|mp3&type=convert_url")
    res.encoding = "UTF-8"
    return res.text


def randomHeader():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Origin": "https://www.kuwo.cn",
        "Host": "www.kuwo.cn",
        "Referer": "https://www.kuwo.cn"
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", datefmt="%a, %d %b %Y %H:%M:%S")
    checkDatabaseTable()

    while True:
        auth = oss2.Auth(os.environ.get('AccessKeyId'), os.environ.get('AccessKeySecret'))
        bucket = oss2.Bucket(auth, os.environ.get('OSS_Endpoint'), os.environ.get('OSS_Bucket'))
        res = requests.get(URL, headers=randomHeader())
        res.encoding = "UTF-8"
        total = res.json().get("total")
        logging.info("total: " + str(total))
        time.sleep(LIMIT_PER_SONG)
        res = requests.get(URL + "&rn=" + str(total), headers=randomHeader())
        res.encoding = "UTF-8"
        response = res.json()
        for music in response.get("musiclist"):
            logging.info(music.get("name"))
            insert((music.get("musicrid"), music.get("name"), music.get("yr"), music.get("artist"), music.get("album"), music.get("formats"), music.get("audio_id")))
            musicURL = getUrl(music.get("musicrid"))
            bucket.put_object(music.get("musicrid") + ".mp3", requests.get(musicURL, headers=randomHeader()))
            time.sleep(LIMIT_PER_SONG)
        time.sleep(LIMIT_PER_SONG)
