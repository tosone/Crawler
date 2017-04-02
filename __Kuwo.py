from config import Config
from os import environ
import logging
import requests
import time


class Run(Config):

    def __init__(self):
        super(Run, self).__init__()
        self.collection = self.Collection(__file__)
        self.protocal = 'http'
        self.host = 'album.kuwo.cn'
        self.exploitUrl = 'http://album.kuwo.cn/album/servlet/commkdtpage?flag=2&listid=2'
        self.total = 900
        self.key = 'musicrid'
        self.main()

    def getUrl(aelf, musicrid):
        res = requests.get('http://antiserver.kuwo.cn/anti.s?rid=MUSIC_' + musicrid + '&response=url&format=mp3|mp3&type=convert_url')
        res.encoding = "UTF-8"
        return res.text

    def main(self):
        while True:
            try:
                res = requests.get(self.exploitUrl, headers=self.Header(self.protocal, self.host))
                res.encoding = "UTF-8"
                print(self.Header(self.protocal, self.host))
                response = res.json()
                self.total = response['total']
                for music in response['musiclist']:
                    logging.info(music['name'])
                    self.MGO[self.collection].find_one_and_replace({self.key: music['musicrid']}, music, upsert=True)
                    print(self.getUrl(music['musicrid']))
                    if not self.Bucket.object_exists(music['musicrid'] + ".mp3"):
                        self.Bucket.put_object(music['musicrid'] + ".mp3", requests.get(self.getUrl(music['musicrid'])))
                    time.sleep(self.RandomLimit())
            except Exception as e:
                logging.error(e)
                time.sleep(self.RandomLimit())
