import logging
import re
import requests

from config import Config
from bs4 import BeautifulSoup

# soup = BeautifulSoup(open("text.html",'rb'),'lxml')

# # print(len(soup.find_all(href=re.compile("^\/song\?id=\d+$"))))
# for i in soup.find_all(href=re.compile("^\/song\?id=\d+$")):
#     print(i)
class Run(Config):
    def __init__(self):
        super(Run, self).__init__()
        self.proxy = 'http'
        self.host = 'music.163.com'
        self.main()
    def main(self):
        res = requests.get("http://music.163.com/playlist?id=648369792", headers=self.Header(self.proxy,self.host))
        # file_object = open('text.txt', 'wb') 
        # file_object.write(res.text.encode(encoding="utf-8"))
        # file_object.close()
        # print(res.text)
        soup = BeautifulSoup(res.text,'lxml')
        print(len(soup.find_all(href=re.compile("^\/song\?id=\d+$"))))
        for i in soup.find_all(href=re.compile("^\/song\?id=\d+$")):
            print(i)


if __name__ == '__main__':
    Run()