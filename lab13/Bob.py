import logging
import random
import json
import socket
from source.gost_stribog import gost_256_512
from source.my_rsa import RSA

users = {"Alice": 4932}
insertion_tag = "\033[36m[+]\033[0m"
secret_key = json.load(open("secret_key.json", "r", encoding="utf-8"))

# print(f"Secret: {secret_key}")

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
                    # print(letter)
                    encrypted_argument = bytes.fromhex(letter["Argument"])
                    decrypted_argument = json.loads(RSA.decrypt(sec_key=secret_key, encrypted_msg=encrypted_argument).decode())
                    # print(decrypted_argument)
                    assert type(decrypted_argument) is dict
                except Exception:
                    # logging.exception("SerializeError")
                    client_sock.sendall(b"DataError")
                else:
                    if decrypted_argument["Id"] in users.values():
                        print(f"{insertion_tag} User Id: {decrypted_argument['Id']}")
                        hash_rand_num_z = gost_256_512(json.dumps(decrypted_argument["RandomParam"]).encode(), 512)
                        if letter["Hash"] == hash_rand_num_z:
                            print(f'{insertion_tag} Random number z: {decrypted_argument["RandomParam"]}.')
                            print(f"{insertion_tag} Hash is math.")
                            print(f"{insertion_tag} Authentication passed.")
                            client_sock.sendall(json.dumps(decrypted_argument["RandomParam"]).encode())
                        else:
                            print(f"{insertion_tag} Authentication failed.")
                    else:
                        print(f"{insertion_tag} Authentication failed.")
                break
            result += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()
