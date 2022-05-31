import logging
import random
import json
import socket
from source.gost_stribog import gost_256_512
from source.sha_ import sha_256_512
from source.my_rsa import RSA

final_password = b''
last_password = b''
amount_passwords = 0
users = {"Alice": 4932}
insertion_tag = "\033[36m[+]\033[0m"


def find_name(id_: int):
    for name_, val_ in users.items():
        if val_ == id_:
            return name_


def password_verification(password: bytes, iteration: int = 1):
    if sha_256_512(bytes_msg=password, size=512) == last_password:
        return True
    else:
        return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50544))
    # 10.0.126.164
    print(serv_sock)
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print('Connected by', client_addr)
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
                    if "Final" in letter.keys():
                        final_password = bytes.fromhex(letter["Final"])
                        last_password = bytes.fromhex(letter["Final"])

                    if "Id" in letter.keys() and letter['Id'] in users.values():
                        name = find_name(letter['Id'])
                        print(f"{insertion_tag} User Id: {letter['Id']}")
                        print(f"{insertion_tag} Name: {name}")

                        if password_verification(password=bytes.fromhex(letter["Password"])):
                            last_password = bytes.fromhex(letter["Password"])

                            print(f"{insertion_tag} Iteration: {letter['Iteration']}")
                            print(f"{insertion_tag} Password: {letter['Password']}.")
                            print(f"{insertion_tag} Authentication passed.")

                            client_sock.sendall(b"AuthenticationPassed")

                        else:
                            print(f"{insertion_tag} Authentication failed.")
                            client_sock.sendall(b"AuthenticationFailed")

                except Exception as err:
                    logging.exception("DataError")
                    print(f'{insertion_tag} {err}')
                    client_sock.sendall(b"DataError")
                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()
