"""
Server流程
1.建立socket
2.绑定ip
3.接受内容
4.反馈消息
"""

import socket

def serverFunc():
    # 建立socket
    # socket.AF_INET:ipv4协议族
    # socket.SOCK_DGRAM：UDP通信
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # 绑定ip和port
    # 127.0.0.1：本机地址
    # 7852：随便指定端口号
    # 地址是tuple类型，(ip，port)
    addr = ("127.0.0.1", 7852)
    sock.bind( addr )

    # 接受对方信息
    # 等待方式为死等
    # recvfrom返回值为tuple，前一项为数据，后一项为地址
    # 参数是缓冲区大小
    data, addr = sock.recvfrom(500)

    text = data.decode()
    print(data)

    rsp = "Hello, nice to meet U."

    data = rsp.encode()
    sock.sendto(data, addr)

if __name__ == "__main__":
    import time
    while 1:
        try:
            print("Starting server >>>")
            serverFunc()
            print("Ending server >>>")
        except Exception as e:
            print(e)
        time.sleep(1)