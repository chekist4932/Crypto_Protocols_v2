# PKCS 7

import socket
import json
import time
from datetime import datetime
import math


def client(send_file: dict):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 50228))
    res = b""
    package_blocks = [json.dumps(send_file).encode()[x:x + 1024] for x in range(0, len(json.dumps(send_file).encode()), 1024)]

    for block in package_blocks:
        client_sock.sendall(block)
        data = client_sock.recv(1024)
        # print(data)
        if data.decode() == str(len(package_blocks) - 1):
            client_sock.sendall(b"Data sent")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                res += data

    client_sock.close()

    return res


# with open("results/Signature 22-04-30-15-57-07.json") as f:
#     client(json.load(f))

