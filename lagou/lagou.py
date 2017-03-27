#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import logging
import math
import random
import re
import sqlite3
import time
import uuid
from datetime import datetime

import requests

LIMIT_PER_PAGE = 30  # 访问一个页面的间隔时间

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

DB_FILE = "company.db"
DB_TABLE = "company"

totalCount = 134492
pageSize = 16


def resetJSESSIONID():
    res = requests.get("https://www.lagou.com")
    return re.search("^JSESSIONID=([0-9A-Z]{32}).*$", res.headers["Set-Cookie"]).group(1)


def getTime():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).rjust(2, "0")
    day = str(now.day).rjust(2, "0")
    hour = str(now.hour).rjust(2, "0")
    minute = str(now.minute).rjust(2, "0")
    second = str(now.second).rjust(2, "0")
    return year + month + day + hour + minute + second


def uid():
    return "".join(str(uuid.uuid4()).split("-"))


def insert(arg):
    con = sqlite3.connect(DB_FILE)
    sql = "INSERT OR REPLACE INTO '" + DB_TABLE + "' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    with con:
        cur = con.cursor()
        cur.execute(sql, arg)


def checkDatabaseTable():
    con = sqlite3.connect(DB_FILE)
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS '" + DB_TABLE + "' ('companyId' TEXT PRIMARY KEY NOT NULL, 'companyFullName' TEXT NOT NULL, 'companyShortName' TEXT NOT NULL, 'companyLogo' TEXT NOT NULL, 'city' TEXT NOT NULL, 'industryField' TEXT NOT NULL, 'companyFeatures' TEXT NOT NULL, 'financeStage' TEXT NOT NULL, 'interviewRemarkNum' TEXT NOT NULL, 'positionNum' TEXT NOT NULL, 'processRate' TEXT NOT NULL, 'approve' TEXT NOT NULL, 'countryScore' TEXT NOT NULL, 'cityScore' TEXT NOT NULL)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", datefmt="%a, %d %b %Y %H:%M:%S")
    checkDatabaseTable()
    while True:
        for num in range(1, math.ceil(totalCount / pageSize)):
            try:
                if num % 10 == 0 or num == 1:  # 每隔十次更换一下 cookie
                    cookie = "JSESSIONID=" + resetJSESSIONID() + "; user_trace_token=" + getTime() + "-" + uid()
                header = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "Origin": "https://www.lagou.com",
                    "Host": "www.lagou.com",
                    "Referer": "https://www.lagou.com",
                    "Cookie": cookie,
                }
                requestBody = {"pn": num, "first": "false", "sortField": 0, "havemark": 0}
                res = requests.post("https://www.lagou.com/gongsi/0-0-0.json", headers=header, timeout=60, data=requestBody)
                response = res.json()
                logging.info(header)
                logging.info(requestBody)
                totalCount = int(response.get("totalCount"))
                pageSize = int(response.get("pageSize"))
                for data in response.get("result"):
                    logging.info(data["companyFullName"])
                    insert((str(data["companyId"]), data["companyFullName"], data["companyShortName"], data["companyLogo"], data["city"], data["industryField"], data["companyFeatures"], data["financeStage"], str(data["interviewRemarkNum"]), str(data["positionNum"]), str(data["processRate"]), str(data["approve"]), str(data["countryScore"]), str(data["cityScore"])))
            except Exception as e:
                totalCount = 134492
                pageSize = 16
                logging.error("Post " + str(num) + " with error.")
                logging.error(e)

            time.sleep(LIMIT_PER_PAGE)
