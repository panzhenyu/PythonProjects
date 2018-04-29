# coding: utf-8
import re

fp = open('baike_Banana.txt', 'r')
try:
    testString = fp.read()
finally:
    fp.close()


def find_title():
    if testString.strip():
        title = re.search('<title>(.*?)</title>', testString, re.S).group(0)
        print(title)
        return title


def find_url():
    if testString.strip():
        url = map(lambda x: 'https://baike.baidu.com/item/' + x, re.findall('href=\"/item/(.*?)\".*?>', testString, re.S))
        return url


for s in find_url():
    print(s.decode("utf-8"))
string = "哈哈adsf，【】"
s = re.findall('哈.*', string)
print(s[0])
