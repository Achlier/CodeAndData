"""
Client流程
1.建立socket
2.发送内容
3.接受反馈内容
"""

import socket

def clientFunc():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    text = "Hello, I'm Acher."
    text = text.encode()

    sock.sendto(text, ("127.0.0.1", 7852))

    data, addr = sock.recvfrom(200)
    data = data.decode()

    print(data)

if __name__ == "__main__":

    clientFunc()