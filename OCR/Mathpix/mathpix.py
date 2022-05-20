import base64
import requests
import json

with open("apikey.json", "r") as f:
    api_key = f.read()
api_key = json.loads(api_key)

my_headers = {"app_id": api_key["app_id"],
           "app_key": api_key["app_key"],
           "Content-type": "application/json"}

service = 'https://api.mathpix.com/v3/latex'

# 从图片地址合成
def iuri_path(ipath):
    with open(ipath, "rb") as f:
        idata = f.read()
    return "data:image/jpg;base64," + base64.b64encode(idata).decode()

# 从图片合成
def iuri_bdata(idata):
    return "data:image/jpg;base64," + base64.b64encode(idata).decode()

# 发送请求
def latex(data, headers=my_headers, timeout=10):
    r = requests.post(service, data=json.dumps(data), 
                      headers=headers, timeout=timeout)
    return json.loads(r.text)
    
# 发送拥有额外设置的请求
def mylatex(idata, headers=my_headers):
    data = {"src":iuri_bdata(idata),
            "ocr":["math", "text"],
            "formats":["latex_styled"],
            "format_options":{
                "latex_styled":{
                    "transforms":["rm_spaces"]
            }}}
    r = requests.post(service, data=json.dumps(data), 
                      headers=headers, timeout=10)
    
    rd = json.loads(r.text)
    return rd["latex_styled"]

if __name__=="__main__":
    ipath = "test.jpg"
    with open(ipath, "rb") as f:
        idata = f.read()
    res_latex = mylatex(idata)
    print(res_latex)