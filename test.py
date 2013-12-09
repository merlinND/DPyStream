# -*-coding:Utf-8 -*

import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("127.0.0.1", 12002))
s.connect(("127.0.0.1", 11113))
s.send(b'GET 1\r\nLISTEN_PORT 12002\r\n\r\n')

s.close()
