import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase, MIMEMultipart
from email.header import Header

mail_mul = MIMEMultipart()
mail_text = MIMEText("Hello, i am Ach","plain","utf-8")
mail_mul.attach(mail_text)
header_from = Header("FROM","utf-8")
mail_text["From"] = header_from
header_sub = Header("SUB","utf-8")
mail_text["Subject"] = header_sub

from_addr = "353975811@qq.com"
from_pwd = "???"#授权码
to_addr = "???"
#SMTP服务器地址
smtp_srv = "smtp.qq.com"

with open("test.txt","rb") as f:
    s = f.read()
    #设置附件MIME和文件名
    m = MIMEText(s, "base64", "utf-8")
    m["Contect-Type"] = "application/octet-stream"
    m["Contect-Disposition"] = "attachment; filename='test.txt'"
    mail_mul.attach(m)

try:
    srv = smtplib.SMTP_SSL(smtp_srv.encode(),465)#SMTP默认端口
    srv.login(from_addr,from_pwd)
    srv.sendmail(from_addr,[to_addr],mail_text.as_string())
    srv.quit()
except Exception as e:
    print(e)
