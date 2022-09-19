import ftplib
import os
import socket

HOST = "ftp.acc.umu.se"
DIR = "Public/EFLIB/"
FILE = "README"

# 1.客户端远程连接远程主机上的FTP
try:
    f = ftplib.FTP()
    f.set_debuglevel(2)
    f.connect(HOST)
except Exception as e:
    print(e)
    exit()
print("***Connected to host {0}".format(HOST))

# 2.客户端输入用户和密码，或者匿名
try:
    f.login()
except Exception as e:
    print(e)
    exit()
print("***Logged in as 'anonymous'")

# 3.进行操作
try:
    f.cwd(DIR)
except Exception as e:
    print(e)
    exit()
print("***Changed dir to {0}".format(DIR))

try:
    #下载文件
    f.retrbinary("RETR {0}".format(FILE), open(FILE, "wb").write)
except Exception as e:
    print(e)
    exit()

f.quit()