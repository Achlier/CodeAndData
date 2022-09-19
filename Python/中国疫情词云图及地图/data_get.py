import requests
from lxml import etree
import json
import re

class Get_data():
    def get_data(self):
        response = requests.get('https://voice.baidu.com/act/newpneumonia/newpneumonia')
        with open('html.txt','w') as file:
            file.write(response.text)
    def get_time(self):
        with open('html.txt', 'r') as file:
            text = file.read()
        time = re.findall('"mapLastUpdatedTime":"(.*?)"',text)[0]
        return time
    def parse_data(self):
        with open('html.txt', 'r') as file:
            text = file.read()
        html = etree.HTML(text)
        result = html.xpath('//script[@type="application/json"]/text()')
        result = result[0]
        result = json.loads(result)
        result_in = result['component'][0]['caseList']
        result_in = json.dumps(result_in)
        with open('data.json','w') as file:
            file.write(result_in)

data = Get_data()
data.get_data()
data.get_time()
data.parse_data()

'''
.:任意字符，除了\n
[]:括号中任意字符
\d:任意数字
\D:除了数字
\s:空格tab键
\S:除了空格
\w:任意单词字符，a-zA-Z0-9
\W:除了单词字符
*:前面内容重复0或多次
+:前面内容至少一次
?:前面内容0或一次
{m,n}:最少n次最多m次
^:字符串开始
$:字符串结尾
\b:字符串边界
():对内容进行分组
\A:仅匹配开头
\Z:仅匹配结尾
|:左或者右
(?p
(?p=name):引用分组
'''