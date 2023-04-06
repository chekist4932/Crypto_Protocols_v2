import logging
import json
import random
import socket
import art
import os
from myScripts.sha_ import sha_256_512
from myScripts.text_tags import Tag

my_name = "Bob"
my_user_id = 2605
protocol_flag = False
prime_mode = 0
alpha = 0
param_g = 0

lab_name = os.path.basename(os.getcwd())
final_password = b''
last_password = b''
amount_passwords = 0
users = {"Alice": 4932}
insertion_tag = "\033[36m[+]\033[0m"


def welcome():
    art.tprint(lab_name, font="chiseled")
    print(f"{Tag.blue} Host Id: {my_user_id}")
    print(f"{Tag.blue} Host Name: {my_name}\n")


def find_name(id_: int):
    for name_, val_ in users.items():
        if val_ == id_:
            return name_


def password_verification(password: bytes, iteration: int = 1):
    now_password = password
    for _ in range(iteration):
        now_password = sha_256_512(bytes_msg=now_password, size=512)
    # if sha_256_512(bytes_msg=password, size=512) == last_password:
    if now_password == last_password:
        return True
    else:
        return False


welcome()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50544))
    # 10.0.126.164
    print(f"{Tag.blue} Socket info: {serv_sock}")
    serv_sock.listen(1)

    while True:
        # Бесконечно обрабатываем входящие подключения
        client_sock, client_addr = serv_sock.accept()
        print(f'{Tag.blue} Connected with: {client_addr}.')
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
                    if protocol_flag and "Alpha" in letter.keys():
                        alpha = letter["Alpha"]
                        prime_mode = letter["PrimeMode"]
                        param_g = letter["PrimaryElement"]

                        print(f"{Tag.blue} Alpha received: {alpha}")
                        print(f"{Tag.blue} Prime number received: {prime_mode}")
                        print(f"{Tag.blue} Value G received: {param_g}")

                        param_y = random.randint(2, prime_mode - 2)
                        beta = pow(param_g, param_y, prime_mode)
                        key = pow(alpha, param_y, prime_mode)

                        print(f"{Tag.blue} Value Y generated: {param_y}")
                        print(f"{Tag.blue} Value beta generated: {beta}")
                        print(f"{Tag.green} Key generated: {key}")

                        letter = {"Beta": beta}
                        client_sock.sendall(json.dumps(letter).encode())

                    if "Final" in letter.keys():
                        final_password = bytes.fromhex(letter["Final"])
                        last_password = bytes.fromhex(letter["Final"])

                    # if "Id" in letter.keys() and letter['Id'] in users.values():
                    elif "Id" in letter.keys() and letter['Id'] in users.values():
                        name = find_name(letter['Id'])
                        print(f"{insertion_tag} User Id: {letter['Id']}")
                        print(f"{insertion_tag} Name: {name}")

                        if password_verification(password=bytes.fromhex(letter["Password"])):
                            last_password = bytes.fromhex(letter["Password"])

                            print(f"{insertion_tag} Iteration: {letter['Iteration']}")
                            print(f"{insertion_tag} Password: {letter['Password']}.")
                            print(f"{insertion_tag} Authentication passed.")

                            protocol_flag = True
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
        print(f"{Tag.blue} Close connection with: {client_addr}.\n")
        client_sock.close()
