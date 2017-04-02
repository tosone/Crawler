import logging
import math
import re
import time
import uuid
from config import Config
from datetime import datetime
from os import path

import requests


class Run(Config):

    def __init__(self):
        super(Run, self).__init__()
        self.collection = self.Collection(__file__)
        self.exploitUrl = 'https://www.lagou.com/gongsi/0-0-0.json'
        self.protocal = 'https'
        self.host = 'www.lagou.com'
        self.totalCount = 2000
        self.pageSize = 16
        self.key = 'companyId'
        self.main()

    def cookie(self):
        now = datetime.now()
        year = str(now.year)
        month = str(now.month).rjust(2, "0")
        day = str(now.day).rjust(2, "0")
        hour = str(now.hour).rjust(2, "0")
        minute = str(now.minute).rjust(2, "0")
        second = str(now.second).rjust(2, "0")
        try:
            res = re.search("^JSESSIONID=([0-9A-Z]{32}).*$", requests.get("https://www.lagou.com").headers["Set-Cookie"]).group(1)
        except Exception as e:
            time.sleep(self.RandomLimit())
            return self.cookie()
        return "JSESSIONID=" + res + "; user_trace_token=" + year + month + day + hour + minute + second + "-" + "".join(str(uuid.uuid4()).split("-"))

    def main(self):
        cookie = self.cookie()
        while True:
            for num in range(1, int(math.ceil(self.totalCount / self.pageSize))):
                try:
                    header = self.Header(self.protocal, self.host)
                    if num % 10 == 0:
                        cookie = self.cookie()
                    header["Cookie"] = cookie
                    requestBody = {"pn": num, "first": "false", "sortField": 0, "havemark": 0}
                    res = requests.post(self.exploitUrl, headers=header, timeout=60, data=requestBody)
                    response = res.json()
                    self.totalCount = int(response.get("totalCount"))
                    self.pageSize = int(response.get("pageSize"))
                    for data in response.get("result"):
                        logging.info(data["companyFullName"])
                        self.MGO[self.collection].find_one_and_replace({'companyId': data["companyId"]}, data, upsert=True)
                except Exception as e:
                    self.totalCount = 2000
                    self.pageSize = 16
                    logging.error("Post " + str(num) + " with error.")
                    logging.error(e)

                time.sleep(self.RandomLimit())
