#coding=utf8
import itchat
from itchat.content import *
import json
import urllib


def ldong():
    print('微信登入')
def edong():
    print('微信登出')
def feedback1(kw):
    urlreq =  'https://groceries.asda.com/api/items/search?keyword='+kw
    response = urllib.request.urlopen(urlreq)
    jresponse = json.load(response)
    st1=''
    for item in jresponse['items'][:10]:
        st1+=item['name']+':'+item['price']+','+item['weight']+'('+item['pricePerUOM']+')\n'
    return st1
def feedback2(kw):
    urlreq = 'https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[keyword]='+kw+'&page_number=1&page_size=10'
    response = urllib.request.urlopen(urlreq)
    jresponse = json.load(response)
    st2=''
    for item in jresponse['products']:
        st2+=item['name']+' '+str(item['retail_price']['price'])+'£'+'('+str(item['unit_price']['price'])+'£'+'/'+item['unit_price']['measure']+')\n'
    return st2

@itchat.msg_register(TEXT, isFriendChat=True)
def friendchat_reply(msg):
    if msg['Text'][0:2]=="kw":
        print(msg['Text'][3:])
        itchat.send(u'Waiting for the searching of %s'%(msg['Text'][3:]), msg['FromUserName'])
        print('Searching')
        fb1=feedback1(msg['Text'][3:])
        fb2=feedback2(msg['Text'][3:])
        print('Sending')
        itchat.send('asda\n'+fb1, msg['FromUserName'])
        itchat.send('sainsburys\n'+fb2, msg['FromUserName'])
        print('Over')
        
 
itchat.auto_login(hotReload=True,loginCallback=ldong, exitCallback=edong)
itchat.run()