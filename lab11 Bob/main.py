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
new_nonce = b""

random_param = 0


def message_processing(letter: dict, key: dict):
    global user_name
    global random_param
    E_k = bytes.fromhex(letter["E(k)"])
    nonce = bytes.fromhex(key["Nonce"])
    key_ = bytes.fromhex(key["key"])
    try:
        decrypted_data = json.loads(AES.new(key_, AES.MODE_EAX, nonce=nonce).decrypt(E_k).decode())
        if decrypted_data["Id"] in users.values():
            for key_word, val in users.items():
                if val == decrypted_data["Id"]:
                    user_name = key_word
                    break
            random_param = decrypted_data['Random param']
            print(f"[+] Authentication successful.")
            print(f"{user_name}: {decrypted_data['Message1']}")
            return True
        else:
            print(f"[+] Authentication failed.")
            return False
    except Exception:
        return False


def get_message():
    while True:
        try:
            third_message = input("Input first message:\t")
            fourth_message = input("Input second message:\t")
            # third_message = "I'm okay. How are you?"
            # fourth_message = "I'm okay too."
        except Exception:
            print("Input error.")
        else:
            return third_message, fourth_message




def gen_answer(third_message):
    global new_nonce

    passport = {"Random param": random_param, "Id": user_id, "Message3": third_message}
    data_to_encrypt = json.dumps(passport).encode()
    cipher = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX)
    new_nonce = cipher.nonce
    encrypted_text = cipher.encrypt(data_to_encrypt)
    return encrypted_text

key = {}
letter = {}


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
            if data == b"DataPut":
                data_: dict = json.loads(res.decode())
                # print(data_)
                if "key" in data_.keys():
                    key = data_
                elif "E(k)" in data_.keys():
                    letter = data_
                    answer = message_processing(letter, key)
                    print(f"{user_name}: {data_['Message2']}")
                    if answer:
                        third_message, fourth_message = get_message()
                        letter = {"Message4": fourth_message, "E(k)": gen_answer(third_message).hex(), "Nonce": new_nonce.hex()}
                        letter = json.dumps(letter).encode()
                        client_sock.sendall(letter)
                    else:
                        client_sock.sendall(b"Error")
                break
            res += data
            client_sock.sendall(str(count).encode())
            count += 1
        print(f"Close connection with {client_addr}")
        client_sock.close()

# cipher = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX)
# nonce = cipher.nonce
# passport = {"Random param": rand_num, "Id": user_id, "Text": text, "Nonce": nonce.hex()}
# message = json.dumps(passport).encode()
# encrypted_text = cipher.encrypt(message)
# decrypted_text = AES.new(bytes.fromhex(key["key"]), AES.MODE_EAX, nonce=nonce).decrypt(encrypted_text)
#
# print(f"Text - {message}")
# print(f"Encrypted - {encrypted_text}")
# print(f"Decrypted - {json.loads(decrypted_text.decode())}")
