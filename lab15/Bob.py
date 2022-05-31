import logging
import random
import json
import socket
from myScripts.gost_stribog import gost_256_512
from myScripts.sha_ import sha_256_512
from myScripts.my_rsa import RSA
from myScripts.text_tags import Tag

mod_num = 0
param_v = 0
param_x = 0
param_y = 0

users = {"Alice": 4932}
insertion_tag = "\033[36m[+]\033[0m"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50544))
    # 10.0.126.164
    print(serv_sock)
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print(f'{Tag.blue} Connected by', client_addr)
        result = b""
        count = 0
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            # print(data)

            if data == b"DataPut":
                try:
                    letter = json.loads(result.decode())
                    assert type(letter) is dict
                    if "N" in letter.keys():
                        mod_num = letter['N']
                        print(f'{Tag.green} N received: {mod_num}.')

                    if "PublicParam" in letter.keys():
                        param_v = letter["PublicParam"]
                        print(f'{Tag.green} V received: {param_v}.')

                    if "Param X" in letter.keys():
                        param_x = letter["Param X"]
                        print(f'{Tag.green} X received: {param_x}.')

                        param_c = round(random.random())
                        answer = {"Param C": param_c}
                        answer = json.dumps(answer).encode()
                        client_sock.sendall(answer)
                        print(f'{Tag.green_dark} C sent: {param_c}.')

                    if "Param Y" in letter.keys():
                        param_y = letter["Param Y"]
                        print(f'{Tag.green} Y received: {param_y}.')

                        if param_y != 0 and \
                                (param_y ** 2)%mod_num == \
                                pow(param_x * (param_v ** param_c), 1, mod_num):
                            answer_ = b"IterationSuccessful"
                        else:
                            answer_ = b"IterationNotSuccessful"
                        client_sock.sendall(answer_)
                        print(f'{Tag.green_dark} Answer sent: {answer_}.')
                except Exception as err:
                    logging.exception("DataError")
                    print(f'{Tag.red} {err}')
                    client_sock.sendall(b"DataError")

                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"{Tag.blue} Close connection with {client_addr[0]}\n")
        client_sock.close()
