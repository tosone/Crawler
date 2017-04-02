# Crawler
Some funny crawler in python3.

### Kuwo

#### 电台栏目
  - URL: `http://album.kuwo.cn/album/servlet/commkdtpage?flag=2&listid=2&rn=20&pn=0`
  - 参数
    - `listid` 电台栏目 ID，不可省略
    - `pn` 页码，默认 0
    - `rn` 分页条数，默认 20

  - 电台栏目 ID

    |ID|栏目|ID|栏目|ID|栏目|ID|栏目|
    |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
    |1|吐小槽扒新闻|2|莫萱日记|3|爆笑糗事段子|4|柜子开了|
    |5|酷我音乐调频|6|一路向北|7|真心话大冒险|8|爱的速递站|
    |9|阳光音乐铺|10|酷我漫音坊|11|听他们说|12|听郭德纲说相声|
    |13|灵异事件簿|14|今日星座运势|15|请给我一首歌的时间|16|贵圈那些事儿|
    |17|萱草私房歌|18|每日正能量|19|历史那点事|20|放肆音乐|
    |21|微时光|22|小曹胡咧咧|23|情感热线|24|晚安蜜语|
    |25|小明和小红的日常生活|26|爆笑录音室|

#### 歌曲链接
  - URL: `http://antiserver.kuwo.cn/anti.s?rid=MUSIC_{musicid}&response=url&format=mp3|mp3&type=convert_url`
