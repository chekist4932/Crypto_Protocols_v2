import random
import socket
import json
from gen_param import GenKey
import time
from datetime import datetime

secret_key = GenKey().prime_num(512)
public_key = 0
prime_p = 0
prime_q = 0
alpha = 0
t_random_param = 0
r_param = 0
s_param = 0
e_param = 0
lambda_ = 0


def mark_chek(data_dict: dict) -> int:
    global prime_p
    global prime_q
    global alpha
    global public_key
    global t_random_param
    global r_param
    global s_param
    global e_param
    global lambda_

    if data_dict["mark"] == "first":
        prime_p = data_dict["prime_p"]
        prime_q = data_dict["prime_q"]
        alpha = data_dict["alpha"]
        public_key = pow(alpha, secret_key, prime_p)
        return public_key
    elif data_dict["mark"] == "two":
        lambda_ = data_dict["lambda"]
        t_random_param = random.randint(2, prime_q-1)
        r_param = pow(alpha, t_random_param, prime_p)
        return r_param
    elif data_dict["mark"] == "three":
        e_param = data_dict["E"]
        s_param = pow(t_random_param + (secret_key * lambda_ * e_param), 1, prime_q)
        print(f"S - {s_param}")
        return s_param
    elif data_dict["mark"] == "four":
        return 1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50500))
    # 10.0.126.164
    print(serv_sock)
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print('Connected by', client_addr)
        res = b""
        count = 0
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            # print(data)
            if data == b"data put":
                data_dict = json.loads(res.decode())
                print(data_dict)
                client_sock.sendall(json.dumps(mark_chek(data_dict)).encode())
                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()
