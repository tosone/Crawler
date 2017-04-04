import logging
import random
from os import environ, path

import oss2
from pymongo import MongoClient

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2561.400 QQBrowser/9.6.10822.400",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.53.2561.400 QQBrowser/9.6.10822.400",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Core/1.53.2561.400 QQBrowser/9.6.10822.400)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
]


class Config(object):

    def __init__(self):
        self.MAX_LIMIT = 30
        self.MIN_LIMIT = 20

        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", datefmt="%a, %d %b %Y %H:%M:%S")

        self.MGO = MongoClient(host=environ.get("MongoHost"), port=int(environ.get("MongoPort")))[environ.get("MongoDB")]
        self.MGO.authenticate(name=environ.get("MongoUser"), password=environ.get("MongoPass"))

        AccessKeyId = environ.get('AccessKeyId')
        AccessKeySecret = environ.get('AccessKeySecret')
        OSS_Endpoint = environ.get('OSS_Endpoint')
        self.Bucket = oss2.Bucket(oss2.Auth(AccessKeyId, AccessKeySecret), OSS_Endpoint, "python-crawler")

    def Header(self, protocal, host):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Origin": protocal + "://" + host,
            "Host": host,
            "Referer": protocal + "://" + host,
        }

    def RandomLimit(self):
        return random.choice(range(self.MIN_LIMIT, self.MAX_LIMIT))

    def Collection(self, filename):
        return path.splitext(path.basename(filename))[0][2:]
