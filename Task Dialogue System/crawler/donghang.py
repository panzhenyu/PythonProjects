import requests
import re

def getCard():
    result = open('../resource/donghang_card.txt', 'w')
    totalsize = 166
    ori_urls = []
    for i in range(totalsize):
        ori_urls.append('https://tieba.baidu.com/f?kw=中国东方航空&ie=utf-8&pn=%d' % (i*50))
    card = set([])
    prefix = 'tieba.baidu.com'
    pattern = r'<a rel="noreferrer".*?href="(/p/\d+)".*?</a>'
    for url in ori_urls:
        print("request : " + url)
        rs = requests.get(url)
        text = rs.text
        retList = re.findall(pattern, text)
        for elem in retList:
            card.add(prefix + elem)
            result.write(prefix + elem + " ")
    result.close()
    print(card)

def getComments(urls):
    pass
