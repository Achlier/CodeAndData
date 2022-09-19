import requests
from lxml import etree
import json
import openpyxl

url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'
response = requests.get(url)
html = etree.HTML(response.text)
result = html.xpath('//script[@type="application/json"]/text()')
result = result[0]
result = json.loads(result)
result_in = result['component'][0]['caseList']
result_out = result['component'][0]['globalList']
wb = openpyxl.Workbook()
ws = wb.active
ws.title = '国内疫情'
ws.append(['地区','现有确诊','累计确诊','累计治愈','累计死亡','现有确诊增量','累计确诊增量','累计治愈增量','累计死亡增量'])
for each in result_in:
    temp_list = ([each['area'],each['curConfirm'],each['confirmed'],each['crued'],each['died'],
                each['curConfirmRelative'],each['confirmedRelative'],
                each['curedRelative'],each['diedRelative']])
    for i in range(len(temp_list)):
        if temp_list[i] == '':
            temp_list[i] = str(0)
    ws.append(temp_list)
for each in result_out:
    sheet_title = each['area']
    ws_out = wb.create_sheet(sheet_title)
    ws_out.append(['国家','现有确诊','累计确诊','累计治愈','累计死亡','累计确诊增量'])
    for country in each['subList']:
        temp_list = ([country['country'],country['curConfirm'],country['confirmed'],
                        country['crued'],country['died'],country['confirmedRelative']])
        for i in range(len(temp_list)):
            if temp_list[i] == '':
                temp_list[i] = str(0)
        ws_out.append(temp_list)
wb.save('./data.xlsx')
# 选取节点
# nodename:选取所有子节点
# /:从根节点开始读取
# //:不考虑位置选取
# .:选取当前节点
# ..:选取父级节点
# @:选取属性
# predicates
# /School/Student[1]:选第一个
# /School/Student[last()]:选最后一个
# /School/Student[last()-1]:选倒数第二个
# /School/Student[position()<3]:选前两个
# //School[@score]:选带有score属性的
# //School[@score="99"]:选分是99的
# //School[@score]/Age:选带有score属性的子节点Age
# 通配符
# ‘*’:任何元素节点
# @*:匹配任何属性节点
# node():匹配任何类型节点
# 多个路径
# //book/title | //book/author

'''
'curConfirm': '8' 现有确诊
'confirmed': '1329' 累计确诊
'crued': '1320' 累计治愈
'died': '1' 累计死亡
'relativeTime': '1618848000' 时间
'curConfirmRelative': '0' 现有确诊增量
'confirmedRelative': '0' 累计确诊增量
'curedRelative': '0' 累计治愈增量
'diedRelative': '0' 累计死亡增量
'''