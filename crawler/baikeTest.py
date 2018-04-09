import requests

num = 0
while num < 100:
    a = requests.get('https://baike.baidu.com/item/%E9%A6%99%E8%95%89/150475?fr=aladdin')
a.encoding = 'utf-8'
