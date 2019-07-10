# -*- coding: utf-8 -*-

import io

import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import re

url = "https://baike.baidu.com"
headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Connection': 'keep-alive',
	'Host': 'baike.baidu.com',
	'Cookie': '0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'Upgrade-Insecure-Requests': '1',
}
response = requests.get('https://baike.baidu.com/item/{}'.format("北京地铁"), headers=headers, allow_redirects=True)
txt = response.content
content = txt.decode('utf-8')
pattern = re.compile(
	r'<tr><td width="204" align="center" valign="middle" colspan="1" rowspan="2"><a target=_blank href="(/item/.*?)">(.*?)</a>\s*(.*?)<')
result = re.findall(pattern, content)
print(result)

# second mod
lines={}
for i in result:
	line = list(i)
	if len(line) == 3:
		line[1] = line[1] + line[2]
	print(line[0], line[1])
	lines[line[1]]=line[0]
site={}
pattern2=re.compile(r'</td><td width="50" colspan="2" rowspan="1"><a target=_blank href="/item/.*?">([\u4e00-\u9fa5]+)</a></td>')
pattern3=re.compile(r'</tr><tr><th.*?>([\u4e00-\u9fa5]+)</th>')
partern4=re.compile(r'</tr><tr><td.*?>([\u4e00-\u9fa5]+)</td>')
for item in lines:
	print(item)
	response=requests.get(url+lines[item],headers=headers)
	content=response.content.decode('utf-8')
	sites=re.findall(pattern2,content)
	if len(sites)==0:
		sites=re.findall(pattern3,content)
		# if len(sites)==0:
		# 	sites=re.findall(partern4,content)
	site[item]=sites

for i in site:
	print(i,site[i])