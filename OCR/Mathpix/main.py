import win32clipboard as wc
import os
import mathpix
from PIL import ImageGrab
from PIL import Image
from io import BytesIO

# 从剪贴板读取图片
im = ImageGrab.grabclipboard()

if isinstance(im, Image.Image): # 如果是图片
    imb = BytesIO()
    im.save(imb, "jpeg")
    imb.seek(0)
    idata = imb.read()
    imb.close()
    
    try:
        clip_text = mathpix.mylatex(idata)
        
    except:
        clip_text = "Mathpix latex api error"
    
else:
    clip_text = "剪切板无图片"

wc.OpenClipboard()
wc.EmptyClipboard()
wc.SetClipboardData(wc.CF_UNICODETEXT, clip_text)
wc.CloseClipboard()
