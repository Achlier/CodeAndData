import socket

def tcp_srv():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    addr = ("127.0.0.1", 8998)
    sock.bind( addr )
    sock.listen()

    while True:
        skt,addr = sock.accept()
        msg = skt.recv(500)
        msg = msg.decode()

        rst = "Received msg: {0} from {1}".format(msg, addr)
        print(rst)

        skt.send(rst.encode())
        skt.close()

if __name__ == "__main__":
        print("Starting server >>>")
        tcp_srv()