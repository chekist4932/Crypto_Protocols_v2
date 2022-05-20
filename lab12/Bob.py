import datetime
import random
import json
import socket
from Crypto.Cipher import AES

my_name = "Bob"
users = {"Alice": 4932}
user_name = ""
user_id = 2605
nonce = b""
random_A = 0
random_B = 0
insertion_tag = "\033[36m[+]\033[0m"
key = {}


def gen_rand_numb():
    return random.randint(10000000, 99999999)


def get_message():
    while True:
        try:
            message = input(f"{insertion_tag} Input message:\t")
        except Exception:
            print(f"{insertion_tag} Input error.")
        else:
            return message


def gen_answer(message: str):
    encrypt_argument = {
        'Random_A': random_A,
        'Random_B': random_B,
        'Id': user_id,
        'Message2': message
    }
    data_to_encrypt = json.dumps(encrypt_argument).encode()
    cipher = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX)
    encrypted_text: bytes = cipher.encrypt(data_to_encrypt)
    return encrypted_text, cipher.nonce


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
    serv_sock.bind(("localhost", 50544))
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
            if data == b"DataPut":
                try:
                    data_: dict = json.loads(res.decode())
                except Exception as error:
                    print(f"{insertion_tag} Authentication failed: {error}")
                # print(data_)
                if "key" in data_.keys():
                    key = data_
                    print(f'{insertion_tag} Key received.')
                elif "E(k)" not in data_.keys():
                    random_A = data_["Random_A"]
                    print(f" - {data_['Message1']}")
                    random_B = gen_rand_numb()
                    second_message = get_message()
                    answer_, new_nonce = gen_answer(second_message)
                    second_letter = {"Message3": get_message(),
                                     "E(k)": answer_.hex(),
                                     'nonce': new_nonce.hex()}
                    letter = json.dumps(second_letter).encode()
                    client_sock.sendall(letter)
                    print(f'{insertion_tag} Answer sent.')
                elif "E(k)" in data_.keys():
                    encrypted_data = bytes.fromhex(data_["E(k)"])
                    key_ = bytes.fromhex(key["key"])
                    nonce = bytes.fromhex(data_['nonce'])
                    try:
                        decrypted_data = json.loads(
                            AES.new(key_, AES.MODE_EAX, nonce=nonce).decrypt(encrypted_data).decode())
                        if decrypted_data["Id"] in users.values():
                            for key_word, val in users.items():
                                if val == decrypted_data["Id"]:
                                    user_name = key_word
                                    break
                            if random_B == decrypted_data['Random_B'] and random_A == decrypted_data['Random_A']:
                                print(f"{insertion_tag} Authentication passed.")
                                print(f"{user_name}: {decrypted_data['Message4']}")
                                print(f"{user_name}: {data_['Message5']}")
                                client_sock.sendall(b"Authentication passed")
                        else:
                            print(f"{insertion_tag} Authentication failed.")
                    except Exception as error:
                        print(f"{insertion_tag} Authentication failed: {error}")
                        print(f"{insertion_tag} Last step.")

                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()
