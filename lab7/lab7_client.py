# PKCS 7

import socket
import json
import time
from datetime import datetime
import math


def client(send_file: dict):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("192.168.33.129", 50500))
    # 10.0.147.102
    # 192.168.33.129
    res = b""

    dd = [json.dumps(send_file).encode()[x:x + 1024] for x in range(0, len(json.dumps(send_file).encode()), 1024)]

    for i in dd:
        client_sock.sendall(i)
        data = client_sock.recv(1024)
        # print(data)
        if data.decode() == str(len(dd) - 1):
            client_sock.sendall(b"Data sent")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                res += data

    client_sock.close()
    # print(res)
    if res == b"Error" or res == b"InDa":
        res = False
    return res


"""
with open("results/Signature 22-04-21-22-16-45.json") as f:
    sign = json.load(f)

print(client(sign))"""
